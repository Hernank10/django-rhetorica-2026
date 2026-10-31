import pytest
from django.core.management import call_command

pytestmark = pytest.mark.django_db

def test_load_progress_fixture_sin_fichero_no_rompe():
    call_command("load_progress_fixture", fixture="fixtures/inexistente.json", verbosity=0)
