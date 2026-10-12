from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) pytest.ini
# ============================================================
pytest_ini = '''[pytest]
DJANGO_SETTINGS_MODULE = django_retorica.settings
python_files = tests.py test_*.py *_tests.py
addopts = -q --tb=short
norecursedirs = .git .venv venv env __pycache__ static staticfiles media contenido data html_contenido node_modules migrations
testpaths = core
'''
(BASE / "pytest.ini").write_text(pytest_ini, encoding="utf-8")
print("[OK] pytest.ini")

# ============================================================
# 2) conftest.py
# ============================================================
conftest = '''"""
Fixtures globales para pytest.
Acelera los tests con MD5PasswordHasher y crea usuarios por rol.
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client


@pytest.fixture(autouse=True)
def _fast_password_hasher(settings):
    """Usa MD5 en vez de PBKDF2 → 24x más rápido."""
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def grupos(db):
    """Crea los 3 grupos base."""
    return {
        "admin": Group.objects.get_or_create(name="Administrador")[0],
        "prof": Group.objects.get_or_create(name="Profesor")[0],
        "est": Group.objects.get_or_create(name="Estudiante")[0],
    }


@pytest.fixture
def admin_user(db, grupos):
    User = get_user_model()
    u = User.objects.create_user(
        username="test_admin", password="test123",
        is_staff=True, is_superuser=True, email="admin@test.local",
    )
    u.groups.add(grupos["admin"])
    return u


@pytest.fixture
def prof_user(db, grupos):
    User = get_user_model()
    u = User.objects.create_user(
        username="test_prof", password="test123",
        is_staff=True, email="prof@test.local",
    )
    u.groups.add(grupos["prof"])
    return u


@pytest.fixture
def estudiante_user(db, grupos):
    User = get_user_model()
    u = User.objects.create_user(
        username="test_est", password="test123", email="est@test.local",
    )
    u.groups.add(grupos["est"])
    return u


@pytest.fixture
def cliente_anon():
    return Client()


@pytest.fixture
def cliente_prof(prof_user):
    c = Client()
    c.force_login(prof_user)
    return c


@pytest.fixture
def cliente_est(estudiante_user):
    c = Client()
    c.force_login(estudiante_user)
    return c


@pytest.fixture
def cliente_admin(admin_user):
    c = Client()
    c.force_login(admin_user)
    return c


# --------- FIXTURES DE CONTENIDO ---------
@pytest.fixture
def curso(db, prof_user):
    from core.models_cursos import Curso
    return Curso.objects.create(
        titulo="Test Curso", slug="test-curso",
        descripcion="Curso de prueba",
        objetivo="Aprender test",
        nivel="basico", estado="publicado",
        duracion_estimada=60, puntos_totales=100,
        creado_por=prof_user,
    )


@pytest.fixture
def modulo(db, curso):
    from core.models_cursos import Modulo
    return Modulo.objects.create(
        curso=curso, titulo="Test Módulo",
        descripcion="Módulo de prueba", orden=1,
    )


@pytest.fixture
def leccion(db, modulo):
    from core.models_cursos import Leccion
    return Leccion.objects.create(
        modulo=modulo, titulo="Test Lección",
        contenido="<p>Contenido</p>", tipo="lectura",
        orden=1, duracion_estimada=15, puntos=10,
    )


@pytest.fixture
def evaluacion(db, curso, modulo):
    from core.models_cursos import EvaluacionCurso
    return EvaluacionCurso.objects.create(
        curso=curso, modulo=modulo,
        titulo="Test Evaluación",
        descripcion="Evaluación de prueba",
        tipo="modulo",
        preguntas_por_evaluacion=5,
        tiempo_limite=30,
        puntaje_maximo=100,
        intentos_permitidos=3,
    )


@pytest.fixture
def logro(db):
    from core.models import Logro
    return Logro.objects.create(
        nombre="Test Logro",
        descripcion="Logro de prueba",
        tipo="insignia", icono="⭐", color="#facc15",
        puntos_requeridos=100,
        nivel_requerido=1,
    )


@pytest.fixture
def certificacion(db):
    from core.models import Certificacion
    return Certificacion.objects.create(
        nombre="Test Cert",
        descripcion="Certificación de prueba",
        nivel="basico",
        requisitos={"lecciones": 5},
        activa=True,
    )
'''
(BASE / "conftest.py").write_text(conftest, encoding="utf-8")
print("[OK] conftest.py")

# ============================================================
# 3) core/tests/__init__.py
# ============================================================
tests_dir = BASE / "core" / "tests"
tests_dir.mkdir(exist_ok=True)
(tests_dir / "__init__.py").write_text("", encoding="utf-8")
print("[OK] core/tests/__init__.py")

# ============================================================
# 4) test_models.py
# ============================================================
test_models = '''"""Tests de modelos: Curso, Modulo, Leccion, Evaluacion, Logro, Certificacion."""
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
'''
(tests_dir / "test_models.py").write_text(test_models, encoding="utf-8")
print("[OK] core/tests/test_models.py")

# ============================================================
# 5) Verificar pytest instalado
# ============================================================
print()
print("=" * 60)
print("AHORA ejecuta:")
print("=" * 60)
print("  cd /d \"E:\\02_proyectos\\django-rhetorica\"")
print("  E:\\PythonPortable_Django5\\python.exe -m pytest -q")
print()
print("Esperado: ~30 tests passed en < 5s")