"""Data del modulo 12: gramatica generativa transformacional. Bloque A (1-15)."""

TECNICAS = [
    {"numero": 101, "bloque": "A", "nivel": "basico", "modulo": "generativa",
     "titulo": "Competencia vs actuacion",
     "teoria": "Chomsky (1965) distingue competencia (conocimiento interiorizado de la lengua) y actuacion (uso concreto en situaciones reales).",
     "explicacion": "La competencia es el sistema de reglas que el hablante conoce inconscientemente. La actuacion es lo que produce al hablar, con fallos, pausas, errores. La linguistica estudia la competencia, no solo la actuacion.",
     "regla": "Competencia = conocimiento interno. Actuacion = uso real",
     "ejemplo_correcto": "Un hablante nativo sabe (competencia) que 'vinieron' es correcto aunque este cansado y diga 'vinio' (actuacion).",
     "ejemplo_incorrecto": "La linguistica generativa solo estudia los errores de la actuacion."},
    {"numero": 102, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Gramatica universal (GU)",
     "teoria": "La GU es el conjunto de principios y estructuras innatas comunes a todas las lenguas humanas que propuso Chomsky.",
     "explicacion": "Los ninos adquieren su lengua materna con estimulos pobres. Chomsky explica esto con una capacidad innata: la GU. Todos los idiomas comparten principios universales; las diferencias son parametricas.",
     "regla": "GU: principios innatos comunes a todas las lenguas",
     "ejemplo_correcto": "Todos los idiomas tienen recursividad (capacidad de anidar estructuras).",
     "ejemplo_incorrecto": "Cada idioma tiene una gramatica completamente distinta sin nada en comun."},
    {"numero": 103, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Principios y parametros",
     "teoria": "El modelo de Principios y Parametros (Chomsky, 1981) explica la variacion linguistica: los principios son universales; los parametros son opciones que cada lengua fija.",
     "explicacion": "Ejemplo: el parametro del sujeto nulo. En castellano se fija en 'si' (se puede omitir el sujeto: 'canto'); en ingles se fija en 'no' (hay que decir 'I sing'). Los principios son iguales para todas las lenguas.",
     "regla": "Principios: universales. Parametros: opciones por lengua",
     "ejemplo_correcto": "El castellano permite sujeto nulo; el ingles no.",
     "ejemplo_incorrecto": "El castellano y el ingles tienen los mismos parametros."},
    {"numero": 104, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Estructura profunda vs estructura superficial",
     "teoria": "En la teoria clasica de Chomsky (1965), cada oracion tiene dos niveles: estructura profunda (EP) y estructura superficial (ES).",
     "explicacion": "La EP es la representacion del significado basico, antes de aplicar transformaciones. La ES es la forma final que se pronuncia. Las transformaciones convierten EP en ES. En el minimalismo esta distincion se reemplaza por otras (Merge/Move).",
     "regla": "EP: significado subyacente. ES: forma final pronunciada",
     "ejemplo_correcto": "'Juan lee el libro' tiene la misma EP y ES (oracion simple).",
     "ejemplo_incorrecto": "La EP y la ES son identicas en todas las oraciones."},
    {"numero": 105, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Reglas de reescritura (SN -> Det N)",
     "teoria": "Las reglas de reescritura de la gramatica generativa describen como se descompone un sintagma en sus constituyentes.",
     "explicacion": "Ejemplo: SN -> Det N. Un sintagma nominal se reescribe como determinante + nombre. 'El nino' -> Det ('el') + N ('nino'). Se encadenan reglas: O -> SN SV; SN -> Det N; SV -> V SN.",
     "regla": "Reescritura: X -> Y Z (descomposicion estructural)",
     "ejemplo_correcto": "O -> SN SV; SN -> Det N; SV -> V (reglas basicas).",
     "ejemplo_incorrecto": "SN -> N Det (orden invertido del castellano)."},
]


TECNICAS_6_10 = [
    {"numero": 106, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Reglas de estructura de frase",
     "teoria": "Las reglas de estructura de frase (phrase structure rules) describen la jerarquia de constituyentes de una oracion.",
     "explicacion": "Son la base del componente sintactico. Cada regla reescribe una categoria en dos o mas categorias. Ejemplos: O -> SN SV (oracion = sintagma nominal + sintagma verbal). Se aplican recursivamente para generar todas las oraciones de una lengua.",
     "regla": "Estructura de frase: reglas recursivas O -> SN SV",
     "ejemplo_correcto": "O -> SN SV; SN -> Det N; SV -> V SN.",
     "ejemplo_incorrecto": "Las reglas de estructura de frase no son recursivas."},
    {"numero": 107, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Recursividad sintactica",
     "teoria": "La recursividad es la capacidad de una regla de aplicarse a su propio resultado, generando estructuras de longitud ilimitada.",
     "explicacion": "Ejemplo: 'Maria dijo que Juan creia que Pedro pensaba que...' — cada 'que' anida una nueva subordinada. Sin recursion, el lenguaje seria finito. Chomsky la considera una propiedad central del lenguaje humano.",
     "regla": "Recursividad: una regla puede aplicarse a su propio resultado",
     "ejemplo_correcto": "Maria dijo que Juan creia que Pedro pensaba que Ana vendria.",
     "ejemplo_incorrecto": "La recursividad limita las oraciones a 10 palabras."},
    {"numero": 108, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Ambiguedad estructural",
     "teoria": "La ambiguedad estructural (o gramatical) ocurre cuando una misma secuencia de palabras tiene mas de una estructura sintactica posible.",
     "explicacion": "Ejemplo clasico: 'El policia golpeo al ladron con la pistola' — 'con la pistola' puede modificar a 'golpeo' (instrumento) o a 'ladron' (que llevaba pistola). Chomsky (1957) la usa para defender la autonomia de la sintaxis.",
     "regla": "Ambiguedad estructural: una secuencia, varias estructuras",
     "ejemplo_correcto": "Veo al hombre con el telescopio (con el telescopio: yo lo veo a traves del telescopio o el hombre tiene un telescopio).",
     "ejemplo_incorrecto": "La ambiguedad estructural es un error del hablante."},
    {"numero": 109, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Oraciones gramaticales vs agramaticales",
     "teoria": "Una oracion es gramatical si el sistema de reglas la genera; agramatical si viola alguna regla de la gramatica.",
     "explicacion": "En linguistica se marca con asterisco (*) lo agramatical. 'Juan canta' es gramatical; '*Juan cantan' es agramatical por fallo de concordancia. La gramaticalidad es una propiedad del sistema, no del significado.",
     "regla": "Gramatical: generada por las reglas. Agramatical: * (viola regla)",
     "ejemplo_correcto": "'Juan canta' (gramatical) vs '*Juan cantan' (agramatical).",
     "ejemplo_incorrecto": "Todas las oraciones con significado son gramaticales."},
    {"numero": 110, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Aceptabilidad vs gramaticalidad",
     "teoria": "La gramaticalidad es una propiedad del sistema linguistico; la aceptabilidad es el juicio del hablante sobre si una oracion es aceptable.",
     "explicacion": "Una oracion puede ser gramatical pero poco aceptable por complejidad: 'El hombre que la mujer que el nino vio saludo se fue' es gramatical pero dificil de procesar. Chomsky distingue ambas: la linguistica estudia la gramaticalidad, no solo la aceptabilidad.",
     "regla": "Gramaticalidad: propiedad del sistema. Aceptabilidad: juicio del hablante",
     "ejemplo_correcto": "Una oracion con muchos anidamientos puede ser gramatical pero poco aceptable.",
     "ejemplo_incorrecto": "Gramaticalidad y aceptabilidad son identicas."},
]
TECNICAS.extend(TECNICAS_6_10)


TECNICAS_11_15 = [
    {"numero": 111, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "El asterisco (*) en linguistica",
     "teoria": "En linguistica, el asterisco (*) marca una secuencia agramatical. Es una convencion de la gramatica generativa.",
     "explicacion": "Ejemplo: *Juan cantan (agramatical). Tambien marca reconstrucciones imposibles: *[CP que dijo Juan [TP que compro __]]. El asterisco es una marca teorica para distinguir lo posible de lo imposible.",
     "regla": "Asterisco (*) = agramatical segun las reglas",
     "ejemplo_correcto": "*Juan cantan (agramatical por concordancia).",
     "ejemplo_incorrecto": "El asterisco marca las oraciones con significado."},
    {"numero": 112, "bloque": "A", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Categorias lexicas vs funcionales",
     "teoria": "La gramatica generativa distingue categorias lexicas (N, V, A, Adv) de categorias funcionales (D, T, C).",
     "explicacion": "Lexicas: contenido semantico (nino, correr, alto). Funcionales: papel gramatical (articulo, tiempo, complementante). En el minimalismo, las funcionales son las que 'activan' el movimiento y la concordancia.",
     "regla": "Lexicas: contenido (N, V, A, Adv). Funcionales: papel (D, T, C)",
     "ejemplo_correcto": "Determinante (el) es funcional; sustantivo (nino) es lexico.",
     "ejemplo_incorrecto": "Todas las palabras son categorias lexicas."},
    {"numero": 113, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Nucleo, complemento, especificador",
     "teoria": "La teoria X-barra (Chomsky, 1970) descompone todo sintagma en tres posiciones: nucleo (X), complemento y especificador.",
     "explicacion": "El nucleo es la palabra central del sintagma (N en un SN). El complemento es lo que el nucleo selecciona ('de Juan' en 'el libro de Juan'). El especificador es una posicion externa ('muy' en 'muy alto'). Toda proyeccion maxima XP tiene estructura [Esp [X' X Compl]].",
     "regla": "Nucleo (X) + complemento. Especificador (Esp) a la izquierda",
     "ejemplo_correcto": "En 'el libro de fisica': nucleo=libro, complemento='de fisica'.",
     "ejemplo_incorrecto": "El nucleo va siempre a la derecha."},
    {"numero": 114, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Proyeccion maxima vs proyeccion intermedia",
     "teoria": "En la teoria X-barra hay tres niveles de proyeccion: X0 (nucleo), X' (proyeccion intermedia) y XP (proyeccion maxima).",
     "explicacion": "X0 es la palabra misma. X' agrupa nucleo + complemento. XP agrega el especificador. Ej: N (libro) -> N' (libro de fisica) -> NP/SN (el libro de fisica). Cada nivel proyecta la estructura hacia arriba.",
     "regla": "X0 -> X' (nucleo+compl) -> XP (espec+nucleo+compl)",
     "ejemplo_correcto": "SN = XP; N' = libro de fisica; N = libro.",
     "ejemplo_incorrecto": "Todos los sintagmas tienen solo dos niveles."},
    {"numero": 115, "bloque": "A", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "El principio de proyeccion",
     "teoria": "El principio de proyeccion (Chomsky, 1981) establece que las propiedades lexicas del nucleo se proyectan en la sintaxis.",
     "explicacion": "Si un verbo exige dos argumentos (agente y tema), esa exigencia se refleja en la estructura sintactica. Ej: 'dar' exige tres argumentos (alguien da algo a alguien). Si faltan, la oracion es agramatical: *Juan da.",
     "regla": "Principio de proyeccion: propiedades lexicas -> estructura sintactica",
     "ejemplo_correcto": "'Juan dio un libro a Maria' (cumple los 3 argumentos de 'dar').",
     "ejemplo_incorrecto": "El principio de proyeccion solo aplica a nombres."},
]
TECNICAS.extend(TECNICAS_11_15)


EJERCICIOS = {
    101: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que distingue la competencia de la actuacion?",
        "opciones": [
            {"id": "a", "texto": "Competencia = conocimiento interno; actuacion = uso real", "correcta": True, "razon": "Chomsky: competencia es el sistema interiorizado; actuacion es el uso concreto."},
            {"id": "b", "texto": "Son identicas", "correcta": False, "razon": "La actuacion incluye errores que la competencia no."},
            {"id": "c", "texto": "Competencia = habla; actuacion = escritura", "correcta": False, "razon": "No es la distincion."},
        ], "justificacion_obligatoria": True, "regla": "Competencia interno, actuacion real"}}],
    102: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la Gramatica Universal (GU)?",
        "opciones": [
            {"id": "a", "texto": "Un conjunto de principios innatos comunes a todas las lenguas", "correcta": True, "razon": "Chomsky: capacidad innata comun."},
            {"id": "b", "texto": "Una gramatica de una lengua especifica", "correcta": False, "razon": "La GU es universal."},
            {"id": "c", "texto": "Una lista de palabras universales", "correcta": False, "razon": "Es estructura, no lexico."},
        ], "justificacion_obligatoria": True, "regla": "GU: principios innatos"}}],
    103: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que diferencia hay entre principio y parametro?",
        "opciones": [
            {"id": "a", "texto": "Principio = universal; parametro = opcion por lengua", "correcta": True, "razon": "Los principios son iguales, los parametros varian."},
            {"id": "b", "texto": "Son sinonimos", "correcta": False, "razon": "No son equivalentes."},
            {"id": "c", "texto": "Parametro = universal; principio = por lengua", "correcta": False, "razon": "Invertido."},
        ], "justificacion_obligatoria": True, "regla": "Principio universal, parametro opcional"}}],
    104: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la estructura profunda (EP)?",
        "opciones": [
            {"id": "a", "texto": "La representacion del significado basico antes de transformaciones", "correcta": True, "razon": "EP = nivel subyacente antes de transformar."},
            {"id": "b", "texto": "La forma final pronunciada", "correcta": False, "razon": "Eso es la ES."},
            {"id": "c", "texto": "Un sinonimo de actuacion", "correcta": False, "razon": "No tiene que ver."},
        ], "justificacion_obligatoria": True, "regla": "EP: significado subyacente"}}],
    105: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que representa una regla como SN -> Det N?",
        "opciones": [
            {"id": "a", "texto": "Una regla de reescritura que descompone un sintagma en sus constituyentes", "correcta": True, "razon": "Las reglas de reescritura describen la descomposicion."},
            {"id": "b", "texto": "Una regla fonologica", "correcta": False, "razon": "Es sintactica."},
            {"id": "c", "texto": "Una regla de traduccion", "correcta": False, "razon": "No tiene que ver."},
        ], "justificacion_obligatoria": True, "regla": "Reescritura: descomposicion"}}],
    106: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que son las reglas de estructura de frase?",
        "opciones": [
            {"id": "a", "texto": "Reglas que describen la jerarquia de constituyentes de una oracion", "correcta": True, "razon": "Son la base del componente sintactico."},
            {"id": "b", "texto": "Reglas de ortografia", "correcta": False, "razon": "No tienen que ver."},
            {"id": "c", "texto": "Listas de palabras", "correcta": False, "razon": "Son reglas estructurales."},
        ], "justificacion_obligatoria": True, "regla": "Estructura de frase: jerarquia"}}],
    107: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la recursividad sintactica?",
        "opciones": [
            {"id": "a", "texto": "La capacidad de una regla de aplicarse a su propio resultado", "correcta": True, "razon": "Permite estructuras ilimitadas."},
            {"id": "b", "texto": "La repeticion de palabras", "correcta": False, "razon": "No es simple repeticion."},
            {"id": "c", "texto": "Una limitacion de las lenguas", "correcta": False, "razon": "Es una propiedad central."},
        ], "justificacion_obligatoria": True, "regla": "Recursividad: regla sobre su resultado"}}],
    108: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la ambiguedad estructural?",
        "opciones": [
            {"id": "a", "texto": "Una secuencia con mas de una estructura sintactica posible", "correcta": True, "razon": "Chomsky la usa para defender la autonomia de la sintaxis."},
            {"id": "b", "texto": "Un error del hablante", "correcta": False, "razon": "No es error."},
            {"id": "c", "texto": "Una oracion agramatical", "correcta": False, "razon": "Puede ser gramatical."},
        ], "justificacion_obligatoria": True, "regla": "Ambiguedad estructural: 2+ estructuras"}}],
    109: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que marca el asterisco (*) en linguistica?",
        "opciones": [
            {"id": "a", "texto": "Una secuencia agramatical", "correcta": True, "razon": "Convencion de la gramatica generativa."},
            {"id": "b", "texto": "Una oracion correcta", "correcta": False, "razon": "El asterisco marca lo incorrecto."},
            {"id": "c", "texto": "Una oracion ambigua", "correcta": False, "razon": "La ambiguedad no se marca con *."},
        ], "justificacion_obligatoria": True, "regla": "* = agramatical"}}],
    110: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que distingue gramaticalidad de aceptabilidad?",
        "opciones": [
            {"id": "a", "texto": "Gramaticalidad = propiedad del sistema; aceptabilidad = juicio del hablante", "correcta": True, "razon": "Chomsky distingue ambas."},
            {"id": "b", "texto": "Son identicas", "correcta": False, "razon": "Una oracion puede ser gramatical pero poco aceptable."},
            {"id": "c", "texto": "La aceptabilidad es del sistema", "correcta": False, "razon": "Invertido."},
        ], "justificacion_obligatoria": True, "regla": "Gramaticalidad vs aceptabilidad"}}],
    111: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que significa * en *Juan cantan?",
        "opciones": [
            {"id": "a", "texto": "Que es agramatical por fallo de concordancia", "correcta": True, "razon": "El * marca agramaticalidad."},
            {"id": "b", "texto": "Que es una oracion enfatica", "correcta": False, "razon": "No es enfasis."},
            {"id": "c", "texto": "Que es una cita", "correcta": False, "razon": "No es cita."},
        ], "justificacion_obligatoria": True, "regla": "* = agramatical"}}],
    112: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada categoria: lexica (L) o funcional (F)",
        "oraciones": [
            {"texto": "nino", "categoria_correcta": "lexica"},
            {"texto": "el", "categoria_correcta": "funcional"},
            {"texto": "correr", "categoria_correcta": "lexica"},
            {"texto": "que", "categoria_correcta": "funcional"},
        ],
        "categorias": ["lexica", "funcional"]}}],
    113: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'el libro de fisica', cual es el nucleo?",
        "opciones": [
            {"id": "a", "texto": "libro", "correcta": True, "razon": "El nucleo del SN es 'libro'."},
            {"id": "b", "texto": "de fisica", "correcta": False, "razon": "Es complemento."},
            {"id": "c", "texto": "el", "correcta": False, "razon": "Es determinante."},
        ], "justificacion_obligatoria": True, "regla": "Nucleo = palabra central"}}],
    114: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En la teoria X-barra, cuantos niveles de proyeccion hay?",
        "opciones": [
            {"id": "a", "texto": "3: X0, X', XP", "correcta": True, "razon": "Nucleo, proyeccion intermedia, proyeccion maxima."},
            {"id": "b", "texto": "2: X0 y XP", "correcta": False, "razon": "Falta la proyeccion intermedia X'."},
            {"id": "c", "texto": "4 niveles", "correcta": False, "razon": "Son 3."},
        ], "justificacion_obligatoria": True, "regla": "3 niveles: X0, X', XP"}}],
    115: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el principio de proyeccion?",
        "opciones": [
            {"id": "a", "texto": "Las propiedades lexicas se proyectan en la sintaxis", "correcta": True, "razon": "Si un verbo exige 3 argumentos, la sintaxis lo refleja."},
            {"id": "b", "texto": "Las palabras no afectan la estructura", "correcta": False, "razon": "Es lo contrario."},
            {"id": "c", "texto": "Solo aplica a nombres", "correcta": False, "razon": "Aplica a todas las categorias."},
        ], "justificacion_obligatoria": True, "regla": "Principio: propiedades lexicas -> sintaxis"}}],
}


