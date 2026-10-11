from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\base.html")
c = p.read_text(encoding="utf-8")

# selector nuevo, sin variables que colisionen
nuevo = '''<li class="nav-item">
  <form action="{% url 'set_language' %}" method="post" style="display:flex;gap:4px;align-items:center;margin:0;">
    {% csrf_token %}
    <input type="hidden" name="next" value="{{ request.get_full_path }}">
    <select name="language" class="form-select form-select-sm"
            style="background:rgba(255,255,255,.15);color:#fff;border:1px solid rgba(255,255,255,.3);"
            onchange="this.form.submit()">
      {% get_current_language as LANG_ACTUAL %}
      {% get_available_languages as LANGS %}
      {% for code, name in LANGS %}
        <option value="{{ code }}"{% if code == LANG_ACTUAL %} selected{% endif %} style="color:#000;">{{ name }}</option>
      {% endfor %}
    </select>
  </form>
</li>'''

# quitar todo el <li class="nav-item...">...</li> que contenga set_language
patron = re.compile(
    r'<li class="nav-item[^"]*">\s*<form[^>]*set_language[^>]*>.*?</form>\s*</li>',
    re.DOTALL
)
c2, n = patron.subn(nuevo, c)

if n == 0:
    print("[!] No se encontro el <li> del selector. Revisa manualmente:")
    print("    findstr /n \"set_language\" core\\templates\\base.html")
else:
    p.write_text(c2, encoding="utf-8")
    print(f"[OK] Selector reemplazado ({n} bloque)")

# verificacion
c3 = p.read_text(encoding="utf-8")
i = c3.find("set_language")
print("\n--- HTML resultante (extracto) ---")
print(c3[i-100:i+900])