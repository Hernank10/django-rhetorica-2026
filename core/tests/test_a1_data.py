"""Tests de los datos del modulo A1 (50 tecnicas actuales)."""
from django.test import TestCase
from core.data.tecnicas_a1 import TECNICAS, EJERCICIOS


class TestDataA1(TestCase):
    def test_total_tecnicas(self):
        self.assertEqual(len(TECNICAS), 50)

    def test_numeros_consecutivos(self):
        nums = sorted(t["numero"] for t in TECNICAS)
        self.assertEqual(nums, list(range(201, 251)))

    def test_todos_modulo_a1(self):
        for t in TECNICAS:
            self.assertEqual(t["modulo"], "a1")
            self.assertIn(t["bloque"], {"A", "B", "C"})

    def test_campos_requeridos(self):
        campos = ["numero", "bloque", "titulo", "teoria", "explicacion",
                  "regla", "ejemplo_correcto", "ejemplo_incorrecto",
                  "nivel", "modulo"]
        for t in TECNICAS:
            for c in campos:
                self.assertIn(c, t)
                self.assertTrue(t[c])

    def test_ejercicios_cubren_todas(self):
        nums_tecnicas = {t["numero"] for t in TECNICAS}
        nums_ejercicios = set(EJERCICIOS.keys())
        faltantes = nums_tecnicas - nums_ejercicios
        self.assertEqual(faltantes, set(), f"Tecnicas sin ejercicios: {faltantes}")