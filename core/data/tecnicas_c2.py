"""Data del modulo C2: Lengua Castellana C2 (100 técnicas, 10 bloques A-J)."""

TECNICAS = [
    {"numero": 801, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Registro literario avanzado: léxico y sintaxis",
     "teoria": "El registro literario avanzado combina selección léxica precisa, sintaxis variada y ritmo propio. No es adorno: cada elección construye sentido.",
     "explicacion": "Léxico: cultismos (efímero, ubicuo, proceloso), palabras de baja frecuencia (cerúleo, ígneo, umbrío). Sintaxis: alternancia de oraciones largas (subordinadas) y cortas (impacto). Ritmo: control de sílabas tónicas, pausas, cadencia final. Referentes: Valle-Inclán, García Márquez, Virginia Woolf, Nabokov.",
     "regla": "registro literario = léxico preciso + sintaxis variada + ritmo propio",
     "ejemplo_correcto": "La ciudad, con sus avenidas de asfalto ardiente, olía a tiempo detenido.",
     "ejemplo_incorrecto": "La ciudad tenía calles y hacía calor. (registro neutro)"},

    {"numero": 802, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Cultismos y palabras de baja frecuencia",
     "teoria": "Los cultismos son palabras de origen latino o griego que entraron por vía escrita, sin evolución popular. Su uso controlado enriquece el registro.",
     "explicacion": "Ejemplos: 'efímero' (breve), 'ubicuo' (en todas partes), 'exiguo' (escaso), 'proceloso' (tempestuoso), 'sempiterno' (eterno), 'lánguido' (débil), 'cerúleo' (azul), 'ígneo' (de fuego), 'umbrío' (con sombra). Advertencia: su abuso produce ampulosidad. Se usan cuando la precisión lo exige, no por decoración.",
     "regla": "cultismo = palabra latina/griega culta | uso controlado (no abuso)",
     "ejemplo_correcto": "Su fama fue efímera; su obra, sempiterna.",
     "ejemplo_incorrecto": "Su fama fue efímera, brevísima, corta, fugaz. (redundante)"},

    {"numero": 803, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Adjetivación literaria: epítetos y adjetivos de matiz",
     "teoria": "La adjetivación literaria selecciona adjetivos que aportan matiz, no solo adornan. El epíteto añade cualidad inherente o valorativa.",
     "explicacion": "Epítetos: 'la blanca nieve', 'el fiero león' (cualidad inherente). Adjetivos de matiz: 'luz cenicienta', 'silencio espeso', 'olor a viejo'. La clave está en la selección: 'un adjetivo preciso vale más que tres vagos'. Adjetivos que resaltan: cárdeno, ceniciento, verdoso, plomizo, ambarino.",
     "regla": "adjetivación literaria = epítetos + adjetivos de matiz (no acumulación)",
     "ejemplo_correcto": "El cielo ceniciento anunciaba una tormenta seca.",
     "ejemplo_incorrecto": "El cielo era gris, oscuro y feo. (adjetivos genéricos)"},

    {"numero": 804, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Sintaxis del período largo: hipotaxis controlada",
     "teoria": "El período largo (hipotaxis) construye significado por acumulación de subordinadas. Requiere control para no perder al lector.",
     "explicacion": "Estructura: principal + subordinadas que matizan (causales, concesivas, relativas, temporales). Cada subordinada añade información. Ejemplo: 'Aunque la lluvia arreciaba, y a pesar de que el viento doblaba los árboles, los vecinos, que llevaban horas reunidos, decidieron salir'. Control: no más de 4-5 subordinadas por período.",
     "regla": "período largo = hipotaxis + matices + control (máx 4-5 subordinadas)",
     "ejemplo_correcto": "Cuando llegó el invierno, que aquel año fue especialmente duro, los ancianos, que no tenían leña, se reunieron en la plaza.",
     "ejemplo_incorrecto": "Cuando llegó el invierno que fue duro que los ancianos que no tenían leña que se reunieron."},

    {"numero": 805, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Ritmo y musicalidad en la prosa",
     "teoria": "La prosa literaria tiene ritmo propio, construido por la alternancia de sílabas tónicas y átonas, las pausas y la cadencia final.",
     "explicacion": "Recursos: alternancia de oraciones largas y cortas, uso de esdrújulas para ralentizar ('cántico, íntimo, pálido'), de agudas para acelerar ('canté, miró, salí'). Cadencias: terminar en llana (neutro), aguda (énfasis), esdrújula (suspensión). Referente: la prosa rítmica de Gabriel Miró o Azorín.",
     "regla": "ritmo = alternancia tónica/átona + pausas + cadencia final",
     "ejemplo_correcto": "Caminaba despacio. Lento. Mirando el horizonte, que se desdibujaba.",
     "ejemplo_incorrecto": "Caminaba despacio mirando el horizonte que se desdibujaba lento."},

    {"numero": 806, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Figuras retóricas avanzadas: metáfora, metonimia, sinécdoque",
     "teoria": "En C2 se analizan y producen figuras retóricas avanzadas: no solo identificarlas, sino evaluar su eficacia y coherencia.",
     "explicacion": "Metáfora pura: 'Tus ojos son dos luceros'. Metonimia: 'Leí a Cervantes' (autor por obra). Sinécdoque: 'Tiene veinte primaveras' (parte por todo). Ironía: '¡Qué puntualidad!' (dice lo contrario). Paradoja: 'Vivo sin vivir en mí'. En C2 no basta identificarlas: hay que valorar si son coherentes con el tono y eficaces en el contexto.",
     "regla": "figura retórica = identificación + evaluación de eficacia y coherencia",
     "ejemplo_correcto": "El silencio era tan denso que dolía. (paradoja + hipálage)",
     "ejemplo_incorrecto": "Es una metáfora. (identificar sin analizar)"},

    {"numero": 807, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Estilo nominal vs verbal en la prosa literaria",
     "teoria": "El estilo nominal (sustantivos + ser) es propio de la prosa reflexiva y del ensayo. El verbal (verbos conjugados) es más dinámico y narrativo.",
     "explicacion": "Nominal: 'La lentitud del tiempo, la pesadez de las horas, la inminencia del final' (sustantivos abstractos). Verbal: 'El tiempo pasaba lento; las horas pesaban; el final se acercaba'. El estilo nominal ralentiza y reflexiona; el verbal acelera y narra. En C2 se elige según el efecto buscado.",
     "regla": "nominal = reflexión / ralentización | verbal = acción / dinamismo",
     "ejemplo_correcto": "La ciudad era una suma de ausencias: calles vacías, voces apagadas, farolas sin luz.",
     "ejemplo_incorrecto": "La ciudad tenía calles vacías, voces apagadas y farolas sin luz. (estilo verbal, pierde el efecto)"},

    {"numero": 808, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Elipsis y silencio en la prosa literaria",
     "teoria": "La elipsis (omitir elementos recuperables) y el silencio (lo no dicho) son recursos de la prosa literaria para sugerir, no explicar.",
     "explicacion": "Elipsis: 'Unos prefieren el cine; otros, el teatro' (se omite el verbo). Silencio: 'Se miraron. Nada más. Nada menos.'. En ambos casos, el lector completa el sentido. El silencio es tan importante como la palabra: 'Decir sin decir'. Referentes: Hemingway, Carver, Monterroso.",
     "regla": "elipsis + silencio = sugerir sin explicar | el lector completa",
     "ejemplo_correcto": "Abrió la puerta. Vacío. Cerró.",
     "ejemplo_incorrecto": "Abrió la puerta y vio que la habitación estaba vacía. Luego cerró la puerta. (explica todo)"},

    {"numero": 809, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Punto de vista y voz narrativa en prosa literaria",
     "teoria": "El punto de vista (quién cuenta) y la voz (cómo cuenta) determinan la interpretación del texto. En C2 se dominan todas las variantes.",
     "explicacion": "1ª persona: intimidad, subjetividad, acceso limitado. 3ª omnisciente: acceso total, distancia. 3ª limitada: sigue a un personaje. 2ª persona: apelación, extrañeza. Estilo indirecto libre: mezcla narrador y personaje sin marcas. La elección del punto de vista define la novela entera.",
     "regla": "punto de vista = 1ª/2ª/3ª persona (omnisciente/limitada) + estilo indirecto libre",
     "ejemplo_correcto": "Marta miró el reloj. Iba a llegar tarde. ¿Por qué siempre le pasaba lo mismo? (indirecto libre)",
     "ejemplo_incorrecto": "Marta dijo que iba a llegar tarde y preguntó por qué siempre le pasaba. (indirecto normal)"},

    {"numero": 810, "bloque": "A", "nivel": "maestria", "modulo": "c2",
     "titulo": "Repaso integrador A (registro literario)",
     "teoria": "Repaso del bloque A: léxico culto, adjetivación literaria, sintaxis del período largo, ritmo, figuras retóricas, estilo nominal/verbal, elipsis, punto de vista.",
     "explicacion": "Ejemplo integrador: 'La casa, con sus muros de cal y sus ventanas ciegas, olía a tiempo detenido. Nada se movía. Solo el viento, que se colaba por las rendijas, susurraba nombres olvidados. Afuera, el mundo seguía; adentro, el silencio era una forma de eternidad'.",
     "regla": "registro literario = léxico + sintaxis + ritmo + figuras + punto de vista",
     "ejemplo_correcto": "La casa olía a tiempo detenido; el silencio, a eternidad.",
     "ejemplo_incorrecto": "La casa estaba vieja y silenciosa. (registro neutro)"},
]

