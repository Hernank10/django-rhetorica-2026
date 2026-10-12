"""
Asocia Recurso a Curso, Modulo, Leccion, EvaluacionCurso y EjercicioLinguistico.
Añade vista unificada de vinculación + botones en los detalles.
Idempotente: se puede ejecutar varias veces sin duplicar.
"""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")
print("=" * 60)
print("ASOCIAR RECURSOS A CURSOS/MODULOS/LECCIONES/EVALUACIONES/EJERCICIOS")
print("=" * 60)

# ============================================================
# 1) MODELO: añadir FKs a Recurso
# ============================================================
print()
print("[1/6] Modelo Recurso")
mp = BASE / "core" / "models.py"
c = mp.read_text(encoding="utf-8")

nuevos_campos = """
    modulo = models.ForeignKey(
        'core.Modulo', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    leccion = models.ForeignKey(
        'core.Leccion', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    evaluacion_curso = models.ForeignKey(
        'core.EvaluacionCurso', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    ejercicio = models.ForeignKey(
        'core.EjercicioLinguistico', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    orden = models.PositiveIntegerField(default=0)
    destacado = models.BooleanField(default=False)
"""

if "modulo = models.ForeignKey" in c and "recursos" in c:
    print("[SKIP] FKs ya estaban en el modelo")
else:
    # Insertar los campos justo antes de "creado_en"
    patron = re.compile(r"(\n    creado_en = models\.DateTimeField\(auto_now_add=True\))")
    if patron.search(c):
        c = patron.sub(nuevos_campos + r"\1", c, count=1)
        mp.write_text(c, encoding="utf-8")
        print("[OK] FKs modulo/leccion/evaluacion_curso/ejercicio + orden + destacado añadidas")
    else:
        print("[!] No se encontró 'creado_en' en Recurso. Revisa manualmente")

# ============================================================
# 2) VISTAS: añadir a views_recursos.py
# ============================================================
print()
print("[2/6] Vistas de vinculación")
vp = BASE / "core" / "views_recursos.py"
c = vp.read_text(encoding="utf-8")