TECNICAS_16_20 = [
    {"numero": 116, "bloque": "B", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "Teoria X-barra: esquema general",
     "teoria": "La teoria X-barra (Chomsky, 1970) describe como cualquier categoria proyecta su estructura sintactica en 3 niveles: nucleo (X0), proyeccion intermedia (X') y proyeccion maxima (XP).",
     "explicacion": "Esquema: XP -> [Especificador [X' X0 Complemento]]. Todo sintagma sigue este patron. El nucleo determina la categoria (N, V, P, A, Adv). El especificador y el complemento son opcionales segun el nucleo.",
     "regla": "X-barra: XP -> Esp [X' X0 Compl]",
     "ejemplo_correcto": "Un SN 'el libro de fisica' sigue X-barra con N como nucleo.",
     "ejemplo_incorrecto": "Cada sintagma tiene una estructura distinta sin patron comun."},
    {"numero": 117, "bloque": "B", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "SN (sintagma nominal)",
     "teoria": "El sintagma nominal tiene como nucleo un sustantivo (N). Su estructura X-barra es SN -> [Det [N' N Compl]].",
     "explicacion": "El SN puede tener determinante (el, un) como especificador, un N como nucleo y un complemento (de fisica) opcional. En algunos analisis, el Det es un nucleo D y se proyecta como SD. Chomsky (1986) propone que el SN sea SD.",
     "regla": "SN: nucleo N, especificador Det, complemento SP",
     "ejemplo_correcto": "El libro de fisica: Det=el, N=libro, Compl=de fisica.",
     "ejemplo_incorrecto": "El SN no tiene estructura interna."},
    {"numero": 118, "bloque": "B", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "SV (sintagma verbal)",
     "teoria": "El sintagma verbal tiene como nucleo un verbo (V). Su estructura es SV -> [V' V0 Compl].",
     "explicacion": "El verbo selecciona su complemento. En 'Juan lee el libro', el SV = 'lee el libro', con 'lee' como nucleo V0 y 'el libro' como complemento SN. El verbo puede tener uno o dos complementos segun su estructura argumental.",
     "regla": "SV: nucleo V, complemento SN/SP",
     "ejemplo_correcto": "En 'Juan lee el libro', lee es el nucleo del SV.",
     "ejemplo_incorrecto": "El SV no tiene nucleo."},
    {"numero": 119, "bloque": "B", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "SP (sintagma preposicional)",
     "teoria": "El sintagma preposicional tiene como nucleo una preposicion (P). Su estructura es SP -> [P' P0 Compl].",
     "explicacion": "En 'de fisica', 'de' es P0 y 'fisica' es complemento SN. El SP funciona como complemento de otros nucleos (V o N) o como modificador. En algunos analisis, la preposicion tambien puede ser nucleo de un SP con un SN como complemento.",
     "regla": "SP: nucleo P, complemento SN",
     "ejemplo_correcto": "En 'de fisica', de es el nucleo del SP.",
     "ejemplo_incorrecto": "El SP tiene como nucleo un sustantivo."},
    {"numero": 120, "bloque": "B", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "SA (sintagma adjetival)",
     "teoria": "El sintagma adjetival tiene como nucleo un adjetivo (A). Su estructura es SA -> [Esp [A' A0 Compl]].",
     "explicacion": "En 'muy alto', 'muy' es el especificador del SA y 'alto' es el nucleo A. En 'orgulloso de su hijo', el complemento es el SP 'de su hijo'. Los adjetivos pueden llevar especificador (muy) y complemento (de...).",
     "regla": "SA: nucleo A, especificador Adv, complemento SP",
     "ejemplo_correcto": "En 'muy orgulloso de su hijo': muy (Esp), orgulloso (A0), de su hijo (Compl).",
     "ejemplo_incorrecto": "El SA tiene como nucleo un verbo."},
]
TECNICAS.extend(TECNICAS_16_20)


TECNICAS_21_25 = [
    {"numero": 121, "bloque": "B", "nivel": "intermedio", "modulo": "generativa",
     "titulo": "SAdv (sintagma adverbial)",
     "teoria": "El sintagma adverbial tiene como nucleo un adverbio (Adv). Su estructura es SAdv -> [Esp [Adv' Adv0 Compl]].",
     "explicacion": "En 'muy rapidamente', 'muy' es el especificador y 'rapidamente' el nucleo. En 'antes de la fiesta', 'antes' es nucleo y 'de la fiesta' complemento. Los adverbios pueden modificar a verbos, adjetivos u otros adverbios.",
     "regla": "SAdv: nucleo Adv, especificador y complemento",
     "ejemplo_correcto": "En 'muy rapidamente', muy (Esp) + rapidamente (Adv0).",
     "ejemplo_incorrecto": "El SAdv tiene como nucleo un sustantivo."},
    {"numero": 122, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "SC (sintagma complementante)",
     "teoria": "El SC (o CP en ingles) tiene como nucleo un complementante (C): que, si, para. Su estructura es SC -> [Esp [C' C0 ST]].",
     "explicacion": "C0 puede ser 'que' en subordinadas sustantivas ('que venga'), 'si' en interrogativas indirectas ('si viene'), o estar vacio. El ST (sintagma tiempo) es su complemento. El SC es la proyeccion maxima de la oracion subordinada.",
     "regla": "SC: nucleo C (que/si/para), complemento ST",
     "ejemplo_correcto": "En 'que Juan venga', 'que' es el nucleo C del SC.",
     "ejemplo_incorrecto": "El SC no tiene nucleo."},
    {"numero": 123, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "ST (sintagma tiempo / flexion)",
     "teoria": "El ST (o IP/SF en la tradicion) tiene como nucleo el tiempo o la flexion. Su estructura es ST -> [Esp [T' T0 SV]].",
     "explicacion": "En la oracion 'Juan lee', el ST tiene como especificador a 'Juan' (sujeto) y como nucleo T (tiempo presente). El SV 'lee' es el complemento. El ST es la proyeccion que alberga la concordancia y el tiempo de la oracion.",
     "regla": "ST: nucleo T (tiempo/flexion), especificador=sujeto",
     "ejemplo_correcto": "En 'Juan lee', Juan es el especificador del ST.",
     "ejemplo_incorrecto": "El ST no tiene relacion con el tiempo."},
    {"numero": 124, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Nucleo funcional: T (Tiempo)",
     "teoria": "T es el nucleo funcional que alberga los rasgos de tiempo y concordancia. Selecciona al SV como complemento.",
     "explicacion": "T puede ser [+finito] (presente, pasado, futuro) o [-finito] (infinitivo). En 'Juan canta', T esta en presente y concuerda con Juan (3a sing). En 'Juan cantar', T es no finito. El movimiento del verbo a T se da en algunas lenguas (frances) pero no en otras.",
     "regla": "T: tiempo + concordancia. Selecciona SV",
     "ejemplo_correcto": "En 'Juan canta', T aporta el tiempo presente y la 3a persona.",
     "ejemplo_incorrecto": "T no tiene relacion con el tiempo verbal."},
    {"numero": 125, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Nucleo funcional: C (Complementante)",
     "teoria": "C es el nucleo funcional que introduce la oracion subordinada. Sus valores tipicos: que, si, para.",
     "explicacion": "C selecciona al ST como complemento. En 'que Juan venga', 'que' es C. En 'si viene', 'si' es C interrogativo. En oraciones principales C esta vacio. C es la posicion de aterrizaje del movimiento-qu en interrogativas.",
     "regla": "C: introduce la subordinada (que/si/para)",
     "ejemplo_correcto": "En 'que Juan venga', que es el nucleo C.",
     "ejemplo_incorrecto": "C solo existe en oraciones principales."},
]
TECNICAS.extend(TECNICAS_21_25)


TECNICAS_26_30 = [
    {"numero": 126, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Nucleo funcional: D (Determinante)",
     "teoria": "D es el nucleo funcional del sintagma determinante (SD). Contiene los articulos, demostrativos y posesivos.",
     "explicacion": "Chomsky (1986) propone que los sintagmas nominales son en realidad SD: SD -> [D' D0 SN]. En 'el libro', 'el' es D y 'libro' es el SN complemento. El sujeto de la oracion puede ser un SD.",
     "regla": "D: nucleo funcional del SD (articulos, demostrativos)",
     "ejemplo_correcto": "En 'el libro', el es D y libro es el SN complemento.",
     "ejemplo_incorrecto": "D es una categoria lexica con contenido pleno."},
    {"numero": 127, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "La concordancia como nucleo funcional",
     "teoria": "La concordancia (genero, numero, persona) se aloja en los nucleos funcionales T (sujeto-verbo) y D (articulo-sustantivo).",
     "explicacion": "En 'los ninos cantan', T concuerda con el sujeto plural (cantan), y D ('los') concuerda con el sustantivo plural (ninos). La concordancia es una relacion entre un nucleo funcional y su especificador o complemento.",
     "regla": "Concordancia: nucleos funcionales T y D",
     "ejemplo_correcto": "En 'los ninos cantan', T concuerda con el sujeto.",
     "ejemplo_incorrecto": "La concordancia no tiene nucleo funcional."},
    {"numero": 128, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Estructura de la oracion simple (ST)",
     "teoria": "La oracion simple se analiza como un ST: ST -> [Esp [T' T0 SV]]. El sujeto ocupa el especificador del ST.",
     "explicacion": "En 'Juan canta', Juan (Esp del ST) concuerda con T (3a sing). El SV 'canta' es el complemento. Si el verbo se mueve a T, la estructura es [ST Juan [T' canta [SV t]]]. Este analisis es central en el minimalismo.",
     "regla": "Oracion simple = ST: [Esp [T' T SV]]",
     "ejemplo_correcto": "ST -> [ST Juan [T' canta [SV <canta>]]].",
     "ejemplo_incorrecto": "La oracion simple no tiene estructura de ST."},
    {"numero": 129, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Estructura de la oracion compuesta (SC)",
     "teoria": "La oracion compuesta se analiza como un SC: SC -> [C' C0 ST]. El complementante C introduce la subordinada.",
     "explicacion": "En 'Maria dijo que Juan canta', el SC es 'que Juan canta' (C='que', ST='Juan canta'). El SC es el complemento del verbo 'dijo'. Las subordinadas sustantivas son SC.",
     "regla": "Oracion compuesta = SC: [C' C ST]",
     "ejemplo_correcto": "SC = 'que Juan canta', con 'que' como nucleo C.",
     "ejemplo_incorrecto": "La oracion compuesta no tiene estructura de SC."},
    {"numero": 130, "bloque": "B", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Diagrama arboreo: como dibujarlo",
     "teoria": "El diagrama arboreo (o arbol sintactico) es la representacion grafica de la estructura X-barra de una oracion.",
     "explicacion": "Cada nodo es una categoria (S, SN, N, V). Las hojas son las palabras. Las ramas muestran la relacion madre-hija. Se dibuja de arriba hacia abajo. Ejemplo: 'El nino canta' -> O -> [SN [Det el] [N nino]] [SV [V canta]]. El arbol refleja la jerarquia de constituyentes.",
     "regla": "Diagrama arboreo: nodos = categorias, hojas = palabras",
     "ejemplo_correcto": "O -> [SN Det+N] [SV V] para 'el nino canta'.",
     "ejemplo_incorrecto": "El diagrama arboreo es una simple lista de palabras."},
]
TECNICAS.extend(TECNICAS_26_30)


