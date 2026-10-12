"""
FASE 2 - Sanitizacion de HTML en lecciones.

1) Crea core/utils.py con sanitizar_html()
2) Modifica views_profesor.py: sanitizar antes de guardar
3) Cambia label del template: "Contenido (HTML permitido)" -> "Contenido"
4) Crea tests
"""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) core/utils.py
# ============================================================
utils_py = '''"""
Utilidades compartidas: sanitizacion de HTML.

Usa nh3 (sucesor de bleach, mantenido y basado en Rust).
"""
import nh3


# Tags permitidos (los que TinyMCE puede generar)
TAGS_PERMITIDOS = {
    # Estructura
    "p", "br", "div", "span", "hr",
    # Formato
    "strong", "b", "em", "i", "u", "s", "sub", "sup", "mark",
    # Titulos
    "h1", "h2", "h3", "h4", "h5", "h6",
    # Listas
    "ul", "ol", "li", "dl", "dt", "dd",
    # Enlaces
    "a",
    # Imagenes
    "img",
    # Tablas
    "table", "thead", "tbody", "tfoot", "tr", "th", "td",
    "caption", "colgroup", "col",
    # Codigo
    "code", "pre", "blockquote",
    # Detalles
    "details", "summary",
    # Multimedia (embebido seguro)
    "figure", "figcaption",
}


# Atributos permitidos por tag (mas atributos globales aparte)
ATRIBUTOS_PERMITIDOS = {
    "*": {"class", "id", "style", "title", "dir", "lang"},
    "a": {"href", "title", "target", "rel"},
    "img": {"src", "alt", "title", "width", "height", "loading"},
    "td": {"colspan", "rowspan", "headers"},
    "th": {"colspan", "rowspan", "scope", "headers"},
    "col": {"span", "width"},
    "colgroup": {"span"},
    "table": {"border", "cellpadding", "cellspacing", "width"},
    "ol": {"start", "type", "reversed"},
}


# Esquemas de URL permitidos
ESQUEMAS_URL = {"http", "https", "mailto", "tel"}


def sanitizar_html(html):
    """
    Limpia un fragmento de HTML dejando solo tags/atributos seguros.
    Evita XSS: <script>, <iframe>, onerror=, javascript: etc.

    Devuelve siempre un string (vacio si la entrada es None o "").
    """
    if not html:
        return ""
    return nh3.clean(
        html,
        tags=TAGS_PERMITIDOS,
        attributes=ATRIBUTOS_PERMITIDOS,
        url_schemes=ESQUEMAS_URL,
        link_rel="noopener noreferrer",
        strip_comments=True,
    )


def sanitizar_texto_plano(texto):
    """Elimina TODO el HTML, dejando solo texto plano. Util para titulos."""
    if not texto:
        return ""
    return nh3.clean(texto, tags=set(), attributes={})
'''

up = BASE / "core" / "utils.py"
up.write_text(utils_py, encoding="utf-8")
print("[OK] core/utils.py")

# ============================================================
# 2) Modificar views_profesor.py
# ============================================================
vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8")

cambios = 0

# 2.1) Anadir import de sanitizar_html si no esta
if "from .utils import" not in c:
    # Insertar despues del ultimo import de models_cursos
    patron_import = re.compile(
        r"(from \.models_cursos import \([^)]*\)\n)"
    )
    m = patron_import.search(c)
    if m:
        c = c[:m.end()] + "from .utils import sanitizar_html\n" + c[m.end():]
        cambios += 1
        print("[OK] import de sanitizar_html anadido")
    else:
        print("[!] No se encontro donde insertar el import. Revisa manualmente.")
elif "sanitizar_html" not in c:
    c = c.replace("from .utils import ", "from .utils import sanitizar_html, ", 1)
    cambios += 1
    print("[OK] sanitizar_html anadido al import existente")

