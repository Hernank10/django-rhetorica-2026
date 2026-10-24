"""Tests de views_profesor.lista_estudiantes_metricas."""
from django.apps import apps
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class TestListaEstudiantesMetricas(TestCase):
    def setUp(self):
        self.prof = User.objects.create_user(
            username="prof_metricas_test",
            password="Test1234!",
        )
        g_prof, _ = Group.objects.get_or_create(name="Profesor")
        self.prof.groups.add(g_prof)

        self.est = User.objects.create_user(
            username="est_metricas_test",
            password="Test1234!",
        )
        g_est, _ = Group.objects.get_or_create(name="Estudiante")
        self.est.groups.add(g_est)

        self.client.login(username="prof_metricas_test", password="Test1234!")

    def test_anonimo_redirect(self):
        self.client.logout()
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        assert r.status_code == 302

    def test_estudiante_redirect(self):
        self.client.logout()
        self.client.login(username="est_metricas_test", password="Test1234!")
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        # Decorador @profesor_required devuelve 403 para autenticados no-profesores
        # (antes devolvía 302 a login hasta v1.1.1)
        assert r.status_code == 403

    def test_profesor_200(self):
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        assert r.status_code == 200

    def test_context_keys(self):
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        for key in ("estudiantes", "cursos", "filtros", "total"):
            assert key in r.context, f"falta {key}"

    def test_filtro_username(self):
        r = self.client.get(
            reverse("profesor:estudiantes_metricas"), {"q": "est_metricas"}
        )
        usernames = [e.username for e in r.context["estudiantes"]]
        assert "est_metricas_test" in usernames
        assert len(usernames) >= 1
        # Ningun username sin el substring
        for u in usernames:
            assert "est_metricas" in u

    def test_annotations_basicas(self):
        Curso = apps.get_model("core", "Curso")
        Modulo = apps.get_model("core", "Modulo")
        Leccion = apps.get_model("core", "Leccion")
        ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")

        curso = Curso.objects.create(
            titulo="Curso Metricas Test",
            slug="curso-metricas-test",
            descripcion="d",
            objetivo="o",
            nivel="principiante",
            estado="publicado",
            creado_por=self.prof,
        )
        modulo = Modulo.objects.create(curso=curso, titulo="M1", orden=1)
        lec1 = Leccion.objects.create(
            modulo=modulo, titulo="L1", contenido="c", tipo="teoria", orden=1
        )
        lec2 = Leccion.objects.create(
            modulo=modulo, titulo="L2", contenido="c", tipo="teoria", orden=2
        )
        ProgresoUsuario.objects.create(
            usuario=self.est, leccion=lec1, completado=True, puntaje_obtenido=80
        )
        ProgresoUsuario.objects.create(
            usuario=self.est, leccion=lec2, completado=True, puntaje_obtenido=90
        )

        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        target = next(
            (e for e in r.context["estudiantes"] if e.username == "est_metricas_test"),
            None,
        )
        assert target is not None
        assert target.cursos_count == 1
        assert target.lecciones_completadas == 2

class TestChartsMetricas(TestCase):
    def setUp(self):
        self.prof = User.objects.create_user(
            username="prof_charts_test", password="Test1234!"
        )
        g_prof, _ = Group.objects.get_or_create(name="Profesor")
        self.prof.groups.add(g_prof)
        self.client.login(username="prof_charts_test", password="Test1234!")

    def test_chart_top_en_context(self):
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        assert "chart_top" in r.context
        assert "labels" in r.context["chart_top"]
        assert "data" in r.context["chart_top"]

    def test_chart_tasa_en_context(self):
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        assert "chart_tasa" in r.context
        assert "labels" in r.context["chart_tasa"]
        assert "data" in r.context["chart_tasa"]
        assert r.context["chart_tasa"]["labels"] == [
            "0-20%", "20-40%", "40-60%", "60-80%", "80-100%"
        ]

    def test_template_tiene_canvas(self):
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        html = r.content.decode("utf-8")
        assert 'id="chartTop"' in html
        assert 'id="chartTasa"' in html
        assert "chart.umd.min.js" in html