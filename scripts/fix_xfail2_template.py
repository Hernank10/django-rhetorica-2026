"""Fix bug 2: crear template core/cambiar_contrasena.html."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tpl = BASE / "core" / "templates" / "core" / "cambiar_contrasena.html"

if tpl.exists():
    print("[SKIP] Template ya existe")
    exit(0)

contenido = '''{% extends 'base.html' %}
{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-lg-6">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-key"></i> Cambiar Contrasena
                    </h4>
                </div>
                <div class="card-body">

                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}

                    <form method="post">
                        {% csrf_token %}

                        <div class="mb-3">
                            <label for="password_actual" class="form-label">
                                <i class="fas fa-lock"></i> Contrasena actual
                            </label>
                            <input type="password" name="password_actual" id="password_actual"
                                   class="form-control" required autofocus>
                        </div>

                        <div class="mb-3">
                            <label for="password_nueva" class="form-label">
                                <i class="fas fa-lock-open"></i> Nueva contrasena
                            </label>
                            <input type="password" name="password_nueva" id="password_nueva"
                                   class="form-control" required minlength="6">
                            <small class="text-muted">Minimo 6 caracteres</small>
                        </div>

                        <div class="mb-3">
                            <label for="password_confirm" class="form-label">
                                <i class="fas fa-check"></i> Confirmar nueva contrasena
                            </label>
                            <input type="password" name="password_confirm" id="password_confirm"
                                   class="form-control" required minlength="6">
                        </div>

                        <div class="d-flex justify-content-between">
                            <a href="{% url 'perfil_usuario' %}" class="btn btn-outline-secondary">
                                <i class="fas fa-arrow-left"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Guardar cambios
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

tpl.write_text(contenido, encoding="utf-8")
print(f"[OK] Template creado: {tpl.relative_to(BASE)}")
