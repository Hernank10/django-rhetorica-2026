# -*- coding: utf-8 -*-
"""Panel del profesor — vistas + templates."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) core/views_profesor.py
# ============================================================
views = '''"""
Panel del profesor: estudiantes, evaluaciones, certificaciones, CRUD cursos y lecciones.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import (
    Logro, LogroObtenido, Certificacion, CertificacionObtenida, Respuesta,
)
from .models_cursos import (
    Curso, Modulo, Leccion, ProgresoUsuario, EvaluacionCurso, PreguntaEvaluacion,
)

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
    estudiante = get_object_or_404(User, id=estudiante_id)
    progresos = ProgresoUsuario.objects.filter(
        usuario=estudiante, completado=True
    ).select_related("leccion__modulo__curso")
    certificados = CertificacionObtenida.objects.filter(
        user=estudiante
    ).select_related("certificacion")
    logros = LogroObtenido.objects.filter(user=estudiante).select_related("logro")
    respuestas = Respuesta.objects.filter(user=estudiante).order_by("-fecha")[:20]
    context = {
        "estudiante": estudiante,
        "progresos": progresos,
        "total_progresos": progresos.count(),
        "certificados": certificados,
        "logros": logros,
        "respuestas": respuestas,
    }
    return render(request, "core/profesor/estudiantes/detalle.html", context)


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
        contenido = request.POST.get("contenido", "")
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
'''

(BASE / "core" / "views_profesor.py").write_text(views, encoding="utf-8")
print("[OK] core/views_profesor.py")

# ============================================================
# 2) TEMPLATES
# ============================================================
TPL_ROOT = BASE / "core" / "templates" / "core" / "profesor"
for sub in ["estudiantes", "evaluaciones", "certificaciones", "cursos", "lecciones"]:
    (TPL_ROOT / sub).mkdir(parents=True, exist_ok=True)

# --- base.html ---
base = '''{% extends 'base.html' %}
{% load i18n %}
{% block content %}
<div class="container-fluid mt-4">
  <div class="row">
    <aside class="col-md-2">
      <div class="list-group shadow-sm">
        <a class="list-group-item list-group-item-action {% if 'dashboard' in request.path %}active{% endif %}"
           href="{% url 'profesor:dashboard' %}">
          <i class="fas fa-tachometer-alt"></i> Dashboard
        </a>
        <a class="list-group-item list-group-item-action {% if '/estudiantes/' in request.path %}active{% endif %}"
           href="{% url 'profesor:estudiantes' %}">
          <i class="fas fa-users"></i> Estudiantes
        </a>
        <a class="list-group-item list-group-item-action {% if '/cursos/' in request.path %}active{% endif %}"
           href="{% url 'profesor:cursos_lista' %}">
          <i class="fas fa-book"></i> Cursos
        </a>
        <a class="list-group-item list-group-item-action {% if '/lecciones/' in request.path %}active{% endif %}"
           href="{% url 'profesor:lecciones_lista' %}">
          <i class="fas fa-file-alt"></i> Lecciones
        </a>
        <a class="list-group-item list-group-item-action {% if '/evaluaciones/' in request.path %}active{% endif %}"
           href="{% url 'profesor:evaluaciones' %}">
          <i class="fas fa-clipboard-check"></i> Evaluaciones
        </a>
        <a class="list-group-item list-group-item-action {% if '/certificaciones/' in request.path %}active{% endif %}"
           href="{% url 'profesor:certificaciones' %}">
          <i class="fas fa-certificate"></i> Certificaciones
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
(TPL_ROOT / "base.html").write_text(base, encoding="utf-8")
print("[OK] profesor/base.html")

