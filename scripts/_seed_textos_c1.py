"""_seed_textos_c1.py - F1 C1: 7 textos en rango 450-700 + 3 nuevos.

Rango C1: 450-700 palabras.
  - id=3  Promesa incumplida (120w)  -> reescribir a ~550w
  - id=5  Manipulación lenguaje (299w) -> ampliar a ~540w
  - id=8  Ruido redes sociales (447w) -> +5w (borde)
  - id=29 Análisis crítico (484w)     -> sin tocar
  - id=30 Elogio de la lentitud (435w) -> +20w (borde)
  - id=31 Cuento que se escribía solo (724w) -> -30w (borde)
  - id=32 Desinformación (945w)      -> -245w (recortar)
  + 3 nuevos: descriptivo (Lisboa), diálogo (entrevista), instructivo (ensayo)
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
MIN_W, MAX_W = 450, 700

def wc(text):
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

REESCRITURAS = {
    3: {
        "titulo": "La promesa incumplida de la empresa energética",
        "tipo": "informativo",
        "cuerpo": """Una vez más, la empresa energética Promesas S.A. prometió reducir sus emisiones de CO2 un 30% antes de 2025. Una vez más, los datos la desmintieron al mes siguiente de la rueda de prensa: según el informe trimestral publicado por la propia compañía, las emisiones habían aumentado un 4% respecto al año anterior. El patrón se repite desde 2018, cuando la empresa anunció por primera vez su compromiso con la descarbonización. Desde entonces, ha presentado seis planes estratégicos de sostenibilidad, ha firmado tres declaraciones de intenciones con el Ministerio de Transición Ecológica, y ha difundido una decena de campañas publicitarias con el lema "Energía limpia, futuro brillante". Sin embargo, sus emisiones acumuladas han crecido un 22% en el mismo periodo.

El director de sostenibilidad, en declaraciones a este periódico, aseguró que "el incremento es temporal y responde a una mayor demanda energética". La explicación no convence a los expertos. Dos analistas independientes consultados por El Debate señalan que la empresa había recibido subvenciones públicas por valor de 47 millones de euros para mejorar sus plantas y que no hay evidencia de que esas mejoras se hayan ejecutado. "La empresa ha cobrado las ayudas, pero no ha presentado ni un solo informe de progreso", explica Marta Ruiz, investigadora del Observatorio de Transición Energética. "Cuando pedimos los datos, respondieron con un comunicado genérico".

El caso de Promesas S.A. no es aislado. Según un estudio de la Universidad de Barcelona (2024), el 68% de las grandes empresas energéticas europeas incumple los objetivos climáticos que ellas mismas se fijan. El fenómeno tiene nombre: greenwashing, o lavado verde. Consiste en presentar como sostenible una actividad que no lo es, mediante campañas de marketing, declaraciones públicas o informes maquillados. La práctica está regulada en teoría por la Directiva Europea de Información Corporativa en Materia de Sostenibilidad, pero su aplicación es desigual y las sanciones, ridículas en comparación con los beneficios.

"El problema no es que las empresas mientan", señala el catedrático de Ética Empresarial Jorge Marín. "El problema es que mentir les sale gratis. Si una empresa promete reducir emisiones y no lo hace, no devuelve las subvenciones ni enfrenta consecuencias penales. Como mucho, recibe una sanción administrativa que paga con el dinero de otra campaña de marketing". Marín propone que las ayudas públicas se condicionen a la verificación independiente de resultados, y que los directivos respondan con su patrimonio personal en caso de fraude.

La compañía no ha respondido a las preguntas de este periódico. Su página web, sin embargo, sigue mostrando el compromiso: "En Promesas S.A. creemos en un futuro sostenible". El futuro, por ahora, no llega."""
    },
    5: {
        "titulo": "La manipulación del lenguaje en el discurso político",
        "tipo": "informativo",
        "cuerpo": """El lenguaje político no solo transmite información: también construye realidades. Como señala el lingüista George Lakoff (2004) en su obra No pienses en un elefante, "el lenguaje es poder". Quien controla las palabras controla, en parte, lo que los ciudadanos pueden pensar. El análisis crítico del discurso, desarrollado por autores como Norman Fairclough y Teun van Dijk, ha identificado un repertorio de estrategias que los políticos usan para orientar la percepción de la realidad sin mentir explícitamente.

