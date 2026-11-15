import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

ejs = list(EJ.objects.filter(texto_id=48).order_by("orden","id"))
print(f"Renumerando {len(ejs)} ejercicios 1..{len(ejs)}")
for i, ej in enumerate(ejs, start=1):
    print(f"  ej.id={ej.id:>5}  {ej.orden!r:>5} -> {i:>2}  Q: {(ej.enunciado or '')[:50]}")
    ej.orden = i
    ej.save(update_fields=["orden"])
print("OK renumerado")