EJERCICIOS_B = {
    116: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuantos niveles de proyeccion describe la teoria X-barra?",
        "opciones": [
            {"id": "a", "texto": "3: X0, X', XP", "correcta": True, "razon": "Nucleo, proyeccion intermedia, proyeccion maxima."},
            {"id": "b", "texto": "2: X0 y XP", "correcta": False, "razon": "Falta X' (intermedia)."},
            {"id": "c", "texto": "4 niveles", "correcta": False, "razon": "Son 3."},
        ], "justificacion_obligatoria": True, "regla": "3 niveles: X0, X', XP"}}],
    117: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el nucleo del sintagma nominal (SN)?",
        "opciones": [
            {"id": "a", "texto": "El sustantivo (N)", "correcta": True, "razon": "El SN proyecta un nucleo N."},
            {"id": "b", "texto": "El determinante (Det)", "correcta": False, "razon": "El Det es el especificador."},
            {"id": "c", "texto": "El adjetivo (A)", "correcta": False, "razon": "El A modifica al N pero no es el nucleo."},
        ], "justificacion_obligatoria": True, "regla": "SN: nucleo N"}}],
    118: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan lee el libro', cual es el nucleo del SV?",
        "opciones": [
            {"id": "a", "texto": "lee", "correcta": True, "razon": "El verbo es el nucleo del SV."},
            {"id": "b", "texto": "el libro", "correcta": False, "razon": "Es el complemento."},
            {"id": "c", "texto": "Juan", "correcta": False, "razon": "Es el sujeto."},
        ], "justificacion_obligatoria": True, "regla": "SV: nucleo V"}}],
    119: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el nucleo del SP en 'de fisica'?",
        "opciones": [
            {"id": "a", "texto": "de", "correcta": True, "razon": "La preposicion es el nucleo del SP."},
            {"id": "b", "texto": "fisica", "correcta": False, "razon": "Es el complemento SN."},
            {"id": "c", "texto": "No tiene nucleo", "correcta": False, "razon": "Toda proyeccion tiene nucleo."},
        ], "justificacion_obligatoria": True, "regla": "SP: nucleo P"}}],
    120: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'muy alto', que funcion cumple 'muy'?",
        "opciones": [
            {"id": "a", "texto": "Es el especificador del SA", "correcta": True, "razon": "Los adverbios de grado funcionan como especificadores del SA."},
            {"id": "b", "texto": "Es el nucleo del SA", "correcta": False, "razon": "El nucleo es 'alto' (A)."},
            {"id": "c", "texto": "Es el complemento", "correcta": False, "razon": "El complemento iria a la derecha."},
        ], "justificacion_obligatoria": True, "regla": "SA: muy = especificador"}}],
    121: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'muy rapidamente', cual es el nucleo del SAdv?",
        "opciones": [
            {"id": "a", "texto": "rapidamente", "correcta": True, "razon": "El adverbio es el nucleo del SAdv."},
            {"id": "b", "texto": "muy", "correcta": False, "razon": "Es el especificador."},
            {"id": "c", "texto": "No tiene nucleo", "correcta": False, "razon": "Todo sintagma tiene nucleo."},
        ], "justificacion_obligatoria": True, "regla": "SAdv: nucleo Adv"}}],
    122: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'que Juan venga', cual es el nucleo del SC?",
        "opciones": [
            {"id": "a", "texto": "que", "correcta": True, "razon": "El complementante 'que' es el nucleo C."},
            {"id": "b", "texto": "Juan", "correcta": False, "razon": "Es el especificador del ST."},
            {"id": "c", "texto": "venga", "correcta": False, "razon": "Es el verbo del ST."},
        ], "justificacion_obligatoria": True, "regla": "SC: nucleo C"}}],
    123: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan lee', Juan ocupa que posicion en el ST?",
        "opciones": [
            {"id": "a", "texto": "Especificador del ST", "correcta": True, "razon": "El sujeto ocupa el Esp del ST."},
            {"id": "b", "texto": "Nucleo del ST", "correcta": False, "razon": "El nucleo es T (tiempo)."},
            {"id": "c", "texto": "Complemento del ST", "correcta": False, "razon": "El complemento es el SV."},
        ], "justificacion_obligatoria": True, "regla": "Sujeto = Esp del ST"}}],
    124: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que aporta el nucleo T a la oracion?",
        "opciones": [
            {"id": "a", "texto": "Tiempo y concordancia", "correcta": True, "razon": "T alberga rasgos de tiempo y concordancia."},
            {"id": "b", "texto": "Solo tiempo", "correcta": False, "razon": "Tambien concordancia."},
            {"id": "c", "texto": "Solo concordancia", "correcta": False, "razon": "Tambien tiempo."},
        ], "justificacion_obligatoria": True, "regla": "T = tiempo + concordancia"}}],
    125: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que valores tipicos tiene el nucleo C?",
        "opciones": [
            {"id": "a", "texto": "que, si, para", "correcta": True, "razon": "Los complementantes tipicos del castellano."},
            {"id": "b", "texto": "el, la, los", "correcta": False, "razon": "Son determinantes (D)."},
            {"id": "c", "texto": "muy, poco", "correcta": False, "razon": "Son adverbios."},
        ], "justificacion_obligatoria": True, "regla": "C: que, si, para"}}],
    126: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'el libro', cual es el nucleo D?",
        "opciones": [
            {"id": "a", "texto": "el", "correcta": True, "razon": "El articulo es el nucleo D."},
            {"id": "b", "texto": "libro", "correcta": False, "razon": "Es el SN complemento."},
            {"id": "c", "texto": "No hay D", "correcta": False, "razon": "El es D."},
        ], "justificacion_obligatoria": True, "regla": "D: articulo el"}}],
    127: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada concordancia: T (sujeto-verbo) o D (articulo-sustantivo)",
        "oraciones": [
            {"texto": "los ninos cantan", "categoria_correcta": "T"},
            {"texto": "las casas bonitas", "categoria_correcta": "D"},
        ],
        "categorias": ["T", "D"]}}],
    128: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Como se analiza la oracion simple en la GGT?",
        "opciones": [
            {"id": "a", "texto": "Como un ST: [Esp [T' T SV]]", "correcta": True, "razon": "La oracion simple es un ST."},
            {"id": "b", "texto": "Como un SC", "correcta": False, "razon": "El SC es para subordinadas."},
            {"id": "c", "texto": "Como un SN", "correcta": False, "razon": "El SN es un sintagma nominal."},
        ], "justificacion_obligatoria": True, "regla": "Oracion simple = ST"}}],
    129: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Maria dijo que Juan canta', que es 'que Juan canta'?",
        "opciones": [
            {"id": "a", "texto": "Un SC (sintagma complementante)", "correcta": True, "razon": "El complementante 'que' introduce un SC."},
            {"id": "b", "texto": "Un SN", "correcta": False, "razon": "No es un sintagma nominal."},
            {"id": "c", "texto": "Un SP", "correcta": False, "razon": "No empieza por preposicion."},
        ], "justificacion_obligatoria": True, "regla": "SC = que + ST"}}],
    130: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que representa un diagrama arboreo?",
        "opciones": [
            {"id": "a", "texto": "La estructura jerarquica de constituyentes", "correcta": True, "razon": "Nodos = categorias, hojas = palabras."},
            {"id": "b", "texto": "Una lista de palabras", "correcta": False, "razon": "Es una jerarquia, no una lista."},
            {"id": "c", "texto": "Un arbol genealogico de palabras", "correcta": False, "razon": "No es eso."},
        ], "justificacion_obligatoria": True, "regla": "Arbol = jerarquia de constituyentes"}}],
}
EJERCICIOS.update(EJERCICIOS_B)


TECNICAS_31_35 = [
    {"numero": 131, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Que es una transformacion",
     "teoria": "Una transformacion es una operacion formal que convierte una estructura en otra. En la GGT clasica (1957, 1965), las transformaciones mapean la estructura profunda en la estructura superficial.",
     "explicacion": "Ejemplo: la transformacion de pasiva convierte 'El nino lee el libro' (EP) en 'El libro es leido por el nino' (ES). En el minimalismo, el concepto de transformacion se reduce a Move (movimiento).",
     "regla": "Transformacion: operacion que mapea una estructura a otra",
     "ejemplo_correcto": "La pasiva es una transformacion de activa a pasiva.",
     "ejemplo_incorrecto": "Las transformaciones no cambian la estructura."},
    {"numero": 132, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento-alfa (muevase alfa)",
     "teoria": "El movimiento-alfa es el principio general que dice: mueve cualquier categoria a cualquier posicion, pero solo si es necesario.",
     "explicacion": "Alfa es una variable que puede ser cualquier categoria (SN, V, qu, etc). El movimiento no es libre: solo ocurre para satisfacer un rasgo o una necesidad estructural. En el minimalismo se llama simplemente Move.",
     "regla": "Muevase alfa: mueve X a Y si es necesario",
     "ejemplo_correcto": "En una interrogativa, el pronombre-qu se mueve a la posicion de C.",
     "ejemplo_incorrecto": "El movimiento-alfa permite mover cualquier cosa sin restriccion."},
    {"numero": 133, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Huella (trace) y cadena",
     "teoria": "Cuando un elemento se mueve, deja una huella (trace, t) en su posicion original. El elemento movido y su huella forman una cadena.",
     "explicacion": "Ejemplo: en 'Que compro Juan t?', 'que' se movio desde la posicion de objeto (t) a la posicion inicial. La huella t marca donde estaba originalmente. La cadena conecta el elemento movido con su huella.",
     "regla": "Huella t: posicion original. Cadena: elemento movido + huella",
     "ejemplo_correcto": "En 'que compro Juan t', t es la huella del objeto.",
     "ejemplo_incorrecto": "El movimiento no deja rastro."},
    {"numero": 134, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento del verbo a T",
     "teoria": "En algunas lenguas el verbo se mueve desde su posicion en SV a la posicion del nucleo T (tiempo).",
     "explicacion": "En frances, 'Jean mange souvent des pommes' -> 'Jean mange souvent' (el verbo sube). En ingles, el verbo se queda en SV. En castellano, el verbo sube a T. El movimiento V->T esta motivado por la concordancia con el sujeto.",
     "regla": "V->T: el verbo sube a T en castellano",
     "ejemplo_correcto": "En castellano 'Juan canta', el verbo sube a T para concordar con el sujeto.",
     "ejemplo_incorrecto": "El verbo nunca se mueve a T."},
    {"numero": 135, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento del sujeto a ST",
     "teoria": "El sujeto se genera en el especificador del SV (posicion de agente) y se mueve al especificador del ST para satisfacer el rasgo EPP de T.",
     "explicacion": "En 'Juan canta', 'Juan' se genera en [Esp SV] y se mueve a [Esp ST]. El rasgo EPP de T exige que el especificador del ST no este vacio. Por eso el sujeto sube.",
     "regla": "Sujeto: Esp SV -> Esp ST (rasgo EPP)",
     "ejemplo_correcto": "El sujeto se mueve de Esp-SV a Esp-ST.",
     "ejemplo_incorrecto": "El sujeto se queda siempre en el SV."},
]
TECNICAS.extend(TECNICAS_31_35)


TECNICAS_36_40 = [
    {"numero": 136, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento-qu: interrogativas",
     "teoria": "En interrogativas, el pronombre interrogativo (que, quien, cuando, donde, como) se mueve desde su posicion original a la posicion inicial de la oracion (C).",
     "explicacion": "Ejemplo: 'Que compro Juan?' -> 'que' se mueve del objeto (t) a C. En ingles el movimiento-qu es visible ('What did John buy t?'), en chino no hay movimiento visible (queda in situ). El castellano tiene movimiento-qu visible.",
     "regla": "Movimiento-qu: pronombre interrogativo -> C",
     "ejemplo_correcto": "En 'Que compro Juan t?', que esta en C.",
     "ejemplo_incorrecto": "En castellano el pronombre-qu nunca se mueve."},
    {"numero": 137, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento-qu: relativas",
     "teoria": "En oraciones relativas, el pronombre relativo se mueve desde su posicion original al inicio de la subordinada (C).",
     "explicacion": "Ejemplo: 'El libro que compre t es bueno' -> 'que' se mueve del objeto (t) a C. El relativo encabeza la subordinada. Igual que en interrogativas, deja huella.",
     "regla": "Relativas: relativo se mueve a C",
     "ejemplo_correcto": "En 'el libro que compre t', que esta en C.",
     "ejemplo_incorrecto": "Los relativos no se mueven."},
    {"numero": 138, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento del nucleo",
     "teoria": "El movimiento del nucleo es el desplazamiento de un nucleo (V, T, C) a otra posicion de nucleo.",
     "explicacion": "Ejemplo: el verbo se mueve de V a T (V->T). En interrogativas en ingles, el auxiliar se mueve de T a C ('Did he buy t?'). En castellano no hay movimiento T->C visible.",
     "regla": "Movimiento de nucleo: X0 -> Y0 (V->T, T->C)",
     "ejemplo_correcto": "En ingles 'did he buy t', el auxiliar sube a C.",
     "ejemplo_incorrecto": "Los nucleos no se mueven."},
    {"numero": 139, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento de constituyentes",
     "teoria": "El movimiento de constituyentes desplaza un sintagma completo (SN, SP, SC) a otra posicion, no solo el nucleo.",
     "explicacion": "Ejemplo: en pasivas, el objeto SN se mueve al sujeto: 'El libro fue comprado t'. En topicalizacion, el SN se mueve al inicio: 'El libro, Juan compro t'. El constituyente mueve mantiene su integridad.",
     "regla": "Movimiento de constituyentes: SN/SP/SC -> nueva posicion",
     "ejemplo_correcto": "En 'el libro fue comprado t', el SN sube a sujeto.",
     "ejemplo_incorrecto": "Solo se mueven palabras sueltas."},
    {"numero": 140, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Restriccion de isla",
     "teoria": "La restriccion de isla (Ross, 1967) prohibe mover un elemento fuera de ciertas estructuras (islas), como subordinadas o sintagmas nominales complejos.",
     "explicacion": "Ejemplo: '*Quien dijo Maria [que compro el libro t]?' es agramatical: 'quien' no puede salir del SC. La subordinada es una isla. Restricciones: isla del SC, isla del SN, isla del sujeto.",
     "regla": "Isla: no se puede mover un elemento fuera de ciertas estructuras",
     "ejemplo_correcto": "Las subordinadas son islas: no extraes el objeto.",
     "ejemplo_incorrecto": "Puedes mover cualquier elemento desde cualquier posicion."},
]
TECNICAS.extend(TECNICAS_36_40)