Una de las más frecuentes es el uso de términos aparentemente neutros que esconden una carga ideológica. Un ejemplo claro es la expresión "los ciudadanos de bien". Detrás de esa fórmula aparentemente descriptiva se esconde una distinción entre "nosotros" y "los otros": quienes no encajan en esa categoría son, implícitamente, ciudadanos de mal. El político que usa este término no está describiendo la realidad: está construyendo una identidad colectiva que excluye a quienes no lo votan.

Otra estrategia es la nominalización: convertir acciones en sustantivos para ocultar al responsable. "Se ha producido un incremento del desempleo" no es lo mismo que "el gobierno ha destruido empleo". La primera fórmula presenta el hecho como un fenómeno natural; la segunda, como una decisión política. Los gobiernos suelen preferir la primera porque despolitiza el conflicto.

También son comunes los eslóganes aparentemente positivos. El famoso "España va bien" no describe un estado de cosas: invita al oyente a compartir una visión optimista y a desconfiar de quien la critique. Detrás del eslogan hay una intención persuasiva: quien lo pone en duda es presentado como un agorero. La función del eslogan no es informar, sino clausurar el debate.

Las falsas disyuntivas son otro recurso clásico: "o está con nosotros o está contra España". Esta fórmula, que parece ofrecer una elección, en realidad la cancela: solo hay una opción legítima. Es una falacia que los analistas del discurso llevan décadas señalando, pero que sigue funcionando porque simplifica la complejidad y ofrece una identidad clara.

El eufemismo es quizá la estrategia más antigua. "Daños colaterales" en lugar de "muertes civiles"; "ajuste" en lugar de "recortes"; "flexibilización laboral" en lugar de "despidos más baratos". El eufemismo no miente, pero suaviza la percepción del hecho y dificulta la crítica. Como escribió George Orwell en 1984, "el lenguaje político está diseñado para hacer que las mentiras suenen verdaderas".

Para evaluar la calidad de un discurso político, el lector crítico debe preguntarse: ¿qué evidencia respalda cada afirmación? ¿se citan estudios o solo se apela a la emoción? ¿se presentan los datos completos o solo los que apoyan la tesis? ¿quién es el agente de cada acción? ¿qué se omite? Un discurso con estudios verificables, con datos completos y con reconocimiento de las objeciones es más creíble que uno que solo apela a la emoción y a las generalizaciones.

El análisis del lenguaje político no es un ejercicio de cinismo: es una condición para la ciudadanía. Quien no sabe leer el lenguaje del poder está condenado a obedecerle sin darse cuenta. Como dijo el filósofo Cornelius Castoriadis, "la democracia es el régimen de la reflexividad": sin ciudadanos capaces de analizar el discurso, la democracia se convierte en una cáscara vacía."""
    },
    8: {
        "titulo": "El ruido de las redes sociales",
        "tipo": "informativo",
        "cuerpo": """Las redes sociales han transformado la forma en que nos informamos, pero también la forma en que pensamos. Según el informe Digital 2025 de la consultora We Are Social, el 67% de los adultos españoles usa redes sociales a diario, y el 42% las consulta como primera fuente de información. Estos datos deberían hacernos reflexionar: si la mayoría se informa por redes, la calidad de la información pública depende, en gran medida, de la calidad de esas redes.

El primer problema es el ruido. Las redes están diseñadas para maximizar la atención, no para informar. Los algoritmos priorizan el contenido que genera interacción (likes, compartidos, comentarios), y ese contenido suele ser el más emocional, no el más veraz. Un estudio de la Universidad de Oxford (2024) encontró que las noticias falsas se comparten un 70% más que las verdaderas. No es porque la gente sea tonta: es porque el sistema está diseñado para premiar la emoción.

El segundo problema es la cámara de eco. Los algoritmos nos muestran lo que coincide con nuestras opiniones previas, y eso refuerza nuestras creencias en lugar de cuestionarlas. El filósofo Cass Sunstein (2001) llamó a esto "la república de la eco": un espacio donde solo escuchamos lo que ya pensamos. El resultado es una sociedad más polarizada, donde el que piensa distinto no es un interlocutor, sino un enemigo.

El tercer problema es la pérdida de contexto. Un tuit de 280 caracteres no puede explicar un conflicto complejo. Un video de 30 segundos no puede analizar una reforma fiscal. La brevedad es enemiga de la matización, y sin matices no hay pensamiento crítico posible. Como escribió el periodista Ezra Klein (2020), "las redes no nos hacen más tontos, pero sí nos hacen más rápidos, y la rapidez es enemiga de la reflexión".

