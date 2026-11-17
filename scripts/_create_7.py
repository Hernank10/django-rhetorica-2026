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
    # P1
    {"tec_num": 2, "enunciado": "¿Cuál es el tema principal de 'La biblioteca secreta'?",
     "opciones": ["El amor por los libros y la magia de las bibliotecas", "Una aventura en el mar", "Una fiesta de cumpleaños", "Un viaje al extranjero"],
     "correcta": "A", "explicacion": "El texto gira en torno a la biblioteca secreta y los libros."},
    {"tec_num": 5, "enunciado": "¿Cuándo descubre Lucía la biblioteca secreta?",
     "opciones": ["Un martes por la tarde", "Un domingo por la mañana", "En Navidad", "En verano"],
     "correcta": "A", "explicacion": "El texto empieza: 'Aquel martes por la tarde...'."},
    {"tec_num": 4, "enunciado": "¿Dónde está la biblioteca secreta?",
     "opciones": ["Entre la panadería y la ferretería", "En la plaza mayor", "En el parque", "En la escuela"],
     "correcta": "A", "explicacion": "El texto dice: 'entre la panadería y la ferretería'."},
    {"tec_num": 6, "enunciado": "¿Cómo se siente Lucía al encontrar la biblioteca cerrada?",
     "opciones": ["Decepcionada y triste", "Contentísima", "Indiferente", "Enfadada"],
     "correcta": "A", "explicacion": "Lucía 'sintió que el corazón le daba un vuelco' al ver la biblioteca cerrada."},
    # P2
    {"tec_num": 7, "enunciado": "¿Quién es Rosa?",
     "opciones": ["La dueña de la biblioteca secreta", "La madre de Lucía", "Una clienta de la panadería", "La bibliotecaria del barrio"],
     "correcta": "A", "explicacion": "Rosa es la mujer mayor que atiende la biblioteca secreta."},
    {"tec_num": 8, "enunciado": "¿Qué objeto tiene la puerta de la biblioteca?",
     "opciones": ["Un letrero dorado", "Una cortina roja", "Un candado", "Una campana"],
     "correcta": "A", "explicacion": "El texto dice: 'Tenía un letrero dorado que decía: Biblioteca de libros olvidados'."},
    {"tec_num": 9, "enunciado": "¿Cómo es el interior de la biblioteca?",
     "opciones": ["Con estanterías hasta el techo y olor a papel viejo", "Con mesas modernas y luces de colores", "Vacía y oscura", "Con ordenadores y pantallas"],
     "correcta": "A", "explicacion": "El texto dice: 'Las estanterías subían hasta el techo... el aire olía a papel viejo'."},
    # P3
    {"tec_num": 10, "enunciado": "¿Qué regla tiene la biblioteca de Rosa?",
     "opciones": ["Los libros no se prestan, se regalan", "Los libros se venden", "Los libros no se pueden tocar", "Los libros solo se leen allí"],
     "correcta": "A", "explicacion": "Rosa dice: 'Los libros no se prestan. Se regalan. Pero solo a quien los merece'."},
    {"tec_num": 11, "enunciado": "¿De quién era la biblioteca antes de Rosa?",
     "opciones": ["De su padre, un librero", "De su abuelo", "De un amigo", "Del ayuntamiento"],
     "correcta": "A", "explicacion": "Rosa le contó que la biblioteca había sido de su padre, un librero."},
    {"tec_num": 12, "enunciado": "¿Qué creía el padre de Rosa sobre los libros?",
     "opciones": ["Que debían circular libremente", "Que debían guardarse para siempre", "Que debían venderse caros", "Que debían quemarse"],
     "correcta": "A", "explicacion": "El texto dice: 'un librero que creía que los libros debían circular libremente'."},
    # P4
    {"tec_num": 13, "enunciado": "¿Qué le regala Rosa a Lucía al final?",
     "opciones": ["Un libro pequeño de tapas azules", "Una pluma", "Un cuaderno", "Un marcapáginas"],
     "correcta": "A", "explicacion": "El texto dice: 'Rosa le dio un libro pequeño, de tapas azules'."},
    {"tec_num": 14, "enunciado": "¿Qué hace Lucía al llegar a casa?",
     "opciones": ["Leer hasta que se le cierran los ojos", "Dormir inmediatamente", "Contarle todo a su madre", "Ver la televisión"],
     "correcta": "A", "explicacion": "El texto dice: 'Esa noche, leyó hasta que se le cerraron los ojos'."},
    {"tec_num": 15, "enunciado": "¿Qué pasa al día siguiente?",
     "opciones": ["Lucía vuelve a la biblioteca y Rosa la espera con otro libro", "Lucía no vuelve", "Rosa cierra la biblioteca", "Lucía se olvida del libro"],
     "correcta": "A", "explicacion": "El texto dice: 'Al día siguiente volvió a la biblioteca secreta. Rosa la esperaba con otro libro y una sonrisa'."},
]
max_orden = EJ.objects.filter(texto_id=7).aggregate(m=Max("orden"))["m"] or 0
creados = 0
for i, n in enumerate(nuevas, start=1):
    tec = TL.objects.filter(numero=n["tec_num"], nivel_mcer="B1").first()
    if not tec:
        print(f"SKIP tec_num={n['tec_num']} no existe B1"); continue
    if EJ.objects.filter(texto_id=7, enunciado=n["enunciado"]).exists():
        print(f"SKIP duplicado: {n['enunciado'][:50]}"); continue
    ej = EJ.objects.create(texto_id=7, tecnica=tec, enunciado=n["enunciado"],
        tipo="multiple_choice",
        payload={"opciones": n["opciones"], "correcta": n["correcta"], "explicacion": n["explicacion"]},
        orden=max_orden + i)
    print(f"CREADO ej.id={ej.id}  tec=#{tec.numero}  orden={ej.orden}")
    creados += 1
print(f"OK {creados} nuevos")