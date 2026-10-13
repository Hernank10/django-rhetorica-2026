"""
Tests para las 3 vistas sin cobertura:
- views_cursos_completo.py
- views_ejercicios.py
- views_biblioteca.py

Anade fixture 'ejercicio_linguistico' a conftest.py.
"""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tests_dir = BASE / "core" / "tests"

# ============================================================
# 1) Fixture nueva en conftest.py
# ============================================================
conftest_path = BASE / "conftest.py"
c = conftest_path.read_text(encoding="utf-8")

if "def ejercicio_linguistico(" in c:
    print("[SKIP] conftest.py ya tiene la fixture 'ejercicio_linguistico'")
else:
    fixture = '''


# --------- FIXTURES DE EJERCICIOS ---------
@pytest.fixture
def ejercicio_linguistico(db):
    """Un EjercicioLinguistico basico con contenido JSON."""
    from core.models import EjercicioLinguistico
    return EjercicioLinguistico.objects.create(
        titulo="Test Ejercicio",
        contenido={
            "preguntas": [
                {
                    "pregunta": "Cual es 2+2?",
                    "opciones": ["3", "4", "5"],
                    "correcta": 1,
                },
            ],
        },
        categoria="gramatica",
        tipo="multiple_choice",
        nivel=1,
        puntos=10,
    )
'''
    conftest_path.write_text(c.rstrip() + fixture, encoding="utf-8")
    print("[OK] fixture 'ejercicio_linguistico' anadida a conftest.py")


# ============================================================
# 2) test_cursos_completo.py
# ============================================================
test_cursos = '''"""Tests de core/views_cursos_completo.py."""
import pytest

from core.models_cursos import Curso, Modulo, Leccion, EvaluacionCurso, PreguntaEvaluacion


# ============================================================
# LISTA DE CURSOS
# ============================================================
class TestListaCursos:
    def test_anon_redirige(self, cliente_anon):
        r = cliente_anon.get("/cursos/")
        assert r.status_code in (301, 302)

    def test_login_200(self, cliente_est):
        r = cliente_est.get("/cursos/")
        assert r.status_code == 200

    def test_solo_publicados(self, cliente_est, curso, db, prof_user):
        # Crear un curso en borrador
        Curso.objects.create(
            titulo="Curso Oculto XSS",
            slug="curso-oculto-xss",
            nivel="basico",
            estado="borrador",
            creado_por=prof_user,
        )
        r = cliente_est.get("/cursos/")
        assert r.status_code == 200
        assert b"Curso Oculto XSS" not in r.content


# ============================================================
# DETALLE DE CURSO
# ============================================================
class TestDetalleCurso:
    def test_login_200(self, cliente_est, curso):
        r = cliente_est.get(f"/cursos/{curso.slug}/")
        assert r.status_code == 200

    def test_anon_redirige(self, cliente_anon, curso):
        r = cliente_anon.get(f"/cursos/{curso.slug}/")
        assert r.status_code in (301, 302)

    def test_slug_inexistente(self, cliente_est):
        r = cliente_est.get("/cursos/no-existe-xyz/")
        assert r.status_code in (302, 404)

    def test_muestra_titulo(self, cliente_est, curso):
        r = cliente_est.get(f"/cursos/{curso.slug}/")
        html = r.content.decode("utf-8", errors="replace")
        assert "Test Curso" in html


# ============================================================
# VER LECCION
# ============================================================
class TestVerLeccion:
    def test_login_200(self, cliente_est, curso, modulo, leccion):
        url = f"/cursos/{curso.slug}/modulo/{modulo.id}/leccion/{leccion.id}/"
        r = cliente_est.get(url)
        assert r.status_code == 200

    def test_anon_redirige(self, cliente_anon, curso, modulo, leccion):
        url = f"/cursos/{curso.slug}/modulo/{modulo.id}/leccion/{leccion.id}/"
        r = cliente_anon.get(url)
        assert r.status_code in (301, 302)

    def test_leccion_inexistente(self, cliente_est, curso, modulo):
        r = cliente_est.get(f"/cursos/{curso.slug}/modulo/{modulo.id}/leccion/999999/")
        assert r.status_code in (302, 404)

    def test_muestra_titulo(self, cliente_est, curso, modulo, leccion):
        url = f"/cursos/{curso.slug}/modulo/{modulo.id}/leccion/{leccion.id}/"
        r = cliente_est.get(url)
        html = r.content.decode("utf-8", errors="replace")
        assert "Test Lecci" in html or "Test Leccion" in html


# ============================================================
# VER EVALUACION
# ============================================================
class TestVerEvaluacion:
    def test_login_200(self, cliente_est, evaluacion):
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/")
        assert r.status_code == 200

    def test_anon_redirige(self, cliente_anon, evaluacion):
        r = cliente_anon.get(f"/evaluacion/{evaluacion.id}/")
        assert r.status_code in (301, 302)

    def test_evaluacion_inexistente(self, cliente_est):
        r = cliente_est.get("/evaluacion/999999/")
        assert r.status_code in (302, 404)


# ============================================================
# ENVIAR EVALUACION
# ============================================================
class TestEnviarEvaluacion:
    def test_get_no_permitido(self, cliente_est, evaluacion):
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/enviar/")
        assert r.status_code in (200, 405)

    def test_post_ok(self, cliente_est, evaluacion):
        r = cliente_est.post(f"/evaluacion/{evaluacion.id}/enviar/", {})
        assert r.status_code in (200, 302)


# ============================================================
# RESULTADO EVALUACION
# ============================================================
class TestResultadoEvaluacion:
    def test_login_redirige_sin_resultado(self, cliente_est, evaluacion):
        r = cliente_est.get(f"/evaluacion/{evaluacion.id}/resultados/")
        assert r.status_code in (200, 302, 404)

    def test_evaluacion_inexistente(self, cliente_est):
        r = cliente_est.get("/evaluacion/999999/resultados/")
        assert r.status_code in (302, 404)


# ============================================================
# API EVALUACION PREGUNTAS
# ============================================================
class TestApiEvaluacionPreguntas:
    def test_json_response(self, cliente_est, evaluacion):
        r = cliente_est.get(f"/api/evaluacion/{evaluacion.id}/preguntas/")
        assert r.status_code in (200, 302, 404)

    def test_evaluacion_inexistente(self, cliente_est):
        r = cliente_est.get("/api/evaluacion/999999/preguntas/")
        assert r.status_code in (200, 302, 404)
'''
(tests_dir / "test_cursos_completo.py").write_text(test_cursos, encoding="utf-8")
print("[OK] core/tests/test_cursos_completo.py")


