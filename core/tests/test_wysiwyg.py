"""Tests del editor WYSIWYG (TinyMCE) en lecciones.

Cubre:
- TinyMCEWidget (core/widgets.py)
- Template del form (core/templates/core/profesor/lecciones/form.html)
- Integracion POST -> sanitizacion -> BD
"""
import pytest
from django import forms

from core.widgets import TinyMCEWidget
from core.models_cursos import Leccion


# ============================================================
# TinyMCEWidget
# ============================================================
class TestTinyMCEWidget:
    def test_instancia_sin_args(self):
        w = TinyMCEWidget()
        assert w is not None

    def test_clase_tinymce_editor(self):
        w = TinyMCEWidget()
        assert "tinymce-editor" in w.attrs.get("class", "")

    def test_tiene_data_profile(self):
        w = TinyMCEWidget()
        assert "data-tinymce-profile" in w.attrs

    def test_profile_default(self):
        w = TinyMCEWidget()
        assert w.attrs["data-tinymce-profile"] == "default"

    def test_profile_custom(self):
        w = TinyMCEWidget(profile="completo")
        assert w.attrs["data-tinymce-profile"] == "completo"

    def test_media_js_contiene_tinymce(self):
        w = TinyMCEWidget()
        media_js = " ".join(w.media._js)
        assert "tinymce" in media_js.lower()

    def test_attrs_custom_se_respetan(self):
        w = TinyMCEWidget(attrs={"placeholder": "Escribe aqui", "rows": 30})
        assert w.attrs["placeholder"] == "Escribe aqui"
        assert w.attrs["rows"] == 30
        # Sigue teniendo la clase
        assert "tinymce-editor" in w.attrs["class"]

    def test_render_produce_textarea(self):
        w = TinyMCEWidget()
        html = w.render("contenido", "<p>Hola</p>")
        assert "<textarea" in html
        assert 'name="contenido"' in html
        assert "tinymce-editor" in html

    def test_render_incluye_valor(self):
        w = TinyMCEWidget()
        html = w.render("contenido", "<p>Test</p>")
        assert "&lt;p&gt;Test&lt;/p&gt;" in html or "<p>Test</p>" in html


# ============================================================
# Template del formulario
# ============================================================
class TestTemplateForm:
    def test_get_form_crear(self, cliente_prof):
        r = cliente_prof.get("/profesor/lecciones/crear/")
        assert r.status_code == 200

    def test_carga_tinymce_cdn(self, cliente_prof):
        r = cliente_prof.get("/profesor/lecciones/crear/")
        html = r.content.decode("utf-8", errors="replace")
        assert "tinymce" in html.lower()

    def test_tiene_id_contenido(self, cliente_prof):
        r = cliente_prof.get("/profesor/lecciones/crear/")
        html = r.content.decode("utf-8", errors="replace")
        assert 'id="id_contenido"' in html

    def test_tiene_init_script(self, cliente_prof):
        r = cliente_prof.get("/profesor/lecciones/crear/")
        html = r.content.decode("utf-8", errors="replace")
        assert "tinymce.init" in html

    def test_tiene_help_text(self, cliente_prof):
        r = cliente_prof.get("/profesor/lecciones/crear/")
        html = r.content.decode("utf-8", errors="replace")
        # El help_text que pusimos
        assert "barra de herramientas" in html.lower() or "formato" in html.lower()


# ============================================================
# Integracion: POST -> sanitizacion -> BD
# ============================================================
PAYLOAD_XSS = """<p>Seguro</p>
<script>alert('XSS1')</script>
<p onclick="alert('XSS2')">peligroso</p>
<a href="javascript:alert('XSS3')">malo</a>
<p style="background: url(javascript:alert(4))">stylemalo</p>
<strong>Negrita OK</strong>
<ul><li>Lista OK</li></ul>
"""


class TestIntegracionLeccionForm:
    def test_post_sin_contenido(self, cliente_prof, modulo):
        titulo = "__WYSIWYG_TEST__ sin contenido"
        Leccion.objects.filter(titulo=titulo).delete()

        r = cliente_prof.post("/profesor/lecciones/crear/", {
            "modulo": str(modulo.id),
            "titulo": titulo,
            "contenido": "",
            "tipo": "lectura",
            "orden": "1",
            "duracion_estimada": "5",
            "puntos": "10",
        })
        assert r.status_code in (200, 302)

        Leccion.objects.filter(titulo=titulo).delete()

    def test_post_guarda_leccion(self, cliente_prof, modulo):
        titulo = "__WYSIWYG_TEST__ guarda"
        Leccion.objects.filter(titulo=titulo).delete()

        cliente_prof.post("/profesor/lecciones/crear/", {
            "modulo": str(modulo.id),
            "titulo": titulo,
            "contenido": "<p>Hola</p>",
            "tipo": "lectura",
            "orden": "1",
            "duracion_estimada": "5",
            "puntos": "10",
        })

        lec = Leccion.objects.filter(titulo=titulo).first()
        assert lec is not None
        assert lec.modulo_id == modulo.id

        Leccion.objects.filter(titulo=titulo).delete()

    def test_post_sanitiza_script(self, cliente_prof, modulo):
        titulo = "__WYSIWYG_TEST__ xss_script"
        Leccion.objects.filter(titulo=titulo).delete()

        cliente_prof.post("/profesor/lecciones/crear/", {
            "modulo": str(modulo.id),
            "titulo": titulo,
            "contenido": PAYLOAD_XSS,
            "tipo": "lectura",
            "orden": "1",
            "duracion_estimada": "5",
            "puntos": "10",
        })

        lec = Leccion.objects.filter(titulo=titulo).first()
        assert lec is not None
        html = lec.contenido
        assert "<script" not in html.lower()
        assert "onclick=" not in html.lower()
        assert "javascript:" not in html.lower()
        assert "style=" not in html.lower()

        Leccion.objects.filter(titulo=titulo).delete()

    def test_post_conserva_html_valido(self, cliente_prof, modulo):
        titulo = "__WYSIWYG_TEST__ valido"
        Leccion.objects.filter(titulo=titulo).delete()

        html_valido = "<p><strong>Negrita</strong></p><ul><li>Item</li></ul>"

        cliente_prof.post("/profesor/lecciones/crear/", {
            "modulo": str(modulo.id),
            "titulo": titulo,
            "contenido": html_valido,
            "tipo": "lectura",
            "orden": "1",
            "duracion_estimada": "5",
            "puntos": "10",
        })

        lec = Leccion.objects.filter(titulo=titulo).first()
        assert lec is not None
        assert "<strong>" in lec.contenido
        assert "<ul>" in lec.contenido
        assert "<li>" in lec.contenido

        Leccion.objects.filter(titulo=titulo).delete()

    def test_post_sanitiza_style(self, cliente_prof, modulo):
        titulo = "__WYSIWYG_TEST__ xss_style"
        Leccion.objects.filter(titulo=titulo).delete()

        payload = '<p style="background: url(javascript:alert(1))">peligro</p>'

        cliente_prof.post("/profesor/lecciones/crear/", {
            "modulo": str(modulo.id),
            "titulo": titulo,
            "contenido": payload,
            "tipo": "lectura",
            "orden": "1",
            "duracion_estimada": "5",
            "puntos": "10",
        })

        lec = Leccion.objects.filter(titulo=titulo).first()
        assert lec is not None
        assert "javascript:" not in lec.contenido.lower()
        assert "style=" not in lec.contenido.lower()

        Leccion.objects.filter(titulo=titulo).delete()