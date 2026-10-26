"""Servicio de certificaciones: verificar requisitos + otorgar automaticamente."""
from django.db.models import Sum
from django.utils import timezone

from core.models import Certificacion, CertificacionObtenida

try:
    from core.models_cursos import ProgresoUsuario
except ImportError:
    from core.models import ProgresoUsuario

try:
    from core.models import Respuesta
except ImportError:
    from core.models_preguntas import Respuesta


def get_user_stats(user):
    """Devuelve {lecciones, puntos, tasa} del usuario.

    - lecciones: ProgresoUsuario completadas
    - puntos: suma de puntaje_obtenido de lecciones completadas
    - tasa: porcentaje de respuestas correctas (0 si no hay respuestas)
    """
    progresos = ProgresoUsuario.objects.filter(usuario=user, completado=True)
    lecciones = progresos.count()
    puntos = progresos.aggregate(total=Sum("puntaje_obtenido"))["total"] or 0

    total_resp = Respuesta.objects.filter(user=user).count()
    if total_resp > 0:
        correctas = Respuesta.objects.filter(user=user, es_correcta=True).count()
        tasa = round((correctas / total_resp) * 100, 1)
    else:
        tasa = 0.0

    return {"lecciones": lecciones, "puntos": puntos, "tasa": tasa}


def cumple_requisitos(stats, requisitos):
    """True si stats cumple TODOS los requisitos (los que estan presentes)."""
    if not isinstance(requisitos, dict):
        return False
    if "lecciones" in requisitos and stats["lecciones"] < requisitos["lecciones"]:
        return False
    if "puntos" in requisitos and stats["puntos"] < requisitos["puntos"]:
        return False
    if "tasa" in requisitos and stats["tasa"] < requisitos["tasa"]:
        return False
    return True


def verificar_y_otorgar(user, dry_run=False):
    """Otorga certs pendientes al usuario. Idempotente.

    Args:
        user: User
        dry_run: si True, no crea, solo devuelve las que otorgaria.

    Returns:
        list[Certificacion] nuevas (o que otorgaria).
    """
    if not user or not user.is_authenticated:
        return []

    stats = get_user_stats(user)
    ya_obtenidas = CertificacionObtenida.objects.filter(
        user=user
    ).values_list("certificacion_id", flat=True)

    pendientes = Certificacion.objects.filter(activa=True).exclude(id__in=ya_obtenidas)

    nuevas = []
    for cert in pendientes:
        if cumple_requisitos(stats, cert.requisitos):
            nuevas.append(cert)
            if not dry_run:
                codigo = f"CERT-{user.id:04d}-{cert.id:04d}"
                CertificacionObtenida.objects.create(
                    user=user,
                    certificacion=cert,
                    fecha_obtenida=timezone.now(),
                    codigo_verificacion=codigo,
                    url_verificacion=f"/verificar/{codigo}/",
                )

    return nuevas