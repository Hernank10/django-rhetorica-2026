"""Tests de tecnicas_dashboard (100 tecnicas de redaccion)."""
from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestTecnicasDashboard(TestCase):
    @classmethod
    def setUpTestData(cls):
        E = apps.get_model("core", "EjercicioLinguistico")
        for i in range(15):
            E.objects.create(
                titulo=f"T{i:03d} - Tecnica {i}",
                contenido={"teoria": "x", "ejemplo": "y", "enunciado": "z"},
                categoria="test_red",
                tipo="multiple",
                nivel=(i % 3) + 1,
                puntos=10,
                es_adaptativo=False,
                es_redaccion=True,
                tipo_redaccion=("narrativo" if i % 2 == 0 else "argumentativo"),
                idioma="ES",
            )

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="test_red_user", defaults={"email": "r@t.local"}
        )
        self.user.set_password("Test1234!")
        self.user.save()
        self.client.force_login(self.user)

    def test_200_ok(self):
        r = self.client.get(reverse("redaccion_tecnicas"))
        assert r.status_code == 200

    def test_context_tiene_charts(self):
        r = self.client.get(reverse("redaccion_tecnicas"))
        for k in ("chart_tipos", "chart_niveles", "chart_categorias", "tecnicas", "total", "total_global"):
            assert k in r.context, f"falta {k}"
        assert r.context["total_global"] >= 15

    def test_filtro_por_tipo(self):
        r = self.client.get(reverse("redaccion_tecnicas") + "?tipo=narrativo")
        tecnicas = r.context["tecnicas"]
        assert all(t.tipo_redaccion == "narrativo" for t in tecnicas)
        assert r.context["total"] <= r.context["total_global"]

    def test_template_tiene_canvas_y_tabla(self):
        r = self.client.get(reverse("redaccion_tecnicas"))
        html = r.content.decode("utf-8")
        assert 'id="chartTipos"' in html
        assert 'id="chartNiveles"' in html
        assert 'id="chartCategorias"' in html
        assert "chart.umd.min.js" in html
        assert "<table" in html
        assert "100 T" in html or "Técnicas" in html