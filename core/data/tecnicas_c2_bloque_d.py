"""Bloque D del modulo C2: discurso especializado."""

TECNICAS_831_840 = [
    {"numero": 831, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje jurídico: precisión y performatividad",
     "teoria": "El lenguaje jurídico se caracteriza por la precisión terminológica, la performatividad (el decir hace) y las fórmulas fijas que no admiten variación.",
     "explicacion": "Rasgos: tecnicismos ('usufructo', 'dolo', 'prescripción'), locuciones fijas ('a tenor de', 'en virtud de', 'sin perjuicio de'), enunciados performativos ('declaro', 'otorgo', 'condeno'), impersonalidad ('se procede a', 'por medio de la presente'). Su función no es informar, sino vincular jurídicamente. La ambigüedad es un defecto grave: cada término tiene un referente único.",
     "regla": "jurídico = precisión + fórmulas fijas + performatividad + impersonalidad",
     "ejemplo_correcto": "En virtud de lo dispuesto, se procede a la apertura del expediente.",
     "ejemplo_incorrecto": "Vamos a abrir el expediente y ya veremos. (registro coloquial, sin fórmulas)"},

    {"numero": 832, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje médico: tecnicismos y metáforas",
     "teoria": "El lenguaje médico combina tecnicismos grecolatinos con metáforas que traducen lo técnico a lo comprensible. En registro especializado domina la precisión; en divulgación, la analogía.",
     "explicacion": "Tecnicismos: 'infarto agudo de miocardio', 'adenocarcinoma', 'hipertensión arterial'. Metáforas: 'el corazón es una bomba', 'las neuronas son cables', 'el sistema inmune es un ejército'. En la consulta, el médico traduce: 'tiene usted una obstrucción en una arteria' por 'infarto'. La elección depende del interlocutor (colegas vs pacientes).",
     "regla": "médico = tecnicismo (especialista) | metáfora/analogía (paciente)",
     "ejemplo_correcto": "El sistema inmune actúa como un ejército: identifica y ataca a los invasores.",
     "ejemplo_incorrecto": "Tiene usted una enfermedad de las gordas. (registro inadecuado)"},

    {"numero": 833, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje científico-técnico: precisión y evidencialidad",
     "teoria": "El lenguaje científico exige precisión unívoca, evidencialidad (marcar el grado de certeza) y neutralidad afectiva.",
     "explicacion": "Evidencialidad: 'los datos muestran/sugieren/indican' (grados), 'se observa que', 'es probable que'. Neutralidad: sin primera persona ('se analizó', 'se concluye'). Precisión: 'el 78% de la muestra' (no 'la mayoría'). La escritura científica evita la modalidad apreciativa ('lamentablemente') y la primera persona ('yo opino').",
     "regla": "científico = precisión + evidencialidad + neutralidad afectiva",
     "ejemplo_correcto": "Los datos sugieren una correlación positiva, aunque el tamaño de la muestra limita la generalización.",
     "ejemplo_incorrecto": "¡Yo creo que los datos molan! (registro subjetivo, no científico)"},

    {"numero": 834, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje tecnológico: neologismos y anglicismos",
     "teoria": "El lenguaje tecnológico genera neologismos constantes y absorbe anglicismos. La tensión entre adaptación y préstamo es central.",
     "explicacion": "Neologismos por derivación: 'postear', 'tuitear', 'googlear', 'startup', 'big data'. Anglicismos crudos: 'software', 'hardware', 'email', 'chat'. Adaptaciones: 'correo electrónico' (email), 'ratón' (mouse), 'enlace' (link). La RAE admite algunos (tuit, tuitear) y recomienda equivalentes cuando existen. En registro formal se prefieren los equivalentes.",
     "regla": "tecnológico = neologismo + anglicismo (crudo o adaptado) + tensión normativa",
     "ejemplo_correcto": "El software se actualizó automáticamente. (anglicismo admitido)",
     "ejemplo_incorrecto": "El softwaro se actualizó. (adaptación inventada, no normativa)"},

    {"numero": 835, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje económico-financiero: metáforas y eufemismos",
     "teoria": "El lenguaje económico usa metáforas organicistas y eufemismos que suavizan realidades duras (despidos, crisis, ajustes).",
     "explicacion": "Metáforas: 'la economía crece/se contrae', 'el mercado respira', 'la burbuja estalla', 'el motor económico'. Eufemismos: 'ajuste de plantilla' (despidos), 'flexibilización laboral' (precariedad), 'desaceleración' (recesión), 'contención del gasto' (recortes). El análisis crítico desmonta estos eufemismos revelando la ideología subyacente.",
     "regla": "económico = metáfora organicista + eufemismo (ideología subyacente)",
     "ejemplo_correcto": "El eufemismo 'ajuste de plantilla' oculta los despidos reales.",
     "ejemplo_incorrecto": "Las palabras económicas son neutras. (el ACD lo cuestiona)"},

    {"numero": 836, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje periodístico de élite: análisis y opinión",
     "teoria": "El periodismo de élite (análisis, reportaje de fondo, editorial) combina precisión informativa con interpretación experta y voz autoral.",
     "explicacion": "Géneros: noticia (informativa, pirámide invertida), reportaje (profundidad, fuentes), análisis (interpretación), editorial (opinión institucional), columna (opinión personal). Recursos: fuentes expertas, datos, contexto histórico, comparación internacional. La firma con autoridad marca la diferencia con el periodismo de declaración.",
     "regla": "periodismo élite = información + interpretación + voz experta + fuentes",
     "ejemplo_correcto": "El análisis del Financial Times sitúa la crisis en el contexto de la globalización financiera.",
     "ejemplo_incorrecto": "Un titular sensacionalista sin contexto. (no es periodismo de élite)"},

    {"numero": 837, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje diplomático: eufemismo y cortesía estratégica",
     "teoria": "El lenguaje diplomático usa eufemismos, atenuaciones y fórmulas de cortesía para gestionar conflictos sin confrontación directa.",
     "explicacion": "Fórmulas: 'hemos mantenido un intercambio franco de puntos de vista' (discusión tensa), 'la conversación ha sido constructiva' (sin acuerdo), 'el embajador ha sido llamado a consultas' (protesta formal), 'medidas de confianza mutua' (desescalada). La cortesía no es sinceridad: es estrategia. La interpretación diplomática exige descifrar el subtexto.",
     "regla": "diplomático = eufemismo + cortesía estratégica + subtexto",
     "ejemplo_correcto": "«Intercambio franco de puntos de vista» suele significar desacuerdo profundo.",
     "ejemplo_incorrecto": "«Estamos muy enfadados». (registro no diplomático)"},

    {"numero": 838, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje académico-filosófico: abstracción y densidad",
     "teoria": "El lenguaje académico-filosófico privilegia la abstracción conceptual, la densidad argumentativa y la precisión terminológica.",
     "explicacion": "Rasgos: sustantivos abstractos ('la historicidad', 'la alteridad', 'la contingencia'), verbos de pensamiento ('sostener', 'postular', 'argumentar', 'inferir'), estructuras complejas (subordinadas, incisos), vocabulario técnico ('ontología', 'epistemología', 'hermenéutica'). La escritura filosófica exige lentitud: el lector debe reconstruir el argumento. La claridad no es opcional: Kant o Hegel son densos, pero no oscuros por negligencia.",
     "regla": "académico-filosófico = abstracción + densidad + precisión terminológica",
     "ejemplo_correcto": "La historicidad del sujeto implica su inserción en una tradición que lo precede.",
     "ejemplo_incorrecto": "El sujeto está metido en cosas del pasado. (registro coloquial, no filosófico)"},

    {"numero": 839, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Lenguaje publicitario: persuasión y seducción",
     "teoria": "El lenguaje publicitario persuade mediante la seducción emocional, la brevedad y la retórica visual-verbal. Vende estilos de vida, no productos.",
     "explicacion": "Recursos: eslóganes breves ('Just do it'), imperativos ('Descúbrelo'), preguntas retóricas ('¿Y tú, a qué esperas?'), asociación producto-emoción (felicidad, juventud, éxito), testimonios, hipérboles ('el mejor del mundo'), juegos de palabras ('Fanta, no para de...'). La publicidad no informa: sugiere. El ACD desmonta sus mecanismos.",
     "regla": "publicitario = seducción + brevedad + asociación emocional",
     "ejemplo_correcto": "El eslogan asocia el producto con la libertad y la juventud.",
     "ejemplo_incorrecto": "Compra este detergente porque lava bien. (sin carga persuasiva)"},

    {"numero": 840, "bloque": "D", "nivel": "maestria", "modulo": "c2",
     "titulo": "Repaso integrador D (discurso especializado)",
     "teoria": "Repaso: lenguaje jurídico, médico, científico-técnico, tecnológico, económico-financiero, periodístico de élite, diplomático, académico-filosófico, publicitario.",
     "explicacion": "Ejemplo integrador: 'La sentencia (jurídico) aplica los criterios del informe médico (médico) y los datos del peritaje científico (científico). El editorial (periodístico de élite) analiza el caso con la cautela propia del lenguaje diplomático. La conclusión usa un símil publicitario para persuadir'. Cada registro tiene su función.",
     "regla": "discurso especializado = precisión + registro adecuado + función específica",
     "ejemplo_correcto": "El informe médico usa tecnicismos con colegas y analogías con pacientes.",
     "ejemplo_incorrecto": "Todos los registros son intercambiables. (el ACD lo cuestiona)"},
]

