"""Tests de views_profesor.dashboard con charts (Commit 2)."""
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


def crear_staff(username="prof_chart_test"):
    u = User.objects.create_user(
        username=username,
        password="Test1234!",
        is_staff=True,
        is_superuser=True,
    )
    try:
        g = Group.objects.get(name="Profesor")
        u.groups.add(g)
    except Group.DoesNotExist:
        pass
    return u


class TestDashboardProfesorCharts(TestCase):
    def setUp(self):
        self.user = crear_staff()
        self.client.login(username="prof_chart_test", password="Test1234!")

    def test_200_ok(self):
        r = self.client.get(reverse("profesor:dashboard"))
        assert r.status_code == 200

    def test_contexto_tiene_charts(self):
        r = self.client.get(reverse("profesor:dashboard"))
        ctx = r.context
        assert "chart_cursos" in ctx
        assert "chart_actividad" in ctx
        assert "chart_niveles" in ctx
        assert isinstance(ctx["chart_cursos"], list)
        assert isinstance(ctx["chart_actividad"], list)
        assert isinstance(ctx["chart_niveles"], list)

    def test_chart_cursos_estructura(self):
        from django.apps import apps
        Curso = apps.get_model('core', 'Curso')
        Curso.objects.all().delete()
        Curso.objects.create(
            titulo="Curso Chart A",
            slug="curso-chart-a",
            descripcion="d",
            objetivo="o",
            nivel="principiante",
            estado="publicado",
            estudiantes_inscritos=42,
        )
        r = self.client.get(reverse("profesor:dashboard"))
        chart = r.context["chart_cursos"]
        assert len(chart) == 1
        assert chart[0]["titulo"] == "Curso Chart A"
        assert chart[0]["estudiantes_inscritos"] == 42

    def test_chart_niveles_distribucion(self):
        from django.apps import apps
        Curso = apps.get_model('core', 'Curso')
        Curso.objects.all().delete()
        for nivel in ("principiante", "intermedio", "avanzado", "experto"):
            Curso.objects.create(
                titulo="C " + nivel,
                slug="c-" + nivel,
                descripcion="d",
                objetivo="o",
                nivel=nivel,
                estado="publicado",
            )
        r = self.client.get(reverse("profesor:dashboard"))
        chart = r.context["chart_niveles"]
        assert len(chart) == 4
        niveles = {x["nivel"] for x in chart}
        assert niveles == {"principiante", "intermedio", "avanzado", "experto"}

    def test_sin_datos_no_rompe(self):
        from django.apps import apps
        Curso = apps.get_model('core', 'Curso')
        ProgresoUsuario = apps.get_model('core', 'ProgresoUsuario')
        Curso.objects.all().delete()
        ProgresoUsuario.objects.all().delete()
        r = self.client.get(reverse("profesor:dashboard"))
        assert r.status_code == 200
        assert r.context["chart_cursos"] == []
        assert r.context["chart_actividad"] == []
        assert r.context["chart_niveles"] == []

    def test_contiene_canvases(self):
        r = self.client.get(reverse("profesor:dashboard"))
        html = r.content.decode("utf-8")
        assert 'id="chartCursos"' in html
        assert 'id="chartActividad"' in html
        assert 'id="chartNiveles"' in html
        assert 'chart.umd.min.js' in html