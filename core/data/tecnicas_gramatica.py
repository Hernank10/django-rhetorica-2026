"""Data del modulo 11: gramatica castellana. Bloque A (1-15)."""

TECNICAS = [
    {"numero": 1, "bloque": "A", "nivel": "basico",
     "titulo": "Del latin vulgar al castellano",
     "teoria": "El castellano nace del latin vulgar hablado en la peninsula iberica entre los siglos V y X, tras la caida del Imperio Romano.",
     "explicacion": "No viene del latin clasico de Ciceron, sino del latin hablado por el pueblo, que evoluciono de forma distinta en cada region.",
     "regla": "Castellano = evolucion del latin vulgar (no del clasico)",
     "ejemplo_correcto": "El castellano proviene del latin vulgar.",
     "ejemplo_incorrecto": "El castellano proviene del latin clasico."},
    {"numero": 2, "bloque": "A", "nivel": "intermedio",
     "titulo": "Glosas Emilianenses (s. X)",
     "teoria": "Las Glosas Emilianenses son las primeras anotaciones escritas en una lengua romance peninsular, encontradas en el monasterio de San Millan de la Cogolla.",
     "explicacion": "No son textos literarios sino aclaraciones marginales en romance para entender textos latinos. Marcan el nacimiento escrito del castellano.",
     "regla": "Glosas Emilianenses = primeros textos escritos en romance (s. X)",
     "ejemplo_correcto": "Las Glosas Emilianenses son del siglo X.",
     "ejemplo_incorrecto": "Las Glosas Emilianenses son del siglo XV."},
    {"numero": 3, "bloque": "A", "nivel": "intermedio",
     "titulo": "Alfonso X el Sabio y el castellano oficial",
     "teoria": "Alfonso X (s. XIII) hizo del castellano la lengua oficial de la corte y de la administracion, sustituyendo al latin.",
     "explicacion": "Fijo la ortografia, impulso las traducciones y creo prosa cientifica en castellano. Por eso se le llama 'el Sabio'.",
     "regla": "Alfonso X: castellano como lengua oficial (s. XIII)",
     "ejemplo_correcto": "Alfonso X impulso el castellano como lengua oficial.",
     "ejemplo_incorrecto": "Alfonso X prohibio el uso del castellano."},
    {"numero": 4, "bloque": "A", "nivel": "basico",
     "titulo": "Nebrija y su Gramatica castellana (1492)",
     "teoria": "Antonio de Nebrija publico en 1492 la primera gramatica de una lengua romance europea: la Gramatica castellana.",
     "explicacion": "La dedico a Isabel la Catolica. Fue la primera vez que se describieron sistematicamente las reglas del castellano.",
     "regla": "Nebrija: primera gramatica del castellano (1492)",
     "ejemplo_correcto": "Nebrija publico la Gramatica castellana en 1492.",
     "ejemplo_incorrecto": "Nebrija publico la primera gramatica del latin en 1492."},
    {"numero": 5, "bloque": "A", "nivel": "basico",
     "titulo": "El Siglo de Oro",
     "teoria": "Los siglos XVI y XVII (Siglo de Oro) consolidaron el castellano como lengua literaria y diplomatica, con autores como Cervantes, Lope de Vega y Quevedo.",
     "explicacion": "Se publican el Quijote (1605, 1615), se fija la ortografia practica y el castellano se expande por America.",
     "regla": "Siglo de Oro = consolidacion literaria del castellano",
     "ejemplo_correcto": "El Quijote se publico en 1605.",
     "ejemplo_incorrecto": "El Quijote se publico en el siglo XIX."},
]

# Continuacion de TECNICAS: tecnicas 6-10
TECNICAS_6_10 = [
    {"numero": 6, "bloque": "A", "nivel": "basico",
     "titulo": "Fundacion de la RAE (1713)",
     "teoria": "La Real Academia Espanola fue fundada en 1713 por Juan Manuel Fernandez Pacheco, marques de Villena, bajo el reinado de Felipe V.",
     "explicacion": "Su lema es 'limpia, fija y da esplendor'. Publico el Diccionario de Autoridades (1726-1739) y la primera Ortografia (1741).",
     "regla": "RAE fundada en 1713",
     "ejemplo_correcto": "La RAE se fundo en 1713.",
     "ejemplo_incorrecto": "La RAE se fundo en 1813."},
    {"numero": 7, "bloque": "A", "nivel": "avanzado",
     "titulo": "Ortografia RAE 2010",
     "teoria": "La Ortografia de la lengua espanola de 2010 es la referencia actual de las reglas ortograficas del castellano.",
     "explicacion": "Unifico criterios y elimino excepciones. Por ejemplo, elimino la tilde en 'solo' (adverbio) y en los demostrativos, aunque admite su uso si hay ambiguedad.",
     "regla": "Ortografia vigente: RAE 2010",
     "ejemplo_correcto": "Segun la RAE 2010, 'solo' no lleva tilde.",
     "ejemplo_incorrecto": "Segun la RAE 2010, 'solo' siempre lleva tilde."},
    {"numero": 8, "bloque": "A", "nivel": "avanzado",
     "titulo": "Nueva gramatica de la lengua espanola (2009)",
     "teoria": "La Nueva gramatica (2009) es la gramatica academica de referencia actual, publicada por la RAE y la ASALE.",
     "explicacion": "Sustituye a la Gramatica de 1931. Es descriptiva (no prescriptiva) y panhispanica: recoge el uso de todos los paises hispanohablantes.",
     "regla": "Gramatica vigente: Nueva gramatica 2009",
     "ejemplo_correcto": "La Nueva gramatica es de 2009.",
     "ejemplo_incorrecto": "La Nueva gramatica es de 1931."},
    {"numero": 9, "bloque": "A", "nivel": "avanzado",
     "titulo": "Diccionario panhispanico de dudas (2005)",
     "teoria": "El Diccionario panhispanico de dudas (DPD) resuelve dudas gramaticales, lexicas y ortograficas del castellano.",
     "explicacion": "Es la obra de referencia para casos como 'dequeismo', 'leismo' o usos preposicionales. Panhispanico: cubre todo el mundo hispanohablante.",
     "regla": "DPD (2005) = referencia de dudas del espanol",
     "ejemplo_correcto": "El DPD aclara dudas como 'dequeismo'.",
     "ejemplo_incorrecto": "El DPD solo recoge el espanol de Espana."},
    {"numero": 10, "bloque": "A", "nivel": "intermedio",
     "titulo": "El espanol en America",
     "teoria": "El castellano llego a America en 1492 con Colon y evoluciono de forma independiente en cada region, dando lugar a variantes: mexicano, argentino, colombiano, etc.",
     "explicacion": "Todas las variantes son igual de validas. La RAE y la ASALE trabajan juntas desde 1951 en la normativa panhispanica.",
     "regla": "Espanol de America: variantes igual de validas",
     "ejemplo_correcto": "El espanol de America tiene variantes regionales validas.",
     "ejemplo_incorrecto": "Solo el espanol de Espana es correcto."},
]

TECNICAS.extend(TECNICAS_6_10)

TECNICAS_11_15 = [
    {"numero": 11, "bloque": "A", "nivel": "intermedio",
     "titulo": "El espanol global hoy",
     "teoria": "El espanol es la segunda lengua materna del mundo (~500 millones de hablantes nativos) y la segunda mas estudiada como lengua extranjera.",
     "explicacion": "Es lengua oficial en 21 paises. La mayor comunidad de hablantes esta en Mexico, seguida de EE.UU. (donde es la segunda lengua mas hablada).",
     "regla": "Espanol: ~500M nativos, 21 paises oficiales",
     "ejemplo_correcto": "Mexico tiene la mayor comunidad hispanohablante.",
     "ejemplo_incorrecto": "Espana tiene la mayor comunidad hispanohablante."},
    {"numero": 12, "bloque": "A", "nivel": "intermedio",
     "titulo": "Historia de la ortografia espanola",
     "teoria": "La ortografia espanola ha tenido 5 grandes reformas: 1741 (RAE), 1754, 1815, 1844 y 2010. La ultima simplifico reglas y unifico criterios.",
     "explicacion": "Cambios notables: eliminacion de la tilde en 'solo' y demostrativos (2010), cambio de 'quorum' a 'cuorum', y de 'psicologia' a 'sicologia' (ya no se pronuncia la p-).",
     "regla": "Ortografia espanola: 5 reformas desde 1741",
     "ejemplo_correcto": "La ortografia ha cambiado desde 1741.",
     "ejemplo_incorrecto": "La ortografia no ha cambiado desde el siglo XVIII."},
    {"numero": 13, "bloque": "A", "nivel": "avanzado",
     "titulo": "Historia de la acentuacion",
     "teoria": "La tilde espanola surgio en el siglo XVI con Lebrija. La clasificacion actual (agudas, llanas, esdrujulas) se fijo en el siglo XIX y se simplifico en 1999 y 2010.",
     "explicacion": "La tilde diacritica (para distinguir funciones: 'el'/'el') fue variando hasta la RAE 2010. Algunos paises conservan usos no normativos.",
     "regla": "Clasificacion actual de tildes: desde s. XIX, actualizada 2010",
     "ejemplo_correcto": "Las reglas de acentuacion se actualizaron en 2010.",
     "ejemplo_incorrecto": "Las reglas de acentuacion son de 1492."},
    {"numero": 14, "bloque": "A", "nivel": "avanzado",
     "titulo": "Historia de la puntuacion",
     "teoria": "El sistema de puntuacion espanol (punto, coma, punto y coma, dos puntos, comillas, parentesis, rayas) se fue configurando entre los siglos XVI y XVIII.",
     "explicacion": "Los signos de interrogacion y exclamacion de apertura (¿ ? ¡ !) son una peculiaridad del espanol. La RAE 2010 aclaro usos de comillas, comas y rayas.",
     "regla": "Signos de apertura ¿ ¡ son exclusivos del espanol",
     "ejemplo_correcto": "El espanol usa '¿' al inicio de la pregunta.",
     "ejemplo_incorrecto": "El espanol solo usa '?' al final, como el ingles."},
    {"numero": 15, "bloque": "A", "nivel": "intermedio",
     "titulo": "El espanol en la era digital",
     "teoria": "Internet ha acelerado los cambios: anglicismos, nuevos sufijos y abreviaturas. La RAE admite y regula muchos de estos neologismos.",
     "explicacion": "Ejemplos: 'tuit' (validado 2012), 'guglear' (aceptado en 2020 en el diccionario), 'cederrón' (adaptacion de CD-ROM). Otros se rechazan o se proponen alternativas.",
     "regla": "La RAE acepta anglicismos adaptados al espanol",
     "ejemplo_correcto": "'Tuit' es la forma recomendada (no 'tweet').",
     "ejemplo_incorrecto": "'Tuit' no ha sido aceptado por la RAE."},
]
TECNICAS.extend(TECNICAS_11_15)


