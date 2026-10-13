"""Segundo diagnostico: URLs REALES vs nombres referenciados en templates."""
import sys, os, re
from pathlib import Path

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
# 1) TODAS las URLs (nombre -> modulo.funcion)
# ============================================================
print("=" * 78)
print("1) TODAS LAS URLs REGISTRADAS (nombre -> modulo.funcion)")
print("=" * 78)

urls_registradas = {}  # nombre -> (patron, modulo, funcion)

def walk(patterns, prefijo="", namespace=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            ns = namespace
            if hasattr(p, "namespace") and p.namespace:
                ns = f"{namespace}:{p.namespace}" if namespace else p.namespace
            walk(p.url_patterns, prefijo + str(p.pattern), ns)
        else:
            pat = prefijo + str(p.pattern)
            nombre = p.name or "(sin nombre)"
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            func = p.callback.__name__ if hasattr(p.callback, "__name__") else "?"
            clave = f"{namespace}:{nombre}" if namespace else nombre
            urls_registradas[clave] = (pat, mod, func)

walk(get_resolver().url_patterns)

safe(f"Total URLs registradas: {len(urls_registradas)}")
for nombre in sorted(urls_registradas.keys()):
    pat, mod, func = urls_registradas[nombre]
    safe(f"  {nombre:50} -> {mod}.{func}")

# ============================================================
# 2) Nombres de URL referenciados en templates
# ============================================================
print()
print("=" * 78)
print("2) NOMBRES DE URL EN TEMPLATES QUE **NO** EXISTEN (rotas)")
print("=" * 78)

patron_url = re.compile(r"{%\s*url\s+['\"]([^'\"]+)['\"]")
nombres_tpl = set()
for t in BASE.glob("core/templates/**/*.html"):
    c = t.read_text(encoding="utf-8", errors="replace")
    for m in patron_url.finditer(c):
        nombres_tpl.add(m.group(1))

safe(f"Total nombres de URL referenciados en templates: {len(nombres_tpl)}")
safe("")
safe("Nombres ROTOS (no existen como URL registrada):")
rotas = []
for n in sorted(nombres_tpl):
    if n not in urls_registradas and n not in ("set_language",):
        # Ignorar URLs del admin que sí estan registradas con namespace
        if n.startswith("admin:"):
            continue
        rotas.append(n)
        safe(f"  [ROTA] {n}")

if not rotas:
    safe("  (ninguna, todas las URLs referenciadas existen)")

# ============================================================
# 3) Vistas realmente activas (por modulo.funcion)
# ============================================================
print()
print("=" * 78)
print("3) VISTAS ACTIVAS (modulo.funcion que aparecen en al menos 1 URL)")
print("=" * 78)

vistas_activas = set()
for nombre, (pat, mod, func) in urls_registradas.items():
    vistas_activas.add(f"{mod}.{func}")

safe(f"Total vistas activas: {len(vistas_activas)}")
for v in sorted(vistas_activas):
    safe(f"  {v}")

# ============================================================
# 4) Funciones definidas en cada views*.py y su estado
# ============================================================
print()
print("=" * 78)
print("4) ESTADO DE CADA DEF EN views*.py")
print("=" * 78)

for arch in sorted(BASE.glob("core/views*.py")):
    if "__pycache__" in str(arch):
        continue
    c = arch.read_text(encoding="utf-8", errors="replace")
    mod_name = f"core.{arch.stem}"
    defs = [m.group(2) for m in re.finditer(r"^(def|class)\s+(\w+)", c, re.MULTILINE)]
    if not defs:
        continue

    usadas = []
    huerfanas = []
    for d in defs:
        clave = f"{mod_name}.{d}"
        if clave in vistas_activas:
            usadas.append(d)
        else:
            huerfanas.append(d)

    safe(f"\n{arch.name} ({len(defs)} defs, {len(usadas)} activas, {len(huerfanas)} huerfanas)")
    if huerfanas:
        safe(f"  HUERFANAS:")
        for d in huerfanas:
            safe(f"    - {d}")

# ============================================================
# 5) Archivos 100% muertos (0 defs activas)
# ============================================================
print()
print("=" * 78)
print("5) ARCHIVOS 100% MUERTOS (0 defs activas, sin imports)")
print("=" * 78)

for arch in sorted(BASE.glob("core/views*.py")):
    if "__pycache__" in str(arch):
        continue
    c = arch.read_text(encoding="utf-8", errors="replace")
    mod_name = f"core.{arch.stem}"
    defs = [m.group(2) for m in re.finditer(r"^(def|class)\s+(\w+)", c, re.MULTILINE)]
    if not defs:
        continue

    activas = [d for d in defs if f"{mod_name}.{d}" in vistas_activas]
    if not activas:
        safe(f"  [MUERTO] {arch.name}  ({len(defs)} defs, 0 activas)")