"""Data del modulo 12: gramatica generativa transformacional. Bloque A (1-15)."""

TECNICAS = [
    {"numero": 1, "bloque": "A", "nivel": "basico", "modulo": "generativa",
     "titulo": "Competencia vs actuacion",
     "teoria": "Chomsky (1965) distingue competencia (conocimiento interiorizado de la lengua) y actuacion (uso concreto en situaciones reales).",
     "explicacion": "La competencia es el sistema de reglas que el hablante conoce inconscientemente. La actuacion es lo que produce al hablar, con fallos, pausas, errores. La linguistica estudia la competencia, no solo la actuacion.",
     "regla": "Competencia = conocimiento interno. Actuacion = uso real",
     "ejemplo_correcto": "Un hablante nativo sabe (competencia) que 'vinieron' es correcto aunque este cansado y diga 'vinio' (actuacion).",
     "ejemplo_incorrecto": "La linguistica generativa solo estudia los errores de la actuacion."},
    {"numero": 2, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Gramatica universal (GU)",
     "teoria": "La GU es el conjunto de principios y estructuras innatas comunes a todas las lenguas humanas que propuso Chomsky.",
     "explicacion": "Los ninos adquieren su lengua materna con estimulos pobres. Chomsky explica esto con una capacidad innata: la GU. Todos los idiomas comparten principios universales; las diferencias son parametricas.",
     "regla": "GU: principios innatos comunes a todas las lenguas",
     "ejemplo_correcto": "Todos los idiomas tienen recursividad (capacidad de anidar estructuras).",
     "ejemplo_incorrecto": "Cada idioma tiene una gramatica completamente distinta sin nada en comun."},
    {"numero": 3, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Principios y parametros",
     "teoria": "El modelo de Principios y Parametros (Chomsky, 1981) explica la variacion linguistica: los principios son universales; los parametros son opciones que cada lengua fija.",
     "explicacion": "Ejemplo: el parametro del sujeto nulo. En castellano se fija en 'si' (se puede omitir el sujeto: 'canto'); en ingles se fija en 'no' (hay que decir 'I sing'). Los principios son iguales para todas las lenguas.",
     "regla": "Principios: universales. Parametros: opciones por lengua",
     "ejemplo_correcto": "El castellano permite sujeto nulo; el ingles no.",
     "ejemplo_incorrecto": "El castellano y el ingles tienen los mismos parametros."},
    {"numero": 4, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Estructura profunda vs estructura superficial",
     "teoria": "En la teoria clasica de Chomsky (1965), cada oracion tiene dos niveles: estructura profunda (EP) y estructura superficial (ES).",
     "explicacion": "La EP es la representacion del significado basico, antes de aplicar transformaciones. La ES es la forma final que se pronuncia. Las transformaciones convierten EP en ES. En el minimalismo esta distincion se reemplaza por otras (Merge/Move).",
     "regla": "EP: significado subyacente. ES: forma final pronunciada",
     "ejemplo_correcto": "'Juan lee el libro' tiene la misma EP y ES (oracion simple).",
     "ejemplo_incorrecto": "La EP y la ES son identicas en todas las oraciones."},
    {"numero": 5, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Reglas de reescritura (SN -> Det N)",
     "teoria": "Las reglas de reescritura de la gramatica generativa describen como se descompone un sintagma en sus constituyentes.",
     "explicacion": "Ejemplo: SN -> Det N. Un sintagma nominal se reescribe como determinante + nombre. 'El nino' -> Det ('el') + N ('nino'). Se encadenan reglas: O -> SN SV; SN -> Det N; SV -> V SN.",
     "regla": "Reescritura: X -> Y Z (descomposicion estructural)",
     "ejemplo_correcto": "O -> SN SV; SN -> Det N; SV -> V (reglas basicas).",
     "ejemplo_incorrecto": "SN -> N Det (orden invertido del castellano)."},
]


