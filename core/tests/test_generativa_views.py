"""Tests de las vistas de gramatica generativa."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models_gramatica import TecnicaGramatical


class TestIndiceGenerativa(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("gen_v", password="x")
        for i in range(101, 106):
            TecnicaGramatical.objects.create(
                numero=i, bloque="A", titulo=f"T{i} gen", modulo="generativa",
                teoria="t", explicacion="e", regla="r",
                ejemplo_correcto="c", ejemplo_incorrecto="i",
            )

    def setUp(self):
        self.client.force_login(self.user)

    def test_200(self):
        r = self.client.get(reverse("gramatica:indice_generativa"))
        self.assertEqual(r.status_code, 200)

    def test_muestra_solo_generativa(self):
        r = self.client.get(reverse("gramatica:indice_generativa"))
        self.assertContains(r, "T101 gen")
        self.assertNotContains(r, "T1 gram")


class TestProgresoGenerativa(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("gen_p", password="x")

    def test_200(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("gramatica:progreso_generativa"))
        self.assertEqual(r.status_code, 200)


class TestContadorModulo(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("gen_c", password="x")

    def test_contador_gramatica(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("gramatica:contador") + "?modulo=gramatica")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("dominadas", data)
        self.assertIn("total", data)

    def test_contador_generativa(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("gramatica:contador") + "?modulo=generativa")
        self.assertEqual(r.status_code, 200)
        self.assertIn("total", r.json())