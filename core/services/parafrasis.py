"""Servicio de parafrasis mecanica. Sin LLM, 100% determinista."""
from core.services.pos import _cargar, modelo_disponible


PARTICIPIOS_IRREGULARES = {
    "abrir": "abierto", "cubrir": "cubierto", "descubrir": "descubierto",
    "escribir": "escrito", "romper": "roto", "hacer": "hecho",
    "decir": "dicho", "ver": "visto", "poner": "puesto",
    "volver": "vuelto", "devolver": "devuelto", "resolver": "resuelto",
    "morir": "muerto", "freir": "frito", "imprimir": "impreso",
}

SER_FORMAS = {
    "Pres": {"1s": "soy", "2s": "eres", "3s": "es", "1p": "somos", "2p": "sois", "3p": "son"},
    "Past": {"1s": "fui", "2s": "fuiste", "3s": "fue", "1p": "fuimos", "2p": "fuisteis", "3p": "fueron"},
    "Imp": {"1s": "era", "2s": "eras", "3s": "era", "1p": "eramos", "2p": "erais", "3p": "eran"},
    "Fut": {"1s": "sere", "2s": "seras", "3s": "sera", "1p": "seremos", "2p": "sereis", "3p": "seran"},
    "Cond": {"1s": "seria", "2s": "serias", "3s": "seria", "1p": "seriamos", "2p": "seriais", "3p": "serian"},
}


def participio_verbo(infinitivo):
    """Genera el participio (regular o irregular)."""
    if not infinitivo:
        return ""
    infinitivo = infinitivo.lower()
    if infinitivo in PARTICIPIOS_IRREGULARES:
        return PARTICIPIOS_IRREGULARES[infinitivo]
    if infinitivo.endswith("ar"):
        return infinitivo[:-2] + "ado"
    if infinitivo.endswith(("er", "ir")):
        return infinitivo[:-2] + "ido"
    return infinitivo


def _pers_num(tok):
    """'3s', '1p'... a partir de morph. '' si no disponible."""
    try:
        num = tok.morph.get("Number")
        per = tok.morph.get("Person")
        if num and per:
            return f"{per[0]}{num[0].lower()}"
    except Exception:
        pass
    return ""


def _tiempo(tok):
    """'Pres', 'Past', 'Imp', 'Fut', 'Cond'."""
    try:
        vals = tok.morph.get("Tense")
        return vals[0] if vals else ""
    except Exception:
        return ""


def conjugar_ser(tiempo, pers_num):
    """Conjuga 'ser' en tiempo/persona dados. Fallback: presente."""
    return SER_FORMAS.get(tiempo, SER_FORMAS["Pres"]).get(pers_num, "es")


def _doc(texto, modelo="es_core_news_md"):
    """Retorna doc spaCy o None."""
    if not texto or not str(texto).strip() or not modelo_disponible():
        return None
    try:
        return _cargar(modelo)(str(texto))
    except Exception:
        try:
            return _cargar()(str(texto))
        except Exception:
            return None


def es_pasiva(texto):
    """True si el texto tiene voz pasiva con 'ser/estar + participio'.

    Modelo es_core_news_md usa dep=aux (no aux:pass) para el verbo ser,
    y el participio es ROOT con VerbForm=Part. Esta funcion detecta eso.
    """
    doc = _doc(texto)
    if doc is None:
        return False
    for tok in doc:
        if tok.dep_ == "aux:pass":
            return True
        if tok.pos_ == "AUX" and tok.lemma_ in ("ser", "estar"):
            head = tok.head
            if head.pos_ == "VERB":
                verbform = head.morph.get("VerbForm") if head.morph else []
                if verbform and verbform[0] == "Part":
                    return True
                if head.text.lower().endswith(("ado", "ido", "to", "cho")):
                    return True
    return False


def transformar_a_pasiva(texto):
    """Sugiere pasiva desde activa. Retorna dict con esperado."""
    r = {"disponible": False, "esperado": "", "razon": ""}
    doc = _doc(texto)
    if doc is None:
        return r
    r["disponible"] = True

    sujeto = verbo = obj = None
    for tok in doc:
        if tok.dep_ in ("nsubj", "nsubj:pass"):
            sujeto = tok
        elif tok.dep_ == "ROOT" and tok.pos_ in ("VERB", "AUX"):
            verbo = tok
        elif tok.dep_ == "obj":
            obj = tok

    if not (sujeto and verbo and obj):
        r["razon"] = "no se detecta estructura activa (sujeto + verbo + objeto directo)"
        return r

    pers_num = _pers_num(verbo)
    tiempo = _tiempo(verbo) or "Pres"
    ser_conj = conjugar_ser(tiempo, pers_num)
    participio = participio_verbo(verbo.lemma_)
    if not participio:
        r["razon"] = f"no se pudo derivar participio de '{verbo.lemma_}'"
        return r

    esperado = f"{obj.text} {ser_conj} {participio} por {sujeto.text}"
    r["esperado"] = esperado[0].upper() + esperado[1:]
    r["razon"] = f"activa: sujeto='{sujeto.text}', verbo='{verbo.text}', obj='{obj.text}'"
    return r


