"""Tests de vistas y AJAX de notificaciones."""
import json

from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestListaNotificaciones(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="notif_u", password="x")

    def setUp(self):
        self.client.force_login(self.user)

    def test_sin_login_redirige(self):
        self.client.logout()
        r = self.client.get(reverse("notificaciones:lista"))
        assert r.status_code == 302
        assert "login" in r.url

    def test_vacia_muestra_estado(self):
        r = self.client.get(reverse("notificaciones:lista"))
        assert r.status_code == 200
        html = r.content.decode("utf-8")
        assert "No tienes notificaciones" in html

    def test_con_notif_muestra_en_lista(self):
        from core.services.notificaciones import crear_notificacion
        crear_notificacion(
            user=self.user, tipo="sistema",
            titulo="Notif test lista", referencia="test_lista_1",
        )
        r = self.client.get(reverse("notificaciones:lista"))
        assert r.status_code == 200
        html = r.content.decode("utf-8")
        assert "Notif test lista" in html

    def test_filtro_no_leidas(self):
        from core.services.notificaciones import crear_notificacion
        n1, _ = crear_notificacion(
            user=self.user, tipo="sistema", titulo="Notif A leida", referencia="f_a"
        )
        crear_notificacion(
            user=self.user, tipo="sistema", titulo="Notif B sin leer", referencia="f_b"
        )
        n1.leida = True
        n1.save(update_fields=["leida"])

        r = self.client.get(reverse("notificaciones:lista") + "?filtro=no_leidas")
        assert r.status_code == 200
        html = r.content.decode("utf-8")
        assert "Notif B sin leer" in html
        assert "Notif A leida" not in html


class TestAjaxNotificaciones(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="notif_ajax", password="x")

    def setUp(self):
        self.client.force_login(self.user)

    def test_ajax_contador(self):
        from core.services.notificaciones import crear_notificacion
        crear_notificacion(
            user=self.user, tipo="sistema", titulo="N1", referencia="c_1"
        )
        crear_notificacion(
            user=self.user, tipo="sistema", titulo="N2", referencia="c_2"
        )
        r = self.client.get(reverse("notificaciones:ajax_contador"))
        assert r.status_code == 200
        data = json.loads(r.content)
        assert data["count"] == 2

    def test_ajax_marcar_todas(self):
        from core.services.notificaciones import crear_notificacion
        crear_notificacion(
            user=self.user, tipo="sistema", titulo="N1", referencia="mt_1"
        )
        crear_notificacion(
            user=self.user, tipo="sistema", titulo="N2", referencia="mt_2"
        )
        r = self.client.post(reverse("notificaciones:ajax_marcar_todas"))
        assert r.status_code == 200
        data = json.loads(r.content)
        assert data["ok"] is True
        assert data["marcadas"] == 2

        Notificacion = apps.get_model("core", "Notificacion")
        assert Notificacion.objects.filter(
            user=self.user, leida=False
        ).count() == 0

    def test_ajax_marcar_todas_get_rechazado(self):
        r = self.client.get(reverse("notificaciones:ajax_marcar_todas"))
        assert r.status_code == 405

    def test_ajax_marcar_id(self):
        from core.services.notificaciones import crear_notificacion
        n1, _ = crear_notificacion(
            user=self.user, tipo="sistema", titulo="N1", referencia="mi_1"
        )
        n2, _ = crear_notificacion(
            user=self.user, tipo="sistema", titulo="N2", referencia="mi_2"
        )
        r = self.client.post(
            reverse("notificaciones:ajax_marcar_id", args=[n1.id])
        )
        assert r.status_code == 200
        data = json.loads(r.content)
        assert data["ok"] is True
        assert data["count"] == 1

        n1.refresh_from_db()
        n2.refresh_from_db()
        assert n1.leida is True
        assert n2.leida is False

    def test_ajax_marcar_id_otro_usuario_rechazado(self):
        other = User.objects.create_user(username="other_notif", password="x")
        from core.services.notificaciones import crear_notificacion
        n_other, _ = crear_notificacion(
            user=other, tipo="sistema", titulo="Otro", referencia="otro_1"
        )
        r = self.client.post(
            reverse("notificaciones:ajax_marcar_id", args=[n_other.id])
        )
        assert r.status_code in (403, 404)