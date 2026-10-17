"""Servicio de evaluacion morfosintactica. Funciones puras."""

import re

from ._diccionarios_redaccion import COORDINANTES, MARCADORES_PARRAFO, SUBORDINANTES

MIN_PALABRAS = 3
MAX_PALABRAS = 500

# Lista blanca de verbos conjugados comunes (mas preciso que terminaciones)
VERBOS_LISTA_BLANCA = {
    "es", "son", "era", "eran", "fue", "fueron", "sera", "seran", "sido",
    "esta", "estan", "estaba", "estaban", "estuvo", "estuvieron",
    "tiene", "tienen", "tenia", "tenian", "tuvo", "tuvieron",
    "hay", "habia", "hubo",
    "hace", "hacen", "hacia", "hacian", "hizo", "hicieron",
    "puede", "pueden", "podia", "podian",
    "quiere", "quieren", "queria", "querian",
    "estudia", "estudian", "estudiaba", "estudiaban", "estudio", "estudie",
    "corre", "corren", "corria", "corrian", "corrio",
    "nada", "nadan", "nadaba", "nadaban", "nado",
    "juega", "juegan", "jugaba", "jugaban", "jugo",
    "vino", "vinieron", "viene", "vienen", "venia", "venian",
    "trabaja", "trabajan", "trabajaba", "trabajaban", "trabajo",
    "llega", "llegan", "llego", "llegaron", "llegaba",
    "debes", "debe", "deben", "debia",
    "fuimos", "vamos", "van", "iba", "iban",
    "cenamos", "ceno", "comio", "comemos",
    "dijo", "dijeron", "dice", "dicen",
    "cree", "creen", "creia",
    "pienso", "piensan", "penso", "pensaba",
    "opino", "opinan", "considero", "consideran",
    "sabe", "saben", "sabia", "sabemos",
    "afirmo", "afirman",
}

VERBOS_PENSAMIENTO = {
    "pienso", "pensaba", "penso", "creo", "creia", "cree",
    "digo", "dice", "dijo", "opino", "considero", "afirmo",
    "sabe", "sabemos", "sabia", "se",
}

PREPOSICIONES = {
    "a", "ante", "bajo", "con", "contra", "de", "desde",
    "en", "entre", "hacia", "hasta", "para", "por", "segun",
    "sin", "sobre", "tras", "el", "la", "los", "las", "un",
    "una", "unos", "unas", "mi", "tu", "su", "nuestro",
}


def _normalizar(texto):
    return " ".join(texto.lower().split()) if texto else ""


def _tokenizar_oraciones(texto):
    if not texto:
        return []
    return [s.strip() for s in re.split(r"[.!?]+", texto) if s.strip()]


def _contar_verbos(oracion):
    tokens = re.findall(r"\b[a-záéíóúñ]+\b", oracion.lower())
    verbos = 0
    for t in tokens:
        if t in VERBOS_LISTA_BLANCA:
            verbos += 1
            continue
        if len(t) < 3:
            continue
        if t.endswith(("ando", "iendo")):
            verbos += 1
        elif t.endswith(("amos", "aron", "ieron", "aba", "aban")):
            verbos += 1
        elif t.endswith(("aste", "iste")):
            verbos += 1
    return verbos


def _encontrar_conectores(texto):
    texto_lower = texto.lower()
    encontrados = []
    for nexo in sorted(COORDINANTES.keys(), key=len, reverse=True):
        patron = r"\b" + re.escape(nexo) + r"\b"
        for m in re.finditer(patron, texto_lower):
            encontrados.append({
                "texto": nexo, "tipo": COORDINANTES[nexo],
                "posicion": m.start(), "categoria": "coordinante",
            })
    for nexo in sorted(SUBORDINANTES.keys(), key=len, reverse=True):
        patron = r"\b" + re.escape(nexo) + r"\b"
        for m in re.finditer(patron, texto_lower):
            encontrados.append({
                "texto": nexo, "tipo": SUBORDINANTES[nexo],
                "posicion": m.start(), "categoria": "subordinante",
            })
    return encontrados


def _clasificar_subordinada_por_contexto(nexo, posicion, texto):
    """Para 'que': sustantiva tras verbo de pensamiento, adjetiva tras sustantivo."""
    tipo_default = SUBORDINANTES.get(nexo, "desconocida")

    if nexo != "que":
        if tipo_default.startswith("adjetiva"):
            return "adjetiva"
        if tipo_default.startswith("sustantiva"):
            return "sustantiva"
        if tipo_default.startswith("adverbial"):
            return "adverbial"
        return tipo_default

    antes = texto[:posicion].strip().split()
    if not antes:
        return "sustantiva"

    anterior = antes[-1].lower()
    if anterior in VERBOS_PENSAMIENTO:
        return "sustantiva"
    if anterior in VERBOS_LISTA_BLANCA:
        return "sustantiva"
    if anterior in PREPOSICIONES:
        return "sustantiva"

    # Si el anterior no es verbo ni preposicion → probablemente sustantivo → adjetiva
    return "adjetiva"


