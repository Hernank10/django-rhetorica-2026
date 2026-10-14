"""Diagnostico de lineas sin cubrir en views.py."""
import sys, os, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# ============================================================
# 1) Cobertura de views.py
# ============================================================
safe("=" * 78)
safe("1) LINEAS SIN CUBRIR EN views.py")
safe("=" * 78)

cob = BASE / "cob_final.txt"
if not cob.exists():
    cob = BASE / "cobertura10.txt"
if not cob.exists():
    cob = BASE / "cobertura9.txt"

miss_lineas = set()
if cob.exists():
    txt = cob.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"core\\views\.py\s+\d+\s+\d+\s+\d+%\s+([\d,\s\-]+)", txt)
    if m:
        miss_str = m.group(1).strip()
        safe(f"  Miss string: {miss_str[:400]}")
        # Parsear rangos: "44-45, 77, 87-90"
        for parte in miss_str.split(","):
            parte = parte.strip()
            if "-" in parte:
                try:
                    a, b = parte.split("-")
                    for i in range(int(a.strip()), int(b.strip()) + 1):
                        miss_lineas.add(i)
                except ValueError:
                    pass
            else:
                try:
                    miss_lineas.add(int(parte))
                except ValueError:
                    pass

safe(f"  Total lineas sin cubrir: {len(miss_lineas)}")


# ============================================================
# 2) Ver las lineas no cubiertas en contexto
# ============================================================
safe("")
safe("=" * 78)
safe("2) CONTEXTO DE LAS LINEAS SIN CUBRIR")
safe("=" * 78)

vp = BASE / "core" / "views.py"
lineas = vp.read_text(encoding="utf-8", errors="replace").split("\n")

# Agrupar lineas sin cubrir en bloques
bloques = []
bloque = []
for i in range(1, len(lineas) + 1):
    if i in miss_lineas:
        bloque.append(i)
    else:
        if bloque:
            bloques.append((bloque[0], bloque[-1]))
            bloque = []
if bloque:
    bloques.append((bloque[0], bloque[-1]))

safe(f"  {len(bloques)} bloques sin cubrir:")
for ini, fin in bloques:
    # Encontrar la def mas cercana arriba
    funcion = "(global)"
    for i in range(ini - 1, max(0, ini - 100), -1):
        if re.match(r"^def\s+(\w+)", lineas[i - 1]):
            funcion = re.match(r"^def\s+(\w+)", lineas[i - 1]).group(1)
            break
    safe(f"\n  [BLOQUE] lineas {ini}-{fin}  (en {funcion})")
    for i in range(ini, min(fin + 1, ini + 5)):
        safe(f"      {i:4}: {lineas[i-1]}")


# ============================================================
# 3) Funciones definidas en views.py
# ============================================================
safe("")
safe("=" * 78)
safe("3) FUNCIONES EN views.py")
safe("=" * 78)
for m in re.finditer(r"^def\s+(\w+)\s*\(([^)]*)\):", vp.read_text(encoding="utf-8", errors="replace"), re.MULTILINE):
    nombre = m.group(1)
    args = m.group(2).strip()
    safe(f"  def {nombre}({args[:60]})")


# ============================================================
# 4) URLs que apuntan a core.views
# ============================================================
safe("")
safe("=" * 78)
safe("4) URLS ACTIVAS -> core.views")
safe("=" * 78)

from django.urls import get_resolver

def walk(patterns, prefijo="", namespace=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            ns = namespace
            if hasattr(p, "namespace") and p.namespace:
                ns = f"{namespace}:{p.namespace}" if namespace else p.namespace
            walk(p.url_patterns, prefijo + str(p.pattern), ns)
        else:
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            func = p.callback.__name__ if hasattr(p.callback, "__name__") else "?"
            if mod == "core.views":
                pat = prefijo + str(p.pattern)
                nombre = f"{namespace}:{p.name}" if namespace and p.name else (p.name or "(sin nombre)")
                safe(f"  {pat:60} -> {nombre}  ({func})")

walk(get_resolver().url_patterns)
