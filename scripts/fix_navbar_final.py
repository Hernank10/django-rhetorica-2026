from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

# El bloque actual tiene este aspecto (según la inspección):
# <li class="nav-item">
#     <a class="nav-link" href="{% url 'core:dashboard_profesor' %}">
#         <i class="fas fa-chalkboard-teacher"></i> Profesor
#     </a>
# </li>

viejo = """{% if user.is_staff %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'core:dashboard_profesor' %}">
                                    <i class="fas fa-chalkboard-teacher"></i> Profesor
                                </a>
                            </li>"""

nuevo = """{% if user.is_staff %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'profesor:dashboard' %}"
                                   style="font-weight:700;color:#fff;">
                                    <i class="fas fa-chalkboard-teacher"></i> Panel Profesor
                                </a>
                            </li>"""

if viejo in c:
    c = c.replace(viejo, nuevo)
    p.write_text(c, encoding="utf-8")
    print("[OK] botón navbar actualizado")
elif "profesor:dashboard" in c:
    print("[SKIP] ya apunta al panel nuevo")
else:
    print("[!] Sigue sin coincidir. Pégame estas 5 líneas del base.html:")
    idx = c.find("dashboard_profesor")
    if idx > 0:
        print(c[idx-200:idx+200])
