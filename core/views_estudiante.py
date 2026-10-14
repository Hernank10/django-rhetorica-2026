"""
Panel del Estudiante: dashboard personal, cursos, evaluaciones,
logros, certificados, estadísticas y ranking.
"""
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    Certificacion,
    CertificacionObtenida,
    Logro,
    LogroObtenido,
    Respuesta,
)
from .models_cursos import (
    Curso,
    EvaluacionCurso,
    Leccion,
    Modulo,
    PreguntaEvaluacion,
    ProgresoUsuario,
    ResultadoEvaluacionCurso,
)

User = get_user_model()


def _get_user(request):
    return request.user


# ============================================================
# DASHBOARD PRINCIPAL
# ============================================================
@login_required
def dashboard(request):
    u = _get_user(request)

    # KPIs
    cursos_activos = ProgresoUsuario.objects.filter(
        usuario=u
    ).values("leccion__modulo__curso").distinct().count()

    lecciones_completadas = ProgresoUsuario.objects.filter(
        usuario=u, completado=True
    ).count()

    certificados = CertificacionObtenida.objects.filter(user=u).count()
    logros = LogroObtenido.objects.filter(user=u).count()

    total_resp = Respuesta.objects.filter(user=u).count()
    correctas = Respuesta.objects.filter(user=u, es_correcta=True).count()
    tasa = round((correctas / total_resp) * 100, 1) if total_resp else 0

    # Progreso por curso (para gráfico de barras)
    cursos_progreso = []
    cursos_ids = ProgresoUsuario.objects.filter(usuario=u).values_list(
        "leccion__modulo__curso_id", flat=True
    ).distinct()
    for cid in cursos_ids:
        curso = Curso.objects.filter(id=cid).first()
        if not curso:
            continue
        total = Leccion.objects.filter(modulo__curso=curso).count()
        completadas = ProgresoUsuario.objects.filter(
            usuario=u, leccion__modulo__curso=curso, completado=True
        ).count()
        pct = round((completadas / total) * 100, 1) if total else 0
        cursos_progreso.append({
            "curso": curso,
            "completadas": completadas,
            "total": total,
            "pct": pct,
        })
    cursos_progreso.sort(key=lambda x: x["pct"], reverse=True)
    cursos_progreso = cursos_progreso[:8]

    # Actividad últimos 30 días
    hoy = timezone.now()
    actividad = []
    for i in range(30):
        dia = hoy - timedelta(days=29 - i)
        inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = inicio + timedelta(days=1)
        n = ProgresoUsuario.objects.filter(
            usuario=u, completado=True,
            completado_en__gte=inicio, completado_en__lt=fin
        ).count()
        actividad.append({"dia": inicio.strftime("%d/%m"), "count": n})

    # Aciertos por tipo de ejercicio
    aciertos_por_tipo = (
        Respuesta.objects.filter(user=u)
        .values("tipo_ejercicio")
        .annotate(
            total=Count("id"),
            correctas=Count("id", filter=Q(es_correcta=True)),
        )
        .order_by("-total")[:6]
    )
    aciertos_data = [
        {"tipo": a["tipo_ejercicio"], "correctas": a["correctas"], "total": a["total"]}
        for a in aciertos_por_tipo
    ]

    # Últimos logros
    ultimos_logros = LogroObtenido.objects.filter(user=u).select_related(
        "logro"
    ).order_by("-fecha_obtenida")[:5]

    # Últimos certificados
    ultimos_certs = CertificacionObtenida.objects.filter(user=u).select_related(
        "certificacion"
    ).order_by("-fecha_obtenida")[:3]

    # Próximas lecciones sugeridas (no completadas)
    proximas = Leccion.objects.filter(
        modulo__curso__estado="publicado"
    ).exclude(
        id__in=ProgresoUsuario.objects.filter(
            usuario=u, completado=True
        ).values_list("leccion_id", flat=True)
    ).select_related("modulo__curso")[:5]

    context = {
        "kpis": {
            "cursos_activos": cursos_activos,
            "lecciones": lecciones_completadas,
            "certificados": certificados,
            "logros": logros,
            "tasa": tasa,
        },
        "cursos_progreso": cursos_progreso,
        "actividad": actividad,
        "aciertos_data": aciertos_data,
        "ultimos_logros": ultimos_logros,
        "ultimos_certs": ultimos_certs,
        "proximas": proximas,
    }
    return render(request, "core/estudiante/dashboard.html", context)


