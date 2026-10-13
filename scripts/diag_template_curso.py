from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

print("=" * 60)
print("VISTAS QUE RENDERIZAN detalle*.html")
print("=" * 60)

for p in BASE.rglob("views*.py"):
    if "migrations" in str(p) or "__pycache__" in str(p):
        continue
    c = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"def\s+(\w+)\s*\([^)]*\):(.*?)(?=^def |\Z)", c, re.MULTILINE | re.DOTALL):
        nombre = m.group(1)
        cuerpo = m.group(2)
        for rm in re.finditer(r"render\s*\(\s*request\s*,\s*['\"]([^'\"]*detalle[^'\"]*\.html)['\"]", cuerpo):
            print(f"  {p.name:25} → {nombre}()  →  {rm.group(1)}")

print()
print("=" * 60)
print("CONTENIDO DE detalle.html (primeras 30 líneas)")
print("=" * 60)
det = BASE / "core" / "templates" / "core" / "cursos" / "detalle.html"
if det.exists():
    for i, l in enumerate(det.read_text(encoding="utf-8", errors="replace").split("\n")[:30], 1):
        print(f"  {i:3}: {l}")
else:
    print("  [!] No existe detalle.html")
