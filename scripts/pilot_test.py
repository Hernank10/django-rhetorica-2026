"""pilot_test.py - Prueba integral del sistema (versionado, URL admin corregida)"""
import json, os, sys
sys.path.insert(0, ".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count
from core.models_lectura import (TecnicaLectura, Texto, EjercicioLectura,
                                 RespuestaLectura, ProgresoTecnicaLectura, ProgresoTexto)
try:
    from core.models import Certificacion, CertificacionObtenida
    CERT_MODELS_OK = True
except ImportError:
    CERT_MODELS_OK = False

U = get_user_model()
FAILS, OK, WARN = [], [], []

def header(n, title):
    print(); print("=" * 78); print(f"[{n}] {title}"); print("=" * 78)

# [1] USUARIOS
header(1, "USUARIOS - verificacion")
supers = list(U.objects.filter(is_superuser=True).order_by("username"))
print(f"  Superusuarios ({len(supers)}):")
for u in supers[:10]:
    print(f"    {u.username:<20} is_staff={u.is_staff}  active={u.is_active}")
(OK if len(supers) >= 3 else FAILS).append(f"{len(supers)} superusuarios")

grp_prof = Group.objects.filter(name="Profesor").first()
if grp_prof:
    n_prof = grp_prof.user_set.count()
    print(f"\n  Profesores (grupo 'Profesor'): {n_prof}")
    (OK if n_prof >= 9 else WARN).append(f"{n_prof} profesores")
else:
    WARN.append("Grupo 'Profesor' no existe")

grp_est = Group.objects.filter(name="Estudiante").first()
if grp_est:
    n_est = grp_est.user_set.count()
    print(f"\n  Estudiantes (grupo 'Estudiante'): {n_est}")
    (OK if n_est >= 96 else WARN).append(f"{n_est} estudiantes")
else:
    WARN.append("Grupo 'Estudiante' no existe")

print(f"\n  Por prefijo: testest*={U.objects.filter(username__startswith='testest').count()}  "
      f"testprofe*={U.objects.filter(username__startswith='testprofe').count()}  "
      f"testadmin*={U.objects.filter(username__startswith='testadmin').count()}")

# [2] LOGIN
header(2, "LOGIN - verificacion de password 'Test1234!'")
n_ok = n_fail = 0
fail_users = []
for u in U.objects.filter(username__startswith="testest"):
    if u.check_password("Test1234!"):
        n_ok += 1
    else:
        n_fail += 1
        fail_users.append(u.username)
print(f"  Estudiantes testest* con 'Test1234!': {n_ok}/{n_ok + n_fail}")
if n_fail > 0:
    WARN.append(f"{n_fail} estudiantes con password distinto: {fail_users[:5]}")
else:
    OK.append(f"Los {n_ok} estudiantes pueden hacer login")

# [3] ADMIN
header(3, "RUTAS - TODOS los superusuarios")
admin_routes = ["/", "/admin/",
                "/admin/core/tecnicalectura/",   # <-- CORREGIDO
                "/admin/core/texto/", "/lectura/"]
n_admin_ok = 0
for u in supers:
    c = Client(); c.force_login(u); all_ok = True
    for url in admin_routes:
        try:
            r = c.get(url)
            if r.status_code not in (200, 302):
                all_ok = False
                FAILS.append(f"admin {u.username} {url}: {r.status_code}")
        except Exception as e:
            all_ok = False
            FAILS.append(f"admin {u.username} {url} EXC: {e}")
    if all_ok: n_admin_ok += 1
print(f"  Admins OK: {n_admin_ok}/{len(supers)}")
if n_admin_ok == len(supers):
    OK.append(f"Los {len(supers)} admins acceden a todas las rutas")

# [4] PROFESOR
header(4, "RUTAS - TODOS los profesores")
prof_routes = ["/", "/profesor/", "/profesor/estudiantes/metricas/",
               "/profesor/certificaciones/", "/lectura/"]
profesores = list(U.objects.filter(username__startswith="testprofe").order_by("username"))
if grp_prof:
    profesores += list(grp_prof.user_set.exclude(username__startswith="testprofe"))
profesores = list(set(profesores))
n_prof_ok = 0
for u in profesores:
    c = Client(); c.force_login(u); all_ok = True
    for url in prof_routes:
        try:
            r = c.get(url)
            if r.status_code not in (200, 302):
                all_ok = False
                FAILS.append(f"prof {u.username} {url}: {r.status_code}")
        except Exception as e:
            all_ok = False
            FAILS.append(f"prof {u.username} {url} EXC: {e}")
    if all_ok: n_prof_ok += 1
print(f"  Profesores OK: {n_prof_ok}/{len(profesores)}")
if n_prof_ok == len(profesores):
    OK.append(f"Los {len(profesores)} profesores acceden a todas las rutas")

# [5] ESTUDIANTE
header(5, "RUTAS - TODOS los estudiantes")
estudiantes = list(U.objects.filter(username__startswith="testest").order_by("username"))
n_est_ok = 0
for u in estudiantes:
    c = Client()
    try:
        c.force_login(u)
        r1 = c.get("/estudiante/"); r2 = c.get("/lectura/")
        if r1.status_code == 200 and r2.status_code == 200:
            n_est_ok += 1
        else:
            FAILS.append(f"est {u.username}: /estudiante/={r1.status_code}, /lectura/={r2.status_code}")
    except Exception as e:
        FAILS.append(f"est {u.username} EXC: {e}")
print(f"  Estudiantes OK: {n_est_ok}/{len(estudiantes)}")
if n_est_ok == len(estudiantes):
    OK.append(f"Los {len(estudiantes)} estudiantes acceden a /estudiante/ y /lectura/")

# [6] DETALLE muestra
header(6, "RUTAS - muestra completa (testest044)")
est_user = U.objects.filter(username="testest044").first() or (estudiantes[0] if estudiantes else None)
if est_user:
    est_routes = ["/", "/estudiante/", "/estudiante/estadisticas/",
                  "/estudiante/ranking/", "/lectura/", "/lectura/progreso/",
                  "/lectura/flashcards/", "/lectura/flashcards/?nivel=A1",
                  "/lectura/flashcards/?nivel=A2", "/lectura/flashcards/?nivel=B1"]
    c = Client(); c.force_login(est_user)
    for url in est_routes:
        try:
            r = c.get(url)
            ok = r.status_code in (200, 302)
            print(f"  {'[OK]' if ok else '[FAIL]'} {url:<40} -> {r.status_code} ({len(r.content)} bytes)")
            if not ok: FAILS.append(f"est {url}: {r.status_code}")
        except Exception as e:
            print(f"  [EXC] {url}: {e}"); FAILS.append(f"est {url} EXC: {e}")
    OK.append("Estudiante: rutas completas OK")

# [7] TEXTOS
header(7, "DETALLE DE TEXTOS - todos los niveles")
if est_user:
    c = Client(); c.force_login(est_user)
    for nivel in ["A1", "A2", "B1", "B2", "C1"]:
        texto = Texto.objects.filter(nivel_mcer=nivel).first()
        if texto:
            r = c.get(f"/lectura/{texto.id}/")
            ok = r.status_code == 200
            print(f"  {'[OK]' if ok else '[FAIL]'} [{nivel}] {texto.titulo[:40]:<40} -> {r.status_code} ({len(r.content)} bytes)")
            if not ok: FAILS.append(f"detalle {nivel} (id={texto.id}): {r.status_code}")
    OK.append("Detalle de textos: todos los niveles accesibles")

# [8] AJAX
header(8, "EVALUACION AJAX - POST /lectura/evaluar/")
if est_user:
    ej = EjercicioLectura.objects.filter(tipo="multiple_choice").first()
    if ej:
        n_antes = RespuestaLectura.objects.filter(user=est_user, ejercicio=ej).count()
        c = Client(); c.force_login(est_user)
        try:
            r = c.post("/lectura/evaluar/",
                       data=json.dumps({"ejercicio_id": ej.id, "respuesta": "B"}),
                       content_type="application/json")
            if r.status_code == 200:
                data = r.json()
                print(f"  [OK] Ejercicio {ej.id} -> 200  correcta={data.get('es_correcta')}")
                OK.append("Evaluacion AJAX: 200")
                n_despues = RespuestaLectura.objects.filter(user=est_user, ejercicio=ej).count()
                if n_despues > n_antes:
                    for _ in range(n_despues - n_antes):
                        resp = RespuestaLectura.objects.filter(user=est_user, ejercicio=ej).order_by("-fecha").first()
                        if resp: resp.delete()
                    print(f"  [OK] Cleanup: {n_despues - n_antes} respuesta(s) borrada(s)")
            else:
                print(f"  [FAIL] Ejercicio {ej.id} -> {r.status_code}"); FAILS.append(f"evaluar: {r.status_code}")
        except Exception as e:
            print(f"  [EXC] {e}"); FAILS.append(f"evaluar EXC: {e}")
    else:
        WARN.append("No hay ejercicios multiple_choice")

# [9] CERTIFICACIONES
header(9, "CERTIFICACIONES PILOTO (45 esperadas)")
if CERT_MODELS_OK:
    n_certs = Certificacion.objects.count(); n_obt = CertificacionObtenida.objects.count()
    print(f"  Disponibles: {n_certs}   Obtenidas: {n_obt}")
    (OK if n_obt >= 45 else WARN).append(f"{n_obt} certificaciones obtenidas")
    for cert in Certificacion.objects.all()[:10]:
        print(f"    - {cert.nombre[:60]}")
else:
    WARN.append("Modelos de certificaciones no disponibles")

# [10] INTEGRITY
header(10, "DATA INTEGRITY - conteos y cobertura")
print(f"  TecnicaLectura: {TecnicaLectura.objects.count()}")
print(f"  Texto:          {Texto.objects.count()}")
print(f"  Ejercicio:      {EjercicioLectura.objects.count()}")
print("\n  Tecnicas por nivel MCER:")
for nivel in ["A1", "A2", "B1", "B2", "C1", "C2"]:
    n = TecnicaLectura.objects.filter(nivel_mcer=nivel).count()
    mark = " [!]" if nivel in ("A1", "A2") and n != 100 else ""
    print(f"    {nivel}: {n:>3}{mark}")
    if nivel in ("A1", "A2") and n != 100:
        FAILS.append(f"{nivel}: {n} (esperado 100)")
print("\n  Cobertura:")
cub = set(EjercicioLectura.objects.values_list("tecnica_id", flat=True))
for nivel in ["A1", "A2", "B1"]:
    tec = TecnicaLectura.objects.filter(nivel_mcer=nivel)
    c = tec.filter(id__in=cub).count()
    pct = round(100 * c / tec.count()) if tec.count() else 0
    print(f"    {nivel}: {c}/{tec.count()} ({pct}%)")
    if nivel in ("A1", "A2") and c != tec.count():
        FAILS.append(f"{nivel}: {c}/{tec.count()} cobertura")

# [11] WARNINGS de Python/Django (captura RuntimeWarning como el de naive datetime)
header(11, "WARNINGS de Python/Django durante requests")
import warnings as _w
_url_clients = []
# Cliente PROFESOR para rutas de profesor
_prof_user = U.objects.filter(username__startswith="testprofe").first()
if not _prof_user and grp_prof:
    _prof_user = grp_prof.user_set.first()
if _prof_user:
    _c_prof = Client(); _c_prof.force_login(_prof_user)
    _url_clients.append(("/profesor/", _c_prof))
    _url_clients.append(("/profesor/estudiantes/metricas/", _c_prof))
# Cliente ESTUDIANTE para rutas de estudiante
if est_user:
    _c_est = Client(); _c_est.force_login(est_user)
    _url_clients.append(("/estudiante/", _c_est))
    _url_clients.append(("/lectura/", _c_est))
for _url, _cli in _url_clients:
    with _w.catch_warnings(record=True) as caught:
        _w.simplefilter("always")
        try:
            _cli.get(_url)
        except Exception:
            pass
    for w in caught:
        msg = str(w.message)
        if "naive datetime" in msg or "RuntimeWarning" in msg:
            print(f"  [??] {_url}: {msg[:120]}")
            WARN.append(f"RuntimeWarning en {_url}: {msg[:80]}")
# RESUMEN
print(); print("=" * 78); print("RESUMEN PILOT TEST"); print("=" * 78)
if OK:    print(f"\nOK ({len(OK)}):");   [print(f"  [OK] {o}") for o in OK]
if WARN:  print(f"\nWARN ({len(WARN)}):"); [print(f"  [??] {w}") for w in WARN]
if FAILS:
    print(f"\nFAIL ({len(FAILS)}):"); [print(f"  [!!] {f}") for f in FAILS]
    print(f"\n  *** {len(FAILS)} fallo(s) ***"); sys.exit(1)
else:
    print("\n  *** PILOT TEST OK: sistema listo para produccion ***")