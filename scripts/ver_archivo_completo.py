"""Mostrar lineas 1-260 de views_cursos_completo.py."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
vp = BASE / "core" / "views_cursos_completo.py"
lineas = vp.read_text(encoding="utf-8", errors="replace").split("\n")

print(f"Total lineas del archivo: {len(lineas)}")
print()

# Imprimir en 2 bloques: lineas 1-30, luego 200-260
print("=" * 75)
print("BLOQUE A: lineas 1 a 60  (primera version + entorno)")
print("=" * 75)
for i in range(0, min(60, len(lineas))):
    try:
        print(f"  {i+1:4}: {lineas[i]}")
    except UnicodeEncodeError:
        print(f"  {i+1:4}: {lineas[i].encode('ascii', 'replace').decode('ascii')}")

print()
print("=" * 75)
print("BLOQUE B: lineas 190 a 260  (segunda version + entorno)")
print("=" * 75)
for i in range(189, min(260, len(lineas))):
    try:
        print(f"  {i+1:4}: {lineas[i]}")
    except UnicodeEncodeError:
        print(f"  {i+1:4}: {lineas[i].encode('ascii', 'replace').decode('ascii')}")