"""Tests de las vistas del módulo 10 (sintaxis)."""
import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models_sintaxis import TecnicaSintactica, EjercicioTecnica, ProgresoTecnica


class BaseSintaxisViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("sint_u", password="x")
        cls.t1 = TecnicaSintactica.objects.create(
            numero=1, bloque="A", titulo="T1",
            teoria="t", explicacion="e", regla="r",
            ejemplo_correcto="ok", ejemplo_incorrecto="no",
        )
        cls.ej1 = EjercicioTecnica.objects.create(
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


class TestIndiceView(BaseSintaxisViewTest):
    def test_200(self):
        r = self.client.get(reverse("sintaxis:indice"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Sintaxis")

    def test_anonimo_redirect(self):
        self.client.logout()
        r = self.client.get(reverse("sintaxis:indice"))
        self.assertEqual(r.status_code, 302)


class TestTecnicaView(BaseSintaxisViewTest):
    def test_200(self):
        r = self.client.get(reverse("sintaxis:tecnica", args=[1]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "T1")

    def test_404_si_no_existe(self):
        r = self.client.get(reverse("sintaxis:tecnica", args=[999]))
        self.assertEqual(r.status_code, 404)

    def test_progreso_creado(self):
        self.client.get(reverse("sintaxis:tecnica", args=[1]))
        self.assertTrue(ProgresoTecnica.objects.filter(
            usuario=self.user, tecnica=self.t1,
        ).exists())


class TestEvaluarAjax(BaseSintaxisViewTest):
    def test_post_correcto(self):
        r = self.client.post(
            reverse("sintaxis:evaluar"),
            data=json.dumps({"ejercicio_id": self.ej1.id, "respuesta": {"opcion_id": "b"}}),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data["ok"])
        self.assertIn("Correcto", data["feedback"])

    def test_post_incorrecto(self):
        r = self.client.post(
            reverse("sintaxis:evaluar"),
            data=json.dumps({"ejercicio_id": self.ej1.id, "respuesta": {"opcion_id": "a"}}),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.json()["ok"])

    def test_get_rechazado(self):
        r = self.client.get(reverse("sintaxis:evaluar"))
        self.assertEqual(r.status_code, 405)

    def test_json_invalido(self):
        r = self.client.post(
            reverse("sintaxis:evaluar"),
            data="no es json",
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 400)

    def test_falta_ejercicio_id(self):
        r = self.client.post(
            reverse("sintaxis:evaluar"),
            data=json.dumps({"respuesta": {}}),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 400)


class TestProgresoView(BaseSintaxisViewTest):
    def test_200(self):
        r = self.client.get(reverse("sintaxis:progreso"))
        self.assertEqual(r.status_code, 200)


class TestContadorAjax(BaseSintaxisViewTest):
    def test_json(self):
        r = self.client.get(reverse("sintaxis:contador"))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("dominadas", data)
        self.assertIn("total", data)