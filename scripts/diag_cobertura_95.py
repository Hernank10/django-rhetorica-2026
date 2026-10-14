"""Diagnostico detallado de lineas sin cubrir en los archivos objetivo."""
import re
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# Leer reporte de cobertura
cob = BASE / "cov_check.txt"
if not cob.exists():
    cob = BASE / "cob_i2.txt"
if not cob.exists():
    print("[!] No se encontro reporte de cobertura. Corre primero:")
    print("    pytest --cov=core --cov-report=term-missing -q")
    exit(1)

txt = cob.read_text(encoding="utf-8", errors="replace")

# Archivos objetivo
objetivos = [
    ("core\\decorators.py", "decorators.py"),
    ("core\\forms.py", "forms.py"),
    ("core\\models.py", "models.py"),
    ("core\\views_estudiante.py", "views_estudiante.py"),
    ("core\\views_profesor.py", "views_profesor.py"),
]

for patron, nombre in objetivos:
    safe("")
    safe("=" * 75)
    safe(f"{nombre}")
    safe("=" * 75)

    # Buscar la linea de cobertura
    m = re.search(re.escape(patron) + r"\s+\d+\s+\d+\s+(\d+)%\s+([\d,\s\-]+)", txt)
    if not m:
        safe(f"  [!] No encontrado en el reporte")
        continue

    pct = m.group(1)
    miss_str = m.group(2).strip()
    safe(f"  Cobertura: {pct}%")
    safe(f"  Lineas sin cubrir: {miss_str}")

    # Parsear y mostrar contexto
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

    # Leer el archivo real
    file_path = BASE / patron
    if not file_path.exists():
        continue
    lineas = file_path.read_text(encoding="utf-8", errors="replace").split("\n")

    safe("")
    safe(f"  Contexto de lineas sin cubrir:")
    for i in sorted(lineas_miss):
        if 1 <= i <= len(lineas):
            l = lineas[i - 1]
            safe(f"    {i:4}: {l[:100]}")