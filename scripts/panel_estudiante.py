from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) core/views_estudiante.py
# ============================================================
views = '''"""
Panel del Estudiante: dashboard personal, cursos, evaluaciones,
logros, certificados, estadísticas y ranking.
"""
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q, Sum
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import (
    Logro, LogroObtenido, Certificacion, CertificacionObtenida, Respuesta,
)
from .models_cursos import (
    Curso, Modulo, Leccion, ProgresoUsuario, EvaluacionCurso, PreguntaEvaluacion,
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
'''
(BASE / "core" / "views_estudiante.py").write_text(views, encoding="utf-8")
print("[OK] core/views_estudiante.py")

# ============================================================
# 2) core/urls_estudiante.py
# ============================================================
urls = '''# -*- coding: utf-8 -*-
"""URLs del panel del estudiante."""
from django.urls import path
from . import views_estudiante as est

app_name = "estudiante"

urlpatterns = [
    path('', est.dashboard, name='dashboard'),
    path('cursos/', est.mis_cursos, name='cursos'),
    path('evaluaciones/', est.mis_evaluaciones, name='evaluaciones'),
    path('logros/', est.mis_logros, name='logros'),
    path('certificados/', est.mis_certificados, name='certificados'),
    path('estadisticas/', est.mis_estadisticas, name='estadisticas'),
    path('ranking/', est.mi_ranking, name='ranking'),
    path('certificados/<int:certificado_id>/pdf/', est.descargar_certificado_pdf, name='certificado_pdf'),
    path('certificados/<int:certificado_id>/docx/', est.descargar_certificado_docx, name='certificado_docx'),
]
'''
(BASE / "core" / "urls_estudiante.py").write_text(urls, encoding="utf-8")
print("[OK] core/urls_estudiante.py")

# ============================================================
# 3) Templates
# ============================================================
TPL = BASE / "core" / "templates" / "core" / "estudiante"
TPL.mkdir(parents=True, exist_ok=True)

# base.html
base = '''{% extends 'base.html' %}
{% load i18n %}
{% block content %}
<div class="container-fluid mt-4">
  <div class="row">
    <aside class="col-md-2">
      <div class="list-group shadow-sm">
        <a class="list-group-item list-group-item-action {% if request.path == '/estudiante/' or 'estudiante/estadisticas' not in request.path and 'estudiante/cursos' not in request.path and 'estudiante/evaluaciones' not in request.path and 'estudiante/logros' not in request.path and 'estudiante/certificados' not in request.path and 'estudiante/ranking' not in request.path %}active{% endif %}"
           href="{% url 'estudiante:dashboard' %}">
          <i class="fas fa-home"></i> Inicio
        </a>
        <a class="list-group-item list-group-item-action {% if 'estudiante/cursos' in request.path %}active{% endif %}"
           href="{% url 'estudiante:cursos' %}">
          <i class="fas fa-book"></i> Mis Cursos
        </a>
        <a class="list-group-item list-group-item-action {% if 'estudiante/evaluaciones' in request.path %}active{% endif %}"
           href="{% url 'estudiante:evaluaciones' %}">
          <i class="fas fa-clipboard-check"></i> Evaluaciones
        </a>
        <a class="list-group-item list-group-item-action {% if 'estudiante/logros' in request.path %}active{% endif %}"
           href="{% url 'estudiante:logros' %}">
          <i class="fas fa-trophy"></i> Logros
        </a>
        <a class="list-group-item list-group-item-action {% if 'estudiante/certificados' in request.path %}active{% endif %}"
           href="{% url 'estudiante:certificados' %}">
          <i class="fas fa-certificate"></i> Certificados
        </a>
        <a class="list-group-item list-group-item-action {% if 'estudiante/estadisticas' in request.path %}active{% endif %}"
           href="{% url 'estudiante:estadisticas' %}">
          <i class="fas fa-chart-line"></i> Estadísticas
        </a>
        <a class="list-group-item list-group-item-action {% if 'estudiante/ranking' in request.path %}active{% endif %}"
           href="{% url 'estudiante:ranking' %}">
          <i class="fas fa-medal"></i> Ranking
        </a>
      </div>
    </aside>
    <main class="col-md-10">
      {% if messages %}
        {% for m in messages %}
          <div class="alert alert-{{ m.tags|default:'info' }} alert-dismissible fade show">
            {{ m }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
          </div>
        {% endfor %}
      {% endif %}
      {% block panel %}{% endblock %}
    </main>
  </div>
</div>
{% endblock %}
'''
(TPL / "base.html").write_text(base, encoding="utf-8")
print("[OK] estudiante/base.html")