# --- dashboard.html ---
dash = '''{% extends 'core/profesor/base.html' %}
{% load i18n %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-tachometer-alt"></i> Panel del Profesor</h2>

<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-primary text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.estudiantes }}</div>
        <div><i class="fas fa-users"></i> Estudiantes</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-success text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.cursos }}</div>
        <div><i class="fas fa-book"></i> Cursos</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-info text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.lecciones }}</div>
        <div><i class="fas fa-file-alt"></i> Lecciones</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-warning text-dark">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.evaluaciones }}</div>
        <div><i class="fas fa-clipboard-check"></i> Evaluaciones</div>
      </div>
    </div>
  </div>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-body">
        <h6 class="text-muted">Certificados emitidos</h6>
        <div class="fs-3 fw-bold text-success">{{ kpis.certificados }}</div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-body">
        <h6 class="text-muted">Lecciones completadas</h6>
        <div class="fs-3 fw-bold text-primary">{{ kpis.progresos }}</div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-body">
        <h6 class="text-muted">Tasa de aciertos</h6>
        <div class="fs-3 fw-bold text-info">{{ kpis.tasa_aciertos }}%</div>
      </div>
    </div>
  </div>
</div>

<div class="row g-3">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold">Últimos estudiantes</div>
      <ul class="list-group list-group-flush">
        {% for e in ultimos_estudiantes %}
        <li class="list-group-item d-flex justify-content-between">
          <span><i class="fas fa-user"></i> {{ e.username }}</span>
          <a href="{% url 'profesor:estudiante_detalle' e.id %}" class="btn btn-sm btn-outline-primary">Ver</a>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin estudiantes</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold">Cursos más populares</div>
      <ul class="list-group list-group-flush">
        {% for c in cursos_top %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ c.titulo }}</span>
          <span class="badge bg-primary">{{ c.estudiantes_inscritos }} inscritos</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin cursos</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>
{% endblock %}
'''
(TPL_ROOT / "dashboard.html").write_text(dash, encoding="utf-8")
print("[OK] profesor/dashboard.html")

# --- estudiantes/lista.html ---
est_lista = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-users"></i> Estudiantes ({{ total }})</h2>

<form method="get" class="mb-3">
  <div class="input-group">
    <input type="text" name="q" value="{{ q }}" class="form-control" placeholder="Buscar por nombre, usuario o email...">
    <button class="btn btn-primary"><i class="fas fa-search"></i> Buscar</button>
  </div>
</form>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Usuario</th>
        <th>Nombre</th>
        <th>Email</th>
        <th>Lecciones</th>
        <th>Logros</th>
        <th>Certificados</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {% for row in estudiantes_data %}
      <tr>
        <td><strong>{{ row.user.username }}</strong></td>
        <td>{{ row.user.get_full_name|default:"—" }}</td>
        <td>{{ row.user.email|default:"—" }}</td>
        <td><span class="badge bg-primary">{{ row.progresos }}</span></td>
        <td><span class="badge bg-warning text-dark">{{ row.logros }}</span></td>
        <td><span class="badge bg-success">{{ row.certificados }}</span></td>
        <td>
          <a href="{% url 'profesor:estudiante_detalle' row.user.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-eye"></i>
          </a>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="7" class="text-center text-muted">Sin estudiantes</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
'''
(TPL_ROOT / "estudiantes" / "lista.html").write_text(est_lista, encoding="utf-8")
print("[OK] profesor/estudiantes/lista.html")

# --- estudiantes/detalle.html ---
est_det = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:estudiantes' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>
<h2 class="mb-3"><i class="fas fa-user"></i> {{ estudiante.username }}</h2>

<div class="row g-3 mb-4">
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-body">
        <h6 class="text-muted">Nombre</h6>
        <div>{{ estudiante.get_full_name|default:"—" }}</div>
        <h6 class="text-muted mt-3">Email</h6>
        <div>{{ estudiante.email|default:"—" }}</div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-body text-center">
        <h6 class="text-muted">Lecciones completadas</h6>
        <div class="fs-2 fw-bold text-primary">{{ total_progresos }}</div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card shadow-sm">
      <div class="card-body text-center">
        <h6 class="text-muted">Logros / Certificados</h6>
        <div class="fs-3">
          <span class="badge bg-warning text-dark">{{ logros.count }}</span>
          <span class="badge bg-success">{{ certificados.count }}</span>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="row g-3">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header fw-bold">Lecciones completadas</div>
      <ul class="list-group list-group-flush" style="max-height:300px;overflow:auto;">
        {% for p in progresos %}
        <li class="list-group-item">
          <strong>{{ p.leccion.titulo }}</strong><br>
          <small class="text-muted">{{ p.leccion.modulo.curso.titulo }} · {{ p.puntaje_obtenido }} pts</small>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin progreso</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm mb-3">
      <div class="card-header fw-bold">Logros</div>
      <ul class="list-group list-group-flush">
        {% for l in logros %}
        <li class="list-group-item">{{ l.logro.icono }} {{ l.logro.nombre }}</li>
        {% empty %}
        <li class="list-group-item text-muted">Sin logros</li>
        {% endfor %}
      </ul>
    </div>
    <div class="card shadow-sm">
      <div class="card-header fw-bold">Certificados</div>
      <ul class="list-group list-group-flush">
        {% for c in certificados %}
        <li class="list-group-item">{{ c.certificacion.nombre }} <small class="text-muted">{{ c.fecha_obtenida|date:"SHORT_DATE_FORMAT" }}</small></li>
        {% empty %}
        <li class="list-group-item text-muted">Sin certificados</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>
{% endblock %}
'''
(TPL_ROOT / "estudiantes" / "detalle.html").write_text(est_det, encoding="utf-8")
print("[OK] profesor/estudiantes/detalle.html")

