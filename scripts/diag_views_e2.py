"""Fase E2: diagnostico quirurgico de views.py.

Detecta:
  - Defs duplicadas (mismo nombre)
  - Defs huerfanas (no aparecen en URLs)
  - Tamano de cada bloque

NO modifica nada. Solo reporta.
"""
import sys, os, re
from pathlib import Path
from collections import defaultdict

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
# 1) URLs activas de core.views
# ============================================================
vistas_activas = set()

def walk(patterns):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            walk(p.url_patterns)
        else:
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            func = p.callback.__name__ if hasattr(p.callback, "__name__") else "?"
            if mod == "core.views":
                vistas_activas.add(func)

walk(get_resolver().url_patterns)

safe("=" * 78)
safe("VISTAS ACTIVAS EN core.views (referenciadas por URLs)")
safe("=" * 78)
for v in sorted(vistas_activas):
    safe(f"  {v}")


# ============================================================
# 2) Analizar views.py
# ============================================================
p = BASE / "core" / "views.py"
c = p.read_text(encoding="utf-8", errors="replace")
lineas = c.split("\n")

safe("")
safe("=" * 78)
safe("TODAS LAS DEFS DE views.py CON LINEAS Y ESTADO")
safe("=" * 78)

# Encontrar todas las defs (con decoradores previos)
patron_def = re.compile(r"^(def|class)\s+(\w+)")

defs = []
for i, l in enumerate(lineas):
    m = patron_def.match(l)
    if m:
        # Buscar decoradores arriba
        inicio = i
        j = i - 1
        while j >= 0 and (lineas[j].strip().startswith("@") or lineas[j].strip() == ""):
            if lineas[j].strip().startswith("@"):
                inicio = j
            j -= 1

        defs.append({
            "nombre": m.group(2),
            "tipo": m.group(1),
            "linea_def": i + 1,
            "linea_inicio": inicio + 1,
        })

# Calcular fin de cada def (siguiente def o EOF)
for idx, d in enumerate(defs):
    if idx + 1 < len(defs):
        d["linea_fin"] = defs[idx + 1]["linea_inicio"] - 1
    else:
        d["linea_fin"] = len(lineas)
    d["size"] = d["linea_fin"] - d["linea_inicio"] + 1

# Detectar duplicados
por_nombre = defaultdict(list)
for d in defs:
    por_nombre[d["nombre"]].append(d)

duplicados = {n: ds for n, ds in por_nombre.items() if len(ds) > 1}

safe("")
safe("DEFS DUPLICADAS (mismo nombre, varias veces):")
if duplicados:
    for nombre, ds in sorted(duplicados.items()):
        safe(f"  [{len(ds)}x] {nombre}")
        for d in ds:
            safe(f"      linea {d['linea_def']:4}  (size {d['size']:3} lineas)")
else:
    safe("  (ninguna)")

# Marcar estado de cada def
safe("")
safe("ESTADO DE CADA DEF:")
safe("")

# Para duplicados, la ULTIMA definicion es la que Django usa
ultima_def_por_nombre = {}
for d in defs:
    ultima_def_por_nombre[d["nombre"]] = d["linea_def"]

total_activas = 0
total_huerfanas = 0
total_duplicadas_anteriores = 0

for d in defs:
    nombre = d["nombre"]
    activa = nombre in vistas_activas
    es_ultima = ultima_def_por_nombre[nombre] == d["linea_def"]
    duplicada_no_ultima = (nombre in duplicados) and not es_ultima

    if activa and es_ultima:
        estado = "ACTIVA"
        total_activas += 1
    elif duplicada_no_ultima:
        estado = "DUPLICADA (no usada)"
        total_duplicadas_anteriores += 1
    else:
        estado = "HUERFANA"
        total_huerfanas += 1

    safe(f"  [{estado:22}] lineas {d['linea_inicio']:4}-{d['linea_fin']:4} ({d['size']:3})  {d['tipo']} {nombre}")

safe("")
safe("=" * 78)
safe(f"RESUMEN: {len(defs)} defs")
safe(f"  Activas:                       {total_activas}")
safe(f"  Huerfanas:                     {total_huerfanas}")
safe(f"  Duplicadas (no ultima):        {total_duplicadas_anteriores}")
safe("=" * 78)


# ============================================================
# 3) Referencias a nombres huerfanos en templates
# ============================================================
safe("")
safe("=" * 78)
safe("REFERENCIAS A VISTAS HUERFANAS EN TEMPLATES ({% url 'X' %})")
safe("=" * 78)

# Recolectar nombres de URL en templates
patron_url = re.compile(r"{%\s*url\s+['\"]([^'\"]+)['\"]")
nombres_en_tpl = set()
for t in BASE.glob("core/templates/**/*.html"):
    c2 = t.read_text(encoding="utf-8", errors="replace")
    for m in patron_url.finditer(c2):
        nombres_en_tpl.add(m.group(1))

# Para cada def huerfana, ver si su nombre esta en templates
huerfanas_nombres = set()
for d in defs:
    nombre = d["nombre"]
    if nombre in vistas_activas:
        continue
    huerfanas_nombres.add(nombre)

refs = huerfanas_nombres & nombres_en_tpl
if refs:
    safe("  [!] Estas vistas huerfanas SI se referencian en templates:")
    for r in sorted(refs):
        safe(f"      - {r}")
    safe("")
    safe("  Si borras estas defs, los templates seguiran con links rotos")
    safe("  (pero ya estaban rotos antes porque no hay URL que las exponga).")
else:
    safe("  (ninguna referencia a vistas huerfanas en templates)")


# ============================================================
# 4) Importancia: cuantas lineas borraria
# ============================================================
safe("")
safe("=" * 78)
safe("IMPACTO DE BORRAR DEFS HUERFANAS + DUPLICADAS")
safe("=" * 78)

lineas_borrables = 0
for d in defs:
    nombre = d["nombre"]
    activa = nombre in vistas_activas
    es_ultima = ultima_def_por_nombre[nombre] == d["linea_def"]
    if not activa or not es_ultima:
        lineas_borrables += d["size"]

safe(f"  Lineas totales de views.py: {len(lineas)}")
safe(f"  Lineas borrables:           {lineas_borrables}")
safe(f"  Archivo resultante:         ~{len(lineas) - lineas_borrables} lineas")