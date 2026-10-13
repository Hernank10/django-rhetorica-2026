"""Ver bloque exacto de dashboard_gamificacion con repr()."""
from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\views.py")
c = p.read_text(encoding="utf-8")
lineas = c.split("\n")

# Buscar la funcion dashboard_gamificacion
for i, l in enumerate(lineas):
    if l.strip().startswith("def dashboard_gamificacion"):
        print(f"ENCONTRADA EN LINEA {i+1}")
        for j in range(i, min(i + 45, len(lineas))):
            print(f"{j+1:4}: {repr(lineas[j])}")
        break