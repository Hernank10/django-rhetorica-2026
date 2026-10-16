"""Tests de core/views_analytics.py."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Respuesta


User = get_user_model()


@pytest.fixture
def profesor_staff(db):
    return User.objects.create_user(
        username="prof_staff_analytics",
        password="x",
        is_staff=True,
    )


@pytest.fixture
def alumno_analytics(db):
    return User.objects.create_user(
        username="alumno_analytics",
        password="x",
    )


def _url(nombre, *args):
    return reverse(f"profesor:{nombre}", args=args)


class TestAuth:
    def test_anonimo_401(self, client):
        r = client.get(_url("analytics_heatmap"))
        assert r.status_code == 401

    def test_alumno_403(self, client, alumno_analytics):
        client.force_login(alumno_analytics)
        r = client.get(_url("analytics_heatmap"))
        assert r.status_code == 403

    def test_profesor_200(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_heatmap"))
        assert r.status_code == 200


class TestHeatmapAlumnos:
    def test_vacio(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_heatmap"))
        assert r.json() == {"usuarios": [], "categorias": [], "valores": []}

    def test_con_datos(self, client, profesor_staff, alumno_analytics):
        Respuesta.objects.create(
            user=alumno_analytics, tipo_ejercicio="A",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_heatmap"))
        assert r.status_code == 200
        assert "categorias" in r.json()

    def test_dias_invalido_se_clampa(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_heatmap") + "?dias=abc")
        assert r.status_code == 200

    def test_dias_negativo_se_clampa(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_heatmap") + "?dias=-5")
        assert r.status_code == 200


class TestHeatmapGrupo:
    def test_vacio(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_heatmap_grupo"))
        assert r.json() == {"grupos": []}

    def test_con_datos(self, client, profesor_staff, alumno_analytics):
        Respuesta.objects.create(
            user=alumno_analytics, tipo_ejercicio="A",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_heatmap_grupo"))
        assert len(r.json()["grupos"]) == 1


class TestTiempos:
    def test_vacio(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_tiempos"))
        assert r.json() == {"categorias": []}


class TestRetencion:
    def test_vacio(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_retencion"))
        assert r.json() == {"semanas": []}

    def test_semanas_invalido(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_retencion") + "?semanas=999")
        assert r.status_code == 200


class TestErrores:
    def test_default_la(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_errores"))
        assert r.json()["idioma"] == "LA"

    def test_idioma_invalido_se_clampa_la(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_errores") + "?idioma=XX")
        assert r.json()["idioma"] == "LA"

    def test_idioma_valido(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_errores") + "?idioma=EN")
        assert r.json()["idioma"] == "EN"


class TestResumenAlumno:
    def test_404_si_no_existe(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_alumno", 99999))
        assert r.status_code == 404

    def test_404_si_es_staff(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_alumno", profesor_staff.id))
        assert r.status_code == 404

    def test_200_con_alumno(self, client, profesor_staff, alumno_analytics):
        client.force_login(profesor_staff)
        r = client.get(_url("analytics_alumno", alumno_analytics.id))
        assert r.status_code == 200
        data = r.json()
        assert data["username"] == "alumno_analytics"
        assert "progreso" in data

# ============================================================
# Vista HTML (Fase 4)
# ============================================================
class TestDashboardHTML:
    def test_anonimo_redirige_login(self, client):
        """Sin autenticar, el decorador solo_profesor devuelve 401 JSON."""
        r = client.get(reverse("profesor:analytics_dashboard"))
        assert r.status_code == 401

    def test_alumno_403(self, client, alumno_analytics):
        client.force_login(alumno_analytics)
        r = client.get(reverse("profesor:analytics_dashboard"))
        assert r.status_code == 403

    def test_profesor_200(self, client, profesor_staff):
        client.force_login(profesor_staff)
        r = client.get(reverse("profesor:analytics_dashboard"))
        assert r.status_code == 200

    def test_contiene_widgets(self, client, profesor_staff):
        """El HTML debe incluir los 4 canvas/widgets."""
        client.force_login(profesor_staff)
        r = client.get(reverse("profesor:analytics_dashboard"))
        html = r.content.decode("utf-8")
        assert "chartErrores" in html
        assert "chartTiempos" in html
        assert "chartRetencion" in html
        assert "heatmap-wrap" in html
