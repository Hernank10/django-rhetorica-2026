"""Diagnostico de codigo muerto.

1) Lista de URLs activas -> funciones referenciadas
2) Defs en cada archivo de views
3) Imports cruzados entre archivos de views
4) Referencias en templates
"""
import sys, os
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.urls import get_resolver

def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))

# ============================================================
# 1) URLs ACTIVAS
# ============================================================
print("=" * 78)
print("1) URLs ACTIVAS -> FUNCIONES USADAS")
print("=" * 78)

urls_por_modulo = {}
def walk(patterns, prefijo=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            walk(p.url_patterns, prefijo + str(p.pattern))
        else:
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            func = p.callback.__name__ if hasattr(p.callback, "__name__") else "?"
            urls_por_modulo.setdefault(mod, set()).add(func)

walk(get_resolver().url_patterns)

for mod in sorted(urls_por_modulo.keys()):
    if "core.views" in mod or "core.urls" in mod:
        safe(f"  {mod}:")
        for fn in sorted(urls_por_modulo[mod]):
            safe(f"    - {fn}")

# ============================================================
# 2) DEFS EN CADA ARCHIVO DE VIEWS
# ============================================================
print()
print("=" * 78)
print("2) DEFS EN CADA ARCHIVO views*.py")
print("=" * 78)

archivos_views = sorted(BASE.glob("core/views*.py"))
archivos_info = {}

for arch in archivos_views:
    if arch.name == "views_uploads.py" or "__pycache__" in str(arch):
        pass
    c = arch.read_text(encoding="utf-8", errors="replace")
    defs = [m.group(2) for m in re.finditer(r"^(def|class)\s+(\w+)", c, re.MULTILINE)]
    lineas = len(c.split("\n"))
    stmts_aprox = sum(1 for l in c.split("\n") if l.strip() and not l.strip().startswith("#"))
    archivos_info[arch.name] = {
        "path": arch,
        "defs": defs,
        "lineas": lineas,
        "stmts": stmts_aprox,
    }
    safe(f"  {arch.name:40} {len(defs):3} defs, {lineas:4} lineas")

# ============================================================
# 3) IMPORTS CRUZADOS
# ============================================================
print()
print("=" * 78)
print("3) IMPORTS CRUZADOS ENTRE ARCHIVOS DE CORE")
print("=" * 78)

# Buscar en TODO core/ por imports hacia views*.py o urls*.py
patron_import = re.compile(r"from\s+\.(views\w*|urls\w*)\s+import|import\s+\.(views\w*|urls\w*)")

for py in sorted(BASE.glob("core/**/*.py")):
    if "__pycache__" in str(py) or "migrations" in str(py):
        continue
    c = py.read_text(encoding="utf-8", errors="replace")
    for i, l in enumerate(c.split("\n"), 1):
        if patron_import.search(l):
            # Ignorar imports propios del archivo
            if py.name in l:
                continue
            safe(f"  {py.relative_to(BASE)}:{i}  {l.strip()}")

# ============================================================
# 4) URLs EN templates -> nombres
# ============================================================
print()
print("=" * 78)
print("4) REFERENCIAS {% url ... %} EN templates DE core/")
print("=" * 78)

patron_url = re.compile(r"{%\s*url\s+['\"]([^'\"]+)['\"]")
nombres_url_usados = set()

for t in BASE.glob("core/templates/**/*.html"):
    c = t.read_text(encoding="utf-8", errors="replace")
    for m in patron_url.finditer(c):
        nombres_url_usados.add(m.group(1))

safe(f"  Total nombres de URL referenciados en templates: {len(nombres_url_usados)}")
for n in sorted(nombres_url_usados):
    safe(f"    - {n}")

# ============================================================
# 5) ANALISIS: DEFS NO REFERENCIADAS POR URLs
# ============================================================
print()
print("=" * 78)
print("5) FUNCIONES EN views*.py QUE NO APARECEN EN URLs ACTIVAS")
print("=" * 78)

# Recolectar TODAS las funciones activas
funcs_activas = set()
for mod, fns in urls_por_modulo.items():
    funcs_activas.update(fns)

for nombre, info in archivos_info.items():
    defs_sin_url = [d for d in info["defs"] if d not in funcs_activas and not d.startswith("_")]
    if defs_sin_url:
        safe(f"\n  {nombre} ({len(defs_sin_url)} defs huerfanas):")
        for d in defs_sin_url[:20]:
            safe(f"    - {d}")
        if len(defs_sin_url) > 20:
            safe(f"    ... y {len(defs_sin_url) - 20} mas")

# ============================================================
# 6) REFERENCIAS EN TESTS
# ============================================================
print()
print("=" * 78)
print("6) TESTS QUE IMPORTAN DE views*.py")
print("=" * 78)

for py in sorted(BASE.glob("core/tests/*.py")):
    c = py.read_text(encoding="utf-8", errors="replace")
    for i, l in enumerate(c.split("\n"), 1):
        if re.search(r"from\s+core\.views|import\s+core\.views|from\s+\.\.views|from\s+core\s+import\s+views", l):
            safe(f"  {py.name}:{i}  {l.strip()}")