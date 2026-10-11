from pathlib import Path
import re
p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\index.html")
c = p.read_text(encoding="utf-8")
# quitar load i18n si esta antes de extends
c = re.sub(r"^\{%\s*load\s+i18n\s*%\}\s*\r?\n(?=\{%\s*extends)", "", c, flags=re.MULTILINE)
# asegurar que extends sea la primera linea no vacia
if not c.lstrip().startswith("{% extends"):
    c = "{% extends 'base.html' %}\n{% load i18n %}\n" + re.sub(r"^\{%\s*extends[^%]*%\}\s*\r?\n", "", c, count=1, flags=re.MULTILINE)
else:
    # insertar load i18n despues de extends si no esta
    if "{% load i18n %}" not in c.split("\n", 5)[0:3]:
        c = re.sub(r"(\{%\s*extends[^%]*%\}\s*\r?\n)", r"\1{% load i18n %}\n", c, count=1)
p.write_text(c, encoding="utf-8")
print("[OK] index.html arreglado. Primeras 3 lineas:")
for i, line in enumerate(c.splitlines()[:3], 1):
    print(f"{i}: {line}")