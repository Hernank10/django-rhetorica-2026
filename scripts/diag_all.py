"""diag_all.py - Diagnostico unificado del proyecto (local o Render Shell).

Cubre 9 secciones:
  A. Settings y entorno
  B. Usuarios por rol
  C. Contenido MCER (tecnicas / textos / ejercicios / flashcards)
  D. Integridad (600 tecnicas, B1=100, cobertura)
  E. Admin: modelos + URLs HTTP reales
  F. Timezone: naive datetimes
  G. Dashboard: invariantes del onboarding (hero + metas)
  H. Static files
  I. Deploy readiness
  J. Veredicto

Modo: read-only excepto un usuario temporal (con cleanup garantizado).

Uso:
    python scripts/diag_all.py
    python scripts/diag_all.py --log docs/DIAG_ALL.md
"""
import os, sys, argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--log", default=None)
args, _ = parser.parse_known_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))

if "DJANGO_SETTINGS_MODULE" not in os.environ:
    for cand in ("django_retorica.settings.dev",
                 "django_retorica.settings.production",
                 "django_retorica.settings"):
        try:
            __import__(cand)
            os.environ["DJANGO_SETTINGS_MODULE"] = cand
            break
        except ImportError:
            continue

import django
django.setup()

from django.conf import settings
from django.apps import apps
from django.test import Client
from django.utils import timezone
from django.db import models as dj_models
from django.contrib.auth import get_user_model
from django.contrib import admin

U = get_user_model()
OK, WARN, FAILS, INFO = [], [], [], []

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

def safe_get(name):
    try:
        return apps.get_model("core", name)
    except LookupError:
        return None

