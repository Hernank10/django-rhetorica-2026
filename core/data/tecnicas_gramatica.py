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