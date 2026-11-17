import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
TX = apps.get_model("core", "Texto")

tx = TX.objects.get(id=7)
with open("docs/_body_7.txt", "w", encoding="utf-8") as f:
    f.write(tx.cuerpo)
print(f"Guardado en docs/_body_7.txt ({len(tx.cuerpo)} caracteres)")