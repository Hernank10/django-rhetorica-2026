"""Vistas completas para cursos, lecciones y evaluaciones"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models_cursos import (
    Curso, Modulo, Leccion, EvaluacionCurso, PreguntaEvaluacion,
    ResultadoEvaluacionCurso,
)

@login_required
def lista_cursos(request):
    cursos = Curso.objects.filter(estado='publicado')
    context = {
        'cursos': cursos,
        'total_cursos': cursos.count(),
    }
    return render(request, 'core/cursos/lista.html', context)

@login_required
def detalle_curso(request, curso_slug):
    """Mostrar detalle de un curso con módulos y lecciones"""
    try:
        curso = Curso.objects.get(slug=curso_slug)
    except Curso.DoesNotExist:
        messages.error(request, 'Curso no encontrado')
        return redirect('lista_cursos')

    # Obtener módulos con lecciones
    modulos = curso.modulos.all().order_by('orden')
    modulos_data = []
    for modulo in modulos:
        lecciones = modulo.lecciones.all().order_by('orden')
        modulos_data.append({
            'modulo': modulo,
            'lecciones': lecciones,
            'progreso': 0,
        })

    # Obtener evaluaciones del curso
    evaluaciones = EvaluacionCurso.objects.filter(curso=curso)

    context = {
        'curso': curso,
        'modulos': modulos_data,
        'evaluaciones': evaluaciones,
        'progreso_total': 0,
    }
    return render(request, 'core/cursos/detalle_completo.html', context)

@login_required
def ver_leccion(request, curso_slug, modulo_id, leccion_id):
    """Ver una lección específica"""
    curso = get_object_or_404(Curso, slug=curso_slug)
    modulo = get_object_or_404(Modulo, id=modulo_id, curso=curso)
    leccion = get_object_or_404(Leccion, id=leccion_id, modulo=modulo)

    ejercicios = leccion.ejercicios_relacionados.all()
    evaluaciones = EvaluacionCurso.objects.filter(modulo=modulo)

    lecciones = list(modulo.lecciones.all().order_by('orden'))
    idx = lecciones.index(leccion)
    leccion_anterior = lecciones[idx - 1] if idx > 0 else None
    leccion_siguiente = lecciones[idx + 1] if idx < len(lecciones) - 1 else None

    context = {
        'curso': curso,
        'modulo': modulo,
        'leccion': leccion,
        'ejercicios': ejercicios,
        'evaluaciones': evaluaciones,
        'leccion_anterior': leccion_anterior,
        'leccion_siguiente': leccion_siguiente,
    }
    return render(request, 'core/cursos/leccion_detalle.html', context)

@login_required
def ver_evaluacion(request, evaluacion_id):
    """Ver una evaluación para realizar"""
    evaluacion = get_object_or_404(EvaluacionCurso, id=evaluacion_id)
    preguntas = PreguntaEvaluacion.objects.filter(evaluacion=evaluacion).order_by('orden')

    curso = evaluacion.curso
    modulo = evaluacion.modulo

    # Primera leccion del modulo (para breadcrumb y boton Volver)
    leccion = None
    if modulo is not None:
        leccion = modulo.lecciones.order_by('orden').first()

    context = {
        'evaluacion': evaluacion,
        'preguntas': preguntas,
        'curso': curso,
        'modulo': modulo,
        'leccion': leccion,
        'total_preguntas': preguntas.count(),
        'intento_actual': 1,
    }
    return render(request, 'core/cursos/evaluacion_detalle.html', context)

@login_required
def enviar_evaluacion(request, evaluacion_id):
    """Procesar el envio de una evaluacion y guardar el resultado."""
    if request.method != 'POST':
        return redirect('lista_cursos')

    evaluacion = get_object_or_404(EvaluacionCurso, id=evaluacion_id)
    preguntas = PreguntaEvaluacion.objects.filter(evaluacion=evaluacion).order_by('orden')

    puntaje_obtenido = 0
    respuestas = {}

    for pregunta in preguntas:
        respuesta_usuario = request.POST.get(f'pregunta_{pregunta.id}', '').strip()
        respuestas[str(pregunta.id)] = respuesta_usuario
        if respuesta_usuario.lower() == pregunta.respuesta_correcta.lower():
            puntaje_obtenido += pregunta.puntaje

    # Guardar/actualizar el resultado del usuario
    resultado, creado = ResultadoEvaluacionCurso.objects.get_or_create(
        evaluacion=evaluacion,
        usuario=request.user,
        defaults={
            'intento': 1,
            'fecha_inicio': timezone.now(),
        },
    )
    if not creado:
        resultado.intento += 1

    resultado.puntaje_obtenido = puntaje_obtenido
    resultado.puntaje_maximo = evaluacion.puntaje_maximo
    resultado.respuestas = respuestas
    resultado.completado = True
    resultado.fecha_completado = timezone.now()
    resultado.save()

    messages.success(
        request,
        f'Evaluacion completada. Puntaje: {puntaje_obtenido}/{evaluacion.puntaje_maximo}',
    )
    return redirect('resultado_evaluacion', evaluacion_id=evaluacion.id)


@login_required
def resultado_evaluacion(request, evaluacion_id):
    """Ver el resultado de la ultima evaluacion del usuario."""
    evaluacion = get_object_or_404(EvaluacionCurso, id=evaluacion_id)
    preguntas = PreguntaEvaluacion.objects.filter(evaluacion=evaluacion).order_by('orden')

    # Ultimo resultado del usuario actual
    resultado = ResultadoEvaluacionCurso.objects.filter(
        evaluacion=evaluacion,
        usuario=request.user,
    ).order_by('-fecha_completado').first()

    # Breadcrumb (mismo patron que ver_evaluacion)
    curso = evaluacion.curso
    modulo = evaluacion.modulo
    leccion = None
    if modulo is not None:
        leccion = modulo.lecciones.order_by('orden').first()

    # Combinar preguntas + respuestas
    preguntas_con_respuestas = []
    if resultado and resultado.respuestas:
        for p in preguntas:
            resp = resultado.respuestas.get(str(p.id), '') or ''
            correcta = resp.strip().lower() == (p.respuesta_correcta or '').strip().lower()
            preguntas_con_respuestas.append({
                'pregunta': p,
                'respuesta_usuario': resp,
                'es_correcta': correcta,
            })

    # Aprobado si >= 60% (ajustable)
    aprobado = False
    porcentaje = 0
    if resultado and resultado.puntaje_maximo:
        porcentaje = int(resultado.puntaje_obtenido * 100 / resultado.puntaje_maximo)
        aprobado = porcentaje >= 60

    context = {
        'evaluacion': evaluacion,
        'preguntas': preguntas,
        'resultado': resultado,
        'curso': curso,
        'modulo': modulo,
        'leccion': leccion,
        'preguntas_con_respuestas': preguntas_con_respuestas,
        'aprobado': aprobado,
        'porcentaje': porcentaje,
    }
    return render(request, 'core/cursos/resultado_evaluacion.html', context)


def api_evaluacion_preguntas(request, evaluacion_id):
    """API para obtener preguntas de una evaluación"""
    try:
        evaluacion = EvaluacionCurso.objects.get(id=evaluacion_id)
        preguntas = PreguntaEvaluacion.objects.filter(evaluacion=evaluacion).order_by('orden')

        data = []
        for p in preguntas:
            data.append({
                'id': p.id,
                'enunciado': p.enunciado,
                'tipo': p.tipo,
                'opciones': p.opciones if p.opciones else [],
                'puntaje': p.puntaje,
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def detalle_curso(request, curso_slug):
    """Mostrar detalle de un curso con módulos y lecciones"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"=== DETALLE CURSO: {curso_slug} ===")
    print(f"=== DETALLE CURSO: {curso_slug} ===")

    try:
        curso = Curso.objects.get(slug=curso_slug)
        print(f"✅ Curso encontrado: {curso.titulo} (ID: {curso.id})")
        logger.info(f"Curso encontrado: {curso.titulo}")
    except Curso.DoesNotExist:
        print(f"❌ Curso NO encontrado con slug: {curso_slug}")
        messages.error(request, 'Curso no encontrado')
        return redirect('lista_cursos')

    # Obtener módulos con lecciones
    modulos = curso.modulos.all().order_by('orden')
    modulos_data = []
    for modulo in modulos:
        lecciones = modulo.lecciones.all().order_by('orden')
        print(f"  📂 Módulo: {modulo.titulo} - {lecciones.count()} lecciones")
        modulos_data.append({
            'modulo': modulo,
            'lecciones': lecciones,
            'progreso': 0,
        })

    # Obtener evaluaciones del curso
    evaluaciones = EvaluacionCurso.objects.filter(curso=curso)
    print(f"  📝 Evaluaciones: {evaluaciones.count()}")

    context = {
        'curso': curso,
        'modulos': modulos_data,
        'evaluaciones': evaluaciones,
        'progreso_total': 0,
    }
    return render(request, 'core/cursos/detalle_completo.html', context)
