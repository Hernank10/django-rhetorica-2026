from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Añadir vistas de Módulos al final de views_profesor.py
# ============================================================
vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8")

nuevas = '''

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
        opciones = [{"texto": o.strip()} for o in opciones_raw.split("\n") if o.strip()]

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
'''

if "def modulos_lista" not in c:
    c = c.rstrip() + "\n" + nuevas
    vp.write_text(c, encoding="utf-8")
    print("[OK] views_profesor.py extendido (módulos + evaluaciones + preguntas)")
else:
    print("[SKIP] vistas ya existían")

# ============================================================
# 2) Templates
# ============================================================
TPL = BASE / "core" / "templates" / "core" / "profesor"
for sub in ["modulos", "evaluaciones"]:
    (TPL / sub).mkdir(parents=True, exist_ok=True)

# modulos/lista.html
(TPL / "modulos" / "lista.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="mb-0"><i class="fas fa-layer-group"></i> Módulos</h2>
  <a href="{% url 'profesor:modulo_crear' %}" class="btn btn-primary">
    <i class="fas fa-plus"></i> Nuevo módulo
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
        <th>Orden</th>
        <th>Módulo</th>
        <th>Lecciones</th>
        <th class="text-end">Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for m in modulos %}
      <tr>
        <td>{{ m.curso.titulo }}</td>
        <td>{{ m.orden }}</td>
        <td>
          <strong>{{ m.titulo }}</strong><br>
          <small class="text-muted">{{ m.descripcion|truncatechars:80 }}</small>
        </td>
        <td>{{ m.lecciones.count }}</td>
        <td class="text-end">
          <a href="{% url 'profesor:modulo_editar' m.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-edit"></i>
          </a>
          <form method="post" action="{% url 'profesor:modulo_eliminar' m.id %}" class="d-inline"
                onsubmit="return confirm('¿Eliminar el módulo y todas sus lecciones?');">
            {% csrf_token %}
            <button class="btn btn-sm btn-outline-danger"><i class="fas fa-trash"></i></button>
          </form>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="5" class="text-center text-muted">Sin módulos</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] modulos/lista.html")

# modulos/form.html
(TPL / "modulos" / "form.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:modulos_lista' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>
<h2 class="mb-4">
  {% if modulo %}<i class="fas fa-edit"></i> Editar módulo{% else %}<i class="fas fa-plus"></i> Nuevo módulo{% endif %}
</h2>

<form method="post" class="card shadow-sm">
  {% csrf_token %}
  <div class="card-body">
    <div class="mb-3">
      <label class="form-label">Curso *</label>
      <select name="curso" class="form-select" required>
        <option value="">— Selecciona un curso —</option>
        {% for c in cursos %}
          <option value="{{ c.id }}"
            {% if modulo.curso_id == c.id %}selected{% elif curso_pre == c.id|stringformat:"s" %}selected{% endif %}>
            {{ c.titulo }}
          </option>
        {% endfor %}
      </select>
    </div>
    <div class="mb-3">
      <label class="form-label">Título *</label>
      <input type="text" name="titulo" class="form-control" required
             value="{{ modulo.titulo|default:'' }}">
    </div>
    <div class="mb-3">
      <label class="form-label">Descripción</label>
      <textarea name="descripcion" class="form-control" rows="3">{{ modulo.descripcion|default:'' }}</textarea>
    </div>
    <div class="mb-3">
      <label class="form-label">Orden</label>
      <input type="number" name="orden" class="form-control" value="{{ modulo.orden|default:1 }}">
    </div>
  </div>
  <div class="card-footer text-end bg-white">
    <a href="{% url 'profesor:modulos_lista' %}" class="btn btn-secondary">Cancelar</a>
    <button class="btn btn-primary"><i class="fas fa-save"></i> Guardar</button>
  </div>
</form>
{% endblock %}
''', encoding="utf-8")
print("[OK] modulos/form.html")

# evaluaciones/form.html
(TPL / "evaluaciones" / "form.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:evaluaciones' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>
<h2 class="mb-4">
  {% if evaluacion %}<i class="fas fa-edit"></i> Editar evaluación{% else %}<i class="fas fa-plus"></i> Nueva evaluación{% endif %}
</h2>

<form method="post" class="card shadow-sm">
  {% csrf_token %}
  <div class="card-body">
    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label">Curso *</label>
        <select name="curso" class="form-select" required>
          <option value="">— Selecciona —</option>
          {% for c in cursos %}
            <option value="{{ c.id }}"
              {% if evaluacion.curso_id == c.id %}selected{% elif curso_pre == c.id|stringformat:"s" %}selected{% endif %}>
              {{ c.titulo }}
            </option>
          {% endfor %}
        </select>
      </div>
      <div class="col-md-6 mb-3">
        <label class="form-label">Módulo (opcional)</label>
        <select name="modulo" class="form-select">
          <option value="">— Ninguno (evaluación del curso) —</option>
          {% for m in modulos %}
            <option value="{{ m.id }}" {% if evaluacion.modulo_id == m.id %}selected{% endif %}>
              {{ m.curso.titulo }} → {{ m.titulo }}
            </option>
          {% endfor %}
        </select>
      </div>
    </div>

    <div class="mb-3">
      <label class="form-label">Título *</label>
      <input type="text" name="titulo" class="form-control" required
             value="{{ evaluacion.titulo|default:'' }}">
    </div>
    <div class="mb-3">
      <label class="form-label">Descripción</label>
      <textarea name="descripcion" class="form-control" rows="2">{{ evaluacion.descripcion|default:'' }}</textarea>
    </div>
    <div class="row">
      <div class="col-md-3 mb-3">
        <label class="form-label">Tipo de evaluación *</label>
        <select name="tipo" class="form-select">
          <option value="diagnostica" {% if evaluacion.tipo == "diagnostica" %}selected{% endif %}>📋 Diagnóstica</option>
          <option value="modulo" {% if evaluacion.tipo == "modulo" or not evaluacion %}selected{% endif %}>📝 Por módulo</option>
          <option value="recapitulacion" {% if evaluacion.tipo == "recapitulacion" %}selected{% endif %}>🔄 Recapitulación</option>
          <option value="final" {% if evaluacion.tipo == "final" %}selected{% endif %}>🎓 Final</option>
        </select>
      </div>
      <div class="col-md-2 mb-3">
        <label class="form-label">Preguntas / intento</label>
        <input type="number" name="preguntas_por_evaluacion" class="form-control"
               value="{{ evaluacion.preguntas_por_evaluacion|default:5 }}">
      </div>
      <div class="col-md-2 mb-3">
        <label class="form-label">Tiempo (min)</label>
        <input type="number" name="tiempo_limite" class="form-control"
               value="{{ evaluacion.tiempo_limite|default:30 }}">
      </div>
      <div class="col-md-2 mb-3">
        <label class="form-label">Puntaje máximo</label>
        <input type="number" name="puntaje_maximo" class="form-control"
               value="{{ evaluacion.puntaje_maximo|default:100 }}">
      </div>
      <div class="col-md-3 mb-3">
        <label class="form-label">Intentos permitidos</label>
        <input type="number" name="intentos_permitidos" class="form-control"
               value="{{ evaluacion.intentos_permitidos|default:3 }}">
      </div>
    </div>
  </div>
  <div class="card-footer text-end bg-white">
    <a href="{% url 'profesor:evaluaciones' %}" class="btn btn-secondary">Cancelar</a>
    <button class="btn btn-primary"><i class="fas fa-save"></i> Guardar</button>
  </div>
</form>
{% endblock %}
''', encoding="utf-8")
print("[OK] evaluaciones/form.html")

