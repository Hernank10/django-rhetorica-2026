"""Diagnostico de lineas sin cubrir en models.py."""
import re
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


cob = BASE / "cov_a1b.txt"
txt = cob.read_text(encoding="utf-8", errors="replace")

# models.py
m = re.search(r"core\\models\.py\s+\d+\s+\d+\s+(\d+)%\s+([\d,\s\-]+)", txt)
if not m:
    safe("[!] No se encontro core\\models.py en el reporte")
    exit(1)

pct = m.group(1)
miss_str = m.group(2).strip()
safe("=" * 75)
safe("core/models.py")
safe("=" * 75)
safe(f"  Cobertura: {pct}%")
safe(f"  Sin cubrir: {miss_str}")

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

# Leer archivo
mp = BASE / "core" / "models.py"
lineas = mp.read_text(encoding="utf-8", errors="replace").split("\n")

safe("")
safe("Contexto de lineas sin cubrir:")
for i in sorted(lineas_miss):
    if 1 <= i <= len(lineas):
        safe(f"  {i:4}: {lineas[i-1][:100]}")