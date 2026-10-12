"""Tests de core/utils_certificados.py: huella, folio, url publica."""
import pytest
from django.utils import timezone

from core.models import Certificacion, CertificacionObtenida


# ============================================================
# FIXTURE LOCAL
# ============================================================
@pytest.fixture
def cert_obtenida(db, estudiante_user, certificacion):
    return CertificacionObtenida.objects.create(
        user=estudiante_user,
        certificacion=certificacion,
        codigo_verificacion="TEST-0001-XX",
        url_verificacion="https://test.local/verificar/TEST-0001-XX",
    )


# ============================================================
# HUELLA
# ============================================================
class TestHuellaCertificado:
    def test_existe_funcion(self):
        from core import utils_certificados as uc
        assert hasattr(uc, "huella_certificado")
        assert callable(uc.huella_certificado)

    def test_devuelve_string(self, cert_obtenida):
        from core.utils_certificados import huella_certificado
        h = huella_certificado(cert_obtenida)
        assert isinstance(h, str)
        assert len(h) > 0

    def test_determinista(self, cert_obtenida):
        from core.utils_certificados import huella_certificado
        h1 = huella_certificado(cert_obtenida)
        h2 = huella_certificado(cert_obtenida)
        assert h1 == h2

    def test_distinta_para_otro_usuario(self, db, certificacion, estudiante_user):
        from django.contrib.auth import get_user_model
        from core.utils_certificados import huella_certificado
        User = get_user_model()
        otro = User.objects.create_user(username="otro_test", password="x")

        c1 = CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=certificacion,
            codigo_verificacion="A", url_verificacion="https://a",
        )
        c2 = CertificacionObtenida.objects.create(
            user=otro, certificacion=certificacion,
            codigo_verificacion="B", url_verificacion="https://b",
        )
        assert huella_certificado(c1) != huella_certificado(c2)


class TestHuellaCorta:
    def test_existe(self):
        from core import utils_certificados as uc
        assert hasattr(uc, "huella_corta")

    def test_devuelve_string(self, cert_obtenida):
        from core.utils_certificados import huella_corta
        h = huella_corta(cert_obtenida)
        assert isinstance(h, str)

    def test_mas_corta_que_huella(self, cert_obtenida):
        from core.utils_certificados import huella_certificado, huella_corta
        larga = huella_certificado(cert_obtenida)
        corta = huella_corta(cert_obtenida)
        assert len(corta) <= len(larga)


# ============================================================
# FOLIO
# ============================================================
class TestFolioUnico:
    def test_existe(self):
        from core import utils_certificados as uc
        assert hasattr(uc, "folio_unico")

    def test_devuelve_string(self, cert_obtenida):
        from core.utils_certificados import folio_unico
        f = folio_unico(cert_obtenida)
        assert isinstance(f, str)
        assert len(f) > 0

    def test_no_contiene_simbolos_raros(self, cert_obtenida):
        from core.utils_certificados import folio_unico
        f = folio_unico(cert_obtenida)
        # Solo letras, numeros, guiones
        import re
        assert re.match(r"^[A-Za-z0-9\-_/]+$", f) is not None


# ============================================================
# URL PUBLICA
# ============================================================
class TestUrlPublica:
    def test_existe(self):
        from core import utils_certificados as uc
        assert hasattr(uc, "url_publica")

    def test_contiene_codigo(self, cert_obtenida):
        from core.utils_certificados import url_publica
        u = url_publica(cert_obtenida)
        assert isinstance(u, str)
        assert "verificar" in u.lower() or cert_obtenida.codigo_verificacion in u
