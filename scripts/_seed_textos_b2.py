"""_seed_textos_b2.py - F1 B2: recortar 3 textos largos + ampliar 1 + crear 3 nuevos.

Rango B2: 300-500 palabras.
  - id=6  IA educación (297w)  -> ampliar a ~305w
  - id=26 Regreso de Amina (515w) -> recortar a ~490w
  - id=27 Casa de los relojes (532w) -> recortar a ~495w
  - id=28 Móviles institutos (587w) -> recortar a ~490w
  + 3 nuevos: descriptivo (Cádiz), diálogo (conversación), opinión (lectura)
"""
import os, sys, re, argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
from django.db import transaction

TX = apps.get_model("core", "Texto")
MIN_W, MAX_W = 300, 500

def wc(text):
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

REESCRITURAS = {
    6: {
        "titulo": "La inteligencia artificial en la educación: promesas y riesgos",
        "tipo": "informativo",
        "cuerpo": """El uso de la inteligencia artificial (IA) en la educación ha crecido de forma exponencial en los últimos años. Según el informe de la OCDE de 2025, el 67% de los centros educativos de los países desarrollados utiliza alguna herramienta de IA, desde asistentes virtuales hasta sistemas de evaluación automática. En España, el 45% de los institutos ha incorporado alguna herramienta de este tipo en el último curso. Los defensores de la IA en la educación argumentan que permite personalizar el aprendizaje. Un asistente virtual, por ejemplo, puede adaptar los ejercicios al ritmo de cada estudiante y ofrecer retroalimentación inmediata. Además, los sistemas de evaluación automática liberan a los profesores de tareas repetitivas, permitiéndoles dedicar más tiempo a la enseñanza. Sin embargo, los críticos señalan varios riesgos. El primero es la desigualdad: no todos los centros tienen acceso a las mismas herramientas, lo que puede ampliar la brecha entre estudiantes. El segundo es la deshumanización: si la IA sustituye al profesor en la retroalimentación, se pierde el vínculo humano, que es esencial en la educación. El tercero es la privacidad: los sistemas de IA recopilan datos de los estudiantes, y no siempre queda claro cómo se usan. Un ejemplo de esta tensión se produjo en 2024, cuando un instituto de Barcelona decidió sustituir parte de las tutorías por un asistente de IA. La medida generó protestas de las familias, que consideraban que la educación requiere un acompañamiento humano que la tecnología no puede ofrecer. El instituto dio marcha atrás. El debate sigue abierto y probablemente seguirá estándolo durante años. La pregunta no es si la IA estará en la educación, sino cómo integrarla de forma que potencie el aprendizaje sin perder lo humano. Como señala un informe de la UNESCO (2023), la tecnología debe estar al servicio de las personas, no al revés, y esa es la clave del futuro educativo.""",
    },
    26: {
        "titulo": "El regreso de Amina",
        "tipo": "literario",
        "cuerpo": """Amina bajó del autobús al amanecer. El pueblo la recibió con el mismo olor a higuera y polvo que recordaba de su infancia. Habían pasado veinte años desde que se marchó a la ciudad para estudiar medicina. Ahora volvía, no como médico famosa, sino como una mujer que había perdido a su madre y regresaba a enterrarla.

La casa de la familia seguía allí, con su fachada blanca y sus contraventanas azules. En aquel pueblo, el azul significaba protección: las madres lo pintaban en las puertas para alejar los malos espíritus. Amina sonrió al recordarlo. Su madre había pintado aquellas ventanas cada primavera, sin fallar una sola vez.

Su abuela, que tenía noventa años y la memoria intacta, la esperaba en el umbral. "Has vuelto, hija", dijo, sin sorpresa. "La casa te estaba llamando". Amina la abrazó. La abuela era la memoria del pueblo: sabía quién había vivido en cada casa, quién había emigrado, quién había vuelto. Su función en la familia había sido siempre la de guardar las historias.

Durante el entierro, Amina observó el cementerio. La mitad de las tumbas estaban vacías: los jóvenes se habían ido y ya no volvían. El pueblo se moría lentamente. Los que quedaban eran ancianos que esperaban. Amina sintió una punzada: ella también había formado parte de ese éxodo.

Aquella tarde, mientras tomaban té en la cocina, la abuela le contó que el alcalde quería cerrar la escuela por falta de alumnos. "Dicen que es por el progreso", dijo la abuela con ironía, "pero el progreso que se lleva a los niños no es progreso, es desierto".

Amina pasó tres días en el pueblo. Recorrió los caminos de su infancia, habló con los vecinos, visitó la escuela abandonada. Al cuarto día, tomó una decisión: no volvería a la ciudad. Iría a la capital a pedir una subvención para reabrir la escuela y la consulta médica del pueblo. No sabía si lo conseguiría. Pero algo dentro de ella le decía que valía la pena intentarlo.

Cuando se lo contó a la abuela, esta sonrió con malicia. "Sabía que volverías. Las raíces tiran más que los aviones". Amina se rió. Su abuela tenía razón: la vida era como un árbol; por muchas ramas que eche, siempre tira de la raíz.

El periódico local publicó meses después un artículo sobre el proyecto de Amina. Incluía un gráfico que mostraba la evolución de la población: una línea roja que caía desde 1980. El gráfico omitía el ligero repunte de los últimos dos años, coincidiendo con la llegada de algunas familias jóvenes.

Cinco años después, la escuela tenía veinte alumnos. No era mucho, pero era un comienzo.""",
    },
    27: {
        "titulo": "La casa de los relojes",
        "tipo": "literario",
        "cuerpo": """La casa de don Elías era la única del barrio que tenía relojes en todas las habitaciones. No era una casa grande, pero había un reloj en el recibidor, otro en la cocina, otro en el pasillo, dos en el salón y hasta uno pequeño en el baño. Todos estaban parados. Todos marcaban la misma hora: las siete y diez.

Yo iba a visitarlo todos los jueves. Él era el abuelo de mi mejor amigo, y desde que su mujer murió, nadie lo visitaba. Mi amigo decía que don Elías se había vuelto loco; yo no estaba tan seguro. Había algo en su manera de mirar los relojes que me hacía pensar que sabía exactamente lo que hacía.

"Los paré todos el mismo día, a la misma hora", me explicó una tarde, mientras tomábamos café. "A las siete y diez de la mañana del 14 de abril de 1987. Ese día, mi mujer se fue de casa. No volvió. Desde entonces, para mí, el tiempo se detuvo".

Don Elías hablaba con una calma que desconcertaba. Su voz era suave, casi musical. "La gente cree que estoy loco", decía, "pero en realidad soy el único cuerdo de este barrio. Los demás viven esclavos del tiempo; yo lo he vencido".

Yo lo escuchaba sin decir nada. Pensaba que don Elías tenía razón en algo: la gente corría todo el día sin saber hacía dónde. Pero también pensaba que negar el tiempo era una forma de negar la vida. Mientras él hablaba, yo miraba los relojes y pensaba en mi propia vida, en las horas que perdía en el móvil, en los días que se me escapaban.

Una tarde, don Elías me contó la historia de su vida. Había sido relojero de joven, había tenido un taller en la calle Mayor, había arreglado relojes para medio barrio. Su mujer, Emilia, era la que le daba cuerda a los relojes cada mañana. Cuando ella se fue, don Elías dejó de darles cuerda. Y así, poco a poco, todos se fueron parando. Primero uno, luego otro. El último fue el del recibidor. "Ese era el favorito de Emilia", me dijo. "Por eso fue el último en pararse".

Una noche, mientras volvía a casa, me di cuenta de que yo también vivía rodeado de relojes parados. Mi vida era una sucesión de horas que no aprovechaba. Decidí, entonces, que cambiaría algo. No sabía qué, pero algo.

Al jueves siguiente, cuando llegué a casa de don Elías, encontré la puerta abierta. Él no estaba. Sobre la mesa del recibidor había una nota: "Me he ido a buscar a Emilia. Si vuelvo, dale cuerda al reloj del recibidor. Si no vuelvo, déjalo parado".

Nunca supe si don Elías volvió. A veces, cuando paso por su casa, miro por la ventana. Los relojes siguen allí, parados, marcando las siete y diez. Y yo, cada mañana, cuando me levanto, miro el reloj de mi cocina y me acuerdo de don Elías. El tiempo, pienso, es lo único que no se puede parar. Pero quizá se pueda vivir de otra manera.""",
    },
    28: {
        "titulo": "Móviles en los institutos: prohibir o educar",
        "tipo": "argumentativo",
        "cuerpo": """El debate sobre el uso del móvil en los institutos está de actualidad. Algunos defienden prohibirlo; otros, educar en su uso. En este texto analizamos los principales argumentos y algunas falacias que circulan en el debate.

Argumentos a favor de la prohibición

Quienes defienden la prohibición sostienen que los móviles distraen y bajan el rendimiento. Un estudio de la Universidad de Madrid (2023) encontró que los alumnos con móvil en clase obtenían peores notas. Sin embargo, hay que tener cuidado: el estudio se hizo solo en dos institutos de una misma ciudad, por lo que su muestra no es representativa del conjunto del país.

Algunos llevan el argumento más lejos: "Si permitimos el móvil, los alumnos se distraerán, luego no estudiarán, luego fracasarán, luego no encontrarán trabajo y acabarán en la marginación". Este argumento es una pendiente resbaladiza: afirma una cadena de consecuencias catastrofistas sin justificar cada paso.

Otros dicen: "Los profesores que defienden el móvil no entienden a los jóvenes". Esto es un argumento ad hominem: ataca a la persona en lugar de refutar su argumento.

Argumentos a favor de educar en el uso

Quienes defienden educar en el uso señalan que el móvil es una herramienta y que prohibirlo no enseña a usarlo bien. Algunos dicen: "Es como prohibir los cuchillos porque pueden cortar; mejor enseñar a usarlos con cuidado". Es un argumento por analogía: su solidez depende de que la comparación sea relevante.

Sin embargo, algunos críticos responden: "Quienes defienden educar quieren llenar las aulas de pantallas y eliminar la autoridad del profesor". Esto es un hombre de paja: distorsiona el argumento del oponente para refutarlo más fácilmente.

Datos y encuestas

Un dato que se repite: "El 80% de los padres quiere prohibir el móvil". Hay que analizar la fuente: si la encuesta se hizo solo entre padres de un colegio concreto, la muestra no es representativa. También se oye: "El 70% de los alumnos con móvil suspende, luego el móvil causa el suspenso". Aquí hay una falacia de falsa causa: hay otros factores que explican ambos hechos. La correlación no implica causalidad.

Conclusiones

La conclusión del debate no es fácil. Un argumento válido podría ser: "Todos los alumnos necesitan concentrarse para aprender. Los móviles distraen. Por tanto, en clase conviene limitar su uso". Pero hay que distinguir validez de verdad: un argumento puede ser válido aunque sus premisas sean falsas.

En mi opinión, ni la prohibición total ni la permisividad absoluta son buenas soluciones. Probablemente lo mejor sea una vía intermedia: educar en el uso responsable y regular el móvil en determinados momentos. Los institutos deberían elaborar normas consensuadas con alumnos y familias.

La calidad global del texto depende de su claridad, su coherencia, la solidez de sus argumentos y la presencia de contraargumentos.""",
    },
}

