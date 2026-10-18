"""Servicio de analisis de corpus. Funciones puras + gatherers de BD."""
import re
from collections import Counter


_PATRON_TOKEN = re.compile(r"\b[a-záéíóúñü]+\b")

FUENTES = [
    "ejercicio_enunciado",
    "ejercicio_teoria",
    "ejercicio_ejemplo",
    "ejercicio_respuesta_esperada",
    "evaluacion_texto",
    "evaluacion_feedback",
    "flashcard_frente",
    "flashcard_reverso",
    "etimologia_regla",
    "etimologia_ejemplo",
]


def tokenizar(texto):
    """Lowercase + solo letras (con acentos). Texto vacio -> []."""
    if not texto:
        return []
    return _PATRON_TOKEN.findall(texto.lower())


def frecuencias(textos):
    """Cuenta palabras en un iterable de strings. Retorna dict[str, int]."""
    c = Counter()
    for t in textos:
        c.update(tokenizar(t))
    return dict(c)


def concordancias(texto_corpus, termino, contexto=5):
    """KWIC (keyword in context) sobre un texto unico.

    Retorna list[dict] con {izq, palabra, der, posicion}.
    """
    if not termino or not texto_corpus:
        return []
    termino_norm = termino.lower().strip()
    if not termino_norm:
        return []

    tokens = tokenizar(texto_corpus)
    resultado = []
    for i, tok in enumerate(tokens):
        if tok == termino_norm:
            izq = " ".join(tokens[max(0, i - contexto):i])
            der = " ".join(tokens[i + 1:i + 1 + contexto])
            resultado.append({
                "izq": izq,
                "palabra": tokens[i],
                "der": der,
                "posicion": i,
            })
    return resultado


def n_gramas(textos, n=2, top=20):
    """N-gramas mas frecuentes. Retorna list[(tuple, count)]."""
    if n < 1:
        return []
    c = Counter()
    for t in textos:
        tokens = tokenizar(t)
        for i in range(len(tokens) - n + 1):
            c[tuple(tokens[i:i + n])] += 1
    return c.most_common(top)


def corpus_desde_etimos():
    """Etimos del modulo 2 como items de corpus (sin BD)."""
    from ._etimos_filologia import ETIMOS
    items = []
    for e in ETIMOS:
        latin = e.get("latin", "?")
        if e.get("regla"):
            items.append({"texto": e["regla"], "fuente": "etimologia_regla", "id": latin})
        if e.get("ejemplo"):
            items.append({"texto": e["ejemplo"], "fuente": "etimologia_ejemplo", "id": latin})
    return items


def corpus_desde_bd():
    """Corpus agregado de Ejercicio + Evaluacion + Flashcard."""
    from core.models import EjercicioLinguistico, EvaluacionRedaccion, Flashcard

    items = []

    for ej_id, contenido in EjercicioLinguistico.objects.values_list("id", "contenido"):
        c = contenido or {}
        if not isinstance(c, dict):
            continue
        for campo in ("enunciado", "teoria", "ejemplo", "respuesta_esperada"):
            val = c.get(campo)
            if val:
                items.append({
                    "texto": str(val),
                    "fuente": f"ejercicio_{campo}",
                    "id": ej_id,
                })

    for ev_id, texto, fb in EvaluacionRedaccion.objects.values_list(
        "id", "texto_estudiante", "feedback"
    ):
        if texto:
            items.append({"texto": texto, "fuente": "evaluacion_texto", "id": ev_id})
        if fb:
            items.append({"texto": fb, "fuente": "evaluacion_feedback", "id": ev_id})

    for fc_id, frente, reverso in Flashcard.objects.values_list(
        "id", "frente", "reverso"
    ):
        if frente:
            items.append({"texto": frente, "fuente": "flashcard_frente", "id": fc_id})
        if reverso:
            items.append({"texto": reverso, "fuente": "flashcard_reverso", "id": fc_id})

    return items


def corpus_completo():
    """Union de BD + etimos."""
    return corpus_desde_bd() + corpus_desde_etimos()