# --- evaluaciones/lista.html ---
eval_lista = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-clipboard-check"></i> Evaluaciones ({{ total }})</h2>
<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Curso</th>
        <th>Módulo</th>
        <th>Evaluación</th>
        <th>Tipo</th>
        <th>Preguntas</th>
        <th>Puntaje</th>
      </tr>
    </thead>
    <tbody>
      {% for e in evaluaciones %}
      <tr>
        <td>{{ e.curso.titulo }}</td>
        <td>{{ e.modulo.titulo|default:"—" }}</td>
        <td><strong>{{ e.titulo }}</strong></td>
        <td><span class="badge bg-secondary">{{ e.tipo }}</span></td>
        <td>{{ e.num_preguntas }}</td>
        <td>{{ e.puntaje_maximo }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="6" class="text-center text-muted">Sin evaluaciones</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
'''
(TPL_ROOT / "evaluaciones" / "lista.html").write_text(eval_lista, encoding="utf-8")
print("[OK] profesor/evaluaciones/lista.html")

# --- certificaciones/lista.html ---
cert_lista = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<h2 class="mb-4"><i class="fas fa-certificate"></i> Certificaciones</h2>

<div class="row mb-4">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-success text-white fw-bold">
        Emitidas ({{ total_emitidas }})
      </div>
      <ul class="list-group list-group-flush" style="max-height:500px;overflow:auto;">
        {% for c in emitidas %}
        <li class="list-group-item d-flex justify-content-between">
          <div>
            <strong>{{ c.certificacion.nombre }}</strong><br>
            <small class="text-muted">{{ c.user.username }} · {{ c.codigo_verificacion }}</small>
          </div>
          <span class="badge bg-success">{{ c.fecha_obtenida|date:"SHORT_DATE_FORMAT" }}</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin certificados emitidos</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-primary text-white fw-bold">
        Disponibles ({{ disponibles.count }})
      </div>
      <ul class="list-group list-group-flush">
        {% for c in disponibles %}
        <li class="list-group-item">
          <strong>{{ c.nombre }}</strong><br>
          <small class="text-muted">{{ c.descripcion|default:"" }}</small>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin certificaciones configuradas</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>
{% endblock %}
'''
(TPL_ROOT / "certificaciones" / "lista.html").write_text(cert_lista, encoding="utf-8")
print("[OK] profesor/certificaciones/lista.html")

# --- cursos/lista.html ---
cur_lista = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="mb-0"><i class="fas fa-book"></i> Cursos ({{ total }})</h2>
  <a href="{% url 'profesor:curso_crear' %}" class="btn btn-primary">
    <i class="fas fa-plus"></i> Nuevo curso
  </a>
</div>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Título</th>
        <th>Nivel</th>
        <th>Estado</th>
        <th>Módulos</th>
        <th>Inscritos</th>
        <th class="text-end">Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for c in cursos %}
      <tr>
        <td>
          <strong>{{ c.titulo }}</strong><br>
          <small class="text-muted">{{ c.descripcion|truncatechars:70 }}</small>
        </td>
        <td><span class="badge bg-info text-dark">{{ c.get_nivel_display|default:c.nivel }}</span></td>
        <td>
          {% if c.estado == "publicado" %}
            <span class="badge bg-success">Publicado</span>
          {% else %}
            <span class="badge bg-secondary">{{ c.estado }}</span>
          {% endif %}
        </td>
        <td>{{ c.num_modulos }}</td>
        <td>{{ c.estudiantes_inscritos }}</td>
        <td class="text-end">
          <a href="{% url 'profesor:curso_editar' c.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-edit"></i>
          </a>
          <form method="post" action="{% url 'profesor:curso_eliminar' c.id %}" class="d-inline"
                onsubmit="return confirm('¿Eliminar el curso {{ c.titulo }}?');">
            {% csrf_token %}
            <button class="btn btn-sm btn-outline-danger"><i class="fas fa-trash"></i></button>
          </form>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="6" class="text-center text-muted">Sin cursos</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
