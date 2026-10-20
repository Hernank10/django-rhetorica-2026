"""Fixtures E2E: Playwright + Django live_server.

DJANGO_ALLOW_ASYNC_UNSAFE: pytest-playwright envuelve tests sync en un
event loop async. live_server -> transactional_db -> connection.close()
esta marcado @async_unsafe en Django y explota. Este env var lo salta.
Solo aplica a tests e2e (este conftest).

preload_spacy: calienta _cargar() una vez por sesion. Sin esto, la primera
llamada a un endpoint con spaCy tarda 5-8s y rompe expect_response(timeout=5s).
"""
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import pytest


@pytest.fixture(scope="session", autouse=True)
def preload_spacy():
    """Calienta spaCy una vez para toda la sesion e2e."""
    from core.services.pos import _cargar, modelo_disponible
    if modelo_disponible():
        _cargar()
    return


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Chromium headless."""
    return {
        **browser_type_launch_args,
        "headless": True,
    }


@pytest.fixture
def page(page):
    """Page con timeout default."""
    page.set_default_timeout(5000)
    return page