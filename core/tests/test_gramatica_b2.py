"""Tests B2 — Lengua Castellana Bloque A."""
import pytest
from core.data.tecnicas_b2 import TECNICAS, EJERCICIOS
from core.models_gramatica import TecnicaGramatical, EjercicioGramatical

pytestmark = pytest.mark.django_db


@pytest.fixture
def b2_data():
    for t in TECNICAS:
        TecnicaGramatical.objects.update_or_create(
            numero=t["numero"],
            defaults={k: v for k, v in t.items() if k != "numero"},
        )
    yield
    TecnicaGramatical.objects.filter(modulo="b2").delete()


class TestB2BloqueA:
    def test_10_tecnicas(self, b2_data):
        assert TecnicaGramatical.objects.filter(modulo="b2").count() == 10

    def test_rango_601_610(self, b2_data):
        ns = sorted(TecnicaGramatical.objects.filter(modulo="b2").values_list("numero", flat=True))
        assert ns == list(range(601, 611))