El cuarto problema es la erosión de la confianza. Cuando el 67% se informa por redes y las noticias falsas se comparten más que las verdaderas, la consecuencia es que la sociedad deja de creer en cualquier información. El escepticismo universal es tan peligroso como la credulidad universal: si nada es verdad, cualquier cosa puede serlo.

La solución no es abandonar las redes, sino exigirles lo que no tienen: contexto, verificación y responsabilidad. Las redes no son el problema; el problema es creer que las redes son la solución. Como escribió el filósofo Byung-Chul Han (2021), "la transparencia total no es la verdad: es la muerte de la verdad". La educación mediática, la verificación de fuentes y el pensamiento crítico son las únicas vacunas contra el ruido. Y esa vacuna no se administra en las redes: se administra en la escuela, en la familia y en la lectura."""
    },
    30: {
        "titulo": "Elogio de la lentitud",
        "tipo": "argumentativo",
        "cuerpo": """Vivimos en la era de la prisa. Todo debe ser ya, ahora, inmediato. La sociedad nos empuja a correr sin saber hacía dónde. Pero yo me pregunto: ¿de verdad queremos vivir así?

El tiempo es oro, dicen. Y como todo el mundo lo repite, parece que nadie se atreve a cuestionarlo. Sin embargo, esa metáfora económica esconde una trampa: si el tiempo es dinero, entonces el que no corre está perdiendo. Y así, todos corremos, sin detenernos a preguntar hacia dónde ni por qué.

Los defensores de la velocidad sostienen que la rapidez es progreso. "El que no corre, vuela", afirman, como si la vida fuera una competición. Pero detrás de esa idea se esconde una premisa que nunca se explicita: que el valor de la vida se mide en productividad. ¿Y si no fuera así? ¿Y si el valor estuviera en otra parte? ¿Y si la vida no fuera un proyecto que hay que optimizar, sino una experiencia que hay que habitar?

Mientras escribo esto, mi vecino sale corriendo a las siete de la mañana con un café en la mano. Vuelve a las once de la noche, agotado. Su vida es una línea recta entre el trabajo y la cama. ¿Es eso vivir? ¿O es solo sobrevivir? No lo digo con desprecio: lo digo con tristeza. Porque yo también he vivido así, y sé que ese ritmo no deja espacio para nada más. Ni para pensar, ni para sentir, ni para estar.

Algunos me dirán que soy un nostálgico. "Claro", responden, "tú quieres volver al siglo XIX". Nada más lejos de la realidad. Yo no quiero volver al pasado: quiero recuperar el presente. Y el presente exige tiempo, atención, pausa. Exige detenerse, aunque solo sea un momento, y mirar lo que tenemos delante.

Pensemos en el arte de la conversación. Una buena conversación requiere tiempo: escuchar, pensar, responder. La velocidad la mata. Lo mismo ocurre con el amor, con la amistad, con la lectura. Todo lo valioso necesita tiempo. Lo dijo Milan Kundera: "La lentitud es la felicidad". Y tenía razón. No porque la lentitud sea un fin en sí misma, sino porque sin ella no hay profundidad.

Algunos objetarán que la lentitud es un privilegio de ricos. Es cierto: no todos pueden permitirse el lujo de bajar el ritmo. Pero esa objeción, lejos de refutar mi tesis, la refuerza: precisamente porque la lentitud es un derecho, deberíamos defenderla para todos, no solo para unos pocos. La lentitud no debería ser un lujo: debería ser una condición de la vida buena.

Y no me vengan con que la tecnología nos hará más libres. La tecnología, en manos de las grandes corporaciones, se ha convertido en una nueva forma de esclavitud: notificaciones, algoritmos, likes. Nos prometieron libertad y nos dieron vigilancia. Nos prometieron conexión y nos dieron soledad. Nos prometieron velocidad y nos dieron ansiedad.

¿Qué hacer, entonces? La respuesta no es fácil. Pero quizá el primer paso sea reconocer que vivimos en una mentira: la mentira de la velocidad como valor. Solo reconociéndola podremos empezar a desmontarla. Y quizá el segundo paso sea empezar por nosotros mismos: bajar el ritmo, aunque sea un poco, y ver qué pasa.

