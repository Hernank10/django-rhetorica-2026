from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\core\base.html")
c = p.read_text(encoding="utf-8")

# Envolver el link "Cursos" del navbar en {% if not user.is_staff %}
import re
pat = re.compile(
    r'(<li class="nav-item">\s*<a class="nav-link[^"]*"\s+href="\{%\s*url\s+\'lista_cursos\'\s*%\}".*?</li>)',
    re.DOTALL
)

def envolver(match):
    return '{% if not user.is_staff %}\n' + match.group(1) + '\n{% endif %}'

c2, n = pat.subn(envolver, c, count=1)
if n:
    p.write_text(c2, encoding="utf-8")
    print(f"[OK] 'Cursos' oculto para staff en navbar ({n} coincidencia)")
else:
    print("[!] No se encontró. Pégame las líneas del navbar")