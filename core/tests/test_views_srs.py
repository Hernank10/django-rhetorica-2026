"""Tests de vistas SRS (con BD)."""
from datetime import date, timedelta

import pytest
from django.urls import reverse

from core.models import Flashcard, Review
from core.services.srs_db import programar_primera_revision


HOY = date(2026, 10, 18)


@pytest.fixture
def usuario(db, django_user_model):
    return django_user_model.objects.create_user(username="srs_v_u", password="x")


@pytest.fixture
def flashcard(db, usuario):
    return Flashcard.objects.create(
        estudiante=usuario, idioma="ES", tipo="vocabulario",
        frente="miles, militis", reverso="soldado (3a decl.)",
    )


class TestRepasoVista:
    def test_sin_login_redirige(self, client, db):
        r = client.get(reverse("srs_repaso"))
        assert r.status_code == 302
        assert "login" in r.url

    def test_sin_pendientes_todo_al_dia(self, client, usuario):
        client.force_login(usuario)
        r = client.get(reverse("srs_repaso"))
        assert r.status_code == 200
        contenido = r.content.decode("utf-8").lower()
        assert "todo al dia" in contenido or "todo al d" in contenido

    def test_con_pendiente_muestra_frente(self, client, usuario, flashcard):
        programar_primera_revision(flashcard, hoy=HOY)
        client.force_login(usuario)
        r = client.get(reverse("srs_repaso"))
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "miles" in contenido

    def test_post_calidad_5_crea_nueva_review(self, client, usuario, flashcard):
        r_inicial = programar_primera_revision(flashcard, hoy=HOY)
        client.force_login(usuario)

        r = client.post(reverse("srs_repaso"), {"calidad": 5})
        assert r.status_code == 302
        assert reverse("srs_repaso") in r.url

        r_inicial.refresh_from_db()
        assert r_inicial.completada_en is not None
        assert r_inicial.calidad_respuesta == 5
        # Debe haber una nueva Review pendiente
        assert Review.objects.filter(
            flashcard=flashcard, completada_en__isnull=True
        ).count() == 1

    def test_post_calidad_invalida_usa_default(self, client, usuario, flashcard):
        programar_primera_revision(flashcard, hoy=HOY)
        client.force_login(usuario)
        r = client.post(reverse("srs_repaso"), {"calidad": "abc"})
        assert r.status_code == 302
        # Se aplico default=3
        completada = Review.objects.filter(
            flashcard=flashcard, completada_en__isnull=False
        ).first()
        assert completada.calidad_respuesta == 3

    def test_post_sin_pendiente_no_crashea(self, client, usuario):
        client.force_login(usuario)
        r = client.post(reverse("srs_repaso"), {"calidad": 5})
        assert r.status_code == 302

class TestEstadisticasVista:
    def test_sin_login_redirige(self, client, db):
        r = client.get(reverse("srs_estadisticas"))
        assert r.status_code == 302
        assert "login" in r.url

    def test_vacio_muestra_ceros(self, client, usuario):
        client.force_login(usuario)
        r = client.get(reverse("srs_estadisticas"))
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "Estadisticas" in contenido
        # El template muestra "-" cuando retencion_pct es None
        assert "Total flashcards" in contenido

    def test_con_datos_renderiza_metricas(self, client, usuario, flashcard):
        programar_primera_revision(flashcard, hoy=HOY)
        client.force_login(usuario)
        r = client.get(reverse("srs_estadisticas"))
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        assert "Pendientes hoy" in contenido
        assert "Retencion" in contenido

    def test_muestra_proxima_revision(self, client, usuario, flashcard):
        programar_primera_revision(flashcard, hoy=HOY)
        client.force_login(usuario)
        r = client.get(reverse("srs_estadisticas"))
        assert r.status_code == 200
        contenido = r.content.decode("utf-8")
        # El template formatea date como YYYY-MM-DD
        assert "2026-10-18" in contenido