EJERCICIOS = {
    801: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué caracteriza el registro literario avanzado?",
        "opciones": [
            {"id": "a", "texto": "léxico preciso + sintaxis variada + ritmo propio", "correcta": True, "razon": "Los 3 pilares."},
            {"id": "b", "texto": "solo palabras raras", "correcta": False, "razon": "Insuficiente."},
            {"id": "c", "texto": "solo oraciones cortas", "correcta": False, "razon": "Incompleto."},
        ], "justificacion_obligatoria": False, "regla": "registro literario completo"}}],
    802: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Efímero» significa:",
        "opciones": [
            {"id": "a", "texto": "que dura poco", "correcta": True, "razon": "Cultismo."},
            {"id": "b", "texto": "que dura mucho", "correcta": False, "razon": "Opuesto."},
            {"id": "c", "texto": "eterno", "correcta": False, "razon": "Opuesto."},
        ], "justificacion_obligatoria": False, "regla": "efímero = breve"}}],
    803: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué adjetivo es más literario para un cielo gris?",
        "opciones": [
            {"id": "a", "texto": "ceniciento", "correcta": True, "razon": "Matiz literario."},
            {"id": "b", "texto": "gris", "correcta": False, "razon": "Genérico."},
            {"id": "c", "texto": "feo", "correcta": False, "razon": "Subjetivo."},
        ], "justificacion_obligatoria": False, "regla": "adjetivo de matiz"}}],
    804: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuántas subordinadas debe tener un período largo controlado?",
        "opciones": [
            {"id": "a", "texto": "máximo 4-5", "correcta": True, "razon": "Control."},
            {"id": "b", "texto": "10 o más", "correcta": False, "razon": "Ilegible."},
            {"id": "c", "texto": "ninguna", "correcta": False, "razon": "No es período largo."},
        ], "justificacion_obligatoria": False, "regla": "máx 4-5 subordinadas"}}],
    805: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué recurso crea ritmo en la prosa?",
        "opciones": [
            {"id": "a", "texto": "alternancia de oraciones largas y cortas", "correcta": True, "razon": "Cadencia."},
            {"id": "b", "texto": "todas las oraciones iguales", "correcta": False, "razon": "Monótono."},
            {"id": "c", "texto": "sin pausas", "correcta": False, "razon": "Agota."},
        ], "justificacion_obligatoria": False, "regla": "alternancia"}}],
    806: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«El silencio era ensordecedor» es un ejemplo de:",
        "opciones": [
            {"id": "a", "texto": "paradoja", "correcta": True, "razon": "Contradicción aparente."},
            {"id": "b", "texto": "metáfora", "correcta": False, "razon": "No es identificación."},
            {"id": "c", "texto": "anáfora", "correcta": False, "razon": "No hay repetición."},
        ], "justificacion_obligatoria": False, "regla": "paradoja"}}],
    807: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué estilo es más reflexivo?",
        "opciones": [
            {"id": "a", "texto": "nominal", "correcta": True, "razon": "Sustantivos abstractos."},
            {"id": "b", "texto": "verbal", "correcta": False, "razon": "Más dinámico."},
            {"id": "c", "texto": "coloquial", "correcta": False, "razon": "No aplica."},
        ], "justificacion_obligatoria": False, "regla": "nominal = reflexivo"}}],
    808: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Abrió la puerta. Vacío. Cerró». Es un ejemplo de:",
        "opciones": [
            {"id": "a", "texto": "elipsis y silencio", "correcta": True, "razon": "Sugerir sin explicar."},
            {"id": "b", "texto": "hipotaxis", "correcta": False, "razon": "No hay subordinadas."},
            {"id": "c", "texto": "figura retórica", "correcta": False, "razon": "No específicamente."},
        ], "justificacion_obligatoria": False, "regla": "elipsis + silencio"}}],
    809: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Marta miró el reloj. Iba a llegar tarde. ¿Por qué siempre le pasaba?» es:",
        "opciones": [
            {"id": "a", "texto": "estilo indirecto libre", "correcta": True, "razon": "3ª persona + subjetividad."},
            {"id": "b", "texto": "estilo directo", "correcta": False, "razon": "Faltan comillas."},
            {"id": "c", "texto": "estilo indirecto normal", "correcta": False, "razon": "Falta 'dijo que'."},
        ], "justificacion_obligatoria": False, "regla": "indirecto libre"}}],
    810: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál combina el registro literario correctamente?",
        "opciones": [
            {"id": "a", "texto": "La casa olía a tiempo detenido; el silencio, a eternidad.", "correcta": True, "razon": "Léxico + elipsis + ritmo."},
            {"id": "b", "texto": "La casa estaba vieja y silenciosa.", "correcta": False, "razon": "Registro neutro."},
            {"id": "c", "texto": "La casa tenía un olor raro.", "correcta": False, "razon": "Coloquial."},
        ], "justificacion_obligatoria": False, "regla": "registro literario completo"}}],
}

