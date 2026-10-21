"""Tests de paginacion en ejercicios_biblioteca."""
from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestBibliotecaPaginada(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 50 ejercicios propios -> 3 paginas con per_page=24
        E = apps.get_model("core", "EjercicioLinguistico")
        for i in range(50):
            E.objects.create(
                titulo=f"Ej Pag {i:03d}",
                contenido={"pregunta": f"p{i}", "respuesta": f"r{i}"},
                categoria="test_pag",
                tipo="multiple",
                nivel=1,
                puntos=10,
                es_adaptativo=False,
                es_redaccion=False,
                idioma="ES",
            )

    def setUp(self):
        # Crear/asegurar el user en setUp (no en setUpTestData) y usar
        # force_login() que no depende del password.
        self.user, _ = User.objects.get_or_create(
            username="bib_test_user",
            defaults={"email": "bib@test.local"},
        )
        self.user.set_password("Test1234!")
        self.user.save()
        self.client.force_login(self.user)

    def test_primera_pagina_24(self):
        r = self.client.get(reverse("ejercicios_biblioteca"))
        assert r.status_code == 200, f"esperado 200, obtuve {r.status_code}"
        assert len(r.context["ejercicios"]) == 24

    def test_page_1_y_2_diferentes(self):
        r1 = self.client.get(reverse("ejercicios_biblioteca") + "?page=1")
        r2 = self.client.get(reverse("ejercicios_biblioteca") + "?page=2")
        assert r1.status_code == 200
        assert r2.status_code == 200
        ids_1 = [e.id for e in r1.context["ejercicios"]]
        ids_2 = [e.id for e in r2.context["ejercicios"]]
        assert len(ids_1) > 0
        assert len(ids_2) > 0
        assert set(ids_1).isdisjoint(set(ids_2))

    def test_page_overflow_devuelve_ultima(self):
        r = self.client.get(reverse("ejercicios_biblioteca") + "?page=99999")
        assert r.status_code == 200
        assert r.context["page_obj"].number == r.context["page_obj"].paginator.num_pages

    def test_contiene_paginacion_en_html(self):
        r = self.client.get(reverse("ejercicios_biblioteca"))
        assert r.status_code == 200
        html = r.content.decode("utf-8")
        assert "pagination" in html, "no hay clase 'pagination' en HTML"
        assert "page=2" in html or "page=3" in html