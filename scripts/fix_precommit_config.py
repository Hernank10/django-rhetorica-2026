"""Actualizar .pre-commit-config.yaml para excluir contenido externo."""
from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\.pre-commit-config.yaml")
c = p.read_text(encoding="utf-8")

# Excluir la carpeta de contenido HTML/SQL grande
if "ejercicios_completos" not in c:
    c = c.replace(
        "repos:",
        "exclude: |\n  (?x)^(\n    ejercicios_completos-lengua-castellana/|\n    locale/.*\\.po$|\n    data/|\n    .*\\.sql$\n  )\n\nrepos:",
        1,
    )
    p.write_text(c, encoding="utf-8")
    print("[OK] .pre-commit-config.yaml actualizado con exclusiones")
else:
    print("[SKIP] ya estaba")

# Actualizar rev de pre-commit-hooks a v5 (elimina warning de stages deprecados)
c = p.read_text(encoding="utf-8")
if "v4.5.0" in c:
    c = c.replace("v4.5.0", "v5.0.0")
    p.write_text(c, encoding="utf-8")
    print("[OK] pre-commit-hooks: v4.5.0 -> v5.0.0")

# Mostrar el archivo
print()
print("=" * 70)
print(c)
