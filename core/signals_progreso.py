"""Signal que mantiene ProgresoCategoria actualizado al guardar Respuesta."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Respuesta, ProgresoCategoria



# Imports para señales de notificaciones (sprint #6)
from core.models_cursos import ProgresoUsuario
from core.models import CertificacionObtenida, LogroObtenido


# Imports notificaciones (sprint #6)
from core.services.notificaciones import crear_notificacion

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


# ==== Señales de notificaciones (sprint #6) ====

@receiver(post_save, sender=ProgresoUsuario)
def notif_progreso_completado(sender, instance, created, **kwargs):
    """Notif al completar leccion, y al completar el curso entero."""
    if not instance.completado:
        return
    try:
        from django.apps import apps

        # 1. Leccion completada
        crear_notificacion(
            user=instance.usuario,
            tipo="leccion_completada",
            titulo=f"Leccion completada: {instance.leccion.titulo}",
            mensaje=f"Terminaste '{instance.leccion.titulo}'",
            url_destino=f"/cursos/{instance.leccion.modulo.curso.slug}/",
            icono="check-circle",
            referencia=f"leccion_{instance.leccion_id}_{instance.usuario_id}",
        )

        # 2. Verificar curso completo
        Leccion = apps.get_model("core", "Leccion")
        ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
        curso = instance.leccion.modulo.curso
        total = Leccion.objects.filter(modulo__curso=curso).count()
        completadas = ProgresoUsuario.objects.filter(
            usuario=instance.usuario,
            leccion__modulo__curso=curso,
            completado=True,
        ).count()

        if total > 0 and completadas >= total:
            crear_notificacion(
                user=instance.usuario,
                tipo="curso_completado",
                titulo=f"Curso completado: {curso.titulo}",
                mensaje=f"Completaste todas las lecciones de '{curso.titulo}'",
                url_destino=f"/cursos/{curso.slug}/",
                icono="trophy",
                referencia=f"curso_{curso.id}_{instance.usuario_id}",
            )
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Error notif progreso: {e}")


@receiver(post_save, sender=CertificacionObtenida)
def notif_certificacion(sender, instance, created, **kwargs):
    """Notif al recibir certificacion (solo creacion)."""
    if not created:
        return
    try:
        crear_notificacion(
            user=instance.user,
            tipo="certificacion",
            titulo=f"Certificacion: {instance.certificacion.nombre}",
            mensaje=f"Obtuviste la certificacion '{instance.certificacion.nombre}'",
            url_destino="/estudiante/certificados/",
            icono="award",
            referencia=f"cert_{instance.certificacion_id}_{instance.user_id}",
        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Error notif cert: {e}")


@receiver(post_save, sender=LogroObtenido)
def notif_logro(sender, instance, created, **kwargs):
    """Notif al obtener logro (solo creacion)."""
    if not created:
        return
    try:
        crear_notificacion(
            user=instance.user,
            tipo="logro",
            titulo=f"Logro: {instance.logro.nombre}",
            mensaje=f"Desbloqueaste el logro '{instance.logro.nombre}'",
            url_destino="/estudiante/logros/",
            icono="star",
            referencia=f"logro_{instance.logro_id}_{instance.user_id}",
        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Error notif logro: {e}")

