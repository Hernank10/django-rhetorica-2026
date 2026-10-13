from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

print("=== ¿Existe ya el botón? ===")
print("profesor:dashboard" in c)

print()
print("=== Bloque del navbar (ms-auto) ===")
# Buscar la zona del navbar ms-auto
i = c.find("navbar-nav ms-auto")
if i == -1:
    i = c.find("navbar-nav")
print(c[i-100:i+1500])
