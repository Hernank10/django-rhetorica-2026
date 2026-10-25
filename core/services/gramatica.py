"""Motor de evaluacion de gramatica: wrapper sobre sintaxis + ProgresoGramatical."""
from datetime import timedelta
from django.utils import timezone
from core.models_gramatica import TecnicaGramatical, ProgresoGramatical
from core.services import sintaxis as sintaxis_engine


def evaluar_ejercicio(ejercicio, respuesta, usuario=None):
    """Reusa el evaluador generico (tipos 1-5) del motor de sintaxis."""
    return sintaxis_engine.evaluar_ejercicio(ejercicio, respuesta, usuario)


def _actualizar_sm2(progreso, calidad):
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
    """Actualiza ProgresoGramatical tras un intento + notif al dominar."""
    progreso, _ = ProgresoGramatical.objects.get_or_create(usuario=usuario, tecnica=tecnica)
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
    if progreso.aciertos_consecutivos >= 3 and ejercicio.tipo in (4, 5) and ok:
        progreso.estado = "dominada"
    elif progreso.intentos > 0:
        progreso.estado = "en_progreso"
    progreso.save()

    if progreso.estado == "dominada" and estado_anterior != "dominada":
        try:
            from core.services.notificaciones import crear_notificacion
            crear_notificacion(
                user=usuario, tipo="logro",
                titulo=f"Tecnica {tecnica.numero} dominada",
                mensaje=f"'{tecnica.titulo}' superada",
                url_destino=f"/gramatica/tecnica/{tecnica.numero}/",
                icono="star",
                referencia=f"gramatica_tecnica_{tecnica.numero}_{usuario.id}",
            )
        except Exception:
            pass
    return progreso


def proximas_revisiones(usuario, n=5, modulo=None):
    qs = ProgresoGramatical.objects.filter(
        usuario=usuario, proxima_revision__lte=timezone.now(),
    )
    if modulo:
        qs = qs.filter(tecnica__modulo=modulo)
    return qs.select_related("tecnica").order_by("proxima_revision")[:n]


def resumen_progreso(usuario, modulo=None):
    qs = ProgresoGramatical.objects.filter(usuario=usuario)
    total_qs = TecnicaGramatical.objects.all()
    if modulo:
        qs = qs.filter(tecnica__modulo=modulo)
        total_qs = total_qs.filter(modulo=modulo)
    return {
        "total": total_qs.count(),
        "iniciadas": qs.exclude(estado="no_iniciada").count(),
        "dominadas": qs.filter(estado="dominada").count(),
    }