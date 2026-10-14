"""Configurar ruff conservador + integrar en pre-commit."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


# ============================================================
# 1) Crear pyproject.toml con config de ruff
# ============================================================
pp = BASE / "pyproject.toml"

if pp.exists():
    c = pp.read_text(encoding="utf-8")
    if "[tool.ruff]" in c:
        print("[SKIP] ruff ya configurado en pyproject.toml")
        exit(0)
else:
    c = ""

ruff_config = """
# ============================================================
# Ruff - Linter de Python (conservador)
# ============================================================
# Reglas activas (solo las que detectan bugs reales):
#   E   - Pycodestyle errors (solo errores graves)
#   F   - Pyflakes (variables no usadas, imports rotos)
#   W   - Warnings (espacios trailing, etc.)
#   I   - isort (orden de imports)
#   B   - Bugbear (bugs comunes de Python)
#
# Reglas DESACTIVADAS intencionalmente:
#   E501 - Line too long (mucho ruido en templates)
#   E402 - Module import not at top (comun en Django)
#
# Por archivo:
#   - scripts/       → ignorado (son one-shot)
#   - migrations/    → ignorado (autogeneradas)
#   - tests/         → mas permisivo

[tool.ruff]
line-length = 120
target-version = "py312"
exclude = [
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "migrations",
    "scripts",
    "ejercicios_completos-lengua-castellana",
    "locale",
    "staticfiles",
    "media",
]

[tool.ruff.lint]
select = [
    "E",   # Pycodestyle errors
    "F",   # Pyflakes
    "W",   # Warnings
    "I",   # isort
    "B",   # Bugbear
]
ignore = [
    "E501",  # line too long
    "E402",  # import not at top of file
    "E731",  # lambda assignment
    "E741",  # ambiguous variable name (l, I, O)
    "F401",  # imported but unused (manejado manualmente)
    "F403",  # import *
    "F405",  # maybe undefined from star
    "B008",  # function call in default arg (Django usa esto)
]

[tool.ruff.lint.per-file-ignores]
# Tests pueden tener imports no usados por fixtures
"core/tests/*.py" = ["F811", "F841"]
# Settings de Django tienen imports raros
"django_retorica/settings.py" = ["F401", "F403"]
"django_retorica/*.py" = ["F401", "F403"]
# conftest tiene fixtures globales
"conftest.py" = ["F401", "F811"]

[tool.ruff.lint.isort]
known-first-party = ["core", "django_retorica"]
"""

c = c.rstrip() + "\n" + ruff_config
pp.write_text(c, encoding="utf-8")
print("[OK] pyproject.toml con config ruff creado")


# ============================================================
# 2) Actualizar .pre-commit-config.yaml
# ============================================================
pc = BASE / ".pre-commit-config.yaml"
cp = pc.read_text(encoding="utf-8")

if "ruff-pre-commit" in cp:
    print("[SKIP] ruff ya en pre-commit")
else:
    # Descomentar el bloque de ruff
    viejo = """  # Descomentar cuando quieras linting automatico con ruff:
  # - repo: https://github.com/astral-sh/ruff-pre-commit
  #   rev: v0.4.4
  #   hooks:
  #     - id: ruff
  #       args: [--fix, --exit-non-zero-on-fix]
  #       exclude: ^(scripts/|core/migrations/)"""

    nuevo = """  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]"""

    if viejo in cp:
        cp = cp.replace(viejo, nuevo, 1)
        pc.write_text(cp, encoding="utf-8")
        print("[OK] ruff activado en pre-commit")
    else:
        print("[!] No se encontro el bloque comentado. Revisa .pre-commit-config.yaml")


# ============================================================
# 3) Dry run: cuantos errores hay
# ============================================================
print()
print("=" * 70)
print("DRY RUN: cuantos errores detecta ruff")
print("=" * 70)

import subprocess
r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe -m ruff check core/ conftest.py django_retorica/ --statistics",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
print(r.stdout[:3000])
if r.stderr.strip():
    print("STDERR:", r.stderr[:1000])