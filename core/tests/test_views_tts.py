"""Tests de core/views_tts.py (con gTTS mockeado)."""

from unittest.mock import patch

import pytest
from django.urls import reverse


class TestServirAudio:
    def test_sin_text_400(self, db, client):
        r = client.get(reverse("tts_servir"))
        assert r.status_code == 400

    def test_texto_muy_largo_400(self, db, client):
        from core.services import tts
        texto = "x" * (tts.MAX_TEXTO + 1)
        r = client.get(reverse("tts_servir"), {"text": texto, "lang": "es"})
        assert r.status_code == 400

    def test_idioma_invalido_usa_es(self, db, client, tmp_path):
        path = tmp_path / "fake.mp3"
        path.write_bytes(b"fake mp3 data")
        with patch("core.views_tts.tts.generar_mp3", return_value=path):
            r = client.get(reverse("tts_servir"), {"text": "hola", "lang": "xx"})
            assert r.status_code == 200

    def test_genera_mp3_ok(self, db, client, tmp_path):
        path = tmp_path / "hola.mp3"
        path.write_bytes(b"fake mp3 data")
        with patch("core.views_tts.tts.generar_mp3", return_value=path):
            r = client.get(reverse("tts_servir"), {"text": "hola", "lang": "es"})
            assert r.status_code == 200
            assert r["Content-Type"] == "audio/mpeg"
            assert "max-age" in r["Cache-Control"]

    def test_generacion_fallida_503(self, db, client):
        with patch("core.views_tts.tts.generar_mp3", return_value=None):
            r = client.get(reverse("tts_servir"), {"text": "hola", "lang": "es"})
            assert r.status_code == 503

    def test_url_resuelve(self):
        assert reverse("tts_servir") == "/tts/"