'''
(TPL_ROOT / "cursos" / "lista.html").write_text(cur_lista, encoding="utf-8")
print("[OK] profesor/cursos/lista.html")

# --- cursos/form.html ---
cur_form = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:cursos_lista' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>
<h2 class="mb-4">
  {% if curso %}<i class="fas fa-edit"></i> Editar curso{% else %}<i class="fas fa-plus"></i> Nuevo curso{% endif %}
</h2>

<form method="post" class="card shadow-sm">
  {% csrf_token %}
  <div class="card-body">
    <div class="mb-3">
      <label class="form-label">Título *</label>
      <input type="text" name="titulo" class="form-control" required
             value="{{ curso.titulo|default:'' }}">
    </div>
    <div class="mb-3">
      <label class="form-label">Descripción</label>
      <textarea name="descripcion" class="form-control" rows="3">{{ curso.descripcion|default:'' }}</textarea>
    </div>
    <div class="mb-3">
      <label class="form-label">Objetivo</label>
      <textarea name="objetivo" class="form-control" rows="2">{{ curso.objetivo|default:'' }}</textarea>
    </div>
    <div class="row">
      <div class="col-md-4 mb-3">
        <label class="form-label">Nivel</label>
        <select name="nivel" class="form-select">
          {% for val, label in niveles %}
            <option value="{{ val }}" {% if curso.nivel == val %}selected{% endif %}>{{ label }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="col-md-4 mb-3">
        <label class="form-label">Estado</label>
        <select name="estado" class="form-select">
          {% for val, label in estados %}
            <option value="{{ val }}" {% if curso.estado == val %}selected{% endif %}>{{ label }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="col-md-2 mb-3">
        <label class="form-label">Duración (min)</label>
        <input type="number" name="duracion_estimada" class="form-control"
               value="{{ curso.duracion_estimada|default:60 }}">
      </div>
      <div class="col-md-2 mb-3">
        <label class="form-label">Puntos totales</label>
        <input type="number" name="puntos_totales" class="form-control"
               value="{{ curso.puntos_totales|default:100 }}">
      </div>
    </div>
  </div>
  <div class="card-footer text-end bg-white">
    <a href="{% url 'profesor:cursos_lista' %}" class="btn btn-secondary">Cancelar</a>
    <button class="btn btn-primary"><i class="fas fa-save"></i> Guardar</button>
  </div>
</form>
{% endblock %}
'''
(TPL_ROOT / "cursos" / "form.html").write_text(cur_form, encoding="utf-8")
print("[OK] profesor/cursos/form.html")

# --- lecciones/lista.html ---
lec_lista = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="mb-0"><i class="fas fa-file-alt"></i> Lecciones</h2>
  <a href="{% url 'profesor:leccion_crear' %}" class="btn btn-primary">
    <i class="fas fa-plus"></i> Nueva lección
  </a>
</div>

<form method="get" class="row g-2 mb-3">
  <div class="col-md-4">
    <select name="curso" class="form-select" onchange="this.form.submit()">
      <option value="">— Todos los cursos —</option>
      {% for c in cursos %}
        <option value="{{ c.id }}" {% if curso_sel == c.id|stringformat:"s" %}selected{% endif %}>{{ c.titulo }}</option>
      {% endfor %}
    </select>
  </div>