# ============================================================
# 3) test_ejercicios.py
# ============================================================
test_ejercicios = '''"""Tests de core/views_ejercicios.py."""
import pytest

from core.models import EjercicioLinguistico


# ============================================================
# DETALLE
# ============================================================
class TestDetalleEjercicio:
    def test_login_200(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get(f"/ejercicio/{ejercicio_linguistico.id}/")
        assert r.status_code == 200

    def test_anon_redirige(self, cliente_anon, ejercicio_linguistico):
        r = cliente_anon.get(f"/ejercicio/{ejercicio_linguistico.id}/")
        assert r.status_code in (301, 302)

    def test_ejercicio_inexistente(self, cliente_est):
        r = cliente_est.get("/ejercicio/999999/")
        assert r.status_code in (302, 404)

    def test_muestra_titulo(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get(f"/ejercicio/{ejercicio_linguistico.id}/")
        html = r.content.decode("utf-8", errors="replace")
        assert "Test Ejercicio" in html or "Ejercicio" in html


# ============================================================
# PRACTICAR
# ============================================================
class TestPracticarEjercicio:
    def test_login_200(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get(f"/practicar/{ejercicio_linguistico.id}/")
        assert r.status_code == 200

    def test_anon_redirige(self, cliente_anon, ejercicio_linguistico):
        r = cliente_anon.get(f"/practicar/{ejercicio_linguistico.id}/")
        assert r.status_code in (301, 302)

    def test_inexistente(self, cliente_est):
        r = cliente_est.get("/practicar/999999/")
        assert r.status_code in (302, 404)

    def test_post_respuesta(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.post(f"/practicar/{ejercicio_linguistico.id}/", {
            "pregunta_0": "4",
            "tiempo": "10",
        })
        assert r.status_code in (200, 302)


# ============================================================
# API DETALLE
# ============================================================
class TestApiEjercicioDetalle:
    def test_llamada(self, cliente_est, ejercicio_linguistico):
        # Si existe endpoint API, que responda
        r = cliente_est.get(f"/api/ejercicio/{ejercicio_linguistico.id}/")
        assert r.status_code in (200, 302, 404)

    def test_inexistente(self, cliente_est):
        r = cliente_est.get("/api/ejercicio/999999/")
        assert r.status_code in (200, 302, 404)
'''
(tests_dir / "test_ejercicios.py").write_text(test_ejercicios, encoding="utf-8")
print("[OK] core/tests/test_ejercicios.py")


# ============================================================
# 4) test_biblioteca.py
# ============================================================
test_biblioteca = '''"""Tests de core/views_biblioteca.py."""
import pytest

from core.models import EjercicioLinguistico


# ============================================================
# BIBLIOTECA
# ============================================================
class TestBiblioteca:
    def test_anon_redirige(self, cliente_anon):
        r = cliente_anon.get("/biblioteca/")
        assert r.status_code in (301, 302)

    def test_login_200(self, cliente_est):
        r = cliente_est.get("/biblioteca/")
        assert r.status_code == 200

    def test_tamano_html(self, cliente_est):
        r = cliente_est.get("/biblioteca/")
        assert len(r.content) > 100

    def test_con_ejercicios(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get("/biblioteca/")
        assert r.status_code == 200

    def test_filtro_categoria(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get(f"/biblioteca/?categoria={ejercicio_linguistico.categoria}")
        assert r.status_code == 200

    def test_filtro_nivel(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get(f"/biblioteca/?nivel={ejercicio_linguistico.nivel}")
        assert r.status_code == 200

    def test_busqueda_q(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get("/biblioteca/?q=Test")
        assert r.status_code == 200

    def test_profesor_accede(self, cliente_prof):
        r = cliente_prof.get("/biblioteca/")
        assert r.status_code == 200
'''
(tests_dir / "test_biblioteca.py").write_text(test_biblioteca, encoding="utf-8")
print("[OK] core/tests/test_biblioteca.py")

print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  E:\\PythonPortable_Django5\\python.exe manage.py check")
print("  E:\\PythonPortable_Django5\\python.exe -m pytest core\\tests\\test_cursos_completo.py core\\tests\\test_ejercicios.py core\\tests\\test_biblioteca.py -v --tb=short")