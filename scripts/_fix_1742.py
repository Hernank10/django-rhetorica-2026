import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

ej_id = 1742
nuevo = {
    "enunciado": "¿Cuál de las siguientes afirmaciones resume mejor el texto?",
    "opciones": [
        "El reciclaje de vidrio en España ha crecido, pero aún hay margen de mejora",
        "El reciclaje de vidrio es imposible en España",
        "Nadie recicla vidrio en España",
        "El vidrio no se puede reciclar",
    ],
    "correcta": "A",
    "explicacion": "El texto destaca el crecimiento del reciclaje y la necesidad de mejorar.",
}
try:
    ej = EJ.objects.get(id=ej_id)
    ej.payload = {"opciones": nuevo["opciones"], "correcta": nuevo["correcta"], "explicacion": nuevo["explicacion"]}
    ej.save()
    print(f"OK ej.id={ej_id}  opciones={len(nuevo['opciones'])}  correcta={nuevo['correcta']}")
except EJ.DoesNotExist:
    print(f"SKIP ej.id={ej_id} NO EXISTE")