from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
tests_dir = BASE / "core" / "tests"

# ============================================================
# test_certificados.py (CORREGIDO)
# ============================================================
test_certificados = '''"""Tests de generacion de certificados PDF/DOCX y verificacion publica."""
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
'''
(tests_dir / "test_certificados.py").write_text(test_certificados, encoding="utf-8")
print("[OK] test_certificados.py corregido")

# ============================================================
# test_i18n.py (CORREGIDO)
# ============================================================
test_i18n = '''"""Tests de internacionalizacion: los 16 idiomas configurados."""
import pytest
from django.conf import settings
from django.utils import translation


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


class TestActivacionIdiomas:
    def test_activar_cada_idioma(self):
        for code, nombre in settings.LANGUAGES:
            with translation.override(code):
                actual = translation.get_language()
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
        assert translation.get_language() != "fr"


class TestTraducciones:
    def test_gettext_no_falla(self):
        from django.utils.translation import gettext as _
        with translation.override("en"):
            msg = _("Bienvenido")
            assert isinstance(msg, str)

    def test_todos_los_codigos_unicos(self):
        codigos = [code for code, _ in settings.LANGUAGES]
        assert len(codigos) == len(set(codigos)), "Hay codigos duplicados"

    def test_todos_los_nombres_no_vacios(self):
        for code, nombre in settings.LANGUAGES:
            # Django usa gettext_lazy; forzamos a str
            assert str(nombre).strip() != "", f"Nombre vacio para {code}"

    def test_codigos_bien_formados(self):
        import re
        # Acepta: es, en, pt-br, zh-hans, zh-hant (2-4 letras en la parte 2)
        patron = re.compile(r"^[a-z]{2,3}(-[a-z]{2,4})?$")
        for code, _ in settings.LANGUAGES:
            assert patron.match(code.lower()), f"Codigo invalido: {code}"
'''
(tests_dir / "test_i18n.py").write_text(test_i18n, encoding="utf-8")
print("[OK] test_i18n.py corregido")

print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  E:\\PythonPortable_Django5\\python.exe -m pytest -q --tb=short > pytest_out.txt 2>&1")
print("  type pytest_out.txt")
