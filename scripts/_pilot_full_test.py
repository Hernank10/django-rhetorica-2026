"""
PILOT FULL TEST - Pipeline completo:
  diag -> seed usuarios -> seed grupos -> seed certificados -> seed progreso -> verify -> E2E

MODE:
  - "full"        (default) : ejecuta todo
  - "dry-run"               : muestra plan sin tocar BD
  - "verify-only"           : solo verifica estado actual
  - "cleanup"               : borra *_pilot_* y certificados asociados
"""
MODE = "full"
PASSWORD = "Test1234!"

import os, sys, re, secrets
from datetime import date
from pathlib import Path
sys.path.insert(0, ".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.test import Client

User = get_user_model()

# â”€â”€ Imports defensivos â”€â”€
try:
    from core.models_lectura import (
        CertificacionObtenida, Certificacion,
        Texto, TecnicaLectura, ProgresoTexto,
    )
except ImportError:
    from core.models import CertificacionObtenida, Certificacion
    from core.models_lectura import Texto, TecnicaLectura, ProgresoTexto

# â”€â”€ DetecciÃ³n de campos reales â”€â”€
CERT_FIELDS = {f.name for f in CertificacionObtenida._meta.fields}

def find_field(*candidates):
    return next((fn for fn in candidates if fn in CERT_FIELDS), None)

FK_USER       = next((f.name for f in CertificacionObtenida._meta.fields
                      if f.is_relation and f.related_model == User), None)
FK_CERTIF     = next((f.name for f in CertificacionObtenida._meta.fields
                      if f.is_relation and f.related_model == Certificacion), None)
F_DATE        = find_field("fecha_obtenida", "fecha_obtencion", "fecha_emision", "fecha_completado")
F_CODE        = find_field("codigo_verificacion", "codigo", "folio", "uuid_certificado")
F_URL         = find_field("url_verificacion", "url", "link")

# â”€â”€ Sets esperados â”€â”€
EXPECTED_ADMINS   = [f"admin_pilot_{i:02d}" for i in range(1, 4)]
EXPECTED_PROFS    = [f"prof_pilot_{i:02d}"  for i in range(1, 10)]
EXPECTED_STUDENTS = [f"est_pilot_{i:03d}"   for i in range(1, 97)]
EXPECTED_CERT_STU = EXPECTED_STUDENTS[:45]

# â”€â”€ Contadores â”€â”€
OK, WARN, FAIL = [], [], []
def ok(m):   OK.append(m);   print(f"  [OK]   {m}")
def warn(m): WARN.append(m); print(f"  [WARN] {m}")
def fail(m): FAIL.append(m); print(f"  [FAIL] {m}")

def header(n, title):
    print(); print("=" * 78); print(f"[{n}] {title}"); print("=" * 78)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FASE 0: Resumen del modo
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
header(0, f"PILOT FULL TEST - MODE: {MODE}")
print(f"  FK User:       {FK_USER or 'NO DETECTADA'}")
print(f"  FK Certificacion: {FK_CERTIF or 'â€”'}")
print(f"  Campo fecha:   {F_DATE or 'â€”'}")
print(f"  Campo cÃ³digo:  {F_CODE or 'â€”'}")
print(f"  Campo URL:     {F_URL or 'â€”'}")

if not FK_USER:
    fail("Sin FK CertificacionObtenidaâ†’User, no se puede continuar")
    sys.exit(1)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# MODO cleanup
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
if MODE == "cleanup":
    header(1, "CLEANUP")
    with transaction.atomic():
        qs = User.objects.filter(username__regex=r"^(admin|prof|est)_pilot_")
        n = qs.count()
        print(f"  {n} usuarios *_pilot_* a borrar")
        if n:
            qs.delete()
        print(f"  [OK] {n} usuarios borrados (certificados CASCADE)")
    sys.exit(0)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# MODO dry-run
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
if MODE == "dry-run":
    header(1, "DRY-RUN (nada se modifica)")
    print("  CrearÃ­a:")
    print(f"    - {len(EXPECTED_ADMINS)} admins")
    print(f"    - {len(EXPECTED_PROFS)} profesores")
    print(f"    - {len(EXPECTED_STUDENTS)} estudiantes")
    print(f"    - {len(EXPECTED_CERT_STU)} certificados")
    print(f"    - hasta {len(EXPECTED_CERT_STU) * 3} registros de progreso")
    sys.exit(0)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FASE 1: Pre-flight
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
header(1, "Pre-flight")

n_textos = Texto.objects.count()
n_tecnicas = TecnicaLectura.objects.count()
print(f"  Textos:    {n_textos} (esperado 36)")
print(f"  TÃ©cnicas:  {n_tecnicas} (esperado 600)")

if n_textos == 36:  ok("36 textos")
else:               fail(f"Textos={n_textos}")

if n_tecnicas == 600: ok("600 tÃ©cnicas")
else:                  warn(f"TÃ©cnicas={n_tecnicas}")

# Estado pilot actual
n_pilot = User.objects.filter(username__regex=r"^(admin|prof|est)_pilot_").count()
print(f"  *_pilot_* actuales: {n_pilot}")

if MODE == "verify-only" or n_pilot >= 108:
    print("  â†’ Modo verify: se saltan las fases de seed")

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FASE 2-6: Seed
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
if MODE == "full":
    with transaction.atomic():
        # â”€â”€ 2. CatÃ¡logo Certificacion â”€â”€
        header(2, "CatÃ¡logo Certificacion")
        cert_catalog = None
        try:
            cert_catalog, created = Certificacion.objects.get_or_create(
                nombre="Lectura + Flashcards",
                defaults={"descripcion": "MÃ³dulo de lectura y flashcards completado"}
            )
            print(f"  [{'CREADO' if created else 'EXISTE'}] Certificacion: '{cert_catalog.nombre}' (id={cert_catalog.id})")
        except Exception as e:
            warn(f"No se pudo crear catÃ¡logo Certificacion: {e}")
            # Fallback: usar la primera disponible
            cert_catalog = Certificacion.objects.first()
            if cert_catalog:
                print(f"  [FALLBACK] Usando Certificacion existente: '{cert_catalog}'")

        # â”€â”€ 3. Grupos â”€â”€
        header(3, "Grupos Django")
        groups = {}
        for name in ["Administrador", "Profesor", "Estudiante"]:
            g, created = Group.objects.get_or_create(name=name)
            groups[name] = g
            print(f"  [{'CREADO' if created else 'EXISTE'}] {name}")

        # â”€â”€ 4. Admins â”€â”€
        header(4, "Admins (3)")
        admins = []
        for i, name in enumerate(EXPECTED_ADMINS, 1):
            email = f"admin{i:02d}@pilot.local"
            u, created = User.objects.get_or_create(username=name, defaults={"email": email})
            u.email = email
            u.is_active = True
            u.is_staff = True
            u.is_superuser = True
            u.set_password(PASSWORD)
            u.save()
            u.groups.add(groups["Administrador"])
            admins.append(u)
            print(f"  [{'CREADO' if created else 'EXISTE'}] {name}")

        # â”€â”€ 5. Profesores â”€â”€
        header(5, "Profesores (9)")
        profs = []
        for i, name in enumerate(EXPECTED_PROFS, 1):
            email = f"prof{i:02d}@pilot.local"
            u, created = User.objects.get_or_create(username=name, defaults={"email": email})
            u.email = email
            u.is_active = True
            u.is_staff = True
            u.is_superuser = False
            u.set_password(PASSWORD)
            u.save()
            u.groups.add(groups["Profesor"])
            profs.append(u)
            print(f"  [{'CREADO' if created else 'EXISTE'}] {name}")

        # â”€â”€ 6. Estudiantes â”€â”€
        header(6, "Estudiantes (96)")
        students = []
        for i, name in enumerate(EXPECTED_STUDENTS, 1):
            email = f"est{i:03d}@pilot.local"
            u, created = User.objects.get_or_create(username=name, defaults={"email": email})
            u.email = email
            u.is_active = True
            u.is_staff = False
            u.is_superuser = False
            u.set_password(PASSWORD)
            u.save()
            u.groups.add(groups["Estudiante"])
            students.append(u)
            if i % 20 == 0 or i == 96:
                print(f"  [OK] {i}/96")

        # â”€â”€ 7. Certificados â”€â”€
        header(7, "Certificados (45)")
        cert_students = [s for s in students if s.username in EXPECTED_CERT_STU]
        n_certs_created = 0
        n_certs_existing = 0
        n_certs_failed = 0

        for u in cert_students:
            data = {FK_USER: u}
            if FK_CERTIF and cert_catalog:
                data[FK_CERTIF] = cert_catalog
            if F_DATE:
                data[F_DATE] = date.today()
            if F_CODE:
                data[F_CODE] = f"PILOT-{u.id:04d}-{secrets.token_hex(4).upper()}"
            if F_URL:
                data[F_URL] = f"https://rhetorica.local/verify/{u.id:04d}"

            try:
                cert, created = CertificacionObtenida.objects.get_or_create(
                    **{FK_USER: u}, defaults=data
                )
                if created: n_certs_created += 1
                else:        n_certs_existing += 1
            except Exception as e:
                n_certs_failed += 1
                if n_certs_failed <= 3:
                    print(f"  [FAIL] {u.username}: {e}")

        print(f"  [OK] Creados:     {n_certs_created}")
        print(f"  [OK] Ya existÃ­an: {n_certs_existing}")
        if n_certs_failed:
            fail(f"Certificados fallidos: {n_certs_failed}")

        # â”€â”€ 8. ProgresoTexto (3 textos por estudiante certificado) â”€â”€
        header(8, "ProgresoTexto (opcional)")
        pt_fields = {f.name for f in ProgresoTexto._meta.fields}
        fk_texto = next((f.name for f in ProgresoTexto._meta.fields
                         if f.is_relation and f.related_model == Texto), None)
        fk_user_pt = next((f.name for f in ProgresoTexto._meta.fields
                           if f.is_relation and f.related_model == User), None)

        if fk_texto and fk_user_pt and "completado" in pt_fields:
            textos = list(Texto.objects.all()[:3])
            n_prog_created = 0
            for u in cert_students:
                for t in textos:
                    data = {fk_user_pt: u, fk_texto: t}
                    if "completado" in pt_fields:  data["completado"] = True
                    if "completado_en" in pt_fields: data["completado_en"] = date.today()
                    if "ejercicios_correctos" in pt_fields: data["ejercicios_correctos"] = 5
                    if "ejercicios_totales" in pt_fields: data["ejercicios_totales"] = 5
                    try:
                        _, created = ProgresoTexto.objects.get_or_create(
                            **{fk_user_pt: u, fk_texto: t}, defaults=data
                        )
                        if created: n_prog_created += 1
                    except Exception:
                        pass
            print(f"  [OK] ProgresoTextos creados: {n_prog_created}")
        else:
            warn("ProgresoTexto sin estructura compatible (se omite)")

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FASE 9: VerificaciÃ³n
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
header(9, "VerificaciÃ³n")

admins_db   = list(User.objects.filter(username__in=EXPECTED_ADMINS))
profs_db    = list(User.objects.filter(username__in=EXPECTED_PROFS))
students_db = list(User.objects.filter(username__in=EXPECTED_STUDENTS))

print(f"  Admins:       {len(admins_db)}/3")
print(f"  Profesores:   {len(profs_db)}/9")
print(f"  Estudiantes:  {len(students_db)}/96")

if len(admins_db) == 3: ok("3 admins")
else: fail(f"Admins: {len(admins_db)}/3")

if len(profs_db) == 9: ok("9 profesores")
else: fail(f"Profesores: {len(profs_db)}/9")

if len(students_db) == 96: ok("96 estudiantes")
else: fail(f"Estudiantes: {len(students_db)}/96")

# Flags
bad_admins = [u.username for u in admins_db if not (u.is_staff and u.is_superuser and u.is_active)]
bad_profs  = [u.username for u in profs_db if not (u.is_staff and not u.is_superuser and u.is_active)]
bad_stus   = [u.username for u in students_db if (u.is_staff or u.is_superuser or not u.is_active)]

if not bad_admins: ok("Flags admins OK (staff+superuser+active)")
else: fail(f"Admins con flags raros: {bad_admins[:3]}")

if not bad_profs:  ok("Flags profesores OK (staff+active)")
else: fail(f"Profesores con flags raros: {bad_profs[:3]}")

if not bad_stus:   ok("Flags estudiantes OK")
else: fail(f"Estudiantes con flags raros: {bad_stus[:3]}")

# Grupos
for gname, users in [("Administrador", admins_db), ("Profesor", profs_db), ("Estudiante", students_db)]:
    g = Group.objects.filter(name=gname).first()
    if not g:
        fail(f"Grupo '{gname}' no existe")
        continue
    in_group = sum(1 for u in users if u.groups.filter(name=gname).exists())
    if in_group == len(users):
        ok(f"Todos los '{gname}' en grupo ({in_group}/{len(users)})")
    else:
        fail(f"'{gname}': {in_group}/{len(users)} en grupo")

# Certificados
certs_qs = CertificacionObtenida.objects.filter(**{f"{FK_USER}__username__in": EXPECTED_CERT_STU})
n_certs = certs_qs.count()
print(f"  Certificados *_pilot_*: {n_certs}/45")
if n_certs == 45: ok("45 certificados")
else: fail(f"Certificados: {n_certs}/45")

if F_CODE:
    codigos = list(certs_qs.values_list(F_CODE, flat=True))
    if len(codigos) == len(set(codigos)): ok(f"CÃ³digos Ãºnicos ({len(codigos)})")
    else: fail("CÃ³digos duplicados")

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FASE 10: E2E test
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
header(10, "E2E test (login + navegaciÃ³n + permisos)")

def login_and_test(username, expected_admin_access):
    c = Client()
    if not c.login(username=username, password=PASSWORD):
        return False, "login falla", None

    # Rutas comunes
    r1 = c.get("/")
    r2 = c.get("/lectura/")
    r3 = c.get("/tecnicas/")

    # Admin
    r_admin = c.get("/admin/")

    resultado = {
        "home": r1.status_code,
        "lectura": r2.status_code,
        "tecnicas": r3.status_code,
        "admin": r_admin.status_code,
    }
    admin_ok = (r_admin.status_code in (200, 302)) if expected_admin_access else (r_admin.status_code in (302, 403, 404))
    return admin_ok, resultado, None

# Admin
if admins_db:
    u = admins_db[0]
    admin_ok, results, err = login_and_test(u.username, expected_admin_access=True)
    if err:
        fail(f"Admin '{u.username}': {err}")
    else:
        print(f"  Admin '{u.username}': {results}")
        if admin_ok: ok("Admin accede a /admin/ correctamente")
        else:        fail("Admin NO accede a /admin/")

# Profesor
if profs_db:
    u = profs_db[0]
    admin_ok, results, err = login_and_test(u.username, expected_admin_access=True)
    if err:
        fail(f"Profesor '{u.username}': {err}")
    else:
        print(f"  Profesor '{u.username}': {results}")
        if admin_ok: ok("Profesor accede a /admin/ (staff)")
        else:        warn("Profesor no accede a /admin/")

# Estudiante
if students_db:
    u = students_db[0]
    admin_ok, results, err = login_and_test(u.username, expected_admin_access=False)
    if err:
        fail(f"Estudiante '{u.username}': {err}")
    else:
        print(f"  Estudiante '{u.username}': {results}")
        if admin_ok: ok("Estudiante bloqueado en /admin/")
        else:        fail("Estudiante NO bloqueado en /admin/")

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FASE 11: Resumen + reporte
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
header(11, "RESUMEN")

print(f"\n  OK:   {len(OK)}")
print(f"  WARN: {len(WARN)}")
print(f"  FAIL: {len(FAIL)}")

if FAIL:
    print("\n  *** FAILURES ***")
    for f in FAIL: print(f"    [FAIL] {f}")

if WARN:
    print("\n  *** WARNINGS ***")
    for w in WARN: print(f"    [WARN] {w}")

print()
print("=" * 78)
if FAIL:
    print("*** VEREDICTO: ROJO ***")
    verdict = "ðŸ”´ ROJO"
elif WARN:
    print("*** VEREDICTO: ÃMBAR ***")
    verdict = "ðŸŸ¡ ÃMBAR"
else:
    print("*** VEREDICTO: VERDE - Pilot listo ***")
    verdict = "ðŸŸ¢ VERDE"
print("=" * 78)

# â”€â”€ Guardar reporte â”€â”€
try:
    lines = [f"# Pilot Full Test - {date.today().isoformat()}\n\n"]
    lines.append(f"**Veredicto:** `{verdict}`\n\n")
    lines.append(f"- OK: {len(OK)}\n- WARN: {len(WARN)}\n- FAIL: {len(FAIL)}\n\n")
    lines.append(f"## Estado\n\n")
    lines.append(f"- Admins: {len(admins_db)}/3\n")
    lines.append(f"- Profesores: {len(profs_db)}/9\n")
    lines.append(f"- Estudiantes: {len(students_db)}/96\n")
    lines.append(f"- Certificados: {CertificacionObtenida.objects.filter(**{f'{FK_USER}__username__in': EXPECTED_CERT_STU}).count()}/45\n\n")

    if FAIL:
        lines.append("## FAILURES\n\n")
        for f in FAIL: lines.append(f"- âŒ {f}\n")
        lines.append("\n")
    if WARN:
        lines.append("## WARNINGS\n\n")
        for w in WARN: lines.append(f"- âš ï¸ {w}\n")
        lines.append("\n")
    if OK:
        lines.append("## OK\n\n")
        for o in OK: lines.append(f"- âœ… {o}\n")

    out = Path("docs/PILOT_FULL_TEST.md")
    out.parent.mkdir(exist_ok=True)
    out.write_text("".join(lines), encoding="utf-8")
    print(f"[OK] Reporte: {out}")
except Exception as e:
    print(f"[WARN] No se guardÃ³ reporte: {e}")

sys.exit(0 if not FAIL else 1)
