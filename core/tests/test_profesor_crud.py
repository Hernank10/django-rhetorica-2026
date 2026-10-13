"""Tests CRUD de views_profesor.py: crear/editar/eliminar."""
import pytest

from core.models_cursos import (
    Curso, Modulo, Leccion, EvaluacionCurso, PreguntaEvaluacion,
)


# ============================================================
# CRUD CURSOS
# ============================================================
class TestCRUDCurso:
    def test_crear_post(self, cliente_prof, db, prof_user):
        antes = Curso.objects.count()
        r = cliente_prof.post("/profesor/cursos/crear/", {
            "titulo": "Nuevo Curso Test",
            "descripcion": "desc",
            "objetivo": "obj",
            "nivel": "basico",
            "estado": "borrador",
            "duracion_estimada": 60,
            "puntos_totales": 100,
        })
        assert r.status_code in (200, 302)
        assert Curso.objects.count() > antes

    def test_editar_post(self, cliente_prof, curso):
        r = cliente_prof.post(f"/profesor/cursos/{curso.id}/editar/", {
            "titulo": "Titulo Editado",
            "descripcion": "nueva desc",
            "objetivo": "nuevo obj",
            "nivel": "basico",
            "estado": "publicado",
            "duracion_estimada": 90,
            "puntos_totales": 200,
        })
        assert r.status_code in (200, 302)
        curso.refresh_from_db()
        assert curso.titulo == "Titulo Editado"

    def test_eliminar_post(self, cliente_prof, curso):
        pk = curso.id
        r = cliente_prof.post(f"/profesor/cursos/{pk}/eliminar/")
        assert r.status_code in (200, 302)
        assert not Curso.objects.filter(id=pk).exists()

    def test_toggle_publicar(self, cliente_prof, curso):
        estado_inicial = curso.estado
        r = cliente_prof.get(f"/profesor/cursos/{curso.id}/toggle/")
        assert r.status_code in (200, 302)
        curso.refresh_from_db()
        assert curso.estado != estado_inicial


# ============================================================
# CRUD MODULOS
# ============================================================
class TestCRUDModulo:
    def test_crear_post(self, cliente_prof, curso, db):
        r = cliente_prof.post("/profesor/modulos/crear/", {
            "curso": str(curso.id),
            "titulo": "Nuevo Modulo Test",
            "descripcion": "desc",
            "orden": 5,
        })
        assert r.status_code in (200, 302)
        assert Modulo.objects.filter(titulo="Nuevo Modulo Test").exists()

    def test_editar_post(self, cliente_prof, modulo):
        r = cliente_prof.post(f"/profesor/modulos/{modulo.id}/editar/", {
            "curso": str(modulo.curso.id),
            "titulo": "Modulo Editado",
            "descripcion": "nueva desc",
            "orden": 2,
        })
        assert r.status_code in (200, 302)
        modulo.refresh_from_db()
        assert modulo.titulo == "Modulo Editado"

    def test_eliminar_post(self, cliente_prof, modulo):
        pk = modulo.id
        r = cliente_prof.post(f"/profesor/modulos/{pk}/eliminar/")
        assert r.status_code in (200, 302)
        assert not Modulo.objects.filter(id=pk).exists()


# ============================================================
# CRUD LECCIONES
# ============================================================
class TestCRUDLeccion:
    def test_crear_post(self, cliente_prof, modulo, db):
        r = cliente_prof.post("/profesor/lecciones/crear/", {
            "modulo": str(modulo.id),
            "titulo": "Nueva Leccion Test",
            "contenido": "<p>Contenido</p>",
            "tipo": "lectura",
            "orden": 5,
            "duracion_estimada": 20,
            "puntos": 15,
        })
        assert r.status_code in (200, 302)
        assert Leccion.objects.filter(titulo="Nueva Leccion Test").exists()

    def test_editar_post(self, cliente_prof, leccion):
        r = cliente_prof.post(f"/profesor/lecciones/{leccion.id}/editar/", {
            "modulo": str(leccion.modulo.id),
            "titulo": "Leccion Editada",
            "contenido": "<p>Nuevo contenido</p>",
            "tipo": "lectura",
            "orden": 3,
            "duracion_estimada": 25,
            "puntos": 20,
        })
        assert r.status_code in (200, 302)
        leccion.refresh_from_db()
        assert leccion.titulo == "Leccion Editada"

    def test_eliminar_post(self, cliente_prof, leccion):
        pk = leccion.id
        r = cliente_prof.post(f"/profesor/lecciones/{pk}/eliminar/")
        assert r.status_code in (200, 302)
        assert not Leccion.objects.filter(id=pk).exists()


