"""Tests de cobertura — índices A1/B1, técnica 404, evaluar, progreso."""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from core.models_gramatica import TecnicaGramatical

pytestmark = pytest.mark.django_db


MODULOS = {
    "a1": (201, 210),
    "a2": (501, 510),
    "b1": (301, 310),
    "b2": (601, 610),
    "c1": (701, 710),
    "c2": (801, 810),
}


@pytest.fixture
def seed_modulos():
    """Seed 10 técnicas por módulo (bloque A) para render del índice."""
    for modulo, (start, end) in MODULOS.items():
        for n in range(start, end + 1):
            TecnicaGramatical.objects.update_or_create(
                numero=n,
                defaults={
                    "bloque": "A", "nivel": "avanzado", "modulo": modulo,
                    "titulo": f"Tecnica {n}", "teoria": "T",
                    "explicacion": "E", "regla": "R",
                    "ejemplo_correcto": "C", "ejemplo_incorrecto": "I",
                },
            )
    yield
    for modulo in MODULOS:
        TecnicaGramatical.objects.filter(modulo=modulo).delete()


@pytest.fixture
def user():
    U = get_user_model()
    u, _ = U.objects.get_or_create(username="cov_user")
    return u


# ─── Índices por módulo (cubre indice_a1, indice_b1, ...) ───

@pytest.mark.parametrize("modulo", ["a1", "a2", "b1", "b2", "c1", "c2"])
def test_indice_modulo_200(seed_modulos, user, modulo):
    c = Client(); c.force_login(user)
    r = c.get(f"/gramatica/{modulo}/")
    assert r.status_code == 200


def test_indice_sin_login_redirige(seed_modulos):
    c = Client()
    r = c.get("/gramatica/c2/")
    assert r.status_code in (302, 403)


# ─── Técnica: existente, 404, sin login ───

def test_tecnica_existente_200(seed_modulos, user):
    c = Client(); c.force_login(user)
    r = c.get("/gramatica/tecnica/801/")
    assert r.status_code == 200


def test_tecnica_inexistente_404(seed_modulos, user):
    c = Client(); c.force_login(user)
    r = c.get("/gramatica/tecnica/99999/")
    assert r.status_code == 404


def test_tecnica_sin_login_redirige(seed_modulos):
    c = Client()
    r = c.get("/gramatica/tecnica/801/")
    assert r.status_code in (302, 403)


# ─── Evaluar: POST sin login, POST con login ───

def test_evaluar_post_sin_login_redirige(seed_modulos):
    c = Client()
    r = c.post("/gramatica/evaluar/", data={})
    assert r.status_code in (302, 403)


def test_evaluar_post_con_login_no_rompe(seed_modulos, user):
    """POST con payload vacío — el endpoint no debe dar 500."""
    c = Client(); c.force_login(user)
    r = c.post("/gramatica/evaluar/", data={})
    assert r.status_code in (200, 400)


# ─── Progreso y engine ───

def test_progreso_gramatica_200(seed_modulos, user):
    c = Client(); c.force_login(user)
    r = c.get("/gramatica/progreso/?modulo=c2")
    assert r.status_code == 200


def test_resumen_progreso(seed_modulos, user):
    from core.services import gramatica as engine
    resumen = engine.resumen_progreso(user, modulo="c2")
    assert isinstance(resumen, dict)
