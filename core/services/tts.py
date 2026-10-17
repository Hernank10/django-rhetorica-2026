"""Servicio de Text-to-Speech con gTTS y cache en disco."""

import hashlib
from pathlib import Path

from django.conf import settings


CACHE_DIR = Path(settings.BASE_DIR) / "tts_cache"
MAX_TEXTO = 5000


def _normalizar_texto(texto: str) -> str:
    """Colapsa whitespace para hashing estable."""
    return " ".join(texto.split()) if texto else ""


def hash_tts(texto: str, lang: str = "es") -> str:
    """Hash determinista del par (texto, lang)."""
    normalizado = _normalizar_texto(texto)
    key = f"{lang}:{normalizado}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]


def ruta_cache(texto: str, lang: str = "es") -> Path:
    """Path absoluto del MP3 cacheado."""
    return CACHE_DIR / f"{hash_tts(texto, lang)}.mp3"


def esta_cacheado(texto: str, lang: str = "es") -> bool:
    """True si el MP3 ya existe en disco."""
    if not _normalizar_texto(texto):
        return False
    return ruta_cache(texto, lang).exists()


def generar_mp3(texto: str, lang: str = "es"):
    """Genera (o reutiliza) el MP3. Devuelve Path o None si falla."""
    normalizado = _normalizar_texto(texto)
    if not normalizado or len(normalizado) > MAX_TEXTO:
        return None

    destino = ruta_cache(normalizado, lang)
    if destino.exists():
        return destino

    try:
        from gtts import gTTS
    except ImportError:
        return None

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        gTTS(text=normalizado, lang=lang, slow=False).save(str(destino))
        return destino
    except Exception:
        return None


def limpiar_cache() -> int:
    """Borra todos los MP3s cacheados. Devuelve cuántos borró."""
    if not CACHE_DIR.exists():
        return 0
    n = 0
    for p in CACHE_DIR.glob("*.mp3"):
        try:
            p.unlink()
            n += 1
        except OSError:
            pass
    return n