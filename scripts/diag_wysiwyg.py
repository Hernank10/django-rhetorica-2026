"""Localiza donde se define el form de Leccion y las vistas leccion_crear/editar."""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

print("=" * 70)
print("1) ARCHIVOS .py CON 'leccion_crear' O 'LeccionForm' O 'contenido'")
print("=" * 70)

for py in sorted(BASE.rglob("*.py")):
    if any(x in str(py) for x in ["__pycache__", "migrations", "scripts\\"]):
        continue
    try:
        c = py.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    hallazgos = []
    for patron in ["leccion_crear", "leccion_editar", "LeccionForm", "class LeccionForm",
                   "contenido = forms", "contenido=", "LeccionForm("]:
        if patron in c:
            hallazgos.append(patron)
    if hallazgos:
        print(f"  {py.relative_to(BASE)}")
        for h in hallazgos:
            print(f"      -> {h}")

print()
print("=" * 70)
print("2) FORMS DEFINIDOS EN core/forms.py")
print("=" * 70)
fp = BASE / "core" / "forms.py"
if fp.exists():
    c = fp.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"^class\s+(\w+)\s*\([^)]*\):", c, re.MULTILINE):
        print(f"  {m.group(1)}")
else:
    print("  [!] core/forms.py no existe")

print()
print("=" * 70)
print("3) VISTAS leccion_* EN core/views_profesor.py")
print("=" * 70)
vp = BASE / "core" / "views_profesor.py"
if vp.exists():
    c = vp.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"^def\s+(\w*leccion\w*)\s*\(", c, re.MULTILINE):
        print(f"  def {m.group(1)}")
    for m in re.finditer(r"^@\w+", c, re.MULTILINE):
        pass
else:
    print("  [!] core/views_profesor.py no existe")

print()
print("=" * 70)
print("4) TEMPLATES DE LECCION EN PROFESOR")
print("=" * 70)
for t in sorted(BASE.rglob("*leccion*.html")):
    if "profesor" in str(t):
        print(f"  {t.relative_to(BASE)}")

print()
print("=" * 70)
print("5) CONTENIDO DE core/templates/.../leccion_form.html (primeras 60 lineas)")
print("=" * 70)
for candidato in BASE.rglob("*leccion*.html"):
    if "form" in candidato.name.lower() or "editar" in candidato.name.lower():
        c = candidato.read_text(encoding="utf-8", errors="replace")
        print(f"--- {candidato.relative_to(BASE)} ---")
        for i, l in enumerate(c.split("\n")[:60], 1):
            print(f"  {i:3}: {l}")
        print()

print("=" * 70)
print("6) ¿QUE USA BASE.HTML PARA {% block %} ?")
print("=" * 70)
bh = BASE / "core" / "templates" / "base.html"
if bh.exists():
    c = bh.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"{%\s*block\s+(\w+)\s*%}", c):
        print(f"  block {m.group(1)}")
    for m in re.finditer(r"{%\s*block\s+(\w+)\s*%}(.*?){%\s*endblock", c, re.DOTALL):
        pass
    # Buscar extra_js o extra_css
    for nombre in ["extra_js", "extra_css", "extra_head", "scripts", "javascript"]:
        if f"block {nombre}" in c:
            print(f"  [!] Tiene bloque extra: {nombre}")