# ============================================================
# CRUD EVALUACIONES
# ============================================================
class TestCRUDEvaluacion:
    def test_crear_post(self, cliente_prof, curso, modulo, db):
        r = cliente_prof.post("/profesor/evaluaciones/crear/", {
            "curso": str(curso.id),
            "modulo": str(modulo.id),
            "titulo": "Nueva Evaluacion Test",
            "descripcion": "desc",
            "tipo": "modulo",
            "preguntas_por_evaluacion": 5,
            "tiempo_limite": 30,
            "puntaje_maximo": 100,
            "intentos_permitidos": 3,
        })
        assert r.status_code in (200, 302)
        assert EvaluacionCurso.objects.filter(titulo="Nueva Evaluacion Test").exists()

    def test_editar_post(self, cliente_prof, evaluacion):
        r = cliente_prof.post(f"/profesor/evaluaciones/{evaluacion.id}/editar/", {
            "curso": str(evaluacion.curso.id),
            "modulo": str(evaluacion.modulo.id),
            "titulo": "Evaluacion Editada",
            "descripcion": "nueva desc",
            "tipo": "modulo",
            "preguntas_por_evaluacion": 10,
            "tiempo_limite": 45,
            "puntaje_maximo": 100,
            "intentos_permitidos": 2,
        })
        assert r.status_code in (200, 302)
        evaluacion.refresh_from_db()
        assert evaluacion.titulo == "Evaluacion Editada"

    def test_eliminar_post(self, cliente_prof, evaluacion):
        pk = evaluacion.id
        r = cliente_prof.post(f"/profesor/evaluaciones/{pk}/eliminar/")
        assert r.status_code in (200, 302)
        assert not EvaluacionCurso.objects.filter(id=pk).exists()


# ============================================================
# CRUD PREGUNTAS
# ============================================================
class TestCRUDPregunta:
    def test_crear_post(self, cliente_prof, evaluacion, db):
        r = cliente_prof.post(
            f"/profesor/evaluaciones/{evaluacion.id}/preguntas/crear/",
            {
                "enunciado": "Cual es 2+2?",
                "tipo": "multiple_choice",
                "opciones": '["3","4","5"]',
                "respuesta_correcta": "4",
                "puntaje": 20,
                "orden": 1,
            },
        )
        assert r.status_code in (200, 302)
        assert PreguntaEvaluacion.objects.filter(enunciado="Cual es 2+2?").exists()

    def test_editar_post(self, cliente_prof, evaluacion, db):
        p = PreguntaEvaluacion.objects.create(
            evaluacion=evaluacion,
            enunciado="Pregunta original",
            tipo="multiple_choice",
            opciones=["A", "B"],
            respuesta_correcta="A",
            puntaje=20,
            orden=1,
        )
        r = cliente_prof.post(
            f"/profesor/evaluaciones/{evaluacion.id}/preguntas/{p.id}/editar/",
            {
                "enunciado": "Pregunta editada",
                "tipo": "multiple_choice",
                "opciones": '["A","B"]',
                "respuesta_correcta": "B",
                "puntaje": 30,
                "orden": 1,
            },
        )
        assert r.status_code in (200, 302)
        p.refresh_from_db()
        assert p.enunciado == "Pregunta editada"

    def test_eliminar_post(self, cliente_prof, evaluacion, db):
        p = PreguntaEvaluacion.objects.create(
            evaluacion=evaluacion,
            enunciado="Pregunta a borrar",
            tipo="multiple_choice",
            opciones=["A"],
            respuesta_correcta="A",
            puntaje=20,
            orden=1,
        )
        pk = p.id
        r = cliente_prof.post(
            f"/profesor/evaluaciones/{evaluacion.id}/preguntas/{pk}/eliminar/"
        )
        assert r.status_code in (200, 302)
        assert not PreguntaEvaluacion.objects.filter(id=pk).exists()


# ============================================================
# RECURSOS PROFESOR
# ============================================================
class TestRecursosProfesor:
    def test_asignar_recurso_a_curso(self, cliente_prof, recurso_sin_vincular, curso):
        r = cliente_prof.post(
            f"/profesor/recursos/{recurso_sin_vincular.id}/asignar/",
            {"curso": str(curso.id)},
        )
        assert r.status_code in (200, 302)
        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.curso_id == curso.id

    def test_autovincular_get(self, cliente_prof, db):
        r = cliente_prof.get("/profesor/recursos/autovincular/")
        assert r.status_code in (200, 302)

    def test_autovincular_post(self, cliente_prof, db):
        r = cliente_prof.post("/profesor/recursos/autovincular/", {})
        assert r.status_code in (200, 302)