def transformar_a_activa(texto):
    """Sugiere activa desde pasiva (usa arbol spaCy ES real).

    spaCy ES usa: ROOT VERB con VerbForm=Part, nsubj para el sujeto
    paciente, obj con case='por' como agente.
    """
    r = {"disponible": False, "esperado": "", "razon": ""}
    doc = _doc(texto)
    if doc is None:
        return r
    r["disponible"] = True

    # Buscar el VERBO ROOT con VerbForm=Part (predicado pasivo)
    participio_tok = None
    for tok in doc:
        if tok.pos_ == "VERB" and tok.dep_ == "ROOT":
            verbform = tok.morph.get("VerbForm") if tok.morph else []
            if verbform and verbform[0] == "Part":
                participio_tok = tok
                break

    if participio_tok is None:
        r["razon"] = "no se detecta verbo principal en participio"
        return r

    # Sujeto paciente (nsubj del participio) y agente (obj con case='por')
    sujeto_pac = None
    agente = None
    for tok in doc:
        if tok.dep_ == "nsubj" and tok.head == participio_tok:
            sujeto_pac = tok
        elif tok.dep_ == "obj" and tok.head == participio_tok:
            for child in tok.children:
                if child.dep_ == "case" and child.text.lower() == "por":
                    agente = tok
                    break

    if not (sujeto_pac and agente):
        r["razon"] = "no se detecta estructura pasiva (sujeto + por+agente)"
        return r

    infinitivo = participio_tok.lemma_
    if infinitivo.endswith("ar"):
        verbo_activo = infinitivo[:-2] + "a"
    elif infinitivo.endswith(("er", "ir")):
        verbo_activo = infinitivo[:-2] + "e"
    else:
        verbo_activo = infinitivo

    esperado = f"{agente.text} {verbo_activo} {sujeto_pac.text}"
    r["esperado"] = esperado[0].upper() + esperado[1:]
    r["razon"] = f"pasiva: sujeto_pac='{sujeto_pac.text}', verbo='{participio_tok.text}', agente='{agente.text}'"
    return r


def comparar_features(original, parafraseado, tipo):
    """Compara features clave entre original y parafraseado.

    Retorna dict con flags por tipo de parafrasis.
    """
    if not original or not parafraseado:
        return {"disponible": False, "checks": {}}
    doc_orig = _doc(original)
    doc_par = _doc(parafraseado)
    if doc_orig is None or doc_par is None:
        return {"disponible": False, "checks": {}}

    checks = {}
    if tipo in ("activa_a_pasiva", "reordenamiento"):
        checks["tiene_ser"] = any(
            t.pos_ == "AUX" and t.lemma_ == "ser" for t in doc_par
        )
        checks["tiene_participio"] = any(
            t.pos_ == "VERB"
            and t.morph
            and t.morph.get("VerbForm")
            and t.morph.get("VerbForm")[0] == "Part"
            for t in doc_par
        )
        checks["tiene_por"] = any(t.text.lower() == "por" for t in doc_par)
    elif tipo == "pasiva_a_activa":
        checks["no_tiene_ser"] = not any(
            t.pos_ == "AUX" and t.lemma_ == "ser" for t in doc_par
        )
        checks["no_tiene_participio"] = not any(
            t.pos_ == "VERB"
            and t.morph
            and t.morph.get("VerbForm")
            and t.morph.get("VerbForm")[0] == "Part"
            for t in doc_par
        )

    return {"disponible": True, "checks": checks, "aprobado": all(checks.values()) if checks else False}


def similitud_tokens(a, b):
    """Ratio Jaccard de tokens (sin puntuacion, sin stopwords)."""
    if not a or not b:
        return 0.0
    doc_a = _doc(a)
    doc_b = _doc(b)
    if doc_a is None or doc_b is None:
        return 0.0
    set_a = {t.text.lower() for t in doc_a if not t.is_punct}
    set_b = {t.text.lower() for t in doc_b if not t.is_punct}
    if not set_a or not set_b:
        return 0.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    return round(inter / union, 3) if union else 0.0


def verificar_parafrasis(original, parafraseado, tipo):
    """Evalua si el parafraseado cumple el tipo esperado."""
    r = {
        "aprobado": False, "tipo": tipo,
        "similitud": 0.0, "features": {}, "feedback": "",
    }
    if not original or not parafraseado:
        r["feedback"] = "Falta original o parafrasis"
        return r

    # 1. Rechazo si el parafraseado es identico al original
    if original.strip().lower() == parafraseado.strip().lower():
        r["feedback"] = "La parafrasis es identica al original. Debes transformar la estructura."
        return r

    # 2. Features especificas por tipo
    features = comparar_features(original, parafraseado, tipo)
    r["features"] = features

    # 3. Similitud (informativa, no bloqueante)
    r["similitud"] = similitud_tokens(original, parafraseado)

    # 4. Aprobacion: features pasan Y similitud >= 0.15 (no es copia literal)
    aprobado = features.get("aprobado", False) and r["similitud"] >= 0.15
    r["aprobado"] = aprobado

    if aprobado:
        r["feedback"] = f"Correcto. Transformacion mecanica de tipo '{tipo}' aplicada."
    else:
        faltantes = [k for k, v in features.get("checks", {}).items() if not v]
        if faltantes:
            r["feedback"] = f"Faltan features: {', '.join(faltantes)}"
        else:
            r["feedback"] = f"Similitud muy baja ({r['similitud']}). Revisa el contenido."
    return r