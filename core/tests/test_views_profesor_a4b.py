"""Tests A4b: cubrir los ultimos 4 bloques de views_profesor.py.

Llega la cobertura al 95%:
  - except Curso.DoesNotExist en detalle_estudiante_completo
  - loop de evaluaciones con resultados
  - except en certificado_docx
  - loop de autovincular con keywords
"""
import pytest
from unittest.mock import patch

from core.models import Certificacion, CertificacionObtenida, Recurso
from core.models_cursos import (
    Curso, Leccion, Modulo, ProgresoUsuario, EvaluacionCurso,
    ResultadoEvaluacionCurso,
)


# ============================================================
# Bloque 507-508: except Curso.DoesNotExist
# ============================================================
class TestDetalleEstudianteCursoBorrado:
    def test_curso_borrado_se_salta(
        self, cliente_prof, estudiante_user, curso, modulo, leccion, db
    ):
        """Simula que el curso apunta a un id inexistente."""
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=80,
        )
        # Hacer que Curso.objects.get lance DoesNotExist siempre
        with patch.object(
            Curso.objects, "get", side_effect=Curso.DoesNotExist
        ):
            r = cliente_prof.get(f"/profesor/estudiantes/{estudiante_user.id}/")
            assert r.status_code < 500


# ============================================================
# Bloque 532-537: loop de evaluaciones con resultados
# ============================================================
class TestDetalleEstudianteConEvaluaciones:
    def test_con_resultados_de_evaluaciones(
        self, cliente_prof, estudiante_user,
        curso, modulo, leccion, evaluacion, db
    ):
        """Estudiante con progreso + resultado de evaluacion."""
        # 1. Progreso
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=85,
        )
        # 2. Resultado de evaluacion
        ResultadoEvaluacionCurso.objects.create(
            evaluacion=evaluacion, usuario=estudiante_user,
            puntaje_obtenido=75, puntaje_maximo=100,
            respuestas={}, intento=1, completado=True,
        )
        r = cliente_prof.get(f"/profesor/estudiantes/{estudiante_user.id}/")
        assert r.status_code == 200


# ============================================================
# Bloque 775-777: except en certificado_docx
# ============================================================
class TestCertificadoDocxError:
    def test_docx_con_error(
        self, cliente_prof, estudiante_user, certificacion, db
    ):
        cert = CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=certificacion,
            codigo_verificacion="A4B-DOCX-1",
            url_verificacion="https://test.local/verificar/A4B-DOCX-1",
        )
        with patch(
            "core.utils_certificados.generar_certificado_docx",
            side_effect=Exception("simulado a4b"),
        ):
            r = cliente_prof.get(
                f"/profesor/certificaciones/{cert.id}/docx/"
            )
            assert r.status_code in (200, 302, 404)


# ============================================================
# Bloque 889-896: autovincular asigna recursos
# ============================================================
class TestRecursosAutovincularAsigna:
    def test_autovincular_asigna_recursos(self, cliente_prof, db):
        """Crea curso Morfologia + recurso con 'morfolog' para disparar el loop."""
        # 1. Curso con titulo exacto que esta en las reglas
        curso = Curso.objects.create(
            titulo="Morfología",
            slug="a4b-morfologia",
            nivel="basico",
            estado="publicado",
        )

        # 2. Recurso sin vincular con "morfolog" en el nombre
        recurso = Recurso.objects.create(
            nombre="Cuaderno de morfología del castellano A4b",
            slug="a4b-cuaderno-morfologia",
            archivo="test/a4b-morfolog.html",
            categoria="Cuaderno",
            extension="html",
            tamaño_bytes=100,
        )

        # 3. Verificar que empieza sin curso
        assert recurso.curso_id is None

        # 4. POST a autovincular
        r = cliente_prof.post("/profesor/recursos/autovincular/")
        assert r.status_code in (200, 302)

        # 5. Verificar que ahora SI esta asignado (cubre lineas 889-896)
        recurso.refresh_from_db()
        assert recurso.curso_id == curso.id

    def test_autovincular_con_recurso_sin_match(self, cliente_prof, db):
        """Recurso con nombre sin keywords no se asigna."""
        Curso.objects.create(
            titulo="Morfología",
            slug="a4b-morf-2",
            nivel="basico",
            estado="publicado",
        )
        recurso = Recurso.objects.create(
            nombre="ZZZ sin match ZZ",
            slug="a4b-sin-match",
            archivo="test/sin-match.html",
            categoria="Cuaderno",
            extension="html",
            tamaño_bytes=50,
        )
        r = cliente_prof.post("/profesor/recursos/autovincular/")
        assert r.status_code in (200, 302)

        recurso.refresh_from_db()
        assert recurso.curso_id is None
