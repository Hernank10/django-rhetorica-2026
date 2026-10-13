from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

print("=" * 75)
print("VISTA ver_evaluacion COMPLETA")
print("=" * 75)
p = BASE / "core" / "views_cursos_completo.py"
c = p.read_text(encoding="utf-8")
m = re.search(r"def\s+ver_evaluacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for l in m.group(0).split("\n")[:80]:
        print(l)

print()
print("=" * 75)
print("TEMPLATE evaluacion_detalle.html - Lineas 1-80")
print("=" * 75)
t = BASE / "core" / "templates" / "core" / "cursos" / "evaluacion_detalle.html"
if t.exists():
    for i, l in enumerate(t.read_text(encoding="utf-8", errors="replace").split("\n")[:80], 1):
        print(f"  {i:3}: {l}")