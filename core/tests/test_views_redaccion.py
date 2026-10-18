"""Tests de vistas de redaccion (con BD)."""

import pytest
from django.urls import reverse

from core.models import EjercicioLinguistico, EvaluacionRedaccion


@pytest.fixture
def ejercicio_coordinada(db):
    return EjercicioLinguistico.objects.create(
        titulo="Test coordinada adversativa",
        contenido={"enunciado": "Une dos ideas con 'pero'"},
        categoria="redaccion",
        tipo="produccion_libre",
        nivel=2,
        puntos=10,
        es_redaccion=True,
        tipo_redaccion="oracion_coordinada",
        tecnica="coordinada_adversativa",
        idioma="ES",
    )


@pytest.fixture
def ejercicio_no_redaccion(db):
    return EjercicioLinguistico.objects.create(
        titulo="Test normal",
        contenido={},
        categoria="gramatica",
        tipo="multiple_choice",
        nivel=1,
        puntos=5,
        es_redaccion=False,
        idioma="ES",
    )


@pytest.fixture
def usuario(db, django_user_model):
    return django_user_model.objects.create_user(
        username="estudiante_test",
        password="test12345",
        email="test@example.com",
    )


class TestIndiceRedaccion:
    def test_get_200(self, client):
        r = client.get(reverse("redaccion_indice"))
        assert r.status_code == 200

    def test_renderiza_html(self, client):
        r = client.get(reverse("redaccion_indice"))
        html = r.content.lower()
        assert b"<html" in html or b"<!doctype" in html


class TestEjercicioRedaccion:
    def test_get_200(self, client, ejercicio_coordinada):
        url = reverse("redaccion_ejercicio", args=[ejercicio_coordinada.pk])
        r = client.get(url)
        assert r.status_code == 200

    def test_404_si_no_es_redaccion(self, client, ejercicio_no_redaccion):
        url = reverse("redaccion_ejercicio", args=[ejercicio_no_redaccion.pk])
        r = client.get(url)
        assert r.status_code == 404

    def test_404_si_no_existe(self, client, db):
        url = reverse("redaccion_ejercicio", args=[999999])
        r = client.get(url)
        assert r.status_code == 404

    def test_post_sin_login_redirige(self, client, ejercicio_coordinada):
        url = reverse("redaccion_ejercicio", args=[ejercicio_coordinada.pk])
        r = client.post(url, {"texto": "algo"})
        assert r.status_code in (302, 403)
        if r.status_code == 302:
            assert "login" in r.url.lower() or "accounts" in r.url.lower()

    def test_post_con_login_crea_evaluacion(
        self, client, usuario, ejercicio_coordinada
    ):
        client.force_login(usuario)
        url = reverse("redaccion_ejercicio", args=[ejercicio_coordinada.pk])
        texto = "Juan estudia, pero su hermano juega"
        r = client.post(url, {"texto": texto})
        assert r.status_code in (200, 302)
        ev = EvaluacionRedaccion.objects.filter(estudiante=usuario).first()
        assert ev is not None
        assert ev.texto_estudiante == texto
        assert ev.ejercicio_id == ejercicio_coordinada.pk

    def test_post_aprobado(self, client, usuario, ejercicio_coordinada):
        client.force_login(usuario)
        url = reverse("redaccion_ejercicio", args=[ejercicio_coordinada.pk])
        r = client.post(url, {"texto": "Juan estudia, pero su hermano juega"})
        ev = EvaluacionRedaccion.objects.filter(estudiante=usuario).first()
        assert ev is not None
        assert ev.aprobado is True

    def test_post_no_aprobado(self, client, usuario, ejercicio_coordinada):
        client.force_login(usuario)
        url = reverse("redaccion_ejercicio", args=[ejercicio_coordinada.pk])
        r = client.post(url, {"texto": "Juan estudia"})
        ev = EvaluacionRedaccion.objects.filter(estudiante=usuario).first()
        assert ev is not None
        assert ev.aprobado is False