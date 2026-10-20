"""E2E: demo activa<->pasiva con debounce + AJAX."""
import pytest

pytestmark = pytest.mark.e2e


def test_demo_carga(page, live_server):
    page.goto(live_server.url + "/sintaxis/parafrasis/")
    page.wait_for_selector("#texto_original")
    assert page.locator("#form-parafrasis").is_visible()
    assert page.locator("#resultado").count() == 1


def test_debounce_dispara_ajax(page, live_server):
    page.goto(live_server.url + "/sintaxis/parafrasis/")
    # expect_response: espera el fetch AJAX (default 30s, cubre carga de spaCy)
    with page.expect_response("**/sintaxis/parafrasis/ajax/**", timeout=20000) as resp_info:
        page.fill("#texto_original", "Juan lee el libro")
        page.fill("#texto_parafraseado", "El libro es leido por Juan")
    response = resp_info.value
    assert response.status == 200
    # Render del resultado
    page.wait_for_function(
        "document.getElementById('resultado').textContent.length > 10",
        timeout=5000,
    )
    texto = page.locator("#resultado").text_content()
    assert "aprobado" in texto.lower() or "correcto" in texto.lower()


def test_csrf_token_presente(page, live_server):
    page.goto(live_server.url + "/sintaxis/parafrasis/")
    csrf = page.locator("[name=csrfmiddlewaretoken]").input_value()
    assert csrf is not None and len(csrf) > 10