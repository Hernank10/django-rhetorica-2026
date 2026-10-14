"""Ver contenido de decorators.py y forms.py."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


for nombre in ["decorators.py", "forms.py"]:
    p = BASE / "core" / nombre
    safe("=" * 75)
    safe(f"{nombre}")
    safe("=" * 75)
    if not p.exists():
        safe("  [!] No existe")
        continue
    for i, l in enumerate(p.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
        safe(f"  {i:3}: {l}")
    safe("")