# ══════════════════════════════════════════════════════════
# EJERCICIOS (15 ejercicios, uno por tecnica, tipo 1)
# ══════════════════════════════════════════════════════════
EJERCICIOS = {
    1: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "De que lengua proviene el castellano?",
        "opciones": [
            {"id": "a", "texto": "Del latin clasico", "correcta": False, "razon": "El castellano viene del latin vulgar, no del clasico."},
            {"id": "b", "texto": "Del latin vulgar", "correcta": True, "razon": "El latin hablado por el pueblo evoluciono al castellano."},
            {"id": "c", "texto": "Del griego", "correcta": False, "razon": "El griego es otra rama, no origino el castellano."},
        ], "justificacion_obligatoria": True, "regla": "Castellano = latin vulgar"}}],
    2: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que son las Glosas Emilianenses?",
        "opciones": [
            {"id": "a", "texto": "El primer libro impreso en castellano", "correcta": False, "razon": "La imprenta llego en 1473. Las glosas son muy anteriores."},
            {"id": "b", "texto": "Las primeras anotaciones en romance (s. X)", "correcta": True, "razon": "Son anotaciones marginales del siglo X."},
            {"id": "c", "texto": "Una gramatica del latin", "correcta": False, "razon": "Son anotaciones en romance, no gramaticas."},
        ], "justificacion_obligatoria": False, "regla": "Glosas Emilianenses: s. X"}}],
    3: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que hizo Alfonso X el Sabio?",
        "opciones": [
            {"id": "a", "texto": "Prohibio el castellano", "correcta": False, "razon": "Al contrario, lo impulso."},
            {"id": "b", "texto": "Hizo del castellano lengua oficial", "correcta": True, "razon": "Lo convirtio en lengua de la corte y administracion."},
            {"id": "c", "texto": "Escribio el Quijote", "correcta": False, "razon": "El Quijote es de Cervantes (1605)."},
        ], "justificacion_obligatoria": True, "regla": "Alfonso X: castellano oficial (s. XIII)"}}],
    4: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En que ano publico Nebrija su Gramatica castellana?",
        "opciones": [
            {"id": "a", "texto": "1492", "correcta": True, "razon": "1492 es el ano de la primera gramatica del castellano."},
            {"id": "b", "texto": "1713", "correcta": False, "razon": "1713 es la fundacion de la RAE."},
            {"id": "c", "texto": "1605", "correcta": False, "razon": "1605 es el Quijote."},
        ], "justificacion_obligatoria": False, "regla": "Nebrija 1492"}}],
    5: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que siglo se conoce como Siglo de Oro?",
        "opciones": [
            {"id": "a", "texto": "XVI-XVII", "correcta": True, "razon": "Cervantes, Lope, Quevedo: s. XVI-XVII."},
            {"id": "b", "texto": "X-XI", "correcta": False, "razon": "Siglo X-XI es la Edad Media temprana."},
            {"id": "c", "texto": "XIX", "correcta": False, "razon": "XIX es Romanticismo/Realismo."},
        ], "justificacion_obligatoria": False, "regla": "Siglo de Oro: XVI-XVII"}}],
    6: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En que ano se fundo la RAE?",
        "opciones": [
            {"id": "a", "texto": "1492", "correcta": False, "razon": "1492 es Nebrija."},
            {"id": "b", "texto": "1713", "correcta": True, "razon": "Fundacion de la RAE: 1713."},
            {"id": "c", "texto": "2005", "correcta": False, "razon": "2005 es el DPD."},
        ], "justificacion_obligatoria": False, "regla": "RAE 1713"}}],
    7: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que ortografia esta vigente hoy?",
        "opciones": [
            {"id": "a", "texto": "La de 1741", "correcta": False, "razon": "La de 1741 fue la primera, pero esta superada."},
            {"id": "b", "texto": "La de 2010", "correcta": True, "razon": "La RAE 2010 es la actual."},
            {"id": "c", "texto": "La de 1931", "correcta": False, "razon": "1931 fue la Gramatica, no la Ortografia actual."},
        ], "justificacion_obligatoria": False, "regla": "Ortografia vigente: 2010"}}],
    8: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En que ano se publico la Nueva gramatica?",
        "opciones": [
            {"id": "a", "texto": "1931", "correcta": False, "razon": "1931 es la Gramatica anterior."},
            {"id": "b", "texto": "2009", "correcta": True, "razon": "Nueva gramatica: 2009."},
            {"id": "c", "texto": "2010", "correcta": False, "razon": "2010 es la Ortografia, no la Gramatica."},
        ], "justificacion_obligatoria": False, "regla": "Nueva gramatica 2009"}}],
    9: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que obra resuelve dudas gramaticales?",
        "opciones": [
            {"id": "a", "texto": "El Quijote", "correcta": False, "razon": "Es literatura, no gramatica."},
            {"id": "b", "texto": "El Diccionario panhispanico de dudas", "correcta": True, "razon": "El DPD (2005) resuelve dudas."},
            {"id": "c", "texto": "La Ortografia 2010", "correcta": False, "razon": "Cubre ortografia, no dudas generales."},
        ], "justificacion_obligatoria": False, "regla": "DPD 2005"}}],
    10: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se consideran las variantes del espanol de America?",
        "opciones": [
            {"id": "a", "texto": "Incorrectas", "correcta": False, "razon": "Todas las variantes son validas."},
            {"id": "b", "texto": "Igual de validas que el espanol peninsular", "correcta": True, "razon": "La RAE y ASALE trabajan juntas desde 1951."},
            {"id": "c", "texto": "Solo validas en America", "correcta": False, "razon": "Su validez es global."},
        ], "justificacion_obligatoria": True, "regla": "Todas las variantes son validas"}}],
    11: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuantos hablantes nativos tiene el espanol?",
        "opciones": [
            {"id": "a", "texto": "~500 millones", "correcta": True, "razon": "~500M nativos, 21 paises oficiales."},
            {"id": "b", "texto": "~50 millones", "correcta": False, "razon": "Es mucho mas."},
            {"id": "c", "texto": "~5000 millones", "correcta": False, "razon": "Es demasiado."},
        ], "justificacion_obligatoria": False, "regla": "~500M nativos"}}],
    12: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuantas grandes reformas ortograficas ha tenido el espanol desde 1741?",
        "opciones": [
            {"id": "a", "texto": "1", "correcta": False, "razon": "Han sido varias."},
            {"id": "b", "texto": "5", "correcta": True, "razon": "1741, 1754, 1815, 1844, 2010."},
            {"id": "c", "texto": "10", "correcta": False, "razon": "Son 5."},
        ], "justificacion_obligatoria": False, "regla": "5 reformas"}}],
    13: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuando se fijo la clasificacion actual de tildes?",
        "opciones": [
            {"id": "a", "texto": "1492", "correcta": False, "razon": "1492 es Nebrija, no tildes."},
            {"id": "b", "texto": "Siglo XIX (actualizada 2010)", "correcta": True, "razon": "Clasificacion actual desde XIX, actualizada 2010."},
            {"id": "c", "texto": "2005", "correcta": False, "razon": "2005 es el DPD."},
        ], "justificacion_obligatoria": False, "regla": "Tildes: s. XIX, actualizadas 2010"}}],
    14: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que signo de puntuacion es exclusivo del espanol?",
        "opciones": [
            {"id": "a", "texto": "El punto", "correcta": False, "razon": "El punto lo usan todas las lenguas."},
            {"id": "b", "texto": "El signo de apertura '¿'", "correcta": True, "razon": "El espanol usa '¿' al inicio."},
            {"id": "c", "texto": "La coma", "correcta": False, "razon": "La coma es comun a muchas lenguas."},
        ], "justificacion_obligatoria": False, "regla": "'¿' y '¡' exclusivos del espanol"}}],
    15: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que forma recomienda la RAE para 'tweet'?",
        "opciones": [
            {"id": "a", "texto": "Tweet", "correcta": False, "razon": "Es anglicismo sin adaptar."},
            {"id": "b", "texto": "Tuit", "correcta": True, "razon": "'Tuit' es la adaptacion aceptada."},
            {"id": "c", "texto": "Twit", "correcta": False, "razon": "No es adaptacion al espanol."},
        ], "justificacion_obligatoria": True, "regla": "'Tuit' (no 'tweet')"}}],
}

# ═══ B1a: tecnicas 16-20 (clases de palabras) ═══
TECNICAS_B1A = [
    {"numero": 16, "bloque": "B", "nivel": "basico",
     "titulo": "Las 9 clases de palabras",
     "teoria": "En espanol hay 9 clases de palabras segun la Nueva gramatica (RAE 2009): sustantivo, adjetivo, determinante, pronombre, verbo, adverbio, preposicion, conjuncion e interjeccion.",
     "explicacion": "La tradicion decia 8 (sin separar determinante de adjetivo). La RAE 2009 separa el determinante como clase propia: articulos, demostrativos, posesivos, numerales, indefinidos, interrogativos y exclamativos son determinantes cuando acompanan al sustantivo.",
     "regla": "9 clases: sust, adj, det, pron, verbo, adv, prep, conj, interj",
     "ejemplo_correcto": "En espanol hay 9 clases de palabras (RAE 2009).",
     "ejemplo_incorrecto": "En espanol hay 8 clases de palabras (sin determinantes)."},
    {"numero": 17, "bloque": "B", "nivel": "basico",
     "titulo": "Sustantivo: definicion y tipos",
     "teoria": "El sustantivo (o nombre) designa personas, animales, cosas, lugares, ideas o conceptos. Varia en genero y numero.",
     "explicacion": "Es el nucleo del sintagma nominal. Puede ir con articulo, adjetivo y otros determinantes. Tipos: propio (Juan), comun (mesa), concreto (libro), abstracto (amor), contable (silla), no contable (agua), individual (arbol), colectivo (bosque).",
     "regla": "Sustantivo = nombre (persona, cosa, lugar, idea)",
     "ejemplo_correcto": "'Amor' es un sustantivo abstracto.",
     "ejemplo_incorrecto": "'Amor' es un adjetivo."},
    {"numero": 18, "bloque": "B", "nivel": "basico",
     "titulo": "Adjetivo: definicion y tipos",
     "teoria": "El adjetivo expresa cualidades o propiedades del sustantivo. Concuerda con el en genero y numero.",
     "explicacion": "Tipos: calificativo (rojo, alto) o relacional (espanol, mensual). Los calificativos admiten grados (mas alto, altisimo). Los relacionales no admiten grados (*muy mensual).",
     "regla": "Adjetivo = cualidad del sustantivo (concuerda en gen/num)",
     "ejemplo_correcto": "La casa blanca (adj. concuerda con casa).",
     "ejemplo_incorrecto": "La casa blanco (concordancia incorrecta)."},
    {"numero": 19, "bloque": "B", "nivel": "intermedio",
     "titulo": "Determinante: definicion",
     "teoria": "El determinante actualiza y precisa al sustantivo, indicando genero, numero, posesion, distancia, cantidad, etc.",
     "explicacion": "Tipos: articulos (el, un), demostrativos (este, ese), posesivos (mi, tu), numerales (dos, tercero), indefinidos (algunos, varios), interrogativos (que), exclamativos (cuanto). Es determinante cuando acompana al sustantivo; si lo sustituye, es pronombre.",
     "regla": "Determinante = actualiza al sustantivo (acompana)",
     "ejemplo_correcto": "Este libro es mio. (Este = determinante, acompana a libro).",
     "ejemplo_incorrecto": "Este libro es mio. (Este = pronombre, incorrecto)."},
    {"numero": 20, "bloque": "B", "nivel": "basico",
     "titulo": "Articulo: definido, indefinido, neutro",
     "teoria": "El articulo es un tipo de determinante que presenta al sustantivo como conocido (definido) o desconocido (indefinido).",
     "explicacion": "Definidos: el, la, los, las. Indefinidos: un, una, unos, unas. Neutro: lo (sustantiva adjetivos: lo bueno = la cosa buena). El neutro lo NO acompana a sustantivos sino que sustantiva adjetivos o adverbios.",
     "regla": "Def: el/la/los/las. Indef: un/una/unos/unas. Neutro: lo",
     "ejemplo_correcto": "Lo bueno de viajar es conocer.",
     "ejemplo_incorrecto": "El bueno de viajar es conocer. (usa masculino en vez de neutro)"},
]
TECNICAS.extend(TECNICAS_B1A)