Yo, por mi parte, he decidido bajar el ritmo. Camino más despacio, leo más despacio, escucho más despacio. Y desde entonces, extrañamente, soy más feliz. Quizá la felicidad no esté en correr, sino en detenerse a mirar."""
    },
    31: {
        "titulo": "El cuento que se escribía solo",
        "tipo": "literario",
        "cuerpo": """Aurelio encontró el cuaderno en el fondo de un cajón, entre facturas y fotografías viejas. Era un cuaderno de tapas negras, como los que usaba de joven para escribir sus cuentos. Lo abrió con curiosidad. En la primera página, con su propia letra, había un cuento titulado "El bibliotecario". Lo reconoció: era un cuento que había escrito a los veinte años.

Lo leyó. Trataba de un bibliotecario que descubría que todos los libros de su biblioteca hablaban de él. Aurelio sonrió. Aquel cuento era un homenaje a Borges, a "La biblioteca de Babel". Recordó la frase de Borges: "El universo (que otros llaman la Biblioteca) se compone de un número indefinido, y tal vez infinito, de galerías hexagonales". Siempre le había fascinado esa idea.

Pasó la página. En la segunda, había otro cuento, titulado "El espejo". No lo recordaba. Lo leyó. Trataba de un hombre que se miraba en un espejo y descubría que su reflejo era otro hombre, que a su vez lo miraba a él. Aurelio sintió un escalofrío. No recordaba haber escrito aquel cuento, pero la letra era suya. Y el estilo también.

Pasó otra página. Un tercer cuento, titulado "El sueño". Trataba de un hombre que soñaba con un hombre que soñaba con él. El cuento terminaba con la frase: "Y al despertar, comprendió que él era el sueño del otro". Aurelio dejó el cuaderno sobre la mesa. Aquello era demasiado. Él no había escrito esos cuentos. O quizá sí, y los había olvidado. O quizá alguien los había escrito por él.

Aquella noche no pudo dormir. Se levantó a las tres de la mañana y volvió al cuaderno. En la última página, había un cuento nuevo, titulado "El lector". Lo leyó temblando. Trataba de un hombre llamado Aurelio que encontraba un cuaderno en el fondo de un cajón y leía cuentos que no recordaba haber escrito. El cuento terminaba con la frase: "Y entonces Aurelio comprendió que él también era un personaje, y que alguien, en algún lugar, lo estaba leyendo".

Cerró el cuaderno. Miró por la ventana. La ciudad dormía. Y por primera vez en su vida, Aurelio se preguntó si él también sería un personaje, y si alguien, en algún lugar, estaría leyendo su historia.

Al día siguiente, Aurelio fue a ver a su amigo Bernardo, profesor de literatura. Le contó lo sucedido. Bernardo lo escuchó con atención. "Interesante", dijo. "Es un caso de metaficción. Como en El Quijote, cuando los personajes han leído el Quijote. O como en Cortázar, cuando el lector es personaje. O como en Borges, cuando el sueño y la vigilia se confunden".

"Pero yo no lo escribí", dijo Aurelio. "Yo no escribí esos cuentos".

Bernardo sonrió. "Quizá no los escribiste tú. Quizá te escribieron a ti. Quizá tú eres el personaje de un cuento que alguien está escribiendo ahora mismo, en este instante".

Aurelio sintió un vértigo. Miró sus manos. Miró la mesa. Miró a Bernardo. Todo parecía real. Pero quizá no lo era. Quizá todo era un sueño, o un cuento, o una metáfora.

"Mira", dijo Bernardo, "te voy a contar un cuento. Había una vez un hombre llamado Aurelio que descubrió que era un personaje. Y al descubrirlo, empezó a escribir su propia historia. Y al escribirla, se liberó. Porque escribir es una forma de liberarse, aunque sea de la ficción".

Aurelio lo miró. "¿Y cómo termina el cuento?"

"No termina", dijo Bernardo. "Los cuentos que se escriben solos nunca terminan. Solo se interrumpen. Y luego, en algún otro lugar, alguien los retoma".

Aurelio volvió a su casa. Abrió el cuaderno. En la última página, había un cuento nuevo. Titulado "El principio". Y en él, Aurelio se veía a sí mismo escribiendo el cuento que estaba leyendo. Y así, en un bucle infinito, el cuento se escribía solo.

Aurelio cerró el cuaderno. Sonrió. Y por primera vez en su vida, comprendió que la literatura no es un espejo de la realidad, sino una realidad paralela. Y que él, Aurelio, era a la vez autor y personaje, lector y escrito, principio y fin.

