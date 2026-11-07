"""redaccion_extras.py - Filtros para display de tipo_redaccion y categoria"""
from django import template

register = template.Library()

TIPO_LABELS = {
    'oracion_simple':        'Oración simple',
    'oracion_coordinada':    'Oración coordinada',
    'oracion_subordinada':   'Oración subordinada',
    'oracion_yuxtapuesta':   'Oración yuxtapuesta',
    'parrafo_narrativo':     'Párrafo narrativo',
    'parrafo_descriptivo':   'Párrafo descriptivo',
    'parrafo_expositivo':    'Párrafo expositivo',
    'parrafo_argumentativo': 'Párrafo argumentativo',
}

CATEGORIA_LABELS = {
    'redaccion': 'Redacción',
}

@register.filter
def tipo_label(value):
    if not value:
        return value
    return TIPO_LABELS.get(value, value)

@register.filter
def categoria_label(value):
    if not value:
        return value
    return CATEGORIA_LABELS.get(value, value)