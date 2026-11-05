"""
VERIFICACION POST-SEED PILOT - Solo lectura.
Comprueba que los 108 usuarios + 45 certificados están correctos.

- Veredicto final: VERDE (todo OK), AMBAR (avisos), ROJO (fallos)
- Guarda reporte en docs/PILOT_VERIFICATION.md
"""
import os, sys, re
from pathlib import Path
from datetime import datetime
sys.path.insert(0, ".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client

User = get_user_model()

try:
    from core.models_lectura import CertificacionObtenida
except ImportError:
    from core.models import CertificacionObtenida

# ── Contadores ──
OK, WARN, FAIL = [], [], []
def ok(m):   OK.append(m);   print(f"  [OK]   {m}")
def warn(m): WARN.append(m); print(f"  [WARN] {m}")
def fail(m): FAIL.append(m); print(f"  [FAIL] {m}")

def header(n, title):
    print(); print("=" * 78); print(f"[{n}] {title}"); print("=" * 78)

def safe_first(qs):
    try:    return qs.first()
    except Exception: return None

# ── Detección de FK en CertificacionObtenida ──
user_fk = None
for f in CertificacionObtenida._meta.fields:
    if f.is_relation and f.related_model == User:
        user_fk = f.name; break

cert_fields = {f.name for f in CertificacionObtenida._meta.fields}
module_field = next((fn for fn in ["modulo", "tipo", "curso", "nombre", "descripcion", "titulo"] if fn in cert_fields), None)
date_field   = next((fn for fn in ["fecha_obtencion", "fecha_emision", "fecha_completado", "fecha", "fecha_expedicion"] if fn in cert_fields), None)
code_field   = next((fn for fn in ["codigo", "folio", "uuid_certificado", "identificador", "codigo_certificado"] if fn in cert_fields), None)

# ── Sets esperados ──
EXPECTED_ADMINS   = {f"admin_pilot_{i:02d}" for i in range(1, 4)}
EXPECTED_PROFS    = {f"prof_pilot_{i:02d}"  for i in range(1, 10)}
EXPECTED_STUDENTS = {f"est_pilot_{i:03d}"   for i in range(1, 97)}
EXPECTED_CERT_STU = {f"est_pilot_{i:03d}"   for i in range(1, 46)}  # 45 primeros

# ══════════════════════════════════════════════════════════════════
header(1, "Modelos y FK detectados")
print(f"  CertificacionObtenida FK→User:  {user_fk or 'NO ENCONTRADA'}")
print(f"  Campo módulo:  {module_field or '—'}")
print(f"  Campo fecha:   {date_field or '—'}")
print(f"  Campo código:  {code_field or '—'}")
if user_fk:
    ok(f"FK CertificacionObtenida→User: '{user_fk}'")
else:
    fail("No se encontró FK de CertificacionObtenida a User")

# ══════════════════════════════════════════════════════════════════
header(2, "Existencia de usuarios por rol")

admins_db   = list(User.objects.filter(username__in=EXPECTED_ADMINS).order_by("username"))
profs_db    = list(User.objects.filter(username__in=EXPECTED_PROFS).order_by("username"))
students_db = list(User.objects.filter(username__in=EXPECTED_STUDENTS).order_by("username"))

print(f"  Admins:       {len(admins_db):3d} / 3")
print(f"  Profesores:   {len(profs_db):3d} / 9")
print(f"  Estudiantes:  {len(students_db):3d} / 96")

if len(admins_db) == 3:     ok("3 administradores presentes")
else:                       fail(f"Administradores: {len(admins_db)}/3")

if len(profs_db) == 9:      ok("9 profesores presentes")
else:                       fail(f"Profesores: {len(profs_db)}/9")

if len(students_db) == 96:  ok("96 estudiantes presentes")
else:                       fail(f"Estudiantes: {len(students_db)}/96")

# ── Detectar faltantes / extras ──
missing_admins   = EXPECTED_ADMINS   - {u.username for u in admins_db}
missing_profs    = EXPECTED_PROFS    - {u.username for u in profs_db}
missing_students = EXPECTED_STUDENTS - {u.username for u in students_db}

if missing_admins:
    warn(f"Admins faltantes: {sorted(missing_admins)}")
if missing_profs:
    warn(f"Profesores faltantes: {sorted(missing_profs)}")
if missing_students:
    warn(f"Estudiantes faltantes: {sorted(missing_students)[:5]}" +
         (f" (+{len(missing_students)-5})" if len(missing_students) > 5 else ""))

# ══════════════════════════════════════════════════════════════════
header(3, "Flags por rol (is_staff / is_superuser / is_active)")

# Admins: staff + superuser + active
admins_bad = [u.username for u in admins_db if not (u.is_staff and u.is_superuser and u.is_active)]
if not admins_bad:  ok("Todos los admins: is_staff=True, is_superuser=True, is_active=True")
else:               fail(f"Admins con flags incorrectos: {admins_bad}")

# Profesores: staff + NO superuser + active
profs_bad = [u.username for u in profs_db if not (u.is_staff and not u.is_superuser and u.is_active)]
if not profs_bad:   ok("Todos los profesores: is_staff=True, is_superuser=False, is_active=True")
else:               fail(f"Profesores con flags incorrectos: {profs_bad}")

# Estudiantes: NO staff + NO superuser + active
students_bad = [u.username for u in students_db if (u.is_staff or u.is_superuser or not u.is_active)]
if not students_bad: ok("Todos los estudiantes: is_staff=False, is_superuser=False, is_active=True")
else:                fail(f"Estudiantes con flags incorrectos: {students_bad[:5]}")

# ══════════════════════════════════════════════════════════════════
header(4, "Grupos de Django y membresías")

grupos_ok = True
for gname in ["Administrador", "Profesor", "Estudiante"]:
    g = Group.objects.filter(name=gname).first()
    if not g:
        fail(f"Grupo '{gname}' NO existe"); grupos_ok = False
        continue
    members = g.user_set.filter(username__regex=r"^(admin|prof|est)_pilot_\d+$").count()
    expected = {"Administrador": 3, "Profesor": 9, "Estudiante": 96}[gname]
    if members == expected:
        ok(f"Grupo '{gname}': {members} miembros *_pilot_* (esperado {expected})")
    else:
        warn(f"Grupo '{gname}': {members} miembros (esperado {expected})")

# Verificación bidireccional: cada admin debe estar en grupo Administrador, etc.
def check_group_membership(users, expected_group, label):
    g = Group.objects.filter(name=expected_group).first()
    if not g: return
    bad = [u.username for u in users if not u.groups.filter(name=expected_group).exists()]
    if not bad: ok(f"Todos los {label} están en el grupo '{expected_group}'")
    else:       fail(f"{label} sin grupo '{expected_group}': {bad[:5]}")

check_group_membership(admins_db,   "Administrador", "admins")
check_group_membership(profs_db,    "Profesor",      "profesores")
check_group_membership(students_db, "Estudiante",    "estudiantes")

# ══════════════════════════════════════════════════════════════════
header(5, "Certificados")

if not user_fk:
    fail("Sin FK CertificacionObtenida→User, no se pueden verificar certificados")
else:
    certs_qs = CertificacionObtenida.objects.filter(**{f"{user_fk}__username__regex": r"^est_pilot_\d+$"})
    n_certs = certs_qs.count()
    print(f"  Certificados *_pilot_*: {n_certs} / 45")

    if n_certs == 45:  ok("45 certificados presentes")
    else:              fail(f"Certificados: {n_certs}/45")

    # ¿Cada estudiante certificado tiene exactamente 1?
    students_with_cert = set(
        certs_qs.values_list(f"{user_fk}__username", flat=True)
    )
    missing_certs = EXPECTED_CERT_STU - students_with_cert
    extra_certs   = students_with_cert - EXPECTED_CERT_STU

    if not missing_certs:
        ok("Todos los 45 estudiantes certificados tienen certificado")
    else:
        fail(f"Estudiantes esperados sin certificado: {sorted(missing_certs)[:5]}")

    if extra_certs:
        warn(f"Estudiantes con certificado inesperado: {sorted(extra_certs)[:5]}")

    # Módulo correcto
    if module_field:
        mod_values = set(certs_qs.values_list(module_field, flat=True))
        print(f"  Valores de '{module_field}': {mod_values}")
        if any("Lectura" in str(v) for v in mod_values):
            ok("Módulo contiene 'Lectura'")
        else:
            warn(f"El campo '{module_field}' no contiene 'Lectura + Flashcards'")

    # Fecha presente
    if date_field:
        sin_fecha = certs_qs.filter(**{f"{date_field}__isnull": True}).count()
        if sin_fecha == 0:  ok(f"Todos los certificados tienen '{date_field}'")
        else:               warn(f"{sin_fecha} certificados sin '{date_field}'")

    # Código único
    if code_field:
        codigos = list(certs_qs.values_list(code_field, flat=True))
        if len(codigos) == len(set(codigos)):
            ok(f"Códigos únicos en '{code_field}'")
        else:
            fail(f"Códigos duplicados en '{code_field}'")

# ══════════════════════════════════════════════════════════════════
header(6, "Login y permisos por rol")

PASSWORD = "Test1234!"

def try_login(username):
    c = Client()
    try:
        return c.login(username=username, password=PASSWORD)
    except Exception:
        return False

# Login de un admin
if admins_db:
    u = admins_db[0]
    if try_login(u.username):
        ok(f"Login admin '{u.username}' OK")
        c = Client(); c.login(username=u.username, password=PASSWORD)
        r = c.get("/admin/")
        if r.status_code in (200, 302):
            ok(f"Admin accede a /admin/ → {r.status_code}")
        else:
            fail(f"Admin NO accede a /admin/ → {r.status_code}")
    else:
        fail(f"Login admin '{u.username}' FALLA (¿password correcta?)")

# Login de un profesor
if profs_db:
    u = profs_db[0]
    if try_login(u.username):
        ok(f"Login profesor '{u.username}' OK")
        c = Client(); c.login(username=u.username, password=PASSWORD)
        r = c.get("/admin/")
        if r.status_code in (200, 302):
            ok(f"Profesor accede a /admin/ → {r.status_code}")
        else:
            warn(f"Profesor NO accede a /admin/ → {r.status_code}")
    else:
        fail(f"Login profesor '{u.username}' FALLA")

# Login de un estudiante
if students_db:
    u = students_db[0]
    if try_login(u.username):
        ok(f"Login estudiante '{u.username}' OK")
        c = Client(); c.login(username=u.username, password=PASSWORD)
        # Estudiante NO debe poder acceder a /admin/
        r = c.get("/admin/")
        if r.status_code in (302, 403, 404):
            ok(f"Estudiante BLOQUEADO en /admin/ → {r.status_code}")
        else:
            fail(f"Estudiante NO bloqueado en /admin/ → {r.status_code}")
    else:
        fail(f"Login estudiante '{u.username}' FALLA")

# ══════════════════════════════════════════════════════════════════
header(7, "Passwords comunes")

# Verificar que TODOS los *_pilot_* usan la misma password
def password_ok(username):
    c = Client()
    try:
        return c.login(username=username, password=PASSWORD)
    except Exception:
        return False

# Sample de 5 admins + 9 profs + 10 students (no todos para no tardar)
sample = [u.username for u in admins_db] + \
         [u.username for u in profs_db] + \
         [u.username for u in students_db[:10]]

pwd_fail = [name for name in sample if not password_ok(name)]
if not pwd_fail:
    ok(f"Password '{PASSWORD}' OK en los {len(sample)} usuarios muestreados")
else:
    fail(f"Password '{PASSWORD}' NO funciona en: {pwd_fail[:5]}")

# ══════════════════════════════════════════════════════════════════
header(8, "Datos personales (opcionales)")

# Emails no vacíos
no_email_admins = [u.username for u in admins_db if not u.email]
no_email_profs  = [u.username for u in profs_db if not u.email]
no_email_stus   = [u.username for u in students_db if not u.email]

if not no_email_admins and not no_email_profs and not no_email_stus:
    ok("Todos tienen email")
else:
    if no_email_admins: warn(f"Admins sin email: {no_email_admins}")
    if no_email_profs:  warn(f"Profesores sin email: {no_email_profs[:5]}")
    if no_email_stus:   warn(f"Estudiantes sin email: {no_email_stus[:5]}")

# ══════════════════════════════════════════════════════════════════
header(9, "Resumen global de BD")

from core.models_lectura import Texto, TecnicaLectura
try:
    from core.models_lectura import ProgresoTexto, ProgresoTecnicaLectura
    n_prog_t = ProgresoTexto.objects.count()
    n_prog_tec = ProgresoTecnicaLectura.objects.count()
except Exception:
    n_prog_t, n_prog_tec = "—", "—"

print(f"  Total usuarios:         {User.objects.count()}")
print(f"  Total certificados:     {CertificacionObtenida.objects.count()}")
print(f"  Total textos:           {Texto.objects.count()}")
print(f"  Total técnicas:         {TecnicaLectura.objects.count()}")
print(f"  ProgresoTextos:         {n_prog_t}")
print(f"  ProgresoTecnicas:       {n_prog_tec}")

# ══════════════════════════════════════════════════════════════════
header(10, "RESUMEN")

print()
print(f"  OK:   {len(OK)}")
print(f"  WARN: {len(WARN)}")
print(f"  FAIL: {len(FAIL)}")

if FAIL:
    print()
    print("  *** FAILURES ***")
    for f in FAIL: print(f"    [FAIL] {f}")

if WARN:
    print()
    print("  *** WARNINGS ***")
    for w in WARN: print(f"    [WARN] {w}")

# ── Veredicto ──
print()
print("=" * 78)
if FAIL:
    print("*** VEREDICTO: ROJO - hay fallos que arreglar ***")
    verdict = "ROJO"
elif WARN:
    print("*** VEREDICTO: AMBAR - todo creado pero con avisos ***")
    verdict = "AMBAR"
else:
    print("*** VEREDICTO: VERDE - pilot listo ***")
    verdict = "VERDE"
print("=" * 78)

# ══════════════════════════════════════════════════════════════════
# Guardar reporte
# ══════════════════════════════════════════════════════════════════
try:
    lines = [f"# Verificación del Pilot - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
    lines.append(f"**Veredicto:** `{verdict}`\n\n")
    lines.append(f"- OK: {len(OK)}\n")
    lines.append(f"- WARN: {len(WARN)}\n")
    lines.append(f"- FAIL: {len(FAIL)}\n\n---\n\n")

    lines.append("## Usuarios\n\n")
    lines.append(f"- Admins: {len(admins_db)}/3\n")
    lines.append(f"- Profesores: {len(profs_db)}/9\n")
    lines.append(f"- Estudiantes: {len(students_db)}/96\n\n")
    lines.append("## Certificados\n\n")
    lines.append(f"- Total *_pilot_*: {CertificacionObtenida.objects.count()}\n\n")

    if FAIL:
        lines.append("## FAILURES\n\n")
        for f in FAIL: lines.append(f"- ❌ {f}\n")
        lines.append("\n")
    if WARN:
        lines.append("## WARNINGS\n\n")
        for w in WARN: lines.append(f"- ⚠️ {w}\n")
        lines.append("\n")
    if OK:
        lines.append("## OK\n\n")
        for o in OK: lines.append(f"- ✅ {o}\n")

    out = Path("docs/PILOT_VERIFICATION.md")
    out.parent.mkdir(exist_ok=True)
    out.write_text("".join(lines), encoding="utf-8")
    print(f"[OK] Reporte guardado en: {out}")
except Exception as e:
    print(f"[WARN] No se pudo guardar reporte: {e}")

sys.exit(0 if not FAIL else 1)