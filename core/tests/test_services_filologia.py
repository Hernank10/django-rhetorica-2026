"""Tests de core/services/filologia.py (motor puro, sin BD)."""
from collections import Counter

from core.services._etimos_filologia import ETIMOS
from core.services.filologia import (
    buscar_etimo,
    cadena_evolutiva,
    categorias_disponibles,
)


CATEGORIAS_ESPERADAS = {
    "consonantico",
    "diptongacion",
    "doblete",
    "cognado_ingles",
    "evolucion_curiosa",
}

CLAVES_ETIMO = {
    "latin",
    "es_patrimonial",
    "es_cultismo",
    "en_cognado",
    "regla",
    "ejemplo",
    "categoria",
}


class TestBuscarEtimo:
    def test_vacio(self):
        assert buscar_etimo("") == []

    def test_none(self):
        assert buscar_etimo(None) == []

    def test_sin_match(self):
        assert buscar_etimo("xyzabc") == []

    def test_latin_exacto(self):
        r = buscar_etimo("noctem")
        assert len(r) == 1
        assert r[0]["latin"] == "noctem"

    def test_es_patrimonial(self):
        r = buscar_etimo("noche")
        assert len(r) == 1
        assert r[0]["es_patrimonial"] == "noche"

    def test_es_cultismo(self):
        r = buscar_etimo("nocturno")
        assert len(r) == 1
        assert r[0]["es_cultismo"] == "nocturno"

    def test_en_cognado(self):
        r = buscar_etimo("night")
        assert len(r) == 1
        assert r[0]["en_cognado"] == "night"

    def test_categoria(self):
        r = buscar_etimo("diptongacion")
        assert len(r) == 10
        for e in r:
            assert e["categoria"] == "diptongacion"

    def test_case_insensitive(self):
        assert buscar_etimo("NOCTEM") == buscar_etimo("noctem")
        assert buscar_etimo("Noche") == buscar_etimo("noche")

    def test_sin_acentos(self):
        # "acuatico" esta sin acento en los datos; "acuático" con acento
        # debe encontrar lo mismo via _normalizar
        r_sin = buscar_etimo("acuatico")
        r_con = buscar_etimo("acuático")
        assert len(r_sin) == len(r_con)
        assert len(r_sin) >= 1

    def test_substring(self):
        # "noc" debe matchear noctem (latin + cultismo contienen "noc")
        r = buscar_etimo("noc")
        assert any(e["latin"] == "noctem" for e in r)


class TestCadenaEvolutiva:
    def test_noctem_completo(self):
        r = cadena_evolutiva("noctem")
        assert r is not None
        assert r["latin"] == "noctem"
        assert r["es_patrimonial"] == "noche"
        assert r["es_cultismo"] == "nocturno"
        assert r["en_cognado"] == "night"

    def test_case_insensitive(self):
        r1 = cadena_evolutiva("noctem")
        r2 = cadena_evolutiva("NOCTEM")
        r3 = cadena_evolutiva("Noctem")
        assert r1 == r2 == r3

    def test_inexistente(self):
        assert cadena_evolutiva("xyzabc") is None

    def test_vacio(self):
        assert cadena_evolutiva("") is None

    def test_none(self):
        assert cadena_evolutiva(None) is None


class TestCategoriasDisponibles:
    def test_5_categorias(self):
        assert len(categorias_disponibles()) == 5

    def test_ordenadas(self):
        cats = categorias_disponibles()
        assert cats == sorted(cats)

    def test_categorias_esperadas(self):
        assert set(categorias_disponibles()) == CATEGORIAS_ESPERADAS


class TestIntegridadEtimos:
    def test_50_etimos(self):
        assert len(ETIMOS) == 50

    def test_todos_tienen_7_claves(self):
        for e in ETIMOS:
            assert set(e.keys()) == CLAVES_ETIMO, f"faltan claves en {e.get('latin')}"

    def test_categorias_validas(self):
        for e in ETIMOS:
            assert e["categoria"] in CATEGORIAS_ESPERADAS

    def test_reglas_no_vacias(self):
        for e in ETIMOS:
            assert e["regla"], f"regla vacia en {e['latin']}"

    def test_ejemplos_no_vacios(self):
        for e in ETIMOS:
            assert e["ejemplo"], f"ejemplo vacio en {e['latin']}"

    def test_pares_latin_categoria_unicos(self):
        pares = [(e["latin"], e["categoria"]) for e in ETIMOS]
        assert len(pares) == len(set(pares)), "duplicado latin+categoria"

    def test_distribucion_por_categoria(self):
        dist = Counter(e["categoria"] for e in ETIMOS)
        assert dist["consonantico"] == 15
        assert dist["diptongacion"] == 10
        assert dist["doblete"] == 10
        assert dist["cognado_ingles"] == 10
        assert dist["evolucion_curiosa"] == 5