# dashboard.html
dash = '''{% extends 'core/estudiante/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-home"></i> Hola, {{ user.username }} 👋</h2>

<!-- KPIs -->
<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-primary text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.cursos_activos }}</div>
        <div><i class="fas fa-book"></i> Cursos activos</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-success text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.lecciones }}</div>
        <div><i class="fas fa-check-circle"></i> Lecciones completadas</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-warning text-dark">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.logros }}</div>
        <div><i class="fas fa-trophy"></i> Logros</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-info text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.certificados }}</div>
        <div><i class="fas fa-certificate"></i> Certificados</div>
      </div>
    </div>
  </div>
</div>

<!-- KPIs secundarios -->
<div class="row g-3 mb-4">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-body text-center">
        <h6 class="text-muted mb-2">Tasa de aciertos global</h6>
        <div class="fs-1 fw-bold
          {% if kpis.tasa >= 80 %}text-success{% elif kpis.tasa >= 50 %}text-warning{% else %}text-danger{% endif %}">
          {{ kpis.tasa }}%
        </div>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-body text-center">
        <h6 class="text-muted mb-2">Certificados obtenidos</h6>
        <div class="fs-1 fw-bold text-primary">{{ kpis.certificados }}</div>
      </div>
    </div>
  </div>
</div>

<!-- Gráficos -->
<div class="row g-3 mb-4">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold"><i class="fas fa-chart-bar"></i> Progreso por curso</div>
      <div class="card-body">
        <canvas id="chartCursos" height="140"></canvas>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold"><i class="fas fa-chart-line"></i> Actividad últimos 30 días</div>
      <div class="card-body">
        <canvas id="chartActividad" height="140"></canvas>
      </div>
    </div>
  </div>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-6">
    <div class="card shadow-sm h-100">
      <div class="card-header bg-white fw-bold"><i class="fas fa-award"></i> Últimos logros</div>
      <ul class="list-group list-group-flush">
        {% for l in ultimos_logros %}
          <li class="list-group-item">
            <span class="fs-5">{{ l.logro.icono }}</span>
            <strong class="ms-2">{{ l.logro.nombre }}</strong>
            <small class="text-muted d-block">{{ l.fecha_obtenida|date:"SHORT_DATE_FORMAT" }}</small>
          </li>
        {% empty %}
          <li class="list-group-item text-muted">Sin logros todavía</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm h-100">
      <div class="card-header bg-white fw-bold"><i class="fas fa-lightbulb"></i> Próximas lecciones sugeridas</div>
      <ul class="list-group list-group-flush">
        {% for l in proximas %}
          <li class="list-group-item d-flex justify-content-between">
            <div>
              <strong>{{ l.titulo|truncatechars:45 }}</strong><br>
              <small class="text-muted">{{ l.modulo.curso.titulo }}</small>
            </div>
            <a href="{% url 'ver_leccion' l.modulo.curso.slug l.modulo.id l.id %}"
               class="btn btn-sm btn-outline-primary">
              <i class="fas fa-play"></i>
            </a>
          </li>
        {% empty %}
          <li class="list-group-item text-muted">¡Felicidades, sin lecciones pendientes!</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
const cLabels = [{% for c in cursos_progreso %}"{{ c.curso.titulo|escapejs }}"{% if not forloop.last %},{% endif %}{% endfor %}];
const cData = [{% for c in cursos_progreso %}{{ c.pct }}{% if not forloop.last %},{% endif %}{% endfor %}];
const aLabels = [{% for a in actividad %}"{{ a.dia }}"{% if not forloop.last %},{% endif %}{% endfor %}];
const aData = [{% for a in actividad %}{{ a.count }}{% if not forloop.last %},{% endif %}{% endfor %}];

new Chart(document.getElementById('chartCursos'), {
  type: 'bar',
  data: {
    labels: cLabels,
    datasets: [{
      label: '% completado',
      data: cData,
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    }]
  },
  options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100 } } }
});

new Chart(document.getElementById('chartActividad'), {
  type: 'line',
  data: {
    labels: aLabels,
    datasets: [{
      label: 'Lecciones',
      data: aData,
      borderColor: 'rgba(54, 162, 235, 1)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      tension: 0.3,
      fill: true,
    }]
  },
  options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
});
</script>
{% endblock %}
'''
(TPL / "dashboard.html").write_text(dash, encoding="utf-8")
print("[OK] estudiante/dashboard.html")

