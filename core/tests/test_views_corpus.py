"""Tests de vistas de corpus."""
import pytest
from django.urls import reverse


class TestIndiceCorpus:
    def test_get_200(self, client, db):
        r = client.get(reverse("corpus_indice"))
        assert r.status_code == 200

    def test_renderiza_html(self, client, db):
        r = client.get(reverse("corpus_indice"))
        contenido = r.content.lower()
        assert b"<html" in contenido or b"<!doctype" in contenido

    def test_muestra_top_palabras(self, client, db):
        r = client.get(reverse("corpus_indice"))
        contenido = r.content.decode("utf-8")
        assert "Top 50 palabras" in contenido

class TestConcordanciaVista:
    def test_get_200_sin_q(self, client, db):
        r = client.get(reverse("corpus_concordancia"))
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "Escribe un termino" in contenido

    def test_con_q_noctem(self, client, db):
        # noctem aparece en etimologia_regla (sin BD)
        r = client.get(reverse("corpus_concordancia"), {"q": "noctem"})
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "noctem" in contenido

    def test_con_q_inexistente(self, client, db):
        r = client.get(reverse("corpus_concordancia"), {"q": "xyzabc123"})
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "Sin resultados" in contenido

class TestFrecuenciasVista:
    def test_get_200(self, client, db):
        r = client.get(reverse("corpus_frecuencias"))
        assert r.status_code == 200

    def test_muestra_secciones(self, client, db):
        r = client.get(reverse("corpus_frecuencias"))
        contenido = r.content.decode("utf-8")
        assert "Top 20 bigramas" in contenido
        assert "Tabla de frecuencias" in contenido