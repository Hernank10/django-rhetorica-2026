"""Diagnostico rapido de los 4 tests que fallan."""
import subprocess
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


def run(cmd):
    r = subprocess.run(cmd, shell=True, cwd=str(BASE), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


print("=" * 75)
print("1) TESTS QUE FALLAN (detalle)")
print("=" * 75)

code, out, err = run(
    r'E:\PythonPortable_Django5\python.exe -m pytest core\tests\test_views_principal.py::TestLoginLogout core\tests\test_views_principal.py::TestPerfil core\tests\test_urls_templates.py -v --tb=short --no-header -p no:cacheprovider'
)
print(out[:6000])
if err.strip():
    print("STDERR:", err[:2000])