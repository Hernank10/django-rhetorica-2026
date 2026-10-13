from pathlib import Path
import re
p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\base.html")
c = p.read_text(encoding="utf-8")

nuevo = '''<li class="nav-item">
  <form action="{% url 'set_language' %}" method="post" style="margin:0;">
    {% csrf_token %}
    <input name="next" type="hidden" value="/">
    <select name="language" onchange="this.form.submit();"
            style="background:#fff;color:#000;border:1px solid #ccc;padding:4px 8px;border-radius:4px;">
      {% get_current_language as MI_IDIOMA %}
      {% get_available_languages as IDIOMAS %}
      {% for code, name in IDIOMAS %}
        <option value="{{ code }}"{% if code == MI_IDIOMA %} selected{% endif %}>{{ name }}</option>
      {% endfor %}
    </select>
  </form>
</li>'''

pat = re.compile(
    r'<li class="nav-item[^"]*">\s*<form[^>]*set_language[^>]*>.*?</form>\s*</li>',
    re.DOTALL
)
c2, n = pat.subn(nuevo, c)
p.write_text(c2, encoding="utf-8")
print(f"[OK] Selector simplificado ({n} bloque). next='/' forzado.")
