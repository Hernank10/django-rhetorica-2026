import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

ej_id = 400
nuevo = {
    "enunciado": "En 'Lucía sintió que el corazón le daba un vuelco', ¿qué significa esa expresión?",
    "opciones": ["Que se sorprendió o emocionó mucho", "Que le dolía el pecho", "Que tenía frío", "Que estaba cansada"],
    "correcta": "A",
    "explicacion": "'El corazón le daba un vuelco' es una expresión que indica sorpresa o emoción intensa.",
}
try:
    ej = EJ.objects.get(id=ej_id)
    ej.enunciado = nuevo["enunciado"]
    ej.payload = {"opciones": nuevo["opciones"], "correcta": nuevo["correcta"], "explicacion": nuevo["explicacion"]}
    ej.save()
    print(f"OK ej.id={ej_id}  Q: {nuevo['enunciado'][:70]}")
except EJ.DoesNotExist:
    print(f"SKIP ej.id={ej_id} NO EXISTE")