# ============================================================
# MIS CURSOS
# ============================================================
@login_required
def mis_cursos(request):
    u = _get_user(request)
    cursos = Curso.objects.filter(estado="publicado").order_by("titulo")

    data = []
    for curso in cursos:
        total = Leccion.objects.filter(modulo__curso=curso).count()
        completadas = ProgresoUsuario.objects.filter(
            usuario=u, leccion__modulo__curso=curso, completado=True
        ).count()
        pct = round((completadas / total) * 100, 1) if total else 0
        modulos = Modulo.objects.filter(curso=curso).count()
        data.append({
            "curso": curso,
            "total": total,
            "completadas": completadas,
            "pct": pct,
            "modulos": modulos,
        })

    # Ordenar: en progreso primero, luego sin empezar, luego completados
    data.sort(key=lambda x: (-x["pct"] if 0 < x["pct"] < 100 else 0, x["curso"].titulo))

    return render(request, "core/estudiante/mis_cursos.html", {
        "cursos_data": data,
    })


# ============================================================
# MIS EVALUACIONES
# ============================================================
@login_required
def mis_evaluaciones(request):
    u = _get_user(request)

    # Todas las evaluaciones de cursos en los que tiene progreso
    cursos_ids = ProgresoUsuario.objects.filter(usuario=u).values_list(
        "leccion__modulo__curso_id", flat=True
    ).distinct()

    evaluaciones = EvaluacionCurso.objects.filter(
        curso_id__in=cursos_ids
    ).select_related("curso", "modulo").order_by("curso__titulo", "modulo__orden")

    pendientes = []
    completadas = []

    for ev in evaluaciones:
        resultados = ResultadoEvaluacionCurso.objects.filter(
            evaluacion=ev, usuario=u
        ).order_by("-fecha_inicio")
        if resultados.exists():
            mejor = resultados.order_by("-puntaje_obtenido").first()
            completadas.append({
                "ev": ev,
                "intentos": resultados.count(),
                "mejor": mejor.puntaje_obtenido,
                "max": ev.puntaje_maximo,
                "ultimo": resultados.first().fecha_inicio,
            })
        else:
            pendientes.append({"ev": ev})

    return render(request, "core/estudiante/mis_evaluaciones.html", {
        "pendientes": pendientes,
        "completadas": completadas,
        "total": evaluaciones.count(),
    })


# ============================================================
# MIS LOGROS
# ============================================================
@login_required
def mis_logros(request):
    u = _get_user(request)

    obtenidos_ids = LogroObtenido.objects.filter(user=u).values_list(
        "logro_id", flat=True
    )
    obtenidos = LogroObtenido.objects.filter(user=u).select_related("logro").order_by(
        "-fecha_obtenida"
    )
    por_obtener = Logro.objects.exclude(id__in=obtenidos_ids).order_by(
        "puntos_requeridos", "nivel_requerido"
    )

    return render(request, "core/estudiante/mis_logros.html", {
        "obtenidos": obtenidos,
        "por_obtener": por_obtener,
        "total_obtenidos": obtenidos.count(),
        "total_logros": Logro.objects.count(),
    })


# ============================================================
# MIS CERTIFICADOS
# ============================================================
@login_required
def mis_certificados(request):
    u = _get_user(request)

    obtenidos = CertificacionObtenida.objects.filter(user=u).select_related(
        "certificacion"
    ).order_by("-fecha_obtenida")

    # Certificaciones disponibles que aún no tiene
    obtenidos_ids = obtenidos.values_list("certificacion_id", flat=True)
    disponibles = Certificacion.objects.filter(activa=True).exclude(
        id__in=obtenidos_ids
    )

    return render(request, "core/estudiante/mis_certificados.html", {
        "obtenidos": obtenidos,
        "disponibles": disponibles,
        "total": obtenidos.count(),
    })


