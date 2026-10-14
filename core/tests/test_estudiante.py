"""Tests de las vistas del panel del estudiante."""
import pytest
from django.utils import timezone

from core.models import Certificacion, CertificacionObtenida, Logro, LogroObtenido
from core.models_cursos import Curso, EvaluacionCurso, Leccion, Modulo, ProgresoUsuario


# ============================================================
# ACCESO
# ============================================================
class TestAccesoEstudiante:
    def test_dashboard_anonimo_redirige(self, cliente_anon):
        r = cliente_anon.get("/estudiante/")
        assert r.status_code in (301, 302)

    def test_dashboard_autenticado(self, cliente_est):
        assert cliente_est.get("/estudiante/").status_code == 200

    def test_cursos_anonimo(self, cliente_anon):
        assert cliente_anon.get("/estudiante/cursos/").status_code in (301, 302)

    def test_cursos_autenticado(self, cliente_est):
        assert cliente_est.get("/estudiante/cursos/").status_code == 200

    def test_evaluaciones(self, cliente_est):
        assert cliente_est.get("/estudiante/evaluaciones/").status_code == 200

    def test_logros(self, cliente_est):
        assert cliente_est.get("/estudiante/logros/").status_code == 200

    def test_certificados(self, cliente_est):
        assert cliente_est.get("/estudiante/certificados/").status_code == 200

    def test_estadisticas(self, cliente_est):
        assert cliente_est.get("/estudiante/estadisticas/").status_code == 200

    def test_ranking(self, cliente_est):
        assert cliente_est.get("/estudiante/ranking/").status_code == 200


# ============================================================
# DASHBOARD
# ============================================================
class TestDashboardEstudiante:
    def test_respuesta_html(self, cliente_est):
        r = cliente_est.get("/estudiante/")
        assert "text/html" in r["Content-Type"].lower()

    def test_html_no_vacio(self, cliente_est):
        r = cliente_est.get("/estudiante/")
        assert len(r.content) > 100


# ============================================================
# CURSOS
# ============================================================
class TestCursosEstudiante:
    def test_lista_200(self, cliente_est, curso):
        assert cliente_est.get("/estudiante/cursos/").status_code == 200

    def test_no_muestra_borradores(self, cliente_est, db, prof_user):
        Curso.objects.create(
            titulo="Oculto", slug="oculto",
            nivel="basico", estado="borrador", creado_por=prof_user,
        )
        r = cliente_est.get("/estudiante/cursos/")
        assert r.status_code == 200
        assert b"Oculto" not in r.content


# ============================================================
# LOGROS
# ============================================================
class TestLogrosEstudiante:
    def test_lista_vacia(self, cliente_est):
        assert cliente_est.get("/estudiante/logros/").status_code == 200

    def test_con_logro_obtenido(self, cliente_est, estudiante_user, logro):
        LogroObtenido.objects.create(
            user=estudiante_user, logro=logro,
            fecha_obtenida=timezone.now(),
        )
        r = cliente_est.get("/estudiante/logros/")
        assert r.status_code == 200


# ============================================================
# CERTIFICADOS
# ============================================================
class TestCertificadosEstudiante:
    def test_lista_vacia(self, cliente_est):
        assert cliente_est.get("/estudiante/certificados/").status_code == 200

    def test_con_certificado(self, cliente_est, estudiante_user, certificacion):
        CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=certificacion,
            codigo_verificacion="TEST-0001-01",
            url_verificacion="https://test.local/verificar/TEST-0001-01",
        )
        assert cliente_est.get("/estudiante/certificados/").status_code == 200


# ============================================================
# ESTADISTICAS Y RANKING
# ============================================================
class TestEstadisticasEstudiante:
    def test_estadisticas(self, cliente_est):
        assert cliente_est.get("/estudiante/estadisticas/").status_code == 200

    def test_ranking(self, cliente_est):
        assert cliente_est.get("/estudiante/ranking/").status_code == 200

    def test_ranking_anonimo(self, cliente_anon):
        r = cliente_anon.get("/estudiante/ranking/")
        assert r.status_code in (200, 301, 302)


# ============================================================
# PROGRESO
# ============================================================
class TestProgresoEstudiante:
    def test_progreso_en_leccion(self, cliente_est, estudiante_user, leccion):
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=90,
        )
        assert ProgresoUsuario.objects.filter(
            usuario=estudiante_user, completado=True
        ).count() == 1
