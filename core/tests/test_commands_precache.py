"""Tests de core/management/commands/precache_tts.py."""

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command

from core.models import EjercicioLinguistico


class TestPrecacheTts:
    def test_limpiar_sin_cache(self, db, tmp_path):
        out = StringIO()
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            call_command("precache_tts", "--limpiar", stdout=out)
        assert "Borrados 0 MP3s" in out.getvalue()

    def test_dry_run_sin_ejercicios(self, db, tmp_path):
        out = StringIO()
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            call_command("precache_tts", "--dry-run", stdout=out)
        assert "Procesando 0 ejercicios" in out.getvalue()

    def test_dry_run_con_un_ejercicio(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo="Test",
            contenido={"ejercicio": "Escribe algo"},
        )
        out = StringIO()
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            call_command("precache_tts", "--dry-run", stdout=out)
        assert "Procesando 1 ejercicios" in out.getvalue()
        assert "[dry] habria generado" in out.getvalue()

    def test_ejecuta_generando_mp3(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo="Test",
            contenido={"ejercicio": "Escribe algo"},
        )
        out = StringIO()
        fake_path = tmp_path / "fake.mp3"
        fake_path.write_bytes(b"x")
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            with patch("core.services.tts.generar_mp3", return_value=fake_path):
                call_command("precache_tts", stdout=out)
        assert "Generados" in out.getvalue()

    def test_ejercicio_sin_texto_omitido(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo="",
            contenido={},
        )
        out = StringIO()
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            call_command("precache_tts", "--dry-run", stdout=out)
        assert "Omitidos" in out.getvalue()

    def test_ya_cacheado_no_regenera(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo="Test",
            contenido={"ejercicio": "Hola"},
        )
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            with patch("core.services.tts.esta_cacheado", return_value=True):
                out = StringIO()
                call_command("precache_tts", stdout=out)
        assert "Ya cacheados: 1" in out.getvalue()

    def test_fallo_generacion_incrementa_fallidos(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo="Test",
            contenido={"ejercicio": "Hola"},
        )
        out = StringIO()
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            with patch("core.services.tts.generar_mp3", return_value=None):
                call_command("precache_tts", stdout=out)
        assert "Fallidos: 1" in out.getvalue()

    def test_texto_desde_titulo_si_no_ejercicio(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo="Solo Titulo",
            contenido={},
        )
        out = StringIO()
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            call_command("precache_tts", "--dry-run", stdout=out)
        assert "habria generado: 1" in out.getvalue()

    def test_texto_desde_enunciado(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo="Titulo",
            contenido={"enunciado": "Mi enunciado"},
        )
        out = StringIO()
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            call_command("precache_tts", "--dry-run", stdout=out)
        assert "habria generado: 1" in out.getvalue()

    def test_ejercicio_contenido_no_dict(self, db, tmp_path):
        EjercicioLinguistico.objects.create(
            titulo="Con titulo",
            contenido="string plano",
        )
        out = StringIO()
        with patch("core.services.tts.CACHE_DIR", tmp_path):
            call_command("precache_tts", "--dry-run", stdout=out)
        # cae al titulo
        assert "habria generado: 1" in out.getvalue()