TECNICAS_6_10 = [
    {"numero": 6, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Reglas de estructura de frase",
     "teoria": "Las reglas de estructura de frase (phrase structure rules) describen la jerarquia de constituyentes de una oracion.",
     "explicacion": "Son la base del componente sintactico. Cada regla reescribe una categoria en dos o mas categorias. Ejemplos: O -> SN SV (oracion = sintagma nominal + sintagma verbal). Se aplican recursivamente para generar todas las oraciones de una lengua.",
     "regla": "Estructura de frase: reglas recursivas O -> SN SV",
     "ejemplo_correcto": "O -> SN SV; SN -> Det N; SV -> V SN.",
     "ejemplo_incorrecto": "Las reglas de estructura de frase no son recursivas."},
    {"numero": 7, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Recursividad sintactica",
     "teoria": "La recursividad es la capacidad de una regla de aplicarse a su propio resultado, generando estructuras de longitud ilimitada.",
     "explicacion": "Ejemplo: 'Maria dijo que Juan creia que Pedro pensaba que...' — cada 'que' anida una nueva subordinada. Sin recursion, el lenguaje seria finito. Chomsky la considera una propiedad central del lenguaje humano.",
     "regla": "Recursividad: una regla puede aplicarse a su propio resultado",
     "ejemplo_correcto": "Maria dijo que Juan creia que Pedro pensaba que Ana vendria.",
     "ejemplo_incorrecto": "La recursividad limita las oraciones a 10 palabras."},
    {"numero": 8, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Ambiguedad estructural",
     "teoria": "La ambiguedad estructural (o gramatical) ocurre cuando una misma secuencia de palabras tiene mas de una estructura sintactica posible.",
     "explicacion": "Ejemplo clasico: 'El policia golpeo al ladron con la pistola' — 'con la pistola' puede modificar a 'golpeo' (instrumento) o a 'ladron' (que llevaba pistola). Chomsky (1957) la usa para defender la autonomia de la sintaxis.",
     "regla": "Ambiguedad estructural: una secuencia, varias estructuras",
     "ejemplo_correcto": "Veo al hombre con el telescopio (con el telescopio: yo lo veo a traves del telescopio o el hombre tiene un telescopio).",
     "ejemplo_incorrecto": "La ambiguedad estructural es un error del hablante."},
    {"numero": 9, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Oraciones gramaticales vs agramaticales",
     "teoria": "Una oracion es gramatical si el sistema de reglas la genera; agramatical si viola alguna regla de la gramatica.",
     "explicacion": "En linguistica se marca con asterisco (*) lo agramatical. 'Juan canta' es gramatical; '*Juan cantan' es agramatical por fallo de concordancia. La gramaticalidad es una propiedad del sistema, no del significado.",
     "regla": "Gramatical: generada por las reglas. Agramatical: * (viola regla)",
     "ejemplo_correcto": "'Juan canta' (gramatical) vs '*Juan cantan' (agramatical).",
     "ejemplo_incorrecto": "Todas las oraciones con significado son gramaticales."},
    {"numero": 10, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Aceptabilidad vs gramaticalidad",
     "teoria": "La gramaticalidad es una propiedad del sistema linguistico; la aceptabilidad es el juicio del hablante sobre si una oracion es aceptable.",
     "explicacion": "Una oracion puede ser gramatical pero poco aceptable por complejidad: 'El hombre que la mujer que el nino vio saludo se fue' es gramatical pero dificil de procesar. Chomsky distingue ambas: la linguistica estudia la gramaticalidad, no solo la aceptabilidad.",
     "regla": "Gramaticalidad: propiedad del sistema. Aceptabilidad: juicio del hablante",
     "ejemplo_correcto": "Una oracion con muchos anidamientos puede ser gramatical pero poco aceptable.",
     "ejemplo_incorrecto": "Gramaticalidad y aceptabilidad son identicas."},
]
TECNICAS.extend(TECNICAS_6_10)


