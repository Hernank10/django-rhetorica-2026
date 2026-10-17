"""Tests de core/services/redaccion.py (sin BD)."""

from core.services.redaccion import (
    analizar_oracion,
    analizar_parrafo,
    clasificar_error,
    evaluar_ejercicio,
)


class TestAnalizarOracion:
    def test_vacia(self):
        assert analizar_oracion("")["tipo"] == "insuficiente"

    def test_corta(self):
        assert analizar_oracion("hola que")["tipo"] == "insuficiente"

    def test_simple(self):
        r = analizar_oracion("Juan estudia matematicas en su casa")
        assert r["tipo"] == "simple"
        assert r["conectores"] == []

    def test_coordinada_pero(self):
        r = analizar_oracion("Juan estudia, pero su hermano juega")
        assert r["tipo"] == "compuesta_coordinada"
        assert any(c["texto"] == "pero" for c in r["conectores"])

    def test_coordinada_y(self):
        r = analizar_oracion("Juan corre y Maria nada todos los dias")
        assert r["tipo"] == "compuesta_coordinada"

    def test_subordinada_porque(self):
        r = analizar_oracion("Juan se fue porque estaba cansado")
        assert r["tipo"] == "compuesta_subordinada"

    def test_subordinada_adjetiva(self):
        r = analizar_oracion("El hombre que vino ayer era mi tio")
        assert r["tipo"] == "compuesta_subordinada"
        tipos = [s["tipo"] for s in r["subordinadas"]]
        assert "adjetiva" in tipos

    def test_subordinada_sustantiva(self):
        r = analizar_oracion("Pienso que debes estudiar mas")
        tipos = [s["tipo"] for s in r["subordinadas"]]
        assert "sustantiva" in tipos

    def test_muy_larga(self):
        r = analizar_oracion("palabra " * 600)
        assert r["tipo"] == "demasiado_largo"


class TestAnalizarParrafo:
    def test_vacio(self):
        assert analizar_parrafo("")["tipo_dominante"] == "vacio"

    def test_narrativo(self):
        r = analizar_parrafo(
            "Primero fuimos al parque. Luego regresamos. Despues cenamos."
        )
        assert r["tipo_dominante"] == "narrativos"

    def test_argumentativo(self):
        r = analizar_parrafo(
            "Es malo porque perjudica. Por lo tanto, debe revisarse. En consecuencia, la rechazo."
        )
        assert r["tipo_dominante"] == "argumentativos"

    def test_expositivo(self):
        r = analizar_parrafo(
            "La gravedad consiste en una fuerza. Por ejemplo atrae. Esto significa que la masa importa."
        )
        assert r["tipo_dominante"] == "expositivos"

    def test_neutro(self):
        r = analizar_parrafo("Un texto cualquiera sin marcadores claros")
        assert r["tipo_dominante"] == "neutro"


class TestEvaluarEjercicio:
    def test_aprobado_coordinada(self):
        r = evaluar_ejercicio(
            "Juan estudia, pero su hermano juega", "oracion_coordinada"
        )
        assert r["aprobado"] is True

    def test_no_aprobado_simple(self):
        r = evaluar_ejercicio("Juan estudia", "oracion_coordinada")
        assert r["aprobado"] is False

    def test_aprobado_subordinada(self):
        r = evaluar_ejercicio(
            "Juan se fue porque estaba cansado", "oracion_subordinada"
        )
        assert r["aprobado"] is True

    def test_aprobado_parrafo_argumentativo(self):
        r = evaluar_ejercicio(
            "Porque es importante, por lo tanto actuamos. Sin embargo, cuidado.",
            "parrafo_argumentativo",
        )
        assert r["aprobado"] is True

    def test_no_aprobado_parrafo(self):
        r = evaluar_ejercicio("Hola mundo cruel", "parrafo_argumentativo")
        assert r["aprobado"] is False


class TestClasificarError:
    def test_aprobado_none(self):
        r = clasificar_error(
            "Juan estudia, pero Maria trabaja", "oracion_coordinada"
        )
        assert r is None

    def test_fallido_dict(self):
        r = clasificar_error("Hola mundo cruel", "oracion_coordinada")
        assert r is not None
        assert r["categoria_gramatical"] == "oracion_coordinada"
        assert r["idioma"] == "ES"
        assert "en_lugar_de_oracion_coordinada" in r["patron_error"]
