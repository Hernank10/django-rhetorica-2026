"""Fix del decorador admin_required (2 bugs reales)."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
p = BASE / "core" / "decorators.py"
c = p.read_text(encoding="utf-8")

# Fix 1: is_admin -> is_superuser
c = c.replace(
    "if not request.user.is_authenticated or not request.user.is_admin:",
    "if not request.user.is_authenticated or not request.user.is_superuser:",
)

# Fix 2: 'dashboard' -> 'dashboard_estudiante'
c = c.replace(
    "return redirect('dashboard')",
    "return redirect('dashboard_estudiante')",
)

p.write_text(c, encoding="utf-8")
print("[OK] decorators.py arreglado")
print()
print("Contenido resultante:")
for i, l in enumerate(c.split("\n"), 1):
    print(f"  {i:3}: {l}")