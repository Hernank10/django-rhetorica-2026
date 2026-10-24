"""Motor de evaluación de las 100 técnicas de sintaxis.

Funciones publicas:
- evaluar_ejercicio(ejercicio, respuesta, usuario) -> dict
- actualizar_progreso(usuario, tecnica, ejercicio, ok) -> ProgresoTecnica
- proximas_revisiones(usuario, n=5) -> QuerySet

Reglas de mastery (segun diseno del modulo 10):
- 3 aciertos consecutivos Y ultimo acertado de tipo 4 o 5 -> dominada
"""
import re
import unicodedata
from datetime import timedelta
from difflib import SequenceMatcher

from django.utils import timezone

from core.services.notificaciones import crear_notificacion

from core.models_sintaxis import TecnicaSintactica, ProgresoTecnica


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────
def _normalizar(texto):
    """Lowercase + trim + sin acentos ni puntuacion (para comparar respuestas)."""
    if not texto:
        return ""
    # Descomponer y quitar diacriticos
    nfkd = unicodedata.normalize("NFKD", str(texto))
    sin_acentos = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Solo alfanumerico y espacios
    limpio = "".join(c for c in sin_acentos.lower() if c.isalnum() or c.isspace())
    return " ".join(limpio.split())


def _fuzzy_match(texto_a, texto_b):
    """Ratio de similitud entre dos textos normalizados. 0.0-1.0."""
    a = _normalizar(texto_a)
    b = _normalizar(texto_b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


# ──────────────────────────────────────────────────────────────
# Evaluadores por tipo
# ──────────────────────────────────────────────────────────────
def _evaluar_tipo1(payload, respuesta):
    """Seleccion multiple con justificacion opcional."""
    opciones = payload.get("opciones", [])
    correcta = next((o for o in opciones if o.get("correcta")), None)
    if not correcta:
        return {"ok": False, "feedback": "Error: payload sin opcion correcta", "regla": "", "ejemplo_correcto": ""}

    opcion_id = respuesta.get("opcion_id")
    ok_opcion = opcion_id == correcta.get("id")

    ok_just = True
    if payload.get("justificacion_obligatoria"):
        razon = respuesta.get("justificacion", "")
        ok_just = _fuzzy_match(razon, correcta.get("razon", "")) >= 0.5

    ok = ok_opcion and ok_just

    if ok:
        feedback = "Correcto. " + correcta.get("razon", "")
    elif not ok_opcion:
        feedback = "Incorrecto. " + correcta.get("razon", "")
    else:
        feedback = "Opcion correcta, pero la justificacion no coincide. " + correcta.get("razon", "")

    return {
        "ok": ok,
        "feedback": feedback,
        "regla": payload.get("regla", ""),
        "ejemplo_correcto": correcta.get("texto", ""),
    }


def _evaluar_tipo2(payload, respuesta):
    """Correccion inline. Compara texto del alumno con respuesta_correcta."""
    esperado = payload.get("respuesta_correcta", "")
    recibido = respuesta.get("texto", "")

    # Exact match normalizado
    if _normalizar(recibido) == _normalizar(esperado):
        return {
            "ok": True,
            "feedback": "Correcto. " + payload.get("regla", ""),
            "regla": payload.get("regla", ""),
            "ejemplo_correcto": esperado,
        }

    # Fuzzy >= 0.85: aceptable (variante)
    ratio = _fuzzy_match(recibido, esperado)
    if ratio >= 0.85:
        return {
            "ok": True,
            "feedback": "Correcto (variante valida). " + payload.get("regla", ""),
            "regla": payload.get("regla", ""),
            "ejemplo_correcto": esperado,
        }

    return {
        "ok": False,
        "feedback": "Incorrecto. " + payload.get("regla", "") + ". Ejemplo: " + esperado,
        "regla": payload.get("regla", ""),
        "ejemplo_correcto": esperado,
    }


def _evaluar_tipo3(payload, respuesta):
    """Clasificacion: lista de categorias correctas vs recibidas."""
    oraciones = payload.get("oraciones", [])
    recibidas = respuesta.get("clasificacion", [])

    if not isinstance(recibidas, list) or len(recibidas) != len(oraciones):
        return {
            "ok": False,
            "feedback": f"Se esperaban {len(oraciones)} clasificaciones, se recibieron {len(recibidas)}",
            "regla": "",
            "ejemplo_correcto": "",
        }

    aciertos = 0
    detalle = []
    for i, (oracion, recibida) in enumerate(zip(oraciones, recibidas), 1):
        correcta = oracion.get("categoria_correcta", "")
        ok_i = _normalizar(recibida) == _normalizar(correcta)
        if ok_i:
            aciertos += 1
        else:
            detalle.append(f"{i}: era '{correcta}', diste '{recibida}'")

    ok = aciertos == len(oraciones)

    return {
        "ok": ok,
        "feedback": f"{aciertos}/{len(oraciones)} correctas" + (" | " + "; ".join(detalle) if detalle else ""),
        "regla": "",
        "ejemplo_correcto": "",
    }


def _evaluar_tipo4(payload, respuesta):
    """Construccion guiada: conector como palabra + fuzzy ALTO contra esperado.

    Reglas:
    1. Respuesta vacia -> rechazo.
    2. Exact match normalizado -> OK.
    3. Conector (si existe) debe aparecer como PALABRA separada.
    4. Fuzzy >= 0.85 contra respuesta_correcta -> OK (variante valida).
    5. Resto -> rechazo.
    """
    texto = respuesta.get("texto", "")
    esperado = payload.get("respuesta_correcta", "")
    conector = (payload.get("conector") or "").strip()
    regla = payload.get("regla", "")

    if not texto.strip():
        return {
            "ok": False,
            "feedback": "Respuesta vacia. " + regla,
            "regla": regla,
            "ejemplo_correcto": esperado,
        }

    # 1. Exact match
    if _normalizar(texto) == _normalizar(esperado):
        return {
            "ok": True,
            "feedback": "Correcto. " + regla,
            "regla": regla,
            "ejemplo_correcto": esperado,
        }

    # 2. Validar conector como palabra separada
    if conector:
        patron_conector = r"\b" + re.escape(conector) + r"\b"
        if not re.search(patron_conector, texto.lower()):
            return {
                "ok": False,
                "feedback": "Falta el conector '" + conector + "'. " + regla,
                "regla": regla,
                "ejemplo_correcto": esperado,
            }

    # 3. Fuzzy ALTO contra esperado (>= 0.85)
    ratio = _fuzzy_match(texto, esperado)
    if ratio >= 0.85:
        return {
            "ok": True,
            "feedback": "Correcto (variante valida). " + regla,
            "regla": regla,
            "ejemplo_correcto": esperado,
        }

    # 4. Rechazo
    return {
        "ok": False,
        "feedback": "Incorrecto. " + regla + ". Ejemplo: " + esperado,
        "regla": regla,
        "ejemplo_correcto": esperado,
    }


def _evaluar_tipo5(payload, respuesta):
    """Deteccion de error: posicion + regla_violada."""
    posicion_recibida = respuesta.get("posicion")
    regla_recibida = _normalizar(respuesta.get("regla", ""))
    regla_esperada = _normalizar(payload.get("regla_violada", ""))

    ok_pos = posicion_recibida == payload.get("error_posicion")
    ok_regla = regla_recibida == regla_esperada

    ok = ok_pos and ok_regla

    return {
        "ok": ok,
        "feedback": ("Correcto. " if ok else "Incorrecto. La regla violada es: " + payload.get("regla_violada", "")),
        "regla": payload.get("regla_violada", ""),
        "ejemplo_correcto": payload.get("error_texto", ""),
    }


# ──────────────────────────────────────────────────────────────
# API publica
# ──────────────────────────────────────────────────────────────
def evaluar_ejercicio(ejercicio, respuesta, usuario=None):
    """Evalua un ejercicio segun su tipo. Retorna dict con ok, feedback, regla, ejemplo_correcto."""
    tipo = ejercicio.tipo
    payload = ejercicio.payload

    if tipo == 1:
        return _evaluar_tipo1(payload, respuesta)
    if tipo == 2:
        return _evaluar_tipo2(payload, respuesta)
    if tipo == 3:
        return _evaluar_tipo3(payload, respuesta)
    if tipo == 4:
        return _evaluar_tipo4(payload, respuesta)
    if tipo == 5:
        return _evaluar_tipo5(payload, respuesta)

    return {"ok": False, "feedback": f"Tipo {tipo} no soportado", "regla": "", "ejemplo_correcto": ""}


def _actualizar_sm2(progreso, calidad):
    """SM-2 simplificado. calidad: 0-5 (0=mal, 5=perfecto)."""
    ef = progreso.sm2_ef or 2.5
    ef = ef + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02))
    progreso.sm2_ef = max(1.3, ef)

    if calidad < 3:
        progreso.sm2_repetitions = 0
        progreso.sm2_interval = 1
    else:
        progreso.sm2_repetitions = (progreso.sm2_repetitions or 0) + 1
        if progreso.sm2_repetitions == 1:
            progreso.sm2_interval = 1
        elif progreso.sm2_repetitions == 2:
            progreso.sm2_interval = 6
        else:
            progreso.sm2_interval = round((progreso.sm2_interval or 1) * progreso.sm2_ef)

    progreso.proxima_revision = timezone.now() + timedelta(days=progreso.sm2_interval)


