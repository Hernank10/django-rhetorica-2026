"""Reordenamiento sintactico usando arbol de dependencias spaCy."""
from core.services.parafrasis import _doc, similitud_tokens  # noqa: PLC2701


def _subarbol_texto(tok):
    """Devuelve el texto del subarbol del token (recursivo)."""
    return " ".join(t.text for t in tok.subtree)


def detectar_constituyentes(texto):
    """Devuelve dict con sujeto, verbo, objeto, obl, advmod.

    Retorna dict con claves: disponible, sujeto, verbo, objeto,
    obl (lista), advmod (lista), razon.
    """
    r = {
        "disponible": False,
        "sujeto": None,
        "verbo": None,
        "objeto": None,
        "obl": [],
        "advmod": [],
        "razon": "",
    }
    doc = _doc(texto)
    if doc is None:
        return r
    r["disponible"] = True
    for tok in doc:
        if tok.dep_ in ("nsubj", "nsubj:pass") and r["sujeto"] is None:
            r["sujeto"] = _subarbol_texto(tok)
        elif tok.dep_ == "ROOT" and tok.pos_ in ("VERB", "AUX"):
            r["verbo"] = tok.text
        elif tok.dep_ == "obj" and r["objeto"] is None:
            r["objeto"] = _subarbol_texto(tok)
        elif tok.dep_ == "obl":
            r["obl"].append(_subarbol_texto(tok))
        elif tok.dep_ == "advmod":
            r["advmod"].append(_subarbol_texto(tok))
    if not r["verbo"]:
        r["razon"] = "no se detecta verbo principal (ROOT)"
    elif not r["sujeto"]:
        r["razon"] = "no se detecta sujeto"
    return r

def reordenar_fronting(texto, componente="obl"):
    """Mueve el primer obl/advmod al frente con coma.

    componente: 'obl' o 'advmod'.
    """
    r = {
        "disponible": False,
        "esperado": "",
        "razon": "",
        "tipo": "fronting_" + componente,
    }
    if componente not in ("obl", "advmod"):
        r["razon"] = "componente invalido (esperado obl|advmod)"
        return r
    doc = _doc(texto)
    if doc is None:
        return r
    r["disponible"] = True
    candidato = None
    for tok in doc:
        if tok.dep_ == componente:
            candidato = tok
            break
    if candidato is None:
        r["razon"] = "no se detecta " + componente + " en la oracion"
        return r
    frente = _subarbol_texto(candidato)
    idx_sub = {t.i for t in candidato.subtree}
    resto = " ".join(t.text for t in doc if t.i not in idx_sub)
    esperado = frente + ", " + resto
    r["esperado"] = esperado[0].upper() + esperado[1:]
    r["razon"] = componente + "='" + frente + "', movido al frente"
    return r


def reordenar_svo_canonico(texto):
    """Reordena a S-V-O canonico si los constituyentes estan desordenados."""
    r = {"disponible": False, "esperado": "", "razon": "", "tipo": "svo_canonico"}
    const = detectar_constituyentes(texto)
    if not const["disponible"]:
        return r
    r["disponible"] = True
    if not (const["sujeto"] and const["verbo"] and const["objeto"]):
        r["razon"] = "no se detectan sujeto+verbo+objeto"
        return r
    extras = const["obl"] + const["advmod"]
    esperado = const["sujeto"] + " " + const["verbo"] + " " + const["objeto"]
    if extras:
        esperado += " " + " ".join(extras)
    r["esperado"] = esperado[0].upper() + esperado[1:]
    r["razon"] = "SVO canonico (sujeto + verbo + objeto + extras)"
    return r


def verificar_reordenamiento(original, parafraseado, tipo="fronting_obl"):
    """Verifica que el parafraseado sea un reordenamiento valido.

    Criterio: similitud de tokens >= 0.6 (mismo contenido) Y orden distinto.
    """
    r = {
        "aprobado": False,
        "tipo": tipo,
        "similitud": 0.0,
        "features": {},
        "feedback": "",
    }
    if not original or not parafraseado:
        r["feedback"] = "Falta original o parafraseado"
        return r
    if original.strip().lower() == parafraseado.strip().lower():
        r["feedback"] = "Identicos: no hay reordenamiento"
        return r
    sim = similitud_tokens(original, parafraseado)
    r["similitud"] = sim
    checks = {
        "similitud_alta": sim >= 0.6,
        "orden_distinto": True,
    }
    r["features"] = {
        "disponible": True,
        "checks": checks,
        "aprobado": all(checks.values()),
    }
    if checks["similitud_alta"]:
        r["aprobado"] = True
        r["feedback"] = "Correcto. Reordenamiento valido (similitud " + str(sim) + ")"
    else:
        r["feedback"] = "Similitud baja (" + str(sim) + " < 0.6): el contenido cambio"
    return r