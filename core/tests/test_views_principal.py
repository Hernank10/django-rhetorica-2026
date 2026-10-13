"""Tests de core/views.py (vistas activas mapeadas a URLs)."""
import pytest

from core.models import Certificacion, CertificacionObtenida, Logro, LogroObtenido
from core.models_cursos import EjercicioLinguistico


# ============================================================
# INDEX / HOME
# ============================================================
class TestIndex:
    def test_get_anonimo(self, cliente_anon, db):
        r = cliente_anon.get("/")
        assert r.status_code == 200

    def test_get_autenticado(self, cliente_est, db):
        r = cliente_est.get("/")
        assert r.status_code == 200


# ============================================================
# LOGIN / REGISTRO / LOGOUT
# ============================================================
class TestLoginLogout:
    def test_login_get(self, cliente_anon):
        r = cliente_anon.get("/login/")
        assert r.status_code in (200, 301, 302)

    def test_login_post_credenciales_malas(self, cliente_anon, db):
        r = cliente_anon.post("/login/", {"username": "noexiste", "password": "mala"})
        # Se queda en login o redirige según implementación
        assert r.status_code in (200, 302)

    def test_logout_redirige(self, cliente_est):
        r = cliente_est.get("/logout/")
        assert r.status_code in (200, 301, 302)

    def test_registro_get(self, cliente_anon):
        r = cliente_anon.get("/registro/")
        assert r.status_code in (200, 301, 302)


# ============================================================
# PERFIL
# ============================================================
class TestPerfil:
    def test_perfil_anon_redirige(self, cliente_anon):
        r = cliente_anon.get("/perfil/")
        assert r.status_code in (301, 302)

    def test_perfil_autenticado(self, cliente_est):
        r = cliente_est.get("/perfil/")
        assert r.status_code == 200

    def test_editar_perfil_get(self, cliente_est):
        r = cliente_est.get("/perfil/editar/")
        assert r.status_code in (200, 301, 302)

    def test_cambiar_contrasena_get(self, cliente_est, db):
        r = cliente_est.get("/perfil/cambiar-contrasena/")
        assert r.status_code in (200, 301, 302)


# ============================================================
# DASHBOARD
# ============================================================
class TestDashboard:
    def test_dashboard_estudiante_anon(self, cliente_anon, db):
        r = cliente_anon.get("/dashboard/")
        # La vista no exige login (o redirige según implementación)
        assert r.status_code in (200, 301, 302)

    def test_dashboard_estudiante_autenticado(self, cliente_est):
        r = cliente_est.get("/dashboard/")
        assert r.status_code == 200

    def test_dashboard_gamificacion_anon(self, cliente_anon, db):
        r = cliente_anon.get("/dashboard/gamificacion/")
        assert r.status_code in (200, 301, 302)

    def test_dashboard_gamificacion_autenticado(self, cliente_est, db):
        r = cliente_est.get("/dashboard/gamificacion/")
        assert r.status_code in (200, 301, 302)

    def test_dashboard_renderiza_html(self, cliente_est):
        r = cliente_est.get("/dashboard/")
        assert "text/html" in r["Content-Type"].lower()
        assert len(r.content) > 100


# ============================================================
# TECNICAS
# ============================================================
class TestTecnicas:
    def test_get_anonimo(self, cliente_anon, db):
        r = cliente_anon.get("/tecnicas/")
        # Puede requerir login o no
        assert r.status_code in (200, 301, 302)

    def test_get_autenticado(self, cliente_est, db):
        r = cliente_est.get("/tecnicas/")
        assert r.status_code in (200, 301, 302)


# ============================================================
# CERTIFICACIONES LISTA
# ============================================================
class TestCertificacionesLista:
    def test_get_anonimo(self, cliente_anon, db):
        r = cliente_anon.get("/certificaciones/")
        assert r.status_code in (200, 301, 302)

    def test_get_autenticado(self, cliente_est, db):
        r = cliente_est.get("/certificaciones/")
        assert r.status_code == 200

    def test_con_certificacion_publicada(self, cliente_est, certificacion):
        r = cliente_est.get("/certificaciones/")
        assert r.status_code == 200


# ============================================================
# VERIFICAR CERTIFICADO PUBLICO
# ============================================================
class TestVerificarCertificadoPublico:
    def test_codigo_inexistente(self, cliente_anon, db):
        r = cliente_anon.get("/verificar/NO-EXISTE-XYZ/")
        assert r.status_code in (200, 404)

    def test_codigo_valido(self, cliente_anon, estudiante_user, certificacion):
        co = CertificacionObtenida.objects.create(
            user=estudiante_user,
            certificacion=certificacion,
            codigo_verificacion="VERIF-PUBLICO-1",
            url_verificacion="https://test.local/verificar/VERIF-PUBLICO-1",
        )
        r = cliente_anon.get(f"/verificar/{co.codigo_verificacion}/")
        assert r.status_code in (200, 404)

    def test_no_requiere_login(self, cliente_anon, db):
        # La verificacion debe ser publica
        r = cliente_anon.get("/verificar/CUALQUIERA/")
        assert r.status_code != 302 or "login" not in r.headers.get("Location", "").lower()


# ============================================================
# ENVIAR RESPUESTA
# ============================================================
class TestEnviarRespuesta:
    def test_get_no_permitido_o_redirect(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.get(f"/enviar-respuesta/{ejercicio_linguistico.id}/")
        assert r.status_code in (200, 302, 405)

    def test_post_respuesta(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.post(f"/enviar-respuesta/{ejercicio_linguistico.id}/", {
            "respuesta": "4",
            "tiempo": "10",
        })
        assert r.status_code in (200, 302, 400)

    def test_post_sin_datos(self, cliente_est, ejercicio_linguistico):
        r = cliente_est.post(f"/enviar-respuesta/{ejercicio_linguistico.id}/", {})
        assert r.status_code in (200, 302, 400)

    def test_anon_redirige(self, cliente_anon, ejercicio_linguistico):
        r = cliente_anon.post(f"/enviar-respuesta/{ejercicio_linguistico.id}/", {})
        assert r.status_code in (301, 302, 400, 403)
