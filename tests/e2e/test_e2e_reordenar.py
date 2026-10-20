"""E2E: boton reordenar en demo.html."""
import pytest

pytestmark = pytest.mark.e2e


def test_boton_reordenar_visible(page, live_server):
    page.goto(live_server.url + "/sintaxis/parafrasis/")
    assert page.locator("#btn-reordenar").is_visible()
    assert page.locator("#sugerencias").count() == 1


def test_boton_sin_texto_muestra_mensaje(page, live_server):
    page.goto(live_server.url + "/sintaxis/parafrasis/")
    page.click("#btn-reordenar")
    page.wait_for_function(
        "document.getElementById('sugerencias').textContent.length > 0",
        timeout=2000,
    )
    assert "Escribe" in page.locator("#sugerencias").text_content()


def test_boton_con_texto_muestra_sugerencias(page, live_server):
    page.goto(live_server.url + "/sintaxis/parafrasis/")
    page.fill("#texto_original", "Juan lee el libro en el parque")
    page.click("#btn-reordenar")
    page.wait_for_function(
        "document.getElementById('sugerencias').textContent.length > 10",
        timeout=3000,
    )
    texto = page.locator("#sugerencias").text_content()
    # Debe contener al menos un tipo de sugerencia (fronting o svo)
    assert "fronting" in texto.lower() or "svo" in texto.lower()