TECNICAS_41_45 = [
    {"numero": 141, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Principio de subyacencia",
     "teoria": "El principio de subyacencia (Chomsky, 1973) prohibe mover un elemento a traves de mas de un nodo limite (SC o SN) en un solo paso.",
     "explicacion": "Ejemplo: no puedes mover 'quien' desde dentro de un SC a otra oracion principal directamente. El movimiento debe ser ciclico: primero al SC, luego al siguiente. Cada paso atraviesa un nodo limite.",
     "regla": "Subyacencia: no saltar mas de un nodo limite por paso",
     "ejemplo_correcto": "El movimiento-qu es ciclico (paso por cada SC).",
     "ejemplo_incorrecto": "Puedes mover un elemento a traves de muchos SC en un solo paso."},
    {"numero": 142, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Restriccion de sujeto complejo",
     "teoria": "La restriccion de sujeto complejo prohibe extraer un elemento de un SN que esta en posicion de sujeto.",
     "explicacion": "Ejemplo: '*De quien [la madre t] es famosa?' es agramatical: 'de quien' no puede salir del SN sujeto. La restriccion protege el sujeto como isla. Solo se puede extraer del objeto.",
     "regla": "Sujeto complejo = isla. Solo se extrae de objetos",
     "ejemplo_correcto": "No puedes extraer de un SN en posicion de sujeto.",
     "ejemplo_incorrecto": "Puedes extraer cualquier cosa del sujeto."},
    {"numero": 143, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento-A vs movimiento-A-barra",
     "teoria": "El movimiento-A (movimiento de argumento) desplaza un elemento a una posicion de argumento (Esp-ST, Esp-SV). El movimiento-A-barra lo hace a una posicion no-argumental (C, adjuntos).",
     "explicacion": "Movimiento-A: sujeto de SV a sujeto de ST, objeto a sujeto en pasivas. Movimiento-A-barra: pronombre-qu a C, topicalizacion a la izquierda. Los dos tipos tienen propiedades distintas de ligamiento.",
     "regla": "Mov-A: a posicion de argumento. Mov-A-barra: a no-argumento",
     "ejemplo_correcto": "El pronombre-qu hace movimiento-A-barra a C.",
     "ejemplo_incorrecto": "Todo movimiento es igual."},
    {"numero": 144, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Insercion (do-support, hacer en espanol)",
     "teoria": "En algunas lenguas, cuando no hay auxiliar para mover a C, se inserta un auxiliar de apoyo. En ingles es 'do', en espanol no hay equivalente directo.",
     "explicacion": "Ejemplo: 'Did he buy?' — se inserta 'did' porque no hay auxiliar. En castellano no hay do-support: 'Compro?' funciona sin auxiliar. En preguntas negativas en ingles: 'Didn't he buy?'.",
     "regla": "Do-support: insertar auxiliar cuando falta",
     "ejemplo_correcto": "En ingles 'Did he buy?' inserta 'did'.",
     "ejemplo_incorrecto": "El castellano tambien usa do-support."},
    {"numero": 145, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Borrado en estructura superficial",
     "teoria": "En la GGT clasica, el borrado (deletion) elimina elementos en la estructura superficial que no se pronuncian pero son interpretables.",
     "explicacion": "Ejemplo: 'Juan compro un libro y Maria t tambien' — se borra 'compro un libro' bajo identidad. Otro: elipsis del verbo en respuestas: '-Quien vino? -Juan (vino)'. El borrado no es lo mismo que el movimiento.",
     "regla": "Borrado: eliminar elementos en ES bajo identidad",
     "ejemplo_correcto": "'Juan compro un libro y Maria tambien' borra 'compro un libro'.",
     "ejemplo_incorrecto": "El borrado y el movimiento son lo mismo."},
]
TECNICAS.extend(TECNICAS_41_45)


TECNICAS_46_50 = [
    {"numero": 146, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Elipsis verbal",
     "teoria": "La elipsis verbal es la omision de un verbo o sintagma verbal en contexto, recuperable del antecedente.",
     "explicacion": "Ejemplo: 'Juan compro un libro y Maria tambien (compro un libro)'. El verbo 'compro' se elide pero se interpreta. La elipsis es una transformacion de borrado. Requiere identidad con el antecedente.",
     "regla": "Elipsis verbal: omision recuperable del SV",
     "ejemplo_correcto": "En 'Juan comio y Maria tambien', se elide 'comio'.",
     "ejemplo_incorrecto": "La elipsis verbal no requiere antecedente."},
    {"numero": 147, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Sujeto nulo (pro-drop) en castellano",
     "teoria": "El castellano es una lengua pro-drop: permite omitir el sujeto pronominal porque el verbo lleva la informacion de persona y numero.",
     "explicacion": "Ejemplo: 'Canto' = 'Yo canto'. El sujeto se recupera por la desinencia verbal. El ingles es no pro-drop: '*Sing' no es posible. El parametro pro-drop distingue lenguas. Castellano, italiano, griego son pro-drop; ingles, frances (parcialmente) no.",
     "regla": "Pro-drop: se puede omitir el sujeto (castellano)",
     "ejemplo_correcto": "En castellano 'canto' funciona sin 'yo'.",
     "ejemplo_incorrecto": "En ingles 'sing' funciona sin 'I'."},
    {"numero": 148, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Topicalizacion",
     "teoria": "La topicalizacion mueve un constituyente al inicio de la oracion para marcarlo como topico (informacion conocida).",
     "explicacion": "Ejemplo: 'El libro, Juan lo compro' — 'el libro' se mueve a la posicion inicial, y aparece un pronombre resuntivo 'lo'. El topico es lo que se comenta. La topicalizacion es movimiento-A-barra.",
     "regla": "Topicalizacion: constituyente -> inicio (topico)",
     "ejemplo_correcto": "En 'el libro, Juan lo compro', 'el libro' es topico.",
     "ejemplo_incorrecto": "La topicalizacion no mueve nada."},
    {"numero": 149, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Focalizacion",
     "teoria": "La focalizacion marca un constituyente como foco (informacion nueva o contrastiva), generalmente con movimiento o prosodia especial.",
     "explicacion": "Ejemplo: 'A JUAN vi (no a Pedro)' — el foco 'a Juan' se marca con prosodia y/o movimiento. La focalizacion puede ser in situ (solo prosodia) o con movimiento. En castellano el foco contrastivo suele ir al final.",
     "regla": "Focalizacion: marca de informacion nueva o contrastiva",
     "ejemplo_correcto": "En 'A JUAN vi', 'a Juan' es foco contrastivo.",
     "ejemplo_incorrecto": "El foco y el topico son lo mismo."},
    {"numero": 150, "bloque": "C", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Dislocacion a la izquierda",
     "teoria": "La dislocacion a la izquierda mueve un constituyente al inicio de la oracion, dejando un pronombre resuntivo en su posicion original.",
     "explicacion": "Ejemplo: 'El libro, lo compre ayer' — 'el libro' se disloca a la izquierda; 'lo' es el pronombre resuntivo. Es similar a la topicalizacion, pero mas marcada. La dislocacion es frecuente en castellano coloquial.",
     "regla": "Dislocacion: constituyente -> inicio + pronombre resuntivo",
     "ejemplo_correcto": "En 'el libro, lo compre', 'lo' es resuntivo.",
     "ejemplo_incorrecto": "La dislocacion no deja pronombre."},
]
TECNICAS.extend(TECNICAS_46_50)


EJERCICIOS_C = {
    131: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es una transformacion en la GGT?",
        "opciones": [
            {"id": "a", "texto": "Una operacion que convierte una estructura en otra", "correcta": True, "razon": "Mapea EP en ES."},
            {"id": "b", "texto": "Un cambio de palabra", "correcta": False, "razon": "Es estructural."},
            {"id": "c", "texto": "Un error del hablante", "correcta": False, "razon": "No es error."},
        ], "justificacion_obligatoria": True, "regla": "Transformacion: EP -> ES"}}],
    132: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el principio de 'movimiento-alfa'?",
        "opciones": [
            {"id": "a", "texto": "Mueve cualquier categoria si es necesario", "correcta": True, "razon": "Solo si satisface una necesidad estructural."},
            {"id": "b", "texto": "Mueve cualquier cosa sin restriccion", "correcta": False, "razon": "No es libre."},
            {"id": "c", "texto": "No se mueve nada", "correcta": False, "razon": "Hay movimiento."},
        ], "justificacion_obligatoria": True, "regla": "Muevase alfa: solo si es necesario"}}],
    133: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es una huella (trace) en sintaxis generativa?",
        "opciones": [
            {"id": "a", "texto": "La posicion original que deja un elemento movido", "correcta": True, "razon": "Marca donde estaba antes del movimiento."},
            {"id": "b", "texto": "La posicion final del elemento", "correcta": False, "razon": "Esa es la nueva posicion."},
            {"id": "c", "texto": "Un error de escritura", "correcta": False, "razon": "Es una marca teorica."},
        ], "justificacion_obligatoria": True, "regla": "Huella = posicion original"}}],
    134: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En castellano, el verbo sube a T?",
        "opciones": [
            {"id": "a", "texto": "Si, el verbo sube a T", "correcta": True, "razon": "En castellano hay movimiento V->T."},
            {"id": "b", "texto": "No, el verbo se queda en SV", "correcta": False, "razon": "Eso pasa en ingles."},
            {"id": "c", "texto": "Solo en infinitivo", "correcta": False, "razon": "El infinitivo no tiene T."},
        ], "justificacion_obligatoria": True, "regla": "Castellano: V->T"}}],
    135: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Por que el sujeto sube al especificador del ST?",
        "opciones": [
            {"id": "a", "texto": "Para satisfacer el rasgo EPP de T", "correcta": True, "razon": "T exige que su Esp este lleno."},
            {"id": "b", "texto": "Porque no cabe en SV", "correcta": False, "razon": "Cabe pero T lo atrae."},
            {"id": "c", "texto": "Por razones estilisticas", "correcta": False, "razon": "Es estructural."},
        ], "justificacion_obligatoria": True, "regla": "EPP: T exige Esp lleno"}}],
    136: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Que compro Juan t?', que es 't'?",
        "opciones": [
            {"id": "a", "texto": "La huella del objeto movido", "correcta": True, "razon": "'Que' se movio desde la posicion de objeto."},
            {"id": "b", "texto": "Un error de tipeo", "correcta": False, "razon": "Es una huella."},
            {"id": "c", "texto": "El sujeto", "correcta": False, "razon": "El sujeto es Juan."},
        ], "justificacion_obligatoria": True, "regla": "t = huella del objeto"}}],
    137: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'el libro que compre t', que funcion tiene 'que'?",
        "opciones": [
            {"id": "a", "texto": "Relativo movido a C", "correcta": True, "razon": "'Que' es el relativo que sube a C."},
            {"id": "b", "texto": "Complementante de una sustantiva", "correcta": False, "razon": "Es relativo, no complementante."},
            {"id": "c", "texto": "Conjuncion", "correcta": False, "razon": "No es conjuncion."},
        ], "justificacion_obligatoria": True, "regla": "Relativo -> C"}}],
    138: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es el movimiento de nucleo?",
        "opciones": [
            {"id": "a", "texto": "El desplazamiento de un nucleo (V, T, C) a otra posicion de nucleo", "correcta": True, "razon": "V->T, T->C."},
            {"id": "b", "texto": "El movimiento de un SN", "correcta": False, "razon": "Eso es movimiento de constituyentes."},
            {"id": "c", "texto": "El movimiento de una palabra suelta", "correcta": False, "razon": "Solo nucleos."},
        ], "justificacion_obligatoria": True, "regla": "Movimiento de nucleo: X0->Y0"}}],
    139: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'el libro fue comprado t', que tipo de movimiento hay?",
        "opciones": [
            {"id": "a", "texto": "Movimiento de constituyente (objeto a sujeto)", "correcta": True, "razon": "En pasivas el objeto sube a sujeto."},
            {"id": "b", "texto": "Movimiento de nucleo", "correcta": False, "razon": "No es un nucleo."},
            {"id": "c", "texto": "Movimiento-qu", "correcta": False, "razon": "No es interrogativo."},
        ], "justificacion_obligatoria": True, "regla": "Pasiva: objeto -> sujeto"}}],
    140: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que prohibe la restriccion de isla?",
        "opciones": [
            {"id": "a", "texto": "Mover un elemento fuera de ciertas estructuras (islas)", "correcta": True, "razon": "Las subordinadas son islas."},
            {"id": "b", "texto": "Mover cualquier elemento", "correcta": False, "razon": "Todo lo contrario."},
            {"id": "c", "texto": "Construir oraciones", "correcta": False, "razon": "No es eso."},
        ], "justificacion_obligatoria": True, "regla": "Isla: no se extrae"}}],
    141: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el principio de subyacencia?",
        "opciones": [
            {"id": "a", "texto": "No se puede saltar mas de un nodo limite por paso", "correcta": True, "razon": "Movimiento ciclico."},
            {"id": "b", "texto": "Se puede saltar cualquier nodo", "correcta": False, "razon": "No es libre."},
            {"id": "c", "texto": "No hay movimiento", "correcta": False, "razon": "Si hay."},
        ], "justificacion_obligatoria": True, "regla": "Subyacencia: 1 nodo por paso"}}],
    142: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que prohibe la restriccion de sujeto complejo?",
        "opciones": [
            {"id": "a", "texto": "Extraer un elemento de un SN en posicion de sujeto", "correcta": True, "razon": "El sujeto es isla."},
            {"id": "b", "texto": "Extraer de un objeto", "correcta": False, "razon": "Del objeto si se puede."},
            {"id": "c", "texto": "Extraer de una preposicion", "correcta": False, "razon": "No es la restriccion."},
        ], "justificacion_obligatoria": True, "regla": "Sujeto complejo = isla"}}],
    143: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que distingue movimiento-A de movimiento-A-barra?",
        "opciones": [
            {"id": "a", "texto": "Mov-A va a argumento; Mov-A-barra va a no-argumento", "correcta": True, "razon": "Posiciones distintas."},
            {"id": "b", "texto": "Son identicos", "correcta": False, "razon": "Tienen propiedades distintas."},
            {"id": "c", "texto": "Mov-A es solo de sujetos", "correcta": False, "razon": "No es exacto."},
        ], "justificacion_obligatoria": True, "regla": "Mov-A: argumento; A-barra: no"}}],
    144: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El castellano tiene do-support como el ingles?",
        "opciones": [
            {"id": "a", "texto": "No, el castellano no tiene do-support", "correcta": True, "razon": "No hay auxiliar de apoyo."},
            {"id": "b", "texto": "Si, usa 'hacer'", "correcta": False, "razon": "No es do-support."},
            {"id": "c", "texto": "Solo en pasado", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": True, "regla": "Castellano: sin do-support"}}],
    145: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es el borrado en la GGT?",
        "opciones": [
            {"id": "a", "texto": "Eliminar elementos en ES bajo identidad", "correcta": True, "razon": "Es una transformacion."},
            {"id": "b", "texto": "Mover un elemento", "correcta": False, "razon": "Es diferente."},
            {"id": "c", "texto": "Un error de escritura", "correcta": False, "razon": "Es formal."},
        ], "justificacion_obligatoria": True, "regla": "Borrado: elimina en ES"}}],
    146: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan comio y Maria tambien', que se elide?",
        "opciones": [
            {"id": "a", "texto": "El verbo 'comio' en la segunda oracion", "correcta": True, "razon": "Elipsis verbal."},
            {"id": "b", "texto": "El sujeto 'Maria'", "correcta": False, "razon": "El sujeto se mantiene."},
            {"id": "c", "texto": "Nada", "correcta": False, "razon": "Se elide el SV."},
        ], "justificacion_obligatoria": True, "regla": "Elipsis: SV omitido"}}],
    147: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es el parametro pro-drop?",
        "opciones": [
            {"id": "a", "texto": "Permite omitir el sujeto pronominal (castellano)", "correcta": True, "razon": "Castellano es pro-drop."},
            {"id": "b", "texto": "Permite omitir el verbo", "correcta": False, "razon": "No es eso."},
            {"id": "c", "texto": "Obliga a omitir el objeto", "correcta": False, "razon": "No es eso."},
        ], "justificacion_obligatoria": True, "regla": "Pro-drop: sujeto omitido"}}],
    148: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'el libro, Juan lo compro', que es 'el libro'?",
        "opciones": [
            {"id": "a", "texto": "El topico (dislocado a la izquierda)", "correcta": True, "razon": "Marca informacion conocida."},
            {"id": "b", "texto": "El sujeto", "correcta": False, "razon": "El sujeto es Juan."},
            {"id": "c", "texto": "El objeto en su posicion original", "correcta": False, "razon": "Se movio al inicio."},
        ], "justificacion_obligatoria": True, "regla": "Topico: al inicio"}}],
    149: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'A JUAN vi', que funcion tiene 'a Juan'?",
        "opciones": [
            {"id": "a", "texto": "Foco contrastivo", "correcta": True, "razon": "Marca informacion nueva o contrastiva."},
            {"id": "b", "texto": "Topico", "correcta": False, "razon": "Es foco, no topico."},
            {"id": "c", "texto": "Sujeto", "correcta": False, "razon": "El sujeto es 'yo' (omitido)."},
        ], "justificacion_obligatoria": True, "regla": "Foco: informacion nueva"}}],
    150: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'el libro, lo compre', que es 'lo'?",
        "opciones": [
            {"id": "a", "texto": "Pronombre resuntivo", "correcta": True, "razon": "Recupera la posicion original del objeto."},
            {"id": "b", "texto": "El topico", "correcta": False, "razon": "El topico es 'el libro'."},
            {"id": "c", "texto": "El sujeto", "correcta": False, "razon": "El sujeto es 'yo' (omitido)."},
        ], "justificacion_obligatoria": True, "regla": "Dislocacion: pronombre resuntivo"}}],
}
EJERCICIOS.update(EJERCICIOS_C)


