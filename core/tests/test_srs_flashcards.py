"""Tests de SRS: modelo, populate, dashboard, verificar, repaso."""
from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestFlashcardSRS(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, _ = User.objects.get_or_create(
            username="srs_test_user",
            defaults={"email": "srs@test.local"},
        )

    def test_modelo_tiene_campos_nuevos(self):
        Flashcard = apps.get_model("core", "Flashcard")
        campos = {f.name for f in Flashcard._meta.get_fields()}
        for c in ("explicacion", "ejemplo", "ejercicio", "respuesta_ejercicio", "fuente_id"):
            assert c in campos, f"falta {c}"

    def test_populate_creates_flashcards(self):
        from importlib import import_module
        from pathlib import Path
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "populate_fc",
            r"E:\02_proyectos\django-rhetorica\scripts\populate_flashcards_sintaxis.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        r = mod.populate(self.user, apply=True)
        assert r["creados"] == 100
        assert r["existentes"] == 0
        # Idempotente
        r2 = mod.populate(self.user, apply=True)
        assert r2["creados"] == 0
        assert r2["existentes"] == 100


class TestSRSVerificar(TestCase):
    @classmethod
    def setUpTestData(cls):
        from datetime import date
        Flashcard = apps.get_model("core", "Flashcard")
        Review = apps.get_model("core", "Review")
        cls.user, _ = User.objects.get_or_create(
            username="srs_v_user", defaults={"email": "v@t.local"}
        )
        fc = Flashcard.objects.create(
            estudiante=cls.user,
            frente="Constituyente sintáctico",
            reverso="Unidad",
            explicacion="Unidad que forma grupo",
            ejemplo="El niño come",
            ejercicio="¿Cuál es el SN en 'María estudia'?",
            respuesta_ejercicio="María",
            categoria_gramatical="Conceptos",
            tipo="regla",
            idioma="ES",
        )
        cls.review = Review.objects.create(
            flashcard=fc,
            programada_para=date.today(),
            intervalo_dias=1,
            facilidad=2.5,
            repeticiones=0,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_verificar_correcto(self):
        url = reverse("srs_verificar", args=[self.review.id])
        r = self.client.post(url, {"respuesta": "María"})
        assert r.status_code == 200
        data = r.json()
        assert data["aprobado"] is True
        assert data["similitud"] == 1.0

    def test_verificar_incorrecto(self):
        url = reverse("srs_verificar", args=[self.review.id])
        r = self.client.post(url, {"respuesta": "Juan"})
        assert r.status_code == 200
        data = r.json()
        assert data["aprobado"] is False
        assert data["esperada"] == "María"

    def test_verificar_vacio(self):
        url = reverse("srs_verificar", args=[self.review.id])
        r = self.client.post(url, {"respuesta": ""})
        assert r.status_code == 200
        assert r.json()["aprobado"] is False


class TestDashboardSRS(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, _ = User.objects.get_or_create(
            username="srs_dash_user", defaults={"email": "d@t.local"}
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_charts_en_context(self):
        r = self.client.get(reverse("srs_estadisticas"))
        assert r.status_code == 200
        assert "charts" in r.context
        for k in ("madurez", "facilidad", "intervalos", "retencion"):
            assert k in r.context["charts"], f"falta {k}"

    def test_repaso_renderiza_interactivo(self):
        r = self.client.get(reverse("srs_repaso"))
        assert r.status_code == 200
        # Si hay review, verificar botones SM-2
        if r.context.get("review"):
            html = r.content.decode("utf-8")
            assert "Verificar respuesta" in html
            assert "Ver pista" in html
            assert 'name="calidad"' in html