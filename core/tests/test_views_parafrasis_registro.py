"""Tests de core/views_parafrasis_registro.py (S5.5.2)."""
import json

from django.urls import reverse


class TestRegistroDemo:
    def test_get_ok(self, client):
        r = client.get(reverse("registro_demo"))
        assert r.status_code == 200

    def test_get_contiene_ids(self, client):
        r = client.get(reverse("registro_demo"))
        c = r.content.decode("utf-8")
        assert 'id="form-registro"' in c
        assert 'id="texto_original"' in c
        assert 'id="texto_parafraseado"' in c
        assert 'id="tipo"' in c
        assert 'id="resultado"' in c

    def test_get_contiene_url_ajax(self, client):
        r = client.get(reverse("registro_demo"))
        c = r.content.decode("utf-8")
        assert "/sintaxis/parafrasis/registro/ajax/" in c

    def test_post_ok(self, client):
        r = client.post(reverse("registro_demo"), {})
        assert r.status_code == 200


class TestRegistroAjaxValidation:
    def test_get_method_not_allowed(self, client):
        r = client.get(reverse("registro_ajax"))
        assert r.status_code == 405

    def test_post_sin_original(self, client):
        r = client.post(reverse("registro_ajax"), {"tipo": "formal_a_coloquial"})
        assert r.status_code == 400
        assert "error" in json.loads(r.content)

    def test_post_tipo_invalido(self, client):
        r = client.post(reverse("registro_ajax"), {
            "original": "Usted tiene dinero",
            "tipo": "xyz",
        })
        assert r.status_code == 400
        assert "error" in json.loads(r.content)


class TestRegistroAjaxHappyPath:
    def test_solo_original(self, client):
        r = client.post(reverse("registro_ajax"), {
            "original": "Usted tiene dinero",
            "tipo": "formal_a_coloquial",
        })
        assert r.status_code == 200
        data = json.loads(r.content)
        assert data["deteccion_original"]["registro"] == "formal"
        assert data["transformacion_sugerida"]["esperado"] == "Vos tiene plata"
        assert "verificacion" not in data

    def test_con_parafraseado_aprobado(self, client):
        r = client.post(reverse("registro_ajax"), {
            "original": "Usted tiene dinero",
            "parafraseado": "Vos tiene plata",
            "tipo": "formal_a_coloquial",
        })
        assert r.status_code == 200
        data = json.loads(r.content)
        assert data["verificacion"]["aprobado"] is True

    def test_contrato_json(self, client):
        r = client.post(reverse("registro_ajax"), {
            "original": "Vos tiene plata",
            "parafraseado": "Usted tiene dinero",
            "tipo": "coloquial_a_formal",
        })
        data = json.loads(r.content)
        for key in ("deteccion_original", "transformacion_sugerida", "verificacion"):
            assert key in data, f"falta {key}"
        for key in ("disponible", "registro", "formal_count", "coloquial_count"):
            assert key in data["deteccion_original"], f"falta {key} en deteccion"
        for key in ("aprobado", "tipo", "feedback", "features"):
            assert key in data["verificacion"], f"falta {key} en verificacion"