"""Ver el chequeo de admin en seed_content."""
import sys, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


p = BASE / "core" / "management" / "commands" / "seed_content.py"
c = p.read_text(encoding="utf-8", errors="replace")
lineas = c.split("\n")

print("=" * 70)
print("LINEAS 80-130 DE seed_content.py")
print("=" * 70)
for i in range(79, min(130, len(lineas))):
    safe(f"  {i+1:4}: {lineas[i]}")

print()
print("=" * 70)
print("TODAS LAS REFERENCIAS A 'admin' EN seed_content.py")
print("=" * 70)
for i, l in enumerate(lineas, 1):
    if "admin" in l.lower():
        safe(f"  {i:4}: {l}")

print()
print("=" * 70)
print("IMPORTS EN seed_content.py")
print("=" * 70)
for i, l in enumerate(lineas[:30], 1):
    if l.strip().startswith(("from ", "import ")):
        safe(f"  {i:4}: {l}")