# Bloques B y C (811-830): ironía fina + intertextualidad
from .tecnicas_c2_bloque_b import TECNICAS_811_820, EJERCICIOS_811_820
from .tecnicas_c2_bloque_c import TECNICAS_821_830, EJERCICIOS_821_830
TECNICAS.extend(TECNICAS_811_820)
TECNICAS.extend(TECNICAS_821_830)
EJERCICIOS.update(EJERCICIOS_811_820)
EJERCICIOS.update(EJERCICIOS_821_830)

# Bloques D y E (831-850): discurso especializado + argumentación compleja
from .tecnicas_c2_bloque_d import TECNICAS_831_840, EJERCICIOS_831_840
from .tecnicas_c2_bloque_e import TECNICAS_841_850, EJERCICIOS_841_850
TECNICAS.extend(TECNICAS_831_840)
TECNICAS.extend(TECNICAS_841_850)
EJERCICIOS.update(EJERCICIOS_831_840)
EJERCICIOS.update(EJERCICIOS_841_850)

# Bloques F y G (851-870): variación dialectal + estilística avanzada
from .tecnicas_c2_bloque_f import TECNICAS_851_860, EJERCICIOS_851_860
from .tecnicas_c2_bloque_g import TECNICAS_861_870, EJERCICIOS_861_870
TECNICAS.extend(TECNICAS_851_860)
TECNICAS.extend(TECNICAS_861_870)
EJERCICIOS.update(EJERCICIOS_851_860)
EJERCICIOS.update(EJERCICIOS_861_870)

# Bloques H y I (871-890): creación literaria + ensayo de autor
from .tecnicas_c2_bloque_h import TECNICAS_871_880, EJERCICIOS_871_880
from .tecnicas_c2_bloque_i import TECNICAS_881_890, EJERCICIOS_881_890
TECNICAS.extend(TECNICAS_871_880)
TECNICAS.extend(TECNICAS_881_890)
EJERCICIOS.update(EJERCICIOS_871_880)
EJERCICIOS.update(EJERCICIOS_881_890)
