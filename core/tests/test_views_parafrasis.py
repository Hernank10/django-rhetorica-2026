"""Tests de core/views_parafrasis.py (S5.2)."""
import json

import pytest
from django.urls import reverse

from core.services.pos import modelo_disponible

requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_md no disponible",
)


class TestDemoView:
    def test_get_ok(self, client):
        r = client.get(reverse("parafrasis_demo"))
        assert r.status_code == 200

    def test_get_contiene_url_ajax(self, client):
        r = client.get(reverse("parafrasis_demo"))
        contenido = r.content.decode("utf-8")
        assert "/sintaxis/parafrasis/ajax/" in contenido

    def test_get_contiene_ids(self, client):
        r = client.get(reverse("parafrasis_demo"))
        contenido = r.content.decode("utf-8")
        assert 'id="resultado"' in contenido
        assert 'id="texto_original"' in contenido
        assert 'id="texto_parafraseado"' in contenido
        assert 'id="tipo"' in contenido

    def test_post_ok(self, client):
        r = client.post(reverse("parafrasis_demo"), {})
        assert r.status_code == 200


class TestAjaxValidation:
    def test_get_method_not_allowed(self, client):
        r = client.get(reverse("parafrasis_ajax"))
        assert r.status_code == 405

    def test_post_sin_original(self, client):
        r = client.post(reverse("parafrasis_ajax"),
                        {"parafraseado": "X", "tipo": "activa_a_pasiva"})
        assert r.status_code == 400
        assert "error" in json.loads(r.content)

    def test_post_sin_parafraseado(self, client):
        r = client.post(reverse("parafrasis_ajax"),
                        {"original": "X", "tipo": "activa_a_pasiva"})
        assert r.status_code == 400
        assert "error" in json.loads(r.content)

    def test_post_tipo_invalido(self, client):
        r = client.post(reverse("parafrasis_ajax"),
                        {"original": "X", "parafraseado": "Y", "tipo": "xxx"})
        assert r.status_code == 400
        assert "error" in json.loads(r.content)


@requiere_modelo
class TestAjaxHappyPath:
    def test_activa_a_pasiva(self, client):
        r = client.post(reverse("parafrasis_ajax"), {
            "original": "Juan lee el libro",
            "parafraseado": "El libro es leido por Juan",
            "tipo": "activa_a_pasiva",
        })
        assert r.status_code == 200
        data = json.loads(r.content)
        assert data["aprobado"] is True
        assert "sugerencia" in data
        assert "es_pasiva_original" in data

    def test_pasiva_a_activa(self, client):
        r = client.post(reverse("parafrasis_ajax"), {
            "original": "El libro fue leido por Juan",
            "parafraseado": "Juan lee el libro",
            "tipo": "pasiva_a_activa",
        })
        assert r.status_code == 200
        data = json.loads(r.content)
        assert "aprobado" in data

    def test_copia_identica_rechazada(self, client):
        texto = "Juan lee el libro"
        r = client.post(reverse("parafrasis_ajax"), {
            "original": texto,
            "parafraseado": texto,
            "tipo": "activa_a_pasiva",
        })
        assert r.status_code == 200
        data = json.loads(r.content)
        assert data["aprobado"] is False

    def test_contrato_json_completo(self, client):
        r = client.post(reverse("parafrasis_ajax"), {
            "original": "Juan lee el libro",
            "parafraseado": "El libro es leido por Juan",
            "tipo": "activa_a_pasiva",
        })
        data = json.loads(r.content)
        for clave in ("aprobado", "tipo", "similitud", "features", "feedback",
                      "sugerencia", "es_pasiva_original"):
            assert clave in data, f"falta {clave}"