# ═══ B1a: ejercicios 16-20 ═══
EJERCICIOS_16_20 = {
    16: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada palabra por su clase:",
        "oraciones": [
            {"texto": "el", "categoria_correcta": "determinante"},
            {"texto": "corre", "categoria_correcta": "verbo"},
            {"texto": "rapidamente", "categoria_correcta": "adverbio"},
            {"texto": "pero", "categoria_correcta": "conjuncion"}],
        "categorias": ["sustantivo","adjetivo","determinante","pronombre","verbo","adverbio","preposicion","conjuncion"]}}],
    17: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual de estas palabras es un sustantivo?",
        "opciones": [
            {"id":"a","texto":"rapido","correcta":False,"razon":"Rapido es adjetivo."},
            {"id":"b","texto":"cantar","correcta":False,"razon":"Cantar es verbo."},
            {"id":"c","texto":"tristeza","correcta":True,"razon":"Tristeza es sustantivo abstracto."},
            {"id":"d","texto":"muy","correcta":False,"razon":"Muy es adverbio."}],
        "justificacion_obligatoria": True, "regla": "Sustantivo = nombre"}}],
    18: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual de estas palabras es un adjetivo?",
        "opciones": [
            {"id":"a","texto":"libro","correcta":False,"razon":"Libro es sustantivo."},
            {"id":"b","texto":"estudia","correcta":False,"razon":"Estudia es verbo."},
            {"id":"c","texto":"hermoso","correcta":True,"razon":"Hermoso es adjetivo calificativo."},
            {"id":"d","texto":"despacio","correcta":False,"razon":"Despacio es adverbio."}],
        "justificacion_obligatoria": True, "regla": "Adjetivo = cualidad"}}],
    19: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Esta casa es mia', que clase de palabra es 'esta'?",
        "opciones": [
            {"id":"a","texto":"Determinante demostrativo","correcta":True,"razon":"Acompana al sustantivo casa, por lo tanto es determinante."},
            {"id":"b","texto":"Pronombre demostrativo","correcta":False,"razon":"Seria pronombre si sustituyera al sustantivo."},
            {"id":"c","texto":"Adjetivo","correcta":False,"razon":"El adjetivo expresa cualidad; esta no."}],
        "justificacion_obligatoria": True, "regla": "Determinante acompana al sustantivo"}}],
    20: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que articulo falta en '___ importante es aprender'?",
        "opciones": [
            {"id":"a","texto":"El","correcta":False,"razon":"El masculino no sustantiva adjetivo aqui."},
            {"id":"b","texto":"Lo","correcta":True,"razon":"Lo es el articulo neutro que sustantiva adjetivos."},
            {"id":"c","texto":"La","correcta":False,"razon":"El femenino no aplica aqui."},
            {"id":"d","texto":"Los","correcta":False,"razon":"El plural no aplica."}],
        "justificacion_obligatoria": True, "regla": "Neutro lo + adjetivo"}}],
}
EJERCICIOS.update(EJERCICIOS_16_20)

# ═══ B1b: tecnicas 21-25 (clases de palabras parte 2) ═══
TECNICAS_B1B = [
    {"numero": 21, "bloque": "B", "nivel": "intermedio",
     "titulo": "Pronombre: definicion y tipos",
     "teoria": "El pronombre sustituye al sustantivo o al sintagma nominal sin nombrarlo. Tiene significado ocasional: solo se entiende por el contexto.",
     "explicacion": "Tipos: personales (yo, tu, el, nosotros), demostrativos (este, ese, aquel), posesivos (mio, tuyo, suyo), relativos (que, quien, cual, cuyo), interrogativos (que, quien, cual, cuanto), indefinidos (alguien, nadie, algo, nada, todos).",
     "regla": "Pronombre = sustituye al sustantivo (significado ocasional)",
     "ejemplo_correcto": "Juan vino; el se sento. (el pronombre sustituye a Juan)",
     "ejemplo_incorrecto": "Juan vino; Juan se sento. (repite, no usa pronombre)"},
    {"numero": 22, "bloque": "B", "nivel": "basico",
     "titulo": "Verbo: definicion",
     "teoria": "El verbo es la palabra que expresa accion, proceso o estado. Es el nucleo del predicado y varia en persona, numero, tiempo, modo y aspecto.",
     "explicacion": "Los verbos se conjugan (excepto infinitivos, gerundios y participios que son formas no personales). En espanol hay 3 conjugaciones: -ar (amar), -er (temer), -ir (partir).",
     "regla": "Verbo = accion/proceso/estado. Nucleo del predicado",
     "ejemplo_correcto": "'Corre' expresa accion. 'Es' expresa estado.",
     "ejemplo_incorrecto": "'Corre' es un sustantivo."},
    {"numero": 23, "bloque": "B", "nivel": "intermedio",
     "titulo": "Adverbio: definicion y tipos",
     "teoria": "El adverbio modifica al verbo, al adjetivo u otro adverbio. Es invariable: no tiene genero ni numero.",
     "explicacion": "Tipos: lugar (aqui, alla, cerca), tiempo (hoy, ayer, siempre), modo (bien, mal, rapidamente, asi), cantidad (mucho, poco, muy), duda (quizas, acaso), afirmacion (si, ciertamente), negacion (no, nunca, jamas).",
     "regla": "Adverbio = modifica verbo/adjetivo/adverbio. Invariable",
     "ejemplo_correcto": "Corre rapidamente. (rapidamente modifica a corre)",
     "ejemplo_incorrecto": "Corre rapidos. (concordancia incorrecta: el adverbio no varia)"},
    {"numero": 24, "bloque": "B", "nivel": "intermedio",
     "titulo": "Preposicion: lista cerrada",
     "teoria": "La preposicion une palabras y establece relaciones de dependencia. Es una clase cerrada: hay 23 en espanol (RAE 2009).",
     "explicacion": "Las 23: a, ante, bajo, cabe, con, contra, de, desde, durante, en, entre, hacia, hasta, mediante, para, por, segun, sin, sobre, tras, versus, via. 'Cabe' y 'so' son arcaicas. Algunas son locuciones: 'a pesar de', 'en virtud de'.",
     "regla": "23 preposiciones en espanol (RAE 2009)",
     "ejemplo_correcto": "Voy a casa con Juan por el parque.",
     "ejemplo_incorrecto": "Voy casa Juan el parque. (sin preposiciones)"},
    {"numero": 25, "bloque": "B", "nivel": "intermedio",
     "titulo": "Conjuncion: tipos",
     "teoria": "La conjuncion une palabras, sintagmas u oraciones. Es invariable y no tiene significado pleno.",
     "explicacion": "Tipos: coordinantes (y, e, ni, o, u, pero, sino, mas) y subordinantes (que, si, porque, aunque, cuando, mientras, para que). Las locuciones conjuntivas: 'sin embargo', 'a pesar de que', 'ya que'.",
     "regla": "Conjuncion = une palabras/oraciones (coord. o subord.)",
     "ejemplo_correcto": "Juan y Maria vienen porque quieren.",
     "ejemplo_incorrecto": "Juan y Maria vienen ya que porque quieren. (doble conjuncion)"},
]
TECNICAS.extend(TECNICAS_B1B)

# ═══ B1b: ejercicios 21-25 ═══
EJERCICIOS_21_25 = {
    21: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Maria vino y ella trajo el pastel', que es 'ella'?",
        "opciones": [
            {"id":"a","texto":"Sustantivo","correcta":False,"razon":"Ella no nombra, sustituye."},
            {"id":"b","texto":"Pronombre personal","correcta":True,"razon":"Ella sustituye a Maria: pronombre personal femenino."},
            {"id":"c","texto":"Articulo","correcta":False,"razon":"El articulo acompana al sustantivo, no lo sustituye."},
            {"id":"d","texto":"Adjetivo","correcta":False,"razon":"El adjetivo expresa cualidad."}],
        "justificacion_obligatoria": True, "regla": "Pronombre = sustituye al sustantivo"}}],
    22: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual de estas palabras es un verbo?",
        "opciones": [
            {"id":"a","texto":"casa","correcta":False,"razon":"Casa es sustantivo."},
            {"id":"b","texto":"corre","correcta":True,"razon":"Corre es forma del verbo correr."},
            {"id":"c","texto":"rapido","correcta":False,"razon":"Rapido es adjetivo o adverbio."},
            {"id":"d","texto":"muy","correcta":False,"razon":"Muy es adverbio."}],
        "justificacion_obligatoria": True, "regla": "Verbo = accion/estado"}}],
    23: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Habla muy claro', que clase de palabra es 'muy'?",
        "opciones": [
            {"id":"a","texto":"Adjetivo","correcta":False,"razon":"Muy no expresa cualidad del sustantivo."},
            {"id":"b","texto":"Adverbio de cantidad","correcta":True,"razon":"Muy modifica al adverbio 'claro', es adverbio de cantidad."},
            {"id":"c","texto":"Determinante","correcta":False,"razon":"No acompana al sustantivo."},
            {"id":"d","texto":"Preposicion","correcta":False,"razon":"No une palabras."}],
        "justificacion_obligatoria": True, "regla": "Adverbio = modifica verbo/adj/adv"}}],
    24: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada palabra: preposicion (P) o conjuncion (C)",
        "oraciones": [
            {"texto":"con","categoria_correcta":"preposicion"},
            {"texto":"pero","categoria_correcta":"conjuncion"},
            {"texto":"para","categoria_correcta":"preposicion"},
            {"texto":"porque","categoria_correcta":"conjuncion"}],
        "categorias": ["preposicion","conjuncion"]}}],
    25: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'No vino sino que llamo', que tipo de conjuncion es 'sino'?",
        "opciones": [
            {"id":"a","texto":"Copulativa","correcta":False,"razon":"Copulativas son y, e, ni (suman)."},
            {"id":"b","texto":"Adversativa","correcta":True,"razon":"Sino opone una idea afirmativa a una negacion previa."},
            {"id":"c","texto":"Disyuntiva","correcta":False,"razon":"Disyuntivas son o, u (alternan)."},
            {"id":"d","texto":"Subordinante","correcta":False,"razon":"Sino coordina, no subordina."}],
        "justificacion_obligatoria": True, "regla": "Sino = adversativa (tras negacion)"}}],
}
EJERCICIOS.update(EJERCICIOS_21_25)

