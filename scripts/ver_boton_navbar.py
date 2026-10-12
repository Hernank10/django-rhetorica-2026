from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")
lineas = c.split("\n")

print("=" * 60)
print("BUSCAR 'recursos:lista' EN core/templates/core/base.html")
print("=" * 60)
for i, l in enumerate(lineas):
    if "recursos:lista" in l:
        print(f"\n--- Línea {i+1} ---")
        for j in range(max(0, i-6), min(len(lineas), i+8)):
            mark = ">>>" if j == i else "   "
            print(f"{mark} {j+1}: {lineas[j]}")