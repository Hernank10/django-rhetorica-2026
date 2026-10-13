"""Tests de core/views_biblioteca.py."""
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
