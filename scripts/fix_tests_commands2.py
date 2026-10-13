"""Fix definitivo: seed_content necesita un admin creado antes."""
from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\tests\test_management_commands.py")
c = p.read_text(encoding="utf-8")

# Reemplazar la clase TestSeedContent completa
viejo_seed_content = '''class TestSeedContent:
    def test_comando_existe(self):
        from django.core.management import get_commands
        assert "seed_content" in get_commands()

    def test_ejecuta_sin_crash(self, db):
        out = StringIO()
        call_command("seed_content", reset=True, stdout=out)
        # No crashea

    def test_crea_cursos(self, db):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Curso.objects.count() > 0

    def test_crea_modulos(self, db):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Modulo.objects.count() > 0

    def test_crea_lecciones(self, db):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Leccion.objects.count() > 0

    def test_crea_evaluaciones(self, db):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert EvaluacionCurso.objects.count() > 0

    def test_crea_logros(self, db):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Logro.objects.count() > 0

    def test_crea_certificaciones(self, db):
        call_command("seed_content", reset=True, stdout=StringIO())
        assert Certificacion.objects.count() > 0

    def test_imprime_output(self, db):
        out = StringIO()
        call_command("seed_content", reset=True, stdout=out)
        assert len(out.getvalue()) > 0'''

nuevo_seed_content = '''class TestSeedContent:
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
        assert len(out.getvalue()) > 0'''

if viejo_seed_content in c:
    c = c.replace(viejo_seed_content, nuevo_seed_content, 1)
    print("[OK] TestSeedContent reemplazada con admin_user fixture")
else:
    print("[!] No se encontro el bloque TestSeedContent")

# Reemplazar la clase TestSeedAndTest completa
viejo_seed_and = '''class TestSeedAndTest:
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
        # Asegurar grupos base
        call_command("seed_and_test", reset=True, stdout=StringIO())
        nombres = set(Group.objects.values_list("name", flat=True))
        assert len(nombres) >= 3

    def test_crea_cursos(self, db):
        call_command("seed_and_test", reset=True, stdout=StringIO())
        assert Curso.objects.count() > 0'''

nuevo_seed_and = '''class TestSeedAndTest:
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
        assert Curso.objects.count() > 0'''

if viejo_seed_and in c:
    c = c.replace(viejo_seed_and, nuevo_seed_and, 1)
    print("[OK] TestSeedAndTest actualizada")
else:
    print("[!] No se encontro el bloque TestSeedAndTest")

p.write_text(c, encoding="utf-8")
print("[OK] tests reescritos")
