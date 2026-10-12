"""
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
