"""Tests de las vistas de Lengua Castellana A1 (modulo 13)."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models_gramatica import TecnicaGramatical


class BaseA1Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("a1_u", password="x")
        # 2 A1
        for i in [201, 202]:
            TecnicaGramatical.objects.create(
                numero=i, bloque="A", titulo=f"T{i} A1", modulo="a1",
                teoria="t", explicacion="e", regla="r",
                ejemplo_correcto="c", ejemplo_incorrecto="i",
            )
        # 1 gramatica (para verificar filtro)
        TecnicaGramatical.objects.create(
            numero=1, bloque="A", titulo="T1 gram", modulo="gramatica",
            teoria="t", explicacion="e", regla="r",
            ejemplo_correcto="c", ejemplo_incorrecto="i",
        )

    def setUp(self):
        self.client.force_login(self.user)


class TestIndiceA1(BaseA1Test):
    def test_200(self):
        r = self.client.get(reverse("gramatica:indice_a1"))
        self.assertEqual(r.status_code, 200)

    def test_solo_muestra_a1(self):
        r = self.client.get(reverse("gramatica:indice_a1"))
        self.assertContains(r, "T201 A1")
        self.assertContains(r, "T202 A1")
        self.assertNotContains(r, "T1 gram")

    def test_anonimo_redirect(self):
        self.client.logout()
        r = self.client.get(reverse("gramatica:indice_a1"))
        self.assertEqual(r.status_code, 302)


class TestTecnicaA1(BaseA1Test):
    def test_tecnica_201_200(self):
        r = self.client.get(reverse("gramatica:tecnica", args=[201]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "T201 A1")

    def test_tecnica_201_bloque_A1(self):
        # Verifica que pasa es_a1 al template
        r = self.client.get(reverse("gramatica:tecnica", args=[201]))
        self.assertEqual(r.context["es_a1"], True)
        self.assertEqual(r.context["es_generativa"], False)