vistas_nuevas = '''

# ============================================================
# VINCULACIÓN DE RECURSOS A OBJETOS DE APRENDIZAJE
# ============================================================
from django.contrib import messages
from django.shortcuts import redirect

from .models import Curso, Modulo, Leccion, EvaluacionCurso, EjercicioLinguistico


def _catalogo_objetos():
    """Devuelve dicts para los selects del formulario."""
    return {
        "cursos": Curso.objects.all().order_by("titulo"),
        "modulos": Modulo.objects.select_related("curso").order_by("curso__titulo", "titulo"),
        "lecciones": Leccion.objects.select_related("modulo__curso").order_by("modulo__curso__titulo", "orden"),
        "evaluaciones": EvaluacionCurso.objects.select_related("curso").order_by("curso__titulo", "titulo"),
        "ejercicios": EjercicioLinguistico.objects.all().order_by("titulo")[:500],
    }


@login_required
def vincular_recurso(request, slug):
    """Formulario único para vincular un Recurso a curso/modulo/leccion/evaluacion/ejercicio."""
    recurso = get_object_or_404(Recurso, slug=slug)

    if request.method == "POST":
        recurso.curso_id = request.POST.get("curso") or None
        recurso.modulo_id = request.POST.get("modulo") or None
        recurso.leccion_id = request.POST.get("leccion") or None
        recurso.evaluacion_curso_id = request.POST.get("evaluacion_curso") or None
        recurso.ejercicio_id = request.POST.get("ejercicio") or None
        try:
            recurso.orden = int(request.POST.get("orden") or 0)
        except ValueError:
            recurso.orden = 0
        recurso.destacado = "destacado" in request.POST
        recurso.save()
        messages.success(request, f"Recurso «{recurso.nombre}» vinculado correctamente.")
        return redirect("recursos:ver", slug=recurso.slug)

    ctx = {"recurso": recurso}
    ctx.update(_catalogo_objetos())
    return render(request, "core/recursos/vincular.html", ctx)


@login_required
def desvincular_recurso(request, slug, tipo):
    """Quita un vínculo específico del recurso."""
    recurso = get_object_or_404(Recurso, slug=slug)
    campos = {"curso", "modulo", "leccion", "evaluacion_curso", "ejercicio"}
    if tipo not in campos:
        raise Http404("Tipo inválido")

    if request.method == "POST":
        setattr(recurso, f"{tipo}_id", None)
        recurso.save(update_fields=[tipo])
        messages.info(request, f"Vínculo «{tipo}» eliminado.")
    return redirect("recursos:ver", slug=recurso.slug)


@login_required
def recursos_para_objeto(request, tipo, obj_id):
    """Lista los recursos vinculados a un objeto (curso/modulo/leccion/evaluacion/ejercicio)."""
    mapa = {
        "curso": (Curso, "curso"),
        "modulo": (Modulo, "modulo"),
        "leccion": (Leccion, "leccion"),
        "evaluacion": (EvaluacionCurso, "evaluacion_curso"),
        "ejercicio": (EjercicioLinguistico, "ejercicio"),
    }
    if tipo not in mapa:
        raise Http404("Tipo inválido")
    modelo, campo = mapa[tipo]
    obj = get_object_or_404(modelo, pk=obj_id)

    vinculados = Recurso.objects.filter(**{campo: obj}).order_by("orden", "nombre")
    disponibles = Recurso.objects.exclude(pk__in=[r.pk for r in vinculados]).order_by("categoria", "nombre")[:500]

    return render(request, "core/recursos/para_objeto.html", {
        "tipo": tipo,
        "objeto": obj,
        "vinculados": vinculados,
        "disponibles": disponibles,
        "campo": campo,
    })


@login_required
def asignar_recursos(request, tipo, obj_id):
    """POST: recibe [recurso_ids] y los asigna al objeto."""
    mapa = {
        "curso": (Curso, "curso"),
        "modulo": (Modulo, "modulo"),
        "leccion": (Leccion, "leccion"),
        "evaluacion": (EvaluacionCurso, "evaluacion_curso"),
        "ejercicio": (EjercicioLinguistico, "ejercicio"),
    }
    if tipo not in mapa:
        raise Http404("Tipo inválido")
    modelo, campo = mapa[tipo]
    obj = get_object_or_404(modelo, pk=obj_id)

    if request.method == "POST":
        ids = request.POST.getlist("recurso_ids")
        if ids:
            Recurso.objects.filter(pk__in=ids).update(**{campo: obj})
            messages.success(request, f"{len(ids)} recurso(s) asignado(s).")
        else:
            messages.warning(request, "No seleccionaste ningún recurso.")
    return redirect("recursos:para_objeto", tipo=tipo, obj_id=obj_id)


@login_required
def quitar_recurso(request, tipo, obj_id, recurso_id):
    """POST: quita un recurso específico del objeto."""
    mapa = {
        "curso": "curso",
        "modulo": "modulo",
        "leccion": "leccion",
        "evaluacion": "evaluacion_curso",
        "ejercicio": "ejercicio",
    }
    if tipo not in mapa:
        raise Http404("Tipo inválido")
    campo = mapa[tipo]
    recurso = get_object_or_404(Recurso, pk=recurso_id)
    setattr(recurso, f"{campo}_id", None)
    recurso.save(update_fields=[campo])
    messages.info(request, f"Recurso «{recurso.nombre}» desvinculado.")
    return redirect("recursos:para_objeto", tipo=tipo, obj_id=obj_id)
'''

if "def vincular_recurso(" in c:
    print("[SKIP] Vistas de vinculación ya existen")
else:
    c = c.rstrip() + vistas_nuevas
    vp.write_text(c, encoding="utf-8")
    print("[OK] Vistas añadidas a views_recursos.py")

# ============================================================
# 3) URLs: añadir a urls_recursos.py
# ============================================================
print()
print("[3/6] URLs")
up = BASE / "core" / "urls_recursos.py"
c = up.read_text(encoding="utf-8")

if "vincular" in c:
    print("[SKIP] URLs ya existen")
else:
    nuevas = """    path("<slug:slug>/vincular/", r.vincular_recurso, name="vincular"),
    path("<slug:slug>/desvincular/<str:tipo>/", r.desvincular_recurso, name="desvincular"),
    path("objeto/<str:tipo>/<int:obj_id>/", r.recursos_para_objeto, name="para_objeto"),
    path("objeto/<str:tipo>/<int:obj_id>/asignar/", r.asignar_recursos, name="asignar"),
    path("objeto/<str:tipo>/<int:obj_id>/quitar/<int:recurso_id>/", r.quitar_recurso, name="quitar"),
"""
    idx = c.rfind("]")
    c = c[:idx] + nuevas + c[idx:]
    up.write_text(c, encoding="utf-8")
    print("[OK] URLs añadidas")

# ============================================================
# 4) Template: vincular.html
# ============================================================
print()
print("[4/6] Templates")
TPL = BASE / "core" / "templates" / "core" / "recursos"
TPL.mkdir(parents=True, exist_ok=True)

