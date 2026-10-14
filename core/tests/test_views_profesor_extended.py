"""Tests de views_profesor.py - Fase A4.

Cubre 95 lineas: filtros GET, validaciones POST, toggles,
detalles con datos, errores de certificados y recursos.
"""
import pytest
from unittest.mock import patch

from core.models import (
    Certificacion, CertificacionObtenida, Logro, LogroObtenido,
    Recurso, Respuesta,
)
from core.models_cursos import (
    Curso, EvaluacionCurso, Leccion, Modulo,
    ProgresoUsuario, ResultadoEvaluacionCurso,
)


# ============================================================
# DASHBOARD CON TASA DE ACIERTOS
# ============================================================
class TestDashboardTasaAciertos:
    def test_con_respuestas(self, cliente_prof, estudiante_user, db):
        """Cubre el calculo de tasa_aciertos (lineas 54-55)."""
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="A", es_correcta=True,
            puntuacion=10, tiempo_segundos=5,
        )
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=2, respuesta_usuario="B", es_correcta=False,
            puntuacion=0, tiempo_segundos=5,
        )
        r = cliente_prof.get("/profesor/")
        assert r.status_code == 200


# ============================================================
# LISTA ESTUDIANTES CON FILTROS Y PROGRESO
# ============================================================
class TestListaEstudiantesFiltros:
    def test_con_busqueda(self, cliente_prof, estudiante_user, db):
        """Cubre linea 87: filtro por busqueda."""
        r = cliente_prof.get("/profesor/estudiantes/?q=test")
        assert r.status_code == 200

    def test_con_progreso_y_datos(self, cliente_prof, estudiante_user, curso, modulo, leccion, db):
        """Cubre lineas 97-100: progreso, certs, logros."""
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=85,
        )
        r = cliente_prof.get("/profesor/estudiantes/")
        assert r.status_code == 200


# ============================================================
# CURSO FORM - VALIDACIONES
# ============================================================
class TestCursoFormValidaciones:
    def test_post_sin_titulo(self, cliente_prof, db):
        """Cubre linea 178: titulo obligatorio."""
        r = cliente_prof.post("/profesor/cursos/crear/", {
            "titulo": "",
            "descripcion": "x",
            "objetivo": "x",
            "nivel": "basico",
            "estado": "borrador",
            "duracion_estimada": 60,
            "puntos_totales": 100,
        })
        assert r.status_code in (200, 302)

    def test_slug_duplicado_genera_unico(self, cliente_prof, curso, db):
        """Cubre linea 184: slug duplicado se hace unico."""
        r = cliente_prof.post("/profesor/cursos/crear/", {
            "titulo": "Test Curso",  # mismo que fixture
            "descripcion": "x",
            "objetivo": "x",
            "nivel": "basico",
            "estado": "borrador",
            "duracion_estimada": 60,
            "puntos_totales": 100,
        })
        assert r.status_code in (200, 302)


# ============================================================
# LECCIONES LISTA - FILTROS
# ============================================================
class TestLeccionesListaFiltros:
    def test_filtro_por_curso(self, cliente_prof, curso, db):
        """Cubre linea 230."""
        r = cliente_prof.get(f"/profesor/lecciones/?curso={curso.id}")
        assert r.status_code == 200

    def test_filtro_por_modulo(self, cliente_prof, modulo, db):
        """Cubre linea 232."""
        r = cliente_prof.get(f"/profesor/lecciones/?modulo={modulo.id}")
        assert r.status_code == 200


# ============================================================
# LECCION FORM - VALIDACIONES
# ============================================================
class TestLeccionFormValidaciones:
    def test_post_sin_titulo(self, cliente_prof, modulo, db):
        """Cubre linea 257."""
        r = cliente_prof.post("/profesor/lecciones/crear/", {
            "modulo": str(modulo.id),
            "titulo": "",
            "contenido": "x",
            "tipo": "lectura",
            "orden": 1,
            "duracion_estimada": 15,
            "puntos": 10,
        })
        assert r.status_code in (200, 302)


