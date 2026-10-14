"""Ver las 2 versiones de detalle_curso con contexto completo."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
vp = BASE / "core" / "views_cursos_completo.py"
lineas = vp.read_text(encoding="utf-8", errors="replace").split("\n")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# Encontrar las 2 defs
defs = []
for i, l in enumerate(lineas):
    if l.strip().startswith("def detalle_curso("):
        # Buscar decoradores arriba
        inicio = i
        j = i - 1
        while j >= 0:
            s = lineas[j].strip()
            if s.startswith("@"):
                inicio = j
                j -= 1
            elif s == "":
                if j > 0 and lineas[j-1].strip().startswith("@"):
                    inicio = j
                    j -= 1
                else:
                    break
            else:
                break
        defs.append(inicio)

safe(f"Defs encontradas en lineas (0-index): {defs}")

for idx, ini in enumerate(defs):
    # Fin: siguiente def o 5 lineas despues
    fin = len(lineas)
    for k in range(ini + 1, len(lineas)):
        if lineas[k].strip().startswith(("def ", "@login_required", "@user_passes_test")):
            fin = k
            break

    safe("")
    safe("=" * 75)
    safe(f"VERSION {idx+1}: lineas {ini+1} a {fin}")
    safe("=" * 75)
    for k in range(ini, min(fin, ini + 40)):
        safe(f"  {k+1:4}: {lineas[k]}")
    if fin - ini > 40:
        safe(f"  ... ({fin - ini - 40} lineas mas)")