NUEVOS = [
    {
        "titulo": "Una ciudad que cambia",
        "tipo": "descriptivo",
        "cuerpo": """Cádiz siempre ha sido una ciudad de contrastes. En sus calles estrechas, los edificios de piedra caliza conviven con locales modernos de comida rápida. Los balcones de forja antigua se asoman sobre tiendas con pantallas LED. Es una ciudad que no ha decidido si quiere ser antigua o moderna, y por eso mismo tiene un encanto único.

El casco histórico conserva la estructura del siglo XVIII. Las casas son altas y estrechas, con patios interiores llenos de macetas. Las paredes blancas reflejan el sol del verano, y en verano el calor es tan intenso que las calles se vacían al mediodía. Los vecinos mayores se sientan en la puerta de sus casas al atardecer, cuando la brisa del mar llega. Los turistas, en cambio, llenan las plazas al anochecer, buscando el fresco y las fotos.

En los últimos años, la ciudad ha cambiado. Los pisos turísticos han desplazado a los vecinos del centro. Los alquileres han subido y muchos jóvenes se han ido a vivir a la periferia. Los comercios tradicionales cierran y abren tiendas de souvenirs. Pero también han aparecido nuevas iniciativas: bibliotecas de barrio, huertos urbanos, mercados de productores locales. Hay una resistencia silenciosa.

En el barrio de La Viña, los vecinos han organizado una asociación para proteger los patios de vecinos. En el barrio del Pópulo, un grupo de artesanos ha abierto un taller compartido en una casa antigua. En la playa de La Caleta, los pescadores venden el pescado del día a los restaurantes del barrio. Es una ciudad que sigue viva, aunque a veces parezca dormida.

Al atardecer, cuando el sol cae sobre el océano, Cádiz se vuelve dorada. Las olas rompen contra las rocas, y el viento trae olor a sal. En la plaza de San Juan de Dios, los niños juegan, los mayores conversan y los jóvenes miran el móvil. Esa mezcla de generaciones, de lo antiguo y lo nuevo, es lo que hace única a esta ciudad. Una ciudad que cambia, pero que no pierde su esencia.""",
    },
    {
        "titulo": "Una conversación difícil",
        "tipo": "dialogo",
        "cuerpo": """—Papá, tenemos que hablar.
—¿Qué pasa, Lucía? ¿Estás bien?
—Sí, estoy bien. Es sobre el trabajo. He decidido dejar el despacho.
—¿Cómo que dejar el despacho? Llevas ocho años ahí. Tienes un buen sueldo, estabilidad, posibilidades de ascenso.
—Lo sé, papá. Pero no soy feliz.
—La felicidad no paga el alquiler, hija.
—Tal vez no. Pero he pensado mucho. Quiero abrir un pequeño taller de cerámica.
—¿Cerámica? ¿Como tu abuela?
—Sí. Como la abuela. He estado dando clases los fines de semana y me encanta. La gente que viene quiere aprender, no está huyendo de nada. Es un ambiente distinto.
—Lucía, esto es una locura. Dejas un trabajo estable por una afición.
—No es una afición, papá. Llevo dos años formándome. Tengo un plan de negocio. He hablado con el banco.
—¿Con el banco? ¿Y si no funciona?
—Entonces habré intentado algo que me importa. ¿Tú nunca has querido hacer algo distinto?
—Yo no tuve esa opción. Tuve que trabajar desde los dieciséis años para mantener a la familia.
—Lo sé. Y te admiro por eso. Pero yo tengo otra oportunidad. Quiero aprovecharla.
—(silencio)
—Papá, dime algo.
—Estoy pensando.
—¿En qué?
—En que tu abuela estaría orgullosa. Ella también dejó su trabajo en la fábrica para montar su taller. Al principio nadie la apoyó. Decían que era una locura.
—¿Y qué pasó?
—Pasó que el taller funcionó. Y que ella fue la mujer más feliz que he conocido. No porque ganara mucho dinero, sino porque hacía lo que amaba.
—Entonces... ¿me apoyas?
—No he dicho eso. He dicho que tu abuela estaría orgullosa. Yo necesito pensarlo.
—Vale. Pero prométeme que lo pensarás de verdad.
—Te lo prometo.
—Gracias, papá.
—Y llámame cuando tengas el plan de negocio. Quiero verlo.
—¿En serio?
—En serio. Si vas a hacer una locura, al menos hazla bien.
—Te quiero, papá.
—Y yo a ti, hija. Y yo a ti.""",
    },
    {
        "titulo": "Leer en la era digital",
        "tipo": "opinion",
        "cuerpo": """Vivimos rodeados de pantallas. Leemos mensajes, correos, noticias, redes sociales. Pero ¿leemos de verdad? La pregunta no es retórica. Según un informe de la UNESCO (2024), el 40% de los jóvenes entre 15 y 24 años no lee ningún libro al año. La cifra sube al 60% en algunos países desarrollados. Y sin embargo, nunca habíamos tenido tanto acceso a la lectura: bibliotecas digitales, audiolibros, suscripciones ilimitadas.

En mi opinión, el problema no es la tecnología. El problema es que hemos confundido información con conocimiento, y entretenimiento con lectura. Un titular no es un artículo. Un mensaje de texto no es una novela. Un vídeo de diez minutos no es un ensayo. Y aunque todos esos formatos tienen su valor, ninguno sustituye a la lectura profunda.

Leer un libro requiere tiempo, silencio y concentración. Tres cosas que el mundo digital nos roba constantemente. Cuando leemos en papel, el cerebro procesa la información de forma distinta: la memoria retiene mejor lo que leemos, la imaginación se activa, la empatía se desarrolla. Un estudio de la Universidad de Valencia (2023) encontró que los lectores habituales de libros en papel muestran mayor capacidad de concentración y mejor comprensión lectora que los que solo leen en pantalla.

No se trata de demonizar lo digital. Los audiolibros, por ejemplo, han acercado la lectura a personas que no pueden leer en papel. Las bibliotecas digitales han democratizado el acceso a libros que antes eran caros o difíciles de encontrar. Las plataformas de lectura social permiten compartir opiniones y descubrir nuevos autores.

Pero hay algo que se pierde cuando solo leemos en pantalla. Se pierde la pausa. La pantalla nos empuja a hacer scroll, a pasar al siguiente estímulo, a no detenernos. El libro, en cambio, nos invita a quedarnos. A releer un párrafo. A subrayar una frase. A cerrar los ojos y pensar.

Mi propuesta es simple: recuperemos el hábito de leer un libro al mes. No hace falta más. Un libro al mes son doce libros al año. Doce oportunidades de aprender algo nuevo, de viajar a otros mundos, de entender otras vidas. Doce oportunidades de parar, de pensar, de crecer.

La lectura no es una pérdida de tiempo. Es una inversión. Y como toda inversión, requiere constancia. Pero los beneficios son enormes: mejor vocabulario, mejor expresión, mejor comprensión del mundo. Y sobre todo, una vida interior más rica.

En la era digital, leer es un acto de rebeldía. Es decir: 'No voy a dejar que las pantallas decidan cómo pienso'. Es recuperar el control. Y ese control, hoy, vale más que nunca.""",
    },
]

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", "ESTADO ACTUAL B2")
textos_actuales = list(TX.objects.filter(nivel_mcer="B2").order_by("id"))
print(f"  Textos B2: {len(textos_actuales)}")
for t in textos_actuales:
    w = wc(t.cuerpo)
    ok = MIN_W <= w <= MAX_W
    print(f"  [{'OK ' if ok else 'FUERA'}] id={t.id:>3}  {w:>4}w  {t.titulo[:50]}")

