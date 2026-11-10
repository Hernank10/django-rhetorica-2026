"""_seed_textos_b1.py - F1 B1: reescribe 3 textos fuera rango + crea 3 nuevos.

Rango B1: 180-350 palabras.
  - id=2  El reciclaje de vidrio en España (119w -> ~200w) [ampliar]
  - id=22 La decisión de Marta (417w -> ~300w) [acortar]
  - id=23 El viaje de Santiago (508w -> ~300w) [acortar]
  + 3 nuevos: El poder de la empatía, Las bibliotecas del futuro, Mi abuela y la tecnología
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

MIN_W, MAX_W = 180, 350

def wc(text):
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

# Textos a reescribir (por id)
REESCRIBIR = {
    2: {
        "titulo": "El reciclaje de vidrio en España",
        "tipo": "informativo",
        "cuerpo": (
            "El reciclaje de vidrio es una práctica consolidada en España. Cada año, "
            "los ciudadanos depositan millones de envases en los contenedores verdes "
            "que se encuentran en las calles. Según datos de Ecovidrio, en 2023 se "
            "reciclaron más de 900.000 toneladas de vidrio, lo que supone un aumento "
            "del 5% respecto al año anterior. El proceso es relativamente sencillo. "
            "Primero, los ciudadanos separan los envases de vidrio en sus hogares y "
            "los llevan al contenedor correspondiente. Después, camiones especiales "
            "recogen el material y lo transportan a plantas de tratamiento. Allí, el "
            "vidrio se limpia, se tritura y se funde a altas temperaturas. El vidrio "
            "reciclado puede utilizarse para fabricar nuevos envases sin perder "
            "calidad. De hecho, el vidrio es uno de los materiales más reciclables: "
            "puede reciclarse infinitas veces sin degradarse. Además, reciclar vidrio "
            "ahorra energía y reduce las emisiones de CO2. Sin embargo, aún queda "
            "trabajo por hacer. Muchos envases todavía acaban en vertederos, y algunas "
            "regiones tienen tasas de reciclaje muy bajas. Los expertos coinciden en "
            "que la educación ambiental es clave para mejorar estas cifras."
        ),
    },
    22: {
        "titulo": "La decisión de Marta",
        "tipo": "narrativo",
        "cuerpo": (
            "Marta llevaba cinco años trabajando en la misma empresa cuando recibió "
            "una oferta inesperada. Una compañía rival le ofrecía un puesto con mejor "
            "salario y más responsabilidades. La decisión no era fácil. Por un lado, "
            "el nuevo trabajo representaba una oportunidad de crecimiento profesional. "
            "Por otro, implicaba dejar atrás a sus compañeros, con quienes había "
            "construido una relación sólida durante años. Durante varias noches, Marta "
            "dio vueltas a la decisión. Habló con su familia, con amigos, con antiguos "
            "mentores. Cada uno le daba una opinión distinta. Su madre le aconsejaba "
            "aceptar: «Es una oportunidad que no se presenta dos veces». Su mejor "
            "amiga, en cambio, le recordaba lo importante que era sentirse cómoda en "
            "el trabajo. Una semana antes de tener que responder, Marta se dio cuenta "
            "de algo: no estaba comparando dos trabajos, sino dos versiones de sí "
            "misma. Aceptar la oferta significaba elegir el riesgo; quedarse "
            "significaba elegir la estabilidad. Al final, Marta decidió aceptar. "
            "No porque el dinero fuera lo más importante, sino porque necesitaba "
            "descubrir de qué era capaz. Sabía que podía fallar, pero también sabía "
            "que no intentarlo sería peor. El primer día en el nuevo trabajo, Marta "
            "entendió que no estaba empezando de cero: llevaba consigo todo lo "
            "aprendido, todas las personas que la habían formado, todas las decisiones "
            "que la habían traído hasta allí. Y eso, pensó, era lo único que importaba."
        ),
    },
    23: {
        "titulo": "El viaje de Santiago",
        "tipo": "narrativo",
        "cuerpo": (
            "Cuando Santiago cumplió sesenta años, decidió hacer el Camino de Santiago. "
            "Sus hijos le regalaron una mochila, unos zapatos nuevos y un mapa. "
            "«No vas a llegar», le decían en broma. Pero él estaba decidido. La primera "
            "etapa fue la más dura. Le dolían las piernas y los pies, y el sol de julio "
            "era implacable. Al tercer día, Santiago pensó en abandonar. Se sentó en una "
            "piedra junto al camino y se quedó mirando al horizonte. Fue entonces cuando "
            "conoció a otros peregrinos: una pareja de alemanes que caminaba desde hacía "
            "dos semanas, una joven francesa que hacía el Camino por primera vez, un "
            "hombre mayor que lo hacía cada año. Hablaron durante horas, compartieron "
            "comida y bebida, y hablaron de sus vidas. Santiago comprendió que el Camino "
            "no era solo andar: era también escuchar y ser escuchado. Las etapas "
            "siguientes fueron más fáciles, no porque el cuerpo se acostumbrara, sino "
            "porque la mente estaba en otra parte. Cada mañana, Santiago se levantaba "
            "temprano, desayunaba en algún bar del pueblo, y caminaba. Pensaba en su "
            "mujer, que había fallecido dos años antes. Pensaba en sus hijos. Pensaba en "
            "las decisiones que había tomado a lo largo de su vida. En el camino, todas "
            "esas historias se mezclaban con el paisaje, con el silencio, con el sonido "
            "de los pájaros. Al llegar a Santiago de Compostela, después de treinta y "
            "tres días, Santiago se sentó frente a la catedral y lloró. No lloraba de "
            "tristeza, sino de gratitud. Había hecho el Camino. Había llegado. Y en el "
            "camino había encontrado algo que no sabía que estaba buscando: paz."
        ),
    },
}

# Textos nuevos
NUEVOS = [
    {
        "titulo": "El poder de la empatía",
        "tipo": "narrativo",
        "cuerpo": (
            "Cuando Clara entró en el hospital, no sabía qué esperar. Era su primer "
            "día como voluntaria y sentía mariposas en el estómago. La enfermera jefa "
            "la llevó a la sala de espera, donde había varios pacientes ancianos. "
            "«Tu trabajo es simple: hablar con ellos, escucharlos», le dijo. Clara se "
            "acercó a una mujer que estaba sentada sola junto a la ventana. La mujer "
            "se llamaba Rosa y tenía ochenta y dos años. Al principio no quería hablar, "
            "pero poco a poco fue abriéndose. Le contó que había sido maestra durante "
            "cuarenta años, que había tenido tres hijos, que su marido había muerto "
            "hacía cinco. Le habló de sus alumnos favoritos, de las excursiones que "
            "organizaba, de las cartas que todavía guardaba. Clara la escuchaba sin "
            "interrumpir. No intentaba dar consejos ni soluciones. Simplemente estaba "
            "allí, presente. Cuando llegó la hora de irse, Rosa la cogió de la mano. "
            "«Gracias», le dijo. «Hacía mucho tiempo que nadie me escuchaba así». Clara "
            "salió del hospital con una sensación extraña. No había hecho nada "
            "extraordinario, no había curado a nadie, no había salvado ninguna vida. "
            "Pero algo había cambiado. Entendió que la empatía no consiste en resolver "
            "los problemas de los demás, sino en acompañarlos. A veces, el mayor regalo "
            "que podemos hacer a alguien es simplemente estar dispuestos a escuchar."
        ),
    },
    {
        "titulo": "Las bibliotecas del futuro",
        "tipo": "informativo",
        "cuerpo": (
            "Las bibliotecas están cambiando. Ya no son solo lugares donde se guardan "
            "libros: se han convertido en espacios multifuncionales donde se aprende, "
            "se trabaja, se investiga y se comparte. Muchas bibliotecas modernas "
            "ofrecen acceso a internet, salas de estudio, talleres de formación, "
            "espacios para niños y zonas de coworking. En los últimos años, el número "
            "de usuarios ha crecido, no a pesar de internet, sino gracias a internet. "
            "Según datos de la Federación de Gremios de Editores, las bibliotecas "
            "españolas recibieron más de 200 millones de visitas en 2023, la cifra más "
            "alta de la última década. ¿A qué se debe este aumento? Los expertos "
            "señalan varias razones. Primero, las bibliotecas han sabido adaptarse: "
            "ofrecen servicios digitales, préstamo de libros electrónicos, acceso a "
            "bases de datos académicas. Segundo, la sociedad valora cada vez más los "
            "espacios públicos gratuitos, donde cualquiera puede entrar sin gastar "
            "dinero. Tercero, muchas personas buscan lugares tranquilos para trabajar "
            "o estudiar fuera de casa. Sin embargo, no todos están de acuerdo. Algunos "
            "críticos sostienen que las bibliotecas están perdiendo su esencia: «Una "
            "biblioteca no es una cafetería», dicen. Pero otros responden que la "
            "esencia de una biblioteca no son los libros, sino el conocimiento. Y el "
            "conocimiento, hoy, adopta muchas formas. Lo importante es que las "
            "bibliotecas sigan siendo espacios abiertos, gratuitos y accesibles para "
            "todos, independientemente de su edad o condición social."
        ),
    },
    {
        "titulo": "Mi abuela y la tecnología",
        "tipo": "narrativo",
        "cuerpo": (
            "Mi abuela tiene noventa años. Toda la vida ha vivido en un pueblo pequeño "
            "y hasta hace poco no había utilizado nunca un teléfono móvil. Cuando mi "
            "hermano le regaló un smartphone por su cumpleaños, todos pensamos que sería "
            "un desastre. Nos equivocamos. Al principio, la abuela miraba el teléfono "
            "con desconfianza. «Esto es demasiado para mí», decía. Pero mi madre se "
            "sentó con ella una tarde y le enseñó lo básico: cómo desbloquear la "
            "pantalla, cómo hacer una llamada, cómo enviar un mensaje. La abuela "
            "aprendió rápido. En pocos días ya estaba mandando audios a sus hermanas, "
            "que viven en otras ciudades. Aprendió a buscar recetas de cocina en "
            "internet, a ver vídeos de sus nietos, a leer noticias del pueblo. Un día "
            "me llamó por videollamada. Me sorprendió verla con el teléfono en la mano "
            "y una sonrisa enorme. «Mira, mira lo que he aprendido», me dijo, mientras "
            "me enseñaba una foto de su huerto. A partir de ahí, empezó a mandarme "
            "fotos de sus plantas, mensajes de buenos días, emojis de corazones. Un "
            "domingo, le pregunté si le gustaba tener el teléfono. Se quedó pensativa "
            "un momento. «Al principio pensaba que era una tontería», respondió. «Pero "
            "ahora veo a mis nietos todos los días, aunque estén lejos. Y eso, para mí, "
            "no tiene precio». Escuchándola, me di cuenta de que la tecnología, cuando "
            "se enseña con paciencia y cariño, puede acercar mundos que parecían "
            "distantes. Y a veces, incluso, puede hacer que dos generaciones se "
            "entiendan un poco mejor."
        ),
    },
]

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", f"F1 {MIN_W}-{MAX_W} - PLAN")

operaciones = []  # (accion, id, data, words)

# Verificar reescribir
for tx_id, data in REESCRIBIR.items():
    tx = TX.objects.filter(id=tx_id).first()
    if not tx:
        print(f"  [SKIP] id={tx_id} no existe (sera CREATE con nuevo titulo)")
        continue
    w = wc(data["cuerpo"])
    ok = MIN_W <= w <= MAX_W
    operaciones.append(("UPDATE", tx_id, data, w))
    print(f"  [{'OK ' if ok else 'FUERA'}] UPDATE id={tx_id:>3}  {data['titulo'][:40]:<40}  {w:>4}w")

# Verificar nuevos
for data in NUEVOS:
    w = wc(data["cuerpo"])
    ok = MIN_W <= w <= MAX_W
    existente = TX.objects.filter(titulo=data["titulo"], nivel_mcer="B1").first()
    if existente:
        operaciones.append(("UPDATE", existente.id, data, w))
        print(f"  [{'OK ' if ok else 'FUERA'}] UPDATE id={existente.id:>3}  {data['titulo'][:40]:<40}  {w:>4}w")
    else:
        operaciones.append(("CREATE", None, data, w))
        print(f"  [{'OK ' if ok else 'FUERA'}] CREATE       {data['titulo'][:40]:<40}  {w:>4}w")

print(f"\n  Total operaciones: {len(operaciones)}")

header("B", "APLICAR" if args.apply else "DRY-RUN")

if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print("  Ejecuta con --apply para escribir.")
    sys.exit(0)

with transaction.atomic():
    for accion, tx_id, data, w in operaciones:
        if accion == "UPDATE":
            TX.objects.filter(id=tx_id).update(
                titulo=data["titulo"], cuerpo=data["cuerpo"], tipo=data["tipo"],
            )
        else:
            TX.objects.create(
                titulo=data["titulo"], cuerpo=data["cuerpo"], tipo=data["tipo"],
                nivel_mcer="B1", fuente="seed_fase1_b1",
            )
    print(f"  [OK] {len(operaciones)} operaciones aplicadas")

# Verificar
header("C", "VERIFICAR")
textos = list(TX.objects.filter(nivel_mcer="B1").order_by("id"))
en_rango = 0
for t in textos:
    w = wc(t.cuerpo)
    ok = MIN_W <= w <= MAX_W
    en_rango += int(ok)
    print(f"  [{'OK ' if ok else 'FUERA'}] id={t.id:>3}  {w:>4}w  {t.titulo[:50]}")

print(f"\n  En rango {MIN_W}-{MAX_W}: {en_rango}/{len(textos)}")
if en_rango == len(textos) and len(textos) >= 10:
    print(f"\n  [OK] FASE 1 B1 COMPLETA")