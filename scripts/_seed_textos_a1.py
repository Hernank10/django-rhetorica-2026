"""_seed_textos_a1.py - Fase 1: siembra 10 textos A1 (6 nuevos + 4 reescritos).

Idempotente: update_or_create por (titulo, nivel_mcer='A1').

Uso:
    python scripts/_seed_textos_a1.py            # DRY-RUN
    python scripts/_seed_textos_a1.py --apply    # Aplicar
"""
import os, sys, re, argparse
from pathlib import Path

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

TX = apps.get_model("core", "Texto")

def wc(text):
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

TEXTOS = [
    # ═══ 6 NUEVOS ═══
    {
        "titulo": "Un día en la vida de Ana",
        "tipo": "narrativo",
        "cuerpo": (
            "Ana se despierta a las siete de la mañana. Desayuna pan con tomate "
            "y un vaso de leche. A las ocho sale de casa y camina hasta la escuela. "
            "Allí trabaja como profesora de música. Le encanta su trabajo porque "
            "los niños son divertidos. A las dos come en casa con su familia. "
            "Por la tarde lee un libro en el sofá. A veces, cuando hace sol, va "
            "al parque. Por la noche cena con sus amigos. Es feliz con su vida "
            "tranquila."
        ),
    },
    {
        "titulo": "Mi familia",
        "tipo": "descriptivo",
        "cuerpo": (
            "Me llamo Carlos y tengo veinticinco años. Vivo en Madrid con mi "
            "familia. Mi padre se llama Juan y es médico. Mi madre se llama María "
            "y trabaja en una tienda. Tengo una hermana pequeña, Lucía. Ella tiene "
            "ocho años y va a la escuela. También tengo un perro que se llama Toby. "
            "Los domingos comemos todos juntos en casa de mis abuelos. Me gusta "
            "mucho mi familia."
        ),
    },
    {
        "titulo": "La casa de Pablo",
        "tipo": "descriptivo",
        "cuerpo": (
            "Pablo vive en una casa pequeña cerca del mar. La casa tiene dos "
            "dormitorios, un baño y una cocina. En el salón hay un sofá azul, una "
            "mesa y una televisión. La cocina es blanca y tiene una ventana grande. "
            "Desde la ventana se ve el mar. En el jardín hay muchas flores y un "
            "árbol viejo. A Pablo le gusta su casa porque es tranquila y siempre "
            "hay sol. Los fines de semana invita a sus amigos a comer en el jardín."
        ),
    },
    {
        "titulo": "Cómo hacer una tortilla",
        "tipo": "instructivo",
        "cuerpo": (
            "Para hacer una tortilla de patatas necesitas cuatro huevos, dos "
            "patatas, aceite y sal. Primero, pela las patatas y córtalas en trozos "
            "pequeños. Después, fríelas en aceite durante diez minutos. Mientras "
            "se fríen, bate los huevos en un bol. Luego, mezcla las patatas con "
            "los huevos. Finalmente, pon la mezcla en la sartén y cocina la "
            "tortilla cinco minutos por cada lado. La tortilla está lista cuando "
            "es dorada por fuera y jugosa por dentro."
        ),
    },
    {
        "titulo": "Me gusta el verano",
        "tipo": "opinion",
        "cuerpo": (
            "Me gusta mucho el verano. En verano no hay clases y puedo dormir "
            "hasta tarde. Mi familia y yo vamos a la playa en julio. Nadamos en "
            "el mar y comemos helado. También me gusta leer libros en la arena. "
            "No me gusta el invierno porque hace mucho frío y llueve. En invierno "
            "solo quiero quedarme en casa con una manta. Por eso prefiero el "
            "verano: el sol, la playa y las vacaciones."
        ),
    },
    {
        "titulo": "En la cafetería",
        "tipo": "dialogo",
        "cuerpo": (
            "En la cafetería del barrio, Marta trabaja por las mañanas. Hoy hay "
            "mucha gente.\n"
            "—Buenos días, ¿qué desea?\n"
            "—Hola, buenos días. Un café con leche y un croissant, por favor.\n"
            "—Muy bien. ¿Algo más?\n"
            "—No, gracias. ¿Cuánto es?\n"
            "—Son tres euros con cincuenta.\n"
            "—Aquí tiene. ¿Puedo pagar con tarjeta?\n"
            "—Sí, por supuesto. Gracias a usted. ¡Que tenga un buen día!\n"
            "—Igualmente. ¡Hasta luego!\n"
            "El café está muy caliente y el croissant es dulce."
        ),
    },
    # ═══ 4 REESCRITOS ═══
    {
        "titulo": "El perro perdido",
        "tipo": "narrativo",
        "cuerpo": (
            "Ayer por la tarde, Lucía llevó a su perro Toby al parque del barrio. "
            "Mientras jugaban a la pelota, Toby se alejó persiguiendo una paloma. "
            "Lucía lo buscó durante una hora por los caminos, pero no lo encontró. "
            "Estaba muy preocupada. Al final, un vecino le dijo que había visto un "
            "perro pequeño cerca de la fuente. Allí estaba Toby, bebiendo agua. "
            "Lucía lo abrazó fuerte y volvieron a casa juntos. Nunca más lo dejó "
            "suelto."
        ),
    },
    {
        "titulo": "Mi escuela",
        "tipo": "descriptivo",
        "cuerpo": (
            "Mi escuela se llama San Martín y está en el centro de la ciudad. Es "
            "un edificio grande, de color amarillo. Tiene tres pisos y muchas "
            "aulas. En la planta baja hay una biblioteca y una cafetería. En el "
            "patio hay árboles y bancos para sentarse. Mi clase favorita es la "
            "de música, porque el profesor es muy divertido. Mis compañeros son "
            "simpáticos. En el recreo jugamos al fútbol en el patio. Me gusta "
            "mucho mi escuela."
        ),
    },
    {
        "titulo": "La fiesta de cumpleaños",
        "tipo": "narrativo",
        "cuerpo": (
            "El sábado pasado fue el cumpleaños de mi amiga Elena. Cumplió diez "
            "años. Su madre organizó una fiesta en el jardín de su casa. Había "
            "globos de colores y una tarta de chocolate muy grande. Vinieron "
            "muchos amigos. Jugamos a la cuerda y al escondite. Después, Elena "
            "abrió los regalos: libros, un vestido y una muñeca. Comimos tarta, "
            "helado y bebimos zumo de naranja. Todos lo pasamos muy bien. Fue "
            "una fiesta divertida."
        ),
    },
    {
        "titulo": "Los animales de la granja",
        "tipo": "descriptivo",
        "cuerpo": (
            "En la granja de mi abuelo hay muchos animales. Por la mañana, el "
            "gallo canta y despierta a todos. Las gallinas ponen huevos en el "
            "corral. Las vacas comen hierba en el prado y dan leche. Los cerdos "
            "duermen en el barro. Los caballos corren por el campo. También hay "
            "tres ovejas blancas y un perro que cuida la granja. Mi abuelo se "
            "levanta muy temprano para dar de comer a los animales. A mí me "
            "gusta visitarlo en verano."
        ),
    },
]

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", "PLAN DE SEED (10 textos A1)")
existentes_a1 = {t.titulo: t for t in TX.objects.filter(nivel_mcer="A1")}

