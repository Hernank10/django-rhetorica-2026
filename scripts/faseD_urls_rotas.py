"""Fase D: arreglar URLs rotas + limpiar templates legacy + test de validacion."""
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# ============================================================
# 1) FIX base.html: rename core:X -> X
# ============================================================
BASE_HTML = BASE / "core" / "templates" / "core" / "base.html"
c = BASE_HTML.read_text(encoding="utf-8")

RENAMES = [
    ("core:login", "login"),
    ("core:logout", "logout"),
    ("core:registro", "registro"),
    ("core:perfil_usuario", "perfil_usuario"),
    ("core:certificaciones_lista", "certificaciones_lista"),
    ("core:dashboard_gamificacion", "dashboard_gamificacion"),
]

cambios_base = 0
for viejo, nuevo in RENAMES:
    patron = "{% url '" + viejo + "'"
    reemplazo = "{% url '" + nuevo + "'"
    if patron in c:
        c = c.replace(patron, reemplazo)
        cambios_base += 1
        safe(f"  [OK] base.html: {viejo} -> {nuevo}")

if cambios_base > 0:
    BASE_HTML.write_text(c, encoding="utf-8")
    safe(f"[OK] base.html actualizado ({cambios_base} renames)")
else:
    safe("[SKIP] base.html no tenia URLs rotas con core:")


# ============================================================
# 2) Verificar que los 5 legacy no esten renderizados
# ============================================================
LEGACY = [
    "core/templates/core/admin_panel.html",
    "core/templates/core/cursos/leccion.html",
    "core/templates/core/examen.html",
    "core/templates/core/practicar_pregunta.html",
    "core/templates/core/preguntas/lista.html",
]

safe("")
safe("=" * 70)
safe("VERIFICANDO QUE LOS LEGACY NO SE RENDERIZAN")
safe("=" * 70)

# Extraer todos los render(request, 'X') de views activas
patron_render = re.compile(r'render\s*\(\s*[^,]+,\s*["\']([^"\']+)["\']')
templates_renderizados = set()

# Buscar en TODO el codigo de produccion de core/
for py in BASE.rglob("*.py"):
    if "__pycache__" in str(py) or "migrations" in str(py) or "scripts" in str(py):
        continue
    try:
        txt = py.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for m in patron_render.finditer(txt):
        templates_renderizados.add(m.group(1))

safe(f"Templates renderizados por alguna vista: {len(templates_renderizados)}")

legacy_seguros = []
legacy_en_uso = []

for leg in LEGACY:
    # El template en formato normalizado: "core/cursos/leccion.html"
    nombre = leg.replace("core/templates/", "")
    if nombre in templates_renderizados:
        legacy_en_uso.append(leg)
        safe(f"  [!] EN USO: {leg}")
    else:
        legacy_seguros.append(leg)
        safe(f"  [OK] No renderizado: {leg}")

if legacy_en_uso:
    safe("")
    safe("[ABORT] Hay templates legacy en uso. No borramos nada.")
    sys.exit(1)


# ============================================================
# 3) Borrar legacy con git rm
# ============================================================
safe("")
safe("=" * 70)
safe("BORRANDO LEGACY HUERFANOS")
safe("=" * 70)

for leg in legacy_seguros:
    r = subprocess.run(f'git rm "{leg}"', shell=True, cwd=str(BASE), capture_output=True, text=True)
    if r.returncode == 0:
        safe(f"  [OK] git rm {leg}")
    else:
        safe(f"  [!] Fallo git rm {leg}: {r.stderr.strip()}")


# ============================================================
# 4) Crear test de validacion de URLs en templates
# ============================================================
safe("")
safe("=" * 70)
safe("CREANDO TEST DE VALIDACION")
safe("=" * 70)

