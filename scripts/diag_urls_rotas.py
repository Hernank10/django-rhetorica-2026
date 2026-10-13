"""Fase D: mapear cada URL rota -> template + linea + contexto."""
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
# 1) URLs registradas (todas)
# ============================================================
urls_registradas = set()

def walk(patterns, namespace=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            ns = namespace
            if hasattr(p, "namespace") and p.namespace:
                ns = f"{namespace}:{p.namespace}" if namespace else p.namespace
            walk(p.url_patterns, ns)
        else:
            nombre = p.name or ""
            if nombre:
                clave = f"{namespace}:{nombre}" if namespace else nombre
                urls_registradas.add(clave)

walk(get_resolver().url_patterns)

# Lista de nombres rotos conocidos (del diag anterior)
ROTOS = [
    "admin_nuevo_usuario",
    "api_evaluar_respuesta",
    "core:certificaciones_lista",
    "core:dashboard_gamificacion",
    "core:login",
    "core:logout",
    "core:perfil_usuario",
    "core:registro",
    "delete_user",
    "examen_form",
    "generar_preguntas",
    "importar_preguntas",
    "marcar_leccion_completa",
    "practicar_pregunta",
    "toggle_admin",
    "ver_preguntas",
]

# ============================================================
# 2) Mapear cada roto -> templates + lineas + contexto
# ============================================================
mapa = defaultdict(list)  # roto -> [(tpl, lineno, texto)]

patron_url = re.compile(r"{%\s*url\s+['\"]([^'\"]+)['\"]")

for t in sorted(BASE.glob("core/templates/**/*.html")):
    try:
        c = t.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    lineas = c.split("\n")
    for m in patron_url.finditer(c):
        nombre = m.group(1)
        if nombre in ROTOS:
            # Encontrar numero de linea
            pos = m.start()
            lineno = c[:pos].count("\n") + 1
            texto = lineas[lineno - 1].strip()
            mapa[nombre].append((str(t.relative_to(BASE)), lineno, texto))


# ============================================================
# 3) Imprimir agrupado
# ============================================================
safe("=" * 80)
safe("URLS ROTAS -> TEMPLATES Y LINEAS")
safe("=" * 80)

for roto in sorted(mapa.keys()):
    refs = mapa[roto]
    safe(f"\n[{roto}]  ({len(refs)} referencias)")
    for tpl, lineno, texto in refs:
        safe(f"    {tpl}:{lineno}")
        safe(f"        {texto[:100]}")

# ============================================================
# 4) Ver cuales NO aparecen (por si el diag anterior estaba mal)
# ============================================================
safe("")
safe("=" * 80)
safe("ROTOS SIN REFERENCIAS EN TEMPLATES")
safe("=" * 80)
for roto in ROTOS:
    if roto not in mapa:
        safe(f"  {roto}  (ya no se usa, no requiere fix)")

# ============================================================
# 5) Contar archivos unicos afectados
# ============================================================
archivos_afectados = set()
for refs in mapa.values():
    for tpl, _, _ in refs:
        archivos_afectados.add(tpl)

safe("")
safe("=" * 80)
safe(f"ARCHIVOS DE TEMPLATE AFECTADOS: {len(archivos_afectados)}")
safe("=" * 80)
for a in sorted(archivos_afectados):
    safe(f"  {a}")