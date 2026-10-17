"""Tests extra para core/services/tts.py — cobertura de ramas."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.services import tts


class TestGenerarMP3Ramas:
    def test_sin_gtts_importado(self, tmp_path, monkeypatch):
        """Cuando gTTS no se puede importar → None."""
        monkeypatch.setattr(tts, "CACHE_DIR", tmp_path)
        with patch.dict(sys.modules, {"gtts": None}):
            with patch("builtins.__import__", side_effect=ImportError("no gtts")):
                r = tts.generar_mp3("texto unico para forzar import", "es")
        assert r is None

    def test_excepcion_en_gtts_retorna_none(self, tmp_path, monkeypatch):
        """Si gTTS lanza excepcion → None (no propaga)."""
        monkeypatch.setattr(tts, "CACHE_DIR", tmp_path)
        with patch("gtts.gTTS", side_effect=Exception("boom")):
            r = tts.generar_mp3("texto unico exception", "es")
        assert r is None

    def test_excepcion_en_save_retorna_none(self, tmp_path, monkeypatch):
        """Si save() falla → None."""
        monkeypatch.setattr(tts, "CACHE_DIR", tmp_path)
        with patch("gtts.gTTS") as mock_gtts:
            mock_inst = MagicMock()
            mock_inst.save.side_effect = OSError("disk full")
            mock_gtts.return_value = mock_inst
            r = tts.generar_mp3("texto save fail", "es")
        assert r is None


class TestLimpiarCacheErrores:
    def test_no_borra_si_no_existe(self, tmp_path, monkeypatch):
        """Si CACHE_DIR no existe → 0."""
        no_existe = tmp_path / "no_existe"
        monkeypatch.setattr(tts, "CACHE_DIR", no_existe)
        assert tts.limpiar_cache() == 0