TECNICAS_51_55 = [
    {"numero": 151, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Caso abstracto vs caso morfologico",
     "teoria": "El caso abstracto es una marca sintactica invisible asignada por un nucleo (T, V, P). El caso morfologico es la manifestacion visible (terminaciones, pronombres).",
     "explicacion": "En castellano el caso morfologico solo aparece en pronombres (yo/me/mi, tu/te/ti). En latin y aleman aparece tambien en sustantivos y adjetivos. La GGT estudia el caso abstracto como requisito universal.",
     "regla": "Caso abstracto: invisible (T, V, P). Morfologico: visible (pronombres)",
     "ejemplo_correcto": "En 'yo lo vi', 'yo' (nominativo) y 'lo' (acusativo) tienen caso morfologico visible.",
     "ejemplo_incorrecto": "El caso abstracto y el morfologico son identicos en castellano."},
    {"numero": 152, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Caso nominativo",
     "teoria": "El caso nominativo lo asigna el nucleo T (tiempo) al sujeto de la oracion finita.",
     "explicacion": "Ejemplo: 'Juan canta'. 'Juan' recibe caso nominativo de T. En pronombres: 'yo' (nominativo). Si el sujeto no recibe caso nominativo, la oracion es agramatical: *'Juan cantar' (infinitivo no asigna caso).",
     "regla": "Nominativo: T -> sujeto finito",
     "ejemplo_correcto": "En 'yo canto', 'yo' lleva nominativo.",
     "ejemplo_incorrecto": "El sujeto puede quedar sin caso."},
    {"numero": 153, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Caso acusativo",
     "teoria": "El caso acusativo lo asigna el nucleo V (verbo transitivo) al complemento directo.",
     "explicacion": "Ejemplo: 'Juan compro el libro'. 'El libro' recibe caso acusativo de V. En pronombres: 'lo/la' (acusativo). Los verbos transitivos asignan caso acusativo; los intransitivos no.",
     "regla": "Acusativo: V transitivo -> CD",
     "ejemplo_correcto": "En 'Juan lo compro', 'lo' lleva acusativo.",
     "ejemplo_incorrecto": "El acusativo lo asigna T."},
    {"numero": 154, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Caso dativo",
     "teoria": "El caso dativo lo asigna el nucleo V (o P) al complemento indirecto.",
     "explicacion": "Ejemplo: 'Juan dio un libro a Maria'. 'A Maria' recibe caso dativo (o caso oblicuo por P). En pronombres: 'le/les'. Los verbos de transferencia asignan dativo al receptor.",
     "regla": "Dativo: V/P -> CI",
     "ejemplo_correcto": "En 'le di el libro', 'le' lleva dativo.",
     "ejemplo_incorrecto": "El dativo lo asigna T."},
    {"numero": 155, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Caso genitivo",
     "teoria": "El caso genitivo lo asigna el nucleo N al complemento posesivo del sintagma nominal. En castellano se realiza con 'de'.",
     "explicacion": "Ejemplo: 'la casa de Juan'. 'De Juan' recibe caso genitivo del nucleo N 'casa'. En pronombres posesivos: 'mio, tuyo'. En latin y aleman el genitivo tiene caso morfologico propio; en castellano se hace con 'de'.",
     "regla": "Genitivo: N -> complemento posesivo ('de Juan')",
     "ejemplo_correcto": "En 'la casa de Juan', 'de Juan' lleva genitivo.",
     "ejemplo_incorrecto": "El genitivo lo asigna V."},
]
TECNICAS.extend(TECNICAS_51_55)


TECNICAS_56_60 = [
    {"numero": 156, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Asignacion de caso por T (nominativo)",
     "teoria": "El nucleo T asigna caso nominativo a su especificador (el sujeto) bajo concordancia.",
     "explicacion": "Ejemplo: 'Juan canta'. T (presente, 3a sing) asigna nominativo a 'Juan'. Si el sujeto esta en infinitivo, T no puede asignar nominativo y el sujeto sube a otra oracion ('Quiero [que Juan cante]').",
     "regla": "T asigna nominativo al Esp (sujeto)",
     "ejemplo_correcto": "En 'Juan canta', T asigna nominativo a Juan.",
     "ejemplo_incorrecto": "T asigna caso acusativo."},
    {"numero": 157, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Asignacion de caso por V (acusativo)",
     "teoria": "El verbo transitivo asigna caso acusativo a su complemento directo.",
     "explicacion": "Ejemplo: 'Juan compro el libro'. V ('compro') asigna acusativo a 'el libro'. Los verbos intransitivos no asignan acusativo. En pasivas, el objeto sube a sujeto y recibe nominativo de T ('El libro fue comprado t').",
     "regla": "V transitivo asigna acusativo al CD",
     "ejemplo_correcto": "En 'compro el libro', V asigna acusativo a 'el libro'.",
     "ejemplo_incorrecto": "El verbo intransitivo asigna acusativo."},
    {"numero": 158, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Asignacion de caso por P (oblicuo)",
     "teoria": "La preposicion asigna caso oblicuo (o caso de P) a su complemento.",
     "explicacion": "Ejemplo: 'con Juan', 'de Maria', 'para ti'. P ('con', 'de', 'para') asigna caso oblicuo a su complemento. En pronombres: 'conmigo', 'contigo', 'para mi'. El caso oblicuo no es nominativo, acusativo ni dativo: es un caso 'por defecto' de P.",
     "regla": "P asigna caso oblicuo a su complemento",
     "ejemplo_correcto": "En 'conmigo', 'migo' (o 'mi') lleva caso oblicuo de P.",
     "ejemplo_incorrecto": "P asigna nominativo."},
    {"numero": 159, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Filtro de caso",
     "teoria": "El filtro de caso (Chomsky, 1981) establece que todo SN explicito debe recibir caso. Si un SN no recibe caso, la oracion es agramatical.",
     "explicacion": "Ejemplo: '*Juan cantar' es agramatical porque 'Juan' no recibe caso de T (infinitivo). En cambio, 'Quiero que Juan cante' es correcto porque T asigna nominativo. El filtro garantiza que todo SN tenga caso.",
     "regla": "Filtro de caso: todo SN explicito necesita caso",
     "ejemplo_correcto": "'Quiero que Juan cante' asigna caso a Juan.",
     "ejemplo_incorrecto": "'Juan cantar' es gramatical."},
    {"numero": 160, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Papeles tematicos: agente",
     "teoria": "El papel tematico de agente es el que realiza la accion del verbo. Se asigna a la posicion de especificador del SV.",
     "explicacion": "Ejemplo: 'Juan compro el libro'. 'Juan' es agente (el que compra). El agente se asigna en [Esp SV]. En pasivas, el agente puede aparecer en 'por': 'El libro fue comprado por Juan'. En pasivas reflejas se omite.",
     "regla": "Agente: realiza la accion, en Esp SV",
     "ejemplo_correcto": "En 'Juan compro', Juan es agente.",
     "ejemplo_incorrecto": "El agente se asigna a T."},
]
TECNICAS.extend(TECNICAS_56_60)


TECNICAS_61_65 = [
    {"numero": 161, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Tema y paciente",
     "teoria": "El tema es el elemento que sufre el cambio o es afectado por la accion. El paciente es el que recibe la accion de forma directa.",
     "explicacion": "Ejemplo: 'Juan compro el libro'. 'El libro' es tema/paciente (el que se compra). 'Juan rompio la ventana': 'la ventana' es paciente. Se asignan en la posicion de complemento del V.",
     "regla": "Tema/paciente: complemento del V (afectado)",
     "ejemplo_correcto": "En 'Juan rompio la ventana', 'la ventana' es paciente.",
     "ejemplo_incorrecto": "El paciente se asigna en el sujeto."},
    {"numero": 162, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Meta, origen, locativo",
     "teoria": "Estos papeles tematicos los asignan los verbos de movimiento y las preposiciones. Meta es destino, origen es punto de partida, locativo es lugar.",
     "explicacion": "Ejemplo: 'Voy a Madrid' (meta = a Madrid), 'Vengo de Bogota' (origen = de Bogota), 'Vivo en Lima' (locativo = en Lima). Se asignan en el complemento del V o dentro del SP.",
     "regla": "Meta: destino. Origen: punto de partida. Locativo: lugar",
     "ejemplo_correcto": "En 'voy a Madrid', 'a Madrid' es meta.",
     "ejemplo_incorrecto": "La meta es lo mismo que el origen."},
    {"numero": 163, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Criterio tematico",
     "teoria": "El criterio tematico (Chomsky, 1981) establece que cada argumento recibe exactamente un papel tematico, y cada papel tematico se asigna a un solo argumento.",
     "explicacion": "Ejemplo: en 'Juan compro el libro', 'Juan' recibe agente y 'el libro' tema. Si un SN recibiera dos papeles tematicos, o si un papel se asignara a dos SN, la oracion seria agramatical. Es una restriccion bidireccional.",
     "regla": "Criterio tematico: 1 papel por argumento, 1 argumento por papel",
     "ejemplo_correcto": "Cada SN recibe exactamente un papel tematico.",
     "ejemplo_incorrecto": "Un SN puede recibir dos papeles tematicos."},
    {"numero": 164, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Estructura argumental del verbo",
     "teoria": "La estructura argumental de un verbo es el conjunto de argumentos que exige. Cada verbo tiene una 'rejilla tematica' que especifica cuantos y cuales argumentos necesita.",
     "explicacion": "Ejemplo: 'llover' (0 argumentos, impersonal), 'dormir' (1 argumento: agente), 'comprar' (2 argumentos: agente, tema), 'dar' (3 argumentos: agente, tema, meta). Si faltan argumentos, la oracion es agramatical o cambia de sentido.",
     "regla": "Estructura argumental: argumentos que exige el verbo",
     "ejemplo_correcto": "'Comprar' exige 2 argumentos: agente y tema.",
     "ejemplo_incorrecto": "'Comprar' exige 1 argumento."},
    {"numero": 165, "bloque": "D", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Verbos inacusativos vs inergativos",
     "teoria": "Los inacusativos tienen un solo argumento que es tema/paciente (no agente). Los inergativos tienen un solo argumento que es agente.",
     "explicacion": "Ejemplo: 'llegar, nacer, morir, caer' son inacusativos (el argumento es tema). 'Llorar, correr, dormir, nadar' son inergativos (el argumento es agente). La diferencia se ve en la auxiliar: 'ha llegado' (inacusativo) vs 'ha llorado' (inergativo).",
     "regla": "Inacusativo: 1 argumento tema. Inergativo: 1 argumento agente",
     "ejemplo_correcto": "'Nacer' es inacusativo (el sujeto es tema).",
     "ejemplo_incorrecto": "'Nacer' es inergativo."},
]
TECNICAS.extend(TECNICAS_61_65)


EJERCICIOS_D = {
    151: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que distingue el caso abstracto del morfologico?",
        "opciones": [
            {"id": "a", "texto": "Abstracto: invisible (T, V, P); morfologico: visible (pronombres)", "correcta": True, "razon": "El castellano solo marca caso morfologico en pronombres."},
            {"id": "b", "texto": "Son sinonimos", "correcta": False, "razon": "Son distintos."},
            {"id": "c", "texto": "El morfologico solo existe en latin", "correcta": False, "razon": "En castellano existe en pronombres."},
        ], "justificacion_obligatoria": True, "regla": "Abstracto invisible, morfologico visible"}}],
    152: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que nucleo asigna el caso nominativo?",
        "opciones": [
            {"id": "a", "texto": "T (tiempo)", "correcta": True, "razon": "T asigna nominativo al sujeto."},
            {"id": "b", "texto": "V (verbo)", "correcta": False, "razon": "V asigna acusativo."},
            {"id": "c", "texto": "P (preposicion)", "correcta": False, "razon": "P asigna oblicuo."},
        ], "justificacion_obligatoria": True, "regla": "Nominativo: T -> sujeto"}}],
    153: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que nucleo asigna el caso acusativo?",
        "opciones": [
            {"id": "a", "texto": "V transitivo", "correcta": True, "razon": "V asigna acusativo al CD."},
            {"id": "b", "texto": "T", "correcta": False, "razon": "T asigna nominativo."},
            {"id": "c", "texto": "N", "correcta": False, "razon": "N asigna genitivo."},
        ], "justificacion_obligatoria": True, "regla": "Acusativo: V -> CD"}}],
    154: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que caso lleva 'le' en 'le di el libro'?",
        "opciones": [
            {"id": "a", "texto": "Dativo", "correcta": True, "razon": "El CI lleva dativo."},
            {"id": "b", "texto": "Acusativo", "correcta": False, "razon": "Seria 'lo'."},
            {"id": "c", "texto": "Nominativo", "correcta": False, "razon": "Seria 'el' (sujeto)."},
        ], "justificacion_obligatoria": True, "regla": "Dativo: le (CI)"}}],
    155: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'la casa de Juan', que caso lleva 'de Juan'?",
        "opciones": [
            {"id": "a", "texto": "Genitivo (asignado por N)", "correcta": True, "razon": "N asigna genitivo al complemento posesivo."},
            {"id": "b", "texto": "Nominativo", "correcta": False, "razon": "Nominativo es T."},
            {"id": "c", "texto": "Acusativo", "correcta": False, "razon": "Acusativo es V."},
        ], "justificacion_obligatoria": True, "regla": "Genitivo: N -> posesivo"}}],
    156: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan canta', quien asigna caso a 'Juan'?",
        "opciones": [
            {"id": "a", "texto": "T (presente, 3a sing)", "correcta": True, "razon": "T asigna nominativo al sujeto finito."},
            {"id": "b", "texto": "V 'canta'", "correcta": False, "razon": "V asigna acusativo."},
            {"id": "c", "texto": "Ninguno", "correcta": False, "razon": "Alguien debe asignar caso."},
        ], "justificacion_obligatoria": True, "regla": "T asigna nominativo"}}],
    157: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que pasa con el caso en 'Juan cantar' (infinitivo)?",
        "opciones": [
            {"id": "a", "texto": "Es agramatical porque 'Juan' no recibe caso", "correcta": True, "razon": "El infinitivo no asigna nominativo."},
            {"id": "b", "texto": "Es gramatical", "correcta": False, "razon": "Falta caso para el sujeto."},
            {"id": "c", "texto": "Es una pasiva", "correcta": False, "razon": "No es pasiva."},
        ], "justificacion_obligatoria": True, "regla": "Infinitivo no asigna caso"}}],
    158: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'conmigo', que caso lleva 'migo'?",
        "opciones": [
            {"id": "a", "texto": "Oblicuo (asignado por P)", "correcta": True, "razon": "P asigna caso oblicuo."},
            {"id": "b", "texto": "Nominativo", "correcta": False, "razon": "Nominativo es T."},
            {"id": "c", "texto": "Acusativo", "correcta": False, "razon": "Acusativo es V."},
        ], "justificacion_obligatoria": True, "regla": "P asigna oblicuo"}}],
    159: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el filtro de caso?",
        "opciones": [
            {"id": "a", "texto": "Todo SN explicito debe recibir caso", "correcta": True, "razon": "Si no, es agramatical."},
            {"id": "b", "texto": "Los SN pueden quedar sin caso", "correcta": False, "razon": "No es correcto."},
            {"id": "c", "texto": "Solo los pronombres necesitan caso", "correcta": False, "razon": "Todos los SN."},
        ], "justificacion_obligatoria": True, "regla": "Filtro: todo SN necesita caso"}}],
    160: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Quien es el agente en 'Juan compro el libro'?",
        "opciones": [
            {"id": "a", "texto": "Juan", "correcta": True, "razon": "El agente realiza la accion."},
            {"id": "b", "texto": "El libro", "correcta": False, "razon": "Es el tema/paciente."},
            {"id": "c", "texto": "No hay agente", "correcta": False, "razon": "Juan es agente."},
        ], "justificacion_obligatoria": True, "regla": "Agente: realiza la accion"}}],
    161: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica el papel tematico: agente (A) o tema/paciente (T)",
        "oraciones": [
            {"texto": "Juan", "categoria_correcta": "agente"},
            {"texto": "el libro", "categoria_correcta": "tema/paciente"},
            {"texto": "Maria", "categoria_correcta": "agente"},
            {"texto": "la ventana", "categoria_correcta": "tema/paciente"},
        ],
        "categorias": ["agente", "tema/paciente"]}}],
    162: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'voy a Madrid', que papel tematico es 'a Madrid'?",
        "opciones": [
            {"id": "a", "texto": "Meta", "correcta": True, "razon": "Destino del movimiento."},
            {"id": "b", "texto": "Origen", "correcta": False, "razon": "Origen seria 'de Madrid'."},
            {"id": "c", "texto": "Agente", "correcta": False, "razon": "No realiza la accion."},
        ], "justificacion_obligatoria": True, "regla": "Meta: destino del movimiento"}}],
    163: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el criterio tematico?",
        "opciones": [
            {"id": "a", "texto": "1 papel por argumento, 1 argumento por papel", "correcta": True, "razon": "Restriccion bidireccional."},
            {"id": "b", "texto": "Un argumento puede tener 2 papeles", "correcta": False, "razon": "No es correcto."},
            {"id": "c", "texto": "Un papel puede asignarse a 2 argumentos", "correcta": False, "razon": "No es correcto."},
        ], "justificacion_obligatoria": True, "regla": "1:1 papeles-argumentos"}}],
    164: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuantos argumentos exige 'dar'?",
        "opciones": [
            {"id": "a", "texto": "3: agente, tema, meta", "correcta": True, "razon": "Alguien da algo a alguien."},
            {"id": "b", "texto": "1: agente", "correcta": False, "razon": "No es suficiente."},
            {"id": "c", "texto": "0", "correcta": False, "razon": "No es impersonal."},
        ], "justificacion_obligatoria": True, "regla": "Dar: 3 argumentos"}}],
    165: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que tipo de verbo es 'nacer'?",
        "opciones": [
            {"id": "a", "texto": "Inacusativo (sujeto = tema)", "correcta": True, "razon": "No hay agente, el sujeto es tema."},
            {"id": "b", "texto": "Inergativo (sujeto = agente)", "correcta": False, "razon": "No realiza accion."},
            {"id": "c", "texto": "Transitivo", "correcta": False, "razon": "No tiene CD."},
        ], "justificacion_obligatoria": True, "regla": "Nacer: inacusativo"}}],
}
EJERCICIOS.update(EJERCICIOS_D)


