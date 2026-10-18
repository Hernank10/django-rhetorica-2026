"""Servicio de filologia comparada. Funciones puras, sin BD."""
import unicodedata

from ._etimos_filologia import ETIMOS


def _normalizar(texto):
    """Quita acentos, pasa a minusculas y colapsa espacios."""
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_acentos = "".join(c for c in nfkd if not unicodedata.combining(c))
    return " ".join(sin_acentos.lower().split())


def buscar_etimo(termino):
    """Busca etimos por latin, es_patrimonial, es_cultismo, en_cognado o categoria.

    Substring, case-insensitive, sin acentos. Retorna list[dict].
    """
    if not termino:
        return []
    q = _normalizar(termino)
    if not q:
        return []

    resultados = []
    for etimo in ETIMOS:
        campos = (
            etimo.get("latin"),
            etimo.get("es_patrimonial"),
            etimo.get("es_cultismo"),
            etimo.get("en_cognado"),
            etimo.get("categoria"),
        )
        for c in campos:
            if c and q in _normalizar(c):
                resultados.append(etimo)
                break
    return resultados


def cadena_evolutiva(etimo_latin):
    """Retorna el dict completo del etimo si coincide con latin exacto.

    Case-insensitive, sin acentos. Retorna None si no existe.
    """
    if not etimo_latin:
        return None
    q = _normalizar(etimo_latin)
    for etimo in ETIMOS:
        if _normalizar(etimo.get("latin", "")) == q:
            return etimo
    return None


def categorias_disponibles():
    """Lista ordenada de categorias unicas presentes en ETIMOS."""
    return sorted({e["categoria"] for e in ETIMOS if e.get("categoria")})