test_content = '''"""Test de validacion: cada {% url %} en templates debe resolver.

Detecta automaticamente:
  - URLs rotas (nombre no registrado)
  - Namespaces inexistentes (ej: core:login cuando no hay namespace core)

Previene el bug historico de {% url 'core:login' %} -> 500.
"""
import re
from pathlib import Path

import pytest
from django.urls import NoReverseMatch, reverse


# Templates que SI se renderizan en produccion (whitelist estricta)
TEMPLATES_CRITICOS = [
    "core/templates/base.html",
    "core/templates/core/base.html",
    "core/templates/core/profesor/base.html",
    "core/templates/core/estudiante/base.html",
    "core/templates/core/cursos/detalle_completo.html",
    "core/templates/core/cursos/leccion_detalle.html",
    "core/templates/core/cursos/evaluacion_detalle.html",
    "core/templates/core/cursos/resultado_evaluacion.html",
]


def _extraer_urls_de_template(path):
    """Devuelve lista de (nombre_url, lineno, texto)."""
    if not path.exists():
        return []
    c = path.read_text(encoding="utf-8", errors="replace")
    lineas = c.split("\\n")
    patron = re.compile(r"{%\\s*url\\s+['\\\"]([^'\\\"]+)['\\\"]")
    resultado = []
    for m in patron.finditer(c):
        nombre = m.group(1)
        lineno = c[:m.start()].count("\\n") + 1
        resultado.append((nombre, lineno, lineas[lineno - 1].strip()[:100]))
    return resultado


class TestUrlsEnTemplatesCriticos:
    """Verifica que las URLs referenciadas en templates criticos existen."""

    def test_base_html_no_tiene_urls_rotas(self):
        path = Path("core/templates/base.html")
        urls = _extraer_urls_de_template(path)
        rotas = []
        for nombre, lineno, texto in urls:
            try:
                reverse(nombre)
            except NoReverseMatch:
                # Algunos nombres con args requieren kwargs, los saltamos
                # (solo verificamos que el NOMBRE este registrado)
                rotas.append((nombre, lineno, texto))

        assert not rotas, (
            "base.html tiene URLs rotas:\\n" +
            "\\n".join(f"  L{ln}: {n}  ({t})" for n, ln, t in rotas)
        )

    def test_todos_los_templates_de_core_no_tienen_urls_rotas(self):
        """Escanea TODOS los templates de core/ y reporta rotas."""
        base_dir = Path("core/templates/core")
        rotas_totales = []

        for tpl in base_dir.rglob("*.html"):
            urls = _extraer_urls_de_template(tpl)
            for nombre, lineno, texto in urls:
                # Ignorar URLs con namespace admin (las provee Django admin)
                if nombre.startswith("admin:"):
                    continue
                # Ignorar set_language (provee django)
                if nombre == "set_language":
                    continue
                try:
                    reverse(nombre)
                except NoReverseMatch:
                    rel = tpl.relative_to(Path("core/templates/core"))
                    rotas_totales.append((str(rel), nombre, lineno))

        if rotas_totales:
            mensaje = "URLs rotas encontradas:\\n"
            for archivo, nombre, lineno in rotas_totales:
                mensaje += f"  {archivo}:{lineno}  ->  {nombre}\\n"
            pytest.fail(mensaje)
'''

test_path = BASE / "core" / "tests" / "test_urls_templates.py"
test_path.write_text(test_content, encoding="utf-8")
safe(f"[OK] {test_path.relative_to(BASE)}")


# ============================================================
# 5) Verificacion
# ============================================================
safe("")
safe("=" * 70)
safe("VERIFICACION")
safe("=" * 70)

# manage.py check
r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe manage.py check",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
safe(f"  manage.py check -> exit={r.returncode}")
if r.stdout.strip():
    safe(f"    {r.stdout.strip()[:200]}")

# pytest del test nuevo
r = subprocess.run(
    r"E:\PythonPortable_Django5\python.exe -m pytest core\tests\test_urls_templates.py -v --tb=short -p no:cacheprovider",
    shell=True, cwd=str(BASE), capture_output=True, text=True,
)
safe(f"  pytest test_urls_templates.py -> exit={r.returncode}")
for l in (r.stdout + r.stderr).split("\\n")[-15:]:
    if l.strip():
        safe(f"    {l}")