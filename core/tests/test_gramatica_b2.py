"""Tests B2 — Lengua Castellana (B2 completo, 100 técnicas)."""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from core.data.tecnicas_b2 import TECNICAS, EJERCICIOS
from core.models_gramatica import TecnicaGramatical, EjercicioGramatical

pytestmark = pytest.mark.django_db


@pytest.fixture
def b2_data():
    """Carga las 100 técnicas + 100 ejercicios de B2 en la test DB."""
    for t in TECNICAS:
        TecnicaGramatical.objects.update_or_create(
            numero=t["numero"],
            defaults={k: v for k, v in t.items() if k != "numero"},
        )
    for numero, ejs in EJERCICIOS.items():
        t = TecnicaGramatical.objects.get(numero=numero, modulo="b2")
        for ej in ejs:
            EjercicioGramatical.objects.update_or_create(
                tecnica=t, orden=ej["orden"],
                defaults={"tipo": ej["tipo"], "payload": ej["payload"]},
            )
    yield
    TecnicaGramatical.objects.filter(modulo="b2").delete()


@pytest.fixture
def b2_user():
    U = get_user_model()
    user, _ = U.objects.get_or_create(username="b2_test_user")
    return user


class TestB2Completo:
    def test_100_tecnicas(self, b2_data):
        assert TecnicaGramatical.objects.filter(modulo="b2").count() == 100

    def test_10_bloques(self, b2_data):
        for letra in "ABCDEFGHIJ":
            n = TecnicaGramatical.objects.filter(modulo="b2", bloque=letra).count()
            assert n == 10, f"bloque {letra}: {n}"

    def test_rango_601_700(self, b2_data):
        ns = sorted(TecnicaGramatical.objects.filter(modulo="b2").values_list("numero", flat=True))
        assert ns == list(range(601, 701))

    def test_ejercicios(self, b2_data):
        ids = list(TecnicaGramatical.objects.filter(modulo="b2").values_list("id", flat=True))
        assert EjercicioGramatical.objects.filter(tecnica_id__in=ids).count() >= 100

    def test_indice_b2_200(self, b2_data, b2_user):
        client = Client(); client.force_login(b2_user)
        r = client.get("/gramatica/b2/")
        assert r.status_code == 200
        for letra in "ABCDEFGHIJ":
            assert f"Bloque {letra}".encode() in r.content, f"falta bloque {letra}"
        assert "Lengua Castellana B2".encode() in r.content