# ═══ B2a: tecnicas 26-30 (comparaciones entre clases) ═══
TECNICAS_B2A = [
    {"numero": 26, "bloque": "B", "nivel": "intermedio",
     "titulo": "Sustantivo vs adjetivo",
     "teoria": "El sustantivo tiene genero inherente (el/la) y puede ir con articulo. El adjetivo concuerda en genero y numero con el sustantivo al que modifica.",
     "explicacion": "Prueba: si puedes decir 'el X' o 'la X' y tiene genero fijo, es sustantivo. Si varia en genero segun el sustantivo (nino bueno / nina buena), es adjetivo. Algunos adjetivos se sustantivan: 'el bueno'.",
     "regla": "Sustantivo: genero inherente. Adjetivo: concuerda con sustantivo",
     "ejemplo_correcto": "El nino es alto (alto = adjetivo que concuerda con nino).",
     "ejemplo_incorrecto": "El alto es nino (ambiguedad: 'alto' sustantivado aqui)."},
    {"numero": 27, "bloque": "B", "nivel": "intermedio",
     "titulo": "Adjetivo vs adverbio",
     "teoria": "El adjetivo modifica al sustantivo (concuerda con el). El adverbio modifica al verbo, al adjetivo u otro adverbio, y es invariable.",
     "explicacion": "Prueba: si varia en genero/numero, es adjetivo. Si no varia, es adverbio. 'Corre rapido' (adverbio) vs 'nino rapido' (adjetivo). Cuidado: 'rapido' puede ser ambos segun contexto.",
     "regla": "Adjetivo: varia en gen/num. Adverbio: invariable",
     "ejemplo_correcto": "Habla claro (claro = adverbio, invariable).",
     "ejemplo_incorrecto": "Habla clara (concordancia incorrecta: el adverbio no varia)."},
    {"numero": 28, "bloque": "B", "nivel": "intermedio",
     "titulo": "Pronombre vs determinante",
     "teoria": "El determinante acompana al sustantivo (este libro). El pronombre lo sustituye (este es mio).",
     "explicacion": "La misma palabra puede ser determinante o pronombre segun su funcion. Demostrativos, posesivos, numerales, indefinidos, interrogativos y exclamativos pueden ser ambos. La clave: si hay sustantivo explicito despues, es determinante.",
     "regla": "Determinante acompana. Pronombre sustituye",
     "ejemplo_correcto": "Este libro es mio. Este es mio. (libro: determinante vs pronombre).",
     "ejemplo_incorrecto": "Este libro es mio. Este libro es mio. (doble articulo sin necesidad)."},
    {"numero": 29, "bloque": "B", "nivel": "avanzado",
     "titulo": "Locuciones (nominal, adjetiva, verbal, adverbial, prepositiva)",
     "teoria": "Una locucion es un grupo fijo de palabras que funciona como una sola clase. El significado no se deduce de las partes.",
     "explicacion": "Tipos: nominal ('media naranja'), adjetiva ('de armas tomar'), verbal ('dar gato por liebre'), adverbial ('a menu-do', 'de repente'), prepositiva ('a pesar de', 'en virtud de'), conjuntiva ('sin embargo', 'ya que').",
     "regla": "Locucion = grupo fijo con funcion de una clase",
     "ejemplo_correcto": "'A pesar de' es locucion prepositiva.",
     "ejemplo_incorrecto": "'A pesar de' es preposicion simple."},
    {"numero": 30, "bloque": "B", "nivel": "avanzado",
     "titulo": "Perifrasis verbales",
     "teoria": "Una perifrasis verbal es la union de un verbo auxiliar conjugado + una forma no personal (infinitivo, gerundio o participio) + a veces un nexo.",
     "explicacion": "Tipos: modales (poder, deber, tener que + inf), aspectuales (ir a + inf, estar + ger, llevar + part). Ej: 'voy a cantar', 'estoy cantando', 'tengo que ir'. El auxiliar pierde su significado pleno.",
     "regla": "Perifrasis: aux + (nexo) + forma no personal",
     "ejemplo_correcto": "'Voy a cantar' es perifrasis de infinitivo.",
     "ejemplo_incorrecto": "'Voy a cantar' son dos verbos independientes."},
]
TECNICAS.extend(TECNICAS_B2A)

# ═══ B2a: ejercicios 26-30 ═══
EJERCICIOS_26_30 = {
    26: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica: sustantivo (S) o adjetivo (A)",
        "oraciones": [
            {"texto":"mesa","categoria_correcta":"sustantivo"},
            {"texto":"alto","categoria_correcta":"adjetivo"},
            {"texto":"amor","categoria_correcta":"sustantivo"},
            {"texto":"hermoso","categoria_correcta":"adjetivo"}],
        "categorias": ["sustantivo","adjetivo"]}}],
    27: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Corre rapido', que es 'rapido'?",
        "opciones": [
            {"id":"a","texto":"Adjetivo","correcta":False,"razon":"No concuerda con ningun sustantivo."},
            {"id":"b","texto":"Adverbio de modo","correcta":True,"razon":"Modifica al verbo 'corre', invariable."},
            {"id":"c","texto":"Sustantivo","correcta":False,"razon":"No nombra entidad."}],
        "justificacion_obligatoria": True, "regla": "Adverbio modifica al verbo"}}],
    28: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Este libro es mio', que es 'este'?",
        "opciones": [
            {"id":"a","texto":"Pronombre","correcta":False,"razon":"Acompana a 'libro', por lo tanto es determinante."},
            {"id":"b","texto":"Determinante demostrativo","correcta":True,"razon":"Acompana al sustantivo 'libro'."},
            {"id":"c","texto":"Adjetivo","correcta":False,"razon":"No expresa cualidad."}],
        "justificacion_obligatoria": True, "regla": "Determinante acompaña"}}],
    29: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de locucion es 'a pesar de'?",
        "opciones": [
            {"id":"a","texto":"Nominal","correcta":False,"razon":"No funciona como sustantivo."},
            {"id":"b","texto":"Prepositiva","correcta":True,"razon":"Funciona como preposicion: 'a pesar de la lluvia'."},
            {"id":"c","texto":"Verbal","correcta":False,"razon":"No funciona como verbo."},
            {"id":"d","texto":"Conjuntiva","correcta":False,"razon":"No une oraciones."}],
        "justificacion_obligatoria": True, "regla": "Locucion prepositiva"}}],
    30: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que perifrasis es 'voy a cantar'?",
        "opciones": [
            {"id":"a","texto":"Aspectual ingresiva (ir a + inf)","correcta":True,"razon":"Ir a + infinitivo marca inicio de accion."},
            {"id":"b","texto":"Modal de obligacion","correcta":False,"razon":"No expresa obligacion."},
            {"id":"c","texto":"Dos verbos independientes","correcta":False,"razon":"Es una unidad."}],
        "justificacion_obligatoria": True, "regla": "Ir a + inf = perifrasis ingresiva"}}],
}
EJERCICIOS.update(EJERCICIOS_26_30)

# ═══ B2b: tecnicas 31-35 (morfologia) ═══
TECNICAS_B2B = [
    {"numero": 31, "bloque": "B", "nivel": "intermedio",
     "titulo": "Palabras variables vs invariables",
     "teoria": "Las palabras variables cambian de forma segun genero, numero, tiempo o modo. Las invariables no cambian nunca.",
     "explicacion": "Variables: sustantivo (nino/nina/ninos/ninas), adjetivo (alto/alta), verbo (canto/cantas/canta), determinante (este/esta), pronombre personal (el/ella). Invariables: adverbio (hoy, siempre), preposicion (de, con), conjuncion (y, pero), interjeccion (ay, oh).",
     "regla": "Variables: sust/adj/verbo/det/pron. Invariables: adv/prep/conj/interj",
     "ejemplo_correcto": "'Alto' varia (alta, altos, altas): adjetivo.",
     "ejemplo_incorrecto": "'Hoy' varia en genero."},
    {"numero": 32, "bloque": "B", "nivel": "avanzado",
     "titulo": "Palabras lexicas vs gramaticales",
     "teoria": "Las palabras lexicas (o de contenido) tienen significado pleno. Las gramaticales (o funcionales) solo tienen significado gramatical.",
     "explicacion": "Lexicas: sustantivo, adjetivo, verbo, adverbio. Gramaticales: determinante, pronombre, preposicion, conjuncion. Algunas son ambiguas (adverbio puede ser lexico: 'rapidamente'; o gramatical: 'muy').",
     "regla": "Lexicas: contenido. Gramaticales: funcion",
     "ejemplo_correcto": "'Casa' es palabra lexica (tiene contenido).",
     "ejemplo_incorrecto": "'De' es palabra lexica con contenido pleno."},
    {"numero": 33, "bloque": "B", "nivel": "avanzado",
     "titulo": "Palabras simples, derivadas, compuestas",
     "teoria": "Segun su estructura morfologica: simples (un solo lexema), derivadas (lexema + afijos), compuestas (dos o mas lexemas).",
     "explicacion": "Simples: pan, sol, mar. Derivadas: pan-adero, sol-azo, mar-ino. Compuestas: sacacorchos, abrelatas, paraguas. Las compuestas pueden ser propias (dos lexemas: sacacorchos) o sintagmaticas (sustantivo + preposicion: ojo de buey).",
     "regla": "Simple (1 lexema). Derivada (lexema + afijo). Compuesta (2+ lexemas)",
     "ejemplo_correcto": "'Paraguas' es palabra compuesta.",
     "ejemplo_incorrecto": "'Paraguas' es palabra simple."},
    {"numero": 34, "bloque": "B", "nivel": "avanzado",
     "titulo": "Patrimoniales vs cultismos",
     "teoria": "Las palabras patrimoniales evolucionaron del latin al castellano. Los cultismos se tomaron del latin directamente, sin evolucion, en epocas posteriores.",
     "explicacion": "Ejemplos: 'hacer' (patrimonial de facere), 'factible' (cultismo de factibilis). 'Ojo' (patrimonial de oculum), 'ocular' (cultismo). A veces conviven las dos formas: 'hacer' / 'factible'.",
     "regla": "Patrimonial: evoluciono del latin. Cultismo: tomada despues sin evolucion",
     "ejemplo_correcto": "'Ojo' es patrimonial; 'ocular' es cultismo.",
     "ejemplo_incorrecto": "'Ojo' y 'ocular' son ambas patrimoniales."},
    {"numero": 35, "bloque": "B", "nivel": "avanzado",
     "titulo": "Derivacion y composicion",
     "teoria": "La derivacion anade afijos a un lexema (prefijos, sufijos, interfijos). La composicion une dos o mas lexemas.",
     "explicacion": "Prefijos: re-, des-, in-, pre-, sub-. Sufijos: -cion, -miento, -dor, -ito, -on. Interfijos: -ec- (piececito), -it- (cafetera). Composicion: saca + corchos, abre + latas. Parasintesis: prefijo + lexema + sufijo en conjunto: des-templ-ado.",
     "regla": "Derivacion = afijos. Composicion = 2+ lexemas. Parasintesis = afijos + composicion",
     "ejemplo_correcto": "'Des-templ-ado' es parasintetica.",
     "ejemplo_incorrecto": "'Des-templ-ado' es solo derivada."},
]
TECNICAS.extend(TECNICAS_B2B)

# ═══ B2b: ejercicios 31-35 ═══
EJERCICIOS_31_35 = {
    31: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica: variable (V) o invariable (I)",
        "oraciones": [
            {"texto":"alto","categoria_correcta":"variable"},
            {"texto":"hoy","categoria_correcta":"invariable"},
            {"texto":"cantar","categoria_correcta":"variable"},
            {"texto":"pero","categoria_correcta":"invariable"}],
        "categorias": ["variable","invariable"]}}],
    32: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica: lexica (L) o gramatical (G)",
        "oraciones": [
            {"texto":"casa","categoria_correcta":"lexica"},
            {"texto":"de","categoria_correcta":"gramatical"},
            {"texto":"correr","categoria_correcta":"lexica"},
            {"texto":"pero","categoria_correcta":"gramatical"}],
        "categorias": ["lexica","gramatical"]}}],
    33: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de palabra es 'sacacorchos'?",
        "opciones": [
            {"id":"a","texto":"Simple","correcta":False,"razon":"Tiene dos lexemas (saca + corchos)."},
            {"id":"b","texto":"Compuesta","correcta":True,"razon":"Union de dos lexemas."},
            {"id":"c","texto":"Derivada","correcta":False,"razon":"No anade sufijo ni prefijo a un solo lexema."}],
        "justificacion_obligatoria": True, "regla": "Compuesta = 2+ lexemas"}}],
    34: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que relacion hay entre 'ojo' y 'ocular'?",
        "opciones": [
            {"id":"a","texto":"Ambas son patrimoniales","correcta":False,"razon":"'Ocular' no evoluciono, es cultismo."},
            {"id":"b","texto":"'Ojo' es patrimonial, 'ocular' es cultismo","correcta":True,"razon":"'Ojo' evoluciono del latin oculum; 'ocular' se tomo despues."},
            {"id":"c","texto":"Ambas son cultismos","correcta":False,"razon":"'Ojo' evoluciono."}],
        "justificacion_obligatoria": True, "regla": "Patrimonial + cultismo"}}],
    35: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de formacion es 'des-templ-ado'?",
        "opciones": [
            {"id":"a","texto":"Derivacion simple","correcta":False,"razon":"Tiene prefijo Y sufijo a la vez."},
            {"id":"b","texto":"Parasintetica","correcta":True,"razon":"Prefijo + lexema + sufijo en conjunto."},
            {"id":"c","texto":"Composicion","correcta":False,"razon":"Solo hay un lexema (templ-)."}],
        "justificacion_obligatoria": True, "regla": "Parasintesis = pref + lexema + suf"}}],
}
EJERCICIOS.update(EJERCICIOS_31_35)

