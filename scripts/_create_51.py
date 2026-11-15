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

nuevas = [
    {"tec_num": 27,  # Localizar los signos de puntuación
     "enunciado": "¿Cuántos párrafos tiene el texto 'Me gusta el verano'?",
     "opciones": ["Cuatro", "Uno", "Dos"], "correcta": "A",
     "explicacion": "El texto está dividido en cuatro párrafos separados por puntos y aparte."},
    {"tec_num": 14,  # Distinguir causa y consecuencia en una oración
     "enunciado": "En 'No me gusta el invierno porque hace frío', ¿qué es la causa?",
     "opciones": ["Que hace frío", "Que no le gusta el invierno", "Que llueve"], "correcta": "A",
     "explicacion": "La causa es el frío; la consecuencia, que no le gusta el invierno."},
    {"tec_num": 56,  # Inferir si un personaje miente o dice la verdad
     "enunciado": "Cuando el narrador dice 'me gusta mucho el verano', ¿qué expresa?",
     "opciones": ["Una preferencia verdadera", "Una mentira", "Una duda"], "correcta": "A",
     "explicacion": "El narrador expresa una preferencia personal coherente con todo el texto."},
    {"tec_num": 80,  # Distinguir causa de consecuencia en una oración
     "enunciado": "En 'Cuando llega septiembre, ya estoy esperando el próximo verano', ¿qué es la consecuencia?",
     "opciones": ["Esperar el próximo verano", "Que llega septiembre", "Que hace frío"], "correcta": "A",
     "explicacion": "La llegada de septiembre es la causa; esperar el próximo verano, la consecuencia."},
]
max_orden = EJ.objects.filter(texto_id=51).aggregate(m=Max("orden"))["m"] or 0
creados = 0
for i, n in enumerate(nuevas, start=1):
    tec = TL.objects.filter(numero=n["tec_num"], nivel_mcer="A1").first()
    if not tec:
        print(f"SKIP tec_num={n['tec_num']} no existe A1"); continue
    if EJ.objects.filter(texto_id=51, enunciado=n["enunciado"]).exists():
        print(f"SKIP duplicado: {n['enunciado'][:50]}"); continue
    ej = EJ.objects.create(texto_id=51, tecnica=tec, enunciado=n["enunciado"],
        tipo="multiple_choice",
        payload={"opciones": n["opciones"], "correcta": n["correcta"], "explicacion": n["explicacion"]},
        orden=max_orden + i)
    print(f"CREADO ej.id={ej.id}  tec=#{tec.numero}  orden={ej.orden}")
    creados += 1
print(f"OK {creados} nuevos")