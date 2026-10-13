from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

print("=" * 75)
print("1) VISTA leccion_form COMPLETA (core/views_profesor.py)")
print("=" * 75)
vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8", errors="replace")
m = re.search(r"def\s+leccion_form\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    # Limitar a las primeras 80 lineas
    lineas = m.group(0).split("\n")
    for l in lineas[:80]:
        print(l)
else:
    print("[!] No se encontro leccion_form")

print()
print("=" * 75)
print("2) URLs leccion_* (core/urls_profesor.py)")
print("=" * 75)
up = BASE / "core" / "urls_profesor.py"
if up.exists():
    c2 = up.read_text(encoding="utf-8", errors="replace")
    for l in c2.split("\n"):
        if "leccion" in l.lower():
            print(f"  {l.strip()}")

print()
print("=" * 75)
print("3) TODOS LOS TEMPLATES EN core/templates/core/profesor/")
print("=" * 75)
tp = BASE / "core" / "templates" / "core" / "profesor"
if tp.exists():
    for f in sorted(tp.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(BASE)}")
else:
    print("  [!] No existe la carpeta")

print()
print("=" * 75)
print("4) IMPORTS EN views_profesor.py (primeras 40 lineas)")
print("=" * 75)
for i, l in enumerate(vp.read_text(encoding="utf-8", errors="replace").split("\n")[:40], 1):
    print(f"  {i:3}: {l}")

print()
print("=" * 75)
print("5) BUSCAR TODOS LOS FORMS EN EL PROYECTO (no solo core/forms.py)")
print("=" * 75)
for py in sorted(BASE.rglob("*.py")):
    if any(x in str(py) for x in ["__pycache__", "migrations", "scripts"]):
        continue
    txt = py.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"^class\s+(\w*Form\w*)\s*\(([^)]*)\):", txt, re.MULTILINE):
        print(f"  {py.relative_to(BASE):50} -> {m.group(1)}  ({m.group(2)})")

print()
print("=" * 75)
print("6) DONDE SE DEFINE EL CAMPO 'contenido' COMO FORM FIELD")
print("=" * 75)
for py in sorted(BASE.rglob("*.py")):
    if any(x in str(py) for x in ["__pycache__", "migrations", "scripts"]):
        continue
    txt = py.read_text(encoding="utf-8", errors="replace")
    for i, l in enumerate(txt.split("\n"), 1):
        if re.search(r"contenido\s*=\s*forms\.", l):
            print(f"  {py.relative_to(BASE)}:{i}  {l.strip()}")

print()
print("=" * 75)
print("7) CAMPOS DEL MODELO Leccion")
print("=" * 75)
import sys
sys.path.insert(0, str(BASE))
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()
from core.models_cursos import Leccion
for f in Leccion._meta.get_fields():
    if hasattr(f, "name"):
        tipo = f.__class__.__name__
        blank = getattr(f, "blank", "?")
        print(f"  - {f.name:30} {tipo:20} blank={blank}")
