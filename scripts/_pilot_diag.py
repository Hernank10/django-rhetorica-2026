"""
DIAGNOSTICO PRE-SEED PILOT - Solo lectura.
Verifica que el entorno está listo ANTES de crear 108 usuarios + 45 certificados.

NO crea ni modifica nada. Sale con código 0 si todo OK, 1 si hay bloqueos.
"""
import os, sys
from pathlib import Path
sys.path.insert(0, ".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")

OK = []
WARN = []
FAIL = []

def ok(msg):    OK.append(msg);   print(f"  [OK]   {msg}")
def warn(msg):  WARN.append(msg); print(f"  [WARN] {msg}")
def fail(msg):  FAIL.append(msg); print(f"  [FAIL] {msg}")

def header(n, title):
    print()
    print("=" * 78)
    print(f"[{n}] {title}")
    print("=" * 78)

# ══════════════════════════════════════════════════════════════════
# [1] Django setup
# ══════════════════════════════════════════════════════════════════
header(1, "Django + conexión a BD")
try:
    import django; django.setup()
    ok("django.setup() OK")
except Exception as e:
    fail(f"django.setup() falló: {e}")
    sys.exit(1)

from django.db import connection
try:
    connection.ensure_connection()
    ok("Conexión a BD OK")
except Exception as e:
    fail(f"Conexión a BD falló: {e}")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════
# [2] Modelos involucrados
# ══════════════════════════════════════════════════════════════════
header(2, "Modelos involucrados")

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()
ok(f"User: {User._meta.label}")

try:
    from core.models_lectura import CertificacionObtenida
    ok(f"CertificacionObtenida: {CertificacionObtenida._meta.label}")
except ImportError:
    try:
        from core.models import CertificacionObtenida
        ok(f"CertificacionObtenida: {CertificacionObtenida._meta.label} (desde core.models)")
    except ImportError as e:
        fail(f"CertificacionObtenida no se encuentra: {e}")
        sys.exit(1)

try:
    from core.models_lectura import Texto, TecnicaLectura
    ok("Texto y TecnicaLectura importables")
except ImportError as e:
    fail(f"Texto/TecnicaLectura no se encuentran: {e}")
    sys.exit(1)

# ProgresoTexto / ProgresoTecnicaLectura (opcional)
try:
    from core.models_lectura import ProgresoTexto, ProgresoTecnicaLectura
    ok("ProgresoTexto / ProgresoTecnicaLectura importables")
except ImportError as e:
    warn(f"ProgresoTexto / ProgresoTecnicaLectura NO importables: {e}")
    ProgresoTexto = None
    ProgresoTecnicaLectura = None

# ══════════════════════════════════════════════════════════════════
# [3] Inspección de campos de User
# ══════════════════════════════════════════════════════════════════
header(3, "Campos del modelo User")
user_fields = [f.name for f in User._meta.fields]
print(f"  {user_fields}")

for needed in ["username", "email", "password", "is_active", "is_staff", "is_superuser"]:
    if needed in user_fields or hasattr(User, needed):
        ok(f"Campo '{needed}' disponible")
    else:
        fail(f"Campo '{needed}' NO disponible")

# ══════════════════════════════════════════════════════════════════
# [4] Inspección de CertificacionObtenida (detectar campos reales)
# ══════════════════════════════════════════════════════════════════
header(4, "Campos del modelo CertificacionObtenida")
cert_fields = {f.name for f in CertificacionObtenida._meta.fields}
print(f"  {sorted(cert_fields)}")

# FK a User
user_fk = None
for f in CertificacionObtenida._meta.fields:
    if f.is_relation and f.related_model == User:
        user_fk = f.name
        break
if user_fk:
    ok(f"FK a User encontrada: '{user_fk}'")
else:
    fail("No hay FK a User en CertificacionObtenida")

# Campo de módulo
module_field = None
for fn in ["modulo", "tipo", "curso", "certificado_tipo", "nombre", "descripcion", "titulo"]:
    if fn in cert_fields:
        module_field = fn
        break
if module_field:
    ok(f"Campo módulo detectado: '{module_field}'")
else:
    warn("No hay campo obvio para el nombre del módulo (se creará sin él)")

# Campo de fecha
date_field = None
for fn in ["fecha_obtencion", "fecha_emision", "fecha_completado", "fecha", "fecha_expedicion"]:
    if fn in cert_fields:
        date_field = fn
        break
if date_field:
    ok(f"Campo fecha detectado: '{date_field}'")
else:
    warn("No hay campo obvio para la fecha")

# Campo de código
code_field = None
for fn in ["codigo", "folio", "uuid_certificado", "identificador", "codigo_certificado"]:
    if fn in cert_fields:
        code_field = fn
        break
