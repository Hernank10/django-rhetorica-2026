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
    {"tec_num": 27, "enunciado": "¿Cuántos párrafos tiene el texto 'Mi escuela'?",
     "opciones": ["Cuatro", "Uno", "Dos"], "correcta": "A",
     "explicacion": "El texto tiene cuatro párrafos separados por puntos y aparte."},
    {"tec_num": 14, "enunciado": "En 'El viernes hay cine porque es el último día de clase', ¿qué es la causa?",
     "opciones": ["Que es el último día de clase", "Que hay cine", "Que es viernes"], "correcta": "A",
     "explicacion": "La causa es que es el último día de clase; la consecuencia, que hay cine."},
    {"tec_num": 56, "enunciado": "Cuando el narrador dice 'me gusta mucho mi escuela', ¿qué expresa?",
     "opciones": ["Una preferencia verdadera", "Una mentira", "Una duda"], "correcta": "A",
     "explicacion": "El narrador expresa una preferencia personal coherente con todo el texto."},
    {"tec_num": 73, "enunciado": "En 'el profesor es muy divertido', ¿qué recurso se usa?",
     "opciones": ["Una descripción", "Una negación", "Una pregunta"], "correcta": "A",
     "explicacion": "'Muy divertido' es una descripción del profesor."},
    {"tec_num": 80, "enunciado": "En 'En el recreo jugamos al fútbol', ¿qué es la consecuencia?",
     "opciones": ["Que jugamos al fútbol", "Que es el recreo", "Que hay patio"], "correcta": "A",
     "explicacion": "La consecuencia del recreo es que jugamos al fútbol."},
    {"tec_num": 13, "enunciado": "En el texto, ¿quién toca la guitarra?",
     "opciones": ["El profesor de música", "El narrador", "Los compañeros"], "correcta": "A",
     "explicacion": "El texto dice: 'el profesor... toca la guitarra'."},
    {"tec_num": 95, "enunciado": "¿El texto 'Mi escuela' es coherente?",
     "opciones": ["Sí: describe la escuela de forma ordenada", "No: mezcla temas sin sentido", "No se puede saber"], "correcta": "A",
     "explicacion": "El texto sigue un orden claro: edificio, patio, clases y cierre."},
    {"tec_num": 100, "enunciado": "¿Qué valoración global se puede hacer del texto?",
     "opciones": ["Es un texto claro y descriptivo", "Es un texto confuso", "Es un texto sin sentido"], "correcta": "A",
     "explicacion": "El texto describe con claridad la escuela y sus actividades."},
    {"tec_num": 4, "enunciado": "¿En qué lugar está la biblioteca?",
     "opciones": ["En la planta baja", "En el patio", "En la cafetería"], "correcta": "A",
     "explicacion": "El texto dice: 'En la planta baja están la biblioteca y la cafetería'."},
    {"tec_num": 5, "enunciado": "¿A qué hora entra el narrador a la escuela?",
     "opciones": ["A las nueve de la mañana", "A las ocho", "A las diez"], "correcta": "A",
     "explicacion": "El texto dice: 'entro a las nueve de la mañana'."},
]
max_orden = EJ.objects.filter(texto_id=14).aggregate(m=Max("orden"))["m"] or 0
creados = 0
for i, n in enumerate(nuevas, start=1):
    tec = TL.objects.filter(numero=n["tec_num"], nivel_mcer="A1").first()
    if not tec:
        print(f"SKIP tec_num={n['tec_num']} no existe A1"); continue
    if EJ.objects.filter(texto_id=14, enunciado=n["enunciado"]).exists():
        print(f"SKIP duplicado: {n['enunciado'][:50]}"); continue
    ej = EJ.objects.create(texto_id=14, tecnica=tec, enunciado=n["enunciado"],
        tipo="multiple_choice",
        payload={"opciones": n["opciones"], "correcta": n["correcta"], "explicacion": n["explicacion"]},
        orden=max_orden + i)
    print(f"CREADO ej.id={ej.id}  tec=#{tec.numero}  orden={ej.orden}")
    creados += 1
print(f"OK {creados} nuevos")