# evaluaciones/detalle.html
(TPL / "evaluaciones" / "detalle.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:evaluaciones' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>

<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="mb-1">{{ evaluacion.titulo }}</h2>
    <p class="text-muted mb-0">
      {{ evaluacion.curso.titulo }}
      {% if evaluacion.modulo %}· {{ evaluacion.modulo.titulo }}{% endif %}
      · <span class="badge bg-secondary">{{ evaluacion.get_tipo_display|default:evaluacion.tipo }}</span>
    </p>
  </div>
  <a href="{% url 'profesor:pregunta_crear' evaluacion.id %}" class="btn btn-primary">
    <i class="fas fa-plus"></i> Nueva pregunta
  </a>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-3"><div class="card"><div class="card-body">
    <h6 class="text-muted">Preguntas</h6>
    <div class="fs-4">{{ preguntas.count }}</div>
  </div></div></div>
  <div class="col-md-3"><div class="card"><div class="card-body">
    <h6 class="text-muted">Puntaje</h6>
    <div class="fs-4">{{ evaluacion.puntaje_maximo }}</div>
  </div></div></div>
  <div class="col-md-3"><div class="card"><div class="card-body">
    <h6 class="text-muted">Tiempo</h6>
    <div class="fs-4">{{ evaluacion.tiempo_limite }} min</div>
  </div></div></div>
  <div class="col-md-3"><div class="card"><div class="card-body">
    <h6 class="text-muted">Intentos</h6>
    <div class="fs-4">{{ evaluacion.intentos_permitidos }}</div>
  </div></div></div>
</div>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>#</th>
        <th>Enunciado</th>
        <th>Tipo</th>
        <th>Respuesta correcta</th>
        <th>Puntos</th>
        <th class="text-end">Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for p in preguntas %}
      <tr>
        <td>{{ p.orden }}</td>
        <td>{{ p.enunciado|truncatechars:100 }}</td>
        <td><span class="badge bg-secondary">{{ p.tipo }}</span></td>
        <td><code>{{ p.respuesta_correcta|truncatechars:40 }}</code></td>
        <td>{{ p.puntaje }}</td>
        <td class="text-end">
          <a href="{% url 'profesor:pregunta_editar' evaluacion.id p.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-edit"></i>
          </a>
          <form method="post" action="{% url 'profesor:pregunta_eliminar' evaluacion.id p.id %}" class="d-inline"
                onsubmit="return confirm('¿Eliminar la pregunta?');">
            {% csrf_token %}
            <button class="btn btn-sm btn-outline-danger"><i class="fas fa-trash"></i></button>
          </form>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="6" class="text-center text-muted">Sin preguntas. Crea la primera.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] evaluaciones/detalle.html")

