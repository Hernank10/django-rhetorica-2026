from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Fix navbar — insertar botón Recursos
# ============================================================
bt = BASE / "core" / "templates" / "core" / "base.html"
c = bt.read_text(encoding="utf-8")

if "recursos:lista" not in c:
    # Buscar el <ul class="navbar-nav me-auto"> o ms-auto
    import re
    # Estrategia 1: insertar antes del <li> de Cursos
    m = re.search(r'(\s*<li\s+class="nav-item">\s*\n\s*<a[^>]*lista_cursos[^>]*>)', c, re.DOTALL)
    if m:
        boton = '''
                    <li class="nav-item">
                        <a class="nav-link {% if '/recursos/' in request.path %}active{% endif %}"
                           href="{% url 'recursos:lista' %}">
                            <i class="fas fa-folder-open"></i> Recursos
                        </a>
                    </li>'''
        c = c[:m.start()] + boton + c[m.start():]
        bt.write_text(c, encoding="utf-8")
        print("[OK] botón Recursos insertado antes de Cursos")
    else:
        # Fallback: insertar después del primer <li> de la navbar
        m2 = re.search(r'(<ul\s+class="navbar-nav\s+me-auto">\s*\n)', c)
        if m2:
            boton = '''                    <li class="nav-item">
                        <a class="nav-link {% if '/recursos/' in request.path %}active{% endif %}"
                           href="{% url 'recursos:lista' %}">
                            <i class="fas fa-folder-open"></i> Recursos
                        </a>
                    </li>
'''
            c = c[:m2.end()] + boton + c[m2.end():]
            bt.write_text(c, encoding="utf-8")
            print("[OK] botón Recursos insertado al inicio del navbar (me-auto)")
        else:
            print("[!] No se pudo insertar automáticamente. Añade manualmente a base.html:")
            print('   <li class="nav-item"><a class="nav-link" href="{% url \'recursos:lista\' %}"><i class="fas fa-folder-open"></i> Recursos</a></li>')
else:
    print("[SKIP] botón Recursos ya estaba")

# ============================================================
# 2) FK Recurso.curso (opcional)
# ============================================================
mp = BASE / "core" / "models.py"
c = mp.read_text(encoding="utf-8")

if "curso = models.ForeignKey" not in c or "recurso" not in c.lower():
    if "class Recurso" in c and "curso = models.ForeignKey" not in c:
        # Insertar la FK dentro de la clase Recurso
        import re
        # Buscar el bloque de la clase Recurso y añadir la FK antes de "creado_en"
        c2 = re.sub(
            r"(class Recurso\(models\.Model\):.*?)(\n    creado_en = models\.DateTimeField)",
            r"\1\n    curso = models.ForeignKey(\n        'core.Curso', on_delete=models.SET_NULL,\n        null=True, blank=True, related_name='recursos',\n    )\2",
            c,
            count=1,
            flags=re.DOTALL,
        )
        if c2 != c:
            mp.write_text(c2, encoding="utf-8")
            print("[OK] FK Recurso.curso añadida a models.py")
        else:
            print("[!] No se pudo añadir FK. Revisa manualmente")

# ============================================================
# 3) Vistas del profesor para recursos
# ============================================================
vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8")

if "def recursos_lista" not in c:
    nuevas = '''

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
'''
    c = c.rstrip() + nuevas
    vp.write_text(c, encoding="utf-8")
    print("[OK] vistas de recursos del profesor añadidas")

# ============================================================
# 4) URLs del profesor
# ============================================================
up = BASE / "core" / "urls_profesor.py"
c = up.read_text(encoding="utf-8")
if "recursos_lista" not in c:
    nuevas = """    path('recursos/', prof.recursos_lista, name='recursos_lista'),
    path('recursos/autovincular/', prof.recursos_autovincular, name='recursos_autovincular'),
    path('recursos/<int:recurso_id>/asignar/', prof.recurso_asignar, name='recurso_asignar'),
"""
    idx = c.rfind("]")
    c = c[:idx] + nuevas + c[idx:]
    up.write_text(c, encoding="utf-8")
    print("[OK] URLs de recursos del profesor añadidas")

# ============================================================
# 5) Templates del profesor
# ============================================================
TPL = BASE / "core" / "templates" / "core" / "profesor" / "recursos"
TPL.mkdir(parents=True, exist_ok=True)

