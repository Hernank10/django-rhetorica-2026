import re
from pathlib import Path

# 1) Ver que funciones existen en core/views.py
print("=" * 60)
print("FUNCIONES EN core/views.py relacionadas con profesor:")
print("=" * 60)
c = Path("core/views.py").read_text(encoding="utf-8")
claves = ["profesor", "gestion", "crear_", "editar_", "eliminar_",
          "estudiante", "evaluacion", "curso", "leccion", "dashboard"]
encontradas = []
for i, l in enumerate(c.split("\n"), 1):
    if l.startswith("def "):
        nombre = l.split("(")[0][4:].strip()
        if any(k in nombre.lower() for k in claves):
            encontradas.append((i, nombre))
for i, n in encontradas:
    print(f"  {i:5}: {n}")
print(f"\n  Total: {len(encontradas)} funciones")

# 2) Ver templates que existen
print()
print("=" * 60)
print("TEMPLATES EN core/templates/core/:")
print("=" * 60)
raiz = Path("core/templates/core")
for p in sorted(raiz.rglob("*.html")):
    rel = p.relative_to(raiz)
    print(f"  {rel}")

# 3) Ver si existe core/views_profesor.py
print()
print("=" * 60)
print("ARCHIVOS views_*.py EN core/")
print("=" * 60)
for p in sorted(Path("core").glob("views*.py")):
    print(f"  {p.name}  ({p.stat().st_size} bytes)")