# evaluaciones/pregunta_form.html
(TPL / "evaluaciones" / "pregunta_form.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:evaluacion_detalle' evaluacion.id %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver a {{ evaluacion.titulo }}
</a>
<h2 class="mb-4">
  {% if pregunta %}<i class="fas fa-edit"></i> Editar pregunta{% else %}<i class="fas fa-plus"></i> Nueva pregunta{% endif %}
</h2>

<form method="post" class="card shadow-sm">
  {% csrf_token %}
  <div class="card-body">
    <div class="mb-3">
      <label class="form-label">Enunciado *</label>
      <textarea name="enunciado" class="form-control" rows="3" required>{{ pregunta.enunciado|default:'' }}</textarea>
    </div>
    <div class="row">
      <div class="col-md-4 mb-3">
        <label class="form-label">Tipo</label>
        <select name="tipo" class="form-select">
          <option value="multiple_choice" {% if pregunta.tipo == "multiple_choice" or not pregunta %}selected{% endif %}>Opción múltiple</option>
          <option value="verdadero_falso" {% if pregunta.tipo == "verdadero_falso" %}selected{% endif %}>Verdadero/Falso</option>
          <option value="completar" {% if pregunta.tipo == "completar" %}selected{% endif %}>Completar</option>
        </select>
      </div>
      <div class="col-md-4 mb-3">
        <label class="form-label">Puntaje</label>
        <input type="number" name="puntaje" class="form-control" value="{{ pregunta.puntaje|default:20 }}">
      </div>
      <div class="col-md-4 mb-3">
        <label class="form-label">Orden</label>
        <input type="number" name="orden" class="form-control" value="{{ pregunta.orden|default:1 }}">
      </div>
    </div>
    <div class="mb-3">
      <label class="form-label">Opciones (una por línea)</label>
      <textarea name="opciones" class="form-control" rows="4"
        placeholder="Opción A&#10;Opción B&#10;Opción C&#10;Opción D">{% for o in pregunta.opciones %}{{ o.texto }}{% if not forloop.last %}
{% endif %}{% endfor %}</textarea>
    </div>
    <div class="mb-3">
      <label class="form-label">Respuesta correcta *</label>
      <input type="text" name="respuesta_correcta" class="form-control" required
             value="{{ pregunta.respuesta_correcta|default:'' }}">
    </div>
  </div>
  <div class="card-footer text-end bg-white">
    <a href="{% url 'profesor:evaluacion_detalle' evaluacion.id %}" class="btn btn-secondary">Cancelar</a>
    <button class="btn btn-primary"><i class="fas fa-save"></i> Guardar</button>
  </div>
</form>
{% endblock %}
''', encoding="utf-8")
print("[OK] evaluaciones/pregunta_form.html")

# ============================================================
# 3) Actualizar urls_profesor.py
# ============================================================
up = BASE / "core" / "urls_profesor.py"
c = up.read_text(encoding="utf-8")

nuevas_urls = '''    # Módulos
    path('modulos/', prof.modulos_lista, name='modulos_lista'),
    path('modulos/crear/', prof.modulo_form, name='modulo_crear'),
    path('modulos/<int:modulo_id>/editar/', prof.modulo_form, name='modulo_editar'),
    path('modulos/<int:modulo_id>/eliminar/', prof.modulo_eliminar, name='modulo_eliminar'),

    # Evaluaciones + Preguntas
    path('evaluaciones/crear/', prof.evaluacion_form, name='evaluacion_crear'),
    path('evaluaciones/<int:evaluacion_id>/', prof.evaluacion_detalle, name='evaluacion_detalle'),
    path('evaluaciones/<int:evaluacion_id>/editar/', prof.evaluacion_form, name='evaluacion_editar'),
    path('evaluaciones/<int:evaluacion_id>/eliminar/', prof.evaluacion_eliminar, name='evaluacion_eliminar'),
    path('evaluaciones/<int:evaluacion_id>/preguntas/crear/', prof.pregunta_form, name='pregunta_crear'),
    path('evaluaciones/<int:evaluacion_id>/preguntas/<int:pregunta_id>/editar/', prof.pregunta_form, name='pregunta_editar'),
    path('evaluaciones/<int:evaluacion_id>/preguntas/<int:pregunta_id>/eliminar/', prof.pregunta_eliminar, name='pregunta_eliminar'),
'''

if "modulos_lista" not in c:
    # Insertar antes del ']' final
    idx = c.rfind("]")
    c = c[:idx] + nuevas_urls + c[idx:]
    up.write_text(c, encoding="utf-8")
    print("[OK] urls_profesor.py actualizado")
else:
    print("[SKIP] URLs ya estaban")