(TPL / "vincular.html").write_text('''{% extends 'base.html' %}
{% block content %}
<div class="container mt-4">
  <a href="{% url 'recursos:ver' recurso.slug %}" class="btn btn-sm btn-outline-secondary mb-3">
    <i class="fas fa-arrow-left"></i> Volver al recurso
  </a>

  <h2 class="mb-3"><i class="fas fa-link"></i> Vincular recurso</h2>

  <div class="card shadow-sm mb-4">
    <div class="card-body">
      <h5 class="mb-1">{{ recurso.nombre }}</h5>
      <small class="text-muted">
        <span class="badge bg-{{ recurso.color_badge }}">{{ recurso.categoria }}</span>
        .{{ recurso.extension }} · {{ recurso.tamaño_legible }}
      </small>
    </div>
  </div>

  <form method="post" class="card shadow-sm">
    {% csrf_token %}
    <div class="card-body">
      <div class="row g-3">

        <div class="col-md-6">
          <label class="form-label">Curso</label>
          <select name="curso" class="form-select">
            <option value="">— sin curso —</option>
            {% for c in cursos %}
              <option value="{{ c.id }}" {% if recurso.curso_id == c.id %}selected{% endif %}>
                {{ c.titulo }}
              </option>
            {% endfor %}
          </select>
        </div>

        <div class="col-md-6">
          <label class="form-label">Módulo</label>
          <select name="modulo" class="form-select">
            <option value="">— sin módulo —</option>
            {% for m in modulos %}
              <option value="{{ m.id }}" {% if recurso.modulo_id == m.id %}selected{% endif %}>
                {{ m.curso.titulo }} → {{ m.titulo }}
              </option>
            {% endfor %}
          </select>
        </div>

        <div class="col-md-6">
          <label class="form-label">Lección</label>
          <select name="leccion" class="form-select">
            <option value="">— sin lección —</option>
            {% for l in lecciones %}
              <option value="{{ l.id }}" {% if recurso.leccion_id == l.id %}selected{% endif %}>
                {{ l.modulo.curso.titulo }} → {{ l.titulo }}
              </option>
            {% endfor %}
          </select>
        </div>

        <div class="col-md-6">
          <label class="form-label">Evaluación de curso</label>
          <select name="evaluacion_curso" class="form-select">
            <option value="">— sin evaluación —</option>
            {% for e in evaluaciones %}
              <option value="{{ e.id }}" {% if recurso.evaluacion_curso_id == e.id %}selected{% endif %}>
                {{ e.curso.titulo }} → {{ e.titulo }}
              </option>
            {% endfor %}
          </select>
        </div>

        <div class="col-md-6">
          <label class="form-label">Ejercicio (práctica)</label>
          <select name="ejercicio" class="form-select">
            <option value="">— sin ejercicio —</option>
            {% for e in ejercicios %}
              <option value="{{ e.id }}" {% if recurso.ejercicio_id == e.id %}selected{% endif %}>
                {{ e.titulo }}
              </option>
            {% endfor %}
          </select>
        </div>

        <div class="col-md-3">
          <label class="form-label">Orden</label>
          <input type="number" name="orden" value="{{ recurso.orden|default:0 }}" min="0" class="form-control">
        </div>

        <div class="col-md-3 d-flex align-items-end">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" name="destacado" id="destacado"
                   {% if recurso.destacado %}checked{% endif %}>
            <label class="form-check-label" for="destacado">Destacado</label>
          </div>
        </div>

      </div>
    </div>

    <div class="card-footer bg-white text-end">
      <a href="{% url 'recursos:ver' recurso.slug %}" class="btn btn-secondary">Cancelar</a>
      <button class="btn btn-primary"><i class="fas fa-save"></i> Guardar vínculos</button>
    </div>
  </form>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] vincular.html")

(TPL / "para_objeto.html").write_text('''{% extends 'base.html' %}
{% block content %}
<div class="container-fluid mt-4">
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h2 class="mb-0">
      <i class="fas fa-folder-open text-warning"></i>
      Recursos para {{ tipo }}: {{ objeto }}
    </h2>
    <span class="badge bg-secondary">{{ vinculados|length }} vinculados</span>
  </div>

  <div class="row g-3">
    <!-- VINCULADOS -->
    <div class="col-md-6">
      <div class="card shadow-sm">
        <div class="card-header bg-white fw-bold">
          <i class="fas fa-check-circle text-success"></i> Vinculados
        </div>
        <div class="list-group list-group-flush" style="max-height:60vh;overflow:auto;">
          {% for r in vinculados %}
            <div class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <span class="badge bg-{{ r.color_badge }}">{{ r.categoria }}</span>
                <div class="mt-1">{{ r.nombre|truncatechars:70 }}</div>
                <small class="text-muted">.{{ r.extension }} · {{ r.tamaño_legible }}</small>
              </div>
              <form method="post" action="{% url 'recursos:quitar' tipo=tipo obj_id=objeto.id recurso_id=r.id %}"
                    onsubmit="return confirm('¿Quitar este recurso?');">
                {% csrf_token %}
                <button class="btn btn-sm btn-outline-danger"><i class="fas fa-times"></i></button>
              </form>
            </div>
          {% empty %}
            <div class="list-group-item text-muted text-center py-4">
              Sin recursos vinculados aún.
            </div>
          {% endfor %}
        </div>
      </div>
    </div>

    <!-- DISPONIBLES -->
    <div class="col-md-6">
      <div class="card shadow-sm">
        <div class="card-header bg-white fw-bold">
          <i class="fas fa-plus-circle text-primary"></i> Disponibles para asignar
        </div>
        <form method="post" action="{% url 'recursos:asignar' tipo=tipo obj_id=objeto.id %}">
          {% csrf_token %}
          <div class="list-group list-group-flush" style="max-height:50vh;overflow:auto;">
            {% for r in disponibles %}
              <label class="list-group-item d-flex align-items-center">
                <input type="checkbox" name="recurso_ids" value="{{ r.id }}" class="form-check-input me-2">
                <div>
                  <span class="badge bg-{{ r.color_badge }}">{{ r.categoria }}</span>
                  <div class="mt-1">{{ r.nombre|truncatechars:70 }}</div>
                </div>
              </label>
            {% empty %}
              <div class="list-group-item text-muted text-center py-4">
                Todos los recursos ya están vinculados.
              </div>
            {% endfor %}
          </div>
          <div class="card-footer bg-white text-end">
            <button class="btn btn-primary" {% if not disponibles %}disabled{% endif %}>
              <i class="fas fa-check"></i> Asignar seleccionados
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] para_objeto.html")

