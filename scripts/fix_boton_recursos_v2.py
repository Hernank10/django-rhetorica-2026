from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

if "recursos:lista" in c:
    print("[SKIP] botón ya estaba")
else:
    # Buscar cualquier <li> que contenga "lista_cursos" o "Cursos"
    # Regex más flexible
    m = re.search(
        r'(<li\s+class="nav-item[^"]*">\s*\n\s*<a\s+[^>]*?(?:lista_cursos|>\s*<i[^>]*></i>\s*Cursos)[^>]*>)',
        c, re.DOTALL
    )
    if not m:
        # Fallback: buscar la palabra "Cursos" y encontrar el <li> que la contiene
        for match in re.finditer(r'Cursos', c):
            ini = c.rfind("<li", 0, match.start())
            if ini > 0 and c.rfind("<li", 0, match.start()) > c.rfind("</li>", 0, match.start()):
                m = type("M", (), {"start": lambda self: ini})()
                break

    if m:
        boton = '''<li class="nav-item">
                        <a class="nav-link {% if '/recursos/' in request.path %}active{% endif %}"
                           href="{% url 'recursos:lista' %}">
                            <i class="fas fa-folder-open"></i> Recursos
                        </a>
                    </li>
                    '''
        c = c[:m.start()] + boton + c[m.start():]
        p.write_text(c, encoding="utf-8")
        print(f"[OK] botón Recursos insertado en línea ~{c[:m.start()].count(chr(10))+1}")
    else:
        print("[!] No se encontró el navbar. Inserta manualmente en core/templates/core/base.html")
        print("   Después de: <ul class=\"navbar-nav ms-auto\">  o  <ul class=\"navbar-nav me-auto\">")
        print("   Pega:      <li class=\"nav-item\"><a class=\"nav-link\" href=\"{% url 'recursos:lista' %}\"><i class=\"fas fa-folder-open\"></i> Recursos</a></li>")