EJERCICIOS_831_840 = {
    831: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué rasgo es típico del lenguaje jurídico?",
        "opciones": [
            {"id": "a", "texto": "fórmulas fijas + performatividad", "correcta": True, "razon": "Precisión y decir-hacer."},
            {"id": "b", "texto": "coloquialidad y libertad creativa", "correcta": False, "razon": "Contrario."},
            {"id": "c", "texto": "metáforas poéticas constantes", "correcta": False, "razon": "No es su función."},
        ], "justificacion_obligatoria": False, "regla": "jurídico: fórmulas + performatividad"}}],
    832: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«El sistema inmune es un ejército» es un ejemplo de lenguaje médico:",
        "opciones": [
            {"id": "a", "texto": "divulgativo (metáfora)", "correcta": True, "razon": "Analogía para paciente."},
            {"id": "b", "texto": "especializado (tecnicismo)", "correcta": False, "razon": "No es tecnicismo."},
            {"id": "c", "texto": "jurídico", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "médico divulgativo: metáfora"}}],
    833: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué recurso es propio del lenguaje científico?",
        "opciones": [
            {"id": "a", "texto": "evidencialidad (los datos sugieren)", "correcta": True, "razon": "Marca grado de certeza."},
            {"id": "b", "texto": "primera persona constante", "correcta": False, "razon": "Se evita."},
            {"id": "c", "texto": "adjetivación emocional", "correcta": False, "razon": "Neutralidad afectiva."},
        ], "justificacion_obligatoria": False, "regla": "científico: evidencialidad"}}],
    834: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Correo electrónico» es adaptación de:",
        "opciones": [
            {"id": "a", "texto": "email (anglicismo)", "correcta": True, "razon": "Equivalente en español."},
            {"id": "b", "texto": "chat", "correcta": False, "razon": "No."},
            {"id": "c", "texto": "software", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "email → correo electrónico"}}],
    835: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Ajuste de plantilla» por «despidos» es un:",
        "opciones": [
            {"id": "a", "texto": "eufemismo económico", "correcta": True, "razon": "Suaviza realidad dura."},
            {"id": "b", "texto": "tecnicismo neutro", "correcta": False, "razon": "Tiene carga ideológica."},
            {"id": "c", "texto": "disfemismo", "correcta": False, "razon": "Opuesto."},
        ], "justificacion_obligatoria": False, "regla": "eufemismo económico"}}],
    836: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué distingue el periodismo de élite?",
        "opciones": [
            {"id": "a", "texto": "análisis + contexto + voz experta", "correcta": True, "razon": "Frente al de declaración."},
            {"id": "b", "texto": "titulares sensacionalistas", "correcta": False, "razon": "No es su rasgo."},
            {"id": "c", "texto": "ausencia de fuentes", "correcta": False, "razon": "Contrario."},
        ], "justificacion_obligatoria": False, "regla": "periodismo élite: análisis"}}],
    837: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Intercambio franco de puntos de vista» en diplomacia suele significar:",
        "opciones": [
            {"id": "a", "texto": "desacuerdo profundo", "correcta": True, "razon": "Eufemismo diplomático."},
            {"id": "b", "texto": "acuerdo total", "correcta": False, "razon": "Opuesto."},
            {"id": "c", "texto": "encuentro informal sin tema", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "eufemismo diplomático"}}],
    838: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué rasgo es típico del lenguaje académico-filosófico?",
        "opciones": [
            {"id": "a", "texto": "abstracción + densidad + precisión", "correcta": True, "razon": "Tres rasgos."},
            {"id": "b", "texto": "coloquialismos y muletillas", "correcta": False, "razon": "Contrario."},
            {"id": "c", "texto": "solo ejemplos cotidianos", "correcta": False, "razon": "Insuficiente."},
        ], "justificacion_obligatoria": False, "regla": "académico-filosófico"}}],
    839: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué hace el lenguaje publicitario?",
        "opciones": [
            {"id": "a", "texto": "seducir, no informar", "correcta": True, "razon": "Asocia emociones."},
            {"id": "b", "texto": "informar objetivamente", "correcta": False, "razon": "No es su fin."},
            {"id": "c", "texto": "solo describir el producto", "correcta": False, "razon": "Insuficiente."},
        ], "justificacion_obligatoria": False, "regla": "publicitario: seducción"}}],
    840: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál combina registros especializados correctamente?",
        "opciones": [
            {"id": "a", "texto": "El informe médico usa tecnicismos con colegas y analogías con pacientes.", "correcta": True, "razon": "Registro según interlocutor."},
            {"id": "b", "texto": "Todos los registros son intercambiables.", "correcta": False, "razon": "Falso."},
            {"id": "c", "texto": "El juez habla como publicista.", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "repaso D"}}],
}