# ═══════ A. SETTINGS ═══════
header("A", "SETTINGS Y ENTORNO")
print(f"  SETTINGS_MODULE:     {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"  DEBUG:               {settings.DEBUG}")
print(f"  ALLOWED_HOSTS:       {settings.ALLOWED_HOSTS}")
print(f"  USE_TZ:              {settings.USE_TZ}")
print(f"  TIME_ZONE:           {settings.TIME_ZONE}")
print(f"  DATABASES.engine:    {settings.DATABASES['default']['ENGINE']}")
print(f"  STATIC_ROOT:         {settings.STATIC_ROOT}")
print(f"  SECRET_KEY len:      {len(settings.SECRET_KEY)} chars")

if settings.USE_TZ:
    OK.append("USE_TZ=True")
if not settings.STATIC_ROOT:
    WARN.append("STATIC_ROOT no configurado")

# ═══════ B. USUARIOS ═══════
header("B", "USUARIOS POR ROL")
total_users = U.objects.count()
n_super = U.objects.filter(is_superuser=True).count()
print(f"  Total usuarios:  {total_users}")
print(f"  Superusuarios:   {n_super}")
print(f"\n  Por prefijo:")
for pref in ("testest", "testprofe", "testadmin", "est_pilot",
             "admin_pilot", "prof_", "est_"):
    n = U.objects.filter(username__startswith=pref).count()
    if n:
        print(f"    {pref:<12} {n}")

bad_pw = [u.username for i in range(1, 10)
          if (u := U.objects.filter(username=f"testest{i:03d}").first())
          and not u.check_password("Test1234!")]
if bad_pw:
    print(f"\n  [WARN] {len(bad_pw)} testest con password distinto: {bad_pw[:3]}...")
    WARN.append(f"{len(bad_pw)} testest con password distinto")
else:
    print(f"\n  [OK] Passwords testest OK")

if total_users == 0:
    FAILS.append("DB sin usuarios")
elif total_users < 10:
    WARN.append(f"Solo {total_users} usuarios")
else:
    OK.append(f"{total_users} usuarios")

# ═══════ C. CONTENIDO MCER ═══════
header("C", "CONTENIDO MCER")
TL = safe_get("TecnicaLectura")
TX = safe_get("Texto")
EJ = safe_get("EjercicioLectura")
FC = safe_get("Flashcard")
CURSO = safe_get("Curso")
MOD = safe_get("Modulo")
LEC = safe_get("Leccion")
EVAL = safe_get("EvaluacionCurso")
PU = safe_get("ProgresoUsuario")

fc_fields = [f.name for f in FC._meta.get_fields() if hasattr(f, "name")] if FC else []
if FC:
    print(f"  Flashcard fields: {fc_fields}")

def count_fc(nv):
    """Cuenta flashcards por nivel MCER SOLO si hay FK real (no TextField)."""
    if not FC:
        return 0
    for fname in ("tecnica", "ejercicio", "fuente"):
        if fname not in fc_fields:
            continue
        try:
            field = FC._meta.get_field(fname)
        except Exception:
            continue
        related = getattr(field, "related_model", None)
        if related is None:
            continue  # TextField/IntegerField, no joineable
        rname = related.__name__
        try:
            if rname == "TecnicaLectura":
                return FC.objects.filter(**{f"{fname}__nivel_mcer": nv}).count()
            if rname == "EjercicioLectura":
                return FC.objects.filter(**{f"{fname}__tecnica__nivel_mcer": nv}).count()
            if rname == "Texto":
                return FC.objects.filter(**{f"{fname}__nivel_mcer": nv}).count()
        except Exception:
            continue
    return "?"

niveles = ["A1", "A2", "B1", "B2", "C1", "C2"]
if TL and TX and EJ:
    print(f"\n  {'Nivel':<6} {'Tecnicas':>10} {'Textos':>8} {'Ejercicios':>12} {'Flashcards':>12}")
    for nv in niveles:
        try:
            n_t = TL.objects.filter(nivel_mcer=nv).count()
            n_x = TX.objects.filter(nivel_mcer=nv).count()
            n_e = EJ.objects.filter(tecnica__nivel_mcer=nv).count()
            n_f = count_fc(nv)
            print(f"  {nv:<6} {n_t:>10} {n_x:>8} {n_e:>12} {n_f:>12}")
        except Exception as e:
            print(f"  {nv:<6} [EXC: {e}]")
    print(f"\n  Otros modelos:")
    for name, M in [("Curso", CURSO), ("Modulo", MOD), ("Leccion", LEC),
                    ("EvaluacionCurso", EVAL), ("ProgresoUsuario", PU),
                    ("Flashcard (total)", FC)]:
        if M:
            print(f"    {name:<20} {M.objects.count()}")
else:
    print("  [FAIL] modelos MCER no disponibles")
    FAILS.append("Modelos MCER no existen")

# ═══════ D. INTEGRIDAD ═══════
header("D", "INTEGRIDAD DE DATOS")
if TL and EJ:
    total_tec = TL.objects.count()
    total_ej = EJ.objects.count()
    print(f"  Total tecnicas:   {total_tec}")
    print(f"  Total ejercicios: {total_ej}")

    if total_tec == 600:
        OK.append("TecnicaLectura.total == 600")
    else:
        FAILS.append(f"TecnicaLectura.total = {total_tec} (esperado 600)")

    b1 = TL.objects.filter(nivel_mcer="B1").count()
    if b1 == 100:
        OK.append("B1 == 100")
    else:
        FAILS.append(f"B1 = {b1} (esperado 100)")

    print(f"\n  Cobertura por nivel:")
    cub = set(EJ.objects.values_list("tecnica_id", flat=True))
    for nv in ["A1", "A2", "B1"]:
        tec = TL.objects.filter(nivel_mcer=nv)
        if tec.count() == 0:
            continue
        c = tec.filter(id__in=cub).count()
        pct = round(100 * c / tec.count())
        mark = "OK" if c == tec.count() else "FAIL"
        print(f"    [{mark}] {nv}: {c}/{tec.count()} ({pct}%)")
        if c != tec.count():
            WARN.append(f"{nv} cobertura {c}/{tec.count()}")

    from collections import Counter
    ej_por_tec = Counter(EJ.objects.values_list("tecnica_id", flat=True))
    sin_ej = [t for t in TL.objects.all() if ej_por_tec.get(t.id, 0) == 0]
    if sin_ej:
        print(f"\n  {len(sin_ej)} tecnicas SIN ejercicios")
        WARN.append(f"{len(sin_ej)} tecnicas sin ejercicios")
    else:
        OK.append("Todas las tecnicas tienen >=1 ejercicio")

# ═══════ E. ADMIN ═══════
header("E", "ADMIN - modelos y URLs HTTP reales")
reg = admin.site._registry
print(f"  Modelos registrados: {len(reg)}")

su = U.objects.filter(is_superuser=True, is_active=True).first()
if su:
    c = Client(); c.force_login(su)
    urls = ["/admin/"]
    for model in reg:
        if model._meta.app_label == "core":
            urls.append(f"/admin/core/{model._meta.model_name}/")
    print(f"\n  URLs admin (superuser {su.username}):")
    for url in urls[:12]:
        try:
            r = c.get(url)
            ok = r.status_code in (200, 302)
            print(f"    [{'OK' if ok else 'FAIL'}] {url:<45} -> {r.status_code}")
            if not ok:
                FAILS.append(f"admin {url} -> {r.status_code}")
        except Exception as e:
            print(f"    [EXC] {url}: {e}")
            FAILS.append(f"admin {url} EXC: {e}")
else:
    WARN.append("Sin superusuario para admin URLs")

# ═══════ F. TIMEZONE ═══════
header("F", "TIMEZONE - naive datetimes")
def count_naive(M, field_name):
    try:
        field = M._meta.get_field(field_name)
    except Exception:
        return None
    if not isinstance(field, dj_models.DateTimeField):
        return None
    try:
        n = 0
        for val in M.objects.exclude(**{f"{field_name}__isnull": True}).values_list(field_name, flat=True):
            if val and timezone.is_naive(val):
                n += 1
        return n
    except Exception:
        return None

total_naive = 0
for M, campos in [
    (safe_get("ProgresoUsuario"), ["completado_en", "ultima_actividad"]),
    (safe_get("RespuestaLectura"), ["fecha"]),
    (safe_get("Respuesta"), ["fecha"]),
    (safe_get("CertificacionObtenida"), ["fecha_obtencion"]),
]:
    if not M:
        continue
    for f in campos:
        n = count_naive(M, f)
        if n is None:
            continue
        if n > 0:
            print(f"  [WARN] {M.__name__}.{f}: {n} naive")
            total_naive += n
            WARN.append(f"{M.__name__}.{f}: {n} naive")
        else:
            print(f"  [OK]   {M.__name__}.{f}: 0 naive")

if total_naive == 0:
    OK.append("Sin naive datetimes")

# ═══════ G. DASHBOARD ═══════
header("G", "DASHBOARD - invariantes del onboarding")
u_temp = None
try:
    u_temp = U.objects.create_user(username="__diag_all_temp__", password="x")
    c = Client(); c.force_login(u_temp)
    r = c.get("/estudiante/")
    html = r.content.decode("utf-8", errors="replace")
    hero = "Empieza tu recorrido MCER" in html
    print(f"  __diag_all_temp__ (0 cursos): HTTP={r.status_code} hero={hero}")
    if not hero:
        FAILS.append("hero CTA NO aparece con 0 cursos")
    else:
        OK.append("hero CTA visible con 0 cursos")
finally:
    if u_temp:
        try:
            u_temp.delete()
            print("  [OK] temp user borrado")
        except Exception as e:
            print(f"  [WARN] no se pudo borrar temp user: {e}")

u_pilot = U.objects.filter(username="est_pilot_001").first()
if u_pilot:
    c = Client(); c.force_login(u_pilot)
    r = c.get("/estudiante/")
    html = r.content.decode("utf-8", errors="replace")
    hero_no = "Empieza tu recorrido MCER" not in html
    metas = "Meta próxima:" in html
    print(f"  est_pilot_001: hero_oculto={hero_no} metas={metas}")
    if not hero_no:
        FAILS.append("hero aparece con cursos > 0")
    if not metas:
        WARN.append("metas NO aparecen con progreso")
    else:
        OK.append("metas visibles con progreso")

# ═══════ H. STATIC ═══════
header("H", "STATIC FILES")
if settings.STATIC_ROOT:
    sr = Path(settings.STATIC_ROOT)
    if sr.exists():
        n = sum(1 for _ in sr.rglob("*") if _.is_file())
        print(f"  STATIC_ROOT: {sr}")
        print(f"  Archivos:    {n}")
        if n == 0:
            FAILS.append("STATIC_ROOT vacio")
        else:
            OK.append(f"STATIC_ROOT con {n} archivos")
    else:
        print(f"  [WARN] STATIC_ROOT no existe: {sr}")
        if not settings.DEBUG:
            FAILS.append("STATIC_ROOT no existe (falta collectstatic)")
        else:
            WARN.append("STATIC_ROOT no existe (ok en DEBUG)")

# ═══════ I. DEPLOY READINESS ═══════
header("I", "DEPLOY READINESS")
# Nota: FAILs aqui son solo info (checklist para prod), no bloquean
deploy_checks = [
    ("DEBUG=False", not settings.DEBUG),
    ("ALLOWED_HOSTS poblado", bool(settings.ALLOWED_HOSTS)),
    ("STATIC_ROOT configurado", bool(settings.STATIC_ROOT)),
    ("SECRET_KEY > 50 chars", len(settings.SECRET_KEY) > 50),
    ("DB con datos", total_users > 0),
    ("600 tecnicas", (TL.objects.count() == 600) if TL else False),
    ("B1 == 100", (TL.objects.filter(nivel_mcer="B1").count() == 100) if TL else False),
]
for label, ok in deploy_checks:
    mark = "OK" if ok else ("FAIL" if not settings.DEBUG else "WARN")
    print(f"  [{mark}] {label}")

# ═══════ J. VEREDICTO ═══════
header("J", "VEREDICTO FINAL")
print(f"\n  OK:    {len(OK)}")
for o in OK:    print(f"    [OK]   {o}")
if INFO:
    print(f"\n  INFO:  {len(INFO)}")
    for i in INFO: print(f"    [INFO] {i}")
print(f"\n  WARN:  {len(WARN)}")
for w in WARN:  print(f"    [??]   {w}")
print(f"\n  FAILS: {len(FAILS)}")
for f in FAILS: print(f"    [!!]   {f}")

print()
exit_code = 0 if not FAILS else 1
if FAILS:
    print(f"  *** {len(FAILS)} fallo(s) — revisar arriba ***")
else:
    print("  *** Sin fallos bloqueantes. Deploy apto. ***")
    print("  WARNs esperados en local: DEBUG=True, STATIC_ROOT inexistente, SECRET_KEY corta.")
    print("  En Render (DEBUG=False, SECRET_KEY larga, staticfiles/ poblado) desaparecen.")

if args.log:
    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "OK:    {}\nWARN:  {}\nFAILS: {}\n\n".format(len(OK), len(WARN), len(FAILS)) +
        "\n".join(f"[OK]   {o}" for o in OK) + "\n\n" +
        "\n".join(f"[??]   {w}" for w in WARN) + "\n\n" +
        "\n".join(f"[!!]   {f}" for f in FAILS),
        encoding="utf-8",
    )
    print(f"\n  [OK] log guardado en {log_path}")

sys.exit(exit_code)