TECNICAS_11_15 = [
    {"numero": 11, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "El asterisco (*) en linguistica",
     "teoria": "En linguistica, el asterisco (*) marca una secuencia agramatical. Es una convencion de la gramatica generativa.",
     "explicacion": "Ejemplo: *Juan cantan (agramatical). Tambien marca reconstrucciones imposibles: *[CP que dijo Juan [TP que compro __]]. El asterisco es una marca teorica para distinguir lo posible de lo imposible.",
     "regla": "Asterisco (*) = agramatical segun las reglas",
     "ejemplo_correcto": "*Juan cantan (agramatical por concordancia).",
     "ejemplo_incorrecto": "El asterisco marca las oraciones con significado."},
    {"numero": 12, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Categorias lexicas vs funcionales",
     "teoria": "La gramatica generativa distingue categorias lexicas (N, V, A, Adv) de categorias funcionales (D, T, C).",
     "explicacion": "Lexicas: contenido semantico (nino, correr, alto). Funcionales: papel gramatical (articulo, tiempo, complementante). En el minimalismo, las funcionales son las que 'activan' el movimiento y la concordancia.",
     "regla": "Lexicas: contenido (N, V, A, Adv). Funcionales: papel (D, T, C)",
     "ejemplo_correcto": "Determinante (el) es funcional; sustantivo (nino) es lexico.",
     "ejemplo_incorrecto": "Todas las palabras son categorias lexicas."},
    {"numero": 13, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Nucleo, complemento, especificador",
     "teoria": "La teoria X-barra (Chomsky, 1970) descompone todo sintagma en tres posiciones: nucleo (X), complemento y especificador.",
     "explicacion": "El nucleo es la palabra central del sintagma (N en un SN). El complemento es lo que el nucleo selecciona ('de Juan' en 'el libro de Juan'). El especificador es una posicion externa ('muy' en 'muy alto'). Toda proyeccion maxima XP tiene estructura [Esp [X' X Compl]].",
     "regla": "Nucleo (X) + complemento. Especificador (Esp) a la izquierda",
     "ejemplo_correcto": "En 'el libro de fisica': nucleo=libro, complemento='de fisica'.",
     "ejemplo_incorrecto": "El nucleo va siempre a la derecha."},
    {"numero": 14, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Proyeccion maxima vs proyeccion intermedia",
     "teoria": "En la teoria X-barra hay tres niveles de proyeccion: X0 (nucleo), X' (proyeccion intermedia) y XP (proyeccion maxima).",
     "explicacion": "X0 es la palabra misma. X' agrupa nucleo + complemento. XP agrega el especificador. Ej: N (libro) -> N' (libro de fisica) -> NP/SN (el libro de fisica). Cada nivel proyecta la estructura hacia arriba.",
     "regla": "X0 -> X' (nucleo+compl) -> XP (espec+nucleo+compl)",
     "ejemplo_correcto": "SN = XP; N' = libro de fisica; N = libro.",
     "ejemplo_incorrecto": "Todos los sintagmas tienen solo dos niveles."},
    {"numero": 15, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "El principio de proyeccion",
     "teoria": "El principio de proyeccion (Chomsky, 1981) establece que las propiedades lexicas del nucleo se proyectan en la sintaxis.",
     "explicacion": "Si un verbo exige dos argumentos (agente y tema), esa exigencia se refleja en la estructura sintactica. Ej: 'dar' exige tres argumentos (alguien da algo a alguien). Si faltan, la oracion es agramatical: *Juan da.",
     "regla": "Principio de proyeccion: propiedades lexicas -> estructura sintactica",
     "ejemplo_correcto": "'Juan dio un libro a Maria' (cumple los 3 argumentos de 'dar').",
     "ejemplo_incorrecto": "El principio de proyeccion solo aplica a nombres."},
]
TECNICAS.extend(TECNICAS_11_15)


