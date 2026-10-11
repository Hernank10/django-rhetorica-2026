from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

# 1) Cambiar el link "Cursos" del navbar para que sea condicional
viejo_cursos = '<a class="nav-link {% if \'cursos\' in request.path %}active{% endif %}" href="{% url \'lista_cursos\' %}">'
nuevo_cursos = '''<a class="nav-link {% if \'cursos\' in request.path or \'/profesor/cursos\' in request.path %}active{% endif %}"
                       href="{% if user.is_staff %}{% url \'profesor:cursos_lista\' %}{% else %}{% url \'lista_cursos\' %}{% endif %}">'''

if viejo_cursos in c:
    c = c.replace(viejo_cursos, nuevo_cursos)
    p.write_text(c, encoding="utf-8")
    print("[OK] link Cursos del navbar ahora es condicional (staff → /profesor/cursos/)")
else:
    # Fallback: buscar por el href y patrón flexible
    import re
    pat = re.compile(
        r'<a\s+class="nav-link[^"]*"\s+href="\{%\s*url\s+\'lista_cursos\'\s*%\}"',
        re.DOTALL
    )
    c2, n = pat.subn(
        '<a class="nav-link {% if \'/profesor/cursos\' in request.path %}active{% endif %}" '
        'href="{% if user.is_staff %}{% url \'profesor:cursos_lista\' %}{% else %}{% url \'lista_cursos\' %}{% endif %}"',
        c
    )
    if n:
        p.write_text(c2, encoding="utf-8")
        print(f"[OK] link Cursos actualizado (fallback, {n} coincidencia/s)")
    else:
        print("[!] No se encontró. Pégame estas líneas del navbar:")
        idx = c.find("lista_cursos")
        if idx > 0:
            print(c[idx-300:idx+200])