# ═══ C1: tecnicas 36-40 (genero y numero del sustantivo) ═══
TECNICAS_C1 = [
    {"numero": 36, "bloque": "C", "nivel": "basico",
     "titulo": "Genero masculino/femenino",
     "teoria": "Todo sustantivo tiene genero gramatical: masculino (el) o femenino (la). No siempre coincide con el sexo.",
     "explicacion": "Reglas generales: -o/-aje/-or suelen ser masculinos (libro, viaje, amor). -a/-cion/-dad/-tad/-umbre suelen ser femeninos (casa, cancion, ciudad, virtud, costumbre). Excepciones: 'dia', 'mapa', 'planeta' son masculinos; 'mano', 'foto' son femeninos.",
     "regla": "Masculino: -o/-aje/-or. Femenino: -a/-cion/-dad/-tad/-umbre",
     "ejemplo_correcto": "El problema, la solucion, el viaje, la ciudad.",
     "ejemplo_incorrecto": "La problema, el solucion, la viaje, el ciudad."},
    {"numero": 37, "bloque": "C", "nivel": "intermedio",
     "titulo": "Genero ambiguo (el/la)",
     "teoria": "Algunos sustantivos admiten los dos generos con el mismo significado o con significados distintos.",
     "explicacion": "Mismo significado: el/la mar, el/la azucar, el/la arte (plural: las artes). Significado distinto: el cometa (astro) / la cometa (juguete); el capital (dinero) / la capital (ciudad); el cura (sacerdote) / la cura (tratamiento).",
     "regla": "Ambiguos: mismo significado (mar) o distinto (capital)",
     "ejemplo_correcto": "El capital (dinero) / la capital (ciudad).",
     "ejemplo_incorrecto": "La capital (dinero) / el capital (ciudad)."},
    {"numero": 38, "bloque": "C", "nivel": "intermedio",
     "titulo": "Genero epiceno",
     "teoria": "Sustantivos epicenos designan animales o personas sin distinguir sexo. El genero gramatical es fijo.",
     "explicacion": "Ejemplos: la persona, la victima, la jirafa, el puma, el personaje. Para distinguir sexo se anade 'macho/hembra' o 'hombre/mujer': 'la victima (hombre)' o 'la victima (mujer)'.",
     "regla": "Epiceno: genero fijo, sin distinguir sexo",
     "ejemplo_correcto": "La victima era un hombre. (femenino gramatical, sexo masculino)",
     "ejemplo_incorrecto": "El victima era un hombre. (cambio de genero incorrecto)"},
    {"numero": 39, "bloque": "C", "nivel": "basico",
     "titulo": "Genero y numero",
     "teoria": "El sustantivo tiene dos accidentes gramaticales: genero (masculino/femenino) y numero (singular/plural).",
     "explicacion": "El genero es inherente (no cambia), salvo en sustantivos que admiten los dos (el/la mar). El numero varia: singular (una entidad) vs plural (varias). Artículo y adjetivo concuerdan con el sustantivo en ambos.",
     "regla": "Sustantivo: genero (fijo) + numero (variable)",
     "ejemplo_correcto": "El nino alto / la nina alta / los ninos altos / las ninas altas.",
     "ejemplo_incorrecto": "La nino alto (concordancia incorrecta)."},
    {"numero": 40, "bloque": "C", "nivel": "basico",
     "titulo": "Plural regular (-s, -es)",
     "teoria": "El plural regular se forma anadiendo -s o -es segun la terminacion del singular.",
     "explicacion": "Regla: si termina en vocal atona o -a/-e/-o, se anade -s (casa/casas, libro/libros). Si termina en consonante o vocal tonica (a, e, o tonicas), se anade -es (arbol/arboles, rubi/rubies). Excepcion: palabras terminadas en -s atona no cambian (el/los lunes).",
     "regla": "Vocal atona: +s. Consonante o vocal tonica: +es",
     "ejemplo_correcto": "Casa/casas, arbol/arboles, rubi/rubies, lunes/lunes.",
     "ejemplo_incorrecto": "Arbol/arbols, rubi/rubis."},
]
TECNICAS.extend(TECNICAS_C1)

# ═══ C1: ejercicios 36-40 ═══
EJERCICIOS_36_40 = {
    36: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada sustantivo por genero:",
        "oraciones": [
            {"texto":"problema","categoria_correcta":"masculino"},
            {"texto":"solucion","categoria_correcta":"femenino"},
            {"texto":"viaje","categoria_correcta":"masculino"},
            {"texto":"ciudad","categoria_correcta":"femenino"}],
        "categorias": ["masculino","femenino"]}}],
    37: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que significa 'la capital' vs 'el capital'?",
        "opciones": [
            {"id":"a","texto":"Ambos = ciudad","correcta":False,"razon":"'El capital' es dinero."},
            {"id":"b","texto":"La capital = ciudad; el capital = dinero","correcta":True,"razon":"Genero distingue significado."},
            {"id":"c","texto":"Ambos = dinero","correcta":False,"razon":"'La capital' es ciudad."}],
        "justificacion_obligatoria": True, "regla": "Capital: fem=ciudad, masc=dinero"}}],
    38: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es 'la victima'?",
        "opciones": [
            {"id":"a","texto":"Epiceno (genero fijo)","correcta":True,"razon":"Epiceno: femenino gramatical sin distinguir sexo."},
            {"id":"b","texto":"Ambiguo","correcta":False,"razon":"No admite los dos generos."},
            {"id":"c","texto":"Comun (el/la victima)","correcta":False,"razon":"'Comun' es otra categoria."}],
        "justificacion_obligatoria": True, "regla": "Epiceno: genero fijo"}}],
    39: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que accidentes tiene el sustantivo?",
        "opciones": [
            {"id":"a","texto":"Solo numero","correcta":False,"razon":"Tambien tiene genero."},
            {"id":"b","texto":"Genero y numero","correcta":True,"razon":"Son sus dos accidentes gramaticales."},
            {"id":"c","texto":"Solo genero","correcta":False,"razon":"Tambien varia en numero."}],
        "justificacion_obligatoria": True, "regla": "Genero + numero"}}],
    40: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el plural de 'arbol'?",
        "opciones": [
            {"id":"a","texto":"Arbols","correcta":False,"razon":"Termina en consonante: +es."},
            {"id":"b","texto":"Arboles","correcta":True,"razon":"Consonante final: se anade -es."},
            {"id":"c","texto":"Arbolos","correcta":False,"razon":"No es la regla."}],
        "justificacion_obligatoria": True, "regla": "Consonante: +es"}}],
}
EJERCICIOS.update(EJERCICIOS_36_40)

# ═══ C2: tecnicas 41-45 (plural irregular + tipos de sustantivo) ═══
TECNICAS_C2 = [
    {"numero": 41, "bloque": "C", "nivel": "intermedio",
     "titulo": "Plural irregular (el/la, -z -> -ces)",
     "teoria": "Algunos plurales no siguen la regla general y presentan formas irregulares.",
     "explicacion": "Irregulares frecuentes: -z -> -ces (luz/luces, pez/peces). -s atona no cambia (lunes/lunes). Sustantivos que solo existen en plural: las gafas, las tijeras, los pantalones. Cambio de acento: caracter/caracteres, regimen/regimenes.",
     "regla": "-z -> -ces. -s atona: sin cambio. Cambio de acento posible",
     "ejemplo_correcto": "Luz/luces, lunes/lunes, caracter/caracteres.",
     "ejemplo_incorrecto": "Luz/luzes, lunes/luness, caracter/caracters."},
    {"numero": 42, "bloque": "C", "nivel": "basico",
     "titulo": "Sustantivos colectivos",
     "teoria": "Un sustantivo colectivo designa en singular un conjunto de entidades.",
     "explicacion": "Ejemplos: equipo (conjunto de jugadores), rebaño (conjunto de ovejas), bosque (conjunto de arboles), enjambre (conjunto de abejas), gentio (conjunto de personas). Concuerdan en singular aunque designen plural: 'el equipo gano'.",
     "regla": "Colectivo: singular que designa conjunto",
     "ejemplo_correcto": "El equipo gano el partido.",
     "ejemplo_incorrecto": "El equipo ganaron el partido."},
    {"numero": 43, "bloque": "C", "nivel": "basico",
     "titulo": "Sustantivos propios vs comunes",
     "teoria": "Los propios designan una entidad unica (Juan, Madrid, Ebro). Los comunes designan clases (hombre, ciudad, rio).",
     "explicacion": "Los propios se escriben con mayuscula inicial. Pueden llevar articulo (el Madrid de los Austrias) o no (Juan viene). Los comunes llevan articulo normalmente.",
     "regla": "Propio: entidad unica, mayuscula. Comun: clase, minuscula",
     "ejemplo_correcto": "Madrid (propio) es una ciudad (comun).",
     "ejemplo_incorrecto": "madrid es una Ciudad."},
    {"numero": 44, "bloque": "C", "nivel": "intermedio",
     "titulo": "Sustantivos abstractos vs concretos",
     "teoria": "Los concretos designan entidades perceptibles por los sentidos. Los abstractos designan conceptos, ideas o sentimientos.",
     "explicacion": "Concretos: mesa, arbol, perro, casa. Abstractos: amor, libertad, justicia, belleza, tiempo. Los abstractos no pueden ir con 'muchos/muchas' del mismo modo.",
     "regla": "Concreto: perceptible. Abstracto: concepto",
     "ejemplo_correcto": "'Mesa' es concreto; 'amor' es abstracto.",
     "ejemplo_incorrecto": "'Mesa' es abstracto; 'amor' es concreto."},
    {"numero": 45, "bloque": "C", "nivel": "intermedio",
     "titulo": "Sustantivos contables vs no contables",
     "teoria": "Los contables se pueden contar (un libro, dos libros). Los no contables (o de masa) se miden pero no se cuentan (agua, arena, azucar).",
     "explicacion": "Contables: libro, mesa, persona. No contables: agua, arena, azucar, harina. Los no contables no admiten plural normal, pero pueden admitir 'mucho/mucha'. Algunos son ambos segun contexto: 'un cafe' (taza) vs 'cafe' (sustancia).",
     "regla": "Contable: se cuenta. No contable: se mide",
     "ejemplo_correcto": "Dos libros (contable) / mucha agua (no contable).",
     "ejemplo_incorrecto": "Dos aguas (incorrecto como masa)."},
]
TECNICAS.extend(TECNICAS_C2)

