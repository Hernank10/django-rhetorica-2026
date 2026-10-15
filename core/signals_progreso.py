"""Signal que mantiene ProgresoCategoria actualizado al guardar Respuesta."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Respuesta, ProgresoCategoria


def _calcular_nivel_dominio(aciertos, intentos):
    """1-5 segun tasa de aciertos."""
    if intentos == 0:
        return 1
    tasa = aciertos / intentos
    if tasa >= 0.90:
        return 5
    if tasa >= 0.75:
        return 4
    if tasa >= 0.60:
        return 3
    if tasa >= 0.40:
        return 2
    return 1


def _calcular_estrellas(aciertos, intentos):
    """0-5 estrellas segun tasa de aciertos."""
    if intentos == 0:
        return 0
    tasa = aciertos / intentos
    if tasa >= 0.90:
        return 5
    if tasa >= 0.75:
        return 4
    if tasa >= 0.60:
        return 3
    if tasa >= 0.40:
        return 2
    if tasa >= 0.20:
        return 1
    return 0


@receiver(post_save, sender=Respuesta)
def actualizar_progreso_categoria(sender, instance, created, **kwargs):
    """Incrementa contadores en ProgresoCategoria al guardar una Respuesta."""
    if not created:
        return  # Solo en creacion, no en updates

    prog, _ = ProgresoCategoria.objects.get_or_create(
        user_id=instance.user_id,
        categoria=instance.tipo_ejercicio,
        defaults={"aciertos": 0, "intentos": 0},
    )

    prog.intentos += 1
    if instance.es_correcta:
        prog.aciertos += 1
    prog.nivel_dominio = _calcular_nivel_dominio(prog.aciertos, prog.intentos)
    prog.estrellas_obtenidas = _calcular_estrellas(prog.aciertos, prog.intentos)
    prog.save(update_fields=[
        "intentos", "aciertos", "nivel_dominio", "estrellas_obtenidas",
    ])