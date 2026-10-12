from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Vistas de estadísticas + ranking en views_profesor.py
# ============================================================
vp = BASE / "core" / "views_profesor.py"
c = vp.read_text(encoding="utf-8")

if "def estadisticas_dashboard" not in c:
    nuevas = '''

# ============================================================
# ESTADÍSTICAS Y RANKING
# ============================================================
from django.db.models import Count, Avg, Sum, Q
from datetime import timedelta


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

    # --- Distribución de niveles ---
    niveles = (
        User.objects.filter(groups__name="Estudiante")
        .values("nivel")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    niveles_data = [{"nivel": n["nivel"] or "Sin nivel", "count": n["count"]} for n in niveles]

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
'''
    c = c.rstrip() + "\n" + nuevas
    vp.write_text(c, encoding="utf-8")
    print("[OK] vistas de estadísticas + ranking añadidas")
else:
    print("[SKIP] ya existían")

# ============================================================
# 2) URLs
# ============================================================
up = BASE / "core" / "urls_profesor.py"
c = up.read_text(encoding="utf-8")
if "estadisticas_dashboard" not in c:
    nuevas = """    path('estadisticas/', prof.estadisticas_dashboard, name='estadisticas'),
    path('ranking/', prof.ranking_estudiantes, name='ranking'),
"""
    idx = c.rfind("]")
    c = c[:idx] + nuevas + c[idx:]
    up.write_text(c, encoding="utf-8")
    print("[OK] URLs de estadísticas + ranking añadidas")
else:
    print("[SKIP] URLs ya estaban")

# ============================================================
# 3) Template estadisticas.html con Chart.js
# ============================================================
TPL = BASE / "core" / "templates" / "core" / "profesor"

TPL.joinpath("estadisticas.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="mb-0"><i class="fas fa-chart-line"></i> Estadísticas</h2>
  <a href="{% url 'profesor:ranking' %}" class="btn btn-primary">
    <i class="fas fa-trophy"></i> Ver Ranking
  </a>
</div>

<!-- KPIs -->
<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-primary text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.total_est }}</div>
        <div><i class="fas fa-users"></i> Estudiantes</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-success text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.total_progresos }}</div>
        <div><i class="fas fa-check-circle"></i> Lecciones completadas</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-info text-white">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.total_resp }}</div>
        <div><i class="fas fa-clipboard-list"></i> Respuestas</div>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card shadow-sm border-0 bg-warning text-dark">
      <div class="card-body">
        <div class="fs-2 fw-bold">{{ kpis.tasa_global }}%</div>
        <div><i class="fas fa-percent"></i> Tasa de aciertos</div>
      </div>
    </div>
  </div>
</div>

<!-- Gráficos -->
<div class="row g-3 mb-4">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-chart-bar"></i> Top cursos por inscritos
      </div>
      <div class="card-body">
        <canvas id="chartCursos" height="120"></canvas>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-chart-line"></i> Actividad últimos 30 días
      </div>
      <div class="card-body">
        <canvas id="chartActividad" height="120"></canvas>
      </div>
    </div>
  </div>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-chart-pie"></i> Distribución por nivel
      </div>
      <div class="card-body">
        <canvas id="chartNiveles" height="120"></canvas>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-chart-bar"></i> Promedio por curso
      </div>
      <div class="card-body">
        <canvas id="chartPromedios" height="120"></canvas>
      </div>
    </div>
  </div>
</div>

<!-- Top rankings mini -->
<div class="row g-3">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-trophy"></i> Top 10 por progreso
      </div>
      <ol class="list-group list-group-numbered">
        {% for u in top_por_progreso %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ u.username }}</span>
          <span class="badge bg-primary">{{ u.num_progresos }} lecciones</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin datos</li>
        {% endfor %}
      </ol>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header bg-white fw-bold">
        <i class="fas fa-star"></i> Top 10 por aciertos
      </div>
      <ol class="list-group list-group-numbered">
        {% for u in top_por_aciertos %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ u.username }}</span>
          <span class="badge bg-success">{{ u.correctas }} correctas</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin datos</li>
        {% endfor %}
      </ol>
    </div>
  </div>
</div>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
// Datos
const cursosLabels = [{% for c in cursos_stats %}"{{ c.curso.titulo|escapejs }}"{% if not forloop.last %},{% endif %}{% endfor %}];
const cursosInscritos = [{% for c in cursos_stats %}{{ c.inscritos }}{% if not forloop.last %},{% endif %}{% endfor %}];
const cursosPromedios = [{% for c in cursos_stats %}{{ c.promedio }}{% if not forloop.last %},{% endif %}{% endfor %}];

const actividadLabels = [{% for a in actividad_diaria %}"{{ a.dia }}"{% if not forloop.last %},{% endif %}{% endfor %}];
const actividadData = [{% for a in actividad_diaria %}{{ a.count }}{% if not forloop.last %},{% endif %}{% endfor %}];

const nivelesLabels = [{% for n in niveles_data %}"{{ n.nivel|escapejs }}"{% if not forloop.last %},{% endif %}{% endfor %}];
const nivelesData = [{% for n in niveles_data %}{{ n.count }}{% if not forloop.last %},{% endif %}{% endfor %}];

// Chart 1: Top cursos
new Chart(document.getElementById('chartCursos'), {
  type: 'bar',
  data: {
    labels: cursosLabels,
    datasets: [{
      label: 'Inscritos',
      data: cursosInscritos,
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1,
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } }
  }
});

// Chart 2: Actividad
new Chart(document.getElementById('chartActividad'), {
  type: 'line',
  data: {
    labels: actividadLabels,
    datasets: [{
      label: 'Lecciones completadas',
      data: actividadData,
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      tension: 0.3,
      fill: true,
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } }
  }
});

