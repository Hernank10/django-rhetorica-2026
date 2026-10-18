"""Tests de core/services/srs_db.py (con BD)."""
from datetime import date, timedelta

import pytest
from django.apps import apps
from django.utils import timezone

from core.models import Flashcard, Review
from core.services.srs_db import (
    aplicar_sm2_y_guardar,
    crear_flashcards_desde_errores,
    estadisticas_estudiante,
    programar_primera_revision,
    reviews_para_hoy,
)


HOY = date(2026, 10, 18)


@pytest.fixture
def usuario(db, django_user_model):
    return django_user_model.objects.create_user(username="srs_db_u", password="x")


@pytest.fixture
def otro_usuario(db, django_user_model):
    return django_user_model.objects.create_user(username="srs_db_o", password="x")


@pytest.fixture
def flashcard(db, usuario):
    return Flashcard.objects.create(
        estudiante=usuario, idioma="ES", tipo="vocabulario",
        frente="miles", reverso="soldado",
    )


class TestProgramarPrimeraRevision:
    def test_crea_review_inicial(self, flashcard):
        r = programar_primera_revision(flashcard, hoy=HOY)
        assert r.flashcard_id == flashcard.pk
        assert r.programada_para == HOY
        assert r.intervalo_dias == 0
        assert r.facilidad == 2.5
        assert r.repeticiones == 0
        assert r.completada_en is None

    def test_idempotente(self, flashcard):
        r1 = programar_primera_revision(flashcard, hoy=HOY)
        r2 = programar_primera_revision(flashcard, hoy=HOY)
        assert r1.pk == r2.pk
        assert Review.objects.filter(flashcard=flashcard).count() == 1

    def test_sin_hoy_usa_localdate(self, flashcard):
        r = programar_primera_revision(flashcard)
        assert r.programada_para == timezone.localdate()


class TestAplicarSm2YGuardar:
    def test_calidad_5_crea_nueva_pendiente(self, flashcard):
        r = programar_primera_revision(flashcard, hoy=HOY)
        nueva = aplicar_sm2_y_guardar(r, calidad=5, hoy=HOY)

        r.refresh_from_db()
        assert r.completada_en is not None
        assert r.calidad_respuesta == 5

        assert nueva.pk != r.pk
        assert nueva.completada_en is None
        assert nueva.intervalo_dias == 1
        assert nueva.repeticiones == 1
        assert nueva.programada_para == HOY + timedelta(days=1)

    def test_calidad_2_resetea(self, flashcard):
        r = programar_primera_revision(flashcard, hoy=HOY)
        # Forzar estado avanzado
        r.intervalo_dias = 45
        r.facilidad = 2.9
        r.repeticiones = 4
        r.save()

        nueva = aplicar_sm2_y_guardar(r, calidad=2, hoy=HOY)
        assert nueva.intervalo_dias == 1
        assert nueva.repeticiones == 0

    def test_cadena_de_3_repasos(self, flashcard):
        r = programar_primera_revision(flashcard, hoy=HOY)
        r = aplicar_sm2_y_guardar(r, calidad=5, hoy=HOY)
        assert r.intervalo_dias == 1
        r = aplicar_sm2_y_guardar(r, calidad=5, hoy=HOY)
        assert r.intervalo_dias == 6
        r = aplicar_sm2_y_guardar(r, calidad=5, hoy=HOY)
        assert r.intervalo_dias == 16  # round(6 * 2.7)
        assert Review.objects.filter(flashcard=flashcard).count() == 4  # 1 inicial + 3

    def test_review_anterior_queda_completada(self, flashcard):
        r = programar_primera_revision(flashcard, hoy=HOY)
        r_pk = r.pk
        aplicar_sm2_y_guardar(r, calidad=5, hoy=HOY)
        r.refresh_from_db()
        assert r.pk == r_pk
        assert r.completada_en is not None

class TestReviewsParaHoy:
    def test_vacio(self, usuario):
        assert reviews_para_hoy(usuario, hoy=HOY).count() == 0

    def test_filtra_por_estudiante(self, usuario, otro_usuario, flashcard):
        fc2 = Flashcard.objects.create(
            estudiante=otro_usuario, idioma="ES", tipo="vocabulario",
            frente="x", reverso="y",
        )
        programar_primera_revision(flashcard, hoy=HOY)
        programar_primera_revision(fc2, hoy=HOY)

        pendientes = reviews_para_hoy(usuario, hoy=HOY)
        assert pendientes.count() == 1
        assert pendientes[0].flashcard_id == flashcard.pk

    def test_filtra_por_fecha(self, flashcard):
        r = programar_primera_revision(flashcard, hoy=HOY)
        # Mover a futuro
        r.programada_para = HOY + timedelta(days=10)
        r.save()
        assert reviews_para_hoy(flashcard.estudiante, hoy=HOY).count() == 0

    def test_excluye_completadas(self, flashcard):
        r = programar_primera_revision(flashcard, hoy=HOY)
        aplicar_sm2_y_guardar(r, calidad=5, hoy=HOY)
        # Solo queda la nueva programada para mañana, no hoy
        assert reviews_para_hoy(flashcard.estudiante, hoy=HOY).count() == 0


