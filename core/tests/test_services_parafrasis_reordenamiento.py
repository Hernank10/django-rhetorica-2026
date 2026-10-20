"""Tests de core/services/parafrasis_reordenamiento.py."""
import pytest

from core.services.pos import modelo_disponible
from core.services.parafrasis_reordenamiento import (
    detectar_constituyentes,
    reordenar_fronting,
    reordenar_svo_canonico,
    verificar_reordenamiento,
)

requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_md no disponible",
)


@requiere_modelo
class TestDetectarConstituyentes:
    def test_svo_simple(self):
        r = detectar_constituyentes("Juan lee el libro")
        assert r["disponible"] is True
        assert r["sujeto"] == "Juan"
        assert r["verbo"] == "lee"
        assert r["objeto"] == "el libro"

    def test_con_obl(self):
        r = detectar_constituyentes("Juan lee el libro en el parque")
        assert "en el parque" in r["obl"]

    def test_sin_verbo(self):
        r = detectar_constituyentes("El libro rojo")
        assert r["disponible"] is True
        assert r["verbo"] is None
        assert "verbo principal" in r["razon"]

    def test_vacio(self):
        r = detectar_constituyentes("")
        assert r["disponible"] is False


@requiere_modelo
class TestReordenarFronting:
    def test_obl_al_frente(self):
        r = reordenar_fronting("Juan lee el libro en el parque", "obl")
        assert r["disponible"] is True
        assert r["esperado"].startswith("En el parque")
        assert "Juan lee" in r["esperado"]

    def test_advmod_al_frente(self):
        r = reordenar_fronting("el perro come rapidamente", "advmod")
        assert r["disponible"] is True
        assert "rapidamente" in r["esperado"].lower()

    def test_componente_invalido(self):
        r = reordenar_fronting("Juan lee el libro", "xyz")
        assert r["disponible"] is False
        assert "invalido" in r["razon"]

    def test_sin_obl(self):
        r = reordenar_fronting("Juan lee el libro", "obl")
        assert r["disponible"] is True
        assert r["esperado"] == ""
        assert "no se detecta" in r["razon"]

    def test_vacio(self):
        r = reordenar_fronting("", "obl")
        assert r["disponible"] is False

@requiere_modelo
class TestReordenarSvoCanonico:
    def test_obl_fronted(self):
        r = reordenar_svo_canonico("En el parque Juan lee el libro")
        assert r["disponible"] is True
        assert r["esperado"].startswith("Juan")

    def test_sin_objeto(self):
        r = reordenar_svo_canonico("Juan corre")
        assert r["disponible"] is True
        assert r["esperado"] == ""
        assert "no se detectan" in r["razon"]


@requiere_modelo
class TestVerificarReordenamiento:
    def test_valido(self):
        r = verificar_reordenamiento(
            "Juan lee el libro en el parque",
            "En el parque, Juan lee el libro",
        )
        assert r["aprobado"] is True
        assert r["similitud"] >= 0.6

    def test_identicos(self):
        r = verificar_reordenamiento("Juan lee", "Juan lee")
        assert r["aprobado"] is False
        assert "Identicos" in r["feedback"]

    def test_vacio(self):
        r = verificar_reordenamiento("", "")
        assert r["aprobado"] is False

    def test_similitud_baja(self):
        r = verificar_reordenamiento(
            "Juan lee el libro", "Pedro corre en el parque"
        )
        assert r["aprobado"] is False
        assert "Similitud baja" in r["feedback"]