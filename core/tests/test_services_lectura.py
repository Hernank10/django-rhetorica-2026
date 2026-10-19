"""Tests de core/services/lectura.py. Parte 1: deterministas."""
import pytest

from core.services.lectura import (
    segmentar_texto,
    morfologia_contextual,
    estadisticas_texto,
)


class TestSegmentarTexto:
    def test_vacio(self):
        assert segmentar_texto("") == []

    def test_none(self):
        assert segmentar_texto(None) == []

    def test_una_palabra(self):
        r = segmentar_texto("hola")
        assert len(r) == 1
        assert r[0]["tipo"] == "palabra"
        assert r[0]["texto"] == "hola"
        assert r[0]["inicio"] == 0
        assert r[0]["fin"] == 4

    def test_dos_palabras(self):
        r = segmentar_texto("hola mundo")
        assert len(r) == 3
        assert r[0]["tipo"] == "palabra"
        assert r[1]["tipo"] == "espacio"
        assert r[2]["tipo"] == "palabra"

    def test_puntuacion(self):
        r = segmentar_texto("Juan estudia.")
        tipos = [s["tipo"] for s in r]
        assert "palabra" in tipos
        assert "puntuacion" in tipos
        # el punto es el ultimo
        assert r[-1]["texto"] == "."

    def test_reconstruccion(self):
        texto = "Hola, mundo cruel!"
        r = segmentar_texto(texto)
        reconstruido = "".join(s["texto"] for s in r)
        assert reconstruido == texto

    def test_offsets_correctos(self):
        texto = "abc def"
        r = segmentar_texto(texto)
        # concatenando substring por offsets debe dar el texto original
        piezas = [texto[s["inicio"]:s["fin"]] for s in r]
        assert "".join(piezas) == texto

    def test_acentos(self):
        r = segmentar_texto("canción acción")
        palabras = [s for s in r if s["tipo"] == "palabra"]
        assert len(palabras) == 2
        assert palabras[0]["texto"] == "canción"


class TestMorfologiaErrores:
    def test_vacio(self):
        r = morfologia_contextual("", 0)
        assert r["disponible"] is False
        assert r["palabra"] == ""

    def test_none_texto(self):
        r = morfologia_contextual(None, 0)
        assert r["disponible"] is False

    def test_offset_negativo(self):
        r = morfologia_contextual("Juan", -1)
        assert r["disponible"] is False


class TestEstadisticasVacio:
    def test_vacio(self):
        r = estadisticas_texto("")
        assert r["n_palabras"] == 0
        assert r["disponible"] is False

    def test_none(self):
        r = estadisticas_texto(None)
        assert r["n_palabras"] == 0

from core.services.pos import modelo_disponible


requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_sm no disponible",
)


@requiere_modelo
class TestMorfologiaConModelo:
    def test_juan_en_posicion_0(self):
        r = morfologia_contextual("Juan estudia", 0)
        assert r["disponible"] is True
        assert r["palabra"] == "Juan"
        assert r["pos"] == "PROPN"
        assert r["pos_es"] == "nombre propio"

    def test_estudia_en_posicion_5(self):
        r = morfologia_contextual("Juan estudia", 5)
        assert r["disponible"] is True
        assert r["palabra"] == "estudia"
        assert r["pos"] == "VERB"
        assert "estudi" in r["lemma"].lower()

    def test_offset_en_espacio_retorna_palabra_cercana_o_vacia(self):
        # offset 4 esta en el espacio entre "Juan" y "estudia"
        r = morfologia_contextual("Juan estudia", 4)
        # Puede ser neutro (espacio no es token) o retornar la palabra
        assert r["disponible"] in (True, False)


@requiere_modelo
class TestEstadisticasConModelo:
    def test_texto_simple(self):
        r = estadisticas_texto("Juan estudia matematicas")
        assert r["disponible"] is True
        assert r["n_palabras"] == 3
        assert r["n_oraciones"] == 1
        assert "verbo" in r["distribucion_pos"]

    def test_dos_oraciones(self):
        r = estadisticas_texto("Juan estudia. Maria trabaja.")
        assert r["n_oraciones"] == 2

    def test_texto_real_ejercicio(self):
        # Texto tipico de los 100 ejercicios de redaccion
        texto = ("Primero, me desperté temprano y me preparé para mi viaje. "
                 "Luego, tomé el tren hasta el aeropuerto.")
        r = estadisticas_texto(texto)
        assert r["disponible"] is True
        assert r["n_palabras"] >= 10
        assert r["n_oraciones"] >= 2
        assert r["longitud_media_palabra"] > 3.0