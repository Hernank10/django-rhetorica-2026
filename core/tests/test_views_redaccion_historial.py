"""Tests de la vista de historial de redaccion."""

import pytest
from django.urls import reverse

from core.models import EjercicioLinguistico, EvaluacionRedaccion


@pytest.fixture
def usuario(db, django_user_model):
    return django_user_model.objects.create_user(
        username="hist_test", password="x", email="h@h.cl"
    )


@pytest.fixture
def otro_usuario(db, django_user_model):
    return django_user_model.objects.create_user(
        username="otro", password="x", email="o@o.cl"
    )


@pytest.fixture
def ejercicio(db):
    return EjercicioLinguistico.objects.create(
        titulo="Ej hist",
        contenido={},
        categoria="redaccion",
        tipo="produccion_libre",
        nivel=2,
        puntos=10,
        es_redaccion=True,
        tipo_redaccion="oracion_coordinada",
        idioma="ES",
    )


class TestHistorialRedaccion:
    def test_sin_login_redirige(self, client, db):
        r = client.get(reverse("redaccion_historial"))
        assert r.status_code == 302
        assert "login" in r.url

    def test_vacio_muestra_mensaje(self, client, usuario):
        client.force_login(usuario)
        r = client.get(reverse("redaccion_historial"))
        assert r.status_code == 200
        html = r.content.lower()
        assert b"historial" in html
        assert "aún no" in r.content.decode("utf-8").lower() or \
               "aun no" in r.content.decode("utf-8").lower()

    def test_lista_evaluaciones_propias(
        self, client, usuario, otro_usuario, ejercicio
    ):
        EvaluacionRedaccion.objects.create(
            estudiante=usuario, ejercicio=ejercicio,
            texto_estudiante="x", aprobado=True, feedback="mia",
        )
        EvaluacionRedaccion.objects.create(
            estudiante=otro_usuario, ejercicio=ejercicio,
            texto_estudiante="y", aprobado=True, feedback="ajena",
        )
        client.force_login(usuario)
        r = client.get(reverse("redaccion_historial"))
        contenido = r.content.decode("utf-8")
        assert "mia" in contenido
        assert "ajena" not in contenido

    def test_ordering_descendente(
        self, client, usuario, ejercicio
    ):
        EvaluacionRedaccion.objects.create(
            estudiante=usuario, ejercicio=ejercicio,
            texto_estudiante="vieja", aprobado=False, feedback="vieja",
        )
        EvaluacionRedaccion.objects.create(
            estudiante=usuario, ejercicio=ejercicio,
            texto_estudiante="nueva", aprobado=True, feedback="nueva",
        )
        client.force_login(usuario)
        r = client.get(reverse("redaccion_historial"))
        contenido = r.content.decode("utf-8")
        assert contenido.index("nueva") < contenido.index("vieja")

    def test_muestra_estado_aprobado(
        self, client, usuario, ejercicio
    ):
        EvaluacionRedaccion.objects.create(
            estudiante=usuario, ejercicio=ejercicio,
            texto_estudiante="ok", aprobado=True, feedback="bien",
        )
        client.force_login(usuario)
        r = client.get(reverse("redaccion_historial"))
        assert b"Aprobado" in r.content

    def test_muestra_estado_reprobado(
        self, client, usuario, ejercicio
    ):
        EvaluacionRedaccion.objects.create(
            estudiante=usuario, ejercicio=ejercicio,
            texto_estudiante="mal", aprobado=False, feedback="mal",
        )
        client.force_login(usuario)
        r = client.get(reverse("redaccion_historial"))
        assert b"No aprobado" in r.content