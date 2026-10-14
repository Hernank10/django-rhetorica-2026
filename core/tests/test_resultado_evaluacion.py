"""Tests del fix de resultado_evaluacion.

Verifica que:
  1) enviar_evaluacion crea ResultadoEvaluacionCurso
  2) enviar_evaluacion redirige a resultado_evaluacion
  3) resultado_evaluacion renderiza con datos
  4) resultado_evaluacion renderiza sin datos (estado vacio)
  5) El template ya no crashea
"""
import pytest

from core.models_cursos import (
    EvaluacionCurso,
    PreguntaEvaluacion,
    ResultadoEvaluacionCurso,
)


# ============================================================
# FIXTURES LOCALES
# ============================================================
@pytest.fixture
def evaluacion_con_preguntas(db, evaluacion):
    """Evaluacion con 2 preguntas de 50 pts cada una."""
    PreguntaEvaluacion.objects.create(
        evaluacion=evaluacion,
        enunciado="Cual es 2+2?",
        tipo="multiple_choice",
        opciones=["3", "4", "5"],
        respuesta_correcta="4",
        puntaje=50,
        orden=1,
    )
    PreguntaEvaluacion.objects.create(
        evaluacion=evaluacion,
        enunciado="Cual es la capital de Francia?",
        tipo="multiple_choice",
        opciones=["Madrid", "Paris", "Roma"],
        respuesta_correcta="Paris",
        puntaje=50,
        orden=2,
    )
    return evaluacion


# ============================================================
# ENVIAR EVALUACION
# ============================================================
class TestEnviarEvaluacionGuardaResultado:
    def test_crea_resultado(self, cliente_est, evaluacion_con_preguntas, estudiante_user):
        preguntas = list(evaluacion_con_preguntas.preguntas.all().order_by("orden"))
        respuestas = {f"pregunta_{p.id}": p.respuesta_correcta for p in preguntas}

        r = cliente_est.post(
            f"/evaluacion/{evaluacion_con_preguntas.id}/enviar/",
            respuestas,
        )
        assert r.status_code == 302

        resultado = ResultadoEvaluacionCurso.objects.filter(
            evaluacion=evaluacion_con_preguntas,
            usuario=estudiante_user,
        ).first()
        assert resultado is not None
        assert resultado.completado is True

    def test_puntaje_correcto_todo_bien(self, cliente_est, evaluacion_con_preguntas, estudiante_user):
        preguntas = list(evaluacion_con_preguntas.preguntas.all().order_by("orden"))
        respuestas = {f"pregunta_{p.id}": p.respuesta_correcta for p in preguntas}

        cliente_est.post(
            f"/evaluacion/{evaluacion_con_preguntas.id}/enviar/",
            respuestas,
        )

        resultado = ResultadoEvaluacionCurso.objects.get(
            evaluacion=evaluacion_con_preguntas,
            usuario=estudiante_user,
        )
        assert resultado.puntaje_obtenido == 100
        assert resultado.puntaje_maximo == 100

    def test_puntaje_parcial(self, cliente_est, evaluacion_con_preguntas, estudiante_user):
        preguntas = list(evaluacion_con_preguntas.preguntas.all().order_by("orden"))
        # Solo 1 respuesta correcta
        respuestas = {
            f"pregunta_{preguntas[0].id}": preguntas[0].respuesta_correcta,
            f"pregunta_{preguntas[1].id}": "respuesta_incorrecta",
        }

        cliente_est.post(
            f"/evaluacion/{evaluacion_con_preguntas.id}/enviar/",
            respuestas,
        )

        resultado = ResultadoEvaluacionCurso.objects.get(
            evaluacion=evaluacion_con_preguntas,
            usuario=estudiante_user,
        )
        assert resultado.puntaje_obtenido == 50

    def test_redirige_a_resultado(self, cliente_est, evaluacion_con_preguntas):
        preguntas = list(evaluacion_con_preguntas.preguntas.all().order_by("orden"))
        respuestas = {f"pregunta_{p.id}": p.respuesta_correcta for p in preguntas}

        r = cliente_est.post(
            f"/evaluacion/{evaluacion_con_preguntas.id}/enviar/",
            respuestas,
        )
        assert r.status_code == 302
        assert f"/evaluacion/{evaluacion_con_preguntas.id}/resultados/" in r.headers.get("Location", "")

    def test_get_redirige_a_lista_cursos(self, cliente_est, evaluacion_con_preguntas):
        # GET a enviar no permite, redirige a /cursos/
        r = cliente_est.get(f"/evaluacion/{evaluacion_con_preguntas.id}/enviar/")
        assert r.status_code == 302
        assert "/cursos/" in r.headers.get("Location", "")


# ============================================================
# RESULTADO EVALUACION
# ============================================================
class TestResultadoEvaluacionTemplate:
    def test_sin_resultado_renderiza(self, cliente_est, evaluacion_con_preguntas):
        # Sin haber enviado nada: debe mostrar estado vacio
        r = cliente_est.get(f"/evaluacion/{evaluacion_con_preguntas.id}/resultados/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        assert "Aun no has completado" in html or "no has completado" in html.lower()

    def test_con_resultado_muestra_puntaje(
        self, cliente_est, evaluacion_con_preguntas, estudiante_user, db
    ):
        # Crear resultado manualmente
        ResultadoEvaluacionCurso.objects.create(
            evaluacion=evaluacion_con_preguntas,
            usuario=estudiante_user,
            puntaje_obtenido=75,
            puntaje_maximo=100,
            respuestas={},
            intento=1,
            completado=True,
        )

        r = cliente_est.get(f"/evaluacion/{evaluacion_con_preguntas.id}/resultados/")
        assert r.status_code == 200
        html = r.content.decode("utf-8", errors="replace")
        assert "75" in html
        assert "100" in html

    def test_aprobado_si_60_porciento(
        self, cliente_est, evaluacion_con_preguntas, estudiante_user, db
    ):
        ResultadoEvaluacionCurso.objects.create(
            evaluacion=evaluacion_con_preguntas,
            usuario=estudiante_user,
            puntaje_obtenido=80,
            puntaje_maximo=100,
            respuestas={},
            intento=1,
            completado=True,
        )

        r = cliente_est.get(f"/evaluacion/{evaluacion_con_preguntas.id}/resultados/")
        html = r.content.decode("utf-8", errors="replace")
        assert "aprobada" in html.lower()

    def test_no_aprobado_si_menos_60(
        self, cliente_est, evaluacion_con_preguntas, estudiante_user, db
    ):
        ResultadoEvaluacionCurso.objects.create(
            evaluacion=evaluacion_con_preguntas,
            usuario=estudiante_user,
            puntaje_obtenido=40,
            puntaje_maximo=100,
            respuestas={},
            intento=1,
            completado=True,
        )

        r = cliente_est.get(f"/evaluacion/{evaluacion_con_preguntas.id}/resultados/")
        html = r.content.decode("utf-8", errors="replace")
        assert "no aprobada" in html.lower()

    def test_anon_redirige(self, cliente_anon, evaluacion_con_preguntas):
        r = cliente_anon.get(f"/evaluacion/{evaluacion_con_preguntas.id}/resultados/")
        assert r.status_code in (301, 302)

    def test_evaluacion_inexistente(self, cliente_est):
        r = cliente_est.get("/evaluacion/999999/resultados/")
        assert r.status_code in (302, 404)