# mis_cursos.html
mis_cursos = '''{% extends 'core/estudiante/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-book"></i> Mis Cursos</h2>

<div class="row g-3">
  {% for c in cursos_data %}
  <div class="col-md-6 col-lg-4">
    <div class="card shadow-sm h-100">
      <div class="card-body">
        <div class="d-flex justify-content-between mb-2">
          <span class="badge bg-info text-dark">{{ c.curso.nivel|capfirst }}</span>
          <span class="badge bg-secondary">{{ c.curso.duracion_estimada }}h</span>
        </div>
        <h5 class="card-title">{{ c.curso.titulo }}</h5>
        <p class="text-muted small">{{ c.curso.descripcion|truncatechars:110 }}</p>
        <div class="d-flex justify-content-between small text-muted mb-2">
          <span><i class="fas fa-layer-group"></i> {{ c.modulos }} módulos</span>
          <span><i class="fas fa-file-alt"></i> {{ c.total }} lecciones</span>
        </div>
        <div class="progress mb-2" style="height:22px;">
          <div class="progress-bar bg-success" style="width:{{ c.pct }}%;">
            {% if c.pct > 10 %}{{ c.pct }}%{% endif %}
          </div>
        </div>
        <div class="d-flex justify-content-between">
          <small class="text-muted">{{ c.completadas }}/{{ c.total }} completadas</small>
          <a href="{% url 'detalle_curso' c.curso.slug %}" class="btn btn-sm btn-primary">
            {% if c.pct > 0 and c.pct < 100 %}Continuar{% elif c.pct == 100 %}Repasar{% else %}Comenzar{% endif %}
          </a>
        </div>
      </div>
    </div>
  </div>
  {% empty %}
  <div class="col-12 text-center text-muted py-5">
    <i class="fas fa-inbox fa-3x mb-3"></i>
    <p>No hay cursos disponibles.</p>
  </div>
  {% endfor %}
</div>
{% endblock %}
'''
(TPL / "mis_cursos.html").write_text(mis_cursos, encoding="utf-8")
print("[OK] estudiante/mis_cursos.html")

# mis_evaluaciones.html
mis_eval = '''{% extends 'core/estudiante/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-clipboard-check"></i> Mis Evaluaciones</h2>

<div class="row g-3 mb-4">
  <div class="col-md-4">
    <div class="card shadow-sm border-0 bg-warning text-dark">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ pendientes|length }}</div>
        <div>Pendientes</div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card shadow-sm border-0 bg-success text-white">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ completadas|length }}</div>
        <div>Completadas</div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card shadow-sm border-0 bg-primary text-white">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ total }}</div>
        <div>Total disponibles</div>
      </div>
    </div>
  </div>
</div>

<h4><i class="fas fa-hourglass-half"></i> Pendientes ({{ pendientes|length }})</h4>
<div class="row g-3 mb-4">
  {% for p in pendientes %}
  <div class="col-md-6">
    <div class="card shadow-sm border-warning">
      <div class="card-body">
        <span class="badge bg-secondary">{{ p.ev.get_tipo_display|default:p.ev.tipo }}</span>
        <h6 class="mt-2">{{ p.ev.titulo }}</h6>
        <small class="text-muted d-block mb-2">{{ p.ev.curso.titulo }}</small>
        <div class="d-flex justify-content-between align-items-center">
          <div class="small text-muted">
            <i class="fas fa-clock"></i> {{ p.ev.tiempo_limite }} min |
            <i class="fas fa-star"></i> {{ p.ev.puntaje_maximo }} pts
          </div>
          <a href="{% url 'ver_evaluacion' p.ev.id %}" class="btn btn-sm btn-warning">
            <i class="fas fa-play"></i> Empezar
          </a>
        </div>
      </div>
    </div>
  </div>
  {% empty %}
  <div class="col-12 text-muted">¡No tienes evaluaciones pendientes! 🎉</div>
  {% endfor %}
</div>

<h4><i class="fas fa-check-circle text-success"></i> Completadas ({{ completadas|length }})</h4>
<div class="table-responsive">
  <table class="table table-hover">
    <thead class="table-light">
      <tr>
        <th>Evaluación</th>
        <th>Curso</th>
        <th>Intentos</th>
        <th>Mejor puntaje</th>
        <th>Último intento</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {% for c in completadas %}
      <tr>
        <td><strong>{{ c.ev.titulo }}</strong></td>
        <td>{{ c.ev.curso.titulo }}</td>
        <td><span class="badge bg-info text-dark">{{ c.intentos }}</span></td>
        <td>
          <span class="badge {% if c.mejor >= 80 %}bg-success{% elif c.mejor >= 50 %}bg-warning text-dark{% else %}bg-danger{% endif %}">
            {{ c.mejor }}/{{ c.max }}
          </span>
        </td>
        <td>{{ c.ultimo|date:"SHORT_DATETIME_FORMAT" }}</td>
        <td>
          <a href="{% url 'ver_evaluacion' c.ev.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-redo"></i>
          </a>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="6" class="text-center text-muted">Sin evaluaciones completadas</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
'''
(TPL / "mis_evaluaciones.html").write_text(mis_eval, encoding="utf-8")
print("[OK] estudiante/mis_evaluaciones.html")

