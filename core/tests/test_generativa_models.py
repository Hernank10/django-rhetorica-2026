"""Tests de tecnicas de gramatica generativa."""
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from core.models_gramatica import TecnicaGramatical, EjercicioGramatical, ProgresoGramatical
from core.data.tecnicas_generativa import TECNICAS, EJERCICIOS


class TestDataGenerativa(TestCase):
    def test_bloque_A_tiene_15(self):
        bloque_a = [t for t in TECNICAS if t["bloque"] == "A"]
        self.assertEqual(len(bloque_a), 15)
        for t in bloque_a:
            self.assertEqual(t["modulo"], "generativa")

    def test_todos_modulo_generativa(self):
        for t in TECNICAS:
            self.assertEqual(t["modulo"], "generativa")

    def test_numeros_consecutivos(self):
        nums = sorted(t["numero"] for t in TECNICAS)
        # Generativas empiezan en 101 para no colisionar con las 100 gramaticas
        inicio = min(nums)
        self.assertEqual(inicio, 101)
        self.assertEqual(nums, list(range(inicio, inicio + len(nums))))

    def test_campos_requeridos(self):
        campos = ["numero", "bloque", "titulo", "teoria", "explicacion", "regla", "ejemplo_correcto", "ejemplo_incorrecto", "nivel", "modulo"]
        for t in TECNICAS:
            for c in campos:
                self.assertIn(c, t)
                self.assertTrue(t[c])

    def test_ejercicios(self):
        nums_tecnicas = {t["numero"] for t in TECNICAS}
        nums_ejercicios = set(EJERCICIOS.keys())
        faltantes = nums_tecnicas - nums_ejercicios
        self.assertEqual(faltantes, set(), f"Tecnicas sin ejercicios: {faltantes}")


class TestSeedGenerativa(TestCase):
    def test_seed_dos_veces_no_duplica(self):
        from scripts.seed_generativa import main as seed
        seed()
        n1 = TecnicaGramatical.objects.filter(modulo="generativa").count()
        seed()
        n2 = TecnicaGramatical.objects.filter(modulo="generativa").count()
        self.assertEqual(n1, n2)
        self.assertEqual(n1, len(TECNICAS))


class TestIndiceGenerativaView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("gen_u", password="x")
        TecnicaGramatical.objects.create(
            numero=1, bloque="A", titulo="T1 generativa", modulo="generativa",
            teoria="t", explicacion="e", regla="r", ejemplo_correcto="c", ejemplo_incorrecto="i",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_200(self):
        r = self.client.get(reverse("gramatica:indice_generativa"))
        self.assertEqual(r.status_code, 200)

    def test_anonimo_redirect(self):
        self.client.logout()
        r = self.client.get(reverse("gramatica:indice_generativa"))
        self.assertEqual(r.status_code, 302)