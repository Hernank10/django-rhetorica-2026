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
    {"tec_num": 22, "enunciado": "En 'Además, las palabras pueden transformar la realidad', ¿qué relación marca 'Además'?",
     "opciones": ["Adición", "Contraste", "Causa", "Consecuencia"], "correcta": "A",
     "explicacion": "'Además' es un conector de adición: suma información."},
    {"tec_num": 22, "enunciado": "En 'Finalmente, cuidemos lo que decimos', ¿qué relación marca 'Finalmente'?",
     "opciones": ["Cierre o conclusión", "Contraste", "Causa", "Adición"], "correcta": "A",
     "explicacion": "'Finalmente' marca el cierre del texto."},
    {"tec_num": 22, "enunciado": "En 'No obstante, la evidencia contradice esta idea', ¿qué relación marca 'No obstante'?",
     "opciones": ["Contraste", "Adición", "Causa", "Consecuencia"], "correcta": "A",
     "explicacion": "'No obstante' es un conector de contraste."},
    {"tec_num": 22, "enunciado": "En 'Por ejemplo, un elogio sincero puede alegrar el día', ¿qué función cumple 'Por ejemplo'?",
     "opciones": ["Introducir un ejemplo", "Contrastar", "Concluir", "Causar"], "correcta": "A",
     "explicacion": "'Por ejemplo' introduce una ejemplificación."},
    {"tec_num": 22, "enunciado": "En 'Primero, las palabras positivas generan bienestar', ¿qué función cumple 'Primero'?",
     "opciones": ["Marcar orden", "Contrastar", "Concluir", "Causar"], "correcta": "A",
     "explicacion": "'Primero' marca el orden de las ideas."},
    {"tec_num": 22, "enunciado": "En 'Según la doctora García, las palabras construyen o destruyen relaciones', ¿qué función cumple 'Según'?",
     "opciones": ["Introducir la fuente de una cita", "Contrastar", "Concluir", "Adicionar"], "correcta": "A",
     "explicacion": "'Según' introduce la fuente de la cita."},
    {"tec_num": 22, "enunciado": "En 'las palabras son como semillas: crecen en la mente', ¿qué relación hay entre 'semillas' y 'palabras'?",
     "opciones": ["Comparación o metáfora", "Contraste", "Causa", "Consecuencia"], "correcta": "A",
     "explicacion": "'Las palabras son como semillas' es una comparación."},
    {"tec_num": 22, "enunciado": "En 'Un insulto deja una huella duradera', ¿qué significa 'huella' en este contexto?",
     "opciones": ["Marca o efecto que perdura", "Pisada en el suelo", "Dibujo", "Herida física"], "correcta": "A",
     "explicacion": "'Huella' aquí es metafórica: marca o efecto duradero."},
]
max_orden = EJ.objects.filter(texto_id=21).aggregate(m=Max("orden"))["m"] or 0
creados = 0
for i, n in enumerate(nuevas, start=1):
    tec = TL.objects.filter(numero=n["tec_num"], nivel_mcer="B1").first()
    if not tec:
        print(f"SKIP tec_num={n['tec_num']} no existe B1"); continue
    if EJ.objects.filter(texto_id=21, enunciado=n["enunciado"]).exists():
        print(f"SKIP duplicado: {n['enunciado'][:50]}"); continue
    ej = EJ.objects.create(texto_id=21, tecnica=tec, enunciado=n["enunciado"],
        tipo="multiple_choice",
        payload={"opciones": n["opciones"], "correcta": n["correcta"], "explicacion": n["explicacion"]},
        orden=max_orden + i)
    print(f"CREADO ej.id={ej.id}  tec=#{tec.numero}  orden={ej.orden}")
    creados += 1
print(f"OK {creados} nuevos")