TECNICAS_66_70 = [
    {"numero": 166, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Teoria de reccion",
     "teoria": "La reccion (government) es una relacion estructural entre un nucleo y su complemento o especificador. El nucleo 'rige' a sus dependientes.",
     "explicacion": "Un nucleo X rige a su complemento y a su especificador. La reccion es clave para asignar caso y para el ligamiento. En el minimalismo, la reccion se reduce a relaciones de c-command y localidad.",
     "regla": "Reccion: nucleo rige a complemento y especificador",
     "ejemplo_correcto": "El verbo 'compro' rige a su objeto 'el libro'.",
     "ejemplo_incorrecto": "La reccion no tiene relacion con la estructura."},
    {"numero": 167, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Mando-c (c-command)",
     "teoria": "Un nodo A manda-c a un nodo B si A no domina a B y el primer nodo ramificante que domina a A tambien domina a B. Es una relacion estructural fundamental.",
     "explicacion": "En un arbol, un nodo manda-c a sus hermanos y a los descendientes de sus hermanos. El sujeto manda-c al objeto, pero el objeto no manda-c al sujeto. Es la base del ligamiento y la reccion.",
     "regla": "Mando-c: A manda-c a B si su nodo dominante comun los cubre",
     "ejemplo_correcto": "El sujeto manda-c al objeto en la oracion simple.",
     "ejemplo_incorrecto": "Mando-c es lo mismo que dominar."},
    {"numero": 168, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Principio A: anforas",
     "teoria": "El Principio A del ligamiento dice que una anfora (reflexivo o reciproco) debe estar ligada dentro de su categoria rectora.",
     "explicacion": "Ejemplo: 'Juan se lava' (se = Juan). 'se' es anfora, ligada por Juan en la misma oracion. Si no hay antecedente local, es agramatical: *'Juan dice que se lava' (se refiere a Juan pero esta en otra oracion).",
     "regla": "Principio A: anfora ligada en su categoria rectora",
     "ejemplo_correcto": "En 'Juan se lava', 'se' esta ligado por Juan.",
     "ejemplo_incorrecto": "Una anfora puede estar libre en su oracion."},
    {"numero": 169, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Principio B: pronombres",
     "teoria": "El Principio B del ligamiento dice que un pronombre debe estar libre en su categoria rectora (no puede tener antecedente local).",
     "explicacion": "Ejemplo: 'Juan dice que el viene'. 'el' es pronombre: no puede referirse a Juan (que esta en otra oracion, pero si estuviera en la misma, seria agramatical). En 'Juan lo vio', 'lo' no puede ser Juan.",
     "regla": "Principio B: pronombre libre en su categoria rectora",
     "ejemplo_correcto": "En 'Juan lo vio', 'lo' no es Juan.",
     "ejemplo_incorrecto": "Un pronombre puede tener antecedente local."},
    {"numero": 170, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Principio C: expresiones referenciales",
     "teoria": "El Principio C del ligamiento dice que una expresion referencial (nombre propio, descripcion definida) debe estar libre en toda la oracion.",
     "explicacion": "Ejemplo: 'Juan dice que Pedro viene'. 'Pedro' no puede referirse a 'Juan' (son distintos). 'El hombre dice que el hombre viene' es agramatical si ambos 'el hombre' son el mismo. Las expresiones referenciales no se ligan.",
     "regla": "Principio C: expresion referencial libre en toda la oracion",
     "ejemplo_correcto": "En 'Juan dice que Pedro viene', Pedro ≠ Juan.",
     "ejemplo_incorrecto": "Un nombre propio puede tener antecedente."},
]
TECNICAS.extend(TECNICAS_66_70)


TECNICAS_71_75 = [
    {"numero": 171, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Ligamiento de 'se' reflexivo",
     "teoria": "El 'se' reflexivo es una anfora que se liga a un antecedente local (sujeto). Puede ser reflexivo (se lava) o reciproco (se miran).",
     "explicacion": "Ejemplo: 'Juan se lava' (se = Juan, reflexivo). 'Juan y Maria se miran' (se = Juan y Maria, reciproco). En ambos casos, 'se' esta ligado por el sujeto en la misma categoria rectora.",
     "regla": "'Se' reflexivo: ligado al sujeto local",
     "ejemplo_correcto": "En 'Juan se lava', 'se' esta ligado por Juan.",
     "ejemplo_incorrecto": "'Se' puede estar libre."},
    {"numero": 172, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Ligamiento de 'si mismo'",
     "teoria": "'Si mismo' es una anfora intensiva que refuerza la reflexividad. Tambien debe estar ligada localmente.",
     "explicacion": "Ejemplo: 'Juan se lava a si mismo'. 'Si mismo' refuerza 'se'. Si aparece sin 'se': 'Juan lava a si mismo' (tambien valido). En ambos casos, 'si mismo' se liga a Juan. No puede aparecer sin antecedente local.",
     "regla": "'Si mismo': anfora que refuerza la reflexividad",
     "ejemplo_correcto": "En 'Juan se lava a si mismo', 'si mismo' = Juan.",
     "ejemplo_incorrecto": "'Si mismo' puede estar sin antecedente."},
    {"numero": 173, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Pronombres y correferencia",
     "teoria": "Los pronombres pueden ser correferentes con otros SN, pero no pueden tener antecedente en su categoria rectora local (Principio B).",
     "explicacion": "Ejemplo: 'Juan dice que el viene'. 'el' puede ser Juan (correferencia a distancia) o no. Si fuera local: *'Juan lo vio' (lo ≠ Juan). La correferencia depende de la estructura y del contexto.",
     "regla": "Pronombre: correferente posible, pero no localmente",
     "ejemplo_correcto": "En 'Juan dice que el viene', 'el' puede ser Juan.",
     "ejemplo_incorrecto": "En 'Juan lo vio', 'lo' es Juan."},
    {"numero": 174, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "PRO y control",
     "teoria": "PRO es el sujeto nulo de las oraciones infinitivas. Su interpretacion depende del verbo principal (control).",
     "explicacion": "Ejemplo: 'Juan quiere [PRO venir]'. 'PRO' es el sujeto de 'venir', interpretado como Juan (control). 'PRO' no tiene forma fonetica pero si interpretacion. Es distinto de 'pro' (sujeto nulo finito, como en castellano).",
     "regla": "PRO: sujeto nulo de infinitivo, interpretado por control",
     "ejemplo_correcto": "En 'Juan quiere venir', PRO = Juan.",
     "ejemplo_incorrecto": "PRO tiene forma fonetica."},
    {"numero": 175, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Control con infinitivo",
     "teoria": "El control es la interpretacion de PRO por un antecedente en la oracion principal. Puede ser control de sujeto u objeto.",
     "explicacion": "Control de sujeto: 'Juan quiere [PRO venir]' (PRO = Juan). Control de objeto: 'Juan le pidio a Maria [PRO venir]' (PRO = Maria). El tipo de control depende del verbo principal.",
     "regla": "Control: PRO se interpreta por el sujeto u objeto principal",
     "ejemplo_correcto": "En 'Juan quiere venir', control de sujeto.",
     "ejemplo_incorrecto": "PRO no tiene interpretacion."},
]
TECNICAS.extend(TECNICAS_71_75)


TECNICAS_76_80 = [
    {"numero": 176, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Sujeto tacito en subordinadas",
     "teoria": "En subordinadas infinitivas, el sujeto puede ser tacito (PRO). En subordinadas finitas, el sujeto puede ser nulo (pro) en lenguas pro-drop.",
     "explicacion": "Ejemplo: 'Juan quiere [PRO venir]' (sujeto tacito infinitivo). 'Juan dice [que pro viene]' (sujeto nulo finito, en castellano). El castellano permite ambos tipos; el ingles solo PRO (no pro).",
     "regla": "Infinitivo: PRO. Finito pro-drop: pro",
     "ejemplo_correcto": "En 'Juan dice que viene', 'pro' es el sujeto nulo.",
     "ejemplo_incorrecto": "En ingles se permite 'pro' finito."},
    {"numero": 177, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Restricciones de ligamiento en castellano",
     "teoria": "El castellano sigue los principios A, B y C, pero con particularidades: el 'se' puede ser reflexivo, reciproco, pasivo reflejo o impersonal.",
     "explicacion": "Ejemplo: 'Juan se lava' (reflexivo), 'Juan y Maria se miran' (reciproco), 'Se venden casas' (pasivo reflejo), 'Se trabaja mucho' (impersonal). La interpretacion depende del contexto y del verbo.",
     "regla": "Castellano: 'se' con 4 valores (reflexivo, reciproco, pasivo, impersonal)",
     "ejemplo_correcto": "'Se venden casas' es pasivo reflejo.",
     "ejemplo_incorrecto": "El 'se' castellano solo es reflexivo."},
    {"numero": 178, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Reccion del nucleo",
     "teoria": "El nucleo rige a su complemento. Esta reccion es la base para la asignacion de caso acusativo (V) y oblicuo (P).",
     "explicacion": "Ejemplo: 'compro el libro' — V 'compro' rige a SN 'el libro'. 'con Juan' — P 'con' rige a SN 'Juan'. La reccion requiere mando-c y localidad: el nucleo debe mandar-c al complemento.",
     "regla": "Reccion del nucleo: X0 rige a su complemento",
     "ejemplo_correcto": "En 'compro el libro', V rige a 'el libro'.",
     "ejemplo_incorrecto": "El nucleo no rige a su complemento."},
    {"numero": 179, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Reccion del especificador",
     "teoria": "El nucleo tambien rige a su especificador en algunos casos (concordancia). La reccion del especificador es clave para la concordancia sujeto-verbo.",
     "explicacion": "Ejemplo: 'Juan canta' — T rige a su especificador 'Juan' y concuerda con el (3a sing). La reccion del especificador explica la concordancia de numero y persona.",
     "regla": "Reccion del especificador: T rige a su Esp",
     "ejemplo_correcto": "En 'Juan canta', T rige a Juan y concuerda.",
     "ejemplo_incorrecto": "El especificador no es regido."},
    {"numero": 180, "bloque": "E", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Reccion y concordancia",
     "teoria": "La concordancia es una relacion entre un nucleo funcional (T, D) y su especificador o complemento, basada en la reccion.",
     "explicacion": "Ejemplo: 'los ninos cantan' — T concuerda con el sujeto plural (cantan), D concuerda con el sustantivo plural (ninos). La concordancia se da bajo reccion: el nucleo funcional rige a su dependiente y copia sus rasgos.",
     "regla": "Concordancia: bajo reccion, el nucleo copia rasgos",
     "ejemplo_correcto": "En 'los ninos cantan', T y D concuerdan.",
     "ejemplo_incorrecto": "La concordancia es independiente de la estructura."},
]
TECNICAS.extend(TECNICAS_76_80)


