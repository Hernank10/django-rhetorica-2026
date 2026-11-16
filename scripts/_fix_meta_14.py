import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

parches = [
    {"ej_id": 831,
     "enunciado": "En 'Mi escuela es un edificio grande y amarillo', ¿qué significa 'edificio'?",
     "opciones": ["Una construcción", "Un animal", "Una persona"], "correcta": "A",
     "explicacion": "'Edificio' es una construcción: la escuela es un edificio."},
    {"ej_id": 838,
     "enunciado": "Los niños van a la escuela San Martín y juegan en el patio. ¿Qué edad aproximada tienen?",
     "opciones": ["Niños (6-12 años)", "Adultos", "Ancianos"], "correcta": "A",
     "explicacion": "El texto habla de 'compañeros' y 'recreo', propios de niños de 6 a 12 años."},
    {"ej_id": 250,
     "enunciado": "El texto dice que la escuela es 'un edificio grande y amarillo'. ¿De qué material podría estar hecha?",
     "opciones": ["De ladrillo o cemento", "De tela", "De papel"], "correcta": "A",
     "explicacion": "Un edificio grande se construye con ladrillo o cemento, no con tela ni papel."},
    {"ej_id": 847,
     "enunciado": "El texto dice que la puerta de la escuela es 'verde'. ¿De qué color es la puerta?",
     "opciones": ["Verde", "Rojo", "Azul"], "correcta": "A",
     "explicacion": "El texto dice: 'Delante hay una puerta verde'."},
]
for p in parches:
    try:
        ej = EJ.objects.get(id=p["ej_id"])
    except EJ.DoesNotExist:
        print(f"SKIP ej.id={p['ej_id']} NO EXISTE"); continue
    if ej.enunciado == p["enunciado"]:
        print(f"SKIP ej.id={ej.id} ya reformulado"); continue
    ej.enunciado = p["enunciado"]
    ej.payload = {"opciones": p["opciones"], "correcta": p["correcta"], "explicacion": p["explicacion"]}
    ej.save()
    print(f"OK ej.id={ej.id}  Q: {p['enunciado'][:60]}")
print("OK meta reformuladas")