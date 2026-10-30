"""Tests C1 — Lengua Castellana (A-E: 50 técnicas) + resiliencia de tecnica()."""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from core.data.tecnicas_c1 import TECNICAS, EJERCICIOS
from core.models_gramatica import TecnicaGramatical, EjercicioGramatical

pytestmark = pytest.mark.django_db


@pytest.fixture
def c1_data():
    for t in TECNICAS:
        TecnicaGramatical.objects.update_or_create(
            numero=t["numero"],
            defaults={k: v for k, v in t.items() if k != "numero"},
        )
    # Crear también los ejercicios (necesario para test_ejercicios)
    for numero, ejs in EJERCICIOS.items():
        t = TecnicaGramatical.objects.get(numero=numero, modulo="c1")
        for ej in ejs:
            EjercicioGramatical.objects.update_or_create(
                tecnica=t, orden=ej["orden"],
                defaults={"tipo": ej["tipo"], "payload": ej["payload"]},
            )
    yield
    TecnicaGramatical.objects.filter(modulo="c1").delete()


@pytest.fixture
def c1_user():
    U = get_user_model()
    user, _ = U.objects.get_or_create(username="c1_test_user")
    return user


class TestC1BloquesAG:
    def test_70_tecnicas(self, c1_data):
        assert TecnicaGramatical.objects.filter(modulo="c1").count() == 70

    def test_7_bloques(self, c1_data):
        for letra in "ABCDEFG":
            n = TecnicaGramatical.objects.filter(modulo="c1", bloque=letra).count()
            assert n == 10, f"bloque {letra}: {n}"

    def test_rango_701_770(self, c1_data):
        ns = sorted(TecnicaGramatical.objects.filter(modulo="c1").values_list("numero", flat=True))
        assert ns == list(range(701, 771))

    def test_ejercicios(self, c1_data):
        ids = list(TecnicaGramatical.objects.filter(modulo="c1").values_list("id", flat=True))
        assert EjercicioGramatical.objects.filter(tecnica_id__in=ids).count() >= 70

    def test_indice_c1_200(self, c1_data, c1_user):
        client = Client(); client.force_login(c1_user)
        r = client.get("/gramatica/c1/")
        assert r.status_code == 200
        for letra in "ABCDEFG":
            assert f"Bloque {letra}".encode() in r.content
        assert "Lengua Castellana C1".encode() in r.content


class TestTecnicaResiliencia:
    def test_tecnica_sin_login_redirige(self, c1_data):
        client = Client()
        r = client.get("/gramatica/tecnica/701/")
        assert r.status_code in (302, 403)

    def test_tecnica_con_login_200(self, c1_data, c1_user):
        client = Client(); client.force_login(c1_user)
        r = client.get("/gramatica/tecnica/701/")
        assert r.status_code == 200
        assert "701".encode() in r.content or "ensayo".encode() in r.content
