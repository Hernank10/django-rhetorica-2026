from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Añadir botón "Panel Profesor" en navbar (base.html)
# ============================================================
base = BASE / "core" / "templates" / "core" / "base.html"
c = base.read_text(encoding="utf-8")

if "profesor:dashboard" not in c:
    # Botón a la izquierda del selector de idioma
    boton = '''{% if user.is_authenticated and user.is_staff %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'profesor:dashboard' %}"
                           style="color:#fff;font-weight:600;">
                            <i class="fas fa-chalkboard-teacher"></i> Panel Profesor
                        </a>
                    </li>
                    {% endif %}
'''
    # Insertar antes del selector de idioma
    c2 = c.replace(
        '<li class="nav-item">\n                    <form action="{% url \'set_language\' %}"',
        boton + '                    <li class="nav-item">\n                    <form action="{% url \'set_language\' %}"',
        1,
    )
    if c2 != c:
        base.write_text(c2, encoding="utf-8")
        print("[OK] botón Panel Profesor añadido a base.html")
    else:
        # fallback: buscar por set_language
        import re
        pat = re.compile(r'(\s*<li[^>]*>\s*<form[^>]*set_language[^>]*>)', re.DOTALL)
        c2 = pat.sub(lambda m: '\n' + boton + m.group(1), c, count=1)
        if c2 != c:
            base.write_text(c2, encoding="utf-8")
            print("[OK] botón Panel Profesor añadido (fallback)")
        else:
            print("[!] No se pudo insertar el botón. Añádelo manualmente.")
else:
    print("[SKIP] botón Panel Profesor ya estaba")

# ============================================================
# 2) Añadir toggle_publicar al views_profesor.py
# ============================================================
vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8")

if "def curso_toggle_publicar" not in c:
    nuevas = '''

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
'''
    c = c.rstrip() + "\n" + nuevas
    vp.write_text(c, encoding="utf-8")
    print("[OK] curso_toggle_publicar + detalle_estudiante_completo añadidas")
else:
    print("[SKIP] vistas ya estaban")

# ============================================================
# 3) Actualizar urls_profesor.py
# ============================================================
up = BASE / "core" / "urls_profesor.py"
c = up.read_text(encoding="utf-8")

if "curso_toggle_publicar" not in c:
    nuevas_urls = '''    path('cursos/<int:curso_id>/toggle/', prof.curso_toggle_publicar, name='curso_toggle'),'''
    idx = c.rfind("]")
    c = c[:idx] + nuevas_urls + "\n" + c[idx:]
    up.write_text(c, encoding="utf-8")
    print("[OK] URL toggle añadida")
else:
    print("[SKIP] URL toggle ya estaba")

# ============================================================
# 4) Actualizar el detalle de estudiante para usar la nueva vista
# ============================================================
# Sobrescribir la vista detalle_estudiante vieja para que apunte a la completa
# (más simple: reemplazar el decorador y la función)

patron_viejo = '''@profesor_required
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
    return render(request, "core/profesor/estudiantes/detalle.html", context)'''

patron_nuevo = '''@profesor_required
def detalle_estudiante(request, estudiante_id):
    """Alias → detalle_estudiante_completo (vista enriquecida)."""
    return detalle_estudiante_completo(request, estudiante_id)'''

vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8")
if patron_viejo in c:
    c = c.replace(patron_viejo, patron_nuevo)
    vp.write_text(c, encoding="utf-8")
    print("[OK] detalle_estudiante ahora apunta a la versión completa")

# ============================================================
# 5) Template detalle estudiante enriquecido
# ============================================================
tpl = BASE / "core" / "templates" / "core" / "profesor" / "estudiantes" / "detalle.html"

