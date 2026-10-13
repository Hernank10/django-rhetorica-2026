from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# Buscar el template del detalle de curso
candidatos = list(BASE.rglob("**/cursos/detalle*.html"))
if not candidatos:
    candidatos = list(BASE.rglob("**/cursos/*.html"))
    candidatos = [p for p in candidatos if "detalle" in p.name.lower() or p.name == "detalle_completo.html"]

print("Candidatos:")
for c in candidatos:
    print(f"  {c.relative_to(BASE)}")

if not candidatos:
    print("[!] No se encontró template de detalle de curso")
    exit(1)

t = candidatos[0]
c = t.read_text(encoding="utf-8")

if "recursos:para_objeto" in c and "curso.recursos" in c:
    print(f"[SKIP] {t.name} ya tiene la sección")
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
      <i class="fas fa-plus"></i> Añadir recursos
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

# Insertar antes del último {% endblock %}
idx = c.rfind("{% endblock %}")
if idx < 0:
    print("[!] No se encontró {% endblock %} en el template")
    exit(1)

c = c[:idx] + bloque + "\n" + c[idx:]
t.write_text(c, encoding="utf-8")
print(f"[OK] Sección 'Recursos del curso' añadida a {t.name}")
print(f"[OK] Ahora tiene:")
print(f"     - {% if curso.recursos.exists %}")
print(f"     - Botón 'Añadir recursos' → recursos:para_objeto")
print(f"     - Grid de recursos con iconos")
