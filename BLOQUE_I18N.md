# Bloque i18n - 16 idiomas

**Proyecto:** django-rhetorica
**Django:** 5.2.11
**Fecha:** Octubre 2026

## Idiomas soportados

es, en, pt, fr, de, it, ca, gl, eu, zh-hans, ja, ko, ar, ru, hi, tr

## Cambios realizados

### settings.py
- from django.utils.translation import gettext_lazy as _
- django.middleware.locale.LocaleMiddleware (despues de SessionMiddleware)
- LANGUAGES = [16 idiomas]
- LOCALE_PATHS = [BASE_DIR / 'locale']
### urls.py
- path('i18n/', include('django.conf.urls.i18n'))
- urlpatterns += i18n_patterns(..., prefix_default_language=False)
- Admin fuera de i18n_patterns

### base.html
- load i18n
- Selector set_language en navbar

### locale/
- 16 django.po (sin traducir)
- 16 django.mo (compilados, en .gitignore)

## Comandos

python manage.py makemessages -l es -l en -l pt -l fr -l de -l it -l ca -l gl -l eu -l zh_Hans -l ja -l ko -l ar -l ru -l hi -l tr
python manage.py compilemessages

## URLs
- / -> espanol (default)
- /en/ -> ingles
- /zh-hans/ -> chino simplificado
- /ar/ -> arabe (pendiente RTL)

## Pendiente
- Traducir contenido de los 16 .po
- RTL para arabe
- django-rosetta (opcional)
