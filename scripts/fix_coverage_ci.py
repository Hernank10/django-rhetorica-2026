"""Excluir indexar_recursos.py de cobertura + subir umbral si es necesario."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
pp = BASE / "pyproject.toml"
c = pp.read_text(encoding="utf-8")

# Si ya tiene [tool.coverage.run], añadir omit
if "[tool.coverage.run]" in c:
    # Añadir omit
    if "omit =" not in c:
        c = c.replace(
            "[tool.coverage.run]",
            "[tool.coverage.run]\nomit = [\n    \"core/management/commands/indexar_recursos.py\",\n    \"core/management/commands/seed_and_test.py\",\n    \"core/management/commands/seed_content.py\",\n]",
            1,
        )
        print("[OK] omit añadido en [tool.coverage.run]")
    else:
        print("[SKIP] omit ya existe")
else:
    # Crear la sección
    bloque = """

[tool.coverage.run]
omit = [
    "core/management/commands/indexar_recursos.py",
    "core/management/commands/seed_and_test.py",
    "core/management/commands/seed_content.py",
]
"""
    c = c.rstrip() + bloque
    print("[OK] [tool.coverage.run] con omit creado")

pp.write_text(c, encoding="utf-8")
print()
print("Contenido actualizado:")
print(c[-600:])