O quizá no. Quizá todo era un sueño. O quizá todo era un cuento. Pero de algo estaba seguro: mientras alguien lo leyera, él seguiría existiendo. Y eso, después de todo, era una forma de inmortalidad."""
    },
    32: {
        "titulo": "Desinformación: cómo detectar la manipulación",
        "tipo": "argumentativo",
        "cuerpo": """Vivimos en la era de la desinformación. Cada día recibimos cientos de mensajes que intentan convencernos de algo. Algunos son honestos; otros, no. Este texto ofrece herramientas para detectar la manipulación y evaluar críticamente la información.

1. Argumentos con premisas implícitas

Muchos argumentos ocultan premisas que no se explicitan. "Deberíamos prohibir los videojuegos violentos; son peligrosos" presupone que todo lo peligroso debe prohibirse. Si no aceptamos esa premisa, la conclusión no se sigue. Evaluar la solidez de un argumento requiere explicitar esas premisas y comprobar si son verdaderas.

2. Manipulación mediática: framing y priming

Los medios pueden manipular mediante el framing (encuadre) y el priming (activación de marcos mentales). "Inmigrantes ocupan la plaza" presenta el fenómeno como invasión; "familias migrantes llegan a la plaza" presenta el mismo hecho de forma neutra. El encuadre ya orienta la interpretación.

3. Evidencia científica: muestra, método, replicabilidad

Un estudio con 20 participantes no es evidencia suficiente para una conclusión general. La evidencia es de calidad si la muestra es representativa, el método es sólido y los resultados son replicables. Aceptar un estudio sin estos criterios es aceptar evidencia de baja calidad.

4. Falacia de autoridad científica

"Un premio Nobel dice que X, luego X es verdad" es una falacia si no se aporta evidencia. La autoridad no sustituye a la prueba. En el discurso científico, apelar al prestigio del emisor en lugar de a los datos es una forma de manipulación.

5. Coherencia entre discurso y práctica

Una empresa que declara sostenibilidad pero contamina es incoherente. Una institución que defiende la transparencia pero oculta datos también. Evaluar la coherencia entre discurso y práctica permite detectar la hipocresía institucional.

6. Falsa dicotomía

El discurso político suele presentar solo dos opciones: "O estás con nosotros o estás contra nosotros". Es una falsa dicotomía: hay muchas posiciones intermedias. Detectar esta falacia permite analizar críticamente la retórica política.

7. Calidad del debate público

Un debate de calidad incluye contraargumentos, evita falacias y aporta evidencia. Un debate de baja calidad se basa en descalificaciones y datos sin contexto. Evaluar la calidad del debate es esencial para una democracia sana.

8. Manipulación estadística

Los gráficos engañosos (escalas truncadas, 3D), los porcentajes sin base y las tasas sin contexto son formas de manipulación estadística. Un gráfico que empieza en 95 en lugar de 0 exagera una diferencia pequeña.

9. Intención persuasiva oculta

Algunos textos aparentemente informativos tienen una intención persuasiva oculta: selección de datos, framing, fuentes sesgadas. Un reportaje que solo muestra una versión de un conflicto tiene intención persuasiva oculta, aunque no opine explícitamente.

10. Falsa equivalencia

La falsa equivalencia equipara cosas que no son comparables. "Es como comparar el cáncer con un resfriado" es una falsa equivalencia. Detectar esta falacia permite analizar críticamente comparaciones en el discurso público.

11. Argumento estadístico complejo: tasas, base, contexto

"El 50% de los que enferman son vacunados" es engañoso si no se mira la base: si el 95% está vacunado, ese 50% es esperable. Sin analizar la base y el contexto, la estadística engaña. Un argumento estadístico es sólido si la base es clara, las tasas se usan correctamente y el contexto se considera.

12. Sesgo algorítmico

Los algoritmos de selección de información (redes sociales, buscadores) crean cámaras de eco: muestran solo contenido afín a nuestros intereses. Detectar este sesgo permite evaluar críticamente la información que consumimos y salir de la burbuja.

13. Analogía compleja: diferencias relevantes

"Como el cuerpo necesita ejercicio, la mente necesita estimulación" es una analogía relevante. "Como los barcos necesitan capitán, los países necesitan rey" tiene diferencias relevantes (un país no es un barco). Evaluar una analogía requiere identificar esas diferencias.

14. Falsa premisa

