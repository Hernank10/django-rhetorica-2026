"""Diagnostico de utils_certificados.py."""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")
p = BASE / "core" / "utils_certificados.py"
c = p.read_text(encoding="utf-8", errors="replace")
lineas = c.split("\n")

print("=" * 75)
print("1) PRIMERAS 30 LINEAS (imports)")
print("=" * 75)
for i, l in enumerate(lineas[:30], 1):
    print(f"  {i:3}: {l}")

print()
print("=" * 75)
print("2) LINEAS 90-105 (donde falla el PDF)")
print("=" * 75)
for i, l in enumerate(lineas[89:105], 90):
    print(f"  {i:3}: {l}")

print()
print("=" * 75)
print("3) TODAS LAS LLAMADAS A setFont EN EL ARCHIVO")
print("=" * 75)
for i, l in enumerate(lineas, 1):
    if "setFont" in l:
        print(f"  {i:3}: {l}")

print()
print("=" * 75)
print("4) FUNCIONES DEFINIDAS")
print("=" * 75)
for m in re.finditer(r"^def\s+(\w+)\s*\([^)]*\):", c, re.MULTILINE):
    print(f"  {m.group(1)}")

print()
print("=" * 75)
print("5) FUENTES REFERENCIADAS")
print("=" * 75)
fuentes = set(re.findall(r'["\']([A-Za-z]+-[A-Za-z]+)["\']', c))
for f in sorted(fuentes):
    print(f"  {f}")