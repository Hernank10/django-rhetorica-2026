from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

# Cambiar el enlace viejo por el nuevo del panel del profesor
viejo = """<a class="nav-link" href="{% url 'core:dashboard_profesor' %}">
                                    <i class="fas fa-chalkboard-teacher"></i> Profesor
                                </a>"""

nuevo = """<a class="nav-link" href="{% url 'profesor:dashboard' %}" style="font-weight:700;">
                                    <i class="fas fa-chalkboard-teacher"></i> Panel Profesor
                                </a>"""

if viejo in c:
    c = c.replace(viejo, nuevo)
    p.write_text(c, encoding="utf-8")
    print("[OK] botón navbar actualizado a profesor:dashboard")
elif "profesor:dashboard" in c:
    print("[SKIP] ya apuntaba al panel nuevo")
else:
    print("[!] No se encontró el patrón exacto. Busca manualmente en core/templates/core/base.html:")
    print("    la línea con 'core:dashboard_profesor'")