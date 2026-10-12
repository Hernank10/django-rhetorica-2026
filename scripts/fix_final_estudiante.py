from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Navbar: core:dashboard_estudiante → estudiante:dashboard
# ============================================================
base = BASE / "core" / "templates" / "core" / "base.html"
c = base.read_text(encoding="utf-8")

# Reemplazo directo del url name (funciona sin importar el HTML alrededor)
veces = c.count("core:dashboard_estudiante")
if veces:
    c = c.replace("{% url 'core:dashboard_estudiante' %}", "{% url 'estudiante:dashboard' %}")
    base.write_text(c, encoding="utf-8")
    print(f"[OK] navbar: {veces} reemplazo(s) core:dashboard_estudiante → estudiante:dashboard")
else:
    if "estudiante:dashboard" in c:
        print("[SKIP] navbar ya apuntaba al panel del estudiante")
    else:
        # Buscar el bloque y mostrarlo
        idx = c.find("dashboard_estudiante")
        print("[!] No hay core:dashboard_estudiante. Muestra:")
        if idx > 0:
            print(c[max(0,idx-200):idx+200])

# ============================================================
# 2) login_view: estudiantes → /estudiante/
# ============================================================
v = BASE / "core" / "views.py"
c = v.read_text(encoding="utf-8")

if 'return redirect("dashboard_estudiante")' in c:
    c = c.replace(
        'return redirect("dashboard_estudiante")',
        'return redirect("estudiante:dashboard")'
    )
    v.write_text(c, encoding="utf-8")
    print("[OK] login_view: estudiantes → /estudiante/")
elif 'return redirect("estudiante:dashboard")' in c:
    print("[SKIP] login_view ya redirige a /estudiante/")
else:
    print("[!] No se encontró el redirect en login_view")

# ============================================================
# 3) Crear template editar_perfil.html
# ============================================================
tpl = BASE / "core" / "templates" / "core" / "editar_perfil.html"
if not tpl.exists():
    tpl.write_text('''{% extends 'base.html' %}
{% load i18n %}
{% block content %}
<div class="container mt-4" style="max-width:700px;">
  <h2 class="mb-4"><i class="fas fa-user-edit"></i> Editar perfil</h2>

  {% if messages %}
    {% for m in messages %}
      <div class="alert alert-{{ m.tags|default:'info' }}">{{ m }}</div>
    {% endfor %}
  {% endif %}

  <form method="post" class="card shadow-sm">
    {% csrf_token %}
    <div class="card-body">
      <div class="mb-3">
        <label class="form-label">Usuario</label>
        <input type="text" class="form-control" value="{{ user.username }}" disabled>
      </div>
      <div class="mb-3">
        <label class="form-label">Nombre</label>
        <input type="text" name="first_name" class="form-control"
               value="{{ user.first_name|default:'' }}">
      </div>
      <div class="mb-3">
        <label class="form-label">Apellido</label>
        <input type="text" name="last_name" class="form-control"
               value="{{ user.last_name|default:'' }}">
      </div>
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input type="email" name="email" class="form-control"
               value="{{ user.email|default:'' }}">
      </div>
    </div>
    <div class="card-footer text-end bg-white">
      <a href="{% url 'perfil_usuario' %}" class="btn btn-secondary">Cancelar</a>
      <button class="btn btn-primary"><i class="fas fa-save"></i> Guardar</button>
    </div>
  </form>
</div>
{% endblock %}
''', encoding="utf-8")
    print("[OK] core/templates/core/editar_perfil.html creado")
else:
    print("[SKIP] editar_perfil.html ya existía")