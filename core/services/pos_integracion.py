"""Integracion de spaCy con el motor de redaccion.

Agrega analisis de concordancia y funciones sintacticas donde la heuristica
del modulo 4 es debil. Degrada gracefully: si spaCy no esta, todas las
funciones retornan valores neutros.
"""
from core.services.pos import modelo_disponible
from core.services.redaccion import evaluar_ejercicio


def _nlp(texto):
    """Retorna doc spaCy o None si no hay modelo/texto."""
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


def _morph_number(tok):
    """Number del token ('Sing'|'Plur'|''). Fallback heuristico si morph vacio."""
    try:
        vals = tok.morph.get("Number")
        if vals:
            return vals[0]
    except Exception:
        pass
    # Fallback: inferir por forma del token (limitado, pero cubre casos comunes)
    t = (tok.text or "").lower()
    if tok.pos_ in ("NOUN", "PROPN", "PRON", "DET"):
        if t.endswith("s") and len(t) > 2 and not t.endswith(("es", "is", "us")):
            return "Plur"
        return "Sing"
    if tok.pos_ in ("VERB", "AUX"):
        if t.endswith(("an", "en", "aron", "ieron", "aban", "ian", "aran", "ieran")):
            return "Plur"
        return "Sing"
    return ""


def concordancia_sujeto_verbo(texto):
    """Verifica concordancia de numero entre sujeto y verbo principal.

    Retorna dict:
        ok: bool
        razon: str
        sujeto: str
        verbo: str
        sujeto_num: "Sing"|"Plur"|""
        verbo_num: "Sing"|"Plur"|""
    """
    vacio = {
        "ok": True, "razon": "sin analisis",
        "sujeto": "", "verbo": "",
        "sujeto_num": "", "verbo_num": "",
    }
    doc = _nlp(texto)
    if doc is None:
        return vacio

    for tok in doc:
        if tok.dep_ not in ("nsubj", "nsubj_pass", "csubj"):
            continue
        head = tok.head
        subj_num = _morph_number(tok)
        verb_num = _morph_number(head)
        if not subj_num or not verb_num:
            return {
                "ok": True, "razon": "numero no detectable",
                "sujeto": tok.text, "verbo": head.text,
                "sujeto_num": subj_num, "verbo_num": verb_num,
            }
        ok = subj_num == verb_num
        return {
            "ok": ok,
            "razon": "concuerdan" if ok else f"sujeto {subj_num} + verbo {verb_num}",
            "sujeto": tok.text,
            "verbo": head.text,
            "sujeto_num": subj_num,
            "verbo_num": verb_num,
        }
    return vacio


def funciones_sintacticas(texto):
    """Extrae funciones sintacticas principales via dependency parsing.

    Retorna dict:
        sujeto: list[str]
        verbo: list[str]
        objeto_directo: list[str]
        objeto_indirecto: list[str]
        oblicuos: list[str]  (SP: "en casa", "con Juan")
        disponible: bool
    """
    vacio = {
        "sujeto": [], "verbo": [], "objeto_directo": [],
        "objeto_indirecto": [], "oblicuos": [], "disponible": False,
    }
    doc = _nlp(texto)
    if doc is None:
        return vacio

    out = {
        "sujeto": [], "verbo": [], "objeto_directo": [],
        "objeto_indirecto": [], "oblicuos": [], "disponible": True,
    }
    for tok in doc:
        if tok.dep_ in ("nsubj", "nsubj_pass", "csubj"):
            out["sujeto"].append(tok.text)
        elif tok.pos_ in ("VERB", "AUX"):
            out["verbo"].append(tok.text)
        elif tok.dep_ == "obj":
            out["objeto_directo"].append(tok.text)
        elif tok.dep_ == "iobj":
            out["objeto_indirecto"].append(tok.text)
        elif tok.dep_ in ("obl", "nmod"):
            caso = ""
            for child in tok.children:
                if child.dep_ == "case":
                    caso = child.text + " "
                    break
            if not caso:
                prev = tok.i - 1
                if prev >= 0 and doc[prev].pos_ == "ADP":
                    caso = doc[prev].text + " "
            out["oblicuos"].append(caso + tok.text)
    return out


def clasificar_que_spacy(texto):
    """Clasifica 'que' como sustantiva/adjetiva/adverbial via dependencias.

    - PRON + nsubj/obj con ancestro acl -> adjetiva
    - SCONJ/PRON con head ccomp -> sustantiva
    - SCONJ/PRON con head advcl -> adverbial
    - sin 'que' -> ""
    """
    doc = _nlp(texto)
    if doc is None:
        return ""

    for tok in doc:
        if tok.text.lower() != "que":
            continue
        if tok.pos_ == "PRON" and tok.dep_ in ("nsubj", "obj", "obl", "nsubj_pass"):
            actual = tok.head
            while actual is not None:
                if actual.dep_ == "acl":
                    return "adjetiva"
                if actual == actual.head:
                    break
                actual = actual.head
        if tok.pos_ in ("SCONJ", "PRON"):
            # sube hasta 3 niveles buscando ccomp/xcomp/advcl en el arbol del head
            actual = tok.head
            for _ in range(3):
                if actual is None:
                    break
                if actual.dep_ in ("ccomp", "xcomp"):
                    return "sustantiva"
                if actual.dep_ == "advcl":
                    return "adverbial"
                if actual == actual.head:
                    break
                actual = actual.head
            # fallback: que como mark -> subordinada verbal -> sustantiva
            if tok.dep_ == "mark":
                return "sustantiva"
    return ""


def evaluar_ejercicio_con_spacy(texto, tipo_esperado):
    """Enriquece evaluar_ejercicio con concordancia_sujeto_verbo."""
    base = evaluar_ejercicio(texto, tipo_esperado)
    base["concordancia"] = concordancia_sujeto_verbo(texto)
    return base