"""Servicio SM-2 (SuperMemo 2) para repeticion espaciada.

Funciones puras: no tocan BD, no guardan. El caller persiste.
"""

from datetime import timedelta

from django.utils import timezone


def aplicar_sm2(review, calidad, hoy=None):
    """Aplica SM-2 in-place y retorna el review modificado.

    Args:
        review: objeto con atributos intervalo_dias, facilidad, repeticiones,
                calidad_respuesta, programada_para
        calidad: entero 0-5
            0 = fallo total
            1 = fallo con recuerdo parcial
            2 = fallo pero recordaba algo
            3 = correcto con esfuerzo considerable
            4 = correcto con esfuerzo leve
            5 = correcto perfecto
        hoy: date base para calcular programada_para. Default: localdate().

    Returns:
        review (mutado in-place, NO guardado en BD)

    Reglas SM-2:
        calidad < 3  -> reset: repeticiones=0, intervalo=1
        calidad >= 3 -> si repeticiones==0: intervalo=1
                        si repeticiones==1: intervalo=6
                        si repeticiones>=2: intervalo=round(intervalo * facilidad)
                        y repeticiones += 1

        facilidad = max(1.3, facilidad + delta)
        delta = 0.1 - (5-q) * (0.08 + (5-q) * 0.02)
    """
    if not 0 <= calidad <= 5:
        raise ValueError(f"calidad fuera de rango 0-5: {calidad}")

    if hoy is None:
        hoy = timezone.localdate()

    review.calidad_respuesta = calidad

    if calidad < 3:
        review.repeticiones = 0
        review.intervalo_dias = 1
    else:
        if review.repeticiones == 0:
            review.intervalo_dias = 1
        elif review.repeticiones == 1:
            review.intervalo_dias = 6
        else:
            review.intervalo_dias = round(review.intervalo_dias * review.facilidad)
        review.repeticiones += 1

    delta = 0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02)
    review.facilidad = max(1.3, review.facilidad + delta)

    review.programada_para = hoy + timedelta(days=review.intervalo_dias)

    return review


def intervalo_estimado(intervalo_dias, facilidad, repeticiones, calidad):
    """Calcula el intervalo sin mutar nada. Util para previsualizar."""
    if calidad < 3:
        return 1
    if repeticiones == 0:
        return 1
    if repeticiones == 1:
        return 6
    return round(intervalo_dias * facilidad)