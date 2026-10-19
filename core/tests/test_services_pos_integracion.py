"""Tests de core/services/pos_integracion.py."""
import pytest

from core.services.pos import modelo_disponible
from core.services.pos_integracion import (
    clasificar_que_spacy,
    concordancia_sujeto_verbo,
    evaluar_ejercicio_con_spacy,
    funciones_sintacticas,
)


requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_sm no disponible",
)


class TestConcordanciaVacia:
    def test_vacio(self):
        r = concordancia_sujeto_verbo("")
        assert r["ok"] is True
        assert r["razon"] == "sin analisis"

    def test_none(self):
        r = concordancia_sujeto_verbo(None)
        assert r["ok"] is True


@requiere_modelo
class TestConcordanciaConModelo:
    def test_juan_estudia(self):
        r = concordancia_sujeto_verbo("Juan estudia")
        assert r["ok"] is True
        assert r["sujeto"] == "Juan"
        assert r["verbo"] == "estudia"
        assert r["sujeto_num"] == "Sing"
        assert r["verbo_num"] == "Sing"

    def test_plural_ok(self):
        r = concordancia_sujeto_verbo("Los ninos estudian")
        assert r["ok"] is True
        assert r["sujeto_num"] == "Plur"
        assert r["verbo_num"] == "Plur"

    def test_discordancia(self):
        r = concordancia_sujeto_verbo("Juan estudian")
        assert r["ok"] is False
        assert "Sing" in r["razon"] or "Plur" in r["razon"]

@requiere_modelo
class TestFuncionesSintacticas:
    def test_simple(self):
        r = funciones_sintacticas("Juan lee un libro")
        assert r["disponible"] is True
        assert "Juan" in r["sujeto"]
        assert "lee" in r["verbo"]
        assert "libro" in r["objeto_directo"]

    def test_con_obl(self):
        r = funciones_sintacticas("Juan lee un libro en casa")
        assert r["disponible"] is True
        assert any("casa" in o for o in r["oblicuos"])

    def test_vacio(self):
        r = funciones_sintacticas("")
        assert r["disponible"] is False
        assert r["sujeto"] == []


@requiere_modelo
class TestClasificarQue:
    def test_sustantiva(self):
        r = clasificar_que_spacy("Pienso que debes estudiar mas")
        assert r == "sustantiva"

    def test_adjetiva(self):
        r = clasificar_que_spacy("El hombre que vino ayer era mi tio")
        assert r == "adjetiva"

    def test_sin_que(self):
        r = clasificar_que_spacy("Juan estudia")
        assert r == ""


@requiere_modelo
class TestEvaluarConSpacy:
    def test_aprobado_incluye_concordancia(self):
        r = evaluar_ejercicio_con_spacy(
            "Juan estudia, pero su hermano juega",
            "oracion_coordinada",
        )
        assert r["aprobado"] is True
        assert "concordancia" in r
        assert r["concordancia"]["ok"] is True

    def test_fallido_incluye_concordancia(self):
        r = evaluar_ejercicio_con_spacy("Hola mundo", "oracion_coordinada")
        assert r["aprobado"] is False
        assert "concordancia" in r