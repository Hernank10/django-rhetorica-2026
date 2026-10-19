"""Tests de core/services/pos.py. Capa 1: determinista."""
import pytest

from core.services.pos import (
    POS_ES,
    analizar_frase,
    estadisticas_pos,
    modelo_disponible,
)


class TestPosEsMapping:
    def test_17_mapeos(self):
        assert len(POS_ES) == 17

    def test_todos_strings(self):
        for k, v in POS_ES.items():
            assert isinstance(k, str)
            assert isinstance(v, str)

    def test_verbos(self):
        assert POS_ES["VERB"] == "verbo"
        assert POS_ES["AUX"] == "verbo auxiliar"

    def test_sustantivos(self):
        assert POS_ES["NOUN"] == "sustantivo"
        assert POS_ES["PROPN"] == "nombre propio"

    def test_conjunciones(self):
        assert POS_ES["CCONJ"] == "conjuncion coordinante"
        assert POS_ES["SCONJ"] == "conjuncion subordinante"


class TestModeloDisponible:
    def test_retorna_bool(self):
        assert isinstance(modelo_disponible(), bool)

    def test_modelo_inexistente(self):
        assert modelo_disponible("modelo_xyz_no_existe") is False


class TestAnalizarFraseVacia:
    def test_vacio(self):
        r = analizar_frase("")
        assert r["disponible"] is True
        assert r["tokens"] == []
        assert r["oraciones"] == 0

    def test_none(self):
        r = analizar_frase(None)
        assert r["tokens"] == []

    def test_whitespace(self):
        r = analizar_frase("   \n\t  ")
        assert r["tokens"] == []


class TestEstadisticasPos:
    def test_vacio(self):
        assert estadisticas_pos([]) == {}

    def test_simple(self):
        tokens = [
            {"pos_es": "verbo"},
            {"pos_es": "sustantivo"},
            {"pos_es": "verbo"},
            {"pos_es": "verbo"},
        ]
        assert estadisticas_pos(tokens) == {"verbo": 3, "sustantivo": 1}

requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_sm no disponible",
)


@requiere_modelo
class TestAnalizarFraseConModelo:
    def test_frase_simple(self):
        r = analizar_frase("Juan estudia")
        assert r["disponible"] is True
        assert r["error"] is None
        assert len(r["tokens"]) >= 2

    def test_pos_correcto(self):
        r = analizar_frase("Juan estudia")
        por_texto = {t["texto"]: t for t in r["tokens"]}
        assert por_texto["Juan"]["pos"] == "PROPN"
        assert por_texto["estudia"]["pos"] == "VERB"

    def test_dependencia_sujeto(self):
        r = analizar_frase("Juan estudia")
        por_texto = {t["texto"]: t for t in r["tokens"]}
        assert por_texto["Juan"]["dep"] == "nsubj"
        assert por_texto["estudia"]["dep"] == "ROOT"

    def test_lemma_verbo(self):
        r = analizar_frase("Juan esta estudiando")
        lemmas = [t["lemma"] for t in r["tokens"]]
        assert any("estudi" in l for l in lemmas)

    def test_dos_oraciones(self):
        r = analizar_frase("Juan estudia. Maria trabaja.")
        assert r["oraciones"] == 2

    def test_sin_dependencias(self):
        r = analizar_frase("Juan estudia", incluir_dependencias=False)
        for t in r["tokens"]:
            assert t["dep"] == ""
            assert t["head_idx"] == -1

    def test_puntuacion_marcada(self):
        r = analizar_frase("Juan estudia.")
        puntos = [t for t in r["tokens"] if t["es_punct"]]
        assert len(puntos) >= 1

    def test_pos_es_legible(self):
        r = analizar_frase("Juan estudia")
        por_texto = {t["texto"]: t for t in r["tokens"]}
        assert por_texto["Juan"]["pos_es"] == "nombre propio"
        assert por_texto["estudia"]["pos_es"] == "verbo"


@requiere_modelo
class TestIntegracionConCorpus:
    def test_frase_subordinada(self):
        r = analizar_frase("El hombre que vino ayer era mi tio")
        assert r["disponible"] is True
        assert len(r["tokens"]) > 3

    def test_verbos_detectados(self):
        r = analizar_frase("Juan estudia matematicas")
        verbos = [t for t in r["tokens"] if t["pos"] in ("VERB", "AUX")]
        assert len(verbos) >= 1