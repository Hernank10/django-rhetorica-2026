"""Tests de vistas de lectura asistida."""
import json

import pytest
from django.urls import reverse

from core.models import EjercicioLinguistico
from core.services.pos import modelo_disponible


requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_md no disponible",
)


@pytest.fixture
def texto_ejercicio(db):
    return EjercicioLinguistico.objects.create(
        titulo="Test lectura",
        contenido={
            "ejemplo": "Primero, me desperté temprano y preparé el desayuno. Luego, tomé el tren hacia el aeropuerto. Finalmente, abordé el avión rumbo a mi destino.",
            "enunciado": "Narrar una rutina",
        },
        categoria="redaccion",
        tipo="produccion_libre",
        nivel=2,
        puntos=10,
        es_redaccion=True,
        tipo_redaccion="parrafo_narrativo",
        idioma="ES",
    )


class TestSelectorVista:
    def test_get_200(self, client, db):
        r = client.get(reverse("lectura_selector"))
        assert r.status_code == 200

    def test_muestra_texto_creado(self, client, texto_ejercicio):
        r = client.get(reverse("lectura_selector"))
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert texto_ejercicio.titulo in contenido
        assert "Leer" in contenido


class TestLectorVista:
    def test_get_200(self, client, texto_ejercicio):
        url = reverse("lectura_lector", args=[texto_ejercicio.pk])
        r = client.get(url)
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "Primero" in contenido
        assert "palabra" in contenido.lower()
        assert "data-offset" in contenido

    def test_404_si_no_existe(self, client, db):
        url = reverse("lectura_lector", args=[999999])
        r = client.get(url)
        assert r.status_code == 404

    def test_404_si_no_es_redaccion(self, client, db):
        ej = EjercicioLinguistico.objects.create(
            titulo="No redaccion",
            contenido={},
            categoria="gramatica",
            tipo="multiple_choice",
            nivel=1,
            puntos=5,
            es_redaccion=False,
            idioma="ES",
        )
        url = reverse("lectura_lector", args=[ej.pk])
        r = client.get(url)
        assert r.status_code == 404


class TestMorfologiaAjax:
    def test_metodo_get_rechazado(self, client, db):
        url = reverse("lectura_morfologia_ajax")
        r = client.get(url)
        assert r.status_code == 405

    def test_json_invalido(self, client, db):
        url = reverse("lectura_morfologia_ajax")
        r = client.post(url, data="not json", content_type="application/json")
        assert r.status_code == 400
        assert "error" in r.json()

    def test_falta_texto(self, client, db):
        url = reverse("lectura_morfologia_ajax")
        r = client.post(url, data=json.dumps({"offset": 0}), content_type="application/json")
        assert r.status_code == 400
        assert "texto" in r.json()["error"]

    def test_falta_offset(self, client, db):
        url = reverse("lectura_morfologia_ajax")
        r = client.post(url, data=json.dumps({"texto": "hola"}), content_type="application/json")
        assert r.status_code == 400
        assert "offset" in r.json()["error"]

    def test_offset_fuera_de_rango(self, client, db):
        url = reverse("lectura_morfologia_ajax")
        r = client.post(
            url,
            data=json.dumps({"texto": "hola", "offset": 100}),
            content_type="application/json",
        )
        assert r.status_code == 400
        assert "rango" in r.json()["error"]

    @requiere_modelo
    def test_ok_retorna_morfologia(self, client, db):
        url = reverse("lectura_morfologia_ajax")
        r = client.post(
            url,
            data=json.dumps({"texto": "Juan estudia", "offset": 0}),
            content_type="application/json",
        )
        assert r.status_code == 200
        data = r.json()
        assert data["disponible"] is True
        assert data["palabra"] == "Juan"
        assert data["pos_es"] == "nombre propio"