"""Fase D.2: verificar y borrar templates huerfanos con URLs rotas.

Verifica que ningun Python del proyecto (excluyendo scripts/) los renderiza.
Luego borra con git rm.
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

CANDIDATOS = [
    "core/templates/core/admin_panel.html",
    "core/templates/core/examen.html",
    "core/templates/core/practicar_pregunta.html",
    "core/templates/core/cursos/leccion.html",
    "core/templates/core/preguntas/lista.html",
]

# Carpetas a excluir: scripts, instalador.py, node_modules, etc.
EXCLUIR_CARPETAS = ["scripts", "__pycache__", "migrations", "node_modules", ".git",
                    "ejercicios_completos-lengua-castellana"]


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# ============================================================
# 1) Buscar render() que apunte a cada candidato
# ============================================================
safe("=" * 70)
safe("1) BUSCANDO RENDER() QUE APUNTEN A LOS CANDIDATOS")
safe("=" * 70)

patron_render = re.compile(r'render\s*\(\s*[^,]+,\s*["\']([^"\']+)["\']')

# Mapear: nombre_template -> [(py, linea)]
referencias = {}

for py in BASE.rglob("*.py"):
    rel = py.relative_to(BASE)
    if any(part in EXCLUIR_CARPETAS for part in rel.parts):
        continue
    try:
        txt = py.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for i, l in enumerate(txt.split("\n"), 1):
        m = patron_render.search(l)
        if m:
            tpl = m.group(1)
            referencias.setdefault(tpl, []).append((str(rel), i, l.strip()[:100]))

seguros = []
en_uso = []

for cand in CANDIDATOS:
    # Normalizar: el template path en render() suele ser "core/examen.html"
    # Mientras que el archivo real es "core/templates/core/examen.html"
    nombre_render = cand.replace("core/templates/", "")

    if nombre_render in referencias:
        en_uso.append((cand, referencias[nombre_render]))
        safe(f"\n  [!] EN USO: {cand}")
        for py_rel, lineno, texto in referencias[nombre_render]:
            safe(f"      {py_rel}:{lineno}  {texto}")
    else:
        seguros.append(cand)
        safe(f"\n  [OK] Huerfano: {cand}")


# ============================================================
# 2) Decidir
# ============================================================
safe("")
safe("=" * 70)

if en_uso:
    safe("[ABORT] Hay templates en uso. No borramos nada.")
    safe("Templates en uso:")
    for cand, refs in en_uso:
        safe(f"  {cand}")
    sys.exit(1)

if not seguros:
    safe("[SKIP] No hay templates que borrar")
    sys.exit(0)

safe(f"[OK] Todos los {len(seguros)} candidatos son huerfanos")
safe("=" * 70)


# ============================================================
# 3) Borrar con git rm
# ============================================================
safe("")
safe("=" * 70)
safe("2) BORRANDO")
safe("=" * 70)

for cand in seguros:
    p = BASE / cand
    if not p.exists():
        safe(f"  [!] No existe: {cand}")
        continue
    r = subprocess.run(f'git rm "{cand}"', shell=True, cwd=str(BASE),
                       capture_output=True, text=True)
    if r.returncode == 0:
        safe(f"  [OK] git rm {cand}")
    else:
        safe(f"  [!] Fallo: {r.stderr.strip()}")


# ============================================================
# 4) Correr el test de validacion
# ============================================================
safe("")
safe("=" * 70)
safe("3) VERIFICACION")
safe("=" * 70)

r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe -m pytest core\tests\test_urls_templates.py -v --tb=short -p no:cacheprovider",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
safe(f"  pytest test_urls_templates.py -> exit={r.returncode}")
for l in (r.stdout + r.stderr).split("\n")[-8:]:
    if l.strip():
        safe(f"    {l}")


# ============================================================
# 5) manage.py check
# ============================================================
r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe manage.py check",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
safe(f"  manage.py check -> exit={r.returncode}")
if r.stdout.strip():
    safe(f"    {r.stdout.strip()[:200]}")


# ============================================================
# 6) Siguiente
# ============================================================
if r.returncode == 0:
    safe("")
    safe("=" * 70)
    safe("LISTO. Ahora:")
    safe("=" * 70)
    safe("  git add core/tests/test_urls_templates.py scripts/diag_tpls_en_uso.py scripts/faseD2_borrar_tpls.py")
    safe("  git commit -m \"refactor(templates): borrar 5 templates huerfanos con URLs rotas\"")
    safe("  git push")
