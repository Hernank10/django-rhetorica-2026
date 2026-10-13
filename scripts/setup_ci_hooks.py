"""Fase M + N: CI con GitHub Actions + pre-commit hooks."""
import subprocess
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


# ============================================================
# 1) Diagnostico
# ============================================================
print("=" * 70)
print("1) DIAGNOSTICO INICIAL")
print("=" * 70)
print(f"  .github/ existe:       {(BASE / '.github').exists()}")
print(f"  requirements.txt:      {(BASE / 'requirements.txt').exists()}")
print(f"  .pre-commit-config:    {(BASE / '.pre-commit-config.yaml').exists()}")


# ============================================================
# 2) Generar requirements.txt desde pip freeze
# ============================================================
print()
print("=" * 70)
print("2) GENERAR requirements.txt")
print("=" * 70)

r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe -m pip freeze",
    shell=True, capture_output=True, text=True,
)
freeze = r.stdout

IMPORTANTES = [
    "Django", "reportlab", "python-docx", "nh3", "Pillow", "qrcode",
    "pytest", "pytest-django", "pytest-cov", "beautifulsoup4", "lxml",
    "qrcode",
]

lineas = []
for l in freeze.split("\n"):
    l = l.strip()
    if not l or l.startswith("#"):
        continue
    for imp in IMPORTANTES:
        if l.lower().startswith(imp.lower() + "=="):
            lineas.append(l)
            break

lineas = sorted(set(lineas))
req_content = "\n".join(lineas) + "\n"

print(f"  {len(lineas)} paquetes identificados:")
for l in lineas:
    print(f"    {l}")

req_path = BASE / "requirements.txt"
req_path.write_text(req_content, encoding="utf-8")
print(f"  [OK] requirements.txt escrito")


# ============================================================
# 3) Crear .github/workflows/tests.yml
# ============================================================
print()
print("=" * 70)
print("3) CI workflow (.github/workflows/tests.yml)")
print("=" * 70)

ci_path = BASE / ".github" / "workflows" / "tests.yml"
ci_path.parent.mkdir(parents=True, exist_ok=True)

ci_content = """name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Django check
        run: python manage.py check
        env:
          DJANGO_SETTINGS_MODULE: django_retorica.settings

      - name: Run migrations
        run: python manage.py migrate --noinput
        env:
          DJANGO_SETTINGS_MODULE: django_retorica.settings

      - name: Run tests with coverage
        run: |
          pytest --cov=core --cov-report=term-missing --cov-fail-under=85 -q
        env:
          DJANGO_SETTINGS_MODULE: django_retorica.settings
"""

ci_path.write_text(ci_content, encoding="utf-8")
print(f"  [OK] {ci_path.relative_to(BASE)}")


# ============================================================
# 4) Crear .pre-commit-config.yaml
# ============================================================
print()
print("=" * 70)
print("4) Pre-commit config (.pre-commit-config.yaml)")
print("=" * 70)

pc_path = BASE / ".pre-commit-config.yaml"

pc_content = """# Pre-commit hooks para django-rhetorica
# Instalacion: python -m pre_commit install
# Ejecutar sobre todos los archivos: python -m pre_commit run --all-files
# Saltar hooks en un commit puntual: git commit --no-verify

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
        exclude: \\.(md|txt)$
      - id: end-of-file-fixer
        exclude: \\.(md|txt)$
      - id: check-yaml
        args: ['--allow-multiple-documents']
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ['--maxkb=5000']
      - id: mixed-line-ending
        args: ['--fix=lf']
        exclude: \\.(bat|cmd)$
      - id: check-ast
        files: \\.py$
      - id: debug-statements
        files: \\.py$

  # Descomentar cuando quieras linting automatico con ruff:
  # - repo: https://github.com/astral-sh/ruff-pre-commit
  #   rev: v0.4.4
  #   hooks:
  #     - id: ruff
  #       args: [--fix, --exit-non-zero-on-fix]
  #       exclude: ^(scripts/|core/migrations/)
"""

pc_path.write_text(pc_content, encoding="utf-8")
print(f"  [OK] {pc_path.relative_to(BASE)}")


# ============================================================
# 5) Actualizar .gitignore
# ============================================================
print()
print("=" * 70)
print("5) Actualizar .gitignore")
print("=" * 70)

gitignore = BASE / ".gitignore"
patrones_nuevos = [".pre-commit-cache/", "htmlcov/", ".coverage"]

if gitignore.exists():
    c = gitignore.read_text(encoding="utf-8")
    anadidos = []
    for patron in patrones_nuevos:
        if patron not in c:
            anadidos.append(patron)
    if anadidos:
        c = c.rstrip() + "\n" + "\n".join(anadidos) + "\n"
        gitignore.write_text(c, encoding="utf-8")
        print(f"  [OK] {len(anadidos)} patrones añadidos: {anadidos}")
    else:
        print(f"  [SKIP] ya estaban todos")
else:
    print(f"  [!] .gitignore no existe")


# ============================================================
# 6) Instrucciones
# ============================================================
print()
print("=" * 70)
print("LISTO. SIGUIENTE:")
print("=" * 70)
print()
print("  # Instalar pre-commit (una sola vez)")
print("  E:\\PythonPortable_Django5\\python.exe -m pip install pre-commit")
print()
print("  # Instalar los hooks en el repo (una sola vez)")
print("  E:\\PythonPortable_Django5\\python.exe -m pre_commit install")
print()
print("  # Primera pasada: arreglar todos los archivos")
print("  E:\\PythonPortable_Django5\\python.exe -m pre_commit run --all-files")
print()
print("  # Commit de la config")
print("  git add .github/ requirements.txt .pre-commit-config.yaml .gitignore")
print("  git commit -m \"ci: agregar GitHub Actions + pre-commit hooks\"")
print("  git push")
print()
print("  # Esto hara que el CI corra en GitHub.")
print("  # Ve a: https://github.com/Hernank10/django-rhetorica-2026/actions")
