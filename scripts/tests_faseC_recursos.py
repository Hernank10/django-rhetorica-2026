"""
FASE C - Tests de vinculacion de recursos.

1) Anade fixtures 'recurso' y 'recurso_vinculado' a conftest.py
2) Crea core/tests/test_recursos.py con ~22 tests
"""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) Fixtures en conftest.py
# ============================================================
conftest_path = BASE / "conftest.py"
c = conftest_path.read_text(encoding="utf-8")

if "def recurso(" in c:
    print("[SKIP] conftest.py ya tiene la fixture 'recurso'")
else:
    fixtures = '''


# --------- FIXTURES DE RECURSOS ---------
@pytest.fixture
def recurso(db, prof_user, curso):
    """Un Recurso basico sin vincular."""
    from core.models import Recurso
    return Recurso.objects.create(
        nombre="Recurso Test",
        slug="recurso-test",
        archivo="test/recurso.html",
        categoria="Cuaderno",
        extension="html",
        tamaño_bytes=1234,
        curso=curso,
    )


@pytest.fixture
def recurso_vinculado(db, prof_user, curso):
    """Un Recurso ya vinculado a un curso."""
    from core.models import Recurso
    return Recurso.objects.create(
        nombre="Recurso Vinculado",
        slug="recurso-vinculado",
        archivo="test/vinculado.html",
        categoria="Tecnicas",
        extension="html",
        tamaño_bytes=2048,
        curso=curso,
        orden=1,
        destacado=True,
    )


@pytest.fixture
def recurso_sin_vincular(db, prof_user):
    """Un Recurso sin curso/modulo/leccion/evaluacion."""
    from core.models import Recurso
    return Recurso.objects.create(
        nombre="Recurso Libre",
        slug="recurso-libre",
        archivo="test/libre.html",
        categoria="Flota",
        extension="json",
        tamaño_bytes=512,
    )
'''
    conftest_path.write_text(c.rstrip() + fixtures, encoding="utf-8")
    print("[OK] fixtures 'recurso', 'recurso_vinculado', 'recurso_sin_vincular' anadidas a conftest.py")


