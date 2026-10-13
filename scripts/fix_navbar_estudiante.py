from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

# Buscar el link Estudiante (apunta al viejo dashboard_estudiante)
patron = re.compile(
    r'<a\s+class="nav-link[^"]*"\s+href="\{%\s*url\s+\'core:dashboard_estudiante\'\s*%\}">.*?</a>',
    re.DOTALL
)

nuevo = '''<a class="nav-link" href="{% url 'estudiante:dashboard' %}" style="font-weight:700;">
                                    <i class="fas fa-user-graduate"></i> Mi Panel
                                </a>'''

c2, n = patron.subn(nuevo, c)

if n:
    p.write_text(c2, encoding="utf-8")
    print(f"[OK] navbar 'Estudiante' → 'Mi Panel' (/estudiante/) ({n} coincidencia)")
else:
    print("[!] No se encontró el patrón. Pégame estas líneas de base.html:")
    idx = c.find("dashboard_estudiante")
    if idx > 0:
        print(c[max(0,idx-250):idx+250])
