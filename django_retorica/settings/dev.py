"""Settings de desarrollo local (DEBUG=True, SQLite)."""

from .base import *  # noqa: F401, F403

DEBUG = True

# ─── SQLite ───
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# ─── Codespaces / dev remoto ───
CSRF_TRUSTED_ORIGINS = [
    "https://*.githubpreview.dev",
    "https://*.app.github.dev",
    "http://*.githubpreview.dev",
    "http://*.app.github.dev",
    "https://*.codespaces.app",
    "http://*.codespaces.app",
    "https://localhost:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# ─── Cookies no-secure (dev sin HTTPS) ───
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False
