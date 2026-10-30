"""Tests C1 — Lengua Castellana Bloque A + resiliencia de tecnica()."""
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
    yield
    TecnicaGramatical.objects.filter(modulo="c1").delete()


@pytest.fixture
def c1_user():
    U = get_user_model()
    user, _ = U.objects.get_or_create(username="c1_test_user")
    return user


class TestC1BloqueA:
    def test_10_tecnicas(self, c1_data):
        assert TecnicaGramatical.objects.filter(modulo="c1").count() == 10

    def test_rango_701_710(self, c1_data):
        ns = sorted(TecnicaGramatical.objects.filter(modulo="c1").values_list("numero", flat=True))
        assert ns == list(range(701, 711))


class TestTecnicaResiliencia:
    """Verifica que tecnica() no rompe en casos límite (sin manipular FKs)."""

    def test_tecnica_sin_login_redirige(self, c1_data):
        """Sin autenticación, @login_required redirige (no 500)."""
        client = Client()
        r = client.get("/gramatica/tecnica/701/")
        assert r.status_code in (302, 403)

    def test_tecnica_con_login_200(self, c1_data, c1_user):
        """Con login, la vista devuelve 200 y renderiza la técnica."""
        client = Client(); client.force_login(c1_user)
        r = client.get("/gramatica/tecnica/701/")
        assert r.status_code == 200
        assert "701".encode() in r.content or "ensayo".encode() in r.content
