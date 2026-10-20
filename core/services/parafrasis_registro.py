"""Parafrasis de registro: formal <-> coloquial (lexico, determinista)."""
import re


PARES_FORMAL_A_COLOQUIAL = {
    "usted": "vos",
    "ustedes": "vosotros",
    "automovil": "carro",
    "dinero": "plata",
    "trabajo": "laburo",
    "profesor": "profe",
    "estupendo": "genial",
    "comer": "papear",
    "cansado": "reventado",
}

PARES_COLOQUIAL_A_FORMAL = {v: k for k, v in PARES_FORMAL_A_COLOQUIAL.items()}

MARCADORES_FORMAL = set(PARES_FORMAL_A_COLOQUIAL.keys())
MARCADORES_COLOQUIAL = set(PARES_FORMAL_A_COLOQUIAL.values())


def _palabras(texto):
    """Tokeniza a palabras lowercase (regex \\w+)."""
    return [m.group(0).lower() for m in re.finditer(r"\w+", texto)]


def _reemplazar_palabras(texto, mapping):
    """Reemplaza palabras completas preservando capitalizacion inicial."""
    def _sub(match):
        palabra = match.group(0)
        clave = palabra.lower()
        if clave not in mapping:
            return palabra
        nuevo = mapping[clave]
        if palabra[0].isupper():
            nuevo = nuevo[0].upper() + nuevo[1:]
        return nuevo
    return re.sub(r"\w+", _sub, texto)


def detectar_registro(texto):
    """Detecta registro dominante: formal, coloquial o neutral."""
    r = {
        "disponible": False,
        "registro": "neutral",
        "formal_count": 0,
        "coloquial_count": 0,
        "marcadores_formal": [],
        "marcadores_coloquial": [],
        "razon": "",
    }
    if not texto or not str(texto).strip():
        r["razon"] = "texto vacio"
        return r
    r["disponible"] = True
    for p in _palabras(texto):
        if p in MARCADORES_FORMAL:
            r["formal_count"] += 1
            r["marcadores_formal"].append(p)
        if p in MARCADORES_COLOQUIAL:
            r["coloquial_count"] += 1
            r["marcadores_coloquial"].append(p)
    if r["formal_count"] > r["coloquial_count"]:
        r["registro"] = "formal"
    elif r["coloquial_count"] > r["formal_count"]:
        r["registro"] = "coloquial"
    r["razon"] = (
        "formal=" + str(r["formal_count"]) +
        " coloquial=" + str(r["coloquial_count"])
    )
    return r

def transformar_registro(texto, hacia="coloquial"):
    """Transforma registro. hacia: 'coloquial' o 'formal'."""
    r = {
        "disponible": False,
        "esperado": "",
        "cambios": [],
        "razon": "",
        "direccion": hacia,
    }
    if not texto or not str(texto).strip():
        r["razon"] = "texto vacio"
        return r
    if hacia not in ("coloquial", "formal"):
        r["razon"] = "hacia invalido (esperado coloquial|formal)"
        return r
    r["disponible"] = True
    mapping = (
        PARES_FORMAL_A_COLOQUIAL
        if hacia == "coloquial"
        else PARES_COLOQUIAL_A_FORMAL
    )
    resultado = _reemplazar_palabras(texto, mapping)
    if resultado == texto:
        r["razon"] = "sin cambios (no hay marcadores del registro origen)"
        return r
    palabras_orig = _palabras(texto)
    palabras_nuevo = _palabras(resultado)
    for po, pn in zip(palabras_orig, palabras_nuevo):
        if po != pn:
            r["cambios"].append({"de": po, "a": pn})
    r["esperado"] = resultado
    r["razon"] = str(len(r["cambios"])) + " cambio(s) aplicado(s)"
    return r


def verificar_registro(original, parafraseado, tipo):
    """Verifica transformacion de registro.

    tipo: 'formal_a_coloquial' o 'coloquial_a_formal'
    """
    r = {
        "aprobado": False,
        "tipo": tipo,
        "registro_original": "neutral",
        "registro_parafraseado": "neutral",
        "features": {},
        "feedback": "",
    }
    if not original or not parafraseado:
        r["feedback"] = "Falta original o parafraseado"
        return r
    if tipo not in ("formal_a_coloquial", "coloquial_a_formal"):
        r["feedback"] = "tipo invalido"
        return r
    if original.strip().lower() == parafraseado.strip().lower():
        r["feedback"] = "Identicos: no hay transformacion"
        return r
    det_orig = detectar_registro(original)
    det_par = detectar_registro(parafraseado)
    r["registro_original"] = det_orig["registro"]
    r["registro_parafraseado"] = det_par["registro"]
    checks = {}
    if tipo == "formal_a_coloquial":
        checks["original_tiene_formal"] = det_orig["formal_count"] > 0
        checks["reduce_formal"] = (
            det_par["formal_count"] < det_orig["formal_count"]
        )
    else:
        checks["original_tiene_coloquial"] = det_orig["coloquial_count"] > 0
        checks["reduce_coloquial"] = (
            det_par["coloquial_count"] < det_orig["coloquial_count"]
        )
    r["features"] = {
        "checks": checks,
        "aprobado": all(checks.values()),
    }
    if all(checks.values()):
        r["aprobado"] = True
        r["feedback"] = "Correcto. Transformacion de registro aplicada."
    else:
        faltantes = [k for k, v in checks.items() if not v]
        r["feedback"] = "No cumple: " + ", ".join(faltantes)
    return r