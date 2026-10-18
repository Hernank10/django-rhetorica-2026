"""Tests de integracion de las 100 tecnicas de redaccion (R4b)."""

import pytest
from django.core.management import call_command
from django.urls import reverse

from core.models import EjercicioLinguistico


@pytest.fixture(scope="module")
def fixtures_cargadas(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command(
            "loaddata",
            "core/fixtures/redaccion_100_tecnicas.json",
            verbosity=0,
        )


class TestTecnicasR4b:
    def test_100_tecnicas_cargadas(self, fixtures_cargadas, db):
        qs = EjercicioLinguistico.objects.filter(
            es_redaccion=True,
            tecnica__startswith="t",
        )
        assert qs.count() == 100

    def test_distribucion_balanceada(self, fixtures_cargadas, db):
        qs = EjercicioLinguistico.objects.filter(
            es_redaccion=True,
            tecnica__startswith="t",
        )
        for tipo in (
            "parrafo_narrativo",
            "parrafo_descriptivo",
            "parrafo_expositivo",
            "parrafo_argumentativo",
        ):
            n = qs.filter(tipo_redaccion=tipo).count()
            assert n == 25, f"{tipo}: esperado 25, obtenido {n}"

    def test_contenido_completo(self, fixtures_cargadas, db):
        qs = EjercicioLinguistico.objects.filter(
            es_redaccion=True,
            tecnica__startswith="t",
        )
        for ej in qs:
            c = ej.contenido
            assert c.get("teoria"), f"{ej.tecnica}: sin teoria"
            assert c.get("ejemplo"), f"{ej.tecnica}: sin ejemplo"
            assert c.get("enunciado"), f"{ej.tecnica}: sin enunciado"
            assert "tipo_redaccion" in c, f"{ej.tecnica}: sin tipo_redaccion en contenido"

    def test_tecnica_slug_unico(self, fixtures_cargadas, db):
        qs = EjercicioLinguistico.objects.filter(
            es_redaccion=True,
            tecnica__startswith="t",
        )
        slugs = list(qs.values_list("tecnica", flat=True))
        assert len(slugs) == len(set(slugs)), "slugs duplicados"

    def test_indice_carga(self, fixtures_cargadas, client):
        r = client.get(reverse("redaccion_indice"))
        assert r.status_code == 200

    def test_primera_tecnica_accesible(self, fixtures_cargadas, client, db):
        url = reverse("redaccion_ejercicio", args=[30001])
        r = client.get(url)
        assert r.status_code == 200
        contenido = r.content.decode("utf-8").lower()
        assert "t001" in contenido or "narrativa" in contenido

    def test_ultima_tecnica_accesible(self, fixtures_cargadas, client, db):
        url = reverse("redaccion_ejercicio", args=[30100])
        r = client.get(url)
        assert r.status_code == 200