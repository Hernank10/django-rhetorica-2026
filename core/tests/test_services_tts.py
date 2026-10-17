"""Tests de core/services/tts.py (sin llamar a gTTS real)."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.services import tts


class TestHash:
    def test_determinista(self):
        assert tts.hash_tts("hola", "es") == tts.hash_tts("hola", "es")

    def test_distinto_idioma(self):
        assert tts.hash_tts("hola", "es") != tts.hash_tts("hola", "en")

    def test_normaliza_whitespace(self):
        assert tts.hash_tts("hola   mundo", "es") == tts.hash_tts("hola mundo", "es")

    def test_normaliza_saltos_linea(self):
        assert tts.hash_tts("a\nb", "es") == tts.hash_tts("a b", "es")

    def test_vacio(self):
        assert tts.hash_tts("", "es") == tts.hash_tts("", "es")


class TestCacheCheck:
    def test_vacio_no_esta_cacheado(self):
        assert tts.esta_cacheado("", "es") is False

    def test_whitespace_no_esta_cacheado(self):
        assert tts.esta_cacheado("   ", "es") is False


class TestGenerarMP3:
    def test_vacio_retorna_none(self):
        assert tts.generar_mp3("", "es") is None

    def test_texto_muy_largo_retorna_none(self):
        texto = "x" * (tts.MAX_TEXTO + 1)
        assert tts.generar_mp3(texto, "es") is None

    def test_genera_y_guarda(self, tmp_path, monkeypatch):
        monkeypatch.setattr(tts, "CACHE_DIR", tmp_path)

        def fake_save(path):
            Path(path).write_bytes(b"fake mp3 bytes")

        with patch("gtts.gTTS") as mock_gtts:
            mock_inst = MagicMock()
            mock_inst.save.side_effect = fake_save
            mock_gtts.return_value = mock_inst

            r = tts.generar_mp3("hola mundo", "es")
            assert r is not None
            assert r.exists()
            assert mock_gtts.call_count == 1

    def test_cache_hit_no_reinvoca_gtts(self, tmp_path, monkeypatch):
        monkeypatch.setattr(tts, "CACHE_DIR", tmp_path)

        def fake_save(path):
            Path(path).write_bytes(b"fake mp3")

        with patch("gtts.gTTS") as mock_gtts:
            mock_inst = MagicMock()
            mock_inst.save.side_effect = fake_save
            mock_gtts.return_value = mock_inst

            r1 = tts.generar_mp3("hola", "es")
            r2 = tts.generar_mp3("hola", "es")

            assert r1 == r2
            assert mock_gtts.call_count == 1


class TestLimpiarCache:
    def test_vacio_retorna_0(self, tmp_path, monkeypatch):
        monkeypatch.setattr(tts, "CACHE_DIR", tmp_path)
        assert tts.limpiar_cache() == 0

    def test_borra_mp3s(self, tmp_path, monkeypatch):
        monkeypatch.setattr(tts, "CACHE_DIR", tmp_path)
        (tmp_path / "a.mp3").write_bytes(b"x")
        (tmp_path / "b.mp3").write_bytes(b"y")
        (tmp_path / "c.txt").write_text("no borrar")

        assert tts.limpiar_cache() == 2
        assert not (tmp_path / "a.mp3").exists()
        assert (tmp_path / "c.txt").exists()
