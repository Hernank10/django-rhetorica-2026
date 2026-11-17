import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

ej_id = 1737
nuevo = {
    "enunciado": "¿El texto 'La fuerza de las palabras' es coherente y está bien estructurado?",
    "opciones": ["Sí, usa párrafos cortos, ideas claras y ejemplos concretos", "No, es confuso", "No, usa palabras muy técnicas", "No se puede saber"],
    "correcta": "A",
    "explicacion": "El texto tiene introducción, desarrollo y conclusión, con ejemplos y citas claras.",
}
try:
    ej = EJ.objects.get(id=ej_id)
    ej.enunciado = nuevo["enunciado"]
    ej.payload = {"opciones": nuevo["opciones"], "correcta": nuevo["correcta"], "explicacion": nuevo["explicacion"]}
    ej.save()
    print(f"OK ej.id={ej_id}  Q: {nuevo['enunciado'][:70]}")
except EJ.DoesNotExist:
    print(f"SKIP ej.id={ej_id} NO EXISTE")