# ═══ C2: ejercicios 41-45 ═══
EJERCICIOS_41_45 = {
    41: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el plural de 'luz'?",
        "opciones": [
            {"id":"a","texto":"Luzes","correcta":False,"razon":"-z -> -ces."},
            {"id":"b","texto":"Luces","correcta":True,"razon":"Regla: -z -> -ces."},
            {"id":"c","texto":"Luzs","correcta":False,"razon":"No es la regla."}],
        "justificacion_obligatoria": True, "regla": "-z -> -ces"}}],
    42: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es 'rebaño'?",
        "opciones": [
            {"id":"a","texto":"Individual","correcta":False,"razon":"No designa un individuo."},
            {"id":"b","texto":"Colectivo","correcta":True,"razon":"Designa conjunto de ovejas."},
            {"id":"c","texto":"Abstracto","correcta":False,"razon":"Es concreto."}],
        "justificacion_obligatoria": True, "regla": "Colectivo: singular=conjunto"}}],
    43: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica: propio (P) o comun (C)",
        "oraciones": [
            {"texto":"Madrid","categoria_correcta":"propio"},
            {"texto":"ciudad","categoria_correcta":"comun"},
            {"texto":"Ebro","categoria_correcta":"propio"},
            {"texto":"rio","categoria_correcta":"comun"}],
        "categorias": ["propio","comun"]}}],
    44: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica: concreto (C) o abstracto (A)",
        "oraciones": [
            {"texto":"mesa","categoria_correcta":"concreto"},
            {"texto":"amor","categoria_correcta":"abstracto"},
            {"texto":"perro","categoria_correcta":"concreto"},
            {"texto":"libertad","categoria_correcta":"abstracto"}],
        "categorias": ["concreto","abstracto"]}}],
    45: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de sustantivo es 'agua'?",
        "opciones": [
            {"id":"a","texto":"Contable","correcta":False,"razon":"No se cuenta (dos aguas suena raro)."},
            {"id":"b","texto":"No contable (de masa)","correcta":True,"razon":"Se mide, no se cuenta."},
            {"id":"c","texto":"Colectivo","correcta":False,"razon":"No designa conjunto."}],
        "justificacion_obligatoria": True, "regla": "No contable: se mide"}}],
}
EJERCICIOS.update(EJERCICIOS_41_45)

# ═══ C3: tecnicas 46-50 (individual/colectivo + sufijos) ═══
TECNICAS_C3 = [
    {"numero": 46, "bloque": "C", "nivel": "intermedio",
     "titulo": "Sustantivos individuales vs colectivos",
     "teoria": "El individual designa un solo ser (oveja, arbol, estrella). El colectivo designa un conjunto (rebaño, bosque, constelacion).",
     "explicacion": "Parejas: oveja/rebaño, arbol/bosque, estrella/constelacion, pez/banco, soldado/ejercito, persona/gente. El colectivo no es lo mismo que plural: 'rebaño' es singular pero designa conjunto.",
     "regla": "Individual: uno. Colectivo: conjunto (aunque sea singular)",
     "ejemplo_correcto": "Una oveja (individual) / un rebaño (colectivo).",
     "ejemplo_incorrecto": "Un rebaño es plural."},
    {"numero": 47, "bloque": "C", "nivel": "basico",
     "titulo": "Diminutivos (-ito, -illo, -ico)",
     "teoria": "Los diminutivos expresan tamano pequeno, afecto o cortesia. Los sufijos mas comunes son -ito, -illo, -ico.",
     "explicacion": "-ito (casita, perrito) es el mas frecuente y afectivo. -illo (florecilla, rincon) es mas neutro o despectivo. -ico (momentico, gatico) es regional (Caribe, Colombia). Tambien -in (jardincito), -uelo (pequenuelo).",
     "regla": "Diminutivos: -ito, -illo, -ico, -in",
     "ejemplo_correcto": "Casita, florecilla, momentico.",
     "ejemplo_incorrecto": "Casota (es aumentativo, no diminutivo)."},
    {"numero": 48, "bloque": "C", "nivel": "basico",
     "titulo": "Aumentativos (-on, -azo, -ote)",
     "teoria": "Los aumentativos expresan tamano grande, intensidad o, a veces, desprecio.",
     "explicacion": "-on (caseron, mujeron, arbolon): aumentativo grande. -azo (portazo, golazo, exitazo): accion brusca o gran impacto. -ote (grandote, gordote): tamano o desprecio.",
     "regla": "Aumentativos: -on, -azo, -ote",
     "ejemplo_correcto": "Caserón, portazo, grandote.",
     "ejemplo_incorrecto": "Casita (es diminutivo)."},
    {"numero": 49, "bloque": "C", "nivel": "intermedio",
     "titulo": "Despectivos (-ucho, -astro, -zuelo)",
     "teoria": "Los despectivos expresan desprecio, inferioridad o mala calidad.",
     "explicacion": "-ucho: casucha, periodicucho, medicucho. -astro: poetastro, politicastro, medicastro. -zuelo: ladronzuelo, hombrezuelo. Se aplican sobre todo a personas y oficios con intencion despectiva.",
     "regla": "Despectivos: -ucho, -astro, -zuelo",
     "ejemplo_correcto": "Casucha, poetastro, ladronzuelo.",
     "ejemplo_incorrecto": "Casita (es diminutivo afectivo, no despectivo)."},
    {"numero": 50, "bloque": "C", "nivel": "avanzado",
     "titulo": "Derivacion nominal (sufijos)",
     "teoria": "La derivacion nominal forma sustantivos a partir de verbos o adjetivos mediante sufijos.",
     "explicacion": "Sufijos nominalizadores: -cion (cantar -> cancion), -miento (sentir -> sentimiento), -dor (trabajar -> trabajador), -encia (existir -> existencia), -idad (feliz -> felicidad), -ez (noble -> nobleza), -ismo (social -> socialismo).",
     "regla": "Derivacion nominal: -cion, -miento, -dor, -encia, -idad, -ez, -ismo",
     "ejemplo_correcto": "Cantar -> cancion (sufijo -cion).",
     "ejemplo_incorrecto": "Cantar -> cantar (no se deriva, sigue siendo verbo)."},
]
TECNICAS.extend(TECNICAS_C3)

# ═══ C3: ejercicios 46-50 ═══
EJERCICIOS_46_50 = {
    46: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica: individual (I) o colectivo (C)",
        "oraciones": [
            {"texto":"oveja","categoria_correcta":"individual"},
            {"texto":"rebaño","categoria_correcta":"colectivo"},
            {"texto":"arbol","categoria_correcta":"individual"},
            {"texto":"bosque","categoria_correcta":"colectivo"}],
        "categorias": ["individual","colectivo"]}}],
    47: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que expresa 'casita'?",
        "opciones": [
            {"id":"a","texto":"Aumentativo","correcta":False,"razon":"-ita es diminutivo."},
            {"id":"b","texto":"Diminutivo","correcta":True,"razon":"-ita expresa tamano pequeno o afecto."},
            {"id":"c","texto":"Despectivo","correcta":False,"razon":"-ita es afectivo."}],
        "justificacion_obligatoria": True, "regla": "Diminutivo: -ito"}}],
    48: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que expresa 'portazo'?",
        "opciones": [
            {"id":"a","texto":"Aumentativo de accion brusca","correcta":True,"razon":"-azo marca accion brusca o gran impacto."},
            {"id":"b","texto":"Diminutivo","correcta":False,"razon":"-azo es aumentativo."},
            {"id":"c","texto":"Despectivo","correcta":False,"razon":"No es despectivo."}],
        "justificacion_obligatoria": True, "regla": "Aumentativo: -azo"}}],
    49: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que expresa 'poetastro'?",
        "opciones": [
            {"id":"a","texto":"Diminutivo afectivo","correcta":False,"razon":"-astro es despectivo."},
            {"id":"b","texto":"Despectivo","correcta":True,"razon":"-astro indica desprecio."},
            {"id":"c","texto":"Aumentativo","correcta":False,"razon":"No expresa tamano grande."}],
        "justificacion_obligatoria": True, "regla": "Despectivo: -astro"}}],
    50: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el sustantivo derivado de 'cantar'?",
        "opciones": [
            {"id":"a","texto":"Cantante","correcta":True,"razon":"-ante forma sustantivo de agente."},
            {"id":"b","texto":"Cantando","correcta":False,"razon":"Es gerundio, no sustantivo."},
            {"id":"c","texto":"Cantado","correcta":False,"razon":"Es participio."}],
        "justificacion_obligatoria": True, "regla": "Derivacion nominal: -ante/-cion"}}],
}
EJERCICIOS.update(EJERCICIOS_46_50)

# ═══ D1: tecnicas 51-55 (grados y concordancia del adjetivo) ═══
TECNICAS_D1 = [
    {"numero": 51, "bloque": "D", "nivel": "basico",
     "titulo": "Grados del adjetivo: positivo",
     "teoria": "El grado positivo expresa la cualidad sin comparacion ni intensificacion. Es la forma base del adjetivo.",
     "explicacion": "Ejemplos: alto, bajo, bueno, malo. 'Juan es alto' expresa la cualidad en grado positivo, sin comparar ni intensificar. Es la forma que aparece en el diccionario.",
     "regla": "Positivo: cualidad sin comparacion",
     "ejemplo_correcto": "Juan es alto (positivo).",
     "ejemplo_incorrecto": "Juan es mas alto (es comparativo, no positivo)."},
    {"numero": 52, "bloque": "D", "nivel": "intermedio",
     "titulo": "Comparativo (mas... que, tan... como)",
     "teoria": "El grado comparativo establece una comparacion entre dos entidades. Hay tres tipos: superioridad, igualdad e inferioridad.",
     "explicacion": "Superioridad: mas + adj + que (Juan es mas alto que Pedro). Igualdad: tan + adj + como (Juan es tan alto como Pedro). Inferioridad: menos + adj + que (Juan es menos alto que Pedro). Irregulares: mejor/peor (no 'mas bueno/malo').",
     "regla": "Comparativo: mas/menos/tan... que/como. Irreg: mejor, peor",
     "ejemplo_correcto": "Juan es mas alto que Pedro. Maria es mejor que yo.",
     "ejemplo_incorrecto": "Juan es mas alto de Pedro. (preposicion incorrecta)"},
    {"numero": 53, "bloque": "D", "nivel": "intermedio",
     "titulo": "Superlativo (-isimo, muy, el mas)",
     "teoria": "El grado superlativo expresa la cualidad en su grado maximo. Hay dos tipos: absoluto (sin comparacion) y relativo (comparado con un grupo).",
     "explicacion": "Absoluto: muy + adj (muy alto) o adj + -isimo (altisimo). Relativo: el/la/los/las mas + adj + de (el mas alto de la clase). Irregulares: optimo (muy bueno), pesimo (muy malo), maximo (muy grande), minimo (muy pequeno).",
     "regla": "Superlativo: absoluto (muy/-isimo) o relativo (el mas... de)",
     "ejemplo_correcto": "Altisimo, muy alto, el mas alto de todos.",
     "ejemplo_incorrecto": "Mas altisimo (incorrecto: duplica superlativo)."},
    {"numero": 54, "bloque": "D", "nivel": "basico",
     "titulo": "Concordancia adjetivo-sustantivo",
     "teoria": "El adjetivo concuerda con el sustantivo en genero y numero, aunque el sustantivo sea colectivo o haya varios sustantivos.",
     "explicacion": "Regla general: mismo genero y numero. Excepciones: si varios sustantivos de distinto genero, adjetivo en masculino plural (Juan y Maria son altos). Si un sustantivo es de genero ambiguo, adjetivo segun el articulo: 'el agua fria' (femenino interno, articulo el).",
     "regla": "Concordancia gen/num. Varios de distinto genero -> masc plural",
     "ejemplo_correcto": "La casa blanca, el libro rojo, Juan y Maria son altos.",
     "ejemplo_incorrecto": "La casa blanco, Juan y Maria son altas."},
    {"numero": 55, "bloque": "D", "nivel": "intermedio",
     "titulo": "Adjetivos de una vs dos terminaciones",
     "teoria": "Los adjetivos de una terminacion no varian en genero (solo en numero). Los de dos terminaciones tienen forma masculina y femenina.",
     "explicacion": "Una terminacion: feliz (feliz/feliz), fuerte (fuerte/fuerte), grande (grande/grande), interesante (interesante/interesante). Dos terminaciones: alto/alta, bueno/buena, pequeno/pequena, rojo/roja. Suelen terminar en -o los de dos terminaciones.",
     "regla": "1 terminacion: no varia en genero. 2 terminaciones: masc/fem",
     "ejemplo_correcto": "Nino feliz / nina feliz (una terminacion). Nino alto / nina alta (dos terminaciones).",
     "ejemplo_incorrecto": "Nino feliça (no existe forma femenina de feliz)."},
]
TECNICAS.extend(TECNICAS_D1)

