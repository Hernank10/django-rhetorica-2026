"""Tests del contrato JSON de micro-ejercicios."""
import pytest

from core.schemas.validators import es_valido, validar_microejercicio


class TestValidarMicroejercicio:
    def _valido(self):
        return {
            "tipo_adaptativo": "micro_ejercicio",
            "foco": "declinacion_3_consonantica",
            "enunciado": "Seleccione la forma correcta en ablativo singular:",
            "opciones": ["milite", "militis", "militibus"],
            "respuesta_correcta": "milite",
            "retroalimentacion_adaptativa": "Recuerde la desinencia -e del ablativo.",
        }

    def test_valido(self):
        assert validar_microejercicio(self._valido()) == []
        assert es_valido(self._valido())

    def test_no_dict(self):
        assert validar_microejercicio("no soy dict") != []

    def test_falta_campo_obligatorio(self):
        c = self._valido()
        del c["enunciado"]
        assert any("enunciado" in e for e in validar_microejercicio(c))

    def test_tipo_adaptativo_incorrecto(self):
        c = self._valido()
        c["tipo_adaptativo"] = "otro"
        assert any("tipo_adaptativo" in e for e in validar_microejercicio(c))

    def test_opciones_muy_pocas(self):
        c = self._valido()
        c["opciones"] = ["una sola"]
        assert any("opciones" in e for e in validar_microejercicio(c))

    def test_opciones_duplicadas(self):
        c = self._valido()
        c["opciones"] = ["a", "a", "b"]
        assert any("duplicad" in e for e in validar_microejercicio(c))

    def test_respuesta_no_en_opciones(self):
        c = self._valido()
        c["respuesta_correcta"] = "no-existe"
        assert any("respuesta_correcta" in e for e in validar_microejercicio(c))

    def test_enunciado_muy_corto(self):
        c = self._valido()
        c["enunciado"] = "corto"
        assert any("enunciado" in e for e in validar_microejercicio(c))

    def test_retro_muy_corta(self):
        c = self._valido()
        c["retroalimentacion_adaptativa"] = "corta"
        assert any("retroalimentacion" in e for e in validar_microejercicio(c))