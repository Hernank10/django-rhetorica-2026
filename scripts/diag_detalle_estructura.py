from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")
t = BASE / "core" / "templates" / "core" / "cursos" / "detalle.html"
c = t.read_text(encoding="utf-8")

print("=" * 60)
print("ESTRUCTURA DE detalle.html")
print("=" * 60)

for i, l in enumerate(c.split("\n"), 1):
    stripped = l.strip()
    if stripped.startswith("{% extends") or stripped.startswith("{% block") or stripped.startswith("{% endblock"):
        print(f"  L{i:3}: {stripped}")
    if "Recursos del curso" in l:
        print(f"  L{i:3}: >>> {stripped[:80]}")
        # Contexto: 3 lineas arriba y abajo
        lineas = c.split("\n")
        for j in range(max(0, i-4), min(len(lineas), i+4)):
            print(f"         {j+1:3}: {lineas[j][:100]}")

print()
print("=" * 60)
print("ESTRUCTURA DE views_cursos.py detalle_curso")
print("=" * 60)
vp = BASE / "core" / "views_cursos.py"
c2 = vp.read_text(encoding="utf-8")
m = re.search(r"def\s+detalle_curso\s*\([^)]*\):(.*?)(?=^def |\Z)", c2, re.MULTILINE | re.DOTALL)
if m:
    for l in m.group(1).split("\n")[:40]:
        print(f"  {l}")
