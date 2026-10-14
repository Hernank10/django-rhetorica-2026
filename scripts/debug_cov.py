"""Ver primeras 100 lineas de cov_check.txt para debug."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
cob = BASE / "cov_check.txt"

if not cob.exists():
    print("[!] cov_check.txt no existe")
    exit(1)

print(f"Tamano: {cob.stat().st_size} bytes")
print()

txt = cob.read_text(encoding="utf-8", errors="replace")
lineas = txt.split("\n")

# Buscar lineas con "decorators", "models", "views_"
print("=" * 75)
print("LINEAS QUE CONTIENEN 'decorators' o 'forms' o 'views_profesor'")
print("=" * 75)
for i, l in enumerate(lineas):
    if any(x in l for x in ["decorators", "forms.py", "views_profesor", "views_estudiante"]):
        print(f"  {i+1:4}: {repr(l)}")

print()
print("=" * 75)
print("ULTIMAS 15 LINEAS DEL ARCHIVO")
print("=" * 75)
for l in lineas[-15:]:
    print(f"  {l}")