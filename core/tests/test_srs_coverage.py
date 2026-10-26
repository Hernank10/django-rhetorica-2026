"""Tests especificos para cubrir branches de views_srs.py (coverage 97%)."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models_srs import Flashcard, Review


class TestSRSCoverageBranches(TestCase):
    """Cubre las 22 lineas faltantes de views_srs.py."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("srs_cov", password="x")

    def setUp(self):
        self.client.force_login(self.user)

    def test_verificar_no_auth_401(self):
        """Cubre linea 49: verificar sin auth -> 401."""
        fc = Flashcard.objects.create(
            estudiante=self.user, frente="a", reverso="b", tipo="x",
            respuesta_ejercicio="algo",
        )
        rv = Review.objects.create(
            flashcard=fc, programada_para=timezone.now().date(),
        )
        self.client.logout()
        r = self.client.post(reverse("srs_verificar", args=[rv.id]), {})
        self.assertEqual(r.status_code, 401)

    def test_verificar_sin_ejercicio_200(self):
        """Cubre linea 61: verificar con flashcard sin respuesta_ejercicio."""
        fc = Flashcard.objects.create(
            estudiante=self.user, frente="c", reverso="d", tipo="x",
            respuesta_ejercicio="",
        )
        rv = Review.objects.create(
            flashcard=fc, programada_para=timezone.now().date(),
        )
        r = self.client.post(
            reverse("srs_verificar", args=[rv.id]),
            {"respuesta": "algo"},
        )
        self.assertEqual(r.status_code, 200)

    def test_estadisticas_branches(self):
        """Cubre lineas 106-141: branches de madurez/facilidad/intervalos."""
        hoy = timezone.now().date()
        casos = [
            # (repeticiones, intervalo_dias, facilidad)
            (0,  1,  1.4),   # Nueva (0 reps) + facilidad 1.3-1.5 + intervalo 1d
            (1,  2,  1.6),   # Aprendizaje (1-2) + facilidad 1.5-1.8 + intervalo 2-3d
            (3,  5,  1.9),   # Joven (<7d) + facilidad 1.8-2.0 + intervalo 4-7d
            (4,  20, 2.1),   # Madura (7-30d) + facilidad 2.0-2.3 + intervalo 8-30d
            (5,  40, 2.5),   # Dominada (30d+) + facilidad 2.3+ + intervalo 30d+
        ]
        for i, (rep, intervalo, facilidad) in enumerate(casos):
            fc = Flashcard.objects.create(
                estudiante=self.user, frente=f"f{i}", reverso=f"r{i}", tipo="x",
            )
            Review.objects.create(
                flashcard=fc, programada_para=hoy,
                repeticiones=rep, intervalo_dias=intervalo, facilidad=facilidad,
            )

        r = self.client.get(reverse("srs_estadisticas"))
        self.assertEqual(r.status_code, 200)