nuevo_tpl = '''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:estudiantes' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>

<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="mb-1"><i class="fas fa-user-graduate"></i> {{ estudiante.username }}</h2>
    <p class="text-muted mb-0">
      {{ estudiante.get_full_name|default:"—" }} · {{ estudiante.email|default:"—" }}
    </p>
  </div>
  <span class="badge bg-primary fs-6">Estudiante</span>
</div>

<!-- KPIs del estudiante -->
<div class="row g-3 mb-4">
  <div class="col-md-2">
    <div class="card shadow-sm border-0 bg-primary text-white">
      <div class="card-body text-center">
        <div class="fs-3 fw-bold">{{ stats.cursos_activos }}</div>
        <div><small>Cursos activos</small></div>
      </div>
    </div>
  </div>
  <div class="col-md-2">
    <div class="card shadow-sm border-0 bg-info text-white">
      <div class="card-body text-center">
        <div class="fs-3 fw-bold">{{ stats.total_respuestas }}</div>
        <div><small>Respuestas</small></div>
      </div>
    </div>
  </div>
  <div class="col-md-2">
    <div class="card shadow-sm border-0 bg-success text-white">
      <div class="card-body text-center">
        <div class="fs-3 fw-bold">{{ stats.tasa_aciertos }}%</div>
        <div><small>Aciertos</small></div>
      </div>
    </div>
  </div>
  <div class="col-md-2">
    <div class="card shadow-sm border-0 bg-warning text-dark">
      <div class="card-body text-center">
        <div class="fs-3 fw-bold">{{ stats.logros }}</div>
        <div><small>Logros</small></div>
      </div>
    </div>
  </div>
  <div class="col-md-2">
    <div class="card shadow-sm border-0 bg-success text-white">
      <div class="card-body text-center">
        <div class="fs-3 fw-bold">{{ stats.certificados }}</div>
        <div><small>Certificados</small></div>
      </div>
    </div>
  </div>
  <div class="col-md-2">
    <div class="card shadow-sm border-0 bg-secondary text-white">
      <div class="card-body text-center">
        <div class="fs-3 fw-bold">{{ stats.correctas }}</div>
        <div><small>Correctas</small></div>
      </div>
    </div>
  </div>
</div>

<!-- Cursos asignados -->
<div class="card shadow-sm mb-4">
  <div class="card-header bg-white fw-bold">
    <i class="fas fa-book"></i> Cursos asignados ({{ cursos_data|length }})
  </div>
  <div class="table-responsive">
    <table class="table table-hover align-middle mb-0">
      <thead class="table-light">
        <tr>
          <th>Curso</th>
          <th>Progreso</th>
          <th>Lecciones</th>
          <th>Promedio</th>
        </tr>
      </thead>
      <tbody>
        {% for c in cursos_data %}
        <tr>
          <td><strong>{{ c.curso.titulo }}</strong></td>
          <td style="min-width:180px;">
            <div class="progress" style="height:20px;">
              <div class="progress-bar bg-success" style="width:{{ c.progreso_pct }}%;">
                {{ c.progreso_pct }}%
              </div>
            </div>
          </td>
          <td>{{ c.completadas }} / {{ c.total_lecciones }}</td>
          <td><span class="badge bg-info text-dark">{{ c.promedio }} pts</span></td>
        </tr>
        {% empty %}
        <tr><td colspan="4" class="text-center text-muted py-3">Sin cursos con progreso</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<div class="row g-3 mb-4">
  <!-- Evaluaciones realizadas -->
  <div class="col-md-6">
    <div class="card shadow-sm h-100">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-clipboard-check"></i> Evaluaciones realizadas ({{ evaluaciones_data|length }})
      </div>
      <ul class="list-group list-group-flush" style="max-height:300px;overflow:auto;">
        {% for e in evaluaciones_data %}
        <li class="list-group-item">
          <div class="d-flex justify-content-between">
            <div>
              <strong>{{ e.evaluacion.titulo }}</strong><br>
              <small class="text-muted">
                {{ e.evaluacion.curso.titulo }} · {{ e.intentos }} intento(s)
              </small>
            </div>
            <div class="text-end">
              <span class="badge bg-success fs-6">{{ e.mejor_puntaje }}/{{ e.puntaje_maximo }}</span>
            </div>
          </div>
        </li>
        {% empty %}
        <li class="list-group-item text-muted text-center py-3">Sin evaluaciones realizadas</li>
        {% endfor %}
      </ul>
    </div>
  </div>

  <!-- Certificados -->
  <div class="col-md-6">
    <div class="card shadow-sm h-100">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-certificate"></i> Certificados ({{ certificados.count }})
      </div>
      <ul class="list-group list-group-flush">
        {% for c in certificados %}
        <li class="list-group-item">
          <div class="d-flex justify-content-between">
            <div>
              <strong>{{ c.certificacion.nombre }}</strong><br>
              <small class="text-muted">Código: {{ c.codigo_verificacion }}</small>
            </div>
            <span class="badge bg-success">{{ c.fecha_obtenida|date:"SHORT_DATE_FORMAT" }}</span>
          </div>
        </li>
        {% empty %}
        <li class="list-group-item text-muted text-center py-3">Sin certificados</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>

<div class="row g-3">
  <!-- Logros -->
  <div class="col-md-6">
    <div class="card shadow-sm h-100">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-trophy"></i> Logros ({{ logros.count }})
      </div>
      <div class="card-body">
        {% for l in logros %}
        <span class="badge bg-warning text-dark me-1 mb-1" title="{{ l.logro.descripcion }}">
          {{ l.logro.icono }} {{ l.logro.nombre }}
        </span>
        {% empty %}
        <p class="text-muted text-center mb-0">Sin logros</p>
        {% endfor %}
      </div>
    </div>
  </div>

  <!-- Respuestas recientes -->
  <div class="col-md-6">
    <div class="card shadow-sm h-100">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-history"></i> Últimas respuestas
      </div>
      <ul class="list-group list-group-flush" style="max-height:300px;overflow:auto;">
        {% for r in respuestas %}
        <li class="list-group-item d-flex justify-content-between">
          <div>
            <small class="text-muted">{{ r.fecha|date:"SHORT_DATETIME_FORMAT" }}</small><br>
            <span>{{ r.tipo_ejercicio }} #{{ r.item_id }}</span>
          </div>
          <div>
            {% if r.es_correcta %}
              <span class="badge bg-success">✓ {{ r.puntuacion }} pts</span>
            {% else %}
              <span class="badge bg-danger">✗ 0 pts</span>
            {% endif %}
          </div>
        </li>
        {% empty %}
        <li class="list-group-item text-muted text-center py-3">Sin respuestas</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>
{% endblock %}
'''
tpl.write_text(nuevo_tpl, encoding="utf-8")
print("[OK] detalle.html enriquecido")

