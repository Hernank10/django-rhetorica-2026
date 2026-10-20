"""Tests del hub (/) — index.html reescrito."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestHubAnonimo(TestCase):
    def test_get_ok(self):
        r = self.client.get(reverse("index"))
        assert r.status_code == 200

    def test_contiene_login_y_registro(self):
        r = self.client.get(reverse("index"))
        c = r.content.decode("utf-8")
        assert "Iniciar Sesi" in c or "login" in c.lower()
        assert "Registrarse" in c or "registro" in c.lower()

    def test_no_muestra_modulos_anonimo(self):
        r = self.client.get(reverse("index"))
        c = r.content.decode("utf-8")
        # Los links a módulos solo aparecen si autenticado
        assert "/sintaxis/parafrasis/" not in c


class TestHubAutenticado(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="hub_est_test",
            password="Test1234!",
        )
        self.client.login(username="hub_est_test", password="Test1234!")

    def test_get_ok(self):
        r = self.client.get(reverse("index"))
        assert r.status_code == 200

    def test_contiene_links_modulos(self):
        r = self.client.get(reverse("index"))
        c = r.content.decode("utf-8")
        for url in (
            "/pos/",
            "/sintaxis/parafrasis/",
            "/sintaxis/parafrasis/registro/",
            "/filologia/",
            "/lectura/",
            "/redaccion/",
            "/estudiante/srs/repaso/",
            "/corpus/",
        ):
            assert url in c, f"falta link {url}"

    def test_no_contiene_admin_si_no_staff(self):
        r = self.client.get(reverse("index"))
        c = r.content.decode("utf-8")
        assert "/admin/" not in c
        assert "/profesor/" not in c


class TestHubStaff(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username="hub_admin_test",
            password="Test1234!",
            is_staff=True,
            is_superuser=True,
        )
        self.client.login(username="hub_admin_test", password="Test1234!")

    def test_contiene_admin_y_profesor(self):
        r = self.client.get(reverse("index"))
        c = r.content.decode("utf-8")
        assert "/admin/" in c
        assert "/profesor/" in c

    def test_contiene_analytics(self):
        r = self.client.get(reverse("index"))
        c = r.content.decode("utf-8")
        assert "/profesor/analytics/" in c