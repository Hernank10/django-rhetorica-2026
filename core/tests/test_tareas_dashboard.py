"""Tests de tareas pendientes y programadas."""
from datetime import timedelta

from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.services.tareas import (
    evaluaciones_disponibles,
    evaluaciones_programadas,
    lecciones_pendientes,
    resumen_tareas,
)


class TestTareasServicio(TestCase):
    @classmethod
    def setUpTestData(cls):
        Curso = apps.get_model("core", "Curso")
        Modulo = apps.get_model("core", "Modulo")
        Leccion = apps.get_model("core", "Leccion")
        EvaluacionCurso = apps.get_model("core", "EvaluacionCurso")

        cls.user = User.objects.create_user(username="tareas_u", password="x")
        cls.curso = Curso.objects.create(
            titulo="Curso Tareas", slug="curso-tareas",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="publicado",
        )
        cls.mod = Modulo.objects.create(curso=cls.curso, titulo="M1", orden=1)
        cls.lec1 = Leccion.objects.create(
            modulo=cls.mod, titulo="L1", contenido="c", tipo="teoria", orden=1
        )
        cls.lec2 = Leccion.objects.create(
            modulo=cls.mod, titulo="L2", contenido="c", tipo="teoria", orden=2
        )

        now = timezone.now()
        cls.eval_abierta = EvaluacionCurso.objects.create(
            curso=cls.curso, titulo="Eval Abierta", tipo="formativa",
            disponible_desde=now - timedelta(days=1),
            disponible_hasta=now + timedelta(days=7),
        )
        cls.eval_futura = EvaluacionCurso.objects.create(
            curso=cls.curso, titulo="Eval Futura", tipo="formativa",
            disponible_desde=now + timedelta(days=5),
        )
        cls.eval_vencida = EvaluacionCurso.objects.create(
            curso=cls.curso, titulo="Eval Vencida", tipo="formativa",
            disponible_desde=now - timedelta(days=10),
            disponible_hasta=now - timedelta(days=1),
        )

    def test_lecciones_pendientes_incluye_no_completadas(self):
        pend = list(lecciones_pendientes(self.user))
        assert len(pend) == 2
        assert self.lec1 in pend

    def test_lecciones_pendientes_excluye_completadas(self):
        ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
        ProgresoUsuario.objects.create(
            usuario=self.user, leccion=self.lec1, completado=True
        )
        pend = list(lecciones_pendientes(self.user))
        assert self.lec1 not in pend
        assert self.lec2 in pend

    def test_evaluaciones_disponibles_solo_abiertas(self):
        disp = list(evaluaciones_disponibles(self.user))
        assert self.eval_abierta in disp
        assert self.eval_futura not in disp
        assert self.eval_vencida not in disp

    def test_evaluaciones_programadas_solo_futuras(self):
        prog = list(evaluaciones_programadas(self.user))
        assert self.eval_futura in prog
        assert self.eval_abierta not in prog
        assert self.eval_vencida not in prog

    def test_resumen_tareas_cuenta_todo(self):
        r = resumen_tareas(self.user)
        assert r["lecciones"] == 2
        assert r["evaluaciones_disponibles"] == 1
        assert r["evaluaciones_programadas"] == 1


class TestTareasEnDashboard(TestCase):
    @classmethod
    def setUpTestData(cls):
        Curso = apps.get_model("core", "Curso")
        Modulo = apps.get_model("core", "Modulo")
        Leccion = apps.get_model("core", "Leccion")

        cls.user = User.objects.create_user(username="tareas_dash", password="x")
        cls.curso = Curso.objects.create(
            titulo="Curso Dash", slug="curso-dash",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="publicado",
        )
        cls.mod = Modulo.objects.create(curso=cls.curso, titulo="M1", orden=1)
        Leccion.objects.create(
            modulo=cls.mod, titulo="Lec Pendiente Dash", contenido="c",
            tipo="teoria", orden=1,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_muestra_tareas_pendientes(self):
        r = self.client.get(reverse("estudiante:dashboard"))
        assert r.status_code == 200
        html = r.content.decode("utf-8")
        assert "Tareas pendientes" in html
        assert "Lec Pendiente Dash" in html

    def test_dashboard_muestra_secciones_nuevas(self):
        r = self.client.get(reverse("estudiante:dashboard"))
        html = r.content.decode("utf-8")
        assert "Tareas pendientes" in html
        assert "Evaluaciones disponibles" in html
        assert "Próximas evaluaciones programadas" in html