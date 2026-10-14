"""Ver por que no se cubren las lineas 507-508, 532-537, 775-777, 889-896."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
vp = BASE / "core" / "views_profesor.py"
lineas = vp.read_text(encoding="utf-8", errors="replace").split("\n")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


bloques = [
    (490, 545, "detalle_estudiante_completo"),
    (760, 790, "certificado_docx"),
    (875, 905, "recursos_autovincular"),
]

for ini, fin, nombre in bloques:
    safe("")
    safe("=" * 75)
    safe(f"{nombre} - lineas {ini}-{fin}")
    safe("=" * 75)
    for i in range(ini - 1, min(fin, len(lineas))):
        safe(f"  {i+1:4}: {lineas[i]}")