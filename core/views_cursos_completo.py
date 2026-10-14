"""Vistas completas para cursos, lecciones y evaluaciones"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models_cursos import (
    Curso,
    EvaluacionCurso,
    Leccion,
    Modulo,
    PreguntaEvaluacion,
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
