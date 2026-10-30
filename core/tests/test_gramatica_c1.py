"""Tests C1 — Lengua Castellana Bloque A."""
import pytest
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


class TestC1BloqueA:
    def test_10_tecnicas(self, c1_data):
        assert TecnicaGramatical.objects.filter(modulo="c1").count() == 10

    def test_rango_701_710(self, c1_data):
        ns = sorted(TecnicaGramatical.objects.filter(modulo="c1").values_list("numero", flat=True))
        assert ns == list(range(701, 711))
