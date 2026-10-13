from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

# Buscar el link Cursos del navbar (el que apunta a lista_cursos)
# Puede tener cualquier combinación de clases y espacios
patron = re.compile(
    r'<a\s+class="nav-link[^"]*"\s*\n?\s*href="\{%\s*url\s+\'lista_cursos\'\s*%\}">',
    re.DOTALL
)

def reemplazo(m):
    original = m.group(0)
    # Mantener las clases del original
    clase_match = re.search(r'class="([^"]*)"', original)
    clases = clase_match.group(1) if clase_match else "nav-link"
    return (f'<a class="{clases}"\n'
            f'                       href="{{% if user.is_staff %}}{{% url \'profesor:cursos_lista\' %}}{{% else %}}{{% url \'lista_cursos\' %}}{{% endif %}}">')

c2, n = patron.subn(reemplazo, c)

if n:
    p.write_text(c2, encoding="utf-8")
    print(f"[OK] Link 'Cursos' del navbar actualizado ({n} coincidencia/s)")
    # Mostrar el resultado
    idx = c2.find("profesor:cursos_lista")
    if idx > 0:
        print()
        print("=== Link actualizado ===")
        print(c2[idx-250:idx+250])
else:
    print("[!] No se encontró el link. Vamos a ver el navbar:")
    idx = c.find("lista_cursos")
    if idx > 0:
        print(c[max(0, idx-300):idx+300])
