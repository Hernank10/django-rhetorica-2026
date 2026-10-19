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
    def test_post_juan_estudia(self, client):
        r = client.post(reverse("pos_demo"), {"texto": "Juan estudia"})
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "Juan" in contenido
        assert "PROPN" in contenido
        assert "nombre propio" in contenido
        assert "VERB" in contenido
        assert "verbo" in contenido


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