// Chart 3: Niveles (dona)
new Chart(document.getElementById('chartNiveles'), {
  type: 'doughnut',
  data: {
    labels: nivelesLabels,
    datasets: [{
      data: nivelesData,
      backgroundColor: [
        '#4ade80', '#60a5fa', '#fbbf24', '#f472b6', '#a855f7', '#06b6d4'
      ],
    }]
  },
  options: { responsive: true }
});

// Chart 4: Promedios por curso
new Chart(document.getElementById('chartPromedios'), {
  type: 'bar',
  data: {
    labels: cursosLabels,
    datasets: [{
      label: 'Promedio',
      data: cursosPromedios,
      backgroundColor: 'rgba(255, 159, 64, 0.6)',
      borderColor: 'rgba(255, 159, 64, 1)',
      borderWidth: 1,
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true, max: 100 } }
  }
});
</script>
{% endblock %}
''', encoding="utf-8")
print("[OK] estadisticas.html creado")

# ============================================================
# 4) Template ranking.html
# ============================================================
TPL.joinpath("ranking.html").write_text('''{% extends 'core/profesor/base.html' %}
{% block panel %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="mb-0"><i class="fas fa-trophy"></i> Ranking de Estudiantes</h2>
  <a href="{% url 'profesor:estadisticas' %}" class="btn btn-outline-primary">
    <i class="fas fa-chart-line"></i> Ver Estadísticas
  </a>
</div>

<!-- Filtros -->
<div class="btn-group mb-3" role="group">
  <a href="?orden=progreso" class="btn btn-{% if orden == 'progreso' or not orden %}primary{% else %}outline-primary{% endif %}">
    <i class="fas fa-graduation-cap"></i> Por progreso
  </a>
  <a href="?orden=correctas" class="btn btn-{% if orden == 'correctas' %}primary{% else %}outline-primary{% endif %}">
    <i class="fas fa-check-circle"></i> Por aciertos
  </a>
  <a href="?orden=logros" class="btn btn-{% if orden == 'logros' %}primary{% else %}outline-primary{% endif %}">
    <i class="fas fa-trophy"></i> Por logros
  </a>
  <a href="?orden=certificados" class="btn btn-{% if orden == 'certificados' %}primary{% else %}outline-primary{% endif %}">
    <i class="fas fa-certificate"></i> Por certificados
  </a>
</div>

<div class="table-responsive">
  <table class="table table-hover align-middle">
    <thead class="table-light">
      <tr>
        <th style="width:60px;">#</th>
        <th>Estudiante</th>
        <th class="text-center">Lecciones</th>
        <th class="text-center">Respuestas</th>
        <th class="text-center">Correctas</th>
        <th class="text-center">Tasa</th>
        <th class="text-center">Logros</th>
        <th class="text-center">Certif.</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {% for r in ranking %}
      <tr>
        <td>
          {% if r.pos == 1 %}<span class="badge bg-warning text-dark fs-6">🥇</span>
          {% elif r.pos == 2 %}<span class="badge bg-secondary fs-6">🥈</span>
          {% elif r.pos == 3 %}<span class="badge bg-danger fs-6">🥉</span>
          {% else %}<strong>{{ r.pos }}</strong>{% endif %}
        </td>
        <td>
          <strong>{{ r.user.username }}</strong><br>
          <small class="text-muted">{{ r.user.get_full_name|default:"—" }}</small>
        </td>
        <td class="text-center"><span class="badge bg-primary">{{ r.progresos }}</span></td>
        <td class="text-center">{{ r.respuestas }}</td>
        <td class="text-center"><span class="badge bg-success">{{ r.correctas }}</span></td>
        <td class="text-center">
          {% if r.tasa >= 80 %}<span class="badge bg-success">{{ r.tasa }}%</span>
          {% elif r.tasa >= 50 %}<span class="badge bg-warning text-dark">{{ r.tasa }}%</span>
          {% else %}<span class="badge bg-danger">{{ r.tasa }}%</span>{% endif %}
        </td>
        <td class="text-center"><span class="badge bg-warning text-dark">{{ r.logros }}</span></td>
        <td class="text-center"><span class="badge bg-info text-dark">{{ r.certificados }}</span></td>
        <td>
          <a href="{% url 'profesor:estudiante_detalle' r.user.id %}" class="btn btn-sm btn-outline-primary">
            <i class="fas fa-eye"></i>
          </a>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="9" class="text-center text-muted py-4">Sin datos</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
''', encoding="utf-8")
print("[OK] ranking.html creado")

# ============================================================
# 5) Añadir "Estadísticas" y "Ranking" al menú del sidebar
# ============================================================
base = TPL / "base.html"
c = base.read_text(encoding="utf-8")

if "profesor:estadisticas" not in c:
    nuevas = '''        <a class="list-group-item list-group-item-action {% if '/estadisticas/' in request.path %}active{% endif %}"
           href="{% url 'profesor:estadisticas' %}">
          <i class="fas fa-chart-line"></i> Estadísticas
        </a>
        <a class="list-group-item list-group-item-action {% if '/ranking/' in request.path %}active{% endif %}"
           href="{% url 'profesor:ranking' %}">
          <i class="fas fa-trophy"></i> Ranking
        </a>
'''
    # Insertar antes del cierre del list-group
    idx = c.find("Certificaciones\n        </a>")
    if idx > 0:
        idx2 = c.find("</a>", idx) + len("</a>\n")
        c = c[:idx2] + nuevas + c[idx2:]
        base.write_text(c, encoding="utf-8")
        print("[OK] menú Estadísticas + Ranking añadido")
    else:
        print("[!] No se pudo insertar el menú")
else:
    print("[SKIP] menú ya estaba")