def actualizar_progreso(usuario, tecnica, ejercicio, ok):
    """Actualiza ProgresoTecnica tras un intento. Retorna el objeto."""
    progreso, _ = ProgresoTecnica.objects.get_or_create(
        usuario=usuario, tecnica=tecnica,
    )

    progreso.intentos = (progreso.intentos or 0) + 1
    progreso.ultima_revision = timezone.now()

    if ok:
        progreso.aciertos_consecutivos = (progreso.aciertos_consecutivos or 0) + 1
        calidad = 4 if ejercicio.tipo in (4, 5) else 3
    else:
        progreso.aciertos_consecutivos = 0
        calidad = 1

    _actualizar_sm2(progreso, calidad)

    estado_anterior = progreso.estado

    # Mastery: 3+ aciertos consecutivos y ejercicio actual tipo 4/5
    if progreso.aciertos_consecutivos >= 3 and ejercicio.tipo in (4, 5) and ok:
        progreso.estado = "dominada"
    elif progreso.intentos > 0:
        progreso.estado = "en_progreso"

    progreso.save()

    # Notificacion idempotente al pasar a dominada
    if progreso.estado == "dominada" and estado_anterior != "dominada":
        try:
            crear_notificacion(
                user=usuario,
                tipo="logro",
                titulo=f"Tecnica {tecnica.numero} dominada",
                mensaje=f"'{tecnica.titulo}' superada con 3 aciertos consecutivos",
                url_destino=f"/sintaxis/tecnica/{tecnica.numero}/",
                icono="star",
                referencia=f"sintaxis_tecnica_{tecnica.numero}_{usuario.id}",
            )
        except Exception:
            pass  # notificacion no debe romper el flujo de progreso

    return progreso


def proximas_revisiones(usuario, n=5):
    """Tecnicas con proxima_revision <= ahora, ordenadas por urgencia."""
    return ProgresoTecnica.objects.filter(
        usuario=usuario,
        proxima_revision__lte=timezone.now(),
    ).select_related("tecnica").order_by("proxima_revision")[:n]


def resumen_progreso(usuario):
    """Counts rapidos para badges/heatmap."""
    qs = ProgresoTecnica.objects.filter(usuario=usuario)
    return {
        "total": TecnicaSintactica.objects.count(),
        "iniciadas": qs.exclude(estado="no_iniciada").count(),
        "dominadas": qs.filter(estado="dominada").count(),
    }