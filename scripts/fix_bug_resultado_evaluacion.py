"""Fix completo del bug resultado_evaluacion.

1) Import ResultadoEvaluacionCurso en views_cursos_completo.py
2) enviar_evaluacion: guardar en ResultadoEvaluacionCurso + redirigir a resultado
3) resultado_evaluacion: pasar resultado, respuestas, breadcrumb
4) Crear template resultado_evaluacion.html
"""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")
vp = BASE / "core" / "views_cursos_completo.py"
TP = BASE / "core" / "templates" / "core" / "cursos" / "resultado_evaluacion.html"

c = vp.read_text(encoding="utf-8")

# ============================================================
# 1) Anadir import de ResultadoEvaluacionCurso
# ============================================================
if "ResultadoEvaluacionCurso" not in c.split("\n\n")[0] and "ResultadoEvaluacionCurso" not in c[:1500]:
    patron_import = re.compile(
        r"(from \.models_cursos import\s+Curso,\s*Modulo,\s*Leccion,\s*EvaluacionCurso,\s*PreguntaEvaluacion)"
    )
    if patron_import.search(c):
        c = patron_import.sub(
            r"from .models_cursos import (\n    Curso, Modulo, Leccion, EvaluacionCurso, PreguntaEvaluacion,\n    ResultadoEvaluacionCurso,\n)",
            c, count=1,
        )
        print("[OK] Import ResultadoEvaluacionCurso anadido")
    else:
        # Fallback: agregar linea nueva despues del import existente
        patron2 = re.compile(r"(from \.models_cursos import [^\n]+\n)")
        c = patron2.sub(r"\1from .models_cursos import ResultadoEvaluacionCurso\n", c, count=1)
        print("[OK] Import ResultadoEvaluacionCurso anadido (fallback)")
elif "ResultadoEvaluacionCurso" in c[:1500]:
    print("[SKIP] Import ya presente")

vp.write_text(c, encoding="utf-8")


# ============================================================
# 2) Reemplazar enviar_evaluacion
# ============================================================
c = vp.read_text(encoding="utf-8")

viejo_enviar = '''def enviar_evaluacion(request, evaluacion_id):
    """Procesar el env\u00edo de una evaluaci\u00f3n"""
    if request.method != 'POST':
        return redirect('lista_cursos')

    evaluacion = get_object_or_404(EvaluacionCurso, id=evaluacion_id)
    preguntas = PreguntaEvaluacion.objects.filter(evaluacion=evaluacion)

    puntaje_obtenido = 0
    respuestas = {}

    for pregunta in preguntas:
        respuesta_usuario = request.POST.get(f'pregunta_{pregunta.id}', '').strip()
        respuestas[str(pregunta.id)] = respuesta_usuario

        if respuesta_usuario.lower() == pregunta.respuesta_correcta.lower():
            puntaje_obtenido += pregunta.puntaje

    messages.success(request, f'? Evaluaci?n completada! Puntaje: {puntaje_obtenido}/{evaluacion.puntaje_maximo}')
    return redirect('detalle_curso', curso_slug=evaluacion.curso.slug)'''

nuevo_enviar = '''def enviar_evaluacion(request, evaluacion_id):
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
    return redirect('resultado_evaluacion', evaluacion_id=evaluacion.id)'''

if viejo_enviar in c:
    c = c.replace(viejo_enviar, nuevo_enviar, 1)
    vp.write_text(c, encoding="utf-8")
    print("[OK] enviar_evaluacion reescrita (guarda resultado + redirige a resultado)")
elif "resultado, creado = ResultadoEvaluacionCurso.objects.get_or_create" in c:
    print("[SKIP] enviar_evaluacion ya estaba modificada")
