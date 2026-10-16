"""Tests de integración TTS en templates (Fase 1).

Verifica el contrato HTML del botón Web Speech API:
  - Clase .tts-play presente
  - data-tts-text y data-tts-lang
  - Scripts y CSS cargados
  - aria-label en el botón
"""

import re
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent.parent
TEMPLATES = BASE / "core" / "templates"
STATIC = BASE / "static"


class TestContratoTTS:
    def test_boton_tts_en_detalle_ejercicio(self):
        c = (TEMPLATES / "core" / "detalle_ejercicio.html").read_text(encoding="utf-8")
        assert "tts-play" in c, "Falta clase tts-play"
        assert "data-tts-text=" in c, "Falta atributo data-tts-text"
        assert "data-tts-lang=" in c, "Falta atributo data-tts-lang"

    def test_script_y_css_en_detalle_ejercicio(self):
        c = (TEMPLATES / "core" / "detalle_ejercicio.html").read_text(encoding="utf-8")
        assert "js/tts.js" in c, "Falta script tts.js"
        assert "css/tts.css" in c, "Falta css tts.css"

    def test_archivos_estaticos_existen(self):
        assert (STATIC / "js" / "tts.js").exists(), "Falta static/js/tts.js"
        assert (STATIC / "css" / "tts.css").exists(), "Falta static/css/tts.css"

    def test_js_usa_webspeech(self):
        c = (STATIC / "js" / "tts.js").read_text(encoding="utf-8")
        assert "speechSynthesis" in c
        assert "SpeechSynthesisUtterance" in c

    def test_boton_tiene_aria_label(self):
        c = (TEMPLATES / "core" / "detalle_ejercicio.html").read_text(encoding="utf-8")
        bloque = re.search(r"<button[^>]*tts-play[^>]*>", c, re.DOTALL)
        assert bloque, "No se encontro el boton tts-play"
        assert "aria-label=" in bloque.group(0), "El boton TTS no tiene aria-label"

    def test_boton_no_es_decorativo(self):
        """El botón debe tener texto visible, no solo un icono."""
        c = (TEMPLATES / "core" / "detalle_ejercicio.html").read_text(encoding="utf-8")
        bloque = re.search(r"<button[^>]*tts-play[^>]*>.*?</button>", c, re.DOTALL)
        assert bloque, "No se encontro el boton completo"
        assert "Escuchar" in bloque.group(0), "El boton TTS no tiene texto visible"