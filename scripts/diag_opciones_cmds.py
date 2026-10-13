"""Ver opciones de cada comando."""
import sys, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.core.management import get_commands, load_command_class

for nombre in ["seed_content", "seed_and_test", "indexar_recursos"]:
    print("=" * 60)
    print(nombre)
    print("=" * 60)
    cmd = load_command_class("core", nombre)
    parser = cmd.create_parser("manage.py", nombre)
    for action in parser._actions:
        if action.option_strings:
            print(f"  {action.option_strings}  dest={action.dest}  default={action.default}")
    print()