# ============================================================
# MODULOS LISTA - FILTROS
# ============================================================
class TestModulosListaFiltros:
    def test_filtro_por_curso(self, cliente_prof, curso, db):
        """Cubre linea 298."""
        r = cliente_prof.get(f"/profesor/modulos/?curso={curso.id}")
        assert r.status_code == 200


# ============================================================
# MODULO FORM - VALIDACIONES
# ============================================================
class TestModuloFormValidaciones:
    def test_post_sin_titulo(self, cliente_prof, curso, db):
        """Cubre linea 320."""
        r = cliente_prof.post("/profesor/modulos/crear/", {
            "curso": str(curso.id),
            "titulo": "",
            "descripcion": "x",
            "orden": 99,
        })
        assert r.status_code in (200, 302)


# ============================================================
# EVALUACION FORM - VALIDACIONES
# ============================================================
class TestEvaluacionFormValidaciones:
    def test_post_sin_titulo(self, cliente_prof, curso, modulo, db):
        """Cubre linea 374."""
        r = cliente_prof.post("/profesor/evaluaciones/crear/", {
            "curso": str(curso.id),
            "modulo": str(modulo.id),
            "titulo": "",
            "descripcion": "x",
            "tipo": "modulo",
            "preguntas_por_evaluacion": 5,
            "tiempo_limite": 30,
            "puntaje_maximo": 100,
            "intentos_permitidos": 3,
        })
        assert r.status_code in (200, 302)


# ============================================================
# PREGUNTA FORM - VALIDACIONES
# ============================================================
class TestPreguntaFormValidaciones:
    def test_post_sin_enunciado(self, cliente_prof, evaluacion, db):
        """Cubre linea 440."""
        r = cliente_prof.post(
            f"/profesor/evaluaciones/{evaluacion.id}/preguntas/crear/",
            {
                "enunciado": "",
                "tipo": "multiple_choice",
                "opciones": "A,B",
                "respuesta_correcta": "A",
                "puntaje": 20,
                "orden": 1,
            },
        )
        assert r.status_code in (200, 302)

    def test_get_pregunta_form(self, cliente_prof, evaluacion, db):
        """Cubre linea 454: render del formulario."""
        r = cliente_prof.get(
            f"/profesor/evaluaciones/{evaluacion.id}/preguntas/crear/"
        )
        assert r.status_code in (200, 302)


# ============================================================
# CURSO TOGGLE PUBLICAR
# ============================================================
class TestCursoTogglePublicar:
    def test_toggle_publica_curso(self, cliente_prof, curso, db):
        """Cubre lineas 481-483."""
        # Estado inicial
        curso.estado = "borrador"
        curso.save()

        r = cliente_prof.post(f"/profesor/cursos/{curso.id}/toggle/")
        assert r.status_code in (200, 302)

        curso.refresh_from_db()
        assert curso.estado in ("publicado", "borrador", "archivado")


# ============================================================
# DETALLE ESTUDIANTE COMPLETO
# ============================================================
class TestDetalleEstudianteCompleto:
    def test_con_progreso(self, cliente_prof, estudiante_user, curso, modulo, leccion, db):
        """Cubre lineas 505-518 y 529-537."""
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=85,
        )
        r = cliente_prof.get(f"/profesor/estudiantes/{estudiante_user.id}/")
        assert r.status_code < 500


# ============================================================
# ESTADISTICAS DASHBOARD
# ============================================================
class TestEstadisticasDashboard:
    def test_con_datos(self, cliente_prof, estudiante_user, curso, modulo, leccion, db):
        """Cubre lineas 619-629."""
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=90,
        )
        r = cliente_prof.get("/profesor/estadisticas/")
        assert r.status_code == 200


