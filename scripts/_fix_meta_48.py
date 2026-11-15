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
    {"ej_id": 261,  # ¿Quién cuenta la historia?
     "enunciado": "En 'Me llamo Carlos', ¿quién cuenta la historia?",
     "opciones": ["Carlos, en primera persona", "Un narrador externo", "Lucía, en primera persona"],
     "correcta": "A",
     "explicacion": "'Me llamo Carlos' es primera persona: el narrador es Carlos."},
    {"ej_id": 818,  # ¿Qué palabra del texto indica número o cantidad?
     "enunciado": "En 'Lucía tiene ocho años', ¿qué palabra indica cantidad?",
     "opciones": ["ocho", "años", "Lucía"], "correcta": "A",
     "explicacion": "'Ocho' es el número que indica la edad de Lucía."},
    {"ej_id": 269,  # ¿Qué personaje es secundario en el cuento?
     "enunciado": "En 'Mi familia', ¿qué personaje es secundario?",
     "opciones": ["Toby, el perro", "Carlos, el narrador", "El lector"], "correcta": "A",
     "explicacion": "Carlos es el narrador; Toby es un personaje secundario de la historia."},
    {"ej_id": 1421,  # cuento / noticia
     "enunciado": "¿Qué tipo de texto es 'Mi familia'?",
     "opciones": ["Un relato personal", "Una noticia", "Una receta"], "correcta": "A",
     "explicacion": "'Mi familia' es un relato personal: Carlos cuenta su vida y su familia."},
    {"ej_id": 830,  # Lucía personaje
     "enunciado": "Lucía aparece en el texto 'Mi familia'. ¿Qué tipo de personaje es?",
     "opciones": ["Un personaje secundario", "El personaje principal", "El narrador"], "correcta": "A",
     "explicacion": "Carlos es el narrador y protagonista; Lucía es su hermana, un personaje secundario."},
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