EJERCICIOS = {
    1: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que distingue la competencia de la actuacion?",
        "opciones": [
            {"id": "a", "texto": "Competencia = conocimiento interno; actuacion = uso real", "correcta": True, "razon": "Chomsky: competencia es el sistema interiorizado; actuacion es el uso concreto."},
            {"id": "b", "texto": "Son identicas", "correcta": False, "razon": "La actuacion incluye errores que la competencia no."},
            {"id": "c", "texto": "Competencia = habla; actuacion = escritura", "correcta": False, "razon": "No es la distincion."},
        ], "justificacion_obligatoria": True, "regla": "Competencia interno, actuacion real"}}],
    2: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la Gramatica Universal (GU)?",
        "opciones": [
            {"id": "a", "texto": "Un conjunto de principios innatos comunes a todas las lenguas", "correcta": True, "razon": "Chomsky: capacidad innata comun."},
            {"id": "b", "texto": "Una gramatica de una lengua especifica", "correcta": False, "razon": "La GU es universal."},
            {"id": "c", "texto": "Una lista de palabras universales", "correcta": False, "razon": "Es estructura, no lexico."},
        ], "justificacion_obligatoria": True, "regla": "GU: principios innatos"}}],
    3: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que diferencia hay entre principio y parametro?",
        "opciones": [
            {"id": "a", "texto": "Principio = universal; parametro = opcion por lengua", "correcta": True, "razon": "Los principios son iguales, los parametros varian."},
            {"id": "b", "texto": "Son sinonimos", "correcta": False, "razon": "No son equivalentes."},
            {"id": "c", "texto": "Parametro = universal; principio = por lengua", "correcta": False, "razon": "Invertido."},
        ], "justificacion_obligatoria": True, "regla": "Principio universal, parametro opcional"}}],
    4: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la estructura profunda (EP)?",
        "opciones": [
            {"id": "a", "texto": "La representacion del significado basico antes de transformaciones", "correcta": True, "razon": "EP = nivel subyacente antes de transformar."},
            {"id": "b", "texto": "La forma final pronunciada", "correcta": False, "razon": "Eso es la ES."},
            {"id": "c", "texto": "Un sinonimo de actuacion", "correcta": False, "razon": "No tiene que ver."},
        ], "justificacion_obligatoria": True, "regla": "EP: significado subyacente"}}],
    5: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que representa una regla como SN -> Det N?",
        "opciones": [
            {"id": "a", "texto": "Una regla de reescritura que descompone un sintagma en sus constituyentes", "correcta": True, "razon": "Las reglas de reescritura describen la descomposicion."},
            {"id": "b", "texto": "Una regla fonologica", "correcta": False, "razon": "Es sintactica."},
            {"id": "c", "texto": "Una regla de traduccion", "correcta": False, "razon": "No tiene que ver."},
        ], "justificacion_obligatoria": True, "regla": "Reescritura: descomposicion"}}],
    6: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que son las reglas de estructura de frase?",
        "opciones": [
            {"id": "a", "texto": "Reglas que describen la jerarquia de constituyentes de una oracion", "correcta": True, "razon": "Son la base del componente sintactico."},
            {"id": "b", "texto": "Reglas de ortografia", "correcta": False, "razon": "No tienen que ver."},
            {"id": "c", "texto": "Listas de palabras", "correcta": False, "razon": "Son reglas estructurales."},
        ], "justificacion_obligatoria": True, "regla": "Estructura de frase: jerarquia"}}],
    7: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la recursividad sintactica?",
        "opciones": [
            {"id": "a", "texto": "La capacidad de una regla de aplicarse a su propio resultado", "correcta": True, "razon": "Permite estructuras ilimitadas."},
            {"id": "b", "texto": "La repeticion de palabras", "correcta": False, "razon": "No es simple repeticion."},
            {"id": "c", "texto": "Una limitacion de las lenguas", "correcta": False, "razon": "Es una propiedad central."},
        ], "justificacion_obligatoria": True, "regla": "Recursividad: regla sobre su resultado"}}],
    8: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la ambiguedad estructural?",
        "opciones": [
            {"id": "a", "texto": "Una secuencia con mas de una estructura sintactica posible", "correcta": True, "razon": "Chomsky la usa para defender la autonomia de la sintaxis."},
            {"id": "b", "texto": "Un error del hablante", "correcta": False, "razon": "No es error."},
            {"id": "c", "texto": "Una oracion agramatical", "correcta": False, "razon": "Puede ser gramatical."},
        ], "justificacion_obligatoria": True, "regla": "Ambiguedad estructural: 2+ estructuras"}}],
    9: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que marca el asterisco (*) en linguistica?",
        "opciones": [
            {"id": "a", "texto": "Una secuencia agramatical", "correcta": True, "razon": "Convencion de la gramatica generativa."},
            {"id": "b", "texto": "Una oracion correcta", "correcta": False, "razon": "El asterisco marca lo incorrecto."},
            {"id": "c", "texto": "Una oracion ambigua", "correcta": False, "razon": "La ambiguedad no se marca con *."},
        ], "justificacion_obligatoria": True, "regla": "* = agramatical"}}],
    10: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que distingue gramaticalidad de aceptabilidad?",
        "opciones": [
            {"id": "a", "texto": "Gramaticalidad = propiedad del sistema; aceptabilidad = juicio del hablante", "correcta": True, "razon": "Chomsky distingue ambas."},
            {"id": "b", "texto": "Son identicas", "correcta": False, "razon": "Una oracion puede ser gramatical pero poco aceptable."},
            {"id": "c", "texto": "La aceptabilidad es del sistema", "correcta": False, "razon": "Invertido."},
        ], "justificacion_obligatoria": True, "regla": "Gramaticalidad vs aceptabilidad"}}],
    11: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que significa * en *Juan cantan?",
        "opciones": [
            {"id": "a", "texto": "Que es agramatical por fallo de concordancia", "correcta": True, "razon": "El * marca agramaticalidad."},
            {"id": "b", "texto": "Que es una oracion enfatica", "correcta": False, "razon": "No es enfasis."},
            {"id": "c", "texto": "Que es una cita", "correcta": False, "razon": "No es cita."},
        ], "justificacion_obligatoria": True, "regla": "* = agramatical"}}],
    12: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada categoria: lexica (L) o funcional (F)",
        "oraciones": [
            {"texto": "nino", "categoria_correcta": "lexica"},
            {"texto": "el", "categoria_correcta": "funcional"},
            {"texto": "correr", "categoria_correcta": "lexica"},
            {"texto": "que", "categoria_correcta": "funcional"},
        ],
        "categorias": ["lexica", "funcional"]}}],
    13: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'el libro de fisica', cual es el nucleo?",
        "opciones": [
            {"id": "a", "texto": "libro", "correcta": True, "razon": "El nucleo del SN es 'libro'."},
            {"id": "b", "texto": "de fisica", "correcta": False, "razon": "Es complemento."},
            {"id": "c", "texto": "el", "correcta": False, "razon": "Es determinante."},
        ], "justificacion_obligatoria": True, "regla": "Nucleo = palabra central"}}],
    14: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En la teoria X-barra, cuantos niveles de proyeccion hay?",
        "opciones": [
            {"id": "a", "texto": "3: X0, X', XP", "correcta": True, "razon": "Nucleo, proyeccion intermedia, proyeccion maxima."},
            {"id": "b", "texto": "2: X0 y XP", "correcta": False, "razon": "Falta la proyeccion intermedia X'."},
            {"id": "c", "texto": "4 niveles", "correcta": False, "razon": "Son 3."},
        ], "justificacion_obligatoria": True, "regla": "3 niveles: X0, X', XP"}}],
    15: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el principio de proyeccion?",
        "opciones": [
            {"id": "a", "texto": "Las propiedades lexicas se proyectan en la sintaxis", "correcta": True, "razon": "Si un verbo exige 3 argumentos, la sintaxis lo refleja."},
            {"id": "b", "texto": "Las palabras no afectan la estructura", "correcta": False, "razon": "Es lo contrario."},
            {"id": "c", "texto": "Solo aplica a nombres", "correcta": False, "razon": "Aplica a todas las categorias."},
        ], "justificacion_obligatoria": True, "regla": "Principio: propiedades lexicas -> sintaxis"}}],
}

