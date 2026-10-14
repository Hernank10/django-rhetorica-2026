"""Ver lineas 30-100 de models.py para encontrar el nombre real del metodo."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
mp = BASE / "core" / "models.py"
lineas = mp.read_text(encoding="utf-8", errors="replace").split("\n")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


safe("=" * 75)
safe("LINEAS 20-110 DE models.py (User)")
safe("=" * 75)
for i in range(19, min(110, len(lineas))):
    safe(f"  {i+1:4}: {lineas[i]}")