else:
    # Intento flexible con regex
    patron = re.compile(
        r"def\s+enviar_evaluacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if patron.search(c):
        c = patron.sub(nuevo_enviar + "\n\n\n", c, count=1)
        vp.write_text(c, encoding="utf-8")
        print("[OK] enviar_evaluacion reescrita (regex fallback)")
    else:
        print("[!] No se encontro enviar_evaluacion")


# ============================================================
# 3) Reemplazar resultado_evaluacion
# ============================================================
c = vp.read_text(encoding="utf-8")

viejo_resultado = '''def resultado_evaluacion(request, evaluacion_id):
    """Ver resultado de una evaluaci\u00f3n"""
    evaluacion = get_object_or_404(EvaluacionCurso, id=evaluacion_id)

    context = {
        'evaluacion': evaluacion,
        'preguntas': PreguntaEvaluacion.objects.filter(evaluacion=evaluacion),
    }
    return render(request, 'core/cursos/resultado_evaluacion.html', context)'''

nuevo_resultado = '''def resultado_evaluacion(request, evaluacion_id):
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
    return render(request, 'core/cursos/resultado_evaluacion.html', context)'''

if viejo_resultado in c:
    c = c.replace(viejo_resultado, nuevo_resultado, 1)
    vp.write_text(c, encoding="utf-8")
    print("[OK] resultado_evaluacion reescrita")
elif "preguntas_con_respuestas" in c:
    print("[SKIP] resultado_evaluacion ya estaba modificada")
else:
    patron = re.compile(
        r"def\s+resultado_evaluacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if patron.search(c):
        c = patron.sub(nuevo_resultado + "\n\n\n", c, count=1)
        vp.write_text(c, encoding="utf-8")
        print("[OK] resultado_evaluacion reescrita (regex fallback)")
    else:
        print("[!] No se encontro resultado_evaluacion")


# ============================================================
# 4) Anadir import de timezone si falta
# ============================================================
c = vp.read_text(encoding="utf-8")
if "from django.utils import timezone" not in c:
    c = c.replace(
        "from django.shortcuts import render, redirect, get_object_or_404",
        "from django.shortcuts import render, redirect, get_object_or_404\nfrom django.utils import timezone",
        1,
    )
    vp.write_text(c, encoding="utf-8")
    print("[OK] import timezone anadido")
else:
    print("[SKIP] timezone ya importado")


# ============================================================
# 5) Crear template
# ============================================================
if TP.exists():
    print("[SKIP] Template ya existe")
else:
    TP.parent.mkdir(parents=True, exist_ok=True)
    template = '''{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-lg-9 mx-auto">

            <!-- Breadcrumb -->
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{% url 'lista_cursos' %}">Cursos</a></li>
                    {% if curso %}
                        <li class="breadcrumb-item"><a href="{% url 'detalle_curso' curso.slug %}">{{ curso.titulo|truncatechars:30 }}</a></li>
                    {% endif %}
                    {% if modulo and leccion %}
                        <li class="breadcrumb-item"><a href="{% url 'ver_leccion' curso.slug modulo.id leccion.id %}">{{ modulo.titulo|truncatechars:30 }}</a></li>
                    {% endif %}
                    <li class="breadcrumb-item"><a href="{% url 'ver_evaluacion' evaluacion.id %}">Evaluacion</a></li>
                    <li class="breadcrumb-item active">Resultados</li>
                </ol>
            </nav>

            <!-- Card de resultado -->
            <div class="card shadow mb-4">
                <div class="card-header {% if aprobado %}bg-success{% else %}bg-danger{% endif %} text-white">
                    <div class="d-flex justify-content-between align-items-center">
                        <h4 class="mb-0">
                            {% if aprobado %}
                                <i class="fas fa-check-circle"></i> Evaluacion aprobada
                            {% else %}
                                <i class="fas fa-times-circle"></i> Evaluacion no aprobada
                            {% endif %}
                        </h4>
                        <span class="badge bg-light text-dark">{{ evaluacion.titulo|truncatechars:40 }}</span>
                    </div>
                </div>
                <div class="card-body">

                    {% if resultado %}
                        <div class="row text-center mb-4">
                            <div class="col-md-3">
                                <div class="display-3 fw-bold {% if aprobado %}text-success{% else %}text-danger{% endif %}">
                                    {{ resultado.puntaje_obtenido }}
                                </div>
                                <small class="text-muted">Puntaje obtenido</small>
                            </div>
                            <div class="col-md-3">
                                <div class="display-3 fw-bold text-secondary">{{ resultado.puntaje_maximo }}</div>
                                <small class="text-muted">Puntaje maximo</small>
                            </div>
                            <div class="col-md-3">
                                <div class="display-3 fw-bold {% if aprobado %}text-success{% else %}text-danger{% endif %}">
                                    {{ porcentaje }}%
                                </div>
                                <small class="text-muted">Porcentaje</small>
                            </div>
                            <div class="col-md-3">
                                <div class="display-3 fw-bold text-info">{{ resultado.intento }}</div>
                                <small class="text-muted">Intento #</small>
                            </div>
                        </div>

                        <hr>

                        <div class="row mb-3">
                            <div class="col-md-6">
                                <p class="mb-1"><i class="fas fa-calendar-alt"></i> <strong>Completado:</strong>
                                    {{ resultado.fecha_completado|date:"d/m/Y H:i" }}</p>
                            </div>
                            <div class="col-md-6 text-md-end">
                                {% if resultado.tiempo_empleado %}
                                    <p class="mb-1"><i class="fas fa-clock"></i> <strong>Tiempo:</strong>
                                        {{ resultado.tiempo_empleado }}s</p>
                                {% endif %}
                            </div>
                        </div>
                    {% else %}
                        <div class="alert alert-warning">
                            <i class="fas fa-exclamation-triangle"></i>
                            Aun no has completado esta evaluacion.
                            <a href="{% url 'ver_evaluacion' evaluacion.id %}" class="alert-link">Comenzar ahora</a>
                        </div>
                    {% endif %}

                </div>
            </div>

            <!-- Detalle por pregunta -->
            {% if preguntas_con_respuestas %}
            <div class="card shadow mb-4">
                <div class="card-header bg-white">
                    <h5 class="mb-0"><i class="fas fa-list-ol"></i> Detalle por pregunta</h5>
                </div>
                <div class="card-body">
                    {% for item in preguntas_con_respuestas %}
                        <div class="border rounded p-3 mb-3 {% if item.es_correcta %}border-success{% else %}border-danger{% endif %}">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h6 class="mb-0">
                                    <span class="badge {% if item.es_correcta %}bg-success{% else %}bg-danger{% endif %}">
                                        {% if item.es_correcta %}Correcta{% else %}Incorrecta{% endif %}
                                    </span>
                                    Pregunta {{ forloop.counter }}
                                </h6>
                                <small class="text-muted">{{ item.pregunta.puntaje }} pts</small>
                            </div>
                            <p class="mb-2">{{ item.pregunta.enunciado }}</p>

                            <div class="row small">
                                <div class="col-md-6">
                                    <strong>Tu respuesta:</strong>
                                    <code class="{% if item.es_correcta %}text-success{% else %}text-danger{% endif %}">
                                        {{ item.respuesta_usuario|default:"(sin responder)" }}
                                    </code>
                                </div>
                                {% if not item.es_correcta %}
                                <div class="col-md-6">
                                    <strong>Respuesta correcta:</strong>
                                    <code class="text-success">{{ item.pregunta.respuesta_correcta }}</code>
                                </div>
                                {% endif %}
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <!-- Botones de accion -->
            <div class="text-center mb-4">
                <a href="{% url 'ver_evaluacion' evaluacion.id %}" class="btn btn-outline-primary btn-lg">
                    <i class="fas fa-redo"></i> Reintentar evaluacion
                </a>
                <a href="{% url 'detalle_curso' curso.slug %}" class="btn btn-outline-secondary btn-lg">
                    <i class="fas fa-arrow-left"></i> Volver al curso
                </a>
            </div>

        </div>
    </div>
</div>
{% endblock %}
'''
    TP.write_text(template, encoding="utf-8")
    print("[OK] Template creado: core/templates/core/cursos/resultado_evaluacion.html")


# ============================================================
# 6) Verificacion
# ============================================================
print()
print("=" * 60)
print("VERIFICACION")
print("=" * 60)

c = vp.read_text(encoding="utf-8")
print("  Importa ResultadoEvaluacionCurso:     ", "ResultadoEvaluacionCurso" in c)
print("  Importa timezone:                     ", "from django.utils import timezone" in c)
print("  enviar_evaluacion guarda resultado:   ", "resultado, creado = ResultadoEvaluacionCurso" in c)
print("  enviar_evaluacion redirige a result.: ", "redirect('resultado_evaluacion'" in c)
print("  resultado_evaluacion pasa resultado:  ", "'resultado': resultado" in c)
print("  Template existe:                      ", TP.exists())
if TP.exists():
    print("  Tamano template:                      ", TP.stat().st_size, "bytes")