(TPL / "lista.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="mb-0"><i class="fas fa-folder-open text-warning"></i> Recursos</h2>
  <div class="btn-group">
    <a href="{% url 'profesor:recursos_autovincular' %}" class="btn btn-primary">
      <i class="fas fa-magic"></i> Auto-vincular a cursos
    </a>
    <a href="{% url 'recursos:lista' %}" class="btn btn-outline-secondary">
      <i class="fas fa-external-link-alt"></i> Ver galería pública
    </a>
  </div>
</div>

<!-- Filtros -->
<div class="card shadow-sm mb-3">
  <div class="card-body">
    <form method="get" class="row g-2">
      <div class="col-md-3">
        <input type="text" name="q" value="{{ q }}" class="form-control" placeholder="Buscar nombre...">
      </div>
      <div class="col-md-3">
        <select name="curso" class="form-select" onchange="this.form.submit()">
          <option value="">— Todos los cursos —</option>
          {% for c in cursos %}
            <option value="{{ c.id }}" {% if curso_sel == c.id|stringformat:"s" %}selected{% endif %}>{{ c.titulo }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="col-md-3">
        <select name="cat" class="form-select" onchange="this.form.submit()">
          <option value="">— Todas las categorías —</option>
          {% for c in categorias %}
            <option value="{{ c.categoria }}" {% if cat == c.categoria %}selected{% endif %}>{{ c.categoria }} ({{ c.n }})</option>
          {% endfor %}
        </select>
      </div>
      <div class="col-md-3 d-flex gap-2">
        <button class="btn btn-primary flex-grow-1"><i class="fas fa-search"></i> Filtrar</button>
        <a href="{% url 'profesor:recursos_lista' %}" class="btn btn-outline-secondary"><i class="fas fa-times"></i></a>
      </div>
    </form>
  </div>
</div>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th>Recurso</th>
        <th>Categoría</th>
        <th>Ext</th>
        <th>Curso asignado</th>
        <th class="text-end">Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for r in recursos %}
      <tr>
        <td>
          <i class="fas {{ r.icono }}"></i>
          <strong>{{ r.nombre|truncatechars:80 }}</strong><br>
          <small class="text-muted">{{ r.tamaño_legible }}</small>
        </td>
        <td><span class="badge bg-{{ r.color_badge }}">{{ r.categoria }}</span></td>
        <td><span class="badge bg-light text-dark">.{{ r.extension }}</span></td>
        <td>
          {% if r.curso %}
            <span class="badge bg-success">{{ r.curso.titulo }}</span>
          {% else %}
            <span class="text-muted">— sin asignar —</span>
          {% endif %}
        </td>
        <td class="text-end">
          <a href="{% url 'profesor:recurso_asignar' r.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-link"></i>
          </a>
          <a href="{% url 'recursos:ver' r.slug %}" target="_blank" class="btn btn-sm btn-outline-info">
            <i class="fas fa-eye"></i>
          </a>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="5" class="text-center text-muted py-4">Sin recursos</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] profesor/recursos/lista.html")

