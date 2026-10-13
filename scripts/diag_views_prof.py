"""Diagnostico de views_profesor.py para tests CRUD."""
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
# 1) Cobertura por vista (leyendo el archivo cobertura actual)
# ============================================================
safe("=" * 78)
safe("1) LINEAS NO CUBIERTAS EN views_profesor.py")
safe("=" * 78)

cob = BASE / "cobertura9.txt"
if not cob.exists():
    cob = BASE / "cobertura8.txt"

if cob.exists():
    txt = cob.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"core\\views_profesor\.py\s+\d+\s+\d+\s+\d+%\s+([\d,\s\-]+)", txt)
    if m:
        miss = m.group(1).strip()
        safe(f"  Miss: {miss[:500]}")

# ============================================================
# 2) Vistas y que campos POST leen
# ============================================================
safe("")
safe("=" * 78)
safe("2) VISTAS CON POST Y CAMPOS QUE LEEN")
safe("=" * 78)

vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8", errors="replace")

# Encontrar todas las defs
vistas = []
for m in re.finditer(r"^def\s+(\w+)\s*\(([^)]*)\):", c, re.MULTILINE):
    vistas.append({
        "nombre": m.group(1),
        "args": m.group(2).strip(),
        "start": m.start(),
    })

for i, v in enumerate(vistas):
    end = vistas[i + 1]["start"] if i + 1 < len(vistas) else len(c)
    cuerpo = c[v["start"]:end]

    # Detectar metodos HTTP
    es_post = "request.method" in cuerpo and "POST" in cuerpo
    tiene_get = "request.method" in cuerpo and "GET" in cuerpo
    es_delete = ".delete()" in cuerpo and ("POST" in cuerpo or "request.method" in cuerpo)

    # Extraer campos de POST
    campos_post = re.findall(r'request\.POST\.get\(\s*["\'](\w+)["\']', cuerpo)
    campos_post += re.findall(r'request\.POST\[\s*["\'](\w+)["\']\s*\]', cuerpo)

    # Detectar redirect
    tiene_redirect = "redirect(" in cuerpo

    tag = []
    if es_post: tag.append("POST")
    if tiene_get: tag.append("GET")
    if es_delete: tag.append("DELETE")

    safe(f"  def {v['nombre']}({v['args'][:40]})")
    safe(f"       metodos: {', '.join(tag) if tag else 'solo GET'}")
    if campos_post:
        safe(f"       POST fields: {sorted(set(campos_post))}")
    if tiene_redirect:
        safe(f"       redirige al final")

# ============================================================
# 3) URLs CRUD activas
# ============================================================
safe("")
safe("=" * 78)
safe("3) URLS CRUD ACTIVAS DE PROFESOR")
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
            pat = prefijo + str(p.pattern)
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            func = p.callback.__name__ if hasattr(p.callback, "__name__") else "?"
            if mod == "core.views_profesor":
                nombre = p.name or "(sin nombre)"
                safe(f"  {pat:65} -> {nombre}")

walk(get_resolver().url_patterns)
