"""Ver lineas sin cubrir en views.py."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
vp = BASE / "core" / "views.py"
lineas = vp.read_text(encoding="utf-8", errors="replace").split("\n")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# Lineas sin cubrir conocidas del reporte anterior
lineas_miss = [56, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
               79, 80, 81, 82, 83, 84, 85, 86, 87,
               126, 127, 128, 148, 162, 163, 166, 167, 170, 171, 227]

safe("=" * 75)
safe("VIEWS.PY - LINEAS SIN CUBRIR CON CONTEXTO")
safe("=" * 75)

for i in sorted(set(lineas_miss)):
    if 1 <= i <= len(lineas):
        safe(f"  {i:4}: {lineas[i-1][:110]}")

# Encontrar la funcion de cada bloque
safe("")
safe("=" * 75)
safe("FUNCIONES AFECTADAS")
safe("=" * 75)

funcion_actual = "(global)"
for i, l in enumerate(lineas, 1):
    if l.strip().startswith("def "):
        funcion_actual = l.strip().split("(")[0].replace("def ", "")
    if i in lineas_miss:
        safe(f"  linea {i}: {funcion_actual}()")