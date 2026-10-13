"""Anade 'from django.utils import timezone' al primer bloque de imports."""
from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\views_cursos_completo.py")
c = p.read_text(encoding="utf-8")

if "from django.utils import timezone" in c:
    print("[SKIP] timezone ya importado")
else:
    # Insertar despues del ultimo 'from django.xxx' antes de la primera def
    lineas = c.split("\n")
    idx_ultimo_import_django = -1
    for i, l in enumerate(lineas[:50]):
        if l.startswith("from django.") and "import" in l:
            idx_ultimo_import_django = i
        if l.startswith("def ") or l.startswith("class ") or l.startswith("#"):
            break
    if idx_ultimo_import_django >= 0:
        lineas.insert(idx_ultimo_import_django + 1, "from django.utils import timezone")
        c = "\n".join(lineas)
        p.write_text(c, encoding="utf-8")
        print(f"[OK] timezone insertado despues de linea {idx_ultimo_import_django + 1}")
    else:
        # Fallback: al inicio del archivo despues de cualquier docstring
        print("[!] No se encontro ningun 'from django.' en las primeras 50 lineas")
        print("    Insertando al principio del archivo")

c = p.read_text(encoding="utf-8")
print()
print("Verificacion:")
print("  'from django.utils import timezone' en archivo:", "from django.utils import timezone" in c)
for i, l in enumerate(c.split("\n")[:30], 1):
    if "django" in l and "import" in l:
        print(f"  {i:3}: {l}")