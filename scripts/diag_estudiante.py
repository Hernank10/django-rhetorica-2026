from pathlib import Path

# 1) ¿Existe core/urls_estudiante.py?
p1 = Path(r"E:\02_proyectos\django-rhetorica\core\urls_estudiante.py")
print("=== core/urls_estudiante.py existe:", p1.exists(), "===")
if p1.exists():
    print(p1.read_text(encoding="utf-8")[:400])

# 2) ¿Está el include en django_retorica/urls.py?
p2 = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\urls.py")
c = p2.read_text(encoding="utf-8")
print()
print("=== Include de estudiante en django_retorica/urls.py ===")
print("urls_estudiante:", "core.urls_estudiante" in c)
print("urls_profesor:", "core.urls_profesor" in c)

# 3) Mostrar el inicio de i18n_patterns
import re
idx = c.find("i18n_patterns(")
if idx > 0:
    print()
    print("=== Primeras 20 lineas dentro de i18n_patterns ===")
    print(c[idx:idx+800])

# 4) ¿Existe core/views_estudiante.py?
p3 = Path(r"E:\02_proyectos\django-rhetorica\core\views_estudiante.py")
print()
print("=== core/views_estudiante.py existe:", p3.exists(), "===")

# 5) ¿Existen los templates?
tpl = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\estudiante")
print("=== Templates en core/templates/core/estudiante/ ===")
if tpl.exists():
    for f in sorted(tpl.rglob("*.html")):
        print("  ", f.name)
else:
    print("  (no existe la carpeta)")