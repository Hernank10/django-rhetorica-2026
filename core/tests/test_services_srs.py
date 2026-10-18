"""Tests del motor SM-2 puro (sin BD, sin vistas)."""

from datetime import date, timedelta
from types import SimpleNamespace

import pytest

from core.services.srs import aplicar_sm2, intervalo_estimado


HOY = date(2026, 10, 18)


def _make_review(intervalo_dias=0, facilidad=2.5, repeticiones=0):
    """SimpleNamespace con los atributos que SM-2 toca."""
    return SimpleNamespace(
        intervalo_dias=intervalo_dias,
        facilidad=facilidad,
        repeticiones=repeticiones,
        calidad_respuesta=None,
        programada_para=None,
    )


class TestSM2PrimeraRevision:
    """Primera review de una flashcard nueva (reps=0)."""

    def test_calidad_5(self):
        r = _make_review()
        aplicar_sm2(r, calidad=5, hoy=HOY)
        assert r.intervalo_dias == 1
        assert r.repeticiones == 1
        assert r.facilidad == pytest.approx(2.6)
        assert r.programada_para == HOY + timedelta(days=1)
        assert r.calidad_respuesta == 5

    def test_calidad_4(self):
        r = _make_review()
        aplicar_sm2(r, calidad=4, hoy=HOY)
        assert r.intervalo_dias == 1
        assert r.repeticiones == 1
        assert r.facilidad == pytest.approx(2.5)  # sin cambio
        assert r.programada_para == HOY + timedelta(days=1)

    def test_calidad_3(self):
        r = _make_review()
        aplicar_sm2(r, calidad=3, hoy=HOY)
        assert r.intervalo_dias == 1
        assert r.repeticiones == 1
        assert r.facilidad == pytest.approx(2.36)

    def test_calidad_2_resetea(self):
        r = _make_review()
        aplicar_sm2(r, calidad=2, hoy=HOY)
        assert r.intervalo_dias == 1
        assert r.repeticiones == 0  # reset
        assert r.facilidad == pytest.approx(2.18)

    def test_calidad_0_resetea(self):
        r = _make_review()
        aplicar_sm2(r, calidad=0, hoy=HOY)
        assert r.intervalo_dias == 1
        assert r.repeticiones == 0
        assert r.facilidad == pytest.approx(1.7)


class TestSM2SegundaRevision:
    def test_calidad_5_salta_a_6(self):
        r = _make_review(intervalo_dias=1, facilidad=2.6, repeticiones=1)
        aplicar_sm2(r, calidad=5, hoy=HOY)
        assert r.intervalo_dias == 6
        assert r.repeticiones == 2
        assert r.facilidad == pytest.approx(2.7)
        assert r.programada_para == HOY + timedelta(days=6)


class TestSM2TerceraRevision:
    def test_calidad_5_crece_por_facilidad(self):
        r = _make_review(intervalo_dias=6, facilidad=2.7, repeticiones=2)
        aplicar_sm2(r, calidad=5, hoy=HOY)
        assert r.intervalo_dias == round(6 * 2.7)  # 16
        assert r.repeticiones == 3
        assert r.facilidad == pytest.approx(2.8)

    def test_cadena_de_bien_crece_monotonamente(self):
        r = _make_review(intervalo_dias=6, facilidad=2.7, repeticiones=2)
        intervalos = []
        for _ in range(3):
            aplicar_sm2(r, calidad=5, hoy=HOY)
            intervalos.append(r.intervalo_dias)
        assert intervalos[0] < intervalos[1] < intervalos[2]


class TestSM2Reseteo:
    def test_calidad_2_tras_racha_larga(self):
        r = _make_review(intervalo_dias=45, facilidad=2.9, repeticiones=4)
        aplicar_sm2(r, calidad=2, hoy=HOY)
        assert r.intervalo_dias == 1
        assert r.repeticiones == 0
        assert r.programada_para == HOY + timedelta(days=1)

    def test_tras_reseteo_vuelve_a_crecer(self):
        r = _make_review(intervalo_dias=45, facilidad=2.9, repeticiones=4)
        aplicar_sm2(r, calidad=2, hoy=HOY)  # reset
        assert r.repeticiones == 0

        aplicar_sm2(r, calidad=5, hoy=HOY)  # rebuild
        assert r.intervalo_dias == 1
        assert r.repeticiones == 1

        aplicar_sm2(r, calidad=5, hoy=HOY)
        assert r.intervalo_dias == 6
        assert r.repeticiones == 2


class TestFacilidad:
    def test_floor_1_3_no_baja(self):
        r = _make_review(facilidad=1.3)
        aplicar_sm2(r, calidad=0, hoy=HOY)
        assert r.facilidad == 1.3

    def test_no_baja_de_1_3_cuando_deberia(self):
        r = _make_review(facilidad=1.4)
        aplicar_sm2(r, calidad=0, hoy=HOY)
        # 1.4 - 0.8 = 0.6 -> clamp a 1.3
        assert r.facilidad == 1.3

    def test_calidad_4_es_neutro(self):
        for f in (1.5, 2.0, 2.5, 3.0):
            r = _make_review(facilidad=f)
            aplicar_sm2(r, calidad=4, hoy=HOY)
            assert r.facilidad == pytest.approx(f)

    def test_calidad_5_sube_0_1(self):
        r = _make_review(facilidad=2.5)
        aplicar_sm2(r, calidad=5, hoy=HOY)
        assert r.facilidad == pytest.approx(2.6)

    def test_calidad_3_baja_0_14(self):
        r = _make_review(facilidad=2.5)
        aplicar_sm2(r, calidad=3, hoy=HOY)
        assert r.facilidad == pytest.approx(2.36)


class TestValidacion:
    def test_calidad_negativa_raise(self):
        r = _make_review()
        with pytest.raises(ValueError):
            aplicar_sm2(r, calidad=-1, hoy=HOY)

    def test_calidad_mayor_que_5_raise(self):
        r = _make_review()
        with pytest.raises(ValueError):
            aplicar_sm2(r, calidad=6, hoy=HOY)


class TestFechaDefault:
    def test_sin_hoy_usa_localdate(self):
        from django.utils import timezone
        r = _make_review()
        aplicar_sm2(r, calidad=5)  # sin hoy
        esperado = timezone.localdate() + timedelta(days=1)
        assert r.programada_para == esperado


class TestIntervaloEstimado:
    def test_calidad_5_primera(self):
        assert intervalo_estimado(0, 2.5, 0, 5) == 1

    def test_calidad_5_segunda(self):
        assert intervalo_estimado(1, 2.6, 1, 5) == 6

    def test_calidad_5_tercera(self):
        assert intervalo_estimado(6, 2.7, 2, 5) == round(6 * 2.7)

    def test_calidad_baja_resetea(self):
        assert intervalo_estimado(45, 2.9, 4, 2) == 1