"""_fix_12_ejercicios_faltantes.py - Añade el 2do ejercicio a las 12 técnicas
que quedaron con 1 solo tras Fase 3 (error de rangos en _seed_placeholders).

Cada ejercicio toma el texto_id del ejercicio existente de la misma técnica.
Idempotente: si la técnica ya tiene 2+ ejercicios, no hace nada.
"""
import os, sys, argparse
from pathlib import Path
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps
from django.db import transaction

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")

# Los 12 ejercicios nuevos. Cada uno usa la técnica indicada por número.
EJS = [
    # #2 [P3] Identificar el tema de un texto breve
    {"tec": 2, "enun": "¿Cuál es el tema principal de 'El perro perdido'?",
     "ops": ["La búsqueda y el reencuentro de un perro",
             "Una receta de cocina",
             "Un viaje al extranjero"],
     "corr": "A", "expl": "El texto cuenta cómo Lucía busca a Toby y lo encuentra cerca de la fuente."},

    # #3 [P4] Distinguir un cuento de una noticia
    {"tec": 3, "enun": "¿'El perro perdido' es un cuento o una noticia?",
     "ops": ["Un cuento, porque narra una historia con personajes",
             "Una noticia, porque informa de un hecho real",
             "Una receta, porque da instrucciones"],
     "corr": "A", "expl": "Narra una historia con personajes (Lucía, Toby, el vecino): es un cuento."},

    # #4 [P1] Localizar el lugar donde ocurre un hecho
    {"tec": 4, "enun": "En 'El perro perdido', ¿dónde llevó Lucía a Toby?",
     "ops": ["Al parque del barrio", "A la escuela", "A casa de un vecino"],
     "corr": "A", "expl": "El texto dice 'Lucía llevó a su perro Toby al parque del barrio'."},

    # #5 [P1] Localizar el tiempo (cuando ocurre un hecho)
    {"tec": 5, "enun": "En 'La fiesta de cumpleaños', ¿cuándo fue la fiesta?",
     "ops": ["El sábado pasado", "El domingo pasado", "El lunes pasado"],
     "corr": "A", "expl": "El texto dice 'El sábado pasado fue el cumpleaños de mi amiga Elena'."},

    # #6 [P2] Inferir si un personaje está contento o triste
    {"tec": 6, "enun": "En 'La fiesta de cumpleaños', ¿cómo se siente Elena?",
     "ops": ["Triste", "Contento", "Enfadada"],
     "corr": "B", "expl": "El texto dice 'Todos lo pasamos muy bien' y Elena abre sus regalos: está contenta."},

    # #7 [P3] Reconocer si un texto es un cuento o una noticia
    {"tec": 7, "enun": "¿'Mi escuela' es un cuento, una noticia o una descripción?",
     "ops": ["Un cuento", "Una noticia", "Una descripción"],
     "corr": "C", "expl": "'Mi escuela' describe un lugar sin narrar una historia ni informar de un hecho: es descriptivo."},

    # #9 [P2] Inferir si una situación es real o imaginaria
    {"tec": 9, "enun": "¿La historia de 'El perro perdido' es real o imaginaria?",
     "ops": ["Real, porque cuenta hechos cotidianos",
             "Imaginaria, porque hay dragones",
             "No se puede saber"],
     "corr": "A", "expl": "Cuenta hechos cotidianos (un perro, un parque, un vecino): es realista."},

    # #10 [P3] Reconocer el orden de los hechos en una narración
    {"tec": 10, "enun": "¿Cuál es el orden correcto de 'El perro perdido'?",
     "ops": ["Lucía va al parque → Toby se pierde → Lucía lo busca → Lo encuentran",
             "Toby se pierde → Lucía va al parque → Lo encuentran",
             "Lo encuentran → Lucía va al parque → Toby se pierde"],
     "corr": "A", "expl": "El texto sigue ese orden cronológico."},

    # #11 [P1] Localizar palabras que indican cantidad (mucho, poco)
    {"tec": 11, "enun": "En 'Los animales de la granja', ¿qué palabra indica cantidad?",
     "ops": ["'muchos' en 'hay muchos animales'", "'granja'", "'gallo'"],
     "corr": "A", "expl": "'Muchos' indica cantidad: un número elevado de animales."},

    # #12 [P2] Inferir si una acción es buena o mala
    {"tec": 12, "enun": "Al final de 'El perro perdido', ¿es buena o mala la decisión de Lucía?",
     "ops": ["Buena, porque decide no volver a soltar a Toby",
             "Mala, porque abandona a Toby",
             "No se puede saber"],
     "corr": "A", "expl": "Lucía abraza a Toby y decide no volver a soltarlo: protege a su perro."},

    # #13 [P3] Reconocer el personaje que habla en un diálogo
    {"tec": 13, "enun": "En 'En la cafetería', ¿quién dice 'Son tres euros con cincuenta'?",
     "ops": ["La clienta", "Marta (la camarera)", "El narrador"],
     "corr": "B", "expl": "Marta es la camarera y da el precio al cliente."},

    # #14 [P4] Distinguir causa y consecuencia en una oración
    {"tec": 14, "enun": "En 'Toby se alejó persiguiendo una paloma', ¿cuál es la causa?",
     "ops": ["Que Toby persigue una paloma",
             "Que Lucía lo busca",
             "Que el parque es grande"],
     "corr": "A", "expl": "La causa de alejarse es perseguir la paloma."},
]

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", "ESTADO ACTUAL")
contador = Counter(EJ.objects.filter(tecnica__nivel_mcer="A1").values_list("tecnica_id", flat=True))
tecnicas_1ej = []
for t in TL.objects.filter(nivel_mcer="A1").order_by("numero"):
    n = contador.get(t.id, 0)
    if n == 1:
        tecnicas_1ej.append(t)