# ============================================================
# MIS ESTADÍSTICAS
# ============================================================
@login_required
def mis_estadisticas(request):
    u = _get_user(request)

    total_resp = Respuesta.objects.filter(user=u).count()
    correctas = Respuesta.objects.filter(user=u, es_correcta=True).count()
    tasa = round((correctas / total_resp) * 100, 1) if total_resp else 0

    # Promedio por curso
    cursos_stats = []
    cursos_ids = ProgresoUsuario.objects.filter(usuario=u).values_list(
        "leccion__modulo__curso_id", flat=True
    ).distinct()
    for cid in cursos_ids:
        curso = Curso.objects.filter(id=cid).first()
        if not curso:
            continue
        prom = ProgresoUsuario.objects.filter(
            usuario=u, leccion__modulo__curso=curso, completado=True
        ).aggregate(p=Avg("puntaje_obtenido"))["p"] or 0
        completadas = ProgresoUsuario.objects.filter(
            usuario=u, leccion__modulo__curso=curso, completado=True
        ).count()
        cursos_stats.append({
            "curso": curso,
            "promedio": round(prom, 1),
            "completadas": completadas,
        })

    # Progreso por categoría (por tipo de ejercicio)
    por_tipo = (
        Respuesta.objects.filter(user=u)
        .values("tipo_ejercicio")
        .annotate(
            total=Count("id"),
            correctas=Count("id", filter=Q(es_correcta=True)),
        )
        .order_by("-total")
    )
    tipos_data = [
        {
            "tipo": t["tipo_ejercicio"],
            "total": t["total"],
            "correctas": t["correctas"],
            "tasa": round((t["correctas"] / t["total"]) * 100, 1) if t["total"] else 0,
        }
        for t in por_tipo
    ]

    # Actividad
    hoy = timezone.now()
    actividad = []
    for i in range(30):
        dia = hoy - timedelta(days=29 - i)
        inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = inicio + timedelta(days=1)
        n = ProgresoUsuario.objects.filter(
            usuario=u, completado=True,
            completado_en__gte=inicio, completado_en__lt=fin
        ).count()
        actividad.append({"dia": inicio.strftime("%d/%m"), "count": n})

    return render(request, "core/estudiante/mis_estadisticas.html", {
        "total_resp": total_resp,
        "correctas": correctas,
        "tasa": tasa,
        "cursos_stats": cursos_stats,
        "tipos_data": tipos_data,
        "actividad": actividad,
    })


# ============================================================
# MI RANKING
# ============================================================
@login_required
def mi_ranking(request):
    u = _get_user(request)

    # Ranking global por progreso
    estudiantes = User.objects.filter(groups__name="Estudiante").annotate(
        num_progresos=Count(
            "progreso_lecciones",
            filter=Q(progreso_lecciones__completado=True),
            distinct=True,
        ),
        correctas=Count(
            "respuestas",
            filter=Q(respuestas__es_correcta=True),
            distinct=True,
        ),
    ).order_by("-num_progresos", "-correctas")

    mi_posicion = None
    mi_fila = None
    top10 = []
    for i, est in enumerate(estudiantes, start=1):
        if i <= 10:
            top10.append({
                "pos": i,
                "user": est,
                "progresos": est.num_progresos,
                "correctas": est.correctas,
            })
        if est.id == u.id:
            mi_posicion = i
            mi_fila = {
                "pos": i,
                "user": est,
                "progresos": est.num_progresos,
                "correctas": est.correctas,
            }

    return render(request, "core/estudiante/mi_ranking.html", {
        "top10": top10,
        "mi_posicion": mi_posicion,
        "mi_fila": mi_fila,
        "total_estudiantes": estudiantes.count(),
    })


# ============================================================
# DESCARGAS DE CERTIFICADOS (solo los propios)
# ============================================================
@login_required
def descargar_certificado_pdf(request, certificado_id):
    from .utils_certificados import generar_certificado_pdf
    cert = get_object_or_404(CertificacionObtenida, id=certificado_id, user=request.user)
    try:
        pdf_bytes = generar_certificado_pdf(cert, request.user)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("estudiante:certificados")
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="certificado_{cert.codigo_verificacion}.pdf"'
    return response


@login_required
def descargar_certificado_docx(request, certificado_id):
    from .utils_certificados import generar_certificado_docx
    cert = get_object_or_404(CertificacionObtenida, id=certificado_id, user=request.user)
    try:
        docx_bytes = generar_certificado_docx(cert, request.user)
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect("estudiante:certificados")
    response = HttpResponse(
        docx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = f'attachment; filename="certificado_{cert.codigo_verificacion}.docx"'
    return response
