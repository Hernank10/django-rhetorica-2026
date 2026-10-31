"""Bloque I del modulo C2: ensayo de autor."""

TECNICAS_881_890 = [
    {"numero": 881, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "El ensayo personal: voz y experiencia",
     "teoria": "El ensayo personal parte de la experiencia del autor y la eleva a reflexión general. La primera persona no es confesión: es construcción de voz.",
     "explicacion": "Rasgos: experiencia vivida como punto de partida, reflexión que generaliza, voz reconocible, digresiones controladas. Referentes: Montaigne ('los Ensayos'), Ortega y Gasset, Rosa Montero, Joan Didion. La experiencia no sustituye el argumento: lo ancla. El 'yo' del ensayo es una construcción textual, no el autor real.",
     "regla": "ensayo personal = experiencia + reflexión general + voz construida",
     "ejemplo_correcto": "«Recuerdo la primera vez que entendí la muerte. Tenía siete años y mi abuela...» (ensayo personal sobre la finitud).",
     "ejemplo_incorrecto": "«Me pasó una cosa y por eso pienso que sí». (sin reflexión general)"},

    {"numero": 882, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "El ensayo crítico: criterio y evidencia",
     "teoria": "El ensayo crítico evalúa una obra, un fenómeno o una idea con criterio explícito y evidencia. No es opinión: es valoración razonada.",
     "explicacion": "Estructura: descripción del objeto + criterio explícito + análisis con evidencia + valoración razonada. Recursos: citas textuales, comparación con otras obras, contexto histórico. Referentes: T.S. Eliot, Northrop Frye, Harold Bloom, Susan Sontag. La valoración sin criterio es impresionismo; el criterio sin evidencia es dogma.",
     "regla": "ensayo crítico = criterio + evidencia + análisis + valoración razonada",
     "ejemplo_correcto": "«La novela arriesga una estructura fragmentaria que, si bien desconcierta al inicio, acaba construyendo una memoria coral potente».",
     "ejemplo_incorrecto": "«Me gustó mucho, es muy buena». (sin criterio ni evidencia)"},

    {"numero": 883, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "El ensayo aforístico",
     "teoria": "El ensayo aforístico construye pensamiento por fragmentos breves y autónomos que se iluminan mutuamente. No es colección de frases: es red de ideas.",
     "explicacion": "Rasgos: unidades breves (1-3 frases), densidad conceptual, forma abierta, conexión no lineal. Referentes: Nietzsche ('Aurora', 'La gaya ciencia'), Cioran, Antonio Machado ('Juan de Mairena'), Nicolás Gómez Dávila. La disposición de los aforismos crea sentido: no es arbitraria. Cada uno es una chispa; el conjunto, un sistema.",
     "regla": "ensayo aforístico = fragmentos breves + densidad + forma abierta + red de ideas",
     "ejemplo_correcto": "«Quien no puede callar, no sabe aún lo que piensa». (aforismo que exige reflexión)",
     "ejemplo_incorrecto": "Colección de frases célebres ajenas. (no es ensayo aforístico propio)"},

    {"numero": 884, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "La columna periodística de autor",
     "teoria": "La columna periodística firma una voz personal sobre la actualidad. Es ensayo breve aplicado al presente.",
     "explicacion": "Rasgos: anclaje en un hecho actual, voz reconocible, argumentación breve (600-900 palabras), cierre con gancho o propuesta. Recursos: ironía, anécdota, pregunta retórica. Referentes: Javier Marías, Manuel Vicent, Elvira Lindo, Leila Guerriero. La columna no informa: interpreta la información desde una voz.",
     "regla": "columna = actualidad + voz + interpretación + cierre con gancho",
     "ejemplo_correcto": "«La reforma educativa aprobada ayer ignora la evidencia acumulada durante décadas».",
     "ejemplo_incorrecto": "«Pienso que la reforma es mala». (sin argumentación ni voz)"},

    {"numero": 885, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "El ensayo como forma abierta",
     "teoria": "El ensayo es forma abierta: no cierra la cuestión, la abre. Su objetivo no es clausurar el debate, sino iluminarlo.",
     "explicacion": "Rasgos: pregunta inicial más que tesis cerrada, digresiones significativas, cierre abierto o con nuevas preguntas, incorporación de la duda. Referentes: Montaigne ('Que sais-je?'), Lukács ('Sobre la esencia y forma del ensayo'), Adorno ('El ensayo como forma'). El ensayo es el género de la duda productiva.",
     "regla": "ensayo = pregunta + iluminación + cierre abierto | no clausura",
     "ejemplo_correcto": "«¿Qué significa enseñar hoy? Quizá esta pregunta no tenga respuesta, pero formularla ya es una respuesta».",
     "ejemplo_incorrecto": "«La conclusión es X y no admite discusión». (dogmático, no ensayístico)"},

    {"numero": 886, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "Ironía y humor en el ensayo",
     "teoria": "La ironía y el humor no son adorno del ensayo: son herramientas críticas que permiten tomar distancia y desestabilizar lo obvio.",
     "explicacion": "Recursos: ironía verbal ('¡Magnífica la idea de privatizar el agua!'), humor como distancia crítica, parodia de estilos. Referentes: Swift, Sterne, Borges, Umberto Eco, Javier Marías. La ironía permite decir lo que no se puede decir de otro modo. El humor rebaja la solemnidad y aumenta la lucidez.",
     "regla": "ironía + humor = distancia crítica + lucidez + desestabilización de lo obvio",
     "ejemplo_correcto": "«La propuesta de reducir derechos para 'protegerlos' merece un capítulo aparte en la historia de la lógica».",
     "ejemplo_incorrecto": "Humor como fin en sí mismo. (sin función crítica)"},

    {"numero": 887, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "Citas y erudición: uso y abuso",
     "teoria": "Citar en el ensayo no es adorno: es diálogo. Se cita para apoyar, discutir, contrastar. El abuso de citas empobrece la voz propia.",
     "explicacion": "Usos: cita de autoridad (apoyo), cita de contraste ('Como dice X..., aunque...'), cita crítica (para refutar). Formatos: cita textual con referencia, paráfrasis, cita alusiva. La cita debe integrarse en el argumento, no sustituirlo. El ensayo debe tener voz propia aunque dialogue con otros.",
     "regla": "citas = apoyo + contraste + crítica | siempre integradas en el argumento",
     "ejemplo_correcto": "«Como señala Eco, el lector modelo no es el lector real, sino una estrategia textual; sin embargo, esta distinción se difumina en la era digital».",
     "ejemplo_incorrecto": "«Según X: [cita]. Según Y: [cita]. Según Z: [cita]». (sin voz propia)"},

    {"numero": 888, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "La conclusión abierta: cómo cerrar sin cerrar",
     "teoria": "La conclusión del ensayo no repite lo dicho: recapitula y proyecta. Puede cerrar con una pregunta, una imagen o una propuesta que abra el debate.",
     "explicacion": "Tipos: síntesis + proyección ('queda abierto...'), pregunta final, imagen que condensa, propuesta práctica. Evitar: repetir todo lo dicho, cierre moralizante ('debemos reflexionar'), cierre grandilocuente vacío. Referentes: ensayos de Ortega, Paz, Sontag. La conclusión debe dejar al lector pensando, no descansando.",
     "regla": "conclusión = síntesis + proyección + apertura | no repetición ni moraleja",
     "ejemplo_correcto": "«Quizá la pregunta no sea 'cómo enseñar' sino 'para qué seguir enseñando cuando todo está a un clic'».",
     "ejemplo_incorrecto": "«En conclusión, hemos visto X, Y, Z y debemos reflexionar». (repite y moraliza)"},

    {"numero": 889, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "El ensayo breve de revista",
     "teoria": "El ensayo breve de revista (1000-2000 palabras) exige máxima concentración: una idea, desarrollada con precisión, sin digresiones largas.",
     "explicacion": "Rasgos: tesis concentrada, desarrollo lineal, ejemplos precisos, cierre eficaz. Diferencia con el ensayo largo: menos digresiones, más economía. Referentes: The New Yorker, Letras Libres, The Atlantic. La brevedad no es superficialidad: es concentración.",
     "regla": "ensayo breve = una idea + desarrollo preciso + cierre eficaz | sin digresiones largas",
     "ejemplo_correcto": "«¿Por qué ya no leemos novelas largas? Quizá porque la atención se ha fragmentado, pero también porque la novela larga exige una fe que hemos perdido».",
     "ejemplo_incorrecto": "Cuatro tesis distintas en 1500 palabras. (ninguna se desarrolla)"},

    {"numero": 890, "bloque": "I", "nivel": "maestria", "modulo": "c2",
     "titulo": "Repaso integrador I (ensayo de autor)",
     "teoria": "Repaso: ensayo personal, ensayo crítico, ensayo aforístico, columna periodística, ensayo abierto, ironía y humor, citas y erudición, conclusión abierta, ensayo breve.",
     "explicacion": "Ejemplo integrador: 'El ensayo personal parte de la experiencia y generaliza. La ironía desestabiliza lo obvio. Las citas dialogan con otros sin sustituir la voz. La conclusión abre, no cierra. Según el formato (columna, ensayo breve, aforístico), cambia la extensión y la densidad, pero el principio es el mismo: pensar en voz alta con lucidez y criterio'.",
     "regla": "ensayo = voz + argumento + ironía + citas + conclusión abierta según formato",
     "ejemplo_correcto": "El ensayista combina experiencia, ironía y criterio para iluminar una pregunta.",
     "ejemplo_incorrecto": "Opinión sin criterio ni evidencia. (no es ensayo)"},
]

