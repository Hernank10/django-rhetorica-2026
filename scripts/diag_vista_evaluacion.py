from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\views_cursos_completo.py")
c = p.read_text(encoding="utf-8")

# Buscar la funcion ver_evaluacion
m = re.search(r"def\s+ver_evaluacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if not m:
    print("[!] No encontro ver_evaluacion")
    exit(1)

bloque = m.group(0)

# Mostrar caracteres especiales
print("=" * 70)
print("BLOQUE ver_evaluacion - con repr() para ver caracteres ocultos")
print("=" * 70)
for i, l in enumerate(bloque.split("\n")):
    print(f"{i:3}: {repr(l)}")