# ═══ D1: ejercicios 51-55 ═══
EJERCICIOS_51_55 = {
    51: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Maria es inteligente', que grado tiene 'inteligente'?",
        "opciones": [
            {"id":"a","texto":"Positivo","correcta":True,"razon":"Expresa la cualidad sin comparar ni intensificar."},
            {"id":"b","texto":"Comparativo","correcta":False,"razon":"No hay comparacion."},
            {"id":"c","texto":"Superlativo","correcta":False,"razon":"No es grado maximo."}],
        "justificacion_obligatoria": True, "regla": "Positivo = sin comparacion"}}],
    52: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de comparativo es 'Juan es tan alto como Pedro'?",
        "opciones": [
            {"id":"a","texto":"Superioridad","correcta":False,"razon":"No expresa mayor altura."},
            {"id":"b","texto":"Igualdad","correcta":True,"razon":"'Tan... como' expresa igualdad."},
            {"id":"c","texto":"Inferioridad","correcta":False,"razon":"No expresa menor altura."}],
        "justificacion_obligatoria": True, "regla": "Tan... como = igualdad"}}],
    53: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que superlativo corresponde a 'muy bueno'?",
        "opciones": [
            {"id":"a","texto":"Buenisimo","correcta":False,"razon":"Es valido pero coloquial, no la forma culta."},
            {"id":"b","texto":"Optimo","correcta":True,"razon":"Optimo = muy bueno (superlativo irregular)."},
            {"id":"c","texto":"Mas bueno","correcta":False,"razon":"No es superlativo."}],
        "justificacion_obligatoria": True, "regla": "Irregular: optimo = muy bueno"}}],
    54: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan y Maria son ___', que forma del adjetivo 'alto' es correcta?",
        "opciones": [
            {"id":"a","texto":"Altas","correcta":False,"razon":"Juan es masculino: no todo el grupo es femenino."},
            {"id":"b","texto":"Altos","correcta":True,"razon":"Generos mixtos: masculino plural."},
            {"id":"c","texto":"Alto","correcta":False,"razon":"Falta plural."}],
        "justificacion_obligatoria": True, "regla": "Generos mixtos: masc plural"}}],
    55: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada adjetivo: 1 terminacion (U) o 2 terminaciones (D)",
        "oraciones": [
            {"texto":"feliz","categoria_correcta":"1 terminacion"},
            {"texto":"alto","categoria_correcta":"2 terminaciones"},
            {"texto":"fuerte","categoria_correcta":"1 terminacion"},
            {"texto":"pequeno","categoria_correcta":"2 terminaciones"}],
        "categorias": ["1 terminacion","2 terminaciones"]}}],
}
EJERCICIOS.update(EJERCICIOS_51_55)

# ═══ D2: tecnicas 56-60 (tipos de adjetivo) ═══
TECNICAS_D2 = [
    {"numero": 56, "bloque": "D", "nivel": "avanzado",
     "titulo": "Adjetivo explicativo vs especificativo",
     "teoria": "El adjetivo explicativo anade informacion no esencial (va entre comas). El especificativo restringe el significado del sustantivo (sin coma).",
     "explicacion": "Explicativo: 'Los alumnos, cansados, se fueron' (todos estaban cansados). Especificativo: 'Los alumnos cansados se fueron' (solo los cansados). La coma cambia el significado.",
     "regla": "Explicativo: coma, no esencial. Especificativo: sin coma, restringe",
     "ejemplo_correcto": "Los alumnos, cansados, se fueron. / Los alumnos cansados se fueron.",
     "ejemplo_incorrecto": "Los alumnos cansados, se fueron. (coma mal puesta)"},
    {"numero": 57, "bloque": "D", "nivel": "intermedio",
     "titulo": "Apocope (buen, gran, primer)",
     "teoria": "La apocope es la perdida de la vocal final de un adjetivo ante un sustantivo masculino singular.",
     "explicacion": "Apocopados: bueno -> buen (buen dia), malo -> mal (mal tiempo), primero -> primer (primer piso), tercero -> tercer (tercer lugar), grande -> gran (gran hombre), santo -> san (san Juan). Ante sustantivo femenino no se apocopa: buena dia, primera vez.",
     "regla": "Apocope: ante sustantivo masc sing. buen, mal, primer, gran",
     "ejemplo_correcto": "Buen dia, primer piso, gran hombre.",
     "ejemplo_incorrecto": "Buen semana (femenino: buena semana)."},
    {"numero": 58, "bloque": "D", "nivel": "avanzado",
     "titulo": "Adjetivos sustantivados (el bueno)",
     "teoria": "Un adjetivo se sustantiva cuando funciona como sustantivo, generalmente precedido de articulo. Adquiere genero y numero propios.",
     "explicacion": "Ejemplos: 'el bueno' (la persona buena), 'los ricos' (las personas ricas), 'lo importante' (la cosa importante). Tambien con articulo neutro 'lo': lo bello, lo esencial. En estos casos el adjetivo funciona como nucleo del sintagma nominal.",
     "regla": "Adjetivo sustantivado: articulo + adj = sustantivo",
     "ejemplo_correcto": "El bueno gano (el bueno = la persona buena).",
     "ejemplo_incorrecto": "El bueno gano (aqui 'bueno' sigue siendo adjetivo, no sustantivado)."},
    {"numero": 59, "bloque": "D", "nivel": "avanzado",
     "titulo": "Adjetivos relacionales",
     "teoria": "Los adjetivos relacionales expresan una relacion con un sustantivo (no una cualidad). No admiten grados ni se usan como predicativos.",
     "explicacion": "Ejemplos: espanol (de Espana), mensual (del mes), musical (de la musica), presidencial (del presidente). No admiten 'muy' (*muy mensual) ni grado comparativo (*mas espanol). Tampoco van con ser/estar en grado positivo (*es muy espanol).",
     "regla": "Relacional: relacion con sustantivo. No admite grados",
     "ejemplo_correcto": "Horario mensual (relacion con mes).",
     "ejemplo_incorrecto": "Horario muy mensual (no admite grado)."},
    {"numero": 60, "bloque": "D", "nivel": "basico",
     "titulo": "Adjetivos calificativos",
     "teoria": "Los adjetivos calificativos expresan cualidades o propiedades del sustantivo. Admiten grados (positivo, comparativo, superlativo).",
     "explicacion": "Ejemplos: alto, bajo, bueno, malo, bonito, feo, rapido, lento. Expresan propiedades que se pueden medir o comparar. Son la mayoria de los adjetivos en espanol. Admiten 'muy' y formas comparativas y superlativas.",
     "regla": "Calificativo: cualidad, admite grados",
     "ejemplo_correcto": "Casa grande, muy grande, mas grande que, grandisima.",
     "ejemplo_incorrecto": "Casa presidencial (es relacional, no calificativo)."},
]
TECNICAS.extend(TECNICAS_D2)

# ═══ D2: ejercicios 56-60 ═══
EJERCICIOS_56_60 = {
    56: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Los alumnos, cansados, se fueron', que tipo de adjetivo es 'cansados'?",
        "opciones": [
            {"id":"a","texto":"Explicativo","correcta":True,"razon":"Entre comas: informacion no esencial, todos estaban cansados."},
            {"id":"b","texto":"Especificativo","correcta":False,"razon":"Seria sin comas: solo los cansados."}],
        "justificacion_obligatoria": True, "regla": "Explicativo: coma"}}],
    57: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es la forma apocopada de 'primero'?",
        "opciones": [
            {"id":"a","texto":"Primer","correcta":True,"razon":"Ante sustantivo masculino singular: primer piso."},
            {"id":"b","texto":"Primero","correcta":False,"razon":"No se apocopa ante sustantivo masc sing."},
            {"id":"c","texto":"Primera","correcta":False,"razon":"Es femenino."}],
        "justificacion_obligatoria": True, "regla": "Apocope: primer + sustantivo masc"}}],
    58: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Lo importante es aprender', que funcion tiene 'importante'?",
        "opciones": [
            {"id":"a","texto":"Adjetivo calificativo","correcta":False,"razon":"Sustantivado por 'lo', funciona como sustantivo."},
            {"id":"b","texto":"Adjetivo sustantivado","correcta":True,"razon":"Articulo neutro 'lo' + adj = sustantivado."},
            {"id":"c","texto":"Adverbio","correcta":False,"razon":"No modifica verbo."}],
        "justificacion_obligatoria": True, "regla": "Lo + adj = sustantivado"}}],
    59: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de adjetivo es 'mensual'?",
        "opciones": [
            {"id":"a","texto":"Calificativo","correcta":False,"razon":"No expresa cualidad medible."},
            {"id":"b","texto":"Relacional","correcta":True,"razon":"Expresa relacion con 'mes'. No admite grados."},
            {"id":"c","texto":"Sustantivado","correcta":False,"razon":"No esta sustantivado aqui."}],
        "justificacion_obligatoria": True, "regla": "Relacional: no admite grados"}}],
    60: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de adjetivo admite grados (muy, mas... que)?",
        "opciones": [
            {"id":"a","texto":"Relacional","correcta":False,"razon":"No admite grados."},
            {"id":"b","texto":"Calificativo","correcta":True,"razon":"Expresa cualidad, admite grados."},
            {"id":"c","texto":"Sustantivado","correcta":False,"razon":"Funciona como sustantivo."}],
        "justificacion_obligatoria": True, "regla": "Calificativo: admite grados"}}],
}
EJERCICIOS.update(EJERCICIOS_56_60)

