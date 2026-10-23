"""Tests del sistema de notificaciones."""
from unittest.mock import patch

from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase

from core.services.notificaciones import (
    contar_no_leidas,
    crear_notificacion,
    marcar_todas_leidas,
)


class TestModeloNotificacion(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="n_test", password="x")

    def test_crear_basica(self):
        n, created = crear_notificacion(
            user=self.user, tipo="sistema", titulo="Hola", referencia="test_1"
        )
        assert created is True
        assert n.leida is False
        assert str(n).startswith("n_test - Hola")

    def test_idempotente(self):
        n1, c1 = crear_notificacion(
            user=self.user, tipo="sistema", titulo="A", referencia="r_1"
        )
        n2, c2 = crear_notificacion(
            user=self.user, tipo="sistema", titulo="A", referencia="r_1"
        )
        assert c1 is True and c2 is False
        assert n1.id == n2.id
        assert apps.get_model("core", "Notificacion").objects.count() == 1

    def test_contar_y_marcar_leidas(self):
        crear_notificacion(user=self.user, tipo="sistema", titulo="A", referencia="a1")
        crear_notificacion(user=self.user, tipo="sistema", titulo="B", referencia="b1")
        assert contar_no_leidas(self.user) == 2
        n = marcar_todas_leidas(self.user)
        assert n == 2
        assert contar_no_leidas(self.user) == 0


class TestSignalsNotificaciones(TestCase):
    @classmethod
    def setUpTestData(cls):
        Curso = apps.get_model("core", "Curso")
        Modulo = apps.get_model("core", "Modulo")
        Leccion = apps.get_model("core", "Leccion")

        cls.user = User.objects.create_user(username="n_sig", password="x")
        cls.curso = Curso.objects.create(
            titulo="Curso Sig", slug="curso-sig",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="publicado",
        )
        cls.modulo = Modulo.objects.create(curso=cls.curso, titulo="M1", orden=1)
        cls.lec1 = Leccion.objects.create(
            modulo=cls.modulo, titulo="L1", contenido="c", tipo="teoria", orden=1
        )
        cls.lec2 = Leccion.objects.create(
            modulo=cls.modulo, titulo="L2", contenido="c", tipo="teoria", orden=2
        )

    def test_completar_leccion_crea_notif(self):
        ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
        Notificacion = apps.get_model("core", "Notificacion")

        ProgresoUsuario.objects.create(
            usuario=self.user, leccion=self.lec1, completado=True
        )
        notifs = Notificacion.objects.filter(
            user=self.user, tipo="leccion_completada"
        )
        assert notifs.count() == 1
        assert "L1" in notifs.first().titulo

    def test_completar_todas_lecciones_curso_crea_notif_curso(self):
        ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
        Notificacion = apps.get_model("core", "Notificacion")

        ProgresoUsuario.objects.create(
            usuario=self.user, leccion=self.lec1, completado=True
        )
        # Solo 1 de 2: no debe haber notif curso
        assert Notificacion.objects.filter(
            user=self.user, tipo="curso_completado"
        ).count() == 0

        ProgresoUsuario.objects.create(
            usuario=self.user, leccion=self.lec2, completado=True
        )
        # Ahora 2 de 2: sí debe haber
        notifs = Notificacion.objects.filter(
            user=self.user, tipo="curso_completado"
        )
        assert notifs.count() == 1
        assert "Curso Sig" in notifs.first().titulo

    def test_certificacion_crea_notif(self):
        Certificacion = apps.get_model("core", "Certificacion")
        CertificacionObtenida = apps.get_model("core", "CertificacionObtenida")
        Notificacion = apps.get_model("core", "Notificacion")

        cert = Certificacion.objects.create(
            nombre="Cert Test",
            descripcion="d",
            nivel="bronce",
            requisitos={},
            imagen="c.png",
            activa=True,
        )
        CertificacionObtenida.objects.create(
            user=self.user, certificacion=cert, codigo_verificacion="ABC123"
        )
        notifs = Notificacion.objects.filter(user=self.user, tipo="certificacion")
        assert notifs.count() == 1
        assert "Cert Test" in notifs.first().titulo

    def test_logro_crea_notif(self):
        Logro = apps.get_model("core", "Logro")
        LogroObtenido = apps.get_model("core", "LogroObtenido")
        Notificacion = apps.get_model("core", "Notificacion")

        logro = Logro.objects.create(
            nombre="Logro Test",
            descripcion="d",
            tipo="insignia",
            icono="i.png",
            color="#000",
            puntos_requeridos=100,
            nivel_requerido=1,
            ejercicios_completados_requeridos=5,
            tasa_aciertos_requerida=0.7,
        )
        LogroObtenido.objects.create(user=self.user, logro=logro)
        notifs = Notificacion.objects.filter(user=self.user, tipo="logro")
        assert notifs.count() == 1
        assert "Logro Test" in notifs.first().titulo

    def test_signal_falla_no_rompe_flujo(self):
        ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")

        with patch(
            "core.signals_progreso.crear_notificacion",
            side_effect=Exception("boom"),
        ):
            prog = ProgresoUsuario.objects.create(
                usuario=self.user, leccion=self.lec1, completado=True
            )
            assert prog.id is not None
            assert prog.completado is True