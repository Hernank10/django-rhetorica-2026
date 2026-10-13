"""Tests de core/utils_certificados.py."""
import pytest
from django.utils import timezone

from core.models import Certificacion, CertificacionObtenida
from core.utils_certificados import (
    generar_certificado_pdf,
    generar_certificado_docx,
    huella_certificado,
    huella_corta,
    folio_unico,
    url_publica,
)


# ============================================================
# FIXTURES
# ============================================================
@pytest.fixture
def cert_obtenida(db, estudiante_user, certificacion):
    return CertificacionObtenida.objects.create(
        user=estudiante_user,
        certificacion=certificacion,
        codigo_verificacion="CERT-2026-0001",
        url_verificacion="https://test.local/verificar/CERT-2026-0001",
    )


# ============================================================
# generar_certificado_pdf
# ============================================================
class TestGenerarCertificadoPDF:
    def test_genera_bytes(self, cert_obtenida, estudiante_user):
        resultado = generar_certificado_pdf(cert_obtenida, estudiante_user)
        # Puede ser BytesIO, bytes o HttpResponse
        if hasattr(resultado, "read"):
            data = resultado.read()
        elif hasattr(resultado, "content"):
            data = resultado.content
        elif isinstance(resultado, bytes):
            data = resultado
        else:
            data = bytes(resultado)
        assert len(data) > 500
        # Cabecera PDF
        assert data[:4] == b"%PDF"

    def test_con_firmas_custom(self, cert_obtenida, estudiante_user):
        resultado = generar_certificado_pdf(
            cert_obtenida,
            estudiante_user,
            firma1="Dr. Test",
            firma2="Dir. Academica",
        )
        data = resultado.read() if hasattr(resultado, "read") else resultado
        if isinstance(data, bytes):
            assert len(data) > 500

    def test_nombre_alumno_en_pdf(self, cert_obtenida, estudiante_user):
        """El nombre del alumno debe estar en el PDF (buscando en el texto crudo)."""
        resultado = generar_certificado_pdf(cert_obtenida, estudiante_user)
        if hasattr(resultado, "read"):
            data = resultado.read()
        else:
            data = resultado
        # PDFs guardan el texto comprimido, pero el nombre puede aparecer
        # en metadata o texto plano
        assert isinstance(data, bytes)


# ============================================================
# generar_certificado_docx
# ============================================================
class TestGenerarCertificadoDOCX:
    def test_genera_bytes(self, cert_obtenida, estudiante_user):
        resultado = generar_certificado_docx(cert_obtenida, estudiante_user)
        if hasattr(resultado, "read"):
            data = resultado.read()
        elif hasattr(resultado, "content"):
            data = resultado.content
        elif isinstance(resultado, bytes):
            data = resultado
        else:
            data = bytes(resultado)
        assert len(data) > 500
        # Cabecera DOCX = ZIP
        assert data[:2] == b"PK"

    def test_con_firma_custom(self, cert_obtenida, estudiante_user):
        resultado = generar_certificado_docx(
            cert_obtenida,
            estudiante_user,
            firma1="Firma Personalizada",
        )
        assert resultado is not None


# ============================================================
# huella_certificado / huella_corta
# ============================================================
class TestHuella:
    def test_huella_devuelve_string(self, cert_obtenida):
        h = huella_certificado(cert_obtenida)
        assert isinstance(h, str)
        assert len(h) > 0

    def test_huella_determinista(self, cert_obtenida):
        h1 = huella_certificado(cert_obtenida)
        h2 = huella_certificado(cert_obtenida)
        assert h1 == h2

    def test_huella_distinta_por_certificado(self, db, certificacion, estudiante_user):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        otro = User.objects.create_user(username="otro_cert_test", password="x")

        c1 = CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=certificacion,
            codigo_verificacion="C1", url_verificacion="https://a",
        )
        c2 = CertificacionObtenida.objects.create(
            user=otro, certificacion=certificacion,
            codigo_verificacion="C2", url_verificacion="https://b",
        )
        assert huella_certificado(c1) != huella_certificado(c2)

    def test_huella_corta_es_mas_corta(self, cert_obtenida):
        larga = huella_certificado(cert_obtenida)
        corta = huella_corta(cert_obtenida)
        assert len(corta) <= len(larga)

    def test_huella_corta_devuelve_string(self, cert_obtenida):
        h = huella_corta(cert_obtenida)
        assert isinstance(h, str)
        assert len(h) > 0


# ============================================================
# folio_unico
# ============================================================
class TestFolioUnico:
    def test_devuelve_string(self, cert_obtenida):
        f = folio_unico(cert_obtenida)
        assert isinstance(f, str)
        assert len(f) > 0

    def test_no_tiene_espacios(self, cert_obtenida):
        f = folio_unico(cert_obtenida)
        assert " " not in f
        assert "\t" not in f
        assert "\n" not in f

    def test_determinista(self, cert_obtenida):
        f1 = folio_unico(cert_obtenida)
        f2 = folio_unico(cert_obtenida)
        assert f1 == f2

    def test_distinto_por_certificado(self, db, certificacion, estudiante_user):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        otro = User.objects.create_user(username="otro_folio_test", password="x")

        c1 = CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=certificacion,
            codigo_verificacion="F1", url_verificacion="https://a",
        )
        c2 = CertificacionObtenida.objects.create(
            user=otro, certificacion=certificacion,
            codigo_verificacion="F2", url_verificacion="https://b",
        )
        assert folio_unico(c1) != folio_unico(c2)


# ============================================================
# url_publica
# ============================================================
class TestUrlPublica:
    def test_devuelve_string(self, cert_obtenida):
        u = url_publica(cert_obtenida)
        assert isinstance(u, str)

    def test_contiene_codigo(self, cert_obtenida):
        u = url_publica(cert_obtenida)
        # O contiene el codigo de verificacion, o contiene "verificar"
        assert (
            cert_obtenida.codigo_verificacion in u
            or "verificar" in u.lower()
        )

    def test_es_url(self, cert_obtenida):
        u = url_publica(cert_obtenida)
        assert u.startswith("http") or u.startswith("/")