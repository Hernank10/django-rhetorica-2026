"""Tests de tecnicas de gramatica generativa."""
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from core.models_gramatica import TecnicaGramatical, EjercicioGramatical, ProgresoGramatical
from core.data.tecnicas_generativa import TECNICAS, EJERCICIOS


class TestDataGenerativa(TestCase):
    def test_15_tecnicas_bloque_A(self):
        self.assertEqual(len(TECNICAS), 15)
        for t in TECNICAS:
            self.assertEqual(t["modulo"], "generativa")
            self.assertEqual(t["bloque"], "A")

    def test_numeros_consecutivos(self):
        nums = sorted(t["numero"] for t in TECNICAS)
        self.assertEqual(nums, list(range(1, 16)))

    def test_campos_requeridos(self):
        campos = ["numero", "bloque", "titulo", "teoria", "explicacion", "regla", "ejemplo_correcto", "ejemplo_incorrecto", "nivel", "modulo"]
        for t in TECNICAS:
            for c in campos:
                self.assertIn(c, t)
                self.assertTrue(t[c])

    def test_ejercicios(self):
        self.assertEqual(len(EJERCICIOS), 15)
        for i in range(1, 16):
            self.assertIn(i, EJERCICIOS)


class TestSeedGenerativa(TestCase):
    def test_seed_dos_veces_no_duplica(self):
        from scripts.seed_generativa import main as seed
        seed()
        n1 = TecnicaGramatical.objects.filter(modulo="generativa").count()
        seed()
        n2 = TecnicaGramatical.objects.filter(modulo="generativa").count()
        self.assertEqual(n1, n2)
        self.assertEqual(n1, 15)


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