</form>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Curso</th>
        <th>Módulo</th>
        <th>Título</th>
        <th>Tipo</th>
        <th>Duración</th>
        <th>Puntos</th>
        <th class="text-end">Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for l in lecciones %}
      <tr>
        <td>{{ l.modulo.curso.titulo }}</td>
        <td>{{ l.modulo.titulo }}</td>
        <td><strong>{{ l.titulo }}</strong></td>
        <td><span class="badge bg-secondary">{{ l.tipo }}</span></td>
        <td>{{ l.duracion_estimada }} min</td>
        <td>{{ l.puntos }}</td>
        <td class="text-end">
          <a href="{% url 'profesor:leccion_editar' l.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-edit"></i>
          </a>
          <form method="post" action="{% url 'profesor:leccion_eliminar' l.id %}" class="d-inline"
                onsubmit="return confirm('¿Eliminar la lección?');">
            {% csrf_token %}
            <button class="btn btn-sm btn-outline-danger"><i class="fas fa-trash"></i></button>
          </form>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="7" class="text-center text-muted">Sin lecciones</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
'''
(TPL_ROOT / "lecciones" / "lista.html").write_text(lec_lista, encoding="utf-8")
print("[OK] profesor/lecciones/lista.html")

# --- lecciones/form.html ---
lec_form = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:lecciones_lista' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>
<h2 class="mb-4">
  {% if leccion %}<i class="fas fa-edit"></i> Editar lección{% else %}<i class="fas fa-plus"></i> Nueva lección{% endif %}
</h2>

<form method="post" class="card shadow-sm">
  {% csrf_token %}
  <div class="card-body">
    <div class="mb-3">
      <label class="form-label">Módulo *</label>
      <select name="modulo" class="form-select" required>
        <option value="">— Selecciona un módulo —</option>
        {% for m in modulos %}
          <option value="{{ m.id }}" {% if leccion.modulo_id == m.id %}selected{% endif %}>
            {{ m.curso.titulo }} → {{ m.titulo }}
          </option>
        {% endfor %}
      </select>
    </div>
    <div class="mb-3">
      <label class="form-label">Título *</label>
      <input type="text" name="titulo" class="form-control" required
             value="{{ leccion.titulo|default:'' }}">
    </div>
    <div class="mb-3">
      <label class="form-label">Contenido (HTML permitido)</label>
      <textarea name="contenido" class="form-control" rows="10">{{ leccion.contenido|default:'' }}</textarea>
    </div>
    <div class="row">
      <div class="col-md-3 mb-3">
        <label class="form-label">Tipo</label>
        <select name="tipo" class="form-select">
          {% for val, label in tipos %}
            <option value="{{ val }}" {% if leccion.tipo == val %}selected{% endif %}>{{ label }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="col-md-3 mb-3">
        <label class="form-label">Orden</label>
        <input type="number" name="orden" class="form-control" value="{{ leccion.orden|default:1 }}">
      </div>
      <div class="col-md-3 mb-3">
        <label class="form-label">Duración (min)</label>
        <input type="number" name="duracion_estimada" class="form-control" value="{{ leccion.duracion_estimada|default:15 }}">
      </div>
      <div class="col-md-3 mb-3">
        <label class="form-label">Puntos</label>
        <input type="number" name="puntos" class="form-control" value="{{ leccion.puntos|default:10 }}">
      </div>
    </div>
  </div>
  <div class="card-footer text-end bg-white">
    <a href="{% url 'profesor:lecciones_lista' %}" class="btn btn-secondary">Cancelar</a>
    <button class="btn btn-primary"><i class="fas fa-save"></i> Guardar</button>
  </div>
</form>
{% endblock %}
'''
(TPL_ROOT / "lecciones" / "form.html").write_text(lec_form, encoding="utf-8")
print("[OK] profesor/lecciones/form.html")

print()
print("=" * 60)
print("ARCHIVOS CREADOS:")
print("=" * 60)
for p in sorted(TPL_ROOT.rglob("*.html")):
    print("  ", p.relative_to(BASE))
print()
print("  core/views_profesor.py")
print()
print("[OK] Siguiente paso: actualizar core/urls.py e importar views_profesor")