from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
t = BASE / "core" / "templates" / "core" / "cursos" / "detalle_completo.html"
c = t.read_text(encoding="utf-8")

if "Recursos del curso" in c and "recursos:para_objeto" in c:
    print("[SKIP] detalle_completo.html ya tiene la seccion completa")
    exit(0)

bloque = """
{# ============================================================ #}
{# RECURSOS DEL CURSO #}
{# ============================================================ #}
{% if curso.recursos.exists %}
<div class="card shadow-sm mt-4">
  <div class="card-header bg-white d-flex justify-content-between align-items-center">
    <span class="fw-bold">
      <i class="fas fa-folder-open text-warning"></i>
      Recursos del curso ({{ curso.recursos.count }})
    </span>
    <a href="{% url 'recursos:para_objeto' tipo='curso' obj_id=curso.id %}"
       class="btn btn-sm btn-warning">
      <i class="fas fa-plus"></i> Anadir recursos
    </a>
  </div>
  <div class="card-body">
    <div class="row g-2">
      {% for r in curso.recursos.all %}
        <div class="col-md-4">
          <a href="{% url 'recursos:ver' r.slug %}" class="text-decoration-none">
            <div class="card h-100">
              <div class="card-body py-2">
                <small class="badge bg-{{ r.color_badge }} mb-1">{{ r.categoria }}</small>
                <div class="text-dark small">
                  <i class="fas {{ r.icono }}"></i>
                  {{ r.nombre|truncatechars:55 }}
                </div>
              </div>
            </div>
          </a>
        </div>
      {% endfor %}
    </div>
  </div>
</div>
{% endif %}
"""

idx = c.rfind("{% endblock %}")
if idx < 0:
    print("[!] No se encontro {% endblock %}")
    exit(1)

c = c[:idx] + bloque + "\n" + c[idx:]
t.write_text(c, encoding="utf-8")
print("[OK] Seccion 'Recursos del curso' insertada en detalle_completo.html")
print("[OK] Tamano final:", len(c), "bytes")
