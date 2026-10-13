"""Diagnostico de lineas sin cubrir en views_recursos.py."""
import sys, os, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# Cobertura actual
cob = BASE / "cob_h.txt"
miss_lineas = set()
if cob.exists():
    txt = cob.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"core\\views_recursos\.py\s+\d+\s+\d+\s+\d+%\s+([\d,\s\-]+)", txt)
    if m:
        miss_str = m.group(1).strip()
        safe("=" * 78)
        safe("LINEAS SIN CUBRIR EN views_recursos.py")
        safe("=" * 78)
        safe(f"  Miss: {miss_str}")
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

safe(f"  Total: {len(miss_lineas)} lineas")


# Contexto
vp = BASE / "core" / "views_recursos.py"
lineas = vp.read_text(encoding="utf-8", errors="replace").split("\n")

safe("")
safe("=" * 78)
safe("CONTEXTO DE LAS LINEAS SIN CUBRIR")
safe("=" * 78)

for i in sorted(miss_lineas):
    if 1 <= i <= len(lineas):
        safe(f"  {i:4}: {lineas[i-1]}")


# Funciones
safe("")
safe("=" * 78)
safe("FUNCIONES DEFINIDAS")
safe("=" * 78)
for m in re.finditer(r"^def\s+(\w+)\s*\(([^)]*)\):", vp.read_text(encoding="utf-8", errors="replace"), re.MULTILINE):
    safe(f"  def {m.group(1)}({m.group(2)[:60]})")


# URLs
safe("")
safe("=" * 78)
safe("URLS -> core.views_recursos")
safe("=" * 78)
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()
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
            if mod == "core.views_recursos":
                pat = prefijo + str(p.pattern)
                nombre = f"{namespace}:{p.name}" if namespace and p.name else (p.name or "?")
                safe(f"  {pat:65} -> {nombre}  ({func})")

walk(get_resolver().url_patterns)