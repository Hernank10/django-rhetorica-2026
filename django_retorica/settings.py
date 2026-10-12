"""
Django settings for django_retorica project.
"""

DEBUG = True


import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xyz123abc456def789ghi012jkl345mno678pqr901stu234vwx567yza'

# SECURITY WARNING: don't run with debug turned on in production!

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_retorica.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_retorica.wsgi.application'

# Database
DATABASES = {    'default': {        'ENGINE': 'django.db.backends.sqlite3',        'NAME': BASE_DIR / 'db.sqlite3',    }}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# CONFIGURACIÓN PARA CODESPACES Y ENTORNOS REMOTOS
# ============================================================

# Permitir hosts para Codespaces
# CSRF Trusted Origins - Para que los POST funcionen en Codespaces
CSRF_TRUSTED_ORIGINS = [
    'https://*.githubpreview.dev',
    'https://*.app.github.dev',
    'http://*.githubpreview.dev',
    'http://*.app.github.dev',
    'https://*.codespaces.app',
    'http://*.codespaces.app',
    'https://localhost:8000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Configuración de seguridad para desarrollo
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# ============================================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
# ============================================================

# Directorio de archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# ============================================================
# CONFIGURACIÓN DE CSRF Y SEGURIDAD PARA DESARROLLO
# ============================================================

# Para desarrollo - permitir CSRF desde cualquier origen (solo en desarrollo)
# En producción, esto debe ser más restrictivo
CSRF_COOKIE_SECURE = False  # True en producción con HTTPS
SESSION_COOKIE_SECURE = False  # True en producción con HTTPS
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

# Para debugging

# Zona horaria
TIME_ZONE = 'America/Bogota'
USE_TZ = True

# -------------------------------------------------------------
# i18n - 16 idiomas
# -------------------------------------------------------------
LANGUAGES = [
    ('es',      _('Espanol')),
    ('en',      _('English')),
    ('pt',      _('Portugues')),
    ('fr',      _('Francais')),
    ('de',      _('Deutsch')),
    ('it',      _('Italiano')),
    ('ca',      _('Catala')),
    ('gl',      _('Galego')),
    ('eu',      _('Euskara')),
    ('zh-hans', _('Chinese Simplified')),
    ('ja',      _('Japanese')),
    ('ko',      _('Korean')),
    ('ar',      _('Arabic')),
    ('ru',      _('Russian')),
    ('hi',      _('Hindi')),
    ('tr',      _('Turkish')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# -------------------------------------------------------------
# Hosts permitidos (testserver para Django test Client)
# -------------------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
else:
    ALLOWED_HOSTS = ["rhetorica.com", "www.rhetorica.com"]


# -------------------------------------------------------------
# Recursos educativos
# -------------------------------------------------------------
RECURSOS_DIR = BASE_DIR / 'ejercicios_completos-lengua-castellana'
