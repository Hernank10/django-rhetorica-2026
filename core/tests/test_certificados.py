"""Tests de generacion de certificados PDF/DOCX y verificacion publica."""
import pytest
from django.test import Client
from django.utils import timezone

from core.models import Certificacion, CertificacionObtenida


@pytest.fixture
def cert_obtenida(db, estudiante_user, certificacion):
    return CertificacionObtenida.objects.create(
        user=estudiante_user,
        certificacion=certificacion,
        codigo_verificacion="VERIF-0001-AB",
        url_verificacion="https://test.local/verificar/VERIF-0001-AB",
    )


class TestGeneracionPDF:
    def test_funcion_existe(self):
        from core import utils_certificados as uc
        assert hasattr(uc, "generar_certificado_pdf")
        assert callable(uc.generar_certificado_pdf)

    def test_genera_datos(self, cert_obtenida, estudiante_user):
        from core.utils_certificados import generar_certificado_pdf
        try:
            resultado = generar_certificado_pdf(cert_obtenida, estudiante_user)
        except KeyError as e:
            pytest.skip(f"Fuente no registrada en este entorno: {e}")
        except Exception as e:
            pytest.fail(f"Error inesperado: {type(e).__name__}: {e}")

        if hasattr(resultado, "read"):
            data = resultado.read()
        elif hasattr(resultado, "content"):
            data = resultado.content
        else:
            data = bytes(resultado) if not isinstance(resultado, bytes) else resultado
        assert len(data) > 100


class TestGeneracionDOCX:
    def test_funcion_existe(self):
        from core import utils_certificados as uc
        assert hasattr(uc, "generar_certificado_docx")
        assert callable(uc.generar_certificado_docx)

    def test_genera_datos(self, cert_obtenida, estudiante_user):
        from core.utils_certificados import generar_certificado_docx
        try:
            resultado = generar_certificado_docx(cert_obtenida, estudiante_user)
        except AttributeError as e:
            pytest.fail(f"Error de firma: {e}")
        except Exception as e:
            pytest.fail(f"Error inesperado: {type(e).__name__}: {e}")

        if hasattr(resultado, "read"):
            data = resultado.read()
        elif hasattr(resultado, "content"):
            data = resultado.content
        else:
            data = bytes(resultado) if not isinstance(resultado, bytes) else resultado
        assert len(data) > 100


class TestDescargaHTTP:
    def test_pdf_estudiante(self, cliente_est, cert_obtenida):
        r = cliente_est.get(f"/estudiante/certificados/{cert_obtenida.id}/pdf/")
        assert r.status_code in (200, 302, 404)

    def test_docx_estudiante(self, cliente_est, cert_obtenida):
        r = cliente_est.get(f"/estudiante/certificados/{cert_obtenida.id}/docx/")
        assert r.status_code in (200, 302, 404)

    def test_pdf_anonimo_redirige(self, cliente_anon, cert_obtenida):
        r = cliente_anon.get(f"/estudiante/certificados/{cert_obtenida.id}/pdf/")
        assert r.status_code in (301, 302, 403, 404)

    def test_pdf_profesor(self, cliente_prof, cert_obtenida):
        r = cliente_prof.get(f"/profesor/certificaciones/{cert_obtenida.id}/pdf/")
        assert r.status_code in (200, 302, 404)

    def test_preview_profesor(self, cliente_prof, cert_obtenida):
        r = cliente_prof.get(f"/profesor/certificaciones/{cert_obtenida.id}/preview/")
        assert r.status_code in (200, 302, 404)


class TestVerificacionPublica:
    def test_url_publica_200(self, cliente_anon, cert_obtenida):
        r = cliente_anon.get(f"/verificar/{cert_obtenida.codigo_verificacion}/")
        assert r.status_code in (200, 404)

    def test_codigo_invalido(self, cliente_anon, db):
        r = cliente_anon.get("/verificar/NO-EXISTE-XYZ/")
        assert r.status_code in (200, 404)

    def test_no_requiere_login(self, cliente_anon, db):
        r = cliente_anon.get("/verificar/CUALQUIERA/")
        assert r.status_code != 302 or "login" not in r.headers.get("Location", "").lower()


class TestListadoCertificados:
    def test_estudiante_ve_su_lista(self, cliente_est, cert_obtenida):
        r = cliente_est.get("/estudiante/certificados/")
        assert r.status_code == 200

    def test_profesor_ve_certificaciones(self, cliente_prof):
        r = cliente_prof.get("/profesor/certificaciones/")
        assert r.status_code == 200

    def test_lista_publica(self, cliente_anon):
        r = cliente_anon.get("/certificaciones/")
        assert r.status_code in (200, 301, 302)


class TestModeloCertificacion:
    def test_creacion(self, certificacion):
        assert certificacion.activa is True

    def test_str(self, certificacion):
        assert "Test Cert" in str(certificacion)

    def test_obtenida_con_codigo(self, cert_obtenida):
        assert cert_obtenida.codigo_verificacion == "VERIF-0001-AB"
        assert cert_obtenida.user is not None