if code_field:
    ok(f"Campo código detectado: '{code_field}'")
else:
    warn("No hay campo obvio para código (se creará sin él)")

# Campos NOT NULL sin default → riesgo en get_or_create
print()
print("  Análisis de campos obligatorios:")
riesgos = []
for f in CertificacionObtenida._meta.fields:
    if not f.blank and not f.null and not f.has_default() and not f.auto_created:
        if f.primary_key: continue
        if f.name in (user_fk, module_field, date_field, code_field): continue
        riesgos.append(f.name)

if riesgos:
    warn(f"Campos NOT NULL sin default ni valores previstos: {riesgos}")
    warn("  → el get_or_create podría fallar si no se rellenan")
else:
    ok("Todos los campos NOT NULL tienen default o están cubiertos")

# ══════════════════════════════════════════════════════════════════
# [5] Estado actual de usuarios (¿seed parcial ya ejecutado?)
# ══════════════════════════════════════════════════════════════════
header(5, "Estado actual de usuarios")

total_users = User.objects.count()
print(f"  Total usuarios en BD: {total_users}")
print(f"  Superusers:           {User.objects.filter(is_superuser=True).count()}")
print(f"  Staff:                {User.objects.filter(is_staff=True).count()}")

# Buscar *_pilot_* existentes
pilot_admins    = list(User.objects.filter(username__regex=r"^admin_pilot_\d+$"))
pilot_profs     = list(User.objects.filter(username__regex=r"^prof_pilot_\d+$"))
pilot_students  = list(User.objects.filter(username__regex=r"^est_pilot_\d+$"))
total_pilot     = len(pilot_admins) + len(pilot_profs) + len(pilot_students)

print()
print(f"  *_pilot_* existentes:  {total_pilot}")
print(f"    admin_pilot_*:       {len(pilot_admins)}  (esperado 0 o 3)")
print(f"    prof_pilot_*:        {len(pilot_profs)}   (esperado 0 o 9)")
print(f"    est_pilot_*:         {len(pilot_students)}  (esperado 0 o 96)")

if total_pilot == 0:
    ok("BD limpia de *_pilot_* (seed no ejecutado todavía)")
elif len(pilot_admins) == 3 and len(pilot_profs) == 9 and len(pilot_students) == 96:
    warn("Seed YA ejecutado (108 usuarios *_pilot_* existentes)")
    warn("  → re-ejecutar es seguro (es idempotente) pero no creará nada nuevo")
else:
    fail(f"Estado PARCIAL de seed detectado: {total_pilot}/108")
    fail("  → usuarios faltantes o extras. Considera cleanup antes de re-seed")
    print()
    print("  Usuarios *_pilot_* encontrados:")
    for u in (pilot_admins + pilot_profs + pilot_students)[:10]:
        print(f"    {u.username}")

# ¿Hay usuarios con nombres exactos ya tomados?
print()
print("  Verificación de colisión con nombres planificados:")
colisiones = []
plan = (
    [f"admin_pilot_{i:02d}" for i in range(1, 4)] +
    [f"prof_pilot_{i:02d}"  for i in range(1, 10)] +
    [f"est_pilot_{i:03d}"   for i in range(1, 97)]
)
existing_names = set(User.objects.filter(username__in=plan).values_list("username", flat=True))
if existing_names:
    colisiones = sorted(existing_names)
    if len(colisiones) == len(plan):
        warn(f"Los {len(plan)} nombres ya existen (seed idempotente, sin problema)")
    else:
        warn(f"Colisión parcial: {len(colisiones)}/{len(plan)} nombres ya existen")
        for name in colisiones[:5]:
            print(f"    - {name}")
else:
    ok("Ninguno de los 108 nombres planificados existe (creación limpia)")

# ══════════════════════════════════════════════════════════════════
# [6] Estado de certificados
# ══════════════════════════════════════════════════════════════════
header(6, "Estado actual de certificados")

total_certs = CertificacionObtenida.objects.count()
print(f"  Total certificados en BD: {total_certs}")

if total_certs == 0:
    ok("BD sin certificados (seed creará 45)")
else:
    warn(f"Ya hay {total_certs} certificados en BD (el seed puede añadir más)")

# Certificados asociados a *_pilot_*
if user_fk:
    pilot_certs = CertificacionObtenida.objects.filter(
        **{f"{user_fk}__username__regex": r"^est_pilot_\d+$"}
    ).count()
    print(f"  Certificados de *_pilot_*: {pilot_certs}  (esperado 0 o 45)")
    if pilot_certs == 45:
        warn("Los 45 certificados *_pilot_* ya existen")
    elif pilot_certs == 0:
        ok("Sin certificados *_pilot_* todavía")

