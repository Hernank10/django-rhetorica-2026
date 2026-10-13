from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\base.html")
c = p.read_text(encoding="utf-8")

# 1) Reemplazar el selector por uno con boton
nuevo = '''<li class="nav-item">
                    <form action="{% url 'set_language' %}" method="post" style="display:flex;gap:4px;align-items:center;margin:0;">
                        {% csrf_token %}
                        {% get_current_language as LANGUAGE_CODE %}
                        {% get_available_languages as LANGUAGES %}
                        <select name="language" class="form-select form-select-sm"
                                style="background:rgba(255,255,255,.15);color:#fff;border:1px solid rgba(255,255,255,.3);">
                            {% for code, name in LANGUAGES %}
                                <option value="{{ code }}" {% if code == LANGUAGE_CODE %}selected{% endif %} style="color:#000;">{{ name }}</option>
                            {% endfor %}
                        </select>
                        <button type="submit" class="btn btn-sm btn-light">OK</button>
                        <input type="hidden" name="next" value="{{ request.path }}">
                    </form>
                </li>'''

# Buscar el form actual y reemplazar
pat = re.compile(r'<li class="nav-item dropdown">\s*<form action="\{% url .set_language. %\}".*?</li>', re.DOTALL)
c2, n = pat.subn(nuevo, c)

if n == 0:
    print("[!] No se encontro el selector. Busca manualmente:")
    print("    grep -n 'set_language' core\\templates\\base.html")
else:
    p.write_text(c2, encoding="utf-8")
    print(f"[OK] Selector reemplazado ({n} coincidencia/s)")
    print("     Ahora tiene boton 'OK' explicito en vez de onchange")
