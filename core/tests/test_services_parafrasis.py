"""Tests de core/services/parafrasis.py. Parte 1: funciones deterministas."""
import pytest

from core.services.parafrasis import (
    PARTICIPIOS_IRREGULARES,
    SER_FORMAS,
    conjugar_ser,
    participio_verbo,
)


class TestParticipios:
    def test_irregular_escribir(self):
        assert participio_verbo("escribir") == "escrito"

    def test_irregular_hacer(self):
        assert participio_verbo("hacer") == "hecho"

    def test_irregular_ver(self):
        assert participio_verbo("ver") == "visto"

    def test_regular_ar(self):
        assert participio_verbo("hablar") == "hablado"
        assert participio_verbo("estudiar") == "estudiado"

    def test_regular_er(self):
        assert participio_verbo("comer") == "comido"
        assert participio_verbo("beber") == "bebido"

    def test_regular_ir(self):
        assert participio_verbo("vivir") == "vivido"
        assert participio_verbo("salir") == "salido"

    def test_vacio(self):
        assert participio_verbo("") == ""
        assert participio_verbo(None) == ""

    def test_irregulares_dict_poblado(self):
        assert len(PARTICIPIOS_IRREGULARES) >= 15


class TestConjugarSer:
    def test_presente_3s(self):
        assert conjugar_ser("Pres", "3s") == "es"

    def test_presente_1s(self):
        assert conjugar_ser("Pres", "1s") == "soy"

    def test_preterito_3s(self):
        assert conjugar_ser("Past", "3s") == "fue"

    def test_preterito_3p(self):
        assert conjugar_ser("Past", "3p") == "fueron"

    def test_imperfecto_1s(self):
        assert conjugar_ser("Imp", "1s") == "era"

    def test_futuro_3s(self):
        assert conjugar_ser("Fut", "3s") == "sera"

    def test_condicional_1p(self):
        assert conjugar_ser("Cond", "1p") == "seriamos"

    def test_fallback_presente(self):
        # tiempo desconocido -> fallback a presente
        assert conjugar_ser("Xyz", "3s") == "es"

    def test_formas_completas(self):
        for tiempo in ("Pres", "Past", "Imp", "Fut", "Cond"):
            assert tiempo in SER_FORMAS
            assert len(SER_FORMAS[tiempo]) == 6

from core.services.pos import modelo_disponible
from core.services.parafrasis import (
    es_pasiva,
    transformar_a_pasiva,
    transformar_a_activa,
    comparar_features,
    similitud_tokens,
    verificar_parafrasis,
)


requiere_modelo = pytest.mark.skipif(
    not modelo_disponible(),
    reason="es_core_news_md no disponible",
)


@requiere_modelo
class TestEsPasiva:
    def test_activa(self):
        assert es_pasiva("Juan lee el libro") is False

    def test_pasiva_ser_participio(self):
        assert es_pasiva("El libro es leido por Juan") is True

    def test_pasiva_pretérito(self):
        assert es_pasiva("El libro fue escrito por Juan") is True

    def test_sin_modelo(self):
        # sin texto
        assert es_pasiva("") is False
        assert es_pasiva(None) is False


@requiere_modelo
class TestTransformarAPasiva:
    def test_juan_lee_libro(self):
        r = transformar_a_pasiva("Juan lee el libro")
        assert r["disponible"] is True
        assert "libro" in r["esperado"].lower()
        assert "ser" in r["esperado"].lower() or "es" in r["esperado"].lower()
        assert "por" in r["esperado"].lower()
        assert "juan" in r["esperado"].lower()

    def test_falta_objeto(self):
        r = transformar_a_pasiva("Juan corre")
        assert r["disponible"] is True
        assert r["esperado"] == ""
        assert "no se detecta" in r["razon"]

    def test_vacio(self):
        r = transformar_a_pasiva("")
        assert r["disponible"] is False


@requiere_modelo
class TestTransformarAActiva:
    def test_libro_fue_leido(self):
        r = transformar_a_activa("El libro fue leido por Juan")
        assert r["disponible"] is True
        assert r["esperado"] != ""
        assert "juan" in r["esperado"].lower()

    def test_no_es_pasiva(self):
        r = transformar_a_activa("Juan lee el libro")
        assert r["disponible"] is True
        assert r["esperado"] == ""
        assert "no se detecta" in r["razon"]


@requiere_modelo
class TestSimilitud:
    def test_identicos(self):
        s = similitud_tokens("Juan lee el libro", "Juan lee el libro")
        assert s == 1.0

    def test_disimiles(self):
        s = similitud_tokens("Juan lee el libro", "Pedro corre en el parque")
        assert s < 0.3

    def test_vacio(self):
        assert similitud_tokens("", "algo") == 0.0
        assert similitud_tokens("algo", "") == 0.0


@requiere_modelo
class TestVerificarParafrasis:
    def test_aprobado_activa_a_pasiva(self):
        original = "Juan lee el libro"
        parafraseado = "El libro es leido por Juan"
        r = verificar_parafrasis(original, parafraseado, "activa_a_pasiva")
        assert r["aprobado"] is True
        assert "Correcto" in r["feedback"]
        assert r["similitud"] > 0

    def test_rechazo_copia_identica(self):
        texto = "Juan lee el libro"
        r = verificar_parafrasis(texto, texto, "activa_a_pasiva")
        assert r["aprobado"] is False
        assert "identica" in r["feedback"].lower()

    def test_rechazo_sin_features(self):
        r = verificar_parafrasis("Juan lee el libro", "Maria canta", "activa_a_pasiva")
        assert r["aprobado"] is False

    def test_vacio(self):
        r = verificar_parafrasis("", "", "activa_a_pasiva")
        assert r["aprobado"] is False

    def test_estructura_retorno(self):
        r = verificar_parafrasis("Juan lee el libro", "El libro fue leido por Juan", "activa_a_pasiva")
        assert "aprobado" in r
        assert "tipo" in r
        assert "similitud" in r
        assert "features" in r
        assert "feedback" in r
# === Fase 1: tests defensivos (pre-S5.2) ===


class TestParticipioRamasDefensivas:
    """Tests sin modelo: ramas defensivas de participio_verbo."""

    def test_infinitivo_desconocido(self):
        assert participio_verbo("xyz") == "xyz"

    def test_participio_mayusculas(self):
        assert participio_verbo("ESCRIBIR") == "escrito"
        assert participio_verbo("Hablar") == "hablado"


@requiere_modelo
class TestRamasDefensivas:
    """Tests con modelo: ramas defensivas de transformaciones."""

    def test_transformar_a_pasiva_sin_objeto(self):
        r = transformar_a_pasiva("El perro corre")
        assert r["disponible"] is True
        assert r["esperado"] == ""
        assert "no se detecta estructura activa" in r["razon"]

    def test_transformar_a_activa_sin_agente(self):
        r = transformar_a_activa("El libro fue leido")
        assert r["disponible"] is True
        assert r["esperado"] == ""
        assert "no se detecta estructura pasiva" in r["razon"]

    def test_transformar_a_activa_sin_participio(self):
        # "corre" es VERB Fin, no Part -> no hay participio_tok
        r = transformar_a_activa("Juan corre")
        assert r["disponible"] is True
        assert r["esperado"] == ""
        assert "no se detecta verbo principal en participio" in r["razon"]

    def test_es_pasiva_con_haber_ser(self):
        # "ha sido leido" - rama aux ser via token "sido"
        assert es_pasiva("El libro ha sido leido por Juan") is True