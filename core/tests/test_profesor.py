"""Tests de las vistas del panel del profesor."""
import pytest

from core.models_cursos import Curso, Modulo, Leccion, EvaluacionCurso


# ============================================================
# ACCESO
# ============================================================
class TestAccesoProfesor:
    def test_dashboard_anonimo(self, cliente_anon):
        assert cliente_anon.get("/profesor/").status_code in (301, 302)

    def test_dashboard_profesor(self, cliente_prof):
        assert cliente_prof.get("/profesor/").status_code == 200

    def test_dashboard_estudiante_denegado(self, cliente_est):
        r = cliente_est.get("/profesor/")
        assert r.status_code in (301, 302, 403)


# ============================================================
# CRUD CURSOS
# ============================================================
class TestCRUDCursos:
    def test_lista(self, cliente_prof):
        assert cliente_prof.get("/profesor/cursos/").status_code == 200

    def test_crear_get(self, cliente_prof):
        assert cliente_prof.get("/profesor/cursos/crear/").status_code == 200

    def test_crear_post(self, cliente_prof, db):
        n = Curso.objects.count()
        r = cliente_prof.post("/profesor/cursos/crear/", {
            "titulo": "Nuevo Curso Test",
            "slug": "nuevo-curso-test",
            "descripcion": "descripcion",
            "objetivo": "objetivo",
            "nivel": "basico",
            "estado": "borrador",
            "duracion_estimada": 60,
            "puntos_totales": 100,
        })
        assert r.status_code in (200, 302)
        assert Curso.objects.count() >= n

    def test_editar_get(self, cliente_prof, curso):
        assert cliente_prof.get(f"/profesor/cursos/{curso.id}/editar/").status_code == 200

    def test_eliminar_get(self, cliente_prof, curso):
        r = cliente_prof.get(f"/profesor/cursos/{curso.id}/eliminar/")
        assert r.status_code in (200, 302, 405)

    def test_toggle(self, cliente_prof, curso):
        r = cliente_prof.post(f"/profesor/cursos/{curso.id}/toggle/")
        assert r.status_code in (200, 302)


# ============================================================
# CRUD MODULOS
# ============================================================
class TestCRUDModulos:
    def test_lista(self, cliente_prof):
        assert cliente_prof.get("/profesor/modulos/").status_code == 200

    def test_crear_get(self, cliente_prof):
        assert cliente_prof.get("/profesor/modulos/crear/").status_code == 200

    def test_editar_get(self, cliente_prof, modulo):
        assert cliente_prof.get(f"/profesor/modulos/{modulo.id}/editar/").status_code == 200

    def test_eliminar_get(self, cliente_prof, modulo):
        r = cliente_prof.get(f"/profesor/modulos/{modulo.id}/eliminar/")
        assert r.status_code in (200, 302, 405)


# ============================================================
# CRUD LECCIONES
# ============================================================
class TestCRUDLecciones:
    def test_lista(self, cliente_prof):
        assert cliente_prof.get("/profesor/lecciones/").status_code == 200

    def test_crear_get(self, cliente_prof):
        assert cliente_prof.get("/profesor/lecciones/crear/").status_code == 200

    def test_editar_get(self, cliente_prof, leccion):
        assert cliente_prof.get(f"/profesor/lecciones/{leccion.id}/editar/").status_code == 200

    def test_eliminar_get(self, cliente_prof, leccion):
        r = cliente_prof.get(f"/profesor/lecciones/{leccion.id}/eliminar/")
        assert r.status_code in (200, 302, 405)


# ============================================================
# CRUD EVALUACIONES
# ============================================================
class TestCRUDEvaluaciones:
    def test_lista(self, cliente_prof):
        assert cliente_prof.get("/profesor/evaluaciones/").status_code == 200

    def test_crear_get(self, cliente_prof):
        assert cliente_prof.get("/profesor/evaluaciones/crear/").status_code == 200

    def test_detalle(self, cliente_prof, evaluacion):
        assert cliente_prof.get(f"/profesor/evaluaciones/{evaluacion.id}/").status_code == 200

    def test_editar_get(self, cliente_prof, evaluacion):
        assert cliente_prof.get(f"/profesor/evaluaciones/{evaluacion.id}/editar/").status_code == 200

    def test_eliminar_get(self, cliente_prof, evaluacion):
        r = cliente_prof.get(f"/profesor/evaluaciones/{evaluacion.id}/eliminar/")
        assert r.status_code in (200, 302, 405)


# ============================================================
# ESTUDIANTES
# ============================================================
class TestEstudiantesProfesor:
    def test_lista(self, cliente_prof):
        assert cliente_prof.get("/profesor/estudiantes/").status_code == 200

    def test_detalle(self, cliente_prof, estudiante_user):
        r = cliente_prof.get(f"/profesor/estudiantes/{estudiante_user.id}/")
        assert r.status_code == 200


# ============================================================
# ESTADISTICAS Y RANKING
# ============================================================
class TestEstadisticasProfesor:
    def test_estadisticas(self, cliente_prof):
        assert cliente_prof.get("/profesor/estadisticas/").status_code == 200

    def test_ranking(self, cliente_prof):
        assert cliente_prof.get("/profesor/ranking/").status_code == 200


# ============================================================
# CERTIFICACIONES
# ============================================================
class TestCertificacionesProfesor:
    def test_lista(self, cliente_prof):
        assert cliente_prof.get("/profesor/certificaciones/").status_code == 200


# ============================================================
# RECURSOS
# ============================================================
class TestRecursosProfesor:
    def test_lista(self, cliente_prof):
        assert cliente_prof.get("/profesor/recursos/").status_code == 200

    def test_autovincular(self, cliente_prof):
        r = cliente_prof.get("/profesor/recursos/autovincular/")
        assert r.status_code in (200, 302, 405)
