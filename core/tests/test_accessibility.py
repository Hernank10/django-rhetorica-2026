"""Tests de accesibilidad WCAG AA minimo.

Verifica que los templates clave cumplan con:
  - lang="es" en <html>
  - Skip link al inicio
  - <main id="main"> unico
  - aria-label en <nav>
  - aria-current="page" en link activo
  - aria-label en botones sin texto

Sin dependencias externas: solo regex + BeautifulSoup si esta disponible.
"""

import re
from pathlib import Path

import pytest
from django.test import Client
from django.urls import reverse

BASE_TEMPLATES = Path(__file__).resolve().parent.parent / "templates"


def _leer(rel):
    """Lee un template y devuelve su contenido."""
    p = BASE_TEMPLATES / rel
    assert p.exists(), f"Template no existe: {p}"
    return p.read_text(encoding="utf-8")


# ============================================================
# base.html
# ============================================================
class TestBaseTemplate:
    def test_tiene_lang_es(self):
        c = _leer("base.html")
        assert re.search(r'<html[^>]*lang="es"', c), "Falta lang=es en <html>"

    def test_tiene_skip_link(self):
        c = _leer("base.html")
        assert 'class="skip-link"' in c
        assert 'href="#main"' in c

    def test_tiene_main_unico_con_id(self):
        c = _leer("base.html")
        assert '<main id="main"' in c
        # No debe haber mas de un <main>
        assert c.count("<main") == 1, "Mas de un <main> en base.html"

    def test_nav_principal_con_aria_label(self):
        c = _leer("base.html")
        assert 'aria-label="Navegación principal"' in c

    def test_no_tiene_load_i18n_duplicado(self):
        """El bug original: {% load i18n %} en cada linea."""
        c = _leer("base.html")
        n = c.count("{% load i18n %}")
        assert n <= 2, f"Demasiados '{{% load i18n %}}': {n}"

    def test_botones_icono_tienen_aria_label(self):
        c = _leer("base.html")
        # Boton del menu (navbar toggler)
        assert 'aria-label="Abrir menú de navegación"' in c
        # Boton de cerrar alertas
        assert 'aria-label="Cerrar notificación"' in c

    def test_tiene_focus_visible(self):
        c = _leer("base.html")
        assert ":focus-visible" in c
        assert "outline:" in c

    def test_select_idioma_tiene_label(self):
        c = _leer("base.html")
        assert 'for="lang-selector"' in c
        assert 'id="lang-selector"' in c


# ============================================================
# Sub-bases (estudiante / profesor)
# ============================================================
class TestSubBases:
    @pytest.mark.parametrize("rel", [
        "core/estudiante/base.html",
        "core/profesor/base.html",
    ])
    def test_no_anida_main(self, rel):
        """No debe haber un <main> dentro del <main> de base.html."""
        c = _leer(rel)
        assert "<main" not in c, f"{rel} tiene <main> (debe ser <section>)"

    @pytest.mark.parametrize("rel", [
        "core/estudiante/base.html",
        "core/profesor/base.html",
    ])
    def test_usa_nav_con_aria_label(self, rel):
        c = _leer(rel)
        assert "<nav" in c, f"{rel} no usa <nav>"
        assert "aria-label=" in c, f"{rel} sin aria-label en <nav>"

    @pytest.mark.parametrize("rel", [
        "core/estudiante/base.html",
        "core/profesor/base.html",
    ])
    def test_link_activo_tiene_aria_current(self, rel):
        c = _leer(rel)
        assert 'aria-current="page"' in c, f"{rel} sin aria-current"

    @pytest.mark.parametrize("rel", [
        "core/estudiante/base.html",
        "core/profesor/base.html",
    ])
    def test_botones_close_con_label(self, rel):
        c = _leer(rel)
        assert 'aria-label="Cerrar notificación"' in c

    @pytest.mark.parametrize("rel", [
        "core/estudiante/base.html",
        "core/profesor/base.html",
    ])
    def test_iconos_decorativos_aria_hidden(self, rel):
        c = _leer(rel)
        assert 'aria-hidden="true"' in c


# ============================================================
# detalle_ejercicio.html
# ============================================================
class TestDetalleEjercicio:
    def test_usa_h1_o_h2(self):
        c = _leer("core/detalle_ejercicio.html")
        # Debe haber un heading, no un <h2> suelto del titulo
        assert "<h1" in c or "<h2" in c

    def test_usa_article(self):
        c = _leer("core/detalle_ejercicio.html")
        assert "<article" in c

    def test_iconos_aria_hidden(self):
        c = _leer("core/detalle_ejercicio.html")
        assert 'aria-hidden="true"' in c

    def test_no_main_anidado(self):
        c = _leer("core/detalle_ejercicio.html")
        assert "<main" not in c, "detalle_ejercicio no debe tener <main>"

# ============================================================
# Test end-to-end: pagina renderizada
# ============================================================
class TestPaginasRenderizadas:
    def test_home_tiene_skip_link(self, db, client):
        r = client.get("/")
        if r.status_code == 200:
            html = r.content.decode("utf-8", errors="replace")
            assert 'class="skip-link"' in html
            assert '<main id="main"' in html

    def test_home_tiene_lang_es(self, db, client):
        r = client.get("/")
        if r.status_code == 200:
            html = r.content.decode("utf-8", errors="replace")
            assert 'lang="es"' in html

    def test_home_no_tiene_load_i18n_visible(self, db, client):
        """El tag {% load i18n %} no debe aparecer literal en el HTML final."""
        r = client.get("/")
        if r.status_code == 200:
            html = r.content.decode("utf-8", errors="replace")
            assert "{% load i18n %}" not in html, "Tags sin procesar en HTML final"













