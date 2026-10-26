"""Tests del servicio de certificaciones automaticas."""
from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Certificacion, CertificacionObtenida, Respuesta

try:
    from core.models_cursos import Curso, Modulo, Leccion, ProgresoUsuario
except ImportError:
    from core.models import Curso, Modulo, Leccion, ProgresoUsuario

from core.services.certificaciones import (
    cumple_requisitos, get_user_stats, verificar_y_otorgar,
)


def _crear_leccion(titulo="Leccion test", puntos=10, contenido="x"):
    """Crea Curso -> Modulo -> Leccion con orden incremental (evita UNIQUE)."""
    curso, _ = Curso.objects.get_or_create(titulo="Curso test")
    modulo, _ = Modulo.objects.get_or_create(curso=curso, titulo="Modulo test")
    orden = Leccion.objects.filter(modulo=modulo).count() + 1
    return Leccion.objects.create(
        modulo=modulo,
        titulo=titulo,
        contenido=contenido,
        puntos=puntos,
        orden=orden,
    )


class TestGetUserStats(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("test_u1", password="x")
        for i in range(3):
            _crear_leccion(titulo=f"Leccion {i}", puntos=10)
        lecciones = list(Leccion.objects.all())
        ProgresoUsuario.objects.create(
            usuario=cls.user, leccion=lecciones[0],
            completado=True, puntaje_obtenido=10,
        )
        ProgresoUsuario.objects.create(
            usuario=cls.user, leccion=lecciones[1],
            completado=True, puntaje_obtenido=20,
        )
        ProgresoUsuario.objects.create(
            usuario=cls.user, leccion=lecciones[2],
            completado=False, puntaje_obtenido=0,
        )
        for i in range(4):
            Respuesta.objects.create(
                user=cls.user, tipo_ejercicio="x", item_id=1,
                respuesta_usuario="x", es_correcta=(i < 3),
                puntuacion=10 if i < 3 else 0,
            )

    def test_stats_lecciones(self):
        self.assertEqual(get_user_stats(self.user)["lecciones"], 2)

    def test_stats_puntos(self):
        self.assertEqual(get_user_stats(self.user)["puntos"], 30)

    def test_stats_tasa(self):
        self.assertEqual(get_user_stats(self.user)["tasa"], 75.0)

    def test_stats_sin_actividad(self):
        user_vacio = User.objects.create_user("test_empty", password="x")
        stats = get_user_stats(user_vacio)
        self.assertEqual(stats["lecciones"], 0)
        self.assertEqual(stats["puntos"], 0)
        self.assertEqual(stats["tasa"], 0.0)


class TestCumpleRequisitos(TestCase):
    def test_vacio(self):
        self.assertTrue(cumple_requisitos({"lecciones": 0, "puntos": 0, "tasa": 0}, {}))

    def test_todos_cumplen(self):
        stats = {"lecciones": 10, "puntos": 100, "tasa": 80}
        reqs = {"lecciones": 5, "puntos": 50, "tasa": 75}
        self.assertTrue(cumple_requisitos(stats, reqs))

    def test_falta_uno(self):
        stats = {"lecciones": 3, "puntos": 100, "tasa": 80}
        reqs = {"lecciones": 5, "puntos": 50, "tasa": 75}
        self.assertFalse(cumple_requisitos(stats, reqs))

    def test_reqs_no_dict(self):
        self.assertFalse(cumple_requisitos({"lecciones": 10}, None))
        self.assertFalse(cumple_requisitos({"lecciones": 10}, "invalid"))


class TestVerificarYOtorgar(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("test_award", password="x")
        for i in range(2):
            lec = _crear_leccion(titulo=f"L{i}", puntos=10)
            ProgresoUsuario.objects.create(
                usuario=cls.user, leccion=lec,
                completado=True, puntaje_obtenido=25,
            )
        cls.cert_facil = Certificacion.objects.create(
            nombre="Facil", descripcion="x", nivel="bronce",
            requisitos={"lecciones": 1}, activa=True,
        )
        cls.cert_dificil = Certificacion.objects.create(
            nombre="Dificil", descripcion="x", nivel="diamante",
            requisitos={"lecciones": 100}, activa=True,
        )

    def test_otorga_cert_facil(self):
        nuevas = verificar_y_otorgar(self.user)
        self.assertEqual(len(nuevas), 1)
        self.assertEqual(nuevas[0].id, self.cert_facil.id)
        self.assertTrue(
            CertificacionObtenida.objects.filter(
                user=self.user, certificacion=self.cert_facil
            ).exists()
        )

    def test_no_otorga_cert_dificil(self):
        verificar_y_otorgar(self.user)
        self.assertFalse(
            CertificacionObtenida.objects.filter(
                user=self.user, certificacion=self.cert_dificil
            ).exists()
        )

    def test_idempotente(self):
        verificar_y_otorgar(self.user)
        verificar_y_otorgar(self.user)
        verificar_y_otorgar(self.user)
        n = CertificacionObtenida.objects.filter(user=self.user).count()
        self.assertEqual(n, 1)

    def test_dry_run_no_crea(self):
        nuevas = verificar_y_otorgar(self.user, dry_run=True)
        self.assertEqual(len(nuevas), 1)
        self.assertFalse(
            CertificacionObtenida.objects.filter(user=self.user).exists()
        )

    def test_signal_dispara_otorgamiento(self):
        user2 = User.objects.create_user("test_signal", password="x")
        lec = _crear_leccion(titulo="L_sig", puntos=10)
        ProgresoUsuario.objects.create(
            usuario=user2, leccion=lec, completado=True, puntaje_obtenido=25,
        )
        self.assertTrue(
            CertificacionObtenida.objects.filter(
                user=user2, certificacion=self.cert_facil
            ).exists()
        )