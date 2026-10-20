"""Tests de core/services/parafrasis_registro.py."""
from core.services.parafrasis_registro import (
    PARES_COLOQUIAL_A_FORMAL,
    PARES_FORMAL_A_COLOQUIAL,
    detectar_registro,
    transformar_registro,
    verificar_registro,
)


class TestDetectarRegistro:
    def test_formal(self):
        r = detectar_registro("Usted tiene dinero en el automovil")
        assert r["disponible"] is True
        assert r["registro"] == "formal"
        assert r["formal_count"] == 3

    def test_coloquial(self):
        r = detectar_registro("Vos tiene plata en el carro")
        assert r["disponible"] is True
        assert r["registro"] == "coloquial"
        assert r["coloquial_count"] == 3

    def test_neutral(self):
        r = detectar_registro("Juan lee el libro")
        assert r["disponible"] is True
        assert r["registro"] == "neutral"
        assert r["formal_count"] == 0
        assert r["coloquial_count"] == 0

    def test_vacio(self):
        r = detectar_registro("")
        assert r["disponible"] is False
        assert "vacio" in r["razon"]

    def test_mixto_tie_neutral(self):
        r = detectar_registro("Usted tiene plata")
        assert r["formal_count"] == 1
        assert r["coloquial_count"] == 1
        assert r["registro"] == "neutral"


class TestTransformarRegistro:
    def test_formal_a_coloquial(self):
        r = transformar_registro("Usted tiene dinero", "coloquial")
        assert r["disponible"] is True
        assert r["esperado"] == "Vos tiene plata"
        assert len(r["cambios"]) == 2

    def test_coloquial_a_formal(self):
        r = transformar_registro("Vos tiene plata", "formal")
        assert r["disponible"] is True
        assert r["esperado"] == "Usted tiene dinero"

    def test_sin_cambios(self):
        r = transformar_registro("Juan lee el libro", "coloquial")
        assert r["disponible"] is True
        assert r["esperado"] == ""
        assert "sin cambios" in r["razon"]

    def test_hacia_invalido(self):
        r = transformar_registro("Juan", "xyz")
        assert r["disponible"] is False
        assert "invalido" in r["razon"]


class TestDicts:
    def test_dicts_inversos(self):
        for formal, coloquial in PARES_FORMAL_A_COLOQUIAL.items():
            assert PARES_COLOQUIAL_A_FORMAL[coloquial] == formal

    def test_9_pares(self):
        assert len(PARES_FORMAL_A_COLOQUIAL) == 9

    def test_sin_colisiones(self):
        valores = list(PARES_FORMAL_A_COLOQUIAL.values())
        assert len(valores) == len(set(valores))

class TestVerificarRegistro:
    def test_aprobado_formal_a_coloquial(self):
        r = verificar_registro(
            "Usted tiene dinero",
            "Vos tiene plata",
            "formal_a_coloquial",
        )
        assert r["aprobado"] is True
        assert r["registro_original"] == "formal"
        assert r["registro_parafraseado"] == "coloquial"
        assert "Correcto" in r["feedback"]

    def test_aprobado_coloquial_a_formal(self):
        r = verificar_registro(
            "Vos tiene plata",
            "Usted tiene dinero",
            "coloquial_a_formal",
        )
        assert r["aprobado"] is True

    def test_rechazo_identicos(self):
        texto = "Usted tiene dinero"
        r = verificar_registro(texto, texto, "formal_a_coloquial")
        assert r["aprobado"] is False
        assert "Identicos" in r["feedback"]

    def test_rechazo_original_neutral(self):
        r = verificar_registro(
            "Juan lee el libro",
            "Pedro lee el libro",
            "formal_a_coloquial",
        )
        assert r["aprobado"] is False
        assert "No cumple" in r["feedback"]

    def test_tipo_invalido(self):
        r = verificar_registro("Usted", "Vos", "xyz")
        assert r["aprobado"] is False
        assert "invalido" in r["feedback"]

    def test_vacio(self):
        r = verificar_registro("", "", "formal_a_coloquial")
        assert r["aprobado"] is False
        assert "Falta" in r["feedback"]

class TestTransformarRegistroTextVacio:
    """Cubre rama texto vacio en transformar_registro (lineas 84-85)."""

    def test_texto_vacio(self):
        r = transformar_registro("", "coloquial")
        assert r["disponible"] is False
        assert r["esperado"] == ""
        assert "vacio" in r["razon"]

    def test_texto_solo_espacios(self):
        r = transformar_registro("   ", "formal")
        assert r["disponible"] is False
        assert "vacio" in r["razon"]