La falsa premisa se presenta como verdadera sin justificación. "Todos los jóvenes son vagos; por tanto, no hay que contratarlos" contiene una premisa falsa. Detectar esta falacia permite rechazar conclusiones basadas en premisas no sustentadas.

15. Calidad ética de un argumento

Un argumento puede ser lógicamente válido pero éticamente rechazable. Defender la esclavitud con lógica es éticamente rechazable. La calidad ética depende del respeto a la dignidad, la justicia y las personas.

16. Falsa causa compleja: multicausalidad

"La delincuencia se debe solo a la inmigración" ignora la multicausalidad (pobreza, educación, etc.). Detectar esta falacia permite analizar críticamente explicaciones simplistas de fenómenos complejos.

17. Coherencia entre medios, fines y valores

Un argumento político es sólido si los medios propuestos son coherentes con los fines y con los valores declarados. Defender la libertad usando censura es incoherente. Evaluar esta coherencia permite analizar críticamente las propuestas políticas.

18. Manipulación emocional en publicidad

"Si quieres ser feliz, compra este coche" apela a la emoción sin argumentos racionales. La publicidad manipula usando emociones para persuadir. Detectar esta manipulación permite analizar críticamente los anuncios.

Conclusión

La desinformación no se combate con más información, sino con pensamiento crítico. Las 18 herramientas de este texto son un kit básico para detectar la manipulación y evaluar críticamente la información. Aplicarlas no garantiza la verdad, pero al menos nos protege de la mentira."""
    },
}

NUEVOS = [
    {
        "titulo": "Lisboa, ciudad de contrastes",
        "tipo": "descriptivo",
        "cuerpo": """Lisboa no se deja describir fácilmente. Es una ciudad que se ofrece al visitante en capas, como una cebolla que hay que ir pelando. Cada barrio tiene su propio ritmo, su propia luz, su propia manera de estar en el mundo. Quien la visita por primera vez suele llevarse la impresión de una ciudad vieja y cansada, con fachadas desconchadas y tranvías que chirrían. Quien se queda unos días descubre que esa impresión es solo la superficie.

El barrio de Alfama es el más antiguo. Sus calles estrechas serpentean por una colina empinada, y las casas se apiñan unas contra otras como si tuvieran miedo de caerse. Las paredes están cubiertas de azulejos, algunos azules, otros verdes, otros ya descoloridos por el sol. Por las mañanas, las mujeres mayores se asoman a los balcones y sacuden las alfombras; por las tardes, los turistas se pierden entre las callejuelas buscando el mirador de Santa Lucía. Por las noches, el barrio se llena de música: el fado sale de los bares y se mezcla con el olor a sardinas asadas.

El Chiado es lo contrario. Es el barrio elegante, el de las tiendas de lujo y las librerías históricas. Aquí está la librería Bertrand, la más antigua del mundo en funcionamiento, con sus estanterías de madera oscura y sus techos altos. Aquí está también el café A Brasileira, donde Fernando Pessoa se sentaba a escribir y donde hoy una estatua de bronce lo recuerda. El Chiado es un barrio para caminar despacio, para detenerse en cada escaparate, para mirar y dejarse mirar.

Y luego está el Barrio Alto, que es el barrio de la noche. Sus calles, también empinadas, se llenan al anochecer de jóvenes que van de bar en bar. La música sale a la calle, las risas también. Es un barrio ruidoso, desordenado, vivo. Alguien dijo que Lisboa es una ciudad que se vive de noche, y el Barrio Alto parece darle la razón.

Pero Lisboa es también una ciudad de contrastes económicos. A pocos metros de las tiendas de lujo del Chiado, hay edificios abandonados, con las ventanas rotas y las paredes grafiteadas. El turismo ha transformado el centro: los pisos turísticos han desplazado a los vecinos, los alquileres han subido, y muchos jóvenes se han ido a vivir a la periferia. Es una ciudad que se vende a sí misma, y en ese proceso, a veces, se pierde.

Al atardecer, cuando el sol cae sobre el Tajo, Lisboa se vuelve dorada. Las colinas se iluminan, los tejados brillan, y el río parece una cinta de plata. Desde el mirador de São Pedro de Alcântara, la ciudad se extiende a los pies del visitante como un mapa antiguo. Y uno entiende, de repente, por qué Pessoa escribió que Lisboa es "el lugar donde el mar termina y la saudade empieza". Esa mezcla de belleza y melancolía, de esplendor y abandono, es lo que hace única a esta ciudad. Una ciudad que no se deja describir fácilmente, pero que, una vez conocida, no se olvida jamás."""
    },
    {
        "titulo": "La entrevista",
        "tipo": "dialogo",
        "cuerpo": """—Pase, siéntese. Gracias por venir, Laura.

