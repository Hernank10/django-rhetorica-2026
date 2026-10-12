"""
Tests de sanitizacion de HTML (core/utils.py).
"""
import pytest

from core.utils import sanitizar_html, sanitizar_texto_plano


# ============================================================
# CASOS MALICIOSOS (deben neutralizarse)
# ============================================================
class TestXSS:
    def test_script_se_elimina(self):
        html = "<p>Antes</p><script>alert(1)</script><p>Despues</p>"
        limpio = sanitizar_html(html)
        assert "<script>" not in limpio
        assert "alert(1)" not in limpio
        assert "<p>Antes</p>" in limpio
        assert "<p>Despues</p>" in limpio

    def test_onerror_se_elimina(self):
        html = '<img src="x" onerror="alert(1)">'
        limpio = sanitizar_html(html)
        assert "onerror" not in limpio
        assert "<img" in limpio

    def test_onclick_se_elimina(self):
        html = '<p onclick="alert(1)">Click</p>'
        limpio = sanitizar_html(html)
        assert "onclick" not in limpio
        assert "Click" in limpio

    def test_javascript_url_se_neutraliza(self):
        html = '<a href="javascript:alert(1)">Click</a>'
        limpio = sanitizar_html(html)
        assert "javascript:" not in limpio

    def test_iframe_se_elimina(self):
        html = '<iframe src="https://evil.com"></iframe>'
        limpio = sanitizar_html(html)
        assert "<iframe" not in limpio

    def test_style_peligroso(self):
        # Atributos style con expresiones raras
        html = '<p style="background: url(javascript:alert(1))">x</p>'
        limpio = sanitizar_html(html)
        assert "javascript" not in limpio.lower()

    def test_object_embed_se_elimina(self):
        html = '<object data="evil.swf"></object><embed src="evil.swf">'
        limpio = sanitizar_html(html)
        assert "<object" not in limpio
        assert "<embed" not in limpio

    def test_svg_con_script(self):
        html = '<svg><script>alert(1)</script></svg>'
        limpio = sanitizar_html(html)
        assert "<svg" not in limpio
        assert "<script>" not in limpio


# ============================================================
# CASOS LEGITIMOS (deben preservarse)
# ============================================================
class TestHTMLValido:
    def test_parrafo(self):
        assert "<p>Hola</p>" in sanitizar_html("<p>Hola</p>")

    def test_negrita_cursiva(self):
        limpio = sanitizar_html("<p><strong>N</strong> <em>C</em></p>")
        assert "<strong>" in limpio
        assert "<em>" in limpio

    def test_listas(self):
        html = "<ul><li>A</li><li>B</li></ul><ol><li>1</li></ol>"
        limpio = sanitizar_html(html)
        assert "<ul>" in limpio
        assert "<ol>" in limpio
        assert "<li>" in limpio

    def test_enlace_https_se_preserva(self):
        html = '<a href="https://example.com">Enlace</a>'
        limpio = sanitizar_html(html)
        assert "https://example.com" in limpio
        assert "<a " in limpio

    def test_imagen_https_se_preserva(self):
        html = '<img src="https://example.com/img.png" alt="foto">'
        limpio = sanitizar_html(html)
        assert "https://example.com/img.png" in limpio
        assert "<img" in limpio

    def test_tabla(self):
        html = "<table><tr><td>A</td><td>B</td></tr></table>"
        limpio = sanitizar_html(html)
        assert "<table>" in limpio
        assert "<td>" in limpio

    def test_titulos_h1_h6(self):
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            html = f"<{tag}>T</{tag}>"
            assert f"<{tag}>" in sanitizar_html(html)

    def test_blockquote_codigo(self):
        html = "<blockquote>Cita</blockquote><pre><code>code</code></pre>"
        limpio = sanitizar_html(html)
        assert "<blockquote>" in limpio
        assert "<pre>" in limpio
        assert "<code>" in limpio

    def test_enlace_mailto(self):
        html = '<a href="mailto:test@example.com">Email</a>'
        assert "mailto:" in sanitizar_html(html)


# ============================================================
# CASOS BORDE
# ============================================================
class TestCasosBorde:
    def test_none_devuelve_string_vacio(self):
        assert sanitizar_html(None) == ""

    def test_vacio_devuelve_string_vacio(self):
        assert sanitizar_html("") == ""

    def test_solo_espacios(self):
        # Segun nh3, texto sin tags se preserva
        resultado = sanitizar_html("   ")
        assert isinstance(resultado, str)

    def test_texto_sin_tags(self):
        assert sanitizar_html("Hola mundo") == "Hola mundo"

    def test_html_anidado(self):
        html = "<div><p><strong><em>Anidado</em></strong></p></div>"
        limpio = sanitizar_html(html)
        assert "Anidado" in limpio
        assert "<strong>" in limpio
        assert "<em>" in limpio


# ============================================================
# sanitizar_texto_plano
# ============================================================
class TestSanitizarTextoPlano:
    def test_quita_todos_los_tags(self):
        assert sanitizar_texto_plano("<p>Hola <strong>mundo</strong></p>") == "Hola mundo"

    def test_none(self):
        assert sanitizar_texto_plano(None) == ""

    def test_vacio(self):
        assert sanitizar_texto_plano("") == ""

    def test_quita_script(self):
        assert "alert" not in sanitizar_texto_plano("<script>alert(1)</script>Texto")

    def test_preserva_texto(self):
        assert sanitizar_texto_plano("<h1>Titulo</h1>") == "Titulo"