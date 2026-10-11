from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\profesor\base.html")
c = p.read_text(encoding="utf-8")

if "modulos_lista" not in c:
    # insertar después del enlace de Cursos
    bloque = '''        <a class="list-group-item list-group-item-action {% if '/modulos/' in request.path %}active{% endif %}"
           href="{% url 'profesor:modulos_lista' %}">
          <i class="fas fa-layer-group"></i> Módulos
        </a>
'''
    c = c.replace(
        '''<i class="fas fa-book"></i> Cursos
        </a>
''',
        '''<i class="fas fa-book"></i> Cursos
        </a>
''' + bloque
    )
    p.write_text(c, encoding="utf-8")
    print("[OK] menú Módulos añadido a base.html")
else:
    print("[SKIP] ya estaba")