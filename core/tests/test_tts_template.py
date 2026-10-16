"""Tests de integración TTS en templates (Fase 1 + 1B).

Verifica el contrato HTML del botón Web Speech API en los 4 templates
que muestran contenido audible.
"""

import re
from pathlib import Path

import pytest


BASE = Path(__file__).resolve().parent.parent.parent
TEMPLATES = BASE / "core" / "templates"
STATIC = BASE / "static"


TEMPLATES_CON_TTS = [
    "core/detalle_ejercicio.html",
    "core/practicar_ejercicio.html",
    "core/detalle_ejercicio_completo.html",
    "core/practicar_ejercicio_completo.html",
]


class TestContratoTTS:
    @pytest.mark.parametrize("template", TEMPLATES_CON_TTS)
    def test_boton_tts_presente(self, template):
        c = (TEMPLATES / template).read_text(encoding="utf-8")
        assert "tts-play" in c, f"{template}: falta clase tts-play"
        assert "data-tts-text=" in c, f"{template}: falta data-tts-text"
        assert "data-tts-lang=" in c, f"{template}: falta data-tts-lang"

    @pytest.mark.parametrize("template", TEMPLATES_CON_TTS)
    def test_script_y_css_cargados(self, template):
        c = (TEMPLATES / template).read_text(encoding="utf-8")
        assert "js/tts.js" in c, f"{template}: falta script tts.js"
        assert "css/tts.css" in c, f"{template}: falta css tts.css"

    @pytest.mark.parametrize("template", TEMPLATES_CON_TTS)
    def test_boton_tiene_aria_label(self, template):
        c = (TEMPLATES / template).read_text(encoding="utf-8")
        bloque = re.search(r"<button[^>]*tts-play[^>]*>", c, re.DOTALL)
        assert bloque, f"{template}: no se encontro el boton tts-play"
        assert "aria-label=" in bloque.group(0), f"{template}: sin aria-label"

    @pytest.mark.parametrize("template", TEMPLATES_CON_TTS)
    def test_boton_tiene_texto_visible(self, template):
        """El botón debe tener texto visible, no solo un icono."""
        c = (TEMPLATES / template).read_text(encoding="utf-8")
        bloque = re.search(r"<button[^>]*tts-play[^>]*>.*?</button>", c, re.DOTALL)
        assert bloque, f"{template}: no se encontro el boton completo"
        assert "Escuchar" in bloque.group(0), f"{template}: sin texto 'Escuchar'"


class TestArchivosEstaticos:
    def test_archivos_tts_existen(self):
        assert (STATIC / "js" / "tts.js").exists()
        assert (STATIC / "css" / "tts.css").exists()

    def test_js_usa_webspeech(self):
        c = (STATIC / "js" / "tts.js").read_text(encoding="utf-8")
        assert "speechSynthesis" in c
        assert "SpeechSynthesisUtterance" in c

    def test_js_no_tiene_dependencias_externas(self):
        """Sin jQuery ni otras librerias."""
        c = (STATIC / "js" / "tts.js").read_text(encoding="utf-8")
        assert "jquery" not in c.lower()
        assert "$(" not in c  # no uso de jQuery