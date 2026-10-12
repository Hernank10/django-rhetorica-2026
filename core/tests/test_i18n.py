"""Tests de internacionalizacion: los 16 idiomas configurados."""
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
