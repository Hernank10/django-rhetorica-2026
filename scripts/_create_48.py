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
    {"tec_num": 14,  # Distinguir causa y consecuencia
     "enunciado": "En 'Lucía se ríe porque Toby corre detrás de las olas', ¿qué es la causa?",
     "opciones": ["Que Toby corre detrás de las olas", "Que Lucía se ríe", "Que hay playa"], "correcta": "A",
     "explicacion": "La causa es que Toby corre; la consecuencia, que Lucía se ríe."},
    {"tec_num": 27,  # Signos de puntuación / párrafos
     "enunciado": "¿Cuántos párrafos tiene el texto 'Mi familia'?",
     "opciones": ["Cuatro", "Uno", "Dos"], "correcta": "A",
     "explicacion": "El texto tiene cuatro párrafos separados por puntos y aparte."},
    {"tec_num": 56,  # Mentira / verdad
     "enunciado": "Cuando Carlos dice 'me gusta mucho mi familia', ¿qué expresa?",
     "opciones": ["Una preferencia verdadera", "Una mentira", "Una duda"], "correcta": "A",
     "explicacion": "Carlos expresa una preferencia personal coherente con todo el texto."},
    {"tec_num": 73,  # Comparación
     "enunciado": "En 'Toby es el más juguetón de la casa', ¿qué recurso se usa?",
     "opciones": ["Una comparación", "Una negación", "Una pregunta"], "correcta": "A",
     "explicacion": "'El más juguetón' compara a Toby con los demás."},
    {"tec_num": 80,  # Causa / consecuencia
     "enunciado": "En 'Por la tarde volvemos a casa cansados pero contentos', ¿qué es la consecuencia?",
     "opciones": ["Volver cansados pero contentos", "Que es por la tarde", "Que comen juntos"], "correcta": "A",
     "explicacion": "La consecuencia de la comida familiar es volver cansados pero contentos."},
    {"tec_num": 13,  # Personaje que habla en un diálogo
     "enunciado": "En el texto, ¿quién cuenta las historias de cuando era joven?",
     "opciones": ["El abuelo", "El padre", "Toby"], "correcta": "A",
     "explicacion": "El texto dice: 'mi abuelo cuenta historias de cuando era joven'."},
]
max_orden = EJ.objects.filter(texto_id=48).aggregate(m=Max("orden"))["m"] or 0
creados = 0
for i, n in enumerate(nuevas, start=1):
    tec = TL.objects.filter(numero=n["tec_num"], nivel_mcer="A1").first()
    if not tec:
        print(f"SKIP tec_num={n['tec_num']} no existe A1"); continue
    if EJ.objects.filter(texto_id=48, enunciado=n["enunciado"]).exists():
        print(f"SKIP duplicado: {n['enunciado'][:50]}"); continue
    ej = EJ.objects.create(texto_id=48, tecnica=tec, enunciado=n["enunciado"],
        tipo="multiple_choice",
        payload={"opciones": n["opciones"], "correcta": n["correcta"], "explicacion": n["explicacion"]},
        orden=max_orden + i)
    print(f"CREADO ej.id={ej.id}  tec=#{tec.numero}  orden={ej.orden}")
    creados += 1
print(f"OK {creados} nuevos")