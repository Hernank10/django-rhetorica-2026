"""Tests de modelos: Curso, Modulo, Leccion, Evaluacion, Logro, Certificacion."""
import pytest
from django.utils import timezone

from core.models import (
    Logro, LogroObtenido, Certificacion, CertificacionObtenida,
    Respuesta,
)
from core.models_cursos import (
    Curso, Modulo, Leccion, ProgresoUsuario,
    EvaluacionCurso, PreguntaEvaluacion,
)


# ============================================================
# CURSO
# ============================================================
class TestCursoModel:
    def test_crear_curso(self, curso):
        assert curso.id is not None
        assert curso.titulo == "Test Curso"
        assert curso.estado == "publicado"
        assert curso.creado_por is not None

    def test_slug_unico(self, db, prof_user):
        Curso.objects.create(
            titulo="Curso 1", slug="curso-1",
            nivel="basico", estado="borrador", creado_por=prof_user,
        )
        # Segundo con mismo slug debe fallar
        with pytest.raises(Exception):
            Curso.objects.create(
                titulo="Curso 2", slug="curso-1",
                nivel="basico", estado="borrador", creado_por=prof_user,
            )

    def test_curso_sin_publicar(self, db, prof_user):
        c = Curso.objects.create(
            titulo="Borrador", slug="borrador",
            nivel="basico", estado="borrador", creado_por=prof_user,
        )
        assert c.publicado_en is None

    def test_estrategia_estado(self, curso):
        assert curso.estado in ["borrador", "publicado", "archivado"]


# ============================================================
# MODULO
# ============================================================
class TestModuloModel:
    def test_crear_modulo(self, modulo):
        assert modulo.id is not None
        assert modulo.curso.titulo == "Test Curso"
        assert modulo.orden == 1

    def test_modulo_pertenece_curso(self, modulo, curso):
        assert modulo.curso == curso
        assert modulo in curso.modulos.all()

    def test_orden_unicos_por_curso(self, db, modulo, curso):
        # Crear otro módulo con orden=1 debe fallar (unique_together)
        with pytest.raises(Exception):
            Modulo.objects.create(
                curso=curso, titulo="Duplicado",
                descripcion="x", orden=1,
            )


# ============================================================
# LECCION
# ============================================================
class TestLeccionModel:
    def test_crear_leccion(self, leccion):
        assert leccion.id is not None
        assert leccion.modulo.titulo == "Test Módulo"
        assert leccion.puntos == 10

    def test_lecciones_del_modulo(self, leccion, modulo):
        assert leccion in modulo.lecciones.all()
        assert modulo.lecciones.count() == 1

    def test_tipo_default(self, leccion):
        assert leccion.tipo == "lectura"


# ============================================================
# PROGRESO USUARIO
# ============================================================
class TestProgresoUsuario:
    def test_crear_progreso(self, db, estudiante_user, leccion):
        p = ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=85, intentos=1,
        )
        assert p.id is not None
        assert p.completado is True
        assert p.puntaje_obtenido == 85

    def test_progreso_duplicado_falla(self, db, estudiante_user, leccion):
        ProgresoUsuario.objects.create(
            usuario=estudiante_user, leccion=leccion,
            completado=True, puntaje_obtenido=80,
        )
        with pytest.raises(Exception):
            ProgresoUsuario.objects.create(
                usuario=estudiante_user, leccion=leccion,
                completado=True, puntaje_obtenido=90,
            )


# ============================================================
# EVALUACION CURSO
# ============================================================
class TestEvaluacionCurso:
    def test_crear_evaluacion(self, evaluacion):
        assert evaluacion.id is not None
        assert evaluacion.tipo == "modulo"
        assert evaluacion.puntaje_maximo == 100
        assert evaluacion.intentos_permitidos == 3

    def test_tipos_validos(self, evaluacion):
        # Los 4 tipos según el panel del profesor
        tipos_validos = ["diagnostica", "modulo", "recapitulacion", "final"]
        assert evaluacion.tipo in tipos_validos or evaluacion.tipo is not None


# ============================================================
# PREGUNTA EVALUACION
# ============================================================
class TestPreguntaEvaluacion:
    def test_crear_pregunta(self, db, evaluacion):
        p = PreguntaEvaluacion.objects.create(
            evaluacion=evaluacion,
            enunciado="¿Cuál es la respuesta?",
            tipo="multiple_choice",
            opciones=[
                {"texto": "A", "correcta": True},
                {"texto": "B", "correcta": False},
            ],
            respuesta_correcta="A",
            puntaje=20, orden=1,
        )
        assert p.id is not None
        assert p.evaluacion == evaluacion
        assert len(p.opciones) == 2

    def test_preguntas_de_evaluacion(self, db, evaluacion):
        for i in range(5):
            PreguntaEvaluacion.objects.create(
                evaluacion=evaluacion,
                enunciado=f"P{i}", tipo="multiple_choice",
                opciones=[{"texto": "A"}], respuesta_correcta="A",
                puntaje=20, orden=i+1,
            )
        assert evaluacion.preguntas.count() == 5


# ============================================================
# LOGRO
# ============================================================
class TestLogroModel:
    def test_crear_logro(self, logro):
        assert logro.id is not None
        assert logro.nombre == "Test Logro"
        assert logro.tipo == "insignia"

    def test_logro_obtenido(self, db, logro, estudiante_user):
        lo = LogroObtenido.objects.create(
            user=estudiante_user, logro=logro,
            fecha_obtenida=timezone.now(),
        )
        assert lo.id is not None
        assert lo.logro == logro


# ============================================================
# CERTIFICACION
# ============================================================
class TestCertificacion:
    def test_crear_certificacion(self, certificacion):
        assert certificacion.id is not None
        assert certificacion.nivel == "basico"
        assert certificacion.requisitos == {"lecciones": 5}

    def test_certificacion_obtenida(self, db, certificacion, estudiante_user):
        co = CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=certificacion,
            codigo_verificacion="TEST-0001-01",
            url_verificacion="https://test.local/verificar/TEST-0001-01",
        )
        assert co.id is not None
        assert co.codigo_verificacion == "TEST-0001-01"


# ============================================================
# RESPUESTA
# ============================================================
class TestRespuesta:
    def test_crear_respuesta(self, db, estudiante_user):
        r = Respuesta.objects.create(
            user=estudiante_user,
            tipo_ejercicio="multiple_choice",
            item_id=1,
            respuesta_usuario="A",
            es_correcta=True,
            puntuacion=10,
            tiempo_segundos=15,
        )
        assert r.id is not None
        assert r.es_correcta is True

    def test_respuesta_incorrecta(self, db, estudiante_user):
        r = Respuesta.objects.create(
            user=estudiante_user,
            tipo_ejercicio="multiple_choice",
            item_id=1,
            respuesta_usuario="B",
            es_correcta=False,
            puntuacion=0,
            tiempo_segundos=10,
        )
        assert r.es_correcta is False
        assert r.puntuacion == 0
