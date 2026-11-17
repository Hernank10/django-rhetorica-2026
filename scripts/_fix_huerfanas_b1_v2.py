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

# Técnicas B1 que probablemente se han quedado huérfanas tras el cierre del 2
# Ajustar según la salida de _diag_tecnicas_b1_huerfanas.py
nuevas = [
    {"tec_num": 73,  # Reconocer la descripción en un cuento
     "enunciado": "En 'El pueblo seguía igual: las mismas casas bajas', ¿qué recurso se usa?",
     "opciones": ["Una descripción", "Una negación", "Una pregunta", "Una comparación"],
     "correcta": "A",
     "explicacion": "'Las mismas casas bajas' es una descripción del pueblo."},
    {"tec_num": 76,  # Reconocer la repetición como recurso
     "enunciado": "En 'Recordó los veranos de niño', ¿qué recurso narrativo aparece?",
     "opciones": ["Un recuerdo o flashback", "Una negación", "Una pregunta", "Una comparación"],
     "correcta": "A",
     "explicacion": "'Recordó los veranos de niño' es un flashback: un recuerdo del pasado."},
]
max_orden = EJ.objects.filter(texto_id=2).aggregate(m=Max("orden"))["m"] or 0
creados = 0
for i, n in enumerate(nuevas, start=1):
    tec = TL.objects.filter(numero=n["tec_num"], nivel_mcer="B1").first()
    if not tec:
        print(f"SKIP tec_num={n['tec_num']} no existe B1")
        continue
    if EJ.objects.filter(texto_id=2, enunciado=n["enunciado"]).exists():
        print(f"SKIP duplicado: {n['enunciado'][:50]}")
        continue
    ej = EJ.objects.create(
        texto_id=2, tecnica=tec, enunciado=n["enunciado"],
        tipo="multiple_choice",
        payload={"opciones": n["opciones"], "correcta": n["correcta"], "explicacion": n["explicacion"]},
        orden=max_orden + i,
    )
    print(f"CREADO ej.id={ej.id}  tec=#{tec.numero}  orden={ej.orden}")
    creados += 1
print(f"OK {creados} nuevos")