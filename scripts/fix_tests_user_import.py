"""Reemplaza imports rotos de core.models.User en tests."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
TESTS = BASE / "core" / "tests"

VIEJO_AUTH = "from core.models import ("
AUTH_IMPORT = "from django.contrib.auth.models import User"

archivos = [
    TESTS / "test_models_extended.py",
    TESTS / "test_views_branches.py",
]

for p in archivos:
    if not p.exists():
        print(f"[SKIP] {p.name} no existe")
        continue
    c = p.read_text(encoding="utf-8")
    if "User," not in c:
        print(f"[SKIP] {p.name} no usa User")
        continue

    # Quitar 'User,' del import multiple de .models
    c = c.replace("    User,\r\n", "").replace("    User,\n", "")

    # Añadir el import de auth.User si no está
    if AUTH_IMPORT not in c:
        # Insertar antes del primer 'from core.models'
        idx = c.find("from core.models")
        if idx < 0:
            idx = c.find("from .models")
        if idx > 0:
            c = c[:idx] + AUTH_IMPORT + "\n" + c[idx:]
        else:
            c = AUTH_IMPORT + "\n" + c

    p.write_text(c, encoding="utf-8")
    print(f"[OK] {p.name} corregido")

print()
print("Listo. Proximos pasos:")
print("  manage.py check")
print("  pytest -q")