header("B", "PLAN: 4 REESCRITURAS + 3 NUEVOS")
plan = []
for tx_id, data in REESCRITURAS.items():
    w = wc(data["cuerpo"])
    ok = MIN_W <= w <= MAX_W
    plan.append(("UPDATE", tx_id, data, w))
    print(f"  [{'OK ' if ok else 'FUERA'}] UPDATE id={tx_id:>3}  {w:>4}w  {data['titulo'][:45]}")

for data in NUEVOS:
    w = wc(data["cuerpo"])
    ok = MIN_W <= w <= MAX_W
    existente = TX.objects.filter(titulo=data["titulo"], nivel_mcer="B2").first()
    if existente:
        plan.append(("UPDATE", existente.id, data, w))
        print(f"  [{'OK ' if ok else 'FUERA'}] UPDATE id={existente.id:>3}  {w:>4}w  {data['titulo'][:45]}")
    else:
        plan.append(("CREATE", None, data, w))
        print(f"  [{'OK ' if ok else 'FUERA'}] CREATE        {w:>4}w  {data['titulo'][:45]}")

header("C", "APLICAR" if args.apply else "DRY-RUN")
if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print("  Ejecuta con --apply para escribir.")
    sys.exit(0)

with transaction.atomic():
    for accion, tx_id, data, w in plan:
        if accion == "UPDATE":
            TX.objects.filter(id=tx_id).update(
                titulo=data["titulo"], cuerpo=data["cuerpo"], tipo=data["tipo"],
            )
        else:
            TX.objects.create(
                titulo=data["titulo"], cuerpo=data["cuerpo"], tipo=data["tipo"],
                nivel_mcer="B2", fuente="seed_fase1_b2",
            )
    print(f"  [OK] {len(plan)} operaciones aplicadas")

header("D", "VERIFICAR")
textos_final = list(TX.objects.filter(nivel_mcer="B2").order_by("id"))
en_rango = 0
for t in textos_final:
    w = wc(t.cuerpo)
    ok = MIN_W <= w <= MAX_W
    en_rango += int(ok)
    print(f"  [{'OK ' if ok else 'FUERA'}] id={t.id:>3}  {w:>4}w  {t.titulo[:50]}")

print(f"\n  En rango {MIN_W}-{MAX_W}: {en_rango}/{len(textos_final)}")
if en_rango == len(textos_final) and len(textos_final) >= 10:
    print(f"\n  [OK] FASE 1 B2 COMPLETA")