# mis_logros.html
mis_logros = '''{% extends 'core/estudiante/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-trophy"></i> Mis Logros</h2>

<div class="row g-3 mb-4">
  <div class="col-md-6">
    <div class="card shadow-sm border-0 bg-warning text-dark">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ total_obtenidos }} / {{ total_logros }}</div>
        <div>Logros desbloqueados</div>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm border-0 bg-secondary text-white">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ por_obtener|length }}</div>
        <div>Por desbloquear</div>
      </div>
    </div>
  </div>
</div>

<h4><i class="fas fa-check-circle text-success"></i> Obtenidos ({{ total_obtenidos }})</h4>
<div class="row g-3 mb-4">
  {% for l in obtenidos %}
  <div class="col-md-3">
    <div class="card shadow-sm text-center h-100 border-warning">
      <div class="card-body">
        <div class="fs-1">{{ l.logro.icono }}</div>
        <strong>{{ l.logro.nombre }}</strong>
        <p class="small text-muted mb-1">{{ l.logro.descripcion|truncatechars:60 }}</p>
        <small class="text-muted">{{ l.fecha_obtenida|date:"SHORT_DATE_FORMAT" }}</small>
      </div>
    </div>
  </div>
  {% empty %}
  <div class="col-12 text-muted">Aún no tienes logros. ¡Sigue avanzando!</div>
  {% endfor %}
</div>

<h4><i class="fas fa-lock text-secondary"></i> Por desbloquear ({{ por_obtener|length }})</h4>
<div class="row g-3">
  {% for l in por_obtener %}
  <div class="col-md-3">
    <div class="card shadow-sm text-center h-100 border-secondary opacity-75">
      <div class="card-body">
        <div class="fs-1 grayscale" style="filter:grayscale(1); opacity:0.5;">{{ l.icono|default:"🔒" }}</div>
        <strong>{{ l.nombre }}</strong>
        <p class="small text-muted mb-1">{{ l.descripcion|truncatechars:60 }}</p>
        {% if l.puntos_requeridos %}
        <small class="text-muted">{{ l.puntos_requeridos }} pts</small>
        {% endif %}
      </div>
    </div>
  </div>
  {% empty %}
  <div class="col-12 text-muted">¡Felicidades, has desbloqueado todos los logros!</div>
  {% endfor %}
</div>
{% endblock %}
'''
(TPL / "mis_logros.html").write_text(mis_logros, encoding="utf-8")
print("[OK] estudiante/mis_logros.html")

