"""Tests de las vistas de gramatica (modulo 11)."""
import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models_gramatica import TecnicaGramatical, EjercicioGramatical, ProgresoGramatical


class BaseGramaticaViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("gram_u", password="x")
        cls.t1 = TecnicaGramatical.objects.create(
            numero=1, bloque="A", titulo="T1",
            teoria="t", explicacion="e", regla="r",
            ejemplo_correcto="ok", ejemplo_incorrecto="no",
        )
        cls.ej1 = EjercicioGramatical.objects.create(
            tecnica=cls.t1, tipo=1, orden=1, payload={
                "enunciado": "Elige",
                "opciones": [
                    {"id": "a", "texto": "mal", "correcta": False, "razon": "no"},
                    {"id": "b", "texto": "bien", "correcta": True, "razon": "si"},
                ],
                "justificacion_obligatoria": False,
                "regla": "regla X",
            },
        )

    def setUp(self):
        self.client.force_login(self.user)


class TestIndice(BaseGramaticaViewTest):
    def test_200(self):
        r = self.client.get(reverse("gramatica:indice"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Gramatica")

    def test_anonimo_redirect(self):
        self.client.logout()
        r = self.client.get(reverse("gramatica:indice"))
        self.assertEqual(r.status_code, 302)


class TestTecnica(BaseGramaticaViewTest):
    def test_200(self):
        r = self.client.get(reverse("gramatica:tecnica", args=[1]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "T1")

    def test_404(self):
        r = self.client.get(reverse("gramatica:tecnica", args=[999]))
        self.assertEqual(r.status_code, 404)


class TestEvaluarAjax(BaseGramaticaViewTest):
    def test_post_correcto(self):
        r = self.client.post(
            reverse("gramatica:evaluar"),
            data=json.dumps({"ejercicio_id": self.ej1.id, "respuesta": {"opcion_id": "b"}}),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["estado"], "en_progreso")

    def test_post_incorrecto(self):
        r = self.client.post(
            reverse("gramatica:evaluar"),
            data=json.dumps({"ejercicio_id": self.ej1.id, "respuesta": {"opcion_id": "a"}}),
            content_type="application/json",
        )
        self.assertFalse(r.json()["ok"])

    def test_get_rechazado(self):
        r = self.client.get(reverse("gramatica:evaluar"))
        self.assertEqual(r.status_code, 405)

    def test_json_invalido(self):
        r = self.client.post(reverse("gramatica:evaluar"), data="no es json", content_type="application/json")
        self.assertEqual(r.status_code, 400)


class TestProgreso(BaseGramaticaViewTest):
    def test_200(self):
        r = self.client.get(reverse("gramatica:progreso"))
        self.assertEqual(r.status_code, 200)


class TestContador(BaseGramaticaViewTest):
    def test_json(self):
        r = self.client.get(reverse("gramatica:contador"))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("dominadas", data)
        self.assertIn("total", data)


class TestIntegracionDashboard(BaseGramaticaViewTest):
    def test_dashboard_muestra_card_gramatica(self):
        r = self.client.get(reverse("estudiante:dashboard"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Gramatica castellana")