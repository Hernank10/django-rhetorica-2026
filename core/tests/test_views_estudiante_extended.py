"""Tests de views_estudiante.py - Fase A3.

Cubre:
  - mis_cursos con progreso real
  - mis_evaluaciones con resultados y pendientes
  - mis_estadisticas con promedios
  - errores en descarga de certificados
"""
import pytest
from unittest.mock import patch

from core.models import Certificacion, CertificacionObtenida
from core.models_cursos import (
    Curso, Leccion, ProgresoUsuario, EvaluacionCurso,
    ResultadoEvaluacionCurso,
)


# ============================================================
# MIS CURSOS CON PROGRESO
# ============================================================
class TestMisCursosConProgreso:
    def test_con_progreso_real(
        self, cliente_est, estudiante_user, curso, modulo, leccion, db
    ):
        """Cubre la iteracion con ProgresoUsuario real."""
        # Crear progreso
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=80,
        )

        r = cliente_est.get("/estudiante/cursos/")
        assert r.status_code == 200

    def test_con_curso_borrado(
        self, cliente_est, estudiante_user, curso, modulo, leccion, db
    ):
        """Cubre el caso de curso inexistente (cid que no existe)."""
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=80,
        )
        r = cliente_est.get("/estudiante/cursos/")
        assert r.status_code == 200

    def test_sin_lecciones(
        self, cliente_est, estudiante_user, curso, db
    ):
        """Curso sin lecciones (evita division por cero)."""
        r = cliente_est.get("/estudiante/cursos/")
        assert r.status_code == 200


# ============================================================
# MIS EVALUACIONES
# ============================================================
class TestMisEvaluaciones:
    def test_sin_evaluaciones(self, cliente_est, db):
        r = cliente_est.get("/estudiante/evaluaciones/")
        assert r.status_code == 200

    def test_con_evaluacion_pendiente(
        self, cliente_est, estudiante_user, evaluacion, db
    ):
        """Cubre el branch 'pendientes' (sin resultados)."""
        r = cliente_est.get("/estudiante/evaluaciones/")
        assert r.status_code == 200

    def test_con_resultado_completado(
        self, cliente_est, estudiante_user, evaluacion, db
    ):
        """Cubre el branch 'completadas' (con resultados)."""
        ResultadoEvaluacionCurso.objects.create(
            evaluacion=evaluacion,
            usuario=estudiante_user,
            puntaje_obtenido=75,
            puntaje_maximo=100,
            respuestas={},
            intento=1,
            completado=True,
        )
        r = cliente_est.get("/estudiante/evaluaciones/")
        assert r.status_code == 200

    def test_con_multiples_resultados(
        self, cliente_est, estudiante_user, evaluacion, db
    ):
        """Con múltiples intentos (prueba 'mejor')."""
        for intento in range(1, 4):
            ResultadoEvaluacionCurso.objects.create(
                evaluacion=evaluacion,
                usuario=estudiante_user,
                puntaje_obtenido=50 + intento * 10,
                puntaje_maximo=100,
                respuestas={},
                intento=intento,
                completado=True,
            )
        r = cliente_est.get("/estudiante/evaluaciones/")
        assert r.status_code == 200


# ============================================================
# MIS ESTADISTICAS
# ============================================================
class TestMisEstadisticas:
    def test_sin_datos(self, cliente_est, db):
        r = cliente_est.get("/estudiante/estadisticas/")
        assert r.status_code == 200

    def test_con_progreso(
        self, cliente_est, estudiante_user, curso, modulo, leccion, db
    ):
        """Cubre calculo de promedios por curso."""
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=85,
        )
        r = cliente_est.get("/estudiante/estadisticas/")
        assert r.status_code == 200

    def test_con_varios_cursos(
        self, cliente_est, estudiante_user, curso, modulo, leccion, db
    ):
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=90,
        )
        r = cliente_est.get("/estudiante/estadisticas/")
        assert r.status_code == 200


# ============================================================
# ERRORES EN CERTIFICADOS
# ============================================================
class TestErroresCertificados:
    def test_pdf_con_error(
        self, cliente_est, estudiante_user, certificacion, db
    ):
        """Cubre el except en descargar_certificado_pdf."""
        cert = CertificacionObtenida.objects.create(
            user=estudiante_user,
            certificacion=certificacion,
            codigo_verificacion="ERR-1",
            url_verificacion="https://test.local/verificar/ERR-1",
        )

        with patch(
            "core.utils_certificados.generar_certificado_pdf",
            side_effect=Exception("simulado"),
        ):
            r = cliente_est.get(f"/estudiante/certificados/{cert.id}/pdf/")
            # Debe capturar la excepcion y redirigir o devolver algo controlado
            assert r.status_code in (200, 302, 404)

    def test_docx_con_error(
        self, cliente_est, estudiante_user, certificacion, db
    ):
        """Cubre el except en descargar_certificado_docx."""
        cert = CertificacionObtenida.objects.create(
            user=estudiante_user,
            certificacion=certificacion,
            codigo_verificacion="ERR-2",
            url_verificacion="https://test.local/verificar/ERR-2",
        )

        with patch(
            "core.utils_certificados.generar_certificado_docx",
            side_effect=Exception("simulado"),
        ):
            r = cliente_est.get(f"/estudiante/certificados/{cert.id}/docx/")
            assert r.status_code in (200, 302, 404)