# mis_certificados.html
mis_certs = '''{% extends 'core/estudiante/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-certificate"></i> Mis Certificados</h2>

<h4><i class="fas fa-award text-success"></i> Obtenidos ({{ total }})</h4>
<div class="row g-3 mb-4">
  {% for c in obtenidos %}
  <div class="col-md-6">
    <div class="card shadow-sm border-success h-100">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-start">
          <div>
            <span class="badge bg-info text-dark mb-2">{{ c.certificacion.nivel|capfirst }}</span>
            <h5 class="mb-1">{{ c.certificacion.nombre }}</h5>
            <small class="text-muted">{{ c.certificacion.descripcion|truncatechars:100 }}</small>
          </div>
          <i class="fas fa-certificate fa-2x text-success"></i>
        </div>
        <hr>
        <div class="small text-muted">
          <div><strong>Código:</strong> {{ c.codigo_verificacion }}</div>
          <div><strong>Emitido:</strong> {{ c.fecha_obtenida|date:"d/m/Y" }}</div>
        </div>
        <div class="btn-group btn-group-sm mt-3 w-100">
          <a href="{% url 'estudiante:certificado_pdf' c.id %}" class="btn btn-outline-danger" target="_blank">
            <i class="fas fa-file-pdf"></i> PDF
          </a>
          <a href="{% url 'estudiante:certificado_docx' c.id %}" class="btn btn-outline-primary">
            <i class="fas fa-file-word"></i> Word
          </a>
          <a href="/verificar/{{ c.codigo_verificacion }}/" class="btn btn-outline-info" target="_blank">
            <i class="fas fa-external-link-alt"></i> Verificar
          </a>
        </div>
      </div>
    </div>
  </div>
  {% empty %}
  <div class="col-12 text-muted">Aún no tienes certificados. ¡Sigue completando cursos!</div>
  {% endfor %}
</div>

<h4 class="mt-4"><i class="fas fa-bullseye text-muted"></i> Disponibles por obtener ({{ disponibles|length }})</h4>
<div class="row g-3">
  {% for c in disponibles %}
  <div class="col-md-6">
    <div class="card shadow-sm border-secondary opacity-75 h-100">
      <div class="card-body">
        <span class="badge bg-info text-dark">{{ c.nivel|capfirst }}</span>
        <h5 class="mt-2">{{ c.nombre }}</h5>
        <p class="small text-muted mb-0">{{ c.descripcion|truncatechars:110 }}</p>
      </div>
    </div>
  </div>
  {% empty %}
  <div class="col-12 text-muted">¡Ya tienes todas las certificaciones disponibles!</div>
  {% endfor %}
</div>
{% endblock %}
'''
(TPL / "mis_certificados.html").write_text(mis_certs, encoding="utf-8")
print("[OK] estudiante/mis_certificados.html")

# mis_estadisticas.html
mis_est = '''{% extends 'core/estudiante/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-chart-line"></i> Mis Estadísticas</h2>

<div class="row g-3 mb-4">
  <div class="col-md-4">
    <div class="card shadow-sm border-0 bg-primary text-white">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ total_resp }}</div>
        <div>Respuestas</div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card shadow-sm border-0 bg-success text-white">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ correctas }}</div>
        <div>Correctas</div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card shadow-sm border-0 bg-warning text-dark">
      <div class="card-body text-center">
        <div class="fs-2 fw-bold">{{ tasa }}%</div>
        <div>Tasa de aciertos</div>
      </div>
    </div>
  </div>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold"><i class="fas fa-chart-bar"></i> Promedio por curso</div>
      <div class="card-body"><canvas id="chartProm" height="150"></canvas></div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold"><i class="fas fa-chart-line"></i> Actividad (30 días)</div>
      <div class="card-body"><canvas id="chartAct" height="150"></canvas></div>
    </div>
  </div>
</div>

<div class="card shadow-sm mb-4">
  <div class="card-header bg-white fw-bold"><i class="fas fa-list"></i> Aciertos por tipo de ejercicio</div>
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead class="table-light">
        <tr><th>Tipo</th><th>Total</th><th>Correctas</th><th>Tasa</th></tr>
      </thead>
      <tbody>
        {% for t in tipos_data %}
        <tr>
          <td><strong>{{ t.tipo }}</strong></td>
          <td>{{ t.total }}</td>
          <td><span class="badge bg-success">{{ t.correctas }}</span></td>
          <td>
            <div class="progress" style="height:20px;min-width:120px;">
              <div class="progress-bar {% if t.tasa >= 80 %}bg-success{% elif t.tasa >= 50 %}bg-warning{% else %}bg-danger{% endif %}"
                   style="width:{{ t.tasa }}%;">{{ t.tasa }}%</div>
            </div>
          </td>
        </tr>
        {% empty %}
        <tr><td colspan="4" class="text-center text-muted">Sin datos</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
const pLabels = [{% for c in cursos_stats %}"{{ c.curso.titulo|escapejs }}"{% if not forloop.last %},{% endif %}{% endfor %}];
const pData = [{% for c in cursos_stats %}{{ c.promedio }}{% if not forloop.last %},{% endif %}{% endfor %}];
const aLabels = [{% for a in actividad %}"{{ a.dia }}"{% if not forloop.last %},{% endif %}{% endfor %}];
const aData = [{% for a in actividad %}{{ a.count }}{% if not forloop.last %},{% endif %}{% endfor %}];

new Chart(document.getElementById('chartProm'), {
  type: 'bar',
  data: { labels: pLabels, datasets: [{ label: 'Promedio', data: pData,
    backgroundColor: 'rgba(255, 159, 64, 0.6)', borderColor: 'rgba(255, 159, 64, 1)', borderWidth: 1 }] },
  options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100 } } }
});

new Chart(document.getElementById('chartAct'), {
  type: 'line',
  data: { labels: aLabels, datasets: [{ label: 'Lecciones', data: aData,
    borderColor: 'rgba(75, 192, 192, 1)', backgroundColor: 'rgba(75, 192, 192, 0.2)', tension: 0.3, fill: true }] },
  options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
});
</script>
{% endblock %}
'''
(TPL / "mis_estadisticas.html").write_text(mis_est, encoding="utf-8")
print("[OK] estudiante/mis_estadisticas.html")

