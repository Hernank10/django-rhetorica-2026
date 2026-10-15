"""Ver por que falla el test de certificaciones."""
import subprocess

BASE = r"E:\02_proyectos\django-rhetorica"

# 1. Correr SOLO el test que falla
print("=" * 75)
print("1) EL TEST SOLO")
print("=" * 75)
r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe -m pytest "
    r"core\tests\test_views_97.py::TestCertificacionesListaCompleta::test_autenticado_con_certificaciones "
    r"-v --tb=long -p no:cacheprovider",
    shell=True, cwd=BASE, capture_output=True, text=True,
)
print(r.stdout[-3000:])
print(r.stderr[-1000:] if r.stderr else "")

# 2. Ver el modelo CertificacionObtenida
print()
print("=" * 75)
print("2) EL MODELO CertificacionObtenida")
print("=" * 75)
mp = r"E:\02_proyectos\django-rhetorica\core\models.py"
with open(mp, encoding="utf-8") as f:
    c = f.read()

import re
m = re.search(r"class\s+CertificacionObtenida.*?(?=^class |\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for line in m.group(0).split("\n")[:25]:
        print(line)