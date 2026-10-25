"""
Settings base — comunes a dev y prod.
Configuracion sensible se lee desde .env.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Cargar .env (raiz del proyecto)
load_dotenv(BASE_DIR / ".env")

# ─── SECRET_KEY ───
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "SECRET_KEY no esta definida. Crea .env con SECRET_KEY=<clave>"
    )

# ─── Debug (default seguro) ───
# dev.py y prod.py lo sobrescriben explicitamente
DEBUG = False

# ─── ALLOWED_HOSTS ───
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        "ALLOWED_HOSTS", "localhost,127.0.0.1,testserver,[::1]"
    ).split(",")
    if h.strip()
]

# ─── Aplicaciones ───
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

# ─── Middleware (prod agrega WhiteNoise via insert) ───
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_retorica.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_retorica.wsgi.application"

# ─── Password validation ───
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── i18n ───
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("es", _("Español")),
    ("en", _("English")),
    ("pt", _("Portugués")),
    ("fr", _("Francés")),
    ("de", _("Deutsch")),
    ("it", _("Italiano")),
    ("ca", _("Catala")),
    ("gl", _("Galego")),
    ("eu", _("Euskara")),
    ("zh-hans", _("Chinese Simplified")),
    ("ja", _("Japanese")),
    ("ko", _("Korean")),
    ("ar", _("Arabic")),
    ("ru", _("Russian")),
    ("hi", _("Hindi")),
    ("tr", _("Turkish")),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

# ─── Estaticos y media (una sola vez) ───
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ─── Default PK ───
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── Recursos educativos ───
RECURSOS_DIR = BASE_DIR / "ejercicios_completos-lengua-castellana"

# ─── Auth redirects ───
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# ─── Motor de adaptabilidad ───
ADAPTIVE_ERROR_WINDOW_DAYS = 7
ADAPTIVE_ERROR_THRESHOLD = 3
ADAPTIVE_MASTERY_THRESHOLD = 3

# ============================================================
# STORAGES: filesystem local (dev) o S3/SeaweedFS/B2 (USE_S3)
# ============================================================
USE_S3 = os.getenv("USE_S3", "False").lower() in ("true", "1", "yes")

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-east-1")
    AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")

    if not AWS_STORAGE_BUCKET_NAME:
        raise ImproperlyConfigured("USE_S3=True pero falta AWS_STORAGE_BUCKET_NAME")

    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL or None,
            "region_name": AWS_S3_REGION_NAME,
            "default_acl": "public-read",
            "querystring_auth": False,
            "file_overwrite": False,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN or None,
        },
    }

