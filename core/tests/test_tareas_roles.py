"""Tests de tareas por rol y panel admin."""
from datetime import timedelta

from django.apps import apps
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.services.tareas import tareas_profesor, tareas_admin


def _crear_user(username, grupo=None):
    u = User.objects.create_user(username, password="x")
    if grupo:
        g, _ = Group.objects.get_or_create(name=grupo)
        u.groups.add(g)
    return u


class TestTareasProfesor(TestCase):
    @classmethod
    def setUpTestData(cls):
        Curso = apps.get_model("core", "Curso")
        Modulo = apps.get_model("core", "Modulo")
        Leccion = apps.get_model("core", "Leccion")
        ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")

        cls.prof = _crear_user("prof_t", "Profesor")
        cls.est = _crear_user("est_t", "Estudiante")

        cls.curso_borrador = Curso.objects.create(
            titulo="Curso en borrador", slug="curso-borrador",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="borrador",
            profesor_asignado=cls.prof,
        )
        cls.curso_pub = Curso.objects.create(
            titulo="Curso publicado", slug="curso-pub",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="publicado",
            profesor_asignado=cls.prof,
        )
        mod = Modulo.objects.create(curso=cls.curso_pub, titulo="M1", orden=1)
        lec = Leccion.objects.create(
            modulo=mod, titulo="L1", contenido="c", tipo="teoria", orden=1,
        )
        ProgresoUsuario.objects.create(
            usuario=cls.est, leccion=lec, completado=True,
            completado_en=timezone.now() - timedelta(days=8),
        )

    def test_cursos_borrador(self):
        t = tareas_profesor(self.prof)
        self.assertIn(self.curso_borrador, t["cursos_borrador"])

    def test_estudiantes_riesgo(self):
        t = tareas_profesor(self.prof)
        self.assertIn(self.est, t["estudiantes_riesgo"])

    def test_total_calculado(self):
        t = tareas_profesor(self.prof)
        self.assertGreaterEqual(t["total"], 2)


class TestTareasAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser("admin_t", "a@t.com", "x")
        User.objects.create_user("sin_grupo", password="x")

    def test_usuarios_sin_grupo(self):
        t = tareas_admin()
        usernames = [u.username for u in t["usuarios_sin_grupo"]]
        self.assertIn("sin_grupo", usernames)


class TestProfesorDashboardExtended(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prof = _crear_user("prof_dash", "Profesor")

    def setUp(self):
        self.client.force_login(self.prof)

    def test_renderiza_notif_y_tareas(self):
        r = self.client.get(reverse("profesor:dashboard"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Notificaciones recientes")
        self.assertContains(r, "Tareas pendientes")


class TestAdminPanel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser("admin_p", "a@p.com", "x")
        cls.est = _crear_user("est_p", "Estudiante")

    def test_staff_200(self):
        self.client.force_login(self.admin)
        r = self.client.get(reverse("admin_panel"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Panel de administración")
        self.assertContains(r, "Notificaciones recientes")

    def test_no_staff_redirige(self):
        self.client.force_login(self.est)
        r = self.client.get(reverse("admin_panel"))
        self.assertIn(r.status_code, (302, 403))