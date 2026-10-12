"""
FASE 1 - TinyMCE para lecciones.

1) Crea core/widgets.py con TinyMCEWidget (util a futuro)
2) Modifica core/templates/core/profesor/lecciones/form.html:
   - Anade id="id_contenido" al <textarea name="contenido">
   - Anade bloque extra_js con TinyMCE por CDN
"""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) core/widgets.py
# ============================================================
widgets_py = '''"""
Widgets de formulario personalizados.

TinyMCEWidget: textarea que se transforma en editor WYSIWYG.
Requiere que el template cargue TinyMCE via CDN en {% block extra_js %}.
"""
from django import forms


class TinyMCEWidget(forms.Textarea):
    """
    Textarea con atributos para que TinyMCE lo transforme en editor.
    Uso:
        class MiForm(forms.ModelForm):
            class Meta:
                model = MiModelo
                fields = ["contenido"]
                widgets = {"contenido": TinyMCEWidget()}
    """

    def __init__(self, attrs=None, profile="default"):
        default_attrs = {
            "class": "tinymce-editor",
            "rows": 20,
            "cols": 80,
            "data-tinymce-profile": profile,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        js = ("https://cdn.jsdelivr.net/npm/tinymce@7/tinymce.min.js",)
'''

wp = BASE / "core" / "widgets.py"
wp.write_text(widgets_py, encoding="utf-8")
print("[OK] core/widgets.py")

# ============================================================
# 2) Template form.html
# ============================================================
TPL = BASE / "core" / "templates" / "core" / "profesor" / "lecciones" / "form.html"
c = TPL.read_text(encoding="utf-8")

cambios = 0

# 2.1) Asegurar id="id_contenido" en el textarea de contenido
if 'name="contenido"' in c and 'id="id_contenido"' not in c:
    # Caso 1: <textarea name="contenido" ...>
    patron1 = re.compile(r'(<textarea\s+[^>]*name=["\']contenido["\'][^>]*)(>)', re.IGNORECASE)
    def add_id(m):
        return m.group(1) + ' id="id_contenido"' + m.group(2)
    c2, n = patron1.subn(add_id, c, count=1)
    if n:
        c = c2
        cambios += 1
        print('[OK] id="id_contenido" anadido al <textarea name="contenido">')

# 2.2) Asegurar bloque extra_js con TinyMCE
if "tinymce" not in c.lower():
    bloque_js = '''
{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/tinymce@7/tinymce.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function () {
    if (typeof tinymce === "undefined") return;

    var selector = "textarea#id_contenido, textarea[name=contenido], textarea.tinymce-editor";
    if (!document.querySelector(selector)) return;

    tinymce.init({
        selector: selector,
        height: 550,
        menubar: true,
        branding: false,
        promotion: false,
        plugins: [
            "advlist", "autolink", "lists", "link", "image", "charmap",
            "preview", "anchor", "searchreplace", "visualblocks", "code",
            "fullscreen", "insertdatetime", "media", "table", "help",
            "wordcount", "codesample"
        ],
        toolbar: "undo redo | blocks | " +
                 "bold italic forecolor backcolor | " +
                 "alignleft aligncenter alignright alignjustify | " +
                 "bullist numlist outdent indent | " +
                 "link image media table | " +
                 "removeformat code fullscreen preview | help",
        content_style: "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 16px; line-height: 1.6; }",
        language: "es",
        skin: "oxide",
        setup: function (editor) {
            editor.on("change keyup", function () {
                editor.save();
            });
        }
    });
});
</script>
{% endblock %}
'''
    # Insertar antes del ultimo {% endblock %}
    idx = c.rfind("{% endblock %}")
    if idx >= 0:
        c = c[:idx] + bloque_js + "\n" + c[idx:]
        cambios += 1
        print("[OK] Bloque extra_js con TinyMCE insertado")

# 2.3) Si ya habia un bloque extra_js, anadimos TinyMCE dentro
elif "{% block extra_js %}" in c and "tinymce.min.js" not in c:
    bloque = '''
<script src="https://cdn.jsdelivr.net/npm/tinymce@7/tinymce.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function () {
    if (typeof tinymce === "undefined") return;
    var selector = "textarea#id_contenido, textarea[name=contenido], textarea.tinymce-editor";
    if (!document.querySelector(selector)) return;
    tinymce.init({
        selector: selector,
        height: 550,
        branding: false,
        promotion: false,
        plugins: ["advlist", "autolink", "lists", "link", "image", "charmap",
                  "preview", "anchor", "searchreplace", "visualblocks", "code",
                  "fullscreen", "insertdatetime", "media", "table", "help",
                  "wordcount", "codesample"],
        toolbar: "undo redo | blocks | bold italic forecolor backcolor | " +
                 "alignleft aligncenter alignright alignjustify | " +
                 "bullist numlist outdent indent | link image media table | " +
                 "removeformat code fullscreen preview | help",
        language: "es",
        skin: "oxide",
        setup: function (editor) {
            editor.on("change keyup", function () { editor.save(); });
        }
    });
});
</script>
'''
    c = c.replace("{% block extra_js %}", "{% block extra_js %}" + bloque, 1)
    cambios += 1
    print("[OK] TinyMCE insertado dentro del bloque extra_js existente")

# 2.4) Fallback: si el textarea no tenia name="contenido" (raro), avisar
if 'name="contenido"' not in c:
    print("[!] ATENCION: no se encontro name='contenido' en el template. Revisa manualmente.")

if cambios == 0:
    print("[SKIP] No hubo cambios (quizas ya estaba todo)")
else:
    TPL.write_text(c, encoding="utf-8")
    print(f"[OK] {TPL.relative_to(BASE)} actualizado ({cambios} cambios)")

# ============================================================
# 3) Verificacion
# ============================================================
print()
print("=" * 60)
print("VERIFICACION")
print("=" * 60)
c = TPL.read_text(encoding="utf-8")
print(f"  Tiene id_contenido:     {'id=\"id_contenido\"' in c}")
print(f"  Tiene tinymce.min.js:   {'tinymce.min.js' in c}")
print(f"  Tiene tinymce.init:     {'tinymce.init' in c}")
print(f"  Tiene extra_js:         {'{% block extra_js %}' in c}")
print(f"  Tiene name=contenido:   {'name=\"contenido\"' in c}")
print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  E:\\PythonPortable_Django5\\python.exe manage.py check")
print("  E:\\PythonPortable_Django5\\python.exe manage.py runserver 8001 --noreload")