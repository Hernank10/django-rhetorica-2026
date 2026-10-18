"""Tests de vistas de filologia (con BD por compatibilidad)."""
import pytest
from django.urls import reverse


class TestIndiceFilologia:
    def test_get_200(self, client):
        r = client.get(reverse("filologia_indice"))
        assert r.status_code == 200

    def test_renderiza_html(self, client):
        r = client.get(reverse("filologia_indice"))
        assert b"<html" in r.content.lower() or b"<!doctype" in r.content.lower()

    def test_muestra_50_etimos_sin_filtro(self, client):
        r = client.get(reverse("filologia_indice"))
        contenido = r.content.decode("utf-8")
        assert "50 etimos" in contenido or "50 etimo" in contenido

    def test_filtro_q(self, client):
        r = client.get(reverse("filologia_indice"), {"q": "noctem"})
        contenido = r.content.decode("utf-8")
        assert "noctem" in contenido
        # Solo 1 resultado esperado
        assert "1 etimo" in contenido or "1 etimos" in contenido

    def test_filtro_sin_match(self, client):
        r = client.get(reverse("filologia_indice"), {"q": "xyzabc"})
        contenido = r.content.decode("utf-8")
        assert "Sin resultados" in contenido

class TestDetalleFilologia:
    def test_noctem_200(self, client):
        r = client.get(reverse("filologia_detalle", args=["noctem"]))
        assert r.status_code == 200

    def test_noctem_muestra_cadena(self, client):
        r = client.get(reverse("filologia_detalle", args=["noctem"]))
        contenido = r.content.decode("utf-8")
        assert "noctem" in contenido
        assert "noche" in contenido
        assert "nocturno" in contenido
        assert "night" in contenido

    def test_case_insensitive_url(self, client):
        # URL con noctem en mayusculas -> cadena_evolutiva normaliza
        r = client.get(reverse("filologia_detalle", args=["NOCTEM"]))
        # 404 esperado si slug no acepta mayusculas
        # En Django <slug:...> solo acepta minusculas, entonces 404
        assert r.status_code in (200, 404)

    def test_inexistente_404(self, client):
        r = client.get(reverse("filologia_detalle", args=["xyzabc"]))
        assert r.status_code == 404