class TestCrearFlashcardsDesdeErrores:
    @pytest.fixture
    def historial_cls(self):
        return apps.get_model("core", "HistorialErrorSintactico")

    def test_sin_errores(self, usuario):
        resultado = crear_flashcards_desde_errores(usuario)
        assert resultado == []

    def test_con_3_errores_crea_3_flashcards(
        self, usuario, historial_cls
    ):
        for patron in (
            "simple_en_lugar_de_coordinada",
            "simple_en_lugar_de_subordinada",
            "yuxtapuesta_en_lugar_de_coordinada",
        ):
            historial_cls.objects.create(
                estudiante=usuario, idioma="ES",
                categoria_gramatical="oracion_coordinada",
                patron_error=patron, frecuencia=1, resuelto=False,
            )
        resultado = crear_flashcards_desde_errores(usuario)
        assert len(resultado) == 3
        assert Flashcard.objects.filter(estudiante=usuario).count() == 3

    def test_idempotente(self, usuario, historial_cls):
        historial_cls.objects.create(
            estudiante=usuario, idioma="ES",
            categoria_gramatical="oracion_coordinada",
            patron_error="simple_en_lugar_de_coordinada",
            frecuencia=1, resuelto=False,
        )
        r1 = crear_flashcards_desde_errores(usuario)
        r2 = crear_flashcards_desde_errores(usuario)
        assert len(r1) == 1
        assert len(r2) == 1
        assert Flashcard.objects.filter(estudiante=usuario).count() == 1

    def test_ignora_resueltos(self, usuario, historial_cls):
        historial_cls.objects.create(
            estudiante=usuario, idioma="ES",
            categoria_gramatical="oracion_coordinada",
            patron_error="ya_resuelto", frecuencia=1, resuelto=True,
        )
        resultado = crear_flashcards_desde_errores(usuario)
        assert resultado == []

    def test_programa_primera_revision(
        self, usuario, historial_cls
    ):
        historial_cls.objects.create(
            estudiante=usuario, idioma="ES",
            categoria_gramatical="oracion_coordinada",
            patron_error="simple_en_lugar_de_coordinada",
            frecuencia=1, resuelto=False,
        )
        resultado = crear_flashcards_desde_errores(usuario)
        fc = resultado[0]
        assert Review.objects.filter(flashcard=fc, completada_en__isnull=True).count() == 1


class TestEstadisticasEstudiante:
    def test_sin_data(self, usuario):
        e = estadisticas_estudiante(usuario, hoy=HOY)
        assert e["total_flashcards"] == 0
        assert e["reviews_pendientes"] == 0
        assert e["retencion_pct"] is None
        assert e["proxima_revision"] is None

    def test_con_flashcard_y_review(self, flashcard):
        programar_primera_revision(flashcard, hoy=HOY)
        e = estadisticas_estudiante(flashcard.estudiante, hoy=HOY)
        assert e["total_flashcards"] == 1
        assert e["reviews_pendientes"] == 1
        assert e["retencion_pct"] is None
        assert e["proxima_revision"] == HOY

    def test_retencion_calculada(self, flashcard):
        # 3 reviews completadas: 2 con calidad>=3, 1 con calidad<3 -> 66.7%
        for calidad in (5, 4, 1):
            r = programar_primera_revision(flashcard, hoy=HOY)
            aplicar_sm2_y_guardar(r, calidad=calidad, hoy=HOY)

        e = estadisticas_estudiante(flashcard.estudiante, hoy=HOY)
        assert e["retencion_pct"] == 66.7

    def test_proxima_revision(self, flashcard):
        r1 = programar_primera_revision(flashcard, hoy=HOY)
        aplicar_sm2_y_guardar(r1, calidad=5, hoy=HOY)  # nueva: HOY+1
        r2 = programar_primera_revision(flashcard, hoy=HOY + timedelta(days=5))
        # Ya existe la nueva r2? El get_or_create de programar_primera_revision
        # retorna la existente (la de HOY+1) porque no está completada.
        # Entonces proxima_revision = HOY + 1
        e = estadisticas_estudiante(flashcard.estudiante, hoy=HOY)
        assert e["proxima_revision"] == HOY + timedelta(days=1)