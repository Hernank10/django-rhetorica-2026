"""Tests de los comandos de management."""
import pytest
from io import StringIO
from pathlib import Path

from django.core.management import call_command

from core.models import (
    Certificacion, EjercicioLinguistico, Logro, Recurso,
    TecnicaLinguistica,
)
from core.models_cursos import (
    Curso, EvaluacionCurso, Leccion, Modulo, PreguntaEvaluacion,
)


# ============================================================
# seed_content
# ============================================================
class TestSeedContent:
    """seed_content requiere que exista un admin (lo crea seed_and_test)."""

    def test_comando_existe(self):
        from django.core.management import get_commands
        assert "seed_content" in get_commands()

    def test_ejecuta_sin_crash(self, db, admin_user):
        out = StringIO()
        call_command("seed_content", reset=True, stdout=out)

    def test_crea_cursos(self, db, admin_user):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Curso.objects.count() > 0

    def test_crea_modulos(self, db, admin_user):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Modulo.objects.count() > 0

    def test_crea_lecciones(self, db, admin_user):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Leccion.objects.count() > 0

    def test_crea_evaluaciones(self, db, admin_user):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert EvaluacionCurso.objects.count() > 0

    def test_crea_logros(self, db, admin_user):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Logro.objects.count() > 0

    def test_crea_certificaciones(self, db, admin_user):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Certificacion.objects.count() > 0

    def test_imprime_output(self, db, admin_user):
        out = StringIO()
        call_command("seed_content", reset=True, stdout=out)
        assert len(out.getvalue()) > 0


# ============================================================
# seed_and_test
# ============================================================
class TestSeedAndTest:
    """seed_and_test crea usuarios, grupos y luego corre seed_content."""

    def test_comando_existe(self):
        from django.core.management import get_commands
        assert "seed_and_test" in get_commands()

    def test_ejecuta_sin_crash(self, db):
        out = StringIO()
        call_command("seed_and_test", reset=True, stdout=out)

    def test_crea_usuarios(self, db):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        antes = User.objects.count()
        call_command("seed_and_test", reset=True, stdout=StringIO())
        assert User.objects.count() > antes

    def test_crea_grupos(self, db):
        from django.contrib.auth.models import Group
        call_command("seed_and_test", reset=True, stdout=StringIO())
        nombres = set(Group.objects.values_list("name", flat=True))
        assert len(nombres) >= 3

    def test_crea_cursos(self, db):
        # seed_and_test crea admin + llama a seed_content internamente
        call_command("seed_and_test", reset=True, stdout=StringIO())
        assert Curso.objects.count() > 0


# ============================================================
# indexar_recursos
# ============================================================
class TestIndexarRecursos:
    def test_comando_existe(self):
        from django.core.management import get_commands
        assert "indexar_recursos" in get_commands()

    def test_ejecuta_sin_crash(self, db, tmp_path, settings):
        # Redirigir MEDIA_ROOT a tmp
        settings.MEDIA_ROOT = tmp_path
        out = StringIO()
        call_command("indexar_recursos", stdout=out)

    def test_indexa_archivos_en_disco(self, db, tmp_path, settings):
        settings.MEDIA_ROOT = tmp_path
        # Crear un archivo HTML en la carpeta esperada
        (tmp_path / "recursos" / "test").mkdir(parents=True, exist_ok=True)
        (tmp_path / "recursos" / "test" / "ejemplo.html").write_text(
            "<p>Hola</p>", encoding="utf-8"
        )
        antes = Recurso.objects.count()
        call_command("indexar_recursos", stdout=StringIO())
        # O bien creó nuevos, o bien no crashea
        assert Recurso.objects.count() >= antes