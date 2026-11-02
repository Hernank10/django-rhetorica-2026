"""Tests de la lectura v2 (indice, detalle, evaluar, progreso)."""
import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from core.models_lectura import (
    EjercicioLectura, TecnicaLectura, Texto,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    U = get_user_model()
    return U.objects.get_or_create(
        username="test_lectura_v2",
        defaults={"email": "test_lectura_v2@test.local", "is_active": True},
    )[0]


@pytest.fixture
def client_logueado(user):
    c = Client()
    c.force_login(user)
    return c


@pytest.fixture
def tecnica_texto_ejercicio():
    tec, _ = TecnicaLectura.objects.get_or_create(
        numero=9999,
        defaults={
            "proceso": "P1", "nivel_mcer": "A1",
            "titulo": "Tecnica test", "teoria": "T", "explicacion": "E",
            "regla": "R", "ejemplo_correcto": "C", "ejemplo_incorrecto": "I",
        },
    )
    texto, _ = Texto.objects.get_or_create(
        titulo="Texto test v2",
        defaults={
            "tipo": "informativo", "nivel_mcer": "A1", "fuente": "",
            "orden": 99, "cuerpo": "Cuerpo de prueba.",
        },
    )
    ej, _ = EjercicioLectura.objects.get_or_create(
        texto=texto, enunciado="Pregunta test",
        defaults={
            "tecnica": tec, "tipo": "multiple_choice",
            "payload": {"opciones": ["A) si", "B) no"], "correcta": "A"},
            "orden": 1,
        },
    )
    return tec, texto, ej


def test_indice_lectura_200(client_logueado):
    assert client_logueado.get("/lectura/").status_code == 200


def test_texto_detalle_200(client_logueado, tecnica_texto_ejercicio):
    _, texto, _ = tecnica_texto_ejercicio
    assert client_logueado.get(f"/lectura/{texto.id}/").status_code == 200


def test_texto_detalle_404(client_logueado):
    assert client_logueado.get("/lectura/99999/").status_code == 404


def test_mi_progreso_lectura_200(client_logueado):
    assert client_logueado.get("/lectura/progreso/").status_code == 200


def test_evaluar_ejercicio_ok(client_logueado, tecnica_texto_ejercicio):
    _, _, ej = tecnica_texto_ejercicio
    payload = json.dumps({"ejercicio_id": ej.id, "respuesta": "A"})
    r = client_logueado.post("/lectura/evaluar/", data=payload, content_type="application/json")
    assert r.status_code == 200
    data = r.json()
    assert data.get("ok") is True
    assert data.get("es_correcta") is True


def test_evaluar_ejercicio_sin_login():
    c = Client()
    r = c.post("/lectura/evaluar/", data="{}", content_type="application/json")
    assert r.status_code in (302, 403)
