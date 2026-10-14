"""Diagnostico de views_profesor.py (75 lineas sin cubrir)."""
import re
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


cob = BASE / "cov_a3.txt"
txt = cob.read_text(encoding="utf-8", errors="replace")

m = re.search(r"core\\views_profesor\.py\s+\d+\s+\d+\s+(\d+)%\s+([\d,\s\-]+)", txt)
if not m:
    safe("[!] No se encontro views_profesor.py")
    exit(1)

pct = m.group(1)
miss_str = m.group(2).strip()
safe("=" * 75)
safe("core/views_profesor.py")
safe("=" * 75)
safe(f"  Cobertura: {pct}%")

# Parsear
lineas_miss = set()
for parte in miss_str.split(","):
    parte = parte.strip()
    if "-" in parte:
        try:
            a, b = parte.split("-")
            for i in range(int(a.strip()), int(b.strip()) + 1):
                lineas_miss.add(i)
        except ValueError:
            pass
    else:
        try:
            lineas_miss.add(int(parte))
        except ValueError:
            pass

# Agrupar en bloques (rango continuo)
lineas_sorted = sorted(lineas_miss)
bloques = []
bloque = [lineas_sorted[0]] if lineas_sorted else []
for i in lineas_sorted[1:]:
    if i == bloque[-1] + 1:
        bloque.append(i)
    else:
        bloques.append((bloque[0], bloque[-1]))
        bloque = [i]
if bloque:
    bloques.append((bloque[0], bloque[-1]))

safe(f"  Total lineas: {len(lineas_miss)}")
safe(f"  Bloques: {len(bloques)}")

# Leer archivo
vp = BASE / "core" / "views_profesor.py"
lineas = vp.read_text(encoding="utf-8", errors="replace").split("\n")

# Encontrar la funcion de cada bloque
safe("")
safe("BLOQUES CON CONTEXTO Y FUNCION:")
for ini, fin in bloques:
    # Buscar def mas cercana arriba
    funcion = "(global)"
    for i in range(ini - 1, max(0, ini - 200), -1):
        s = lineas[i - 1].strip()
        if s.startswith("def "):
            funcion = s.split("(")[0].replace("def ", "")
            break

    safe("")
    safe(f"  [BLOQUE {ini}-{fin}]  en {funcion}()")
    for i in range(ini, min(fin + 1, ini + 8)):
        if 1 <= i <= len(lineas):
            safe(f"      {i:4}: {lineas[i-1][:110]}")
    if fin - ini > 7:
        safe(f"      ... ({fin - ini - 7} lineas mas)")