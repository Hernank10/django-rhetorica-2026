"""Crea tests extra para cubrir Fase 3 TTS al 97%."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
TESTS = BASE / "core" / "tests"

# ============================================================
# test_commands_precache.py (NUEVO)
# ============================================================
COMMAND_TESTS = """\"\"\"Tests de core/management/commands/precache_tts.py.\"\"\"

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command

from core.models import EjercicioLinguistico


class TestPrecacheTts:
    def test_limpiar_sin_cache(self, db, tmp_path):
        out = StringIO()
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            call_command(\"precache_tts\", \"--limpiar\", stdout=out)
        assert \"Borrados 0 MP3s\" in out.getvalue()

    def test_dry_run_sin_ejercicios(self, db, tmp_path):
        out = StringIO()
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            call_command(\"precache_tts\", \"--dry-run\", stdout=out)
        assert \"Procesando 0 ejercicios\" in out.getvalue()

    def test_dry_run_con_un_ejercicio(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo=\"Test\",
            contenido={\"ejercicio\": \"Escribe algo\"},
        )
        out = StringIO()
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            call_command(\"precache_tts\", \"--dry-run\", stdout=out)
        assert \"Procesando 1 ejercicios\" in out.getvalue()
        assert \"[dry] habria generado\" in out.getvalue()

    def test_ejecuta_generando_mp3(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo=\"Test\",
            contenido={\"ejercicio\": \"Escribe algo\"},
        )
        out = StringIO()
        fake_path = tmp_path / \"fake.mp3\"
        fake_path.write_bytes(b\"x\")
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            with patch(\"core.services.tts.generar_mp3\", return_value=fake_path):
                call_command(\"precache_tts\", stdout=out)
        assert \"Generados\" in out.getvalue()

    def test_ejercicio_sin_texto_omitido(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo=\"\",
            contenido={},
        )
        out = StringIO()
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            call_command(\"precache_tts\", \"--dry-run\", stdout=out)
        assert \"Omitidos\" in out.getvalue()

    def test_ya_cacheado_no_regenera(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo=\"Test\",
            contenido={\"ejercicio\": \"Hola\"},
        )
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            with patch(\"core.services.tts.esta_cacheado\", return_value=True):
                out = StringIO()
                call_command(\"precache_tts\", stdout=out)
        assert \"Ya cacheados: 1\" in out.getvalue()

    def test_fallo_generacion_incrementa_fallidos(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo=\"Test\",
            contenido={\"ejercicio\": \"Hola\"},
        )
        out = StringIO()
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            with patch(\"core.services.tts.generar_mp3\", return_value=None):
                call_command(\"precache_tts\", stdout=out)
        assert \"Fallidos: 1\" in out.getvalue()

    def test_texto_desde_titulo_si_no_ejercicio(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo=\"Solo Titulo\",
            contenido={},
        )
        out = StringIO()
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            call_command(\"precache_tts\", \"--dry-run\", stdout=out)
        assert \"habria generado: 1\" in out.getvalue()

    def test_texto_desde_enunciado(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo=\"Titulo\",
            contenido={\"enunciado\": \"Mi enunciado\"},
        )
        out = StringIO()
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            call_command(\"precache_tts\", \"--dry-run\", stdout=out)
        assert \"habria generado: 1\" in out.getvalue()

    def test_ejercicio_contenido_no_dict(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo=\"Con titulo\",
            contenido=\"string plano\",
        )
        out = StringIO()
        with patch(\"core.services.tts.CACHE_DIR\", tmp_path):
            call_command(\"precache_tts\", \"--dry-run\", stdout=out)
        # cae al titulo
        assert \"habria generado: 1\" in out.getvalue()
"""

# ============================================================
# test_services_tts_extra.py (NUEVO)
# ============================================================
SERVICES_EXTRA = """\"\"\"Tests extra para core/services/tts.py — cobertura de ramas.\"\"\"

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from core.services import tts


class TestGenerarMP3Ramas:
    def test_sin_gtts_importado(self, tmp_path, monkeypatch):
        \"\"\"Cuando gTTS no se puede importar → None.\"\"\"
        monkeypatch.setattr(tts, \"CACHE_DIR\", tmp_path)
        with patch.dict(sys.modules, {\"gtts\": None}):
            with patch(\"builtins.__import__\", side_effect=ImportError(\"no gtts\")):
                r = tts.generar_mp3(\"texto unico para forzar import\", \"es\")
        assert r is None

    def test_excepcion_en_gtts_retorna_none(self, tmp_path, monkeypatch):
        \"\"\"Si gTTS lanza excepcion → None (no propaga).\"\"\"
        monkeypatch.setattr(tts, \"CACHE_DIR\", tmp_path)
        with patch(\"gtts.gTTS\", side_effect=Exception(\"boom\")):
            r = tts.generar_mp3(\"texto unico exception\", \"es\")
        assert r is None

    def test_excepcion_en_save_retorna_none(self, tmp_path, monkeypatch):
        \"\"\"Si save() falla → None.\"\"\"
        monkeypatch.setattr(tts, \"CACHE_DIR\", tmp_path)
        with patch(\"gtts.gTTS\") as mock_gtts:
            mock_inst = MagicMock()
            mock_inst.save.side_effect = OSError(\"disk full\")
            mock_gtts.return_value = mock_inst
            r = tts.generar_mp3(\"texto save fail\", \"es\")
        assert r is None


class TestLimpiarCacheErrores:
    def test_no_borra_si_no_existe(self, tmp_path, monkeypatch):
        \"\"\"Si CACHE_DIR no existe → 0.\"\"\"
        no_existe = tmp_path / \"no_existe\"
        monkeypatch.setattr(tts, \"CACHE_DIR\", no_existe)
        assert tts.limpiar_cache() == 0
"""


def main():
    TESTS.mkdir(parents=True, exist_ok=True)

    p1 = TESTS / "test_commands_precache.py"
    p1.write_text(COMMAND_TESTS, encoding="utf-8")
    print(f"[OK] {p1.relative_to(BASE)} ({len(COMMAND_TESTS)} bytes)")

    p2 = TESTS / "test_services_tts_extra.py"
    p2.write_text(SERVICES_EXTRA, encoding="utf-8")
    print(f"[OK] {p2.relative_to(BASE)} ({len(SERVICES_EXTRA)} bytes)")


if __name__ == "__main__":
    main()