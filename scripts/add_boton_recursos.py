from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

# 1) Verificar si ya está
if "recursos:lista" in c:
    print("[SKIP] ya estaba el botón Recursos")
    exit()

# 2) Buscar la línea con "lista_cursos" y mostrar alrededor
idx = c.find("lista_cursos")
if idx == -1:
    print("[!] No existe 'lista_cursos' en el navbar. Mostrando las primeras líneas del nav:")
    j = c.find("navbar-nav")
    if j > 0:
        print(c[j:j+2500])
else:
    # Mostrar contexto
    ini = c.rfind("<li", 0, idx)
    fin = c.find("</li>", idx) + len("</li>")
    bloque_actual = c[ini:fin]
    print("=== Bloque actual del navbar (link Cursos) ===")
    print(bloque_actual)
    print()

    # 3) Insertar el botón Recursos ANTES del <li> de Cursos
    boton = '''<li class="nav-item">
                        <a class="nav-link {% if '/recursos/' in request.path %}active{% endif %}"
                           href="{% url 'recursos:lista' %}">
                            <i class="fas fa-folder-open"></i> Recursos
                        </a>
                    </li>
                    '''

    # Insertar antes del inicio del bloque
    c_nuevo = c[:ini] + boton + c[ini:]
    p.write_text(c_nuevo, encoding="utf-8")
    print(f"[OK] Botón 'Recursos' insertado en línea ~{c[:ini].count(chr(10))+1}")