# ═══ E1: tecnicas 61-65 (el verbo: fundamentos y presente) ═══
TECNICAS_E1 = [
    {"numero": 61, "bloque": "E", "nivel": "basico",
     "titulo": "Verbos regulares vs irregulares",
     "teoria": "Los verbos regulares mantienen la raiz en toda la conjugacion y toman las terminaciones del modelo (-ar, -er, -ir). Los irregulares cambian la raiz o la terminacion.",
     "explicacion": "Regular: amar (amo, amas, ama). Irregular: ser (soy, eres, es); ir (voy, vas, va); tener (tengo, tienes, tiene). Los irregulares pueden cambiar la vocal de la raiz (e -> ie: pensar -> pienso) o la consonante (tener -> tengo).",
     "regla": "Regular: raiz fija. Irregular: cambia raiz o terminacion",
     "ejemplo_correcto": "Amar: amo, amas, ama (regular). Tener: tengo, tienes (irregular).",
     "ejemplo_incorrecto": "Amar: *amo, *amas, *ama (nada cambia, es regular)."},
    {"numero": 62, "bloque": "E", "nivel": "basico",
     "titulo": "Las 3 conjugaciones (-ar, -er, -ir)",
     "teoria": "En espanol hay tres conjugaciones segun la terminacion del infinitivo: 1.a (-ar), 2.a (-er), 3.a (-ir).",
     "explicacion": "Ejemplos: 1.a amar, cantar, saltar. 2.a temer, comer, beber. 3.a partir, vivir, subir. La vocal tematica (a/e/i) marca la conjugacion en toda la flexión. Saber la conjugacion ayuda a predecir formas regulares.",
     "regla": "1a: -ar. 2a: -er. 3a: -ir",
     "ejemplo_correcto": "Cantar (-ar, 1a), comer (-er, 2a), vivir (-ir, 3a).",
     "ejemplo_incorrecto": "Vivir es 2a conjugacion. (es 3a)"},
    {"numero": 63, "bloque": "E", "nivel": "basico",
     "titulo": "Persona y numero",
     "teoria": "El verbo varia en persona (1a, 2a, 3a) y numero (singular, plural) segun el sujeto.",
     "explicacion": "1a singular: yo. 2a singular: tu. 3a singular: el/ella. 1a plural: nosotros. 2a plural: vosotros. 3a plural: ellos/ellas. En America, 'vosotros' se reemplaza por 'ustedes' (3a plural).",
     "regla": "6 personas gramaticales: yo, tu, el, nosotros, vosotros, ellos",
     "ejemplo_correcto": "Yo canto, tu cantas, el canta, nosotros cantamos.",
     "ejemplo_incorrecto": "Yo cantas. (concordancia incorrecta)"},
    {"numero": 64, "bloque": "E", "nivel": "basico",
     "titulo": "Presente de indicativo",
     "teoria": "El presente de indicativo expresa acciones actuales, habituales o verdades generales.",
     "explicacion": "Usos: accion presente (yo como), habitual (todos los dias voy al trabajo), verdad general (el sol sale por el este), futuro inmediato (manana viajo a Bogota). Regulares: canto, cantas, canta, cantamos, cantais, cantan.",
     "regla": "Presente: accion actual, habitual o verdad general",
     "ejemplo_correcto": "Yo estudio espanol. El agua hierve a 100 grados.",
     "ejemplo_incorrecto": "Yo estudio ayer. (el presente no expresa pasado)"},
    {"numero": 65, "bloque": "E", "nivel": "intermedio",
     "titulo": "Preterito perfecto simple",
     "teoria": "El preterito perfecto simple (o preterito indefinido) expresa acciones terminadas en el pasado, sin conexion con el presente.",
     "explicacion": "Formas regulares: cante, cantaste, canto, cantamos, cantasteis, cantaron. Usos: accion puntual (ayer comi paella), serie de acciones terminadas (vino, saludo y se fue). Marcadores: ayer, la semana pasada, en 1999.",
     "regla": "Preterito simple: accion terminada, sin conexion con presente",
     "ejemplo_correcto": "Ayer cante en el coro.",
     "ejemplo_incorrecto": "Ayer he cantado (mejor: cante, si es accion terminada)"},
]
TECNICAS.extend(TECNICAS_E1)

# ═══ E1: ejercicios 61-65 ═══
EJERCICIOS_61_65 = {
    61: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada verbo: regular (R) o irregular (I)",
        "oraciones": [
            {"texto":"cantar","categoria_correcta":"regular"},
            {"texto":"ser","categoria_correcta":"irregular"},
            {"texto":"vivir","categoria_correcta":"regular"},
            {"texto":"tener","categoria_correcta":"irregular"}],
        "categorias": ["regular","irregular"]}}],
    62: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "A que conjugacion pertenece 'vivir'?",
        "opciones": [
            {"id":"a","texto":"1a (-ar)","correcta":False,"razon":"Termina en -ir."},
            {"id":"b","texto":"2a (-er)","correcta":False,"razon":"Termina en -ir, no -er."},
            {"id":"c","texto":"3a (-ir)","correcta":True,"razon":"Vivir termina en -ir."}],
        "justificacion_obligatoria": True, "regla": "3a conjugacion: -ir"}}],
    63: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que persona es 'cantamos'?",
        "opciones": [
            {"id":"a","texto":"1a persona plural","correcta":True,"razon":"Nosotros cantamos."},
            {"id":"b","texto":"3a persona plural","correcta":False,"razon":"Seria ellos cantan."},
            {"id":"c","texto":"1a persona singular","correcta":False,"razon":"Seria yo canto."}],
        "justificacion_obligatoria": True, "regla": "Nosotros = 1a plural"}}],
    64: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'El sol sale por el este', que valor tiene el presente?",
        "opciones": [
            {"id":"a","texto":"Verdad general","correcta":True,"razon":"Expresa una verdad universal."},
            {"id":"b","texto":"Accion pasada","correcta":False,"razon":"No es pasado."},
            {"id":"c","texto":"Futuro inmediato","correcta":False,"razon":"No es futuro."}],
        "justificacion_obligatoria": True, "regla": "Presente: verdad general"}}],
    65: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que forma es correcta: 'Ayer ___ en el coro'?",
        "opciones": [
            {"id":"a","texto":"he cantado","correcta":False,"razon":"Preterito perfecto compuesto: accion conectada con presente."},
            {"id":"b","texto":"cante","correcta":True,"razon":"Preterito simple: accion terminada en el pasado."},
            {"id":"c","texto":"cantaba","correcta":False,"razon":"Imperfecto: accion habitual o en desarrollo."}],
        "justificacion_obligatoria": True, "regla": "Ayer = preterito simple"}}],
}
EJERCICIOS.update(EJERCICIOS_61_65)

# ═══ E2: tecnicas 66-70 (tiempos del pasado y futuro) ═══
TECNICAS_E2 = [
    {"numero": 66, "bloque": "E", "nivel": "intermedio",
     "titulo": "Preterito imperfecto",
     "teoria": "El preterito imperfecto expresa acciones habituales, en desarrollo o descripciones en el pasado, sin marcar su fin.",
     "explicacion": "Formas regulares: cantaba, cantabas, cantaba, cantabamos, cantabais, cantaban. Usos: habitual (de nino jugaba al futbol), accion en desarrollo (leia cuando sono el telefono), descripcion (la casa era grande). Marcadores: antes, siempre, cuando era nino.",
     "regla": "Imperfecto: accion habitual o en desarrollo (sin fin marcado)",
     "ejemplo_correcto": "Cuando era nino, jugaba al futbol todos los dias.",
     "ejemplo_incorrecto": "Ayer jugaba al futbol (mejor: jugue, si fue puntual)"},
    {"numero": 67, "bloque": "E", "nivel": "intermedio",
     "titulo": "Preterito perfecto compuesto",
     "teoria": "El preterito perfecto compuesto (he cantado) expresa acciones pasadas con conexion con el presente, o acciones en un periodo que aun no ha terminado.",
     "explicacion": "Formacion: haber (he, has, ha, hemos, habeis, han) + participio (cantado, comido, vivido). Usos: hoy he estudiado (periodo aun abierto), he estado en Paris (experiencia vital). En America Latina se prefiere el preterito simple: hoy estudie.",
     "regla": "Perfecto compuesto: pasado con conexion con presente",
     "ejemplo_correcto": "Hoy he trabajado mucho. (periodo aun abierto)",
     "ejemplo_incorrecto": "Ayer he trabajado. (mejor: ayer trabaje)"},
    {"numero": 68, "bloque": "E", "nivel": "avanzado",
     "titulo": "Pluscuamperfecto",
     "teoria": "El pluscuamperfecto (habia cantado) expresa una accion pasada anterior a otra accion tambien pasada.",
     "explicacion": "Formacion: haber en imperfecto (habia, habias, habia, habiamos, habiais, habian) + participio. Uso: 'Cuando llegue, ya se habian ido' (primero se fueron, luego llegue). Marca anterioridad respecto a un punto pasado.",
     "regla": "Pluscuamperfecto: pasado del pasado (anterior a otro pasado)",
     "ejemplo_correcto": "Cuando llegue, ya se habian ido.",
     "ejemplo_incorrecto": "Cuando llegue, ya se han ido. (mezcla con presente)"},
    {"numero": 69, "bloque": "E", "nivel": "intermedio",
     "titulo": "Futuro simple",
     "teoria": "El futuro simple expresa acciones venideras respecto al momento del habla. Tambien puede expresar probabilidad o suposicion presente.",
     "explicacion": "Formas regulares: cantare, cantaras, cantara, cantaremos, cantareis, cantaran. Usos: futuro (manana ire), probabilidad presente (seran las tres = probablemente son las tres), mandato atenuado (cantaras esa cancion).",
     "regla": "Futuro: accion venidera o probabilidad presente",
     "ejemplo_correcto": "Manana ire al cine. Seran las tres.",
     "ejemplo_incorrecto": "Ayer ire al cine. (futuro no puede ser pasado)"},
    {"numero": 70, "bloque": "E", "nivel": "avanzado",
     "titulo": "Condicional simple",
     "teoria": "El condicional simple expresa acciones hipoteticas, probabilidad pasada o cortesia.",
     "explicacion": "Formas regulares: cantaria, cantarias, cantaria, cantariamos, cantariais, cantarian. Usos: hipotesis (si tuviera dinero, viajaria), probabilidad pasada (serian las tres = probablemente eran las tres), cortesia (podrias ayudarme?).",
     "regla": "Condicional: hipotesis, probabilidad pasada o cortesia",
     "ejemplo_correcto": "Si tuviera dinero, viajaria. Podrias ayudarme?",
     "ejemplo_incorrecto": "Si tengo dinero, viajaria. (mezcla indicativo + condicional, no encaja)"},
]
TECNICAS.extend(TECNICAS_E2)

# ═══ E2: ejercicios 66-70 ═══
EJERCICIOS_66_70 = {
    66: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Cuando era nino, jugaba al futbol', que valor tiene 'jugaba'?",
        "opciones": [
            {"id":"a","texto":"Habitual","correcta":True,"razon":"Accion repetida en el pasado: imperfecto."},
            {"id":"b","texto":"Puntual","correcta":False,"razon":"Seria 'jugue' si fuera puntual."},
            {"id":"c","texto":"Futuro","correcta":False,"razon":"Es pasado."}],
        "justificacion_obligatoria": True, "regla": "Imperfecto: habitual"}}],
    67: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que significa 'Hoy he estudiado'?",
        "opciones": [
            {"id":"a","texto":"Accion terminada hace tiempo","correcta":False,"razon":"'Hoy' es periodo aun abierto."},
            {"id":"b","texto":"Accion pasada en periodo aun abierto","correcta":True,"razon":"Perfecto compuesto con marcador de periodo abierto."},
            {"id":"c","texto":"Accion futura","correcta":False,"razon":"Es pasado."}],
        "justificacion_obligatoria": True, "regla": "He + participio = pasado conectado"}}],
    68: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Cuando llegue, ya se habian ido', que expresa 'habian ido'?",
        "opciones": [
            {"id":"a","texto":"Accion futura","correcta":False,"razon":"Es pasado."},
            {"id":"b","texto":"Pasado anterior a otro pasado","correcta":True,"razon":"Pluscuamperfecto: se fueron antes de que llegara."},
            {"id":"c","texto":"Accion presente","correcta":False,"razon":"Es pasado."}],
        "justificacion_obligatoria": True, "regla": "Pluscuamperfecto: pasado del pasado"}}],
    69: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Seran las tres', que valor tiene el futuro?",
        "opciones": [
            {"id":"a","texto":"Futuro real","correcta":False,"razon":"No es el futuro literal."},
            {"id":"b","texto":"Probabilidad presente","correcta":True,"razon":"'Seran las tres' = probablemente son las tres."},
            {"id":"c","texto":"Mandato","correcta":False,"razon":"No es mandato."}],
        "justificacion_obligatoria": True, "regla": "Futuro: probabilidad presente"}}],
    70: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que expresa 'Podrias ayudarme?'",
        "opciones": [
            {"id":"a","texto":"Cortesia","correcta":True,"razon":"Condicional de cortesia, equivalente a 'puedes'."},
            {"id":"b","texto":"Pasado","correcta":False,"razon":"No es pasado aqui."},
            {"id":"c","texto":"Futuro","correcta":False,"razon":"No es futuro."}],
        "justificacion_obligatoria": True, "regla": "Condicional: cortesia"}}],
}
EJERCICIOS.update(EJERCICIOS_66_70)

