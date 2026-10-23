"""Servicio de creacion de notificaciones. Idempotente."""
from django.apps import apps


def crear_notificacion(
    user,
    tipo,
    titulo,
    mensaje="",
    url_destino="",
    icono="bell",
    referencia="",
):
    """Crea una notificacion. Idempotente si `referencia` esta presente.

    Retorna (notif, created).
    """
    Notificacion = apps.get_model("core", "Notificacion")

    if referencia:
        notif, created = Notificacion.objects.get_or_create(
            user=user,
            tipo=tipo,
            referencia=referencia,
            defaults={
                "titulo": titulo,
                "mensaje": mensaje,
                "url_destino": url_destino,
                "icono": icono,
            },
        )
        return notif, created

    notif = Notificacion.objects.create(
        user=user,
        tipo=tipo,
        titulo=titulo,
        mensaje=mensaje,
        url_destino=url_destino,
        icono=icono,
    )
    return notif, True


def contar_no_leidas(user):
    """Cuenta notificaciones no leidas del usuario."""
    Notificacion = apps.get_model("core", "Notificacion")
    return Notificacion.objects.filter(user=user, leida=False).count()


def marcar_todas_leidas(user):
    """Marca todas las notificaciones del usuario como leidas. Retorna el count."""
    Notificacion = apps.get_model("core", "Notificacion")
    return Notificacion.objects.filter(user=user, leida=False).update(leida=True)


def ultimas_notificaciones(user, n=10):
    """Retorna las N notificaciones mas recientes del usuario."""
    Notificacion = apps.get_model("core", "Notificacion")
    return Notificacion.objects.filter(user=user).order_by("-creada_en")[:n]