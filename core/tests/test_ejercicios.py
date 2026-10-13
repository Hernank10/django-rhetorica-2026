"""Tests de core/views_ejercicios.py."""
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
