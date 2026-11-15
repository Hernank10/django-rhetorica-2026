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
    {"ej_id": 1420,
     "enunciado": "En 'No me gusta el invierno porque hace mucho frío', ¿qué es la causa?",
     "opciones": ["Que hace mucho frío", "Que no le gusta el invierno", "Que llueve"],
     "correcta": "A",
     "explicacion": "El texto dice: 'No me gusta el invierno porque hace mucho frío y llueve'."},
    {"ej_id": 1423,
     "enunciado": "En 'Me gusta mucho el verano', ¿es un hecho o una opinión?",
     "opciones": ["Una opinión: expresa una preferencia personal", "Un hecho verificable", "Una instrucción"],
     "correcta": "A",
     "explicacion": "'Me gusta' expresa una preferencia subjetiva."},
    {"ej_id": 1424,
     "enunciado": "En 'En julio vamos a la playa', ¿es un hecho o una opinión?",
     "opciones": ["Un hecho: se puede verificar", "Una opinión personal", "Una pregunta retórica"],
     "correcta": "A",
     "explicacion": "'Vamos a la playa en julio' es un hecho verificable."},
]
for p in parches:
    try:
        ej = EJ.objects.get(id=p["ej_id"])
    except EJ.DoesNotExist:
        print(f"SKIP ej.id={p['ej_id']}"); continue
    if ej.enunciado == p["enunciado"]:
        print(f"SKIP ej.id={ej.id} ya reformulado"); continue
    ej.enunciado = p["enunciado"]
    ej.payload = {"opciones": p["opciones"], "correcta": p["correcta"], "explicacion": p["explicacion"]}
    ej.save()
    print(f"OK ej.id={ej.id}  Q: {p['enunciado'][:60]}")
print("OK meta reformuladas")