EJERCICIOS_E = {
    166: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la reccion en la GGT?",
        "opciones": [
            {"id": "a", "texto": "Relacion estructural entre un nucleo y su complemento/especificador", "correcta": True, "razon": "El nucleo rige a sus dependientes."},
            {"id": "b", "texto": "Una regla fonologica", "correcta": False, "razon": "Es sintactica."},
            {"id": "c", "texto": "Un tipo de concordancia", "correcta": False, "razon": "No es solo concordancia."},
        ], "justificacion_obligatoria": True, "regla": "Reccion: nucleo rige dependientes"}}],
    167: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es el mando-c (c-command)?",
        "opciones": [
            {"id": "a", "texto": "Relacion estructural basada en el nodo dominante comun", "correcta": True, "razon": "El primer nodo ramificante que domina a A domina a B."},
            {"id": "b", "texto": "Lo mismo que dominar", "correcta": False, "razon": "Es distinto."},
            {"id": "c", "texto": "Una relacion lineal", "correcta": False, "razon": "Es estructural."},
        ], "justificacion_obligatoria": True, "regla": "Mando-c: nodo dominante comun"}}],
    168: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el Principio A del ligamiento?",
        "opciones": [
            {"id": "a", "texto": "Una anfora debe estar ligada en su categoria rectora", "correcta": True, "razon": "Reflexivos y reciprocros se ligan localmente."},
            {"id": "b", "texto": "Una anfora debe estar libre", "correcta": False, "razon": "Eso es para pronombres (B)."},
            {"id": "c", "texto": "No hay restricciones", "correcta": False, "razon": "Hay."},
        ], "justificacion_obligatoria": True, "regla": "Principio A: anfora ligada localmente"}}],
    169: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el Principio B del ligamiento?",
        "opciones": [
            {"id": "a", "texto": "Un pronombre debe estar libre en su categoria rectora", "correcta": True, "razon": "No puede tener antecedente local."},
            {"id": "b", "texto": "Un pronombre debe estar ligado", "correcta": False, "razon": "Eso es anfora (A)."},
            {"id": "c", "texto": "No hay restricciones", "correcta": False, "razon": "Hay."},
        ], "justificacion_obligatoria": True, "regla": "Principio B: pronombre libre localmente"}}],
    170: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el Principio C del ligamiento?",
        "opciones": [
            {"id": "a", "texto": "Una expresion referencial debe estar libre en toda la oracion", "correcta": True, "razon": "Nombres propios y descripciones definidas."},
            {"id": "b", "texto": "Puede tener antecedente", "correcta": False, "razon": "No es correcto."},
            {"id": "c", "texto": "Solo aplica a pronombres", "correcta": False, "razon": "Aplica a expresiones referenciales."},
        ], "justificacion_obligatoria": True, "regla": "Principio C: referencial libre"}}],
    171: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan se lava', que tipo de 'se' es?",
        "opciones": [
            {"id": "a", "texto": "Reflexivo", "correcta": True, "razon": "'Se' se refiere al sujeto Juan."},
            {"id": "b", "texto": "Pasivo reflejo", "correcta": False, "razon": "No es pasivo."},
            {"id": "c", "texto": "Impersonal", "correcta": False, "razon": "No es impersonal."},
        ], "justificacion_obligatoria": True, "regla": "Se reflexivo: ligado al sujeto"}}],
    172: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan se lava a si mismo', que funcion tiene 'si mismo'?",
        "opciones": [
            {"id": "a", "texto": "Refuerza la reflexividad", "correcta": True, "razon": "Es una anfora intensiva."},
            {"id": "b", "texto": "Es un pronombre libre", "correcta": False, "razon": "Es anfora."},
            {"id": "c", "texto": "Es un adverbio", "correcta": False, "razon": "No es adverbio."},
        ], "justificacion_obligatoria": True, "regla": "'Si mismo': anfora intensiva"}}],
    173: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Puede 'el' referirse a 'Juan' en 'Juan lo vio'?",
        "opciones": [
            {"id": "a", "texto": "No, por el Principio B", "correcta": True, "razon": "Un pronombre no puede tener antecedente local."},
            {"id": "b", "texto": "Si, sin restriccion", "correcta": False, "razon": "Hay restriccion."},
            {"id": "c", "texto": "Solo en pasivas", "correcta": False, "razon": "No es eso."},
        ], "justificacion_obligatoria": True, "regla": "Pronombre: no antecedente local"}}],
    174: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es PRO en la GGT?",
        "opciones": [
            {"id": "a", "texto": "Sujeto nulo de infinitivo, interpretado por control", "correcta": True, "razon": "En 'Juan quiere PRO venir', PRO = Juan."},
            {"id": "b", "texto": "Un pronombre fonetico", "correcta": False, "razon": "PRO no tiene forma fonetica."},
            {"id": "c", "texto": "Un tipo de verbo", "correcta": False, "razon": "No es verbo."},
        ], "justificacion_obligatoria": True, "regla": "PRO: sujeto nulo infinitivo"}}],
    175: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan quiere venir', como se interpreta PRO?",
        "opciones": [
            {"id": "a", "texto": "PRO = Juan (control de sujeto)", "correcta": True, "razon": "El sujeto del principal controla PRO."},
            {"id": "b", "texto": "PRO = Maria", "correcta": False, "razon": "No hay Maria."},
            {"id": "c", "texto": "PRO no tiene interpretacion", "correcta": False, "razon": "Si la tiene."},
        ], "justificacion_obligatoria": True, "regla": "Control de sujeto"}}],
    176: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que sujeto tacito tiene 'Juan dice que viene'?",
        "opciones": [
            {"id": "a", "texto": "pro (sujeto nulo finito)", "correcta": True, "razon": "El castellano permite pro finito."},
            {"id": "b", "texto": "PRO (sujeto nulo infinitivo)", "correcta": False, "razon": "PRO solo en infinitivo."},
            {"id": "c", "texto": "No hay sujeto", "correcta": False, "razon": "Hay pro."},
        ], "justificacion_obligatoria": True, "regla": "Finito: pro. Infinitivo: PRO"}}],
    177: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'se venden casas', que valor tiene 'se'?",
        "opciones": [
            {"id": "a", "texto": "Pasivo reflejo", "correcta": True, "razon": "El verbo concuerda con 'casas' (sujeto paciente)."},
            {"id": "b", "texto": "Reflexivo", "correcta": False, "razon": "No hay reflexividad."},
            {"id": "c", "texto": "Impersonal", "correcta": False, "razon": "Hay sujeto paciente."},
        ], "justificacion_obligatoria": True, "regla": "Se pasivo reflejo"}}],
    178: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'compro el libro', que relacion hay entre V y el SN?",
        "opciones": [
            {"id": "a", "texto": "V rige al SN (reccion del nucleo)", "correcta": True, "razon": "El nucleo V rige a su complemento."},
            {"id": "b", "texto": "No hay relacion", "correcta": False, "razon": "Hay reccion."},
            {"id": "c", "texto": "El SN rige al V", "correcta": False, "razon": "Es al reves."},
        ], "justificacion_obligatoria": True, "regla": "V rige a su complemento"}}],
    179: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica el tipo de 'se': reflexivo (R), reciproco (Rec), pasivo reflejo (P), impersonal (I)",
        "oraciones": [
            {"texto": "Juan se lava", "categoria_correcta": "R"},
            {"texto": "Juan y Maria se miran", "categoria_correcta": "Rec"},
            {"texto": "Se venden casas", "categoria_correcta": "P"},
            {"texto": "Se trabaja mucho", "categoria_correcta": "I"},
        ],
        "categorias": ["R", "Rec", "P", "I"]}}],
    180: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'los ninos cantan', que explica la concordancia?",
        "opciones": [
            {"id": "a", "texto": "T rige a su Esp y copia rasgos", "correcta": True, "razon": "Concordancia bajo reccion."},
            {"id": "b", "texto": "Es pura casualidad", "correcta": False, "razon": "Es estructural."},
            {"id": "c", "texto": "El verbo copia del objeto", "correcta": False, "razon": "Copia del sujeto."},
        ], "justificacion_obligatoria": True, "regla": "Concordancia: T rige Esp"}}],
}
EJERCICIOS.update(EJERCICIOS_E)


TECNICAS_81_85 = [
    {"numero": 181, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Del modelo de Principios y Parametros al Minimalismo",
     "teoria": "El Programa Minimalista (Chomsky, 1995) reduce la teoria a lo minimo necesario. Elimina niveles (EP/ES) y reemplaza transformaciones por Merge y Move.",
     "explicacion": "En el modelo clasico habia muchos niveles (EP, ES, FL, FF) y reglas. El minimalismo propone solo dos interfaces (FL y FF) y una operacion basica (Merge) + una derivada (Move). El objetivo es la simplicidad teorica.",
     "regla": "Minimalismo: solo FL + FF + Merge/Move",
     "ejemplo_correcto": "El minimalismo reduce la teoria a lo minimo necesario.",
     "ejemplo_incorrecto": "El minimalismo agrega mas niveles de representacion."},
    {"numero": 182, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Merge (ensamble)",
     "teoria": "Merge es la operacion basica del minimalismo: toma dos objetos sintacticos y los combina en uno nuevo.",
     "explicacion": "Merge(X, Y) -> {X, Y}. Ejemplo: Merge(V, SN) = SV; Merge(T, SV) = ST; Merge(C, ST) = SC. Todo el arbol sintactico se construye por Merge binario. Es la operacion mas simple posible.",
     "regla": "Merge: combina dos objetos en uno",
     "ejemplo_correcto": "Merge('lee', 'el libro') = 'lee el libro'.",
     "ejemplo_incorrecto": "Merge combina mas de dos objetos a la vez."},
    {"numero": 183, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Move (movimiento)",
     "teoria": "Move es la operacion que copia un elemento y lo re-mergea en otra posicion, dejando una huella.",
     "explicacion": "Move(X) = copia X y la combina con otro nodo. Ejemplo: en interrogativas, 'que' se copia y se mueve a C. La huella queda en la posicion original. En el minimalismo, Move es 'Merge interno' (re-merge de un elemento ya presente).",
     "regla": "Move: copia + re-merge (deja huella)",
     "ejemplo_correcto": "En 'que compro t', 'que' se mueve a C.",
     "ejemplo_incorrecto": "Move no deja huella."},
    {"numero": 184, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Agree (concordancia)",
     "teoria": "Agree es la operacion que establece concordancia entre un nucleo funcional y un elemento en su dominio (especificador o complemento) copiando rasgos.",
     "explicacion": "Ejemplo: en 'Juan canta', T tiene rasgos no interpretables (persona, numero) que se valoran por Agree con 'Juan' (3a sing). El verbo copia los rasgos de T. Agree no mueve elementos, solo copia rasgos.",
     "regla": "Agree: copia rasgos entre nucleo y dependiente",
     "ejemplo_correcto": "T y Juan hacen Agree para concordancia.",
     "ejemplo_incorrecto": "Agree mueve el sujeto."},
    {"numero": 185, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Rasgos formales (features)",
     "teoria": "Los rasgos formales son propiedades gramaticales de los elementos: persona, numero, genero, caso, tiempo. Se dividen en interpretables y no interpretables.",
     "explicacion": "Ejemplo: 'nino' tiene rasgos [masc, sing] (interpretables). 'el' tiene [masc, sing, def] (algunos no interpretables). T tiene [pres, 3a, sing] que se valoran por Agree. La derivacion consiste en eliminar rasgos no interpretables.",
     "regla": "Rasgos: interpretables (semanticos) vs no interpretables (gramaticales)",
     "ejemplo_correcto": "El rasgo [plural] de 'ninos' es interpretable.",
     "ejemplo_incorrecto": "Todos los rasgos son interpretables."},
]
TECNICAS.extend(TECNICAS_81_85)


TECNICAS_86_90 = [
    {"numero": 186, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Rasgos interpretables vs no interpretables",
     "teoria": "Los rasgos interpretables aportan significado (genero, numero en N). Los no interpretables son gramaticales y deben eliminarse en la derivacion (persona, numero en T, caso).",
     "explicacion": "Ejemplo: 'nino' tiene [masc, sing] interpretables. T en 'canta' tiene [3a, sing, pres] no interpretables: se valoran por Agree con el sujeto y luego se eliminan. Si un rasgo no interpretable no se valora, la derivacion falla.",
     "regla": "Interpretables: significado. No interpretables: se eliminan",
     "ejemplo_correcto": "El [plural] de 'ninos' es interpretable; el de T no.",
     "ejemplo_incorrecto": "Todos los rasgos se conservan en la derivacion."},
    {"numero": 187, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Economia y ultima instancia",
     "teoria": "El principio de economia establece que las derivaciones deben ser lo mas cortas posibles. El movimiento solo ocurre en 'ultima instancia', si es necesario.",
     "explicacion": "Ejemplo: si un rasgo puede valorarse sin mover, no se mueve. El movimiento-qu es necesario (ultima instancia) para valorar el rasgo [+qu] de C. Movimientos innecesarios violan la economia.",
     "regla": "Economia: derivacion mas corta. Move solo si es necesario",
     "ejemplo_correcto": "El movimiento-qu ocurre solo si C tiene rasgo [+qu].",
     "ejemplo_incorrecto": "Se puede mover cualquier cosa sin justificacion."},
    {"numero": 188, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Interfaz PF (forma fonetica)",
     "teoria": "La interfaz PF (Phonetic Form) es el nivel donde la estructura sintactica se traduce en sonidos. Es una de las dos interfaces del minimalismo.",
     "explicacion": "En PF se aplican reglas fonologicas y se pronuncian los elementos. Los elementos con rasgos no interpretables que no se eliminaron pueden causar problemas en PF (agramaticalidad). La interfaz PF conecta la sintaxis con la fonologia.",
     "regla": "PF: interfaz sintaxis-fonologia (como se pronuncia)",
     "ejemplo_correcto": "La estructura de 'Juan canta' se pronuncia via PF.",
     "ejemplo_incorrecto": "PF es lo mismo que LF."},
    {"numero": 189, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Interfaz LF (forma logica)",
     "teoria": "La interfaz LF (Logical Form) es el nivel donde la estructura sintactica se interpreta semanticamente. Es la otra interfaz del minimalismo.",
     "explicacion": "En LF se interpretan los elementos: quien es agente, quien es paciente, que se pregunta. El movimiento-qu deja huella que se interpreta en LF. La interfaz LF conecta la sintaxis con la semantica.",
     "regla": "LF: interfaz sintaxis-semantica (como se interpreta)",
     "ejemplo_correcto": "En 'que compro Juan t', LF interpreta 'que' como objeto.",
     "ejemplo_incorrecto": "LF es lo mismo que PF."},
    {"numero": 190, "bloque": "F", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "La derivacion minimalista",
     "teoria": "La derivacion minimalista es el proceso por el cual se construye una oracion aplicando Merge, Move y Agree paso a paso desde el lexico hasta las interfaces.",
     "explicacion": "Ejemplo: 'Juan canta'. 1) Se extraen del lexico: Juan, canta, T, C. 2) Merge(V, SN) -> SV. 3) Merge(T, SV) -> ST. 4) Move(Juan a Esp ST). 5) Agree(T, Juan). 6) Merge(C, ST) -> SC. 7) LF y PF. Cada paso es una operacion.",
     "regla": "Derivacion: Merge + Move + Agree + interfaces",
     "ejemplo_correcto": "La derivacion de 'Juan canta' usa Merge y Agree.",
     "ejemplo_incorrecto": "La derivacion no sigue pasos."},
]
TECNICAS.extend(TECNICAS_86_90)


TECNICAS_91_95 = [
    {"numero": 191, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Orden SVO vs VSO vs VOS en castellano",
     "teoria": "El castellano es una lengua SVO basica, pero permite VSO y VOS por movimiento. El orden no marcado es SVO.",
     "explicacion": "SVO: 'Juan compro el libro'. VSO: 'Compro Juan el libro' (enfasis). VOS: 'Compro el libro Juan' (foco). El castellano es flexible: el orden cambia por topicalizacion, focalizacion o razones pragmaticas.",
     "regla": "Castellano: SVO basico. VSO/VOS por movimiento",
     "ejemplo_correcto": "SVO es el orden no marcado en castellano.",
     "ejemplo_incorrecto": "El castellano solo permite SVO."},
    {"numero": 192, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Sujeto nulo: parametro del castellano",
     "teoria": "El castellano es una lengua pro-drop: permite el sujeto nulo (pro) porque el verbo lleva los rasgos de persona y numero.",
     "explicacion": "Ejemplo: 'canto' = 'yo canto'. El parametro pro-drop se fija positivo en castellano. En ingles se fija negativo (obliga a 'I sing'). La diferencia se debe a la riqueza morfologica del verbo.",
     "regla": "Castellano: pro-drop positivo (sujeto nulo)",
     "ejemplo_correcto": "En castellano 'canto' funciona sin 'yo'.",
     "ejemplo_incorrecto": "El castellano exige sujeto explicito siempre."},
    {"numero": 193, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Movimiento del verbo en castellano",
     "teoria": "En castellano el verbo sube desde V a T (movimiento V->T) para concordar con el sujeto.",
     "explicacion": "Ejemplo: 'Juan canta'. El verbo 'canta' sube de V a T. En ingles el verbo no sube (se queda en V). La diferencia se debe a la riqueza de la flexion verbal: en castellano T atrae al verbo.",
     "regla": "Castellano: V->T. Ingles: V se queda en SV",
     "ejemplo_correcto": "En castellano el verbo sube a T.",
     "ejemplo_incorrecto": "El verbo nunca sube a T."},
    {"numero": 194, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Cliticos: estructura y movimiento",
     "teoria": "Los cliticos (me, te, lo, la, le) son pronombres atonos que se adjuntan al verbo. En la GGT se analizan como nucleos funcionales o como elementos movidos.",
     "explicacion": "Ejemplo: 'Juan lo compro'. 'lo' es un clitico que se adjunta al verbo. Algunos analisis lo tratan como D movido desde el SN objeto. Otros, como un nucleo funcional (Clitic Phrase, ClP).",
     "regla": "Cliticos: pronombres atonos adjuntos al verbo",
     "ejemplo_correcto": "En 'lo compro', 'lo' es clitico del objeto.",
     "ejemplo_incorrecto": "Los cliticos son palabras independientes."},
    {"numero": 195, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Doble negacion en castellano",
     "teoria": "El castellano permite doble negacion: 'No vi a nadie'. Ambos elementos negativos no se cancelan (a diferencia del ingles).",
     "explicacion": "Ejemplo: 'No vi a nadie' = 'no vi a persona alguna' (doble negacion concordante). En ingles 'I didn't see nobody' es agramatical (doble negacion cancela). En la GGT se analiza como concordancia negativa (NegP).",
     "regla": "Castellano: doble negacion concordante (no cancela)",
     "ejemplo_correcto": "'No vi a nadie' es gramatical en castellano.",
     "ejemplo_incorrecto": "La doble negacion cancela el significado."},
]
TECNICAS.extend(TECNICAS_91_95)


