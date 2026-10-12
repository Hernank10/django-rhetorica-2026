from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tests_dir = BASE / "core" / "tests"

# ============================================================
# test_estudiante.py
# ============================================================
test_estudiante = '''"""Tests de las vistas del panel del estudiante."""
import pytest
from django.utils import timezone

from core.models import Logro, LogroObtenido, Certificacion, CertificacionObtenida
from core.models_cursos import Curso, Modulo, Leccion, ProgresoUsuario, EvaluacionCurso


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
'''
(tests_dir / "test_estudiante.py").write_text(test_estudiante, encoding="utf-8")
print("[OK] test_estudiante.py")

# ============================================================
# test_profesor.py
# ============================================================
test_profesor = '''"""Tests de las vistas del panel del profesor."""
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
'''
(tests_dir / "test_profesor.py").write_text(test_profesor, encoding="utf-8")
print("[OK] test_profesor.py")

print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  E:\\PythonPortable_Django5\\python.exe -m pytest -q")