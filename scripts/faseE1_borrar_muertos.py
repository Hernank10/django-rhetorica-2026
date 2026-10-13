"""Fase E1: borrar 6 archivos 100% muertos con verificacion.

Excluye scripts/ y tests/ del check de imports (no son produccion).
"""
import subprocess
import sys
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

ARCHIVOS_MUERTOS = [
    "core/views_actualizadas.py",
    "core/views_api.py",
    "core/views_cursos.py",
    "core/views_ejercicios_biblioteca.py",
    "core/views_ejercicios_template.py",
    "core/views_preguntas.py",
]

# Carpetas a IGNORAR en el check de imports
EXCLUIR_CARPETAS = ["scripts", "tests", "__pycache__", "migrations", "node_modules", ".git"]


def run(cmd):
    r = subprocess.run(cmd, shell=True, cwd=str(BASE), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


# ============================================================
# 1) Verificar que existen
# ============================================================
print("=" * 70)
print("1) VERIFICANDO QUE LOS ARCHIVOS EXISTEN")
print("=" * 70)

existentes = []
for arch in ARCHIVOS_MUERTOS:
    p = BASE / arch
    if p.exists():
        print(f"  [OK] {arch}  ({p.stat().st_size} bytes)")
        existentes.append(arch)
    else:
        print(f"  [!] {arch} no existe")

if not existentes:
    print()
    print("[SKIP] Nada que borrar")
    sys.exit(0)

# ============================================================
# 2) Pre-flight: buscar imports (excluyendo scripts/, tests/)
# ============================================================
print()
print("=" * 70)
print("2) BUSCANDO IMPORTS EN CODIGO DE PRODUCCION")
print("=" * 70)

nombres_modulos = [Path(a).stem for a in ARCHIVOS_MUERTOS]
nombres_archivos_borrados = [Path(a).name for a in ARCHIVOS_MUERTOS]
encontrados = []

for py in BASE.rglob("*.py"):
    # Saltar si está en carpeta excluida
    rel = py.relative_to(BASE)
    if any(part in EXCLUIR_CARPETAS for part in rel.parts):
        continue
    # Saltar los propios archivos a borrar
    if py.name in nombres_archivos_borrados:
        continue
    try:
        c = py.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for nombre in nombres_modulos:
        if (f"from .{nombre} import" in c
            or f"from core.{nombre} import" in c
            or f"import {nombre}" in c):
            encontrados.append(f"{rel} importa {nombre}")

if encontrados:
    print("  [!] IMPORTS EN PRODUCCION - NO BORRAR:")
    for e in encontrados:
        print(f"      {e}")
    sys.exit(1)
else:
    print("  [OK] Ningun archivo de produccion importa estos modulos")

# ============================================================
# 3) Backup y borrado
# ============================================================
print()
print("=" * 70)
print("3) BORRANDO CON git rm")
print("=" * 70)

for arch in existentes:
    code, out, err = run(f'git rm "{arch}"')
    if code == 0:
        print(f"  [OK] git rm {arch}")
    else:
        print(f"  [!] git rm {arch} fallo: {err.strip()}")

# ============================================================
# 4) Verificacion Django
# ============================================================
print()
print("=" * 70)
print("4) VERIFICACION DJANGO")
print("=" * 70)

code, out, err = run(r"E:\PythonPortable_Django5\python.exe manage.py check")
print(f"  manage.py check -> exit={code}")
if out.strip():
    print(f"  {out.strip()[:200]}")

# ============================================================
# 5) Verificacion pytest rapida
# ============================================================
print()
print("=" * 70)
print("5) VERIFICACION PYTEST")
print("=" * 70)

code, out, err = run(
    r"E:\PythonPortable_Django5\python.exe -m pytest -q --tb=line --no-header -p no:cacheprovider"
)
print(f"  pytest -> exit={code}")

lineas = (out + err).strip().split("\n")
for l in lineas[-3:]:
    print(f"  {l}")

# ============================================================
# 6) Siguiente paso
# ============================================================
print()
print("=" * 70)
print("LISTO. Siguiente:")
print("=" * 70)
print("  E:\\PythonPortable_Django5\\python.exe -m pytest --cov=core --cov-report=term-missing -q -p no:cacheprovider > cobertura4.txt 2>&1")
print("  findstr /C:\"TOTAL\" cobertura4.txt")
print("  git status")