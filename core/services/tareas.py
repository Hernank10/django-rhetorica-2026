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


# ══════════════════════════════════════════════════════════════
# Tareas del profesor
# ══════════════════════════════════════════════════════════════
def tareas_profesor(user, limit=10):
    """Tareas pendientes especificas del profesor.

    Returns dict con:
    - estudiantes_riesgo: alumnos con 0 progreso en ultimos 7 dias
    - cursos_borrador: cursos del profesor sin publicar
    - evaluaciones_sin_calificar: resultados con completado=False
    - total
    """
    from django.apps import apps
    from django.db.models import Count
    from django.utils import timezone

    Curso = apps.get_model("core", "Curso")
    ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
    ResultadoEvaluacionCurso = apps.get_model("core", "ResultadoEvaluacionCurso")
    User = apps.get_model("auth", "User")

    # 1. Cursos en borrador del profesor
    cursos_borrador = list(
        Curso.objects.filter(profesor_asignado=user, estado="borrador")
        .order_by("-creado_en")[:limit]
    )

    # 2. Estudiantes en riesgo: inscritos en cursos del profe con 0 progreso en 7 dias
    hace_7d = timezone.now() - timezone.timedelta(days=7)
    mis_cursos_ids = list(Curso.objects.filter(profesor_asignado=user).values_list("id", flat=True))

    if mis_cursos_ids:
        # Estudiantes que tienen algun progreso en mis cursos
        est_ids = (
            ProgresoUsuario.objects
            .filter(leccion__modulo__curso_id__in=mis_cursos_ids)
            .values_list("usuario_id", flat=True)
            .distinct()
        )
        # De esos, los que NO tienen actividad reciente
        activos_recientes = set(
            ProgresoUsuario.objects
            .filter(
                leccion__modulo__curso_id__in=mis_cursos_ids,
                completado_en__gte=hace_7d,
            )
            .values_list("usuario_id", flat=True)
            .distinct()
        )
        en_riesgo_ids = [eid for eid in est_ids if eid not in activos_recientes]
        estudiantes_riesgo = list(
            User.objects.filter(id__in=en_riesgo_ids)
            .order_by("username")[:limit]
        )
    else:
        estudiantes_riesgo = []

    # 3. Evaluaciones sin calificar (resultados completados=False)
    evaluaciones_sin_calificar = list(
        ResultadoEvaluacionCurso.objects
        .filter(
            evaluacion__curso__profesor_asignado=user,
            completado=False,
        )
        .select_related("evaluacion", "usuario")
        .order_by("-fecha_inicio")[:limit]
    )

    return {
        "estudiantes_riesgo": estudiantes_riesgo,
        "cursos_borrador": cursos_borrador,
        "evaluaciones_sin_calificar": evaluaciones_sin_calificar,
        "total": len(estudiantes_riesgo) + len(cursos_borrador) + len(evaluaciones_sin_calificar),
    }


# ══════════════════════════════════════════════════════════════
# Tareas del admin
# ══════════════════════════════════════════════════════════════
def tareas_admin(limit=10):
    """Tareas pendientes globales (solo admin)."""
    from django.apps import apps

    Curso = apps.get_model("core", "Curso")
    Modulo = apps.get_model("core", "Modulo")
    User = apps.get_model("auth", "User")

    # 1. Usuarios sin grupo asignado
    usuarios_sin_grupo = list(
        User.objects.filter(groups__isnull=True).order_by("username")[:limit]
    )

    # 2. Cursos sin profesor asignado
    cursos_sin_profesor = list(
        Curso.objects.filter(profesor_asignado__isnull=True)
        .order_by("-creado_en")[:limit]
    )

    # 3. Cursos publicados sin modulos
    cursos_sin_modulos = []
    for curso in Curso.objects.filter(estado="publicado"):
        if not Modulo.objects.filter(curso=curso).exists():
            cursos_sin_modulos.append(curso)
            if len(cursos_sin_modulos) >= limit:
                break

    return {
        "usuarios_sin_grupo": usuarios_sin_grupo,
        "cursos_sin_profesor": cursos_sin_profesor,
        "cursos_sin_modulos": cursos_sin_modulos,
        "total": len(usuarios_sin_grupo) + len(cursos_sin_profesor) + len(cursos_sin_modulos),
    }

