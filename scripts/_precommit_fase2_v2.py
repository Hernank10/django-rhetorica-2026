"""Verificacion pre-commit Fase 2 (ahora con 38 ejercicios)."""
import os, sys, subprocess
sys.path.insert(0, ".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django
django.setup()

PY = r"E:\PythonPortable_Django5\python.exe"
FAILS = []

def run(cmd, label):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = r.returncode == 0
    print(f"\n[{label}] {'OK' if ok else 'FAIL'}")
    if r.stdout.strip():
        for line in r.stdout.strip().split("\n")[:6]:
            print("  " + line)
    if not ok and r.stderr.strip():
        for line in r.stderr.strip().split("\n")[:6]:
            print("  " + line)
    if not ok:
        FAILS.append(label)

run(PY + " manage.py check 2>&1", "1. manage.py check")
run(PY + " manage.py makemigrations --check --dry-run 2>&1", "2. makemigrations --check")
run(PY + " -m pytest core/tests/ -q --tb=no 2>&1", "3. pytest (completo)")

# Client rutas
from django.test import Client
from django.contrib.auth import get_user_model
from core.models_lectura import TecnicaLectura, Texto, EjercicioLectura

print("\n[4. Client: rutas con login]")
U = get_user_model()
try:
    u = U.objects.get(username="testest044")
    c = Client()
    c.force_login(u)
    for url in ["/", "/estudiante/", "/lectura/", "/lectura/1/", "/lectura/progreso/"]:
        try:
            r = c.get(url)
            ok = r.status_code == 200
            print(f"  {url:<25} -> {r.status_code} {len(r.content)}b  {'OK' if ok else 'FAIL'}")
            if not ok:
                FAILS.append(f"Ruta {url} = {r.status_code}")
        except Exception as e:
            print(f"  {url:<25} -> EXC: {e}")
            FAILS.append(f"Ruta {url} EXC")
except Exception as e:
    print(f"  ERROR: {e}")
    FAILS.append("Client setup")

# Conteos DB
print("\n[5. Conteos DB]")
tec = TecnicaLectura.objects.count()
txt = Texto.objects.count()
ej = EjercicioLectura.objects.count()
cub = TecnicaLectura.objects.filter(id__in=EjercicioLectura.objects.values_list("tecnica_id", flat=True)).count()
print(f"  TecnicaLectura: {tec}  (esperado 38)")
print(f"  Texto: {txt}  (esperado 6)")
print(f"  EjercicioLectura: {ej}  (esperado 38)")
print(f"  Tecnicas cubiertas: {cub}/38  (esperado 37)")
if tec != 38: FAILS.append(f"TecnicaLectura={tec}")
if txt != 6: FAILS.append(f"Texto={txt}")
if ej != 38: FAILS.append(f"EjercicioLectura={ej}")
if cub != 37: FAILS.append(f"Cubiertas={cub}")

print("\n" + "=" * 70)
if FAILS:
    print(f"FAIL - {len(FAILS)} problema(s):")
    for f in FAILS:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("OK - todo listo para commit")