# ============================================================
# 2) core/tests/test_recursos.py
# ============================================================
test_recursos = '''"""Tests de vinculacion de recursos a curso/modulo/leccion/evaluacion."""
import pytest

from core.models import Recurso
from core.models_cursos import Curso, Modulo, Leccion, EvaluacionCurso


# ============================================================
# VINCULAR
# ============================================================
class TestVinculacionRecurso:
    def test_get_formulario(self, cliente_prof, recurso):
        r = cliente_prof.get(f"/recursos/{recurso.slug}/vincular/")
        assert r.status_code == 200

    def test_vincular_a_curso(self, cliente_prof, recurso_sin_vincular, curso):
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": str(curso.id),
            "modulo": "",
            "leccion": "",
            "evaluacion_curso": "",
            "ejercicio": "",
            "orden": "0",
        })
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.curso_id == curso.id

    def test_vincular_a_modulo(self, cliente_prof, recurso_sin_vincular, modulo):
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": "",
            "modulo": str(modulo.id),
            "leccion": "",
            "evaluacion_curso": "",
            "ejercicio": "",
            "orden": "0",
        })
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.modulo_id == modulo.id

    def test_vincular_a_leccion(self, cliente_prof, recurso_sin_vincular, leccion):
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": "",
            "modulo": "",
            "leccion": str(leccion.id),
            "evaluacion_curso": "",
            "ejercicio": "",
            "orden": "0",
        })
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.leccion_id == leccion.id

    def test_vincular_a_evaluacion(self, cliente_prof, recurso_sin_vincular, evaluacion):
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": "",
            "modulo": "",
            "leccion": "",
            "evaluacion_curso": str(evaluacion.id),
            "ejercicio": "",
            "orden": "0",
        })
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.evaluacion_curso_id == evaluacion.id

    def test_vincular_con_orden_y_destacado(self, cliente_prof, recurso_sin_vincular, curso):
        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/vincular/", {
            "curso": str(curso.id),
            "modulo": "",
            "leccion": "",
            "evaluacion_curso": "",
            "ejercicio": "",
            "orden": "7",
            "destacado": "on",
        })
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.orden == 7
        assert recurso_sin_vincular.destacado is True

    def test_vincular_sin_autenticar(self, cliente_anon, recurso, curso):
        r = cliente_anon.post(f"/recursos/{recurso.slug}/vincular/", {
            "curso": str(curso.id),
        })
        assert r.status_code in (301, 302, 403)


# ============================================================
# DESVINCULAR
# ============================================================
class TestDesvinculacionRecurso:
    def test_desvincular_curso(self, cliente_prof, recurso_vinculado):
        assert recurso_vinculado.curso_id is not None

        r = cliente_prof.post(f"/recursos/{recurso_vinculado.slug}/desvincular/curso/")
        assert r.status_code == 302

        recurso_vinculado.refresh_from_db()
        assert recurso_vinculado.curso_id is None

    def test_desvincular_modulo(self, cliente_prof, db, recurso_sin_vincular, modulo):
        recurso_sin_vincular.modulo = modulo
        recurso_sin_vincular.save()

        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/desvincular/modulo/")
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.modulo_id is None

    def test_desvincular_leccion(self, cliente_prof, db, recurso_sin_vincular, leccion):
        recurso_sin_vincular.leccion = leccion
        recurso_sin_vincular.save()

        r = cliente_prof.post(f"/recursos/{recurso_sin_vincular.slug}/desvincular/leccion/")
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        assert recurso_sin_vincular.leccion_id is None

    def test_tipo_invalido(self, cliente_prof, recurso_vinculado):
        r = cliente_prof.post(f"/recursos/{recurso_vinculado.slug}/desvincular/inventado/")
        assert r.status_code == 404


# ============================================================
# PARA OBJETO (listar vinculados + disponibles)
# ============================================================
class TestRecursosParaObjeto:
    def test_para_curso(self, cliente_prof, curso, recurso_vinculado):
        r = cliente_prof.get(f"/recursos/objeto/curso/{curso.id}/")
        assert r.status_code == 200
        assert b"Vinculados" in r.content

    def test_para_modulo(self, cliente_prof, db, modulo, recurso_sin_vincular):
        recurso_sin_vincular.modulo = modulo
        recurso_sin_vincular.save()

        r = cliente_prof.get(f"/recursos/objeto/modulo/{modulo.id}/")
        assert r.status_code == 200

    def test_para_leccion(self, cliente_prof, leccion):
        r = cliente_prof.get(f"/recursos/objeto/leccion/{leccion.id}/")
        assert r.status_code == 200

    def test_para_evaluacion(self, cliente_prof, evaluacion):
        r = cliente_prof.get(f"/recursos/objeto/evaluacion/{evaluacion.id}/")
        assert r.status_code == 200

    def test_tipo_invalido(self, cliente_prof, curso):
        r = cliente_prof.get(f"/recursos/objeto/inventado/{curso.id}/")
        assert r.status_code == 404

    def test_objeto_inexistente(self, cliente_prof):
        r = cliente_prof.get("/recursos/objeto/curso/999999/")
        assert r.status_code == 404

    def test_sin_autenticar(self, cliente_anon, curso):
        r = cliente_anon.get(f"/recursos/objeto/curso/{curso.id}/")
        assert r.status_code in (301, 302, 403)


# ============================================================
# ASIGNAR (bulk)
# ============================================================
class TestAsignarRecursos:
    def test_asignar_dos_recursos(self, cliente_prof, curso, recurso_sin_vincular, db, prof_user):
        from core.models import Recurso
        r2 = Recurso.objects.create(
            nombre="Recurso 2",
            slug="recurso-2",
            archivo="test/r2.html",
            categoria="Cuaderno",
            extension="html",
            tamaño_bytes=100,
        )

        r = cliente_prof.post(f"/recursos/objeto/curso/{curso.id}/asignar/", {
            "recurso_ids": [str(recurso_sin_vincular.id), str(r2.id)],
        })
        assert r.status_code == 302

        recurso_sin_vincular.refresh_from_db()
        r2.refresh_from_db()
        assert recurso_sin_vincular.curso_id == curso.id
        assert r2.curso_id == curso.id

    def test_asignar_sin_ids(self, cliente_prof, curso):
        r = cliente_prof.post(f"/recursos/objeto/curso/{curso.id}/asignar/", {})
        assert r.status_code == 302

    def test_asignar_tipo_invalido(self, cliente_prof, curso):
        r = cliente_prof.post(f"/recursos/objeto/inventado/{curso.id}/asignar/", {
            "recurso_ids": [],
        })
        assert r.status_code == 404


# ============================================================
# QUITAR
# ============================================================
class TestQuitarRecurso:
    def test_quitar_de_curso(self, cliente_prof, curso, recurso_vinculado):
        assert recurso_vinculado.curso_id == curso.id

        r = cliente_prof.post(
            f"/recursos/objeto/curso/{curso.id}/quitar/{recurso_vinculado.id}/"
        )
        assert r.status_code == 302

        recurso_vinculado.refresh_from_db()
        assert recurso_vinculado.curso_id is None

    def test_quitar_tipo_invalido(self, cliente_prof, curso, recurso_vinculado):
        r = cliente_prof.post(
            f"/recursos/objeto/inventado/{curso.id}/quitar/{recurso_vinculado.id}/"
        )
        assert r.status_code == 404

    def test_quitar_recurso_inexistente(self, cliente_prof, curso):
        r = cliente_prof.post(f"/recursos/objeto/curso/{curso.id}/quitar/999999/")
        assert r.status_code == 404
'''

(BASE / "core" / "tests" / "test_recursos.py").write_text(test_recursos, encoding="utf-8")
print("[OK] core/tests/test_recursos.py (22 tests)")

print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  E:\\PythonPortable_Django5\\python.exe manage.py check")
print("  E:\\PythonPortable_Django5\\python.exe -m pytest core\\tests\\test_recursos.py -v --tb=short")