# ============================================================
# 6) Añadir botón "Toggle publicar" en lista de cursos
# ============================================================
tpl_cursos = BASE / "core" / "templates" / "core" / "profesor" / "cursos" / "lista.html"
c = tpl_cursos.read_text(encoding="utf-8")

if "curso_toggle" not in c:
    # Insertar botón de toggle antes del botón Editar
    c2 = c.replace(
        '''<a href="{% url 'profesor:curso_editar' c.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-edit"></i>
          </a>''',
        '''<form method="post" action="{% url 'profesor:curso_toggle' c.id %}" class="d-inline">
            {% csrf_token %}
            {% if c.estado == "publicado" %}
              <button class="btn btn-sm btn-outline-warning" title="Pasar a borrador">
                <i class="fas fa-eye-slash"></i>
              </button>
            {% else %}
              <button class="btn btn-sm btn-outline-success" title="Publicar">
                <i class="fas fa-eye"></i>
              </button>
            {% endif %}
          </form>
          <a href="{% url 'profesor:curso_editar' c.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-edit"></i>
          </a>''',
        1,
    )
    if c2 != c:
        tpl_cursos.write_text(c2, encoding="utf-8")
        print("[OK] botón toggle publicar añadido a cursos/lista.html")
    else:
        print("[!] No se pudo insertar el botón toggle. Añádelo manualmente.")
else:
    print("[SKIP] botón toggle ya estaba")

print()
print("=" * 60)
print("[OK] FASE 2 completa")
print("=" * 60)
print()
print("Ahora ejecuta:")
print("  python manage.py check")
print("  python manage.py runserver 8001 --noreload")