—Gracias a usted por la oportunidad, señora directora.

—Llámame Carmen. Aquí no somos muy formales. He leído tu currículum. Tienes una trayectoria interesante.

—Muchas gracias. He intentado formarme en distintos ámbitos.

—Veo que has trabajado en tres empresas en cinco años. ¿Por qué tantos cambios?

—Cada cambio ha sido una decisión meditada. En la primera empresa aprendí lo básico del sector. En la segunda, tuve la oportunidad de liderar un equipo pequeño. En la tercera, me ofrecieron un puesto con más responsabilidad, pero la empresa cerró.

—¿Y por qué no has vuelto a buscar trabajo en ese sector?

—Porque me di cuenta de que quería cambiar de rumbo. El sector de la consultoría es muy exigente, y yo quería un trabajo con más impacto social. Por eso me presenté a esta oferta.

—Interesante. ¿Qué sabes de nuestra organización?

—Sé que trabajáis en proyectos de cooperación internacional, sobre todo en África y América Latina. He leído el informe anual del año pasado y me ha impresionado el enfoque de sostenibilidad a largo plazo.

—Bien documentada. Eso me gusta. Ahora dime: ¿cuál es tu mayor debilidad?

—Mi mayor debilidad es que a veces me cuesta delegar. Tiendo a querer controlarlo todo, y eso puede ser un problema cuando trabajo en equipo. Estoy trabajando en ello, aprendiendo a confiar más en mis compañeros.

—Es una respuesta honesta. Mucha gente dice "soy perfeccionista" y se queda tan tranquila. ¿Y tu mayor fortaleza?

—Mi capacidad de adaptación. He cambiado de sector, de ciudad, de equipo, y siempre he sabido encontrar mi lugar. Creo que eso es útil en una organización como esta, donde los proyectos cambian constantemente.

—De acuerdo. ¿Tienes alguna pregunta para mí?

—Sí, dos. La primera: ¿cómo se mide el éxito en este puesto? La segunda: ¿qué espera de la persona que ocupe este cargo en los primeros seis meses?

—Buenas preguntas. El éxito se mide por el impacto de los proyectos, no por el número de horas trabajadas. Y en los primeros seis meses espero que la persona conozca los proyectos en profundidad, que se gane la confianza del equipo y que proponga al menos una mejora concreta.

—Entiendo. Me parece un enfoque muy sensato.

—Bien, Laura. Tengo que entrevistar a dos personas más, pero te adelanto que tu perfil encaja. Te llamaremos en una semana.

—Muchas gracias, Carmen. Ha sido un placer.

—El placer ha sido mío. Hasta pronto."""
    },
    {
        "titulo": "Cómo escribir un ensayo argumentativo",
        "tipo": "instructivo",
        "cuerpo": """Escribir un ensayo argumentativo es una de las habilidades más útiles que puede desarrollar un estudiante. No se trata solo de expresar una opinión, sino de construir un razonamiento sólido, con pruebas y con reconocimiento de las objeciones. Este texto ofrece una guía práctica para escribir un ensayo argumentativo de nivel universitario.

Paso 1: elegir un tema y una tesis

El primer paso es elegir un tema que te interese y sobre el que puedas investigar. No elijas un tema demasiado amplio ("la educación") ni demasiado estrecho ("las sillas del aula 23"). Busca un tema que tenga debate: "¿deberían prohibirse los móviles en los institutos?", "¿es ético el uso de animales en la investigación?".

Una vez elegido el tema, formula una tesis. La tesis es la afirmación central que vas a defender. Debe ser clara, discutible y específica. No escribas "los móviles son malos": escribe "los móviles en los institutos deberían prohibirse durante las horas de clase, pero permitirse en el recreo". Cuanto más específica sea la tesis, más fácil será argumentar.

Paso 2: investigar y seleccionar fuentes

Una tesis sin pruebas es solo una opinión. Necesitas investigar. Busca fuentes académicas, informes de organizaciones reconocidas, datos oficiales. Evita las fuentes anónimas, los blogs sin autoría y las redes sociales. Anota siempre la procedencia de cada dato: autor, año, título, editorial.

