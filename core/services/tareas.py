"""Servicio de tareas del curso: pendientes y programadas.

Sin modelo nuevo: computa desde modelos existentes (Leccion, EvaluacionCurso,
ProgresoUsuario, ResultadoEvaluacionCurso).
"""
from django.apps import apps
from django.db.models import Q
from django.utils import timezone


def lecciones_pendientes(user, limit=10):
    """Lecciones publicadas no completadas por el usuario."""
    Leccion = apps.get_model("core", "Leccion")
    ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")

    completadas_ids = ProgresoUsuario.objects.filter(
        usuario=user, completado=True
    ).values_list("leccion_id", flat=True)

    return (
        Leccion.objects.filter(modulo__curso__estado="publicado")
        .exclude(id__in=completadas_ids)
        .select_related("modulo__curso")
        .order_by("modulo__curso__titulo", "modulo__orden", "orden")[:limit]
    )


def evaluaciones_disponibles(user, limit=10):
    """Evaluaciones con rango de disponibilidad activo, no rendidas."""
    EvaluacionCurso = apps.get_model("core", "EvaluacionCurso")
    ResultadoEvaluacionCurso = apps.get_model(
        "core", "ResultadoEvaluacionCurso"
    )
    now = timezone.now()

    rendidas_ids = ResultadoEvaluacionCurso.objects.filter(
        usuario=user, completado=True
    ).values_list("evaluacion_id", flat=True)

    return (
        EvaluacionCurso.objects.filter(
            Q(disponible_desde__isnull=True) | Q(disponible_desde__lte=now)
        )
        .filter(
            Q(disponible_hasta__isnull=True) | Q(disponible_hasta__gte=now)
        )
        .exclude(id__in=rendidas_ids)
        .select_related("curso")
        .order_by("disponible_hasta", "titulo")[:limit]
    )


def evaluaciones_programadas(user, limit=10):
    """Evaluaciones cuyo 'disponible_desde' es futuro."""
    EvaluacionCurso = apps.get_model("core", "EvaluacionCurso")
    now = timezone.now()
    return (
        EvaluacionCurso.objects.filter(disponible_desde__gt=now)
        .select_related("curso")
        .order_by("disponible_desde")[:limit]
    )


def resumen_tareas(user):
    """Counts rapidos para badges."""
    return {
        "lecciones": lecciones_pendientes(user, limit=9999).count(),
        "evaluaciones_disponibles": evaluaciones_disponibles(user, limit=9999).count(),
        "evaluaciones_programadas": evaluaciones_programadas(user, limit=9999).count(),
    }