EJERCICIOS_881_890 = {
    881: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El ensayo personal parte de:",
        "opciones": [
            {"id": "a", "texto": "la experiencia del autor + reflexión general", "correcta": True, "razon": "Voz construida."},
            {"id": "b", "texto": "la confesión íntima sin generalización", "correcta": False, "razon": "No es ensayo."},
            {"id": "c", "texto": "solo datos", "correcta": False, "razon": "Sin voz."},
        ], "justificacion_obligatoria": False, "regla": "ensayo personal"}}],
    882: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El ensayo crítico exige:",
        "opciones": [
            {"id": "a", "texto": "criterio explícito + evidencia", "correcta": True, "razon": "Valoración razonada."},
            {"id": "b", "texto": "solo gusto personal", "correcta": False, "razon": "Impresionismo."},
            {"id": "c", "texto": "solo resumen", "correcta": False, "razon": "Insuficiente."},
        ], "justificacion_obligatoria": False, "regla": "crítico: criterio + evidencia"}}],
    883: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El ensayo aforístico se construye por:",
        "opciones": [
            {"id": "a", "texto": "fragmentos breves autónomos + densidad", "correcta": True, "razon": "Red de ideas."},
            {"id": "b", "texto": "capítulos extensos", "correcta": False, "razon": "Contrario."},
            {"id": "c", "texto": "citas ajenas", "correcta": False, "razon": "No es propio."},
        ], "justificacion_obligatoria": False, "regla": "aforístico"}}],
    884: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La columna periodística parte de:",
        "opciones": [
            {"id": "a", "texto": "un hecho de actualidad + voz autoral", "correcta": True, "razon": "Interpretación."},
            {"id": "b", "texto": "una ficción", "correcta": False, "razon": "No."},
            {"id": "c", "texto": "un poema", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "columna periodística"}}],
    885: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El ensayo como forma abierta se caracteriza por:",
        "opciones": [
            {"id": "a", "texto": "pregunta + iluminación + cierre abierto", "correcta": True, "razon": "Duda productiva."},
            {"id": "b", "texto": "tesis cerrada + conclusión dogmática", "correcta": False, "razon": "Contrario."},
            {"id": "c", "texto": "solo datos", "correcta": False, "razon": "No es ensayo."},
        ], "justificacion_obligatoria": False, "regla": "ensayo abierto"}}],
    886: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La ironía en el ensayo sirve para:",
        "opciones": [
            {"id": "a", "texto": "tomar distancia crítica y desestabilizar lo obvio", "correcta": True, "razon": "Herramienta crítica."},
            {"id": "b", "texto": "adornar el texto", "correcta": False, "razon": "Insuficiente."},
            {"id": "c", "texto": "mostrar superioridad", "correcta": False, "razon": "Empobrece."},
        ], "justificacion_obligatoria": False, "regla": "ironía crítica"}}],
    887: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El abuso de citas en el ensayo produce:",
        "opciones": [
            {"id": "a", "texto": "pérdida de voz propia", "correcta": True, "razon": "Las citas deben integrarse."},
            {"id": "b", "texto": "más autoridad siempre", "correcta": False, "razon": "No: puede ser parasitario."},
            {"id": "c", "texto": "erudición garantizada", "correcta": False, "razon": "Falso."},
        ], "justificacion_obligatoria": False, "regla": "citas: uso y abuso"}}],
    888: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La conclusión del ensayo debe:",
        "opciones": [
            {"id": "a", "texto": "sintetizar + proyectar + abrir", "correcta": True, "razon": "Deja pensando."},
            {"id": "b", "texto": "repetir todo lo dicho", "correcta": False, "razon": "Empobrece."},
            {"id": "c", "texto": "moralizar", "correcta": False, "razon": "Suele sonar vacío."},
        ], "justificacion_obligatoria": False, "regla": "conclusión abierta"}}],
    889: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El ensayo breve de revista exige:",
        "opciones": [
            {"id": "a", "texto": "una idea + desarrollo preciso + cierre eficaz", "correcta": True, "razon": "Concentración."},
            {"id": "b", "texto": "cuatro tesis en paralelo", "correcta": False, "razon": "Ninguna se desarrolla."},
            {"id": "c", "texto": "digresiones largas", "correcta": False, "razon": "No cabe."},
        ], "justificacion_obligatoria": False, "regla": "ensayo breve"}}],
    890: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué combina bien el ensayo de autor?",
        "opciones": [
            {"id": "a", "texto": "voz + argumento + ironía + citas + conclusión abierta", "correcta": True, "razon": "Todos los recursos."},
            {"id": "b", "texto": "solo opinión", "correcta": False, "razon": "Insuficiente."},
            {"id": "c", "texto": "solo citas", "correcta": False, "razon": "Sin voz."},
        ], "justificacion_obligatoria": False, "regla": "repaso I"}}],
}