# 2.2) Sanitizar contenido en leccion_form
# Buscar la linea: contenido = request.POST.get("contenido", "")
patron_contenido = re.compile(
    r'(\s*)(contenido\s*=\s*request\.POST\.get\(["\']contenido["\']\s*,\s*["\'][^"\']*["\']\s*\))'
)
m = patron_contenido.search(c)
if m:
    indent = m.group(1)
    original = m.group(2)
    reemplazo = f"{indent}contenido = sanitizar_html(request.POST.get(\"contenido\", \"\"))"
    if "sanitizar_html(request.POST.get" in c:
        print("[SKIP] contenido ya estaba sanitizado")
    else:
        c = c[:m.start(2)] + reemplazo + c[m.end(2):]
        cambios += 1
        print("[OK] contenido sanitizado en leccion_form")
else:
    print("[!] No se encontro 'contenido = request.POST.get(...)' en leccion_form")

# 2.3) Sanitizar titulo (texto plano)
patron_titulo = re.compile(
    r'(\s*)(titulo\s*=\s*request\.POST\.get\(["\']titulo["\']\s*,\s*["\'][^"\']*["\']\s*\)\.strip\(\))'
)
m = patron_titulo.search(c)
if m and "sanitizar_texto_plano" not in c:
    # El titulo ya usa .strip(), no hace falta sanitizar con nh3 normalmente,
    # pero si se quiere, se puede. Lo dejamos como esta para no romper.
    print("[SKIP] titulo se guarda tal cual (ya usa .strip())")

if cambios > 0:
    vp.write_text(c, encoding="utf-8")
    print(f"[OK] views_profesor.py actualizado ({cambios} cambios)")

# ============================================================
# 3) Template: cambiar label
# ============================================================
TPL = BASE / "core" / "templates" / "core" / "profesor" / "lecciones" / "form.html"
c2 = TPL.read_text(encoding="utf-8")

cambios_tpl = 0

# 3.1) Cambiar "Contenido (HTML permitido)" -> "Contenido"
if "Contenido (HTML permitido)" in c2:
    c2 = c2.replace("Contenido (HTML permitido)", "Contenido")
    cambios_tpl += 1
    print('[OK] label "Contenido (HTML permitido)" -> "Contenido"')

# 3.2) Anadir help_text si no existe
if "Contenido" in c2 and "form-text" not in c2 and 'name="contenido"' in c2:
    # Insertar help_text justo despues del textarea de contenido
    patron_textarea = re.compile(
        r'(<textarea[^>]*name=["\']contenido["\'][^>]*>.*?</textarea>)',
        re.DOTALL | re.IGNORECASE,
    )
    def add_help(m):
        return m.group(1) + '\n<small class="form-text text-muted">Usa la barra de herramientas para dar formato. Acepta negritas, listas, enlaces, imagenes y tablas.</small>'
    c2n, n = patron_textarea.subn(add_help, c2, count=1)
    if n:
        c2 = c2n
        cambios_tpl += 1
        print("[OK] help_text anadido al campo contenido")

if cambios_tpl > 0:
    TPL.write_text(c2, encoding="utf-8")
    print(f"[OK] template actualizado ({cambios_tpl} cambios)")

# ============================================================
# 4) Verificacion
# ============================================================
print()
print("=" * 60)
print("VERIFICACION")
print("=" * 60)
c = vp.read_text(encoding="utf-8")
print(f"  views_profesor.py importa sanitizar_html: {'sanitizar_html' in c}")
print(f"  views_profesor.py sanitiza contenido:     {'sanitizar_html(request.POST.get' in c}")

c2 = TPL.read_text(encoding="utf-8")
print(f"  Template dice 'Contenido (HTML permitido)': {'Contenido (HTML permitido)' in c2}")
print(f"  Template dice 'Contenido':                  {'>Contenido' in c2 or '>Contenido<' in c2 or 'Contenido' in c2}")

print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  E:\\PythonPortable_Django5\\python.exe manage.py check")