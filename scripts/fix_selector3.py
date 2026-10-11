from pathlib import Path
import re
p = Path(r"E:\02_proyectos\django-rhetorica\core\templates\base.html")
c = p.read_text(encoding="utf-8")

# reemplazar todo bloque set_language por uno limpio
nuevo = '''<li class="nav-item">
  <form action="{% url 'set_language' %}" method="post" class="d-flex align-items-center m-0">
    {% csrf_token %}
    <input name="next" type="hidden" value="{{ request.get_full_path }}">
    <select name="language" onchange="this.form.submit()"
            class="form-select form-select-sm"
            style="background:rgba(255,255,255,.15);color:#fff;border:1px solid rgba(255,255,255,.3);min-width:140px;">
      {% get_current_language as MI_IDIOMA %}
      {% get_available_languages as IDIOMAS %}
      {% for code, name in IDIOMAS %}
        <option value="{{ code }}"{% if code == MI_IDIOMA %} selected{% endif %} style="color:#000;">{{ name }}</option>
      {% endfor %}
    </select>
  </form>
</li>'''

pat = re.compile(
    r'<li class="nav-item[^"]*">\s*<form[^>]*set_language[^>]*>.*?</form>\s*</li>',
    re.DOTALL
)
c2, n = pat.subn(nuevo, c)

if n == 0:
    print("[!] No se encontró el bloque selector")
else:
    p.write_text(c2, encoding="utf-8")
    print(f"[OK] Selector reemplazado ({n} bloque)")
    # mostrar resultado
    i = c2.find("set_language")
    print("\n--- Extracto ---")
    print(c2[i-50:i+700])