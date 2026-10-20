"""E2E: pagina de registro formal<->coloquial."""
import pytest

pytestmark = pytest.mark.e2e


def test_link_registro_desde_demo(page, live_server):
    page.goto(live_server.url + "/sintaxis/parafrasis/")
    page.click("a[href*='/registro/']")
    page.wait_for_selector("#form-registro")
    assert page.url.endswith("/registro/")
    assert page.locator("#tipo").count() == 1


def test_registro_transformar_formal_a_coloquial(page, live_server):
    page.goto(live_server.url + "/sintaxis/parafrasis/registro/")
    page.fill("#texto_original", "Usted tiene dinero")
    page.select_option("#tipo", "formal_a_coloquial")
    page.click("#btn-registro")
    page.wait_for_function(
        "document.getElementById('resultado').textContent.includes('Vos')",
        timeout=8000,
    )
    texto = page.locator("#resultado").text_content()
    assert "Vos" in texto or "plata" in texto