No todas las fuentes valen lo mismo. Una fuente primaria (un estudio original) vale más que una secundaria (un artículo que resume el estudio). Una fuente académica vale más que una periodística. Una fuente reciente vale más que una antigua. Selecciona las fuentes más sólidas y descarta las demás.

Paso 3: estructurar el ensayo

Un ensayo argumentativo tiene tres partes: introducción, desarrollo y conclusión. La introducción presenta el tema y la tesis. El desarrollo expone los argumentos, con pruebas y con reconocimiento de las objeciones. La conclusión sintetiza lo dicho y proyecta el tema hacia el futuro.

En el desarrollo, cada párrafo debe tener una idea principal y varias ideas secundarias que la apoyen. No mezcles ideas en un mismo párrafo. Usa conectores para mostrar la relación entre las ideas: "además", "sin embargo", "por tanto", "en consecuencia".

Paso 4: reconocer las objeciones

Un buen ensayo argumentativo no ignora las objeciones: las reconoce y las responde. Si tu tesis es "los móviles deberían prohibirse en clase", reconoce que "algunos profesores defienden su uso pedagógico" y responde: "sin embargo, los estudios muestran que la mayoría de los usos son recreativos". Reconocer las objeciones fortalece tu argumento, no lo debilita.

Paso 5: revisar y corregir

El último paso es revisar. Lee el ensayo en voz alta: si te trabas, algo falla. Revisa la claridad, la coherencia, la ortografía, la puntuación. Verifica que cada afirmación esté respaldada por una fuente. Y comprueba que la conclusión responda realmente a la tesis planteada.

Un ensayo argumentativo bien escrito es una herramienta poderosa: permite pensar con rigor, comunicar con claridad y participar en el debate público. No es fácil, pero se aprende con la práctica. Como dijo el filósofo Bertrand Russell, "el problema del mundo es que los tontos están seguros de todo y los inteligentes llenos de dudas". Un buen ensayo argumentativo es, ante todo, un ejercicio de duda metódica."""
    },
]

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", "ESTADO ACTUAL C1")
textos_actuales = list(TX.objects.filter(nivel_mcer="C1").order_by("id"))
print(f"  Textos C1: {len(textos_actuales)}")
for t in textos_actuales:
    w = wc(t.cuerpo)
    ok = MIN_W <= w <= MAX_W
    print(f"  [{'OK ' if ok else 'FUERA'}] id={t.id:>3}  {w:>4}w  {t.titulo[:55]}")

header("B", "PLAN: 6 REESCRITURAS + 3 NUEVOS")
plan = []
for tx_id, data in REESCRITURAS.items():
    w = wc(data["cuerpo"])
    ok = MIN_W <= w <= MAX_W
    plan.append(("UPDATE", tx_id, data, w))
    print(f"  [{'OK ' if ok else 'FUERA'}] UPDATE id={tx_id:>3}  {w:>4}w  {data['titulo'][:50]}")

for data in NUEVOS:
    w = wc(data["cuerpo"])
    ok = MIN_W <= w <= MAX_W
    existente = TX.objects.filter(titulo=data["titulo"], nivel_mcer="C1").first()
    if existente:
        plan.append(("UPDATE", existente.id, data, w))
        print(f"  [{'OK ' if ok else 'FUERA'}] UPDATE id={existente.id:>3}  {w:>4}w  {data['titulo'][:50]}")
    else:
        plan.append(("CREATE", None, data, w))
        print(f"  [{'OK ' if ok else 'FUERA'}] CREATE        {w:>4}w  {data['titulo'][:50]}")

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
                nivel_mcer="C1", fuente="seed_fase1_c1",
            )
    print(f"  [OK] {len(plan)} operaciones aplicadas")

header("D", "VERIFICAR")
textos_final = list(TX.objects.filter(nivel_mcer="C1").order_by("id"))
en_rango = 0
for t in textos_final:
    w = wc(t.cuerpo)
    ok = MIN_W <= w <= MAX_W
    en_rango += int(ok)
    print(f"  [{'OK ' if ok else 'FUERA'}] id={t.id:>3}  {w:>4}w  {t.titulo[:55]}")

print(f"\n  En rango {MIN_W}-{MAX_W}: {en_rango}/{len(textos_final)}")
if en_rango == len(textos_final) and len(textos_final) >= 10:
    print(f"\n  [OK] FASE 1 C1 COMPLETA")