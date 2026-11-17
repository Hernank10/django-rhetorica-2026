import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
from django.db.models import Max
EJ = apps.get_model("core", "EjercicioLectura")
TL = apps.get_model("core", "TecnicaLectura")

# Técnicas huérfanas: #7 (definición de término) y #61 (actualidad de fuente)
nuevas = [
    {
        "tec_num": 7,
        "enunciado": "En 'Las palabras no son solo sonidos: tienen poder', ¿qué término se define en el texto?",
        "opciones": ["Las palabras", "Los sonidos", "El poder", "La Universidad de Stanford"],
        "correcta": "A",
        "explicacion": "El texto define las palabras: 'Las palabras no son solo sonidos: tienen poder'.",
    },
    {
        "tec_num": 61,
        "enunciado": "El texto cita un estudio de la Universidad de Stanford de 2023. ¿Qué se puede inferir sobre su actualidad?",
        "opciones": ["Es una fuente reciente y actual", "Es una fuente obsoleta", "No tiene fecha", "Es del siglo XIX"],
        "correcta": "A",
        "explicacion": "El estudio es de 2023, por lo que es una fuente reciente y actual.",
    },
]

max_orden = EJ.objects.filter(texto_id=21).aggregate(m=Max("orden"))["m"] or 0
creados = 0
for i, n in enumerate(nuevas, start=1):
    tec = TL.objects.filter(numero=n["tec_num"], nivel_mcer="B1").first()
    if not tec:
        print(f"SKIP tec_num={n['tec_num']} no existe B1")
        continue
    if EJ.objects.filter(texto_id=21, enunciado=n["enunciado"]).exists():
        print(f"SKIP duplicado: {n['enunciado'][:50]}")
        continue
    ej = EJ.objects.create(
        texto_id=21, tecnica=tec, enunciado=n["enunciado"],
        tipo="multiple_choice",
        payload={"opciones": n["opciones"], "correcta": n["correcta"], "explicacion": n["explicacion"]},
        orden=max_orden + i,
    )
    print(f"CREADO ej.id={ej.id}  tec=#{tec.numero}  orden={ej.orden}")
    creados += 1
print(f"OK {creados} nuevos")