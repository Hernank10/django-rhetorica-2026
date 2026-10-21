"""Tests de views_estudiante.dashboard con charts (Commit 3)."""
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class TestDashboardEstudianteCharts(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="est_chart_test",
            password="Test1234!",
        )
        try:
            g = Group.objects.get(name="Estudiante")
            self.user.groups.add(g)
        except Group.DoesNotExist:
            pass
        self.client.login(username="est_chart_test", password="Test1234!")

    def test_200_ok(self):
        r = self.client.get(reverse("estudiante:dashboard"))
        assert r.status_code == 200

    def test_contexto_aciertos_y_certs(self):
        r = self.client.get(reverse("estudiante:dashboard"))
        ctx = r.context
        assert "aciertos_data" in ctx
        assert "ultimos_certs" in ctx
        assert isinstance(ctx["aciertos_data"], list)

    def test_contiene_canvases(self):
        r = self.client.get(reverse("estudiante:dashboard"))
        html = r.content.decode("utf-8")
        assert 'id="chartAciertos"' in html
        assert 'id="chartTipos"' in html

    def test_contiene_card_certs(self):
        r = self.client.get(reverse("estudiante:dashboard"))
        html = r.content.decode("utf-8")
        assert "Mis certificados recientes" in html

    def test_sin_datos_no_rompe(self):
        # Sin respuestas ni certs, el HTML debe seguir renderizando
        r = self.client.get(reverse("estudiante:dashboard"))
        assert r.status_code == 200
        html = r.content.decode("utf-8")
        # Si no hay aciertos, el JS muestra fallback con "Sin datos"
        assert "chartAciertos" in html
        assert "chartTipos" in html