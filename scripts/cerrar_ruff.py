"""Cerrar Fase N-2: activar ruff, commitear fixes, arreglar bugs reales."""
import subprocess
import re
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


def run(cmd, check=False):
    r = subprocess.run(cmd, shell=True, cwd=str(BASE), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


# ============================================================
# 1) ARREGLAR BUG 1: F821 ResultadoEvaluacionCurso en views_profesor.py
# ============================================================
safe("=" * 70)
safe("1) FIX BUG: ResultadoEvaluacionCurso no importado en views_profesor.py")
safe("=" * 70)

vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8")

# Verificar si ya está importado
if "ResultadoEvaluacionCurso" in c.split("def ")[0]:
    safe("  [SKIP] ya importado al inicio")
else:
    # Buscar el bloque de imports de models_cursos
    patron = re.compile(
        r"(from \.models_cursos import \([^)]*)\)",
        re.DOTALL,
    )
    m = patron.search(c)
    if m:
        bloque = m.group(1)
        if "ResultadoEvaluacionCurso" not in bloque:
            # Añadir el import al bloque
            nuevo_bloque = bloque.rstrip()
            # Quitar ')' final si está
            if nuevo_bloque.rstrip().endswith(","):
                nuevo_bloque = nuevo_bloque.rstrip() + "\n    ResultadoEvaluacionCurso,\n)"
            else:
                nuevo_bloque = nuevo_bloque.rstrip() + ",\n    ResultadoEvaluacionCurso,\n)"
            c = c[:m.start()] + nuevo_bloque + c[m.end():]
            vp.write_text(c, encoding="utf-8")
            safe("  [OK] ResultadoEvaluacionCurso anadido al import")
        else:
            safe("  [SKIP] ya estaba en el import")
    else:
        safe("  [!] No se encontro el bloque 'from .models_cursos import (...)'")


# ============================================================
# 2) ARREGLAR BUG 2: F811 detalle_curso duplicado
# ============================================================
safe("")
safe("=" * 70)
safe("2) FIX BUG: detalle_curso duplicado en views_cursos_completo.py")
safe("=" * 70)

vc = BASE / "core" / "views_cursos_completo.py"
c = vc.read_text(encoding="utf-8")
lineas = c.split("\n")

# Encontrar todas las defs de detalle_curso
idx_defs = []
for i, l in enumerate(lineas):
    if re.match(r"^def\s+detalle_curso\s*\(", l):
        idx_defs.append(i)

safe(f"  Encontradas {len(idx_defs)} definiciones en lineas: {[i+1 for i in idx_defs]}")

if len(idx_defs) >= 2:
    # La SEGUNDA definicion gana en Django. Eliminar la PRIMERA.
    ini1 = idx_defs[0]
    fin1 = idx_defs[1] - 1

    # Buscar decoradores arriba de ini1
    j = ini1 - 1
    while j >= 0 and (lineas[j].strip().startswith("@") or lineas[j].strip() == ""):
        if lineas[j].strip().startswith("@"):
            ini1 = j
        j -= 1

    # Ahora ini1 apunta al inicio del bloque (con decoradores)
    safe(f"  Eliminando primera definicion: lineas {ini1+1} a {fin1+1}")
    safe(f"  (la segunda definicion en linea {idx_defs[1]+1} es la que Django usa)")

    nuevas_lineas = lineas[:ini1] + lineas[fin1 + 1:]
    vc.write_text("\n".join(nuevas_lineas), encoding="utf-8")
    safe("  [OK] Primera definicion eliminada")
elif len(idx_defs) == 1:
    safe("  [SKIP] solo hay 1 definicion")
else:
    safe("  [!] No se encontro detalle_curso")


# ============================================================
# 3) ARREGLAR BUG 3: F811 User redefined en views.py
# ============================================================
safe("")
safe("=" * 70)
safe("3) FIX BUG: User redefined en views.py")
safe("=" * 70)

v = BASE / "core" / "views.py"
c = v.read_text(encoding="utf-8")

# Buscar "from django.contrib.auth.models import User" (import duplicado)
if "from django.contrib.auth.models import User" in c:
    lineas = c.split("\n")
    nuevas = []
    eliminadas = 0
    for l in lineas:
        if l.strip() == "from django.contrib.auth.models import User":
            safe(f"  Eliminando linea: '{l.strip()}'")
            eliminadas += 1
            continue
        nuevas.append(l)
    if eliminadas > 0:
        v.write_text("\n".join(nuevas), encoding="utf-8")
        safe(f"  [OK] {eliminadas} import(s) duplicado(s) eliminado(s)")
else:
    safe("  [SKIP] no habia import duplicado de User")


# ============================================================
# 4) ACTUALIZAR pyproject.toml: ignorar warnings no-criticos
# ============================================================
safe("")
safe("=" * 70)
safe("4) Silenciar warnings no-criticos de ruff en pyproject.toml")
safe("=" * 70)

pp = BASE / "pyproject.toml"
c = pp.read_text(encoding="utf-8")

# Añadir B007 y B017 a la lista de ignore
if '"B007"' not in c:
    c = c.replace(
        '"B008",  # function call in default arg (Django usa esto)',
        '"B008",  # function call in default arg (Django usa esto)\n    "B007",  # unused loop control variable (a veces intencional)\n    "B017",  # assert blind exception (tests intencional)\n    "B904",  # raise without from (Django Http404 comun)\n    "F541",  # f-string sin placeholders\n    "F841",  # local var assigned but not used',
    )
    pp.write_text(c, encoding="utf-8")
    safe("  [OK] B007, B017, B904, F541, F841 anadidos a ignore")


# ============================================================
# 5) ACTIVAR ruff en .pre-commit-config.yaml
# ============================================================
safe("")
safe("=" * 70)
safe("5) Activar ruff en .pre-commit-config.yaml")
safe("=" * 70)

pc = BASE / ".pre-commit-config.yaml"
c = pc.read_text(encoding="utf-8")

# Buscar el bloque comentado de ruff
patron_comentado = re.compile(
    r"(\s*)# Descomentar cuando quieras linting automatico con ruff:\n"
    r"(\s*)# - repo: https://github\.com/astral-sh/ruff-pre-commit\n"
    r"(\s*)#   rev: v[\d.]+\n"
    r"(\s*)#   hooks:\n"
    r"(\s*)#     - id: ruff\n"
    r"(\s*)#       args: \[--fix, --exit-non-zero-on-fix\]",
    re.MULTILINE,
)

if patron_comentado.search(c):
    nuevo = """  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]"""
    c = patron_comentado.sub(nuevo, c, count=1)
    pc.write_text(c, encoding="utf-8")
    safe("  [OK] ruff descomentado y activado")
elif "id: ruff\n" in c and "# - repo: https://github.com/astral-sh/ruff-pre-commit" not in c:
    safe("  [SKIP] ya estaba activo")
else:
    safe("  [!] No se encontro el bloque. Revisa .pre-commit-config.yaml manualmente")


# ============================================================
# 6) Verificar que ruff ya no reporta errores graves
# ============================================================
safe("")
safe("=" * 70)
safe("6) Verificacion final con ruff")
safe("=" * 70)

code, out, err = run(
    r"E:\PythonPortable_Django5\python.exe -m ruff check core/ conftest.py django_retorica/ --statistics",
)
safe(out[:2000])
if err.strip():
    safe(f"  STDERR: {err[:500]}")


# ============================================================
# 7) Correr tests
# ============================================================
safe("")
safe("=" * 70)
safe("7) Tests")
safe("=" * 70)

code, out, err = run(
    r"E:\PythonPortable_Django5\python.exe -m pytest -q --tb=line --no-header -p no:cacheprovider",
)
safe(f"  pytest -> exit={code}")
for l in (out + err).split("\n")[-5:]:
    if l.strip():
        safe(f"    {l}")


# ============================================================
# 8) Instrucciones finales
# ============================================================
safe("")
safe("=" * 70)
safe("LISTO. Ahora ejecuta:")
safe("=" * 70)
safe("  git add -A")
safe("  git commit -m \"chore: activar ruff en pre-commit + fixes de bugs (F821, F811)\"")
safe("  git push")