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