TECNICAS_96_100 = [
    {"numero": 196, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Ser vs estar: analisis generativo",
     "teoria": "En la GGT, 'ser' y 'estar' se analizan como copulativos. 'Ser' expresa cualidad esencial (individuo); 'estar' expresa estado (estadio).",
     "explicacion": "Ejemplo: 'Juan es alto' (cualidad esencial, individuo) vs 'Juan esta cansado' (estado transitorio). En la GGT se propone que 'ser' selecciona un SV pequeno (Small Clause) con interpretacion individual; 'estar' con interpretacion de estadio.",
     "regla": "Ser: cualidad (individuo). Estar: estado (estadio)",
     "ejemplo_correcto": "'Juan es alto' (esencial) vs 'Juan esta cansado' (transitorio).",
     "ejemplo_incorrecto": "Ser y estar son equivalentes."},
    {"numero": 197, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Subordinadas sustantivas: analisis generativo",
     "teoria": "Las subordinadas sustantivas son SC (sintagmas complementantes) que funcionan como argumento del verbo principal.",
     "explicacion": "Ejemplo: 'Juan dijo [que Maria viene]'. El SC 'que Maria viene' es el complemento del verbo 'dijo'. Su nucleo C es 'que'. Si el verbo es transitivo, el SC recibe caso acusativo de V.",
     "regla": "Sustantivas: SC como argumento de V",
     "ejemplo_correcto": "En 'Juan dijo que Maria viene', el SC es complemento de 'dijo'.",
     "ejemplo_incorrecto": "Las sustantivas son SN."},
    {"numero": 198, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Relativas: analisis generativo",
     "teoria": "Las relativas son SC que modifican a un antecedente nominal. El relativo se mueve desde su posicion original a C.",
     "explicacion": "Ejemplo: 'El libro [que compre t] es bueno'. 'Que' se mueve de objeto (t) a C. El SC relativo modifica a 'el libro'. El antecedente y el relativo comparten referencia.",
     "regla": "Relativas: SC que modifica N, relativo -> C",
     "ejemplo_correcto": "En 'el libro que compre t', el SC modifica 'libro'.",
     "ejemplo_incorrecto": "Las relativas son oraciones independientes."},
    {"numero": 199, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Interrogativas: movimiento-qu",
     "teoria": "Las interrogativas (directas e indirectas) tienen un pronombre-qu que se mueve a C.",
     "explicacion": "Directa: 'Que compro Juan t?'. Indirecta: 'No se [que compro Juan t]'. En ambos casos, 'que' se mueve de objeto a C. El movimiento-qu es visible en castellano, pero puede ser in situ en otras lenguas (chino).",
     "regla": "Interrogativas: pronombre-qu -> C",
     "ejemplo_correcto": "En 'que compro t', 'que' esta en C.",
     "ejemplo_incorrecto": "Las interrogativas no tienen movimiento."},
    {"numero": 200, "bloque": "G", "nivel": "avanzado", "modulo": "generativa",
     "titulo": "Analisis generativo completo de una oracion",
     "teoria": "El analisis generativo completo integra todas las operaciones: Merge, Move, Agree, en las interfaces LF y PF.",
     "explicacion": "Ejemplo: 'Juan compro el libro'. 1) Lexico: Juan, compro, el, libro. 2) Merge(el, libro) = SD. 3) Merge(compro, SD) = SV. 4) Merge(Juan, SV) = SV (sujeto en Esp). 5) Merge(T, SV) = ST. 6) Move(Juan a Esp ST). 7) Agree(T, Juan). 8) Merge(C, ST) = SC. 9) LF: interpretacion. 10) PF: pronunciacion.",
     "regla": "Analisis completo: Merge + Move + Agree + LF/PF",
     "ejemplo_correcto": "El analisis de 'Juan compro el libro' integra las 10 operaciones.",
     "ejemplo_incorrecto": "El analisis completo solo requiere Move."},
]
TECNICAS.extend(TECNICAS_96_100)


EJERCICIOS_FG = {
    181: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que busca el Programa Minimalista?",
        "opciones": [
            {"id": "a", "texto": "Reducir la teoria a lo minimo necesario", "correcta": True, "razon": "Solo FL, FF, Merge y Move."},
            {"id": "b", "texto": "Agregar mas niveles", "correcta": False, "razon": "Todo lo contrario."},
            {"id": "c", "texto": "Eliminar la sintaxis", "correcta": False, "razon": "La sintaxis sigue."},
        ], "justificacion_obligatoria": True, "regla": "Minimalismo: simplicidad"}}],
    182: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es Merge en el minimalismo?",
        "opciones": [
            {"id": "a", "texto": "Operacion que combina dos objetos en uno", "correcta": True, "razon": "Merge(X, Y) = {X, Y}."},
            {"id": "b", "texto": "Una regla de movimiento", "correcta": False, "razon": "Eso es Move."},
            {"id": "c", "texto": "Una regla fonologica", "correcta": False, "razon": "Es sintactica."},
        ], "justificacion_obligatoria": True, "regla": "Merge: combina dos objetos"}}],
    183: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que hace Move en el minimalismo?",
        "opciones": [
            {"id": "a", "texto": "Copia un elemento y lo re-mergea, dejando huella", "correcta": True, "razon": "Re-merge interno."},
            {"id": "b", "texto": "Combina dos objetos nuevos", "correcta": False, "razon": "Eso es Merge."},
            {"id": "c", "texto": "Copia rasgos", "correcta": False, "razon": "Eso es Agree."},
        ], "justificacion_obligatoria": True, "regla": "Move: copia + re-merge"}}],
    184: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que hace Agree?",
        "opciones": [
            {"id": "a", "texto": "Copia rasgos entre nucleo y dependiente", "correcta": True, "razon": "Establece concordancia."},
            {"id": "b", "texto": "Mueve el sujeto", "correcta": False, "razon": "Eso es Move."},
            {"id": "c", "texto": "Combina objetos", "correcta": False, "razon": "Eso es Merge."},
        ], "justificacion_obligatoria": True, "regla": "Agree: copia rasgos"}}],
    185: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es un rasgo interpretable?",
        "opciones": [
            {"id": "a", "texto": "Un rasgo que aporta significado (genero, numero en N)", "correcta": True, "razon": "Los interpretables se interpretan en LF."},
            {"id": "b", "texto": "Un rasgo gramatical que se elimina", "correcta": False, "razon": "Eso es no interpretable."},
            {"id": "c", "texto": "Un rasgo fonologico", "correcta": False, "razon": "Es sintactico."},
        ], "justificacion_obligatoria": True, "regla": "Interpretable: significado"}}],
    186: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica el rasgo: interpretable (I) o no interpretable (N)",
        "oraciones": [
            {"texto": "plural de ninos", "categoria_correcta": "I"},
            {"texto": "persona de T", "categoria_correcta": "N"},
            {"texto": "genero de nino", "categoria_correcta": "I"},
            {"texto": "caso de pronombre", "categoria_correcta": "N"},
        ],
        "categorias": ["I", "N"]}}],
    187: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que dice el principio de economia?",
        "opciones": [
            {"id": "a", "texto": "Las derivaciones deben ser lo mas cortas posibles", "correcta": True, "razon": "Move solo si es necesario."},
            {"id": "b", "texto": "Se puede mover cualquier cosa", "correcta": False, "razon": "Solo si es necesario."},
            {"id": "c", "texto": "No hay restricciones", "correcta": False, "razon": "Hay."},
        ], "justificacion_obligatoria": True, "regla": "Economia: derivacion corta"}}],
    188: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la interfaz PF?",
        "opciones": [
            {"id": "a", "texto": "Nivel donde la estructura se traduce en sonidos", "correcta": True, "razon": "Phonetic Form."},
            {"id": "b", "texto": "Nivel donde se interpreta el significado", "correcta": False, "razon": "Eso es LF."},
            {"id": "c", "texto": "Un tipo de movimiento", "correcta": False, "razon": "No es movimiento."},
        ], "justificacion_obligatoria": True, "regla": "PF: sintaxis-fonologia"}}],
    189: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que es la interfaz LF?",
        "opciones": [
            {"id": "a", "texto": "Nivel donde la estructura se interpreta semanticamente", "correcta": True, "razon": "Logical Form."},
            {"id": "b", "texto": "Nivel fonologico", "correcta": False, "razon": "Eso es PF."},
            {"id": "c", "texto": "Un tipo de verbo", "correcta": False, "razon": "No es verbo."},
        ], "justificacion_obligatoria": True, "regla": "LF: sintaxis-semantica"}}],
    190: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que operaciones integra la derivacion minimalista?",
        "opciones": [
            {"id": "a", "texto": "Merge + Move + Agree", "correcta": True, "razon": "Las tres operaciones basicas."},
            {"id": "b", "texto": "Solo Merge", "correcta": False, "razon": "Faltan Move y Agree."},
            {"id": "c", "texto": "Ninguna", "correcta": False, "razon": "Hay 3."},
        ], "justificacion_obligatoria": True, "regla": "Derivacion: Merge+Move+Agree"}}],
    191: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cual es el orden basico del castellano?",
        "opciones": [
            {"id": "a", "texto": "SVO", "correcta": True, "razon": "Sujeto-Verbo-Objeto es el no marcado."},
            {"id": "b", "texto": "VSO", "correcta": False, "razon": "Es marcado."},
            {"id": "c", "texto": "VOS", "correcta": False, "razon": "Es marcado."},
        ], "justificacion_obligatoria": True, "regla": "Castellano: SVO basico"}}],
    192: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El castellano es pro-drop?",
        "opciones": [
            {"id": "a", "texto": "Si, permite sujeto nulo", "correcta": True, "razon": "Ej: 'canto' sin 'yo'."},
            {"id": "b", "texto": "No, exige sujeto explicito", "correcta": False, "razon": "Eso es el ingles."},
            {"id": "c", "texto": "Solo en pasado", "correcta": False, "razon": "En todos los tiempos."},
        ], "justificacion_obligatoria": True, "regla": "Castellano: pro-drop"}}],
    193: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En castellano, el verbo sube a T?",
        "opciones": [
            {"id": "a", "texto": "Si, V->T", "correcta": True, "razon": "Para concordar con el sujeto."},
            {"id": "b", "texto": "No, se queda en SV", "correcta": False, "razon": "Eso pasa en ingles."},
            {"id": "c", "texto": "Solo en infinitivo", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": True, "regla": "Castellano: V->T"}}],
    194: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que son los cliticos en la GGT?",
        "opciones": [
            {"id": "a", "texto": "Pronombres atonos que se adjuntan al verbo", "correcta": True, "razon": "Ej: 'lo compro'."},
            {"id": "b", "texto": "Palabras independientes", "correcta": False, "razon": "No son libres."},
            {"id": "c", "texto": "Verbos auxiliares", "correcta": False, "razon": "No son verbos."},
        ], "justificacion_obligatoria": True, "regla": "Cliticos: atonos, adjuntos"}}],
    195: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En castellano, 'No vi a nadie' es:",
        "opciones": [
            {"id": "a", "texto": "Gramatical (doble negacion concordante)", "correcta": True, "razon": "En castellano la doble negacion no cancela."},
            {"id": "b", "texto": "Agramatical", "correcta": False, "razon": "Es gramatical."},
            {"id": "c", "texto": "Un error", "correcta": False, "razon": "Es correcto."},
        ], "justificacion_obligatoria": True, "regla": "Doble negacion concordante"}}],
    196: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que distingue 'ser' de 'estar' en la GGT?",
        "opciones": [
            {"id": "a", "texto": "Ser: cualidad esencial. Estar: estado transitorio", "correcta": True, "razon": "Individuo vs estadio."},
            {"id": "b", "texto": "Son equivalentes", "correcta": False, "razon": "Son distintos."},
            {"id": "c", "texto": "Ser es para tiempo pasado", "correcta": False, "razon": "No es eso."},
        ], "justificacion_obligatoria": True, "regla": "Ser esencial, estar estadio"}}],
    197: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'Juan dijo que Maria viene', que es 'que Maria viene'?",
        "opciones": [
            {"id": "a", "texto": "Un SC (complemento de 'dijo')", "correcta": True, "razon": "Subordinada sustantiva = SC."},
            {"id": "b", "texto": "Un SN", "correcta": False, "razon": "No es nominal."},
            {"id": "c", "texto": "Un SP", "correcta": False, "razon": "No empieza por preposicion."},
        ], "justificacion_obligatoria": True, "regla": "Sustantiva = SC"}}],
    198: [{"tipo": 3, "orden": 1, "payload": {
        "enunciado": "Clasifica cada subordinada: sustantiva (S) o relativa (R)",
        "oraciones": [
            {"texto": "Juan dijo que Maria viene", "categoria_correcta": "S"},
            {"texto": "El libro que compre es bueno", "categoria_correcta": "R"},
            {"texto": "Maria cree que Juan viene", "categoria_correcta": "S"},
            {"texto": "La casa que vimos es grande", "categoria_correcta": "R"},
        ],
        "categorias": ["S", "R"]}}],
    199: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En 'que compro Juan t', que tipo de movimiento hay?",
        "opciones": [
            {"id": "a", "texto": "Movimiento-qu (interrogativa)", "correcta": True, "razon": "'Que' se mueve a C."},
            {"id": "b", "texto": "Movimiento de nucleo", "correcta": False, "razon": "No es nucleo."},
            {"id": "c", "texto": "Movimiento-A", "correcta": False, "razon": "Es A-barra."},
        ], "justificacion_obligatoria": True, "regla": "Interrogativa: movimiento-qu"}}],
    200: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que operaciones integra el analisis generativo completo?",
        "opciones": [
            {"id": "a", "texto": "Merge + Move + Agree + LF/PF", "correcta": True, "razon": "Las 3 operaciones + 2 interfaces."},
            {"id": "b", "texto": "Solo Merge", "correcta": False, "razon": "Faltan mas."},
            {"id": "c", "texto": "Solo Move", "correcta": False, "razon": "Faltan mas."},
        ], "justificacion_obligatoria": True, "regla": "Analisis completo: 5 elementos"}}],
}
EJERCICIOS.update(EJERCICIOS_FG)

