import json
"""Tests de vistas de POS (con BD por corpus)."""
import pytest
from django.urls import reverse

from core.services.pos import modelo_disponible


requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_sm no disponible",
)


class TestDemoVista:
    def test_get_200(self, client):
        r = client.get(reverse("pos_demo"))
        assert r.status_code == 200

    def test_get_muestra_form(self, client):
        r = client.get(reverse("pos_demo"))
        contenido = r.content.decode("utf-8")
        assert "textarea" in contenido.lower() or "Analizar" in contenido

    def test_post_vacio(self, client):
        r = client.post(reverse("pos_demo"), {"texto": ""})
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "Escribe algo" in contenido

    @requiere_modelo
    def test_post_carga_template_con_ajax(self, client):
        # A partir de R2b, el analisis se hace via AJAX.
        # El POST solo renderiza el template con el form + JS.
        r = client.post(reverse("pos_demo"), {"texto": "Juan estudia"})
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        # El template carga el endpoint AJAX y tiene el contenedor de resultado
        assert "/pos/ajax/analizar/" in contenido
        assert 'id="resultado"' in contenido
        assert 'id="texto"' in contenido


class TestCorpusVista:
    def test_get_200(self, client, db):
        r = client.get(reverse("pos_corpus"))
        assert r.status_code == 200

    def test_get_con_stats(self, client, db):
        from core.models import EjercicioLinguistico

        EjercicioLinguistico.objects.create(
            titulo="Test POS",
            contenido={"enunciado": "Juan estudia matematicas"},
            categoria="gramatica",
            tipo="multiple_choice",
            nivel=1,
            puntos=5,
            idioma="ES",
        )
        r = client.get(reverse("pos_corpus"))
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        # Con o sin modelo, debe contener "Analisis POS del corpus"
        assert "Analisis POS" in contenido or "Analisis POS del corpus" in contenido


class TestAnalizarAjax:
    def test_metodo_get_rechazado(self, client, db):
        r = client.get(reverse("pos_analizar_ajax"))
        assert r.status_code == 405

    def test_json_invalido(self, client, db):
        r = client.post(
            reverse("pos_analizar_ajax"),
            data="not json",
            content_type="application/json",
        )
        assert r.status_code == 400
        assert "error" in r.json()

    def test_falta_texto(self, client, db):
        r = client.post(
            reverse("pos_analizar_ajax"),
            data=json.dumps({"texto": ""}),
            content_type="application/json",
        )
        assert r.status_code == 400
        assert "texto" in r.json()["error"]

    def test_texto_muy_largo(self, client, db):
        r = client.post(
            reverse("pos_analizar_ajax"),
            data=json.dumps({"texto": "a" * 1001}),
            content_type="application/json",
        )
        assert r.status_code == 400
        assert "largo" in r.json()["error"]

    def test_ok_estructura_json(self, client, db):
        r = client.post(
            reverse("pos_analizar_ajax"),
            data=json.dumps({"texto": "Juan estudia"}),
            content_type="application/json",
        )
        assert r.status_code == 200
        data = r.json()
        assert "analisis" in data
        assert "stats" in data
        assert "disponible" in data["analisis"]
        assert "tokens" in data["analisis"]

    @requiere_modelo
    def test_ok_con_modelo(self, client, db):
        r = client.post(
            reverse("pos_analizar_ajax"),
            data=json.dumps({"texto": "Juan estudia"}),
            content_type="application/json",
        )
        assert r.status_code == 200
        data = r.json()
        assert data["analisis"]["disponible"] is True
        assert len(data["analisis"]["tokens"]) >= 2
        assert len(data["stats"]) > 0

