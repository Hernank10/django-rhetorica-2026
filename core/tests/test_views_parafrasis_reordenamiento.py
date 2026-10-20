"""Tests de core/views_parafrasis_reordenamiento.py (S5.4.2)."""
import json

import pytest
from django.urls import reverse

from core.services.pos import modelo_disponible

requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_md no disponible",
)


class TestReordenarValidation:
    def test_get_method_not_allowed(self, client):
        r = client.get(reverse("parafrasis_reordenar"))
        assert r.status_code == 405

    def test_post_sin_original(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {})
        assert r.status_code == 400
        assert "error" in json.loads(r.content)

    def test_post_original_vacio(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {"original": ""})
        assert r.status_code == 400

    def test_post_original_solo_espacios(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {"original": "   "})
        assert r.status_code == 400


@requiere_modelo
class TestReordenarHappyPath:
    def test_con_obl(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {
            "original": "Juan lee el libro en el parque",
        })
        assert r.status_code == 200
        data = json.loads(r.content)
        assert len(data["sugerencias"]) == 3
        obl = data["sugerencias"][0]
        assert obl["tipo"] == "fronting_obl"
        assert obl["disponible"] is True

    def test_sin_obl(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {
            "original": "Juan lee el libro",
        })
        assert r.status_code == 200
        data = json.loads(r.content)
        obl = data["sugerencias"][0]
        assert obl["esperado"] == ""

    def test_svo_canonico(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {
            "original": "En el parque Juan lee el libro",
        })
        assert r.status_code == 200
        data = json.loads(r.content)
        svo = data["sugerencias"][2]
        assert svo["tipo"] == "svo_canonico"
        assert "Juan" in svo["esperado"]

    def test_constituyentes_presentes(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {
            "original": "Juan lee el libro en el parque",
        })
        data = json.loads(r.content)
        c = data["constituyentes"]
        assert c["disponible"] is True
        assert c["sujeto"] == "Juan"
        assert c["verbo"] == "lee"


@requiere_modelo
class TestReordenarContrato:
    def test_keys_top_level(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {
            "original": "Juan lee el libro",
        })
        data = json.loads(r.content)
        assert "sugerencias" in data
        assert "constituyentes" in data

    def test_keys_por_sugerencia(self, client):
        r = client.post(reverse("parafrasis_reordenar"), {
            "original": "Juan lee el libro en el parque",
        })
        data = json.loads(r.content)
        for sug in data["sugerencias"]:
            for key in ("disponible", "esperado", "razon", "tipo"):
                assert key in sug, f"falta {key} en {sug.get('tipo')}"