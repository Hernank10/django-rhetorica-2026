"""Tests de modelos SRS (con BD)."""

from datetime import date

import pytest
from django.db import IntegrityError

from core.models import Flashcard, Review


@pytest.fixture
def usuario(db, django_user_model):
    return django_user_model.objects.create_user(username="srs_u1", password="x")


@pytest.fixture
def flashcard(db, usuario):
    return Flashcard.objects.create(
        estudiante=usuario,
        idioma="ES",
        tipo="vocabulario",
        frente="miles, militis",
        reverso="soldado (3a decl.)",
    )


class TestFlashcardModel:
    def test_str(self, flashcard):
        s = str(flashcard)
        assert "miles" in s
        assert "soldado" in s

    def test_unique_together(self, usuario, flashcard):
        with pytest.raises(IntegrityError):
            Flashcard.objects.create(
                estudiante=usuario,
                idioma="ES",
                tipo="vocabulario",
                frente="miles, militis",  # duplicado
                reverso="soldado",
            )

    def test_mismo_frente_distinto_tipo_ok(self, usuario, flashcard):
        fc2 = Flashcard.objects.create(
            estudiante=usuario,
            idioma="ES",
            tipo="regla",  # distinto tipo, no choca
            frente="miles, militis",
            reverso="otra cosa",
        )
        assert fc2.pk is not None

    def test_cascade_usuario(self, usuario, flashcard):
        assert Flashcard.objects.count() == 1
        usuario.delete()
        assert Flashcard.objects.count() == 0


class TestReviewModel:
    def test_str(self, flashcard):
        r = Review.objects.create(flashcard=flashcard, programada_para=date(2026, 10, 18))
        assert str(r)  # no crashea

    def test_defaults(self, flashcard):
        r = Review.objects.create(flashcard=flashcard, programada_para=date(2026, 10, 18))
        assert r.intervalo_dias == 0
        assert r.facilidad == 2.5
        assert r.repeticiones == 0
        assert r.completada_en is None
        assert r.calidad_respuesta is None
        assert r.pendiente is True

    def test_cascade_flashcard(self, flashcard):
        Review.objects.create(flashcard=flashcard, programada_para=date(2026, 10, 18))
        assert Review.objects.count() == 1
        flashcard.delete()
        assert Review.objects.count() == 0