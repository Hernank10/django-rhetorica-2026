"""Tests de los datos del modulo B1 (100 tecnicas planificadas)."""
from django.test import TestCase
from core.data.tecnicas_b1 import TECNICAS, EJERCICIOS


class TestDataB1(TestCase):
    def test_total_tecnicas(self):
        # Crecimiento progresivo hasta 100 (bloques A-G)
        self.assertGreaterEqual(len(TECNICAS), 15)
        self.assertEqual(len(TECNICAS), 110)

    def test_numeros_consecutivos(self):
        nums = sorted(t["numero"] for t in TECNICAS)
        inicio = min(nums)
        self.assertEqual(inicio, 301)
        self.assertEqual(nums, list(range(inicio, inicio + len(nums))))

    def test_todos_modulo_b1(self):
        # Bloques A-G (plan completo de 100 tecnicas B1)
        BLOQUES_VALIDOS = {"A", "B", "C", "D", "E", "F", "G", "H"}
        for t in TECNICAS:
            self.assertEqual(t["modulo"], "b1")
            self.assertIn(
                t["bloque"], BLOQUES_VALIDOS,
                f"Tecnica {t['numero']} tiene bloque invalido: {t['bloque']}",
            )

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