# mi_ranking.html
mi_rank = '''{% extends 'core/estudiante/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-medal"></i> Mi Ranking</h2>

{% if mi_fila %}
<div class="card shadow-sm border-primary mb-4">
  <div class="card-body text-center">
    <h5 class="text-muted mb-2">Tu posición actual</h5>
    <div class="display-3 fw-bold text-primary">#{{ mi_posicion }}</div>
    <p class="text-muted">de {{ total_estudiantes }} estudiantes</p>
    <div class="row mt-3">
      <div class="col-6">
        <div class="fs-4 fw-bold text-success">{{ mi_fila.progresos }}</div>
        <small class="text-muted">Lecciones completadas</small>
      </div>
      <div class="col-6">
        <div class="fs-4 fw-bold text-info">{{ mi_fila.correctas }}</div>
        <small class="text-muted">Respuestas correctas</small>
      </div>
    </div>
  </div>
</div>
{% endif %}

<h4 class="mb-3"><i class="fas fa-trophy text-warning"></i> Top 10</h4>
<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-light">
      <tr><th>#</th><th>Estudiante</th><th class="text-center">Lecciones</th><th class="text-center">Correctas</th></tr>
    </thead>
    <tbody>
      {% for r in top10 %}
      <tr {% if r.user.id == user.id %}class="table-primary"{% endif %}>
        <td>
          {% if r.pos == 1 %}🥇{% elif r.pos == 2 %}🥈{% elif r.pos == 3 %}🥉{% else %}<strong>{{ r.pos }}</strong>{% endif %}
        </td>
        <td><strong>{{ r.user.username }}</strong>{% if r.user.id == user.id %} <span class="badge bg-primary">Tú</span>{% endif %}</td>
        <td class="text-center"><span class="badge bg-primary">{{ r.progresos }}</span></td>
        <td class="text-center"><span class="badge bg-success">{{ r.correctas }}</span></td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
'''
(TPL / "mi_ranking.html").write_text(mi_rank, encoding="utf-8")
print("[OK] estudiante/mi_ranking.html")

# ============================================================
# 4) Añadir include en django_retorica/urls.py
# ============================================================
udr = BASE / "django_retorica" / "urls.py"
c = udr.read_text(encoding="utf-8")

if "core.urls_estudiante" not in c:
    import re
    patron = re.compile(r"(urlpatterns \+= i18n_patterns\(\r?\n)")
    reemplazo = r"\1    path('estudiante/', include('core.urls_estudiante')),\n"
    c2 = patron.sub(reemplazo, c, count=1)
    if c2 != c:
        udr.write_text(c2, encoding="utf-8")
        print("[OK] path('estudiante/', include(...)) añadido")
    else:
        print("[!] No se pudo insertar el include de estudiante")
else:
    print("[SKIP] include ya estaba")

# ============================================================
# 5) Actualizar navbar: link "Estudiante" → /estudiante/
# ============================================================
base_tpl = BASE / "core" / "templates" / "core" / "base.html"
c = base_tpl.read_text(encoding="utf-8")

# Reemplazar el bloque {% else %} del navbar (que apunta al viejo dashboard_estudiante)
viejo = '''{% else %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'core:dashboard_estudiante' %}">
                                    <i class="fas fa-user-graduate"></i> Estudiante
                                </a>
                            </li>
                        {% endif %}'''

nuevo = '''{% else %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'estudiante:dashboard' %}" style="font-weight:700;">
                                    <i class="fas fa-user-graduate"></i> Mi Panel
                                </a>
                            </li>
                        {% endif %}'''

if viejo in c:
    c = c.replace(viejo, nuevo)
    base_tpl.write_text(c, encoding="utf-8")
    print("[OK] navbar actualizado: link Estudiante → Mi Panel")
elif "estudiante:dashboard" in c:
    print("[SKIP] navbar ya apuntaba al panel del estudiante")
else:
    print("[!] No se encontró el bloque del navbar. Pégame estas líneas para arreglarlo.")
