"""Tests C2 — Lengua Castellana Bloque A."""
import pytest
from core.data.tecnicas_c2 import TECNICAS, EJERCICIOS
from core.models_gramatica import TecnicaGramatical

pytestmark = pytest.mark.django_db


@pytest.fixture
def c2_data():
    for t in TECNICAS:
        TecnicaGramatical.objects.update_or_create(
            numero=t["numero"],
            defaults={k: v for k, v in t.items() if k != "numero"},
        )
    yield
    TecnicaGramatical.objects.filter(modulo="c2").delete()


class TestC2BloquesAI:
    def test_90_tecnicas(self, c2_data):
        assert TecnicaGramatical.objects.filter(modulo="c2").count() == 90

    def test_9_bloques(self, c2_data):
        for letra in "ABCDEFGHI":
            n = TecnicaGramatical.objects.filter(modulo="c2", bloque=letra).count()
            assert n == 10, f"bloque {letra}: {n}"

    def test_rango_801_890(self, c2_data):
        ns = sorted(TecnicaGramatical.objects.filter(modulo="c2").values_list("numero", flat=True))
        assert ns == list(range(801, 891))
