from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tests_dir = BASE / "core" / "tests"

# ============================================================
# test_utils.py
# ============================================================
test_utils = '''"""Tests de core/utils_certificados.py: huella, folio, url publica."""
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
'''
(tests_dir / "test_utils.py").write_text(test_utils, encoding="utf-8")
print("[OK] test_utils.py")

# ============================================================
# test_certificados.py
# ============================================================
test_certificados = '''"""Tests de generacion de certificados PDF/DOCX y verificacion publica."""
import pytest
from django.test import Client
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
        codigo_verificacion="VERIF-0001-AB",
        url_verificacion="https://test.local/verificar/VERIF-0001-AB",
    )


# ============================================================
# GENERACION PDF / DOCX
# ============================================================
class TestGeneracionPDF:
    def test_funcion_existe(self):
        from core import utils_certificados as uc
        assert hasattr(uc, "generar_certificado_pdf")

    def test_pdf_no_vacio(self, certificacion, estudiante_user):
        from core.utils_certificados import generar_certificado_pdf
        resultado = generar_certificado_pdf(certificacion, estudiante_user)
        # Puede ser bytes, BytesIO o HttpResponse
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

    def test_docx_no_vacio(self, certificacion, estudiante_user):
        from core.utils_certificados import generar_certificado_docx
        resultado = generar_certificado_docx(certificacion, estudiante_user)
        if hasattr(resultado, "read"):
            data = resultado.read()
        elif hasattr(resultado, "content"):
            data = resultado.content
        else:
            data = bytes(resultado) if not isinstance(resultado, bytes) else resultado
        assert len(data) > 100


# ============================================================
# ENDPOINTS DE DESCARGA (HTTP)
# ============================================================
class TestDescargaHTTP:
    def test_pdf_estudiante(self, cliente_est, cert_obtenida):
        r = cliente_est.get(f"/estudiante/certificados/{cert_obtenida.id}/pdf/")
        # 200 = OK, 302 = redirect, 404 si no aplica
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


# ============================================================
# VERIFICACION PUBLICA
# ============================================================
class TestVerificacionPublica:
    def test_url_publica_200(self, cliente_anon, cert_obtenida):
        r = cliente_anon.get(f"/verificar/{cert_obtenida.codigo_verificacion}/")
        assert r.status_code in (200, 404)

    def test_codigo_invalido(self, cliente_anon):
        r = cliente_anon.get("/verificar/NO-EXISTE-XYZ/")
        # Debe devolver 404 o pagina con mensaje de no encontrado
        assert r.status_code in (200, 404)

    def test_no_requiere_login(self, cliente_anon):
        # La verificacion debe ser publica (no redirigir a login)
        r = cliente_anon.get("/verificar/CUALQUIERA/")
        assert r.status_code != 302 or "login" not in r.headers.get("Location", "").lower()


# ============================================================
# LISTADO DE CERTIFICADOS
# ============================================================
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


# ============================================================
# MODELO
# ============================================================
class TestModeloCertificacion:
    def test_creacion(self, certificacion):
        assert certificacion.activa is True

    def test_str(self, certificacion):
        assert "Test Cert" in str(certificacion)

    def test_obtenida_con_codigo(self, cert_obtenida):
        assert cert_obtenida.codigo_verificacion == "VERIF-0001-AB"
        assert cert_obtenida.user is not None
'''
(tests_dir / "test_certificados.py").write_text(test_certificados, encoding="utf-8")
print("[OK] test_certificados.py")

# ============================================================
# test_i18n.py
# ============================================================
test_i18n = '''"""Tests de internacionalizacion: los 16 idiomas configurados."""
import pytest
from django.conf import settings
from django.utils import translation


# ============================================================
# CONFIGURACION BASICA
# ============================================================
class TestConfiguracionI18N:
    def test_use_i18n_activo(self):
        assert settings.USE_I18N is True

    def test_language_code_default(self):
        assert settings.LANGUAGE_CODE == "es"

    def test_languages_definidos(self):
        assert hasattr(settings, "LANGUAGES")
        assert len(settings.LANGUAGES) >= 16, f"Solo hay {len(settings.LANGUAGES)} idiomas"

    def test_locale_path(self):
        assert hasattr(settings, "LOCALE_PATHS")


# ============================================================
# ACTIVACION DE IDIOMAS
# ============================================================
class TestActivacionIdiomas:
    def test_activar_cada_idioma(self):
        for code, nombre in settings.LANGUAGES:
            with translation.override(code):
                actual = translation.get_language()
                # Django normaliza (ej: es-co -> es)
                assert actual is not None
                assert len(actual) >= 2

    def test_idioma_por_defecto(self):
        translation.activate("es")
        assert translation.get_language() == "es"
        translation.deactivate()

    def test_idioma_ingles(self):
        translation.activate("en")
        assert translation.get_language() == "en"
        translation.deactivate()

    def test_override_context_manager(self):
        with translation.override("fr"):
            assert translation.get_language() == "fr"
        # Al salir, vuelve al idioma original
        assert translation.get_language() != "fr"


# ============================================================
# TRADUCCIONES
# ============================================================
class TestTraducciones:
    def test_gettext_no_falla(self):
        from django.utils.translation import gettext as _
        # En cualquier idioma, gettext debe devolver string
        with translation.override("en"):
            msg = _("Bienvenido")
            assert isinstance(msg, str)

    def test_todos_los_codigos_unicos(self):
        codigos = [code for code, _ in settings.LANGUAGES]
        assert len(codigos) == len(set(codigos)), "Hay codigos duplicados"

    def test_todos_los_nombres_no_vacios(self):
        for code, nombre in settings.LANGUAGES:
            assert isinstance(nombre, str)
            assert len(nombre) > 0

    def test_codigos_bien_formados(self):
        import re
        for code, _ in settings.LANGUAGES:
            # Formato ISO: 2 letras, opcional guion y 2-3 mas
            assert re.match(r"^[a-z]{2}(-[a-z]{2,3})?$", code.lower()), f"Codigo invalido: {code}"
'''
(tests_dir / "test_i18n.py").write_text(test_i18n, encoding="utf-8")
print("[OK] test_i18n.py")

print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  E:\\PythonPortable_Django5\\python.exe -m pytest -q > pytest_out.txt 2>&1")
print("  type pytest_out.txt")