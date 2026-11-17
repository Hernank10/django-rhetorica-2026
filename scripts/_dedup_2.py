import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

borrar = [983, 985]  # duplicados de 1714, 1717
for ej_id in borrar:
    try:
        ej = EJ.objects.get(id=ej_id)
        print(f"DELETE ej.id={ej_id}  Q: {(ej.enunciado or '')[:60]}")
        ej.delete()
    except EJ.DoesNotExist:
        print(f"SKIP ej.id={ej_id} NO EXISTE")
print("OK dedup")