# ══════════════════════════════════════════════════════════════════
# [7] Textos y técnicas (base del contenido)
# ══════════════════════════════════════════════════════════════════
header(7, "Contenido: textos y técnicas")
print(f"  Textos:   {Texto.objects.count():3d}  (esperado 36)")
print(f"  Técnicas: {TecnicaLectura.objects.count():3d}  (esperado 600)")

if Texto.objects.count() == 36:
    ok("36 textos cargados")
else:
    fail(f"Textos = {Texto.objects.count()} (esperado 36)")

if TecnicaLectura.objects.count() == 600:
    ok("600 técnicas cargadas")
else:
    warn(f"Técnicas = {TecnicaLectura.objects.count()} (esperado 600)")

# ══════════════════════════════════════════════════════════════════
# [8] Grupos de Django
# ══════════════════════════════════════════════════════════════════
header(8, "Grupos de Django")

grupos_actuales = list(Group.objects.values_list("name", flat=True))
print(f"  Grupos existentes: {grupos_actuales}")

for needed in ["Administrador", "Profesor", "Estudiante"]:
    if needed in grupos_actuales:
        ok(f"Grupo '{needed}' existe")
    else:
        warn(f"Grupo '{needed}' NO existe (se creará)")

# ══════════════════════════════════════════════════════════════════
# [9] ProgresoTexto / ProgresoTecnicaLectura (opcional)
# ══════════════════════════════════════════════════════════════════
header(9, "Modelos de progreso")

if ProgresoTexto:
    pt_fields = {f.name for f in ProgresoTexto._meta.fields}
    print(f"  ProgresoTexto fields: {sorted(pt_fields)}")
    fk_texto = next((f.name for f in ProgresoTexto._meta.fields if f.is_relation and f.related_model == Texto), None)
    if fk_texto:
        ok(f"ProgresoTexto tiene FK a Texto: '{fk_texto}'")
    else:
        warn("ProgresoTexto no tiene FK a Texto detectable")

if ProgresoTecnicaLectura:
    ptc_fields = {f.name for f in ProgresoTecnicaLectura._meta.fields}
    print(f"  ProgresoTecnicaLectura fields: {sorted(ptc_fields)}")
    fk_tec = next((f.name for f in ProgresoTecnicaLectura._meta.fields if f.is_relation and f.related_model == TecnicaLectura), None)
    if fk_tec:
        ok(f"ProgresoTecnicaLectura tiene FK a TecnicaLectura: '{fk_tec}'")
    else:
        warn("ProgresoTecnicaLectura no tiene FK a TecnicaLectura detectable")

# ══════════════════════════════════════════════════════════════════
# [10] Smoke test ligero (rutas críticas)
# ══════════════════════════════════════════════════════════════════
header(10, "Smoke test ligero")
from django.test import Client
c = Client()

rutas = [
    ("/", 200),
    ("/login/", 200),
    ("/admin/", (200, 302)),
    ("/lectura/", (200, 302)),
    ("/tecnicas/", (200, 302)),
]
for ruta, esperado in rutas:
    try:
        r = c.get(ruta)
        permitidos = esperado if isinstance(esperado, tuple) else (esperado,)
        if r.status_code in permitidos:
            ok(f"{ruta:<15} → {r.status_code}")
        else:
            fail(f"{ruta:<15} → {r.status_code} (esperado {esperado})")
    except Exception as e:
        fail(f"{ruta:<15} → EXC {e}")

# ══════════════════════════════════════════════════════════════════
# [11] Resumen y veredicto
# ══════════════════════════════════════════════════════════════════
header(11, "RESUMEN")

print()
print(f"  OK:   {len(OK)}")
print(f"  WARN: {len(WARN)}")
print(f"  FAIL: {len(FAIL)}")

if FAIL:
    print()
    print("  *** FAILURES (bloquean el seed) ***")
    for f in FAIL:
        print(f"    [FAIL] {f}")

if WARN:
    print()
    print("  *** WARNINGS (no bloquean, revisar) ***")
    for w in WARN:
        print(f"    [WARN] {w}")

print()
print("=" * 78)
if FAIL:
    print("*** VEREDICTO: NO LISTO PARA SEED ***")
    print("=" * 78)
    sys.exit(1)
else:
    print("*** VEREDICTO: LISTO PARA SEED ***")
    print("=" * 78)
    if WARN:
        print("Puedes ejecutar `_pilot_seed.py`. Revisa los WARN antes si aplica.")
    sys.exit(0)