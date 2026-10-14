"""
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
    "*": {"class", "id", "title", "dir", "lang"},  # SIN "style" (XSS via url(javascript:))
    "a": {"href", "title", "target"},  # nh3 gestiona "rel" via link_rel
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