def analizar_oracion(texto):
    normalizado = _normalizar(texto)
    palabras = normalizado.split()
    if len(palabras) < MIN_PALABRAS:
        return {"tipo": "insuficiente", "n_oraciones": 0, "n_verbos": 0,
                "conectores": [], "subordinadas": [],
                "longitud_palabras": len(palabras),
                "error": "Texto demasiado corto"}
    if len(palabras) > MAX_PALABRAS:
        return {"tipo": "demasiado_largo", "n_oraciones": 0, "n_verbos": 0,
                "conectores": [], "subordinadas": [],
                "longitud_palabras": len(palabras),
                "error": "Maximo 500 palabras"}

    oraciones = _tokenizar_oraciones(normalizado)
    n_verbos = sum(_contar_verbos(o) for o in oraciones)
    conectores = _encontrar_conectores(normalizado)
    coordinantes = [c for c in conectores if c["categoria"] == "coordinante"]
    subordinantes = [c for c in conectores if c["categoria"] == "subordinante"]

    subordinadas = []
    for c in subordinantes:
        tipo = _clasificar_subordinada_por_contexto(c["texto"], c["posicion"], normalizado)
        subordinadas.append({"tipo": tipo, "nexo": c["texto"]})

    if n_verbos <= 1 and not coordinantes and not subordinantes:
        tipo = "simple"
    elif subordinantes:
        tipo = "compuesta_subordinada"
    elif coordinantes:
        tipo = "compuesta_coordinada"
    elif len(oraciones) >= 2 or n_verbos >= 2:
        tipo = "yuxtapuesta"
    else:
        tipo = "simple"

    return {
        "tipo": tipo, "n_oraciones": len(oraciones), "n_verbos": n_verbos,
        "conectores": conectores, "subordinadas": subordinadas,
        "longitud_palabras": len(palabras),
    }


def analizar_parrafo(texto):
    normalizado = _normalizar(texto)
    if not normalizado:
        return {"tipo_dominante": "vacio", "n_oraciones": 0,
                "marcadores_por_tipo": {}}
    marcadores = {k: 0 for k in MARCADORES_PARRAFO}
    for categoria, lista in MARCADORES_PARRAFO.items():
        for m in lista:
            marcadores[categoria] += len(
                re.findall(r"\b" + re.escape(m) + r"\b", normalizado)
            )
    maximo = max(marcadores.values())
    if maximo == 0:
        tipo = "neutro"
    else:
        tipo = next(k for k, v in marcadores.items() if v == maximo)
    return {
        "tipo_dominante": tipo,
        "n_oraciones": len(_tokenizar_oraciones(normalizado)),
        "marcadores_por_tipo": marcadores,
    }


_TIPO_MAP = {
    "oracion_simple": "simple",
    "oracion_coordinada": "compuesta_coordinada",
    "oracion_subordinada": "compuesta_subordinada",
    "oracion_yuxtapuesta": "yuxtapuesta",
    "parrafo_narrativo": "narrativos",
    "parrafo_descriptivo": "descriptivos",
    "parrafo_argumentativo": "argumentativos",
    "parrafo_expositivo": "expositivos",
}


def evaluar_ejercicio(texto, tipo_esperado):
    if tipo_esperado.startswith("parrafo_"):
        analisis = analizar_parrafo(texto)
        esperado = _TIPO_MAP.get(tipo_esperado, "")
        aprobado = analisis["tipo_dominante"] == esperado
        if aprobado:
            feedback = "Correcto. Parrafo " + analisis["tipo_dominante"] + "."
        else:
            feedback = "Pedimos parrafo " + esperado + ". Detectamos " + analisis["tipo_dominante"] + "."
    else:
        analisis = analizar_oracion(texto)
        esperado = _TIPO_MAP.get(tipo_esperado, "")
        aprobado = analisis["tipo"] == esperado
        if aprobado:
            feedback = "Correcto. Tipo detectado: " + analisis["tipo"] + "."
        else:
            feedback = "Pedimos " + esperado + ". Detectamos " + analisis["tipo"] + "."
    return {
        "aprobado": aprobado,
        "tipo_detectado": analisis.get("tipo") or analisis.get("tipo_dominante"),
        "analisis": analisis,
        "feedback": feedback,
    }


def clasificar_error(texto, tipo_esperado):
    r = evaluar_ejercicio(texto, tipo_esperado)
    if r["aprobado"]:
        return None
    return {
        "categoria_gramatical": tipo_esperado,
        "patron_error": r["tipo_detectado"] + "_en_lugar_de_" + tipo_esperado,
        "idioma": "ES",
    }
