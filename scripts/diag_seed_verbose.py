"""Ejecutar seed_content --reset en ambiente aislado y ver que pasa."""
import sys, os
from pathlib import Path
from io import StringIO

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.runner import DiscoverRunner

setup_test_environment()
runner = DiscoverRunner(verbosity=0)
old_config = runner.setup_databases()

try:
    from django.core.management import call_command
    from core.models_cursos import Curso, Modulo, Leccion

    print("=" * 70)
    print("ANTES: Cursos=%d Modulos=%d Lecciones=%d" % (
        Curso.objects.count(), Modulo.objects.count(), Leccion.objects.count()
    ))
    print("=" * 70)

    out = StringIO()
    err = StringIO()
    try:
        call_command("seed_content", reset=True, stdout=out, stderr=err)
    except SystemExit as e:
        print("[SystemExit] codigo=%s" % e.code)
    except Exception as e:
        print("[EXCEPCION] %s: %s" % (type(e).__name__, e))

    print()
    print("=" * 70)
    print("STDOUT DEL COMANDO (primeros 4000 chars):")
    print("=" * 70)
    txt = out.getvalue()
    print(txt[:4000])

    print()
    print("=" * 70)
    print("STDERR DEL COMANDO (primeros 2000 chars):")
    print("=" * 70)
    print(err.getvalue()[:2000])

    print()
    print("=" * 70)
    print("DESPUES: Cursos=%d Modulos=%d Lecciones=%d" % (
        Curso.objects.count(), Modulo.objects.count(), Leccion.objects.count()
    ))
    print("=" * 70)

finally:
    runner.teardown_databases(old_config)
    teardown_test_environment()