print(f"  Técnicas A1 con 1 ejercicio: {len(tecnicas_1ej)}")
print(f"  Técnicas A1 con 2 ejercicios: {sum(1 for n in contador.values() if n >= 2)}")

header("B", "PLAN DE LOS 12 EJERCICIOS")
faltan = []
for data in EJS:
    tec = TL.objects.filter(nivel_mcer="A1", numero=data["tec"]).first()
    if not tec:
        print(f"  [MISS] Técnica #{data['tec']} no existe")
        continue
    n = contador.get(tec.id, 0)
    if n >= 2:
        print(f"  [SKIP] #{tec.numero} ya tiene {n} ejercicios")
        continue
    faltan.append((tec, data))
    print(f"  #{tec.numero:>3} [{tec.proceso}]  {tec.titulo[:45]:<45}  {data['enun'][:50]}")

print(f"\n  A crear: {len(faltan)}")

header("C", "APLICAR" if args.apply else "DRY-RUN")
if not args.apply:
    print("  DRY-RUN. Nada modificado. --apply para crear los ejercicios.")
    sys.exit(0)

with transaction.atomic():
    creados = 0
    for tec, data in faltan:
        # Tomar texto del ejercicio existente (Fase 2 asignó uno)
        ej_exist = EJ.objects.filter(tecnica=tec).first()
        if not ej_exist:
            print(f"  [SKIP] #{tec.numero}: sin ejercicio base")
            continue
        max_orden = EJ.objects.filter(tecnica=tec).order_by("-orden").values_list("orden", flat=True).first() or 0

        EJ.objects.create(
            tecnica=tec,
            texto_id=ej_exist.texto_id,
            enunciado=data["enun"],
            tipo="multiple_choice",
            payload={
                "opciones": [f"{chr(65+i)}) {op}" for i, op in enumerate(data["ops"])],
                "correcta": data["corr"],
                "explicacion": data["expl"],
            },
            orden=max_orden + 1,
        )
        creados += 1
    print(f"\n  [OK] {creados} ejercicios creados")

header("D", "VERIFICAR")
contador2 = Counter(EJ.objects.filter(tecnica__nivel_mcer="A1").values_list("tecnica_id", flat=True))
tecnicas_1ej_2 = [t for t in TL.objects.filter(nivel_mcer="A1") if contador2.get(t.id, 0) == 1]
print(f"  Técnicas A1 con 1 ejercicio: {len(tecnicas_1ej_2)}")
print(f"  Técnicas A1 con 2+ ejercicios: {sum(1 for n in contador2.values() if n >= 2)}")
total = sum(contador2.values())
print(f"  Total ejercicios A1: {total}")
if len(tecnicas_1ej_2) == 0:
    print("\n  [OK] FASE 3 COMPLETA — todas las técnicas con 2 ejercicios")
else:
    print(f"\n  [WARN] {len(tecnicas_1ej_2)} técnicas aún con 1 ejercicio")