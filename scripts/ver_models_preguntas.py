"""Ver contenido de models_preguntas.py."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
mp = BASE / "core" / "models_preguntas.py"

if not mp.exists():
    print("[!] No existe el archivo")
    exit(1)

print("=" * 75)
print("core/models_preguntas.py")
print("=" * 75)
for i, l in enumerate(mp.read_text(encoding="utf-8").split("\n"), 1):
    try:
        print(f"  {i:3}: {l}")
    except UnicodeEncodeError:
        print(f"  {i:3}: {l.encode('ascii', 'replace').decode('ascii')}")