from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Ver el contexto del mensaje en core/views.py
# ============================================================
print("=" * 60)
print("CONTEXTO DEL MENSAJE EN core/views.py")
print("=" * 60)
vp = BASE / "core" / "views.py"
c = vp.read_text(encoding="utf-8")

idx = 0
veces = 0
while True:
    idx = c.find("Usuario no encontrado", idx)
    if idx == -1:
        break
    veces += 1
    # Buscar el "def " anterior
    lineas_antes = c[:idx].split("\n")
    vista = "?"
    for i in range(len(lineas_antes)-1, -1, -1):
        if lineas_antes[i].strip().startswith("def "):
            vista = lineas_antes[i].strip()
            break
    print(f"\n[{veces}] En vista: {vista}")
    print(c[max(0,idx-200):idx+100])
    idx += 1

print(f"\nTotal: {veces} apariciones")

# ============================================================
# 2) Reemplazar el mensaje por silencio (pass)
# ============================================================
if veces > 0:
    print()
    print("=" * 60)
    print("SILENCIANDO MENSAJES")
    print("=" * 60)
    # Reemplazar cualquier variante del mensaje
    patrones = [
        (r'print\([^)]*["\']❌ Usuario no encontrado[^"\']*["\'][^)]*\)', 'pass  # silenciado'),
        (r'print\([^)]*["\']Usuario no encontrado[^"\']*["\'][^)]*\)', 'pass  # silenciado'),
        (r'messages\.(error|warning|info)\([^)]*["\']❌ Usuario no encontrado[^"\']*["\'][^)]*\)', 'pass  # silenciado'),
    ]
    for pat, rep in patrones:
        c2, n = re.subn(pat, rep, c)
        if n:
            print(f"[OK] {n} ocurrencia(s) silenciada(s) con patrón: {pat[:40]}...")
            c = c2
    vp.write_text(c, encoding="utf-8")

# ============================================================
# 3) Chart.js local
# ============================================================
print()
print("=" * 60)
print("CHART.JS LOCAL")
print("=" * 60)
js_dir = BASE / "static" / "js"
js_dir.mkdir(parents=True, exist_ok=True)
js_file = js_dir / "chart.umd.min.js"

if not js_file.exists() or js_file.stat().st_size < 50000:
    try:
        import urllib.request
        url = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"
        urllib.request.urlretrieve(url, str(js_file))
        print(f"[OK] Chart.js descargado: {js_file.stat().st_size} bytes")
    except Exception as e:
        print(f"[!] No se pudo descargar Chart.js: {e}")
        print(f"    Descarga manual: {url}")
        print(f"    Guárdalo en: {js_file}")
else:
    print(f"[SKIP] Chart.js ya existe: {js_file.stat().st_size} bytes")

# ============================================================
# 4) Cambiar templates a Chart.js local
# ============================================================
print()
print("=" * 60)
print("TEMPLATES → CHART.JS LOCAL")
print("=" * 60)

templates = [
    BASE / "core" / "templates" / "core" / "estudiante" / "dashboard.html",
    BASE / "core" / "templates" / "core" / "estudiante" / "mis_estadisticas.html",
    BASE / "core" / "templates" / "core" / "profesor" / "estadisticas.html",
]

for t in templates:
    if not t.exists():
        print(f"[SKIP] {t.name} no existe")
        continue
    c = t.read_text(encoding="utf-8")
    if "js/chart.umd.min.js" in c:
        print(f"[SKIP] {t.name} ya usa local")
        continue
    if "cdn.jsdelivr.net/npm/chart.js" in c:
        # Asegurar {% load static %} al inicio
        if "{% load static %}" not in c.split("\n", 5)[0:5]:
            if c.lstrip().startswith("{% extends"):
                # Insertar {% load static %} después de la primera línea extends
                c = re.sub(
                    r"(\{%\s*extends[^%]*%\}\s*\r?\n)",
                    r"\1{% load static %}\n",
                    c, count=1
                )
            else:
                c = "{% load static %}\n" + c
        # Reemplazar el script
        c = re.sub(
            r'<script src="https://cdn\.jsdelivr\.net/npm/chart\.js[^"]*"></script>',
            "<script src=\"{% static 'js/chart.umd.min.js' %}\"></script>",
            c
        )
        t.write_text(c, encoding="utf-8")
        print(f"[OK] {t.name} → Chart.js local")
    else:
        print(f"[?] {t.name} no tiene script Chart.js")