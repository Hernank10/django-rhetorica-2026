"""
Panel del profesor: estudiantes, evaluaciones, certificaciones, CRUD cursos y lecciones.
"""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg, Count, Q
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
from .utils import sanitizar_html

User = get_user_model()


def _es_profesor(user):
    return user.is_authenticated and (
        user.is_staff or user.groups.filter(name="Profesor").exists()
    )

profesor_required = user_passes_test(_es_profesor, login_url="login")


# ============================================================
# DASHBOARD
# ============================================================
@profesor_required
def dashboard(request):
    total_estudiantes = User.objects.filter(groups__name="Estudiante").count()
    total_cursos = Curso.objects.count()
    total_evaluaciones = EvaluacionCurso.objects.count()
    total_lecciones = Leccion.objects.count()
    total_certificados = CertificacionObtenida.objects.count()
    total_progresos = ProgresoUsuario.objects.filter(completado=True).count()
    total_respuestas = Respuesta.objects.count()
    tasa_aciertos = 0.0
    if total_respuestas > 0:
        correctas = Respuesta.objects.filter(es_correcta=True).count()
        tasa_aciertos = round((correctas / total_respuestas) * 100, 1)

    ultimos_estudiantes = User.objects.filter(
        groups__name="Estudiante"
    ).order_by("-date_joined")[:5]

    cursos_top = Curso.objects.order_by("-estudiantes_inscritos")[:5]

    context = {
        "kpis": {
            "estudiantes": total_estudiantes,
            "cursos": total_cursos,
            "evaluaciones": total_evaluaciones,
            "lecciones": total_lecciones,
            "certificados": total_certificados,
            "progresos": total_progresos,
            "tasa_aciertos": tasa_aciertos,
        },
        "ultimos_estudiantes": ultimos_estudiantes,
        "cursos_top": cursos_top,
    }
    return render(request, "core/profesor/dashboard.html", context)


# ============================================================
# ESTUDIANTES
# ============================================================
@profesor_required
def lista_estudiantes(request):
    q = request.GET.get("q", "").strip()
    estudiantes = User.objects.filter(groups__name="Estudiante")
    if q:
        estudiantes = estudiantes.filter(
            Q(username__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
        )
    estudiantes = estudiantes.order_by("username")

    data = []
    for est in estudiantes:
        progresos = ProgresoUsuario.objects.filter(usuario=est, completado=True).count()
        certs = CertificacionObtenida.objects.filter(user=est).count()
        logros = LogroObtenido.objects.filter(user=est).count()
        data.append({
            "user": est,
            "progresos": progresos,
            "certificados": certs,
            "logros": logros,
        })

    return render(request, "core/profesor/estudiantes/lista.html", {
        "estudiantes_data": data,
        "total": len(data),
        "q": q,
    })


@profesor_required
def detalle_estudiante(request, estudiante_id):
    """Alias → detalle_estudiante_completo (vista enriquecida)."""
    return detalle_estudiante_completo(request, estudiante_id)


# ============================================================
# EVALUACIONES
# ============================================================
@profesor_required
def lista_evaluaciones(request):
    evaluaciones = EvaluacionCurso.objects.select_related("curso", "modulo").annotate(
        num_preguntas=Count("preguntas")
    ).order_by("curso__titulo", "modulo__orden")
    return render(request, "core/profesor/evaluaciones/lista.html", {
        "evaluaciones": evaluaciones,
        "total": evaluaciones.count(),
    })


# ============================================================
# CERTIFICACIONES
# ============================================================
@profesor_required
def lista_certificaciones(request):
    emitidas = CertificacionObtenida.objects.select_related(
        "user", "certificacion"
    ).order_by("-fecha_obtenida")
    disponibles = Certificacion.objects.filter(activa=True)
    return render(request, "core/profesor/certificaciones/lista.html", {
        "emitidas": emitidas,
        "total_emitidas": emitidas.count(),
        "disponibles": disponibles,
    })


# ============================================================
# CRUD CURSOS
# ============================================================
@profesor_required
def cursos_lista(request):
    cursos = Curso.objects.annotate(
        num_modulos=Count("modulos"),
        num_estudiantes=Count("modulos__lecciones__progresos", distinct=True),
    ).order_by("-creado_en")
    return render(request, "core/profesor/cursos/lista.html", {
        "cursos": cursos,
        "total": cursos.count(),
    })


@profesor_required
def curso_form(request, curso_id=None):
    curso = get_object_or_404(Curso, id=curso_id) if curso_id else None
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        objetivo = request.POST.get("objetivo", "").strip()
        nivel = request.POST.get("nivel", "basico")
        estado = request.POST.get("estado", "borrador")
        duracion = request.POST.get("duracion_estimada", 60) or 60
        puntos = request.POST.get("puntos_totales", 100) or 100

        if not titulo:
            messages.error(request, "El título es obligatorio.")
        else:
            if curso is None:
                slug = titulo.lower().replace(" ", "-")
                slug = "".join(ch for ch in slug if ch.isalnum() or ch == "-")
                if Curso.objects.filter(slug=slug).exists():
                    slug = f"{slug}-{int(timezone.now().timestamp())}"
                curso = Curso(
                    titulo=titulo, slug=slug,
                    creado_por=request.user,
                )
            curso.titulo = titulo
            curso.descripcion = descripcion
            curso.objetivo = objetivo
            curso.nivel = nivel
            curso.estado = estado
            curso.duracion_estimada = int(duracion)
            curso.puntos_totales = int(puntos)
            if estado == "publicado" and not curso.publicado_en:
                curso.publicado_en = timezone.now()
            curso.save()
            messages.success(request, f'Curso "{curso.titulo}" guardado.')
            return redirect("profesor:cursos_lista")

    return render(request, "core/profesor/cursos/form.html", {
        "curso": curso,
        "niveles": Curso._meta.get_field("nivel").choices,
        "estados": Curso._meta.get_field("estado").choices,
    })


@profesor_required
def curso_eliminar(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if request.method == "POST":
        nombre = curso.titulo
        curso.delete()
        messages.success(request, f'Curso "{nombre}" eliminado.')
    return redirect("profesor:cursos_lista")


# ============================================================
# CRUD LECCIONES
# ============================================================
@profesor_required
def lecciones_lista(request):
    curso_id = request.GET.get("curso")
    modulo_id = request.GET.get("modulo")
    lecciones = Leccion.objects.select_related("modulo__curso").order_by(
        "modulo__curso__titulo", "modulo__orden", "orden"
    )
    if curso_id:
        lecciones = lecciones.filter(modulo__curso_id=curso_id)
    if modulo_id:
        lecciones = lecciones.filter(modulo_id=modulo_id)
    return render(request, "core/profesor/lecciones/lista.html", {
        "lecciones": lecciones,
        "cursos": Curso.objects.all().order_by("titulo"),
        "curso_sel": curso_id,
        "modulo_sel": modulo_id,
    })


@profesor_required
def leccion_form(request, leccion_id=None):
    leccion = get_object_or_404(Leccion, id=leccion_id) if leccion_id else None
    if request.method == "POST":
        modulo_id = request.POST.get("modulo")
        titulo = request.POST.get("titulo", "").strip()

        contenido = sanitizar_html(request.POST.get("contenido", ""))
        tipo = request.POST.get("tipo", "lectura")
        orden = request.POST.get("orden", 1) or 1
        duracion = request.POST.get("duracion_estimada", 15) or 15
        puntos = request.POST.get("puntos", 10) or 10

        modulo = get_object_or_404(Modulo, id=modulo_id) if modulo_id else None

        if not titulo or not modulo:
            messages.error(request, "Título y módulo son obligatorios.")
        else:
            if leccion is None:
                leccion = Leccion(modulo=modulo)
            else:
                leccion.modulo = modulo
            leccion.titulo = titulo
            leccion.contenido = contenido
            leccion.tipo = tipo
            leccion.orden = int(orden)
            leccion.duracion_estimada = int(duracion)
            leccion.puntos = int(puntos)
            leccion.save()
            messages.success(request, f'Lección "{leccion.titulo}" guardada.')
            return redirect("profesor:lecciones_lista")

    return render(request, "core/profesor/lecciones/form.html", {
        "leccion": leccion,
        "modulos": Modulo.objects.select_related("curso").order_by("curso__titulo", "orden"),
        "tipos": Leccion._meta.get_field("tipo").choices if hasattr(Leccion._meta.get_field("tipo"), "choices") else [("lectura","Lectura"),("practica","Práctica"),("video","Video")],
    })


@profesor_required
def leccion_eliminar(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    if request.method == "POST":
        nombre = leccion.titulo
        leccion.delete()
        messages.success(request, f'Lección "{nombre}" eliminada.')
    return redirect("profesor:lecciones_lista")


# ============================================================
# CRUD MÓDULOS
# ============================================================
@profesor_required
def modulos_lista(request):
    curso_id = request.GET.get("curso")
    modulos = Modulo.objects.select_related("curso").order_by("curso__titulo", "orden")
    if curso_id:
        modulos = modulos.filter(curso_id=curso_id)
    return render(request, "core/profesor/modulos/lista.html", {
        "modulos": modulos,
        "cursos": Curso.objects.all().order_by("titulo"),
        "curso_sel": curso_id,
    })


@profesor_required
def modulo_form(request, modulo_id=None):
    modulo = get_object_or_404(Modulo, id=modulo_id) if modulo_id else None
    curso_pre = request.GET.get("curso")

    if request.method == "POST":
        curso_id = request.POST.get("curso")
        titulo = request.POST.get("titulo", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        orden = request.POST.get("orden", 1) or 1

        curso = get_object_or_404(Curso, id=curso_id) if curso_id else None

        if not titulo or not curso:
            messages.error(request, "Título y curso son obligatorios.")
        else:
            if modulo is None:
                modulo = Modulo(curso=curso)
            else:
                modulo.curso = curso
            modulo.titulo = titulo
            modulo.descripcion = descripcion
            modulo.orden = int(orden)
            modulo.save()
            messages.success(request, f'Módulo "{modulo.titulo}" guardado.')
            return redirect("profesor:modulos_lista")

    return render(request, "core/profesor/modulos/form.html", {
        "modulo": modulo,
        "cursos": Curso.objects.all().order_by("titulo"),
        "curso_pre": curso_pre,
    })


@profesor_required
def modulo_eliminar(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    if request.method == "POST":
        nombre = modulo.titulo
        modulo.delete()
        messages.success(request, f'Módulo "{nombre}" eliminado.')
    return redirect("profesor:modulos_lista")


# ============================================================
# CRUD EVALUACIONES CON TIPOS
# ============================================================
@profesor_required
def evaluacion_form(request, evaluacion_id=None):
    """Crear/editar evaluación con tipo: diagnostica, modulo, recapitulacion, final"""
    ev = get_object_or_404(EvaluacionCurso, id=evaluacion_id) if evaluacion_id else None
    curso_pre = request.GET.get("curso")

    if request.method == "POST":
        curso_id = request.POST.get("curso")
        modulo_id = request.POST.get("modulo") or None
        titulo = request.POST.get("titulo", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        tipo = request.POST.get("tipo", "modulo")
        preguntas_por_evaluacion = int(request.POST.get("preguntas_por_evaluacion", 5) or 5)
        tiempo_limite = int(request.POST.get("tiempo_limite", 30) or 30)
        puntaje_maximo = int(request.POST.get("puntaje_maximo", 100) or 100)
        intentos = int(request.POST.get("intentos_permitidos", 3) or 3)

        curso = get_object_or_404(Curso, id=curso_id) if curso_id else None
        modulo = get_object_or_404(Modulo, id=modulo_id) if modulo_id else None

        if not titulo or not curso:
            messages.error(request, "Título y curso son obligatorios.")
        else:
            if ev is None:
                ev = EvaluacionCurso(curso=curso)
            else:
                ev.curso = curso
            ev.modulo = modulo
            ev.titulo = titulo
            ev.descripcion = descripcion
            ev.tipo = tipo
            ev.preguntas_por_evaluacion = preguntas_por_evaluacion
            ev.tiempo_limite = tiempo_limite
            ev.puntaje_maximo = puntaje_maximo
            ev.intentos_permitidos = intentos
            ev.save()
            messages.success(request, f'Evaluación "{ev.titulo}" guardada.')
            return redirect("profesor:evaluacion_detalle", evaluacion_id=ev.id)

    return render(request, "core/profesor/evaluaciones/form.html", {
        "evaluacion": ev,
        "cursos": Curso.objects.all().order_by("titulo"),
        "modulos": Modulo.objects.select_related("curso").order_by("curso__titulo", "orden"),
        "curso_pre": curso_pre,
    })


@profesor_required
def evaluacion_detalle(request, evaluacion_id):
    ev = get_object_or_404(EvaluacionCurso, id=evaluacion_id)
    preguntas = ev.preguntas.all().order_by("orden")
    return render(request, "core/profesor/evaluaciones/detalle.html", {
        "evaluacion": ev,
        "preguntas": preguntas,
    })


@profesor_required
def evaluacion_eliminar(request, evaluacion_id):
    ev = get_object_or_404(EvaluacionCurso, id=evaluacion_id)
    if request.method == "POST":
        nombre = ev.titulo
        ev.delete()
        messages.success(request, f'Evaluación "{nombre}" eliminada.')
    return redirect("profesor:evaluaciones")


# ============================================================
# CRUD PREGUNTAS (anidadas en evaluación)
# ============================================================
@profesor_required
def pregunta_form(request, evaluacion_id, pregunta_id=None):
    ev = get_object_or_404(EvaluacionCurso, id=evaluacion_id)
    pregunta = get_object_or_404(PreguntaEvaluacion, id=pregunta_id) if pregunta_id else None

    if request.method == "POST":
        enunciado = request.POST.get("enunciado", "").strip()
        tipo = request.POST.get("tipo", "multiple_choice")
        opciones_raw = request.POST.get("opciones", "").strip()
        correcta = request.POST.get("respuesta_correcta", "").strip()
        puntaje = int(request.POST.get("puntaje", 20) or 20)
        orden = int(request.POST.get("orden", 1) or 1)

        # opciones: una por linea
        opciones = [{"texto": o.strip()} for o in opciones_raw.splitlines() if o.strip()]

        if not enunciado:
            messages.error(request, "El enunciado es obligatorio.")
        else:
            if pregunta is None:
                pregunta = PreguntaEvaluacion(evaluacion=ev)
            pregunta.enunciado = enunciado
            pregunta.tipo = tipo
            pregunta.opciones = opciones
            pregunta.respuesta_correcta = correcta
            pregunta.puntaje = puntaje
            pregunta.orden = orden
            pregunta.save()
            messages.success(request, "Pregunta guardada.")
            return redirect("profesor:evaluacion_detalle", evaluacion_id=ev.id)

    return render(request, "core/profesor/evaluaciones/pregunta_form.html", {
        "evaluacion": ev,
        "pregunta": pregunta,
    })


@profesor_required
def pregunta_eliminar(request, evaluacion_id, pregunta_id):
    ev = get_object_or_404(EvaluacionCurso, id=evaluacion_id)
    pregunta = get_object_or_404(PreguntaEvaluacion, id=pregunta_id)
    if request.method == "POST":
        pregunta.delete()
        messages.success(request, "Pregunta eliminada.")
    return redirect("profesor:evaluacion_detalle", evaluacion_id=ev.id)


# ============================================================
# TOGGLE PUBLICAR / BORRADOR
# ============================================================
@profesor_required
def curso_toggle_publicar(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if curso.estado == "publicado":
        curso.estado = "borrador"
        curso.publicado_en = None
        messages.info(request, f'Curso "{curso.titulo}" pasado a borrador.')
    else:
        curso.estado = "publicado"
        curso.publicado_en = timezone.now()
        messages.success(request, f'Curso "{curso.titulo}" publicado.')
    curso.save()
    return redirect("profesor:cursos_lista")


# ============================================================
# DETALLE ESTUDIANTE ENRIQUECIDO
# ============================================================
@profesor_required
def detalle_estudiante_completo(request, estudiante_id):
    """Vista con cursos asignados, evaluaciones y certificados del estudiante."""
    from django.db.models import Avg, Count

    estudiante = get_object_or_404(User, id=estudiante_id)

    # Cursos en los que tiene progreso
    cursos_data = []
    cursos_ids = ProgresoUsuario.objects.filter(
        usuario=estudiante
    ).values_list("leccion__modulo__curso_id", flat=True).distinct()

    for curso_id in cursos_ids:
        try:
            curso = Curso.objects.get(id=curso_id)
        except Curso.DoesNotExist:
            continue
        total_lecciones = Leccion.objects.filter(modulo__curso=curso).count()
        completadas = ProgresoUsuario.objects.filter(
            usuario=estudiante, leccion__modulo__curso=curso, completado=True
        ).count()
        promedio = ProgresoUsuario.objects.filter(
            usuario=estudiante, leccion__modulo__curso=curso, completado=True
        ).aggregate(p=Avg("puntaje_obtenido"))["p"] or 0
        progreso_pct = round((completadas / total_lecciones) * 100, 1) if total_lecciones else 0

        cursos_data.append({
            "curso": curso,
            "total_lecciones": total_lecciones,
            "completadas": completadas,
            "progreso_pct": progreso_pct,
            "promedio": round(promedio, 1),
        })

    # Evaluaciones del curso realizadas
    evaluaciones_data = []
    for curso_info in cursos_data:
        curso = curso_info["curso"]
        evaluaciones = EvaluacionCurso.objects.filter(curso=curso)
        for ev in evaluaciones:
            resultados = ResultadoEvaluacionCurso.objects.filter(
                evaluacion=ev, usuario=estudiante
            ).order_by("-fecha_inicio")
            if resultados.exists():
                mejor = resultados.order_by("-puntaje_obtenido").first()
                evaluaciones_data.append({
                    "evaluacion": ev,
                    "intentos": resultados.count(),
                    "mejor_puntaje": mejor.puntaje_obtenido,
                    "puntaje_maximo": ev.puntaje_maximo,
                    "ultimo_intento": resultados.first().fecha_inicio,
                })

    # Certificados y logros
    certificados = CertificacionObtenida.objects.filter(
        user=estudiante
    ).select_related("certificacion")
    logros = LogroObtenido.objects.filter(user=estudiante).select_related("logro")

    # Respuestas recientes
    respuestas = Respuesta.objects.filter(user=estudiante).order_by("-fecha")[:15]
    total_respuestas = Respuesta.objects.filter(user=estudiante).count()
    correctas = Respuesta.objects.filter(user=estudiante, es_correcta=True).count()
    tasa = round((correctas / total_respuestas) * 100, 1) if total_respuestas else 0

    context = {
        "estudiante": estudiante,
        "cursos_data": cursos_data,
        "evaluaciones_data": evaluaciones_data,
        "certificados": certificados,
        "logros": logros,
        "respuestas": respuestas,
        "stats": {
            "total_respuestas": total_respuestas,
            "correctas": correctas,
            "tasa_aciertos": tasa,
            "cursos_activos": len(cursos_data),
            "certificados": certificados.count(),
            "logros": logros.count(),
        },
    }
    return render(request, "core/profesor/estudiantes/detalle.html", context)


# ============================================================
# ESTADÍSTICAS Y RANKING
# ============================================================
from datetime import timedelta

from django.db.models import Sum


@profesor_required
def estadisticas_dashboard(request):
    """Estadísticas globales con datos para gráficos."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # --- KPIs globales ---
    total_est = User.objects.filter(groups__name="Estudiante").count()
    total_progresos = ProgresoUsuario.objects.filter(completado=True).count()
    total_resp = Respuesta.objects.count()
    total_correctas = Respuesta.objects.filter(es_correcta=True).count()
    tasa_global = round((total_correctas / total_resp) * 100, 1) if total_resp else 0

    # --- Top 10 estudiantes por progreso ---
    top_por_progreso = (
        User.objects.filter(groups__name="Estudiante")
        .annotate(num_progresos=Count("progreso_lecciones", filter=Q(progreso_lecciones__completado=True)))
        .order_by("-num_progresos")[:10]
    )

    # --- Top 10 por respuestas correctas ---
    top_por_aciertos = (
        User.objects.filter(groups__name="Estudiante")
        .annotate(
            correctas=Count("respuestas", filter=Q(respuestas__es_correcta=True)),
            total=Count("respuestas"),
        )
        .filter(total__gt=0)
        .order_by("-correctas")[:10]
    )

    # --- Estadísticas por curso ---
    cursos = Curso.objects.all()
    cursos_stats = []
    for curso in cursos:
        total_lecciones = Leccion.objects.filter(modulo__curso=curso).count()
        total_inscritos = ProgresoUsuario.objects.filter(
            leccion__modulo__curso=curso
        ).values("usuario").distinct().count()
        completadas = ProgresoUsuario.objects.filter(
            leccion__modulo__curso=curso, completado=True
        ).count()
        prom = ProgresoUsuario.objects.filter(
            leccion__modulo__curso=curso, completado=True
        ).aggregate(p=Avg("puntaje_obtenido"))["p"] or 0
        cursos_stats.append({
            "curso": curso,
            "inscritos": total_inscritos,
            "completadas": completadas,
            "promedio": round(prom, 1),
        })
    cursos_stats.sort(key=lambda x: x["inscritos"], reverse=True)

    # --- Actividad últimos 30 días ---
    hoy = timezone.now()
    hace_30 = hoy - timedelta(days=30)
    actividad_diaria = []
    for i in range(30):
        dia = hoy - timedelta(days=29 - i)
        inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = inicio + timedelta(days=1)
        n = ProgresoUsuario.objects.filter(
            completado=True, completado_en__gte=inicio, completado_en__lt=fin
        ).count()
        actividad_diaria.append({
            "dia": inicio.strftime("%d/%m"),
            "count": n,
        })

    # --- Distribución por nivel de actividad (rangos de progreso) ---
    estudiantes_qs = User.objects.filter(groups__name="Estudiante").annotate(
        num_progresos=Count("progreso_lecciones", filter=Q(progreso_lecciones__completado=True))
    )
    rangos = [
        ("Sin actividad", 0, 0),
        ("Principiante (1-5)", 1, 5),
        ("Intermedio (6-20)", 6, 20),
        ("Avanzado (21-50)", 21, 50),
        ("Experto (51+)", 51, 10**9),
    ]
    niveles_data = []
    for nombre, min_, max_ in rangos:
        n = estudiantes_qs.filter(num_progresos__gte=min_, num_progresos__lte=max_).count()
        niveles_data.append({"nivel": nombre, "count": n})

    context = {
        "kpis": {
            "total_est": total_est,
            "total_progresos": total_progresos,
            "total_resp": total_resp,
            "total_correctas": total_correctas,
            "tasa_global": tasa_global,
        },
        "top_por_progreso": top_por_progreso,
        "top_por_aciertos": top_por_aciertos,
        "cursos_stats": cursos_stats,
        "actividad_diaria": actividad_diaria,
        "niveles_data": niveles_data,
    }
    return render(request, "core/profesor/estadisticas.html", context)


@profesor_required
def ranking_estudiantes(request):
    """Ranking completo de estudiantes con filtros."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    orden = request.GET.get("orden", "progreso")

    qs = User.objects.filter(groups__name="Estudiante").annotate(
        num_progresos=Count("progreso_lecciones", filter=Q(progreso_lecciones__completado=True), distinct=True),
        num_respuestas=Count("respuestas", distinct=True),
        correctas=Count("respuestas", filter=Q(respuestas__es_correcta=True), distinct=True),
        num_logros=Count("logros_obtenidos", distinct=True),
        num_certificados=Count("certificaciones_obtenidas", distinct=True),
    )

    if orden == "correctas":
        qs = qs.order_by("-correctas", "-num_progresos")
    elif orden == "logros":
        qs = qs.order_by("-num_logros", "-num_progresos")
    elif orden == "certificados":
        qs = qs.order_by("-num_certificados", "-num_progresos")
    else:  # progreso
        qs = qs.order_by("-num_progresos", "-correctas")

    ranking = qs[:100]

    # Calcular tasa de aciertos para cada uno
    data = []
    for i, u in enumerate(ranking, start=1):
        tasa = round((u.correctas / u.num_respuestas) * 100, 1) if u.num_respuestas else 0
        data.append({
            "pos": i,
            "user": u,
            "progresos": u.num_progresos,
            "respuestas": u.num_respuestas,
            "correctas": u.correctas,
            "tasa": tasa,
            "logros": u.num_logros,
            "certificados": u.num_certificados,
        })

    return render(request, "core/profesor/ranking.html", {
        "ranking": data,
        "orden": orden,
    })


# ============================================================
# DESCARGAR CERTIFICADOS (PDF / DOCX)
# ============================================================
from django.http import HttpResponse


@profesor_required
def certificado_pdf(request, certificado_id):
    """Descarga el certificado en PDF tipo diploma."""
    from django.contrib.auth import get_user_model

    from .utils_certificados import generar_certificado_pdf
    User = get_user_model()

    cert = get_object_or_404(CertificacionObtenida, id=certificado_id)
    alumno = cert.user

    try:
        pdf_bytes = generar_certificado_pdf(cert, alumno)
    except Exception as e:
        messages.error(request, f"Error generando PDF: {e}")
        return redirect("profesor:certificaciones")

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="certificado_{cert.codigo_verificacion}.pdf"'
    return response


@profesor_required
def certificado_docx(request, certificado_id):
    """Descarga el certificado en Word editable."""
    from django.contrib.auth import get_user_model

    from .utils_certificados import generar_certificado_docx
    User = get_user_model()

    cert = get_object_or_404(CertificacionObtenida, id=certificado_id)
    alumno = cert.user

    try:
        docx_bytes = generar_certificado_docx(cert, alumno)
    except Exception as e:
        messages.error(request, f"Error generando DOCX: {e}")
        return redirect("profesor:certificaciones")

    response = HttpResponse(
        docx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = f'attachment; filename="certificado_{cert.codigo_verificacion}.docx"'
    return response


# ============================================================
# VISTA PREVIA HTML DEL CERTIFICADO
# ============================================================
@profesor_required
def certificado_preview(request, certificado_id):
    """Vista previa HTML del certificado (diseño diploma)."""
    from .utils_certificados import folio_unico, huella_certificado, huella_corta

    cert = get_object_or_404(CertificacionObtenida, id=certificado_id)
    return render(request, "core/profesor/certificados/preview.html", {
        "cert": cert,
        "alumno": cert.user,
        "huella": huella_certificado(cert),
        "huella_corta": huella_corta(cert),
        "folio": folio_unico(cert),
    })

# ============================================================
# RECURSOS DEL PROFESOR
# ============================================================
from .models import Recurso


@profesor_required
def recursos_lista(request):
    """Lista de recursos con filtros."""
    from django.db.models import Count, Q

    q = request.GET.get("q", "").strip()
    cat = request.GET.get("cat", "").strip()
    ext = request.GET.get("ext", "").strip()
    curso_id = request.GET.get("curso", "").strip()

    qs = Recurso.objects.all()
    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(archivo__icontains=q))
    if cat:
        qs = qs.filter(categoria=cat)
    if ext:
        qs = qs.filter(extension=ext)
    if curso_id:
        qs = qs.filter(curso_id=curso_id)

    qs = qs.order_by("categoria", "nombre")[:500]

    categorias = Recurso.objects.values("categoria").annotate(n=Count("id")).order_by("-n")
    extensiones = Recurso.objects.values("extension").annotate(n=Count("id")).order_by("-n")

    return render(request, "core/profesor/recursos/lista.html", {
        "recursos": qs,
        "categorias": categorias,
        "extensiones": extensiones,
        "cursos": Curso.objects.all().order_by("titulo"),
        "q": q,
        "cat": cat,
        "ext": ext,
        "curso_sel": curso_id,
    })


@profesor_required
def recurso_asignar(request, recurso_id):
    """Asignar un recurso a un curso."""
    recurso = get_object_or_404(Recurso, id=recurso_id)
    if request.method == "POST":
        curso_id = request.POST.get("curso") or None
        recurso.curso_id = curso_id
        recurso.save(update_fields=["curso"])
        messages.success(request, f'Recurso asignado a {recurso.curso.titulo if recurso.curso else "ninguno"}.')
        return redirect("profesor:recursos_lista")
    return render(request, "core/profesor/recursos/asignar.html", {
        "recurso": recurso,
        "cursos": Curso.objects.all().order_by("titulo"),
    })


@profesor_required
def recursos_autovincular(request):
    """Auto-vincular recursos a cursos por palabras clave en el nombre."""
    if request.method == "POST":
        reglas = {
            "Morfología": ["morfolog", "morfema", "lexema", "raíces", "raices"],
            "Sintaxis": ["sintax", "oración", "oracion", "sujeto", "predicado"],
            "Ortografía": ["ortograf", "tildes", "puntuación", "puntuacion", "coma", "acento"],
            "Redacción": ["redacc", "párrafo", "parrafo", "escritur", "caligraf"],
            "Retórica": ["retóric", "retoric", "figura", "tropos", "metáfora", "metafora"],
            "Etimología": ["etimolog", "grecolatin", "raíz", "helenism", "latinism"],
            "Comprensión Lectora": ["comprensi", "lectura", "lector"],
            "Literatura": ["literatur", "novel", "cuento", "poesía", "poesia"],
            "Poesía": ["poesí", "poesia", "haiku", "verso", "poema"],
            "Ensayo": ["ensay", "aforism"],
            "Oratoria": ["orator", "discurso", "podcast", "teatr"],
            "Argumentación": ["argument", "silogism", "falacia"],
        }

        asignados = 0
        for curso_titulo, keywords in reglas.items():
            try:
                curso = Curso.objects.get(titulo=curso_titulo)
            except Curso.DoesNotExist:
                continue

            from django.db.models import Q
            q = Q()
            for kw in keywords:
                q |= Q(nombre__icontains=kw) | Q(archivo__icontains=kw)
            n = Recurso.objects.filter(q, curso__isnull=True).update(curso=curso)
            asignados += n
            if n:
                messages.info(request, f'{curso.titulo}: {n} recursos asignados')

        messages.success(request, f'Total: {asignados} recursos vinculados.')
        return redirect("profesor:recursos_lista")

    # GET: mostrar previsualización
    return render(request, "core/profesor/recursos/autovincular.html", {
        "cursos": Curso.objects.all().order_by("titulo"),
    })