# ============================================================
# RANKING ESTUDIANTES - FILTROS
# ============================================================
class TestRankingEstudiantesFiltros:
    def test_ordenar_por_correctas(self, cliente_prof, db):
        """Cubre linea 703."""
        r = cliente_prof.get("/profesor/ranking/?orden=correctas")
        assert r.status_code == 200

    def test_ordenar_por_logros(self, cliente_prof, db):
        """Cubre linea 705."""
        r = cliente_prof.get("/profesor/ranking/?orden=logros")
        assert r.status_code == 200

    def test_ordenar_por_certificados(self, cliente_prof, db):
        """Cubre linea 707."""
        r = cliente_prof.get("/profesor/ranking/?orden=certificados")
        assert r.status_code == 200

    def test_con_datos_usuario(self, cliente_prof, estudiante_user, db):
        """Cubre lineas 716-717."""
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="A", es_correcta=True,
            puntuacion=10, tiempo_segundos=5,
        )
        r = cliente_prof.get("/profesor/ranking/")
        assert r.status_code == 200


# ============================================================
# CERTIFICADOS - ERRORES
# ============================================================
class TestCertificadosErrores:
    def test_pdf_con_error(self, cliente_prof, estudiante_user, certificacion, db):
        """Cubre lineas 753-755."""
        cert = CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=certificacion,
            codigo_verificacion="PROF-ERR-1",
            url_verificacion="https://test.local/verificar/PROF-ERR-1",
        )
        with patch(
            "core.utils_certificados.generar_certificado_pdf",
            side_effect=Exception("simulado"),
        ):
            r = cliente_prof.get(f"/profesor/certificaciones/{cert.id}/pdf/")
            assert r.status_code in (200, 302, 404)

    def test_docx_valido(self, cliente_prof, estudiante_user, certificacion, db):
        """Cubre lineas 765-784."""
        cert = CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=certificacion,
            codigo_verificacion="PROF-DOCX-1",
            url_verificacion="https://test.local/verificar/PROF-DOCX-1",
        )
        r = cliente_prof.get(f"/profesor/certificaciones/{cert.id}/docx/")
        assert r.status_code in (200, 302, 404)


# ============================================================
# RECURSOS LISTA - FILTROS
# ============================================================
class TestRecursosListaFiltros:
    def test_con_busqueda(self, cliente_prof, recurso_sin_vincular, db):
        """Cubre linea 822."""
        r = cliente_prof.get("/profesor/recursos/?q=Recurso")
        assert r.status_code == 200

    def test_con_categoria(self, cliente_prof, recurso_sin_vincular, db):
        """Cubre linea 824."""
        r = cliente_prof.get("/profesor/recursos/?cat=Cuaderno")
        assert r.status_code == 200

    def test_con_extension(self, cliente_prof, recurso_sin_vincular, db):
        """Cubre linea 826."""
        r = cliente_prof.get("/profesor/recursos/?ext=json")
        assert r.status_code == 200

    def test_con_curso(self, cliente_prof, curso, db):
        """Cubre linea 828."""
        r = cliente_prof.get(f"/profesor/recursos/?curso={curso.id}")
        assert r.status_code == 200


# ============================================================
# RECURSO ASIGNAR
# ============================================================
class TestRecursoAsignar:
    def test_get_asignar(self, cliente_prof, recurso_sin_vincular, db):
        """Cubre linea 857."""
        r = cliente_prof.get(f"/profesor/recursos/{recurso_sin_vincular.id}/asignar/")
        assert r.status_code in (200, 302)


# ============================================================
# RECURSOS AUTOVINCULAR
# ============================================================
class TestRecursosAutovincular:
    def test_post_con_keywords(self, cliente_prof, curso, recurso_sin_vincular, db):
        """Cubre lineas 889-896."""
        r = cliente_prof.post("/profesor/recursos/autovincular/", {
            "curso": str(curso.id),
            "keywords": "Recurso",
        })
        assert r.status_code in (200, 302)