(TPL / "asignar.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:recursos_lista' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>

<h2 class="mb-4"><i class="fas fa-link"></i> Asignar recurso a curso</h2>

<div class="card shadow-sm mb-4">
  <div class="card-body">
    <div class="d-flex align-items-center">
      <i class="fas {{ recurso.icono }} fa-3x me-3"></i>
      <div>
        <h5 class="mb-1">{{ recurso.nombre }}</h5>
        <small class="text-muted">
          {{ recurso.categoria }} · .{{ recurso.extension }} · {{ recurso.tamaño_legible }}
        </small>
      </div>
    </div>
  </div>
</div>

<form method="post" class="card shadow-sm">
  {% csrf_token %}
  <div class="card-body">
    <label class="form-label">Curso asignado</label>
    <select name="curso" class="form-select">
      <option value="">— Sin asignar —</option>
      {% for c in cursos %}
        <option value="{{ c.id }}" {% if recurso.curso_id == c.id %}selected{% endif %}>
          {{ c.titulo }}
        </option>
      {% endfor %}
    </select>
  </div>
  <div class="card-footer text-end bg-white">
    <a href="{% url 'profesor:recursos_lista' %}" class="btn btn-secondary">Cancelar</a>
    <button class="btn btn-primary"><i class="fas fa-save"></i> Guardar</button>
  </div>
</form>
{% endblock %}
''', encoding="utf-8")
print("[OK] profesor/recursos/asignar.html")

(TPL / "autovincular.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<a href="{% url 'profesor:recursos_lista' %}" class="btn btn-sm btn-outline-secondary mb-3">
  <i class="fas fa-arrow-left"></i> Volver
</a>

<h2 class="mb-4"><i class="fas fa-magic"></i> Auto-vincular recursos</h2>

<div class="alert alert-info">
  <i class="fas fa-info-circle"></i>
  Este proceso asigna automáticamente los recursos a los cursos según palabras clave en el nombre.
  <strong>Solo asigna recursos que aún no tienen curso.</strong>
</div>

<div class="card shadow-sm">
  <div class="card-header bg-white fw-bold">
    Reglas de vinculación
  </div>
  <div class="table-responsive">
    <table class="table table-sm mb-0">
      <thead class="table-light">
        <tr>
          <th>Curso</th>
          <th>Palabras clave</th>
        </tr>
      </thead>
      <tbody>
        {% for c in cursos %}
        <tr>
          <td><strong>{{ c.titulo }}</strong></td>
          <td><small class="text-muted">según temática del curso</small></td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  <div class="card-footer bg-white text-end">
    <form method="post" onsubmit="return confirm('¿Auto-vincular recursos? Esto puede tardar.');">
      {% csrf_token %}
      <button class="btn btn-primary"><i class="fas fa-magic"></i> Ejecutar auto-vinculación</button>
    </form>
  </div>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] profesor/recursos/autovincular.html")

# ============================================================
# 6) Añadir "Recursos" al menú del panel del profesor
# ============================================================
base = BASE / "core" / "templates" / "core" / "profesor" / "base.html"
c = base.read_text(encoding="utf-8")
if "profesor:recursos_lista" not in c:
    nuevas = '''        <a class="list-group-item list-group-item-action {% if '/profesor/recursos/' in request.path %}active{% endif %}"
           href="{% url 'profesor:recursos_lista' %}">
          <i class="fas fa-folder-open"></i> Recursos
        </a>
'''
    # Insertar antes de "Estadísticas"
    idx = c.find("Estadísticas")
    if idx > 0:
        idx2 = c.rfind("<a ", 0, idx)
        c = c[:idx2] + nuevas + c[idx2:]
        base.write_text(c, encoding="utf-8")
        print("[OK] menú Recursos añadido al sidebar del profesor")
    else:
        print("[!] No se encontró punto de inserción")

# ============================================================
# 7) Mostrar recursos del curso en /cursos/<slug>/
# ============================================================
# Añadimos un endpoint que se consulta desde el template con AJAX o
# simplemente mostramos los recursos del curso en el detalle (requiere editar el template)
detalle = BASE / "core" / "templates" / "core" / "cursos" / "detalle_completo.html"
if detalle.exists():
    c = detalle.read_text(encoding="utf-8")
    if "recursos_del_curso" not in c:
        # Añadir al final, antes del último endblock
        bloque = '''
{% if curso.recursos.all %}
<div class="card shadow-sm mt-4">
  <div class="card-header bg-white fw-bold">
    <i class="fas fa-folder-open text-warning"></i> Recursos del curso ({{ curso.recursos.count }})
  </div>
  <div class="card-body">
    <div class="row g-2">
      {% for r in curso.recursos.all %}
      <div class="col-md-4">
        <a href="{% url 'recursos:ver' r.slug %}" class="text-decoration-none">
          <div class="card h-100">
            <div class="card-body py-2">
              <small class="badge bg-{{ r.color_badge }} mb-1">{{ r.categoria }}</small>
              <div class="text-dark small"><i class="fas {{ r.icono }}"></i> {{ r.nombre|truncatechars:55 }}</div>
            </div>
          </div>
        </a>
      </div>
      {% endfor %}
    </div>
  </div>
</div>
{% endif %}
'''
        # Insertar antes del último {% endblock %}
        idx = c.rfind("{% endblock %}")
        if idx > 0:
            c = c[:idx] + bloque + "\n" + c[idx:]
            detalle.write_text(c, encoding="utf-8")
            print("[OK] recursos añadidos a cursos/detalle_completo.html")
        else:
            print("[!] No se encontró {% endblock %} en detalle_completo.html")
    else:
        print("[SKIP] recursos ya estaban en el detalle del curso")
else:
    print("[!] No existe cursos/detalle_completo.html")

print()
print("=" * 60)
print("FASE 2 lista. Ahora ejecuta:")
print("=" * 60)
print("  1) python manage.py makemigrations core")
print("  2) python manage.py migrate")
print("  3) python manage.py check")
print("  4) python manage.py runserver 8001 --noreload")