# ============================================================
# 5) Añadir botón "Vincular" en visor del recurso
# ============================================================
print()
print("[5/6] Botón «Vincular» en el visor del recurso")

for nombre in ("visor_html.html", "visor_json.html", "visor_texto.html"):
    t = TPL / nombre
    if not t.exists():
        continue
    c = t.read_text(encoding="utf-8")
    if "recursos:vincular" in c:
        print(f"[SKIP] {nombre} ya tiene botón vincular")
        continue
    # Insertar antes del cierre del primer div con btn-group o al final del header
    idx = c.find("</div>", c.find("btn-group"))
    if idx < 0:
        # Fallback: insertar antes del cierre del header
        idx = c.find("</div>", c.find("<div class=\"d-flex justify-content-between"))
    if idx > 0:
        boton = '''
      <a href="{% url 'recursos:vincular' recurso.slug %}" class="btn btn-sm btn-outline-warning ms-2">
        <i class="fas fa-link"></i> Vincular
      </a>'''
        c = c[:idx] + boton + c[idx:]
        t.write_text(c, encoding="utf-8")
        print(f"[OK] {nombre} → botón Vincular añadido")

# ============================================================
# 6) Recursos asociados en detalle de curso (ya existía, añadimos botón)
# ============================================================
print()
print("[6/6] Botón «Añadir recursos» en cursos/detalle_completo.html")
det = BASE / "core" / "templates" / "core" / "cursos" / "detalle_completo.html"
if det.exists():
    c = det.read_text(encoding="utf-8")
    if "recursos:para_objeto" in c:
        print("[SKIP] ya tenía botón para asignar")
    else:
        # Insertar dentro del bloque de recursos si existe
        if "Recursos del curso" in c:
            patron = re.compile(r"(<i class=\"fas fa-folder-open text-warning\"></i> Recursos del curso[^<]*)")
            m = patron.search(c)
            if m:
                boton = f''' {{{{ curso.recursos.count }}}}
        <a href="{{% url 'recursos:para_objeto' tipo='curso' obj_id=curso.id %}}"
           class="btn btn-sm btn-warning float-end">
          <i class="fas fa-plus"></i> Añadir recursos
        </a>
        <span style="display:none">'''
                c = patron.sub(boton, c, count=1)
                det.write_text(c, encoding="utf-8")
                print("[OK] Botón «Añadir recursos» añadido al detalle del curso")
        else:
            print("[SKIP] detalle_completo.html no tiene bloque Recursos del curso")
else:
    print("[SKIP] no existe detalle_completo.html")

print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  1) E:\\PythonPortable_Django5\\python.exe manage.py makemigrations core")
print("  2) E:\\PythonPortable_Django5\\python.exe manage.py migrate")
print("  3) E:\\PythonPortable_Django5\\python.exe manage.py check")
print("  4) E:\\PythonPortable_Django5\\python.exe manage.py runserver 8001 --noreload")