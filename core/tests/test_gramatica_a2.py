"""Tests A2 — Lengua Castellana (Bloques A-G). Self-contained."""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from core.data.tecnicas_a2 import TECNICAS, EJERCICIOS
from core.models_gramatica import TecnicaGramatical, EjercicioGramatical

pytestmark = pytest.mark.django_db


@pytest.fixture
def a2_data():
    for t in TECNICAS:
        TecnicaGramatical.objects.update_or_create(
            numero=t["numero"],
            defaults={k: v for k, v in t.items() if k != "numero"},
        )
    for numero, ejs in EJERCICIOS.items():
        t = TecnicaGramatical.objects.get(numero=numero, modulo="a2")
        for ej in ejs:
            EjercicioGramatical.objects.update_or_create(
                tecnica=t, orden=ej["orden"],
                defaults={"tipo": ej["tipo"], "payload": ej["payload"]},
            )
    yield
    TecnicaGramatical.objects.filter(modulo="a2").delete()


@pytest.fixture
def a2_user():
    U = get_user_model()
    user, _ = U.objects.get_or_create(username="a2_test_user")
    return user


class TestA2Bloques:
    def test_70_tecnicas(self, a2_data):
        assert TecnicaGramatical.objects.filter(modulo="a2").count() == 70

    def test_por_bloque(self, a2_data):
        for letra in ("A", "B", "C", "D", "E", "F", "G"):
            n = TecnicaGramatical.objects.filter(modulo="a2", bloque=letra).count()
            assert n == 10, f"bloque {letra}: {n}"

    def test_rango_501_570(self, a2_data):
        ns = sorted(TecnicaGramatical.objects.filter(modulo="a2").values_list("numero", flat=True))
        assert ns == list(range(501, 571))

    def test_ejercicios(self, a2_data):
        ids = list(TecnicaGramatical.objects.filter(modulo="a2").values_list("id", flat=True))
        assert EjercicioGramatical.objects.filter(tecnica_id__in=ids).count() >= 70

    def test_indice_a2_200(self, a2_data, a2_user):
        client = Client(); client.force_login(a2_user)
        r = client.get("/gramatica/a2/")
        assert r.status_code == 200
        for letra in ("Bloque A", "Bloque B", "Bloque C", "Bloque D", "Bloque E", "Bloque F", "Bloque G"):
            assert letra.encode() in r.content
        assert "Lengua Castellana A2".encode() in r.content
