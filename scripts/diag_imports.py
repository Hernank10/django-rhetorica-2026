from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\views_cursos_completo.py")
c = p.read_text(encoding="utf-8")

print("=" * 70)
print("PRIMERAS 40 LINEAS CON repr()")
print("=" * 70)
for i, l in enumerate(c.split("\n")[:40], 1):
    print(f"{i:3}: {repr(l)}")

print()
print("=" * 70)
print("BUSCAR 'timezone'")
print("=" * 70)
for i, l in enumerate(c.split("\n"), 1):
    if "timezone" in l:
        print(f"{i:3}: {l}")