crear = []
actualizar = []
for idx, data in enumerate(TEXTOS, 1):
    words = wc(data["cuerpo"])
    en_rango = 60 <= words <= 100
    existente = existentes_a1.get(data["titulo"])
    accion = "UPDATE" if existente else "CREATE"
    if accion == "CREATE": crear.append((idx, data, words))
    else: actualizar.append((idx, data, words))
    marca = "✓" if en_rango else "✗"
    print(f"  [{marca}] #{idx:>2}  {accion:<6}  {data['titulo'][:35]:<35}  {words:>3} palabras")

print(f"\n  A crear:      {len(crear)}")
print(f"  A actualizar: {len(actualizar)}")
print(f"  Total:        {len(TEXTOS)}")

header("B", "APLICAR" if args.apply else "DRY-RUN")
if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print("  Ejecuta con --apply para sembrar los 10 textos.")
    print("\n  ADVERTENCIA: los 4 textos reescritos cambian su cuerpo.")
    print("  Los ejercicios reales que apuntan a ellos pueden quedar")
    print("  descoherentes. Se re-mapean en Fase 3. El pilot no detecta")
    print("  esto (solo verifica HTTP 200, no coherencia).")
    sys.exit(0)

with transaction.atomic():
    creados = 0
    actualizados = 0
    for idx, data, words in crear + actualizar:
        obj, created = TX.objects.update_or_create(
            titulo=data["titulo"],
            nivel_mcer="A1",
            defaults={
                "cuerpo": data["cuerpo"],
                "tipo": data["tipo"],
                "fuente": "seed_fase1",
                "orden": idx,
            },
        )
        if created:
            creados += 1
        else:
            actualizados += 1
    print(f"\n  [OK] Creados: {creados}, Actualizados: {actualizados}")

header("C", "VERIFICAR")
textos_a1 = list(TX.objects.filter(nivel_mcer="A1").order_by("orden", "id"))
print(f"  Total textos A1: {len(textos_a1)}")
en_rango = 0
for t in textos_a1:
    words = wc(t.cuerpo)
    ok = 60 <= words <= 100
    en_rango += int(ok)
    print(f"  [{'✓' if ok else '✗'}] id={t.id:>3}  {t.titulo[:40]:<40}  {words:>3} palabras")
print(f"\n  En rango 60-100: {en_rango}/{len(textos_a1)}")

if en_rango == len(textos_a1):
    print("\n  [OK] FASE 1 COMPLETA — todos los textos en rango")
else:
    print(f"\n  [WARN] {len(textos_a1) - en_rango} textos fuera de rango")