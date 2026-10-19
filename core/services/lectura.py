"""Servicio de lectura asistida. Preparacion de texto + morfologia contextual."""
import re

from core.services.pos import POS_ES, modelo_disponible


_PATRON_PALABRA = re.compile(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]+")


def segmentar_texto(texto):
    """Divide el texto en segmentos con posiciones.

    Cada segmento: {"tipo", "texto", "inicio", "fin"}.
    Tipos: "palabra" | "espacio" | "puntuacion" | "otro".
    Permite reconstruir el texto original sumando texto de cada segmento.
    """
    if not texto:
        return []

    segmentos = []
    i = 0
    n = len(texto)
    while i < n:
        ch = texto[i]
        if ch.isspace():
            j = i
            while j < n and texto[j].isspace():
                j += 1
            segmentos.append({"tipo": "espacio", "texto": texto[i:j], "inicio": i, "fin": j})
            i = j
        elif _PATRON_PALABRA.match(ch):
            j = i
            while j < n and _PATRON_PALABRA.match(texto[j]):
                j += 1
            segmentos.append({"tipo": "palabra", "texto": texto[i:j], "inicio": i, "fin": j})
            i = j
        elif ch in ".,;:!?¿¡\"'()[]{}":
            segmentos.append({"tipo": "puntuacion", "texto": ch, "inicio": i, "fin": i + 1})
            i += 1
        else:
            segmentos.append({"tipo": "otro", "texto": ch, "inicio": i, "fin": i + 1})
            i += 1
    return segmentos


def _nlp_md(texto):
    """Carga es_core_news_md (o fallback sm). Retorna doc o None."""
    if not texto or not str(texto).strip():
        return None
    if not modelo_disponible():
        return None
    from core.services.pos import _cargar
    try:
        return _cargar("es_core_news_md")(str(texto))
    except Exception:
        try:
            return _cargar()(str(texto))
        except Exception:
            return None


def morfologia_contextual(texto, offset):
    """Retorna morfologia de la palabra en `offset` (char index).

    Si `offset` cae fuera de una palabra (espacio, puntuacion), retorna
    la palabra mas cercana a la derecha. Si no hay texto o modelo,
    retorna dict neutro con disponible=False.
    """
    neutro = {
        "disponible": False, "palabra": "", "lemma": "", "pos": "",
        "pos_es": "", "dep": "", "head": "", "oracion": "",
    }
    if not texto or offset is None or offset < 0:
        return neutro

    doc = _nlp_md(texto)
    if doc is None:
        return neutro

    token = None
    for t in doc:
        if t.idx <= offset < t.idx + len(t.text):
            token = t
            break
    if token is None:
        return neutro

    oracion = ""
    for sent in doc.sents:
        if sent.start <= token.i < sent.end:
            oracion = sent.text.strip()
            break

    return {
        "disponible": True,
        "palabra": token.text,
        "lemma": token.lemma_,
        "pos": token.pos_,
        "pos_es": POS_ES.get(token.pos_, token.pos_),
        "dep": token.dep_,
        "head": token.head.text,
        "oracion": oracion,
    }


def estadisticas_texto(texto):
    """Metricas agregadas del texto."""
    vacio = {"n_palabras": 0, "n_oraciones": 0, "longitud_media_palabra": 0.0,
             "distribucion_pos": {}, "disponible": False}
    if not texto or not str(texto).strip():
        return vacio

    doc = _nlp_md(texto)
    if doc is None:
        # Sin modelo: solo cuenta palabras y oraciones
        palabras = [s for s in segmentar_texto(texto) if s["tipo"] == "palabra"]
        n_oraciones = len([s for s in segmentar_texto(texto)
                          if s["tipo"] == "puntuacion" and s["texto"] in ".!?"])
        long_media = (sum(len(p["texto"]) for p in palabras) / len(palabras)) if palabras else 0.0
        return {
            "n_palabras": len(palabras),
            "n_oraciones": max(n_oraciones, 1) if palabras else 0,
            "longitud_media_palabra": round(long_media, 1),
            "distribucion_pos": {},
            "disponible": False,
        }

    from collections import Counter
    tokens = [t for t in doc if not t.is_punct and not t.is_space]
    dist = Counter(POS_ES.get(t.pos_, t.pos_) for t in tokens)
    long_media = (sum(len(t.text) for t in tokens) / len(tokens)) if tokens else 0.0
    return {
        "n_palabras": len(tokens),
        "n_oraciones": len(list(doc.sents)),
        "longitud_media_palabra": round(long_media, 1),
        "distribucion_pos": dict(dist),
        "disponible": True,
    }