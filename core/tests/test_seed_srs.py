"""Test del management command seed_srs."""
import pytest
from django.core.management import call_command

from core.models import Flashcard, Review


@pytest.mark.django_db
class TestSeedSRS:
    def test_seed_crea_35_flashcards(self, django_user_model):
        user = django_user_model.objects.create_user(username="seed_test")
        call_command("seed_srs", "seed_test", verbosity=0)
        assert Flashcard.objects.filter(estudiante=user).count() == 35

    def test_seed_es_idempotente(self, django_user_model):
        user = django_user_model.objects.create_user(username="seed_idem")
        call_command("seed_srs", "seed_idem", verbosity=0)
        call_command("seed_srs", "seed_idem", verbosity=0)
        assert Flashcard.objects.filter(estudiante=user).count() == 35

    def test_seed_programa_reviews(self, django_user_model):
        user = django_user_model.objects.create_user(username="seed_rev")
        call_command("seed_srs", "seed_rev", verbosity=0)
        assert Review.objects.filter(
            flashcard__estudiante=user, completada_en__isnull=True
        ).count() == 35

    def test_seed_usuario_inexistente_no_crashea(self, capsys):
        call_command("seed_srs", "no_existe", verbosity=0)
        out = capsys.readouterr().out
        assert "no existe" in out.lower() or "Usuario no existe" in out