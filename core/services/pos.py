"""Analisis morfosintactico con spaCy. Degrada gracefully sin modelo."""
from functools import lru_cache

POS_ES = {
    "NOUN": "sustantivo",
    "VERB": "verbo",
    "ADJ": "adjetivo",
    "ADP": "preposicion",
    "DET": "determinante",
    "PRON": "pronombre",
    "CCONJ": "conjuncion coordinante",
    "SCONJ": "conjuncion subordinante",
    "AUX": "verbo auxiliar",
    "ADV": "adverbio",
    "NUM": "numeral",
    "PROPN": "nombre propio",
    "PUNCT": "puntuacion",
    "INTJ": "interjeccion",
    "PART": "particula",
    "SYM": "simbolo",
    "X": "desconocido",
}

MODELO_DEFAULT = "es_core_news_sm"


@lru_cache(maxsize=4)
def _cargar(nombre=MODELO_DEFAULT):
    """Carga spaCy + modelo. Cachea el resultado por nombre."""
    import spacy
    return spacy.load(nombre)


def modelo_disponible(nombre=MODELO_DEFAULT):
    """True si spaCy y el modelo cargan correctamente."""
    try:
        _cargar(nombre)
        return True
    except Exception:
        return False


def analizar_frase(texto, incluir_dependencias=True, modelo=MODELO_DEFAULT):
    """Analiza una frase y retorna tokens con POS, lemma y dependencia.

    Retorna dict:
        disponible: bool  (False si spaCy/modelo no cargan)
        tokens:     list[dict]
        oraciones:  int
        error:      str | None
    """
    if not texto or not str(texto).strip():
        return {
            "disponible": True,
            "tokens": [],
            "oraciones": 0,
            "error": None,
        }

    try:
        nlp = _cargar(modelo)
    except Exception as e:
        return {
            "disponible": False,
            "tokens": [],
            "oraciones": 0,
            "error": f"spaCy no disponible: {type(e).__name__}: {e}",
        }

    doc = nlp(str(texto))
    tokens = []
    for i, t in enumerate(doc):
        tokens.append({
            "texto": t.text,
            "lemma": t.lemma_,
            "pos": t.pos_,
            "pos_es": POS_ES.get(t.pos_, t.pos_),
            "dep": t.dep_ if incluir_dependencias else "",
            "head_idx": t.head.i if incluir_dependencias else -1,
            "es_stop": t.is_stop,
            "es_punct": t.is_punct,
        })

    return {
        "disponible": True,
        "tokens": tokens,
        "oraciones": len(list(doc.sents)),
        "error": None,
    }


def estadisticas_pos(tokens):
    """Cuenta tokens por POS en espanol. Retorna dict {pos_es: count}."""
    from collections import Counter
    c = Counter(t["pos_es"] for t in tokens if t.get("pos_es"))
    return dict(c)