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
    {"ej_id": 779,
     "enunciado": "¿Cuál es el propósito del primer párrafo del texto?",
     "opciones": ["Presentar el reciclaje de vidrio en España", "Describir el proceso de reciclaje", "Criticar a los ciudadanos", "Hablar de la fábula de la cigarra"],
     "correcta": "A",
     "explicacion": "El primer párrafo presenta el tema: el reciclaje de vidrio en España y sus datos."},
    {"ej_id": 799,
     "enunciado": "¿Cuál es la tesis del texto?",
     "opciones": ["El reciclaje de vidrio es importante pero aún hay margen de mejora", "El reciclaje de vidrio es imposible", "Nadie recicla vidrio en España", "El vidrio no se puede reciclar"],
     "correcta": "A",
     "explicacion": "El texto defiende que el reciclaje ha crecido, pero aún queda trabajo por hacer."},
    {"ej_id": 1654,
     "enunciado": "¿Cuál es la idea central que plantea el texto?",
     "opciones": ["El reciclaje de vidrio en España ha crecido, pero aún puede mejorar", "El reciclaje de vidrio es una moda pasajera", "El vidrio es el único material reciclable", "Nadie recicla vidrio en España"],
     "correcta": "A",
     "explicacion": "La idea central es el crecimiento del reciclaje y la necesidad de mejorar."},
    {"ej_id": 1658,
     "enunciado": "¿Para qué fue escrito este texto?",
     "opciones": ["Para informar sobre el reciclaje de vidrio en España", "Para vender contenedores verdes", "Para criticar a los expertos", "Para contar un cuento"],
     "correcta": "A",
     "explicacion": "El texto es informativo: informa sobre el reciclaje de vidrio en España."},
    {"ej_id": 1659,
     "enunciado": "¿Qué idea principal defiende el autor en este texto?",
     "opciones": ["Que el reciclaje de vidrio es positivo y debe mejorar", "Que el reciclaje de vidrio es inútil", "Que el vidrio no se recicla", "Que la educación ambiental no sirve"],
     "correcta": "A",
     "explicacion": "El autor defiende el reciclaje y pide más educación ambiental."},
    {"ej_id": 767,
     "enunciado": "¿Cuál es la idea principal del primer párrafo?",
     "opciones": ["El reciclaje de vidrio en España y sus datos de 2023", "El proceso de reciclaje", "La fábula de la cigarra", "Las tasas de reciclaje bajas"],
     "correcta": "A",
     "explicacion": "El primer párrafo presenta el reciclaje de vidrio en España y los datos de Ecovidrio."},
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