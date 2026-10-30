"""Bloque C del modulo C1: cohesión y coherencia textual avanzadas."""

TECNICAS_721_730 = [
    {"numero": 721, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Cohesión léxica: sinónimos y antónimos",
     "teoria": "La cohesión léxica usa sinónimos (para evitar repetición) y antónimos (para contrastar) como mecanismos de conexión entre oraciones.",
     "explicacion": "Ej: 'El problema es grave. La dificultad radica en la falta de datos'. 'El calor era insoportable; el frío, en cambio, era agradable'. Los sinónimos evitan la monotonía; los antónimos crean contraste. Son mecanismos de cohesión entre oraciones.",
     "regla": "sinónimos = evitar repetición | antónimos = contraste",
     "ejemplo_correcto": "La casa era amplia. El hogar, sin embargo, se sentía pequeño.",
     "ejemplo_incorrecto": "La casa era amplia. La casa tenía jardín. La casa era bonita. (repetición monótona)"},

    {"numero": 722, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Cohesión léxica: hiperónimos e hipónimos",
     "teoria": "Los hiperónimos son términos generales (animal, mueble). Los hipónimos son términos específicos (perro, silla). Sustituir un hipónimo por su hiperónimo mantiene la referencia.",
     "explicacion": "Ej: 'Compré un perro. El animal es muy cariñoso' (perro = hipónimo; animal = hiperónimo). 'Compré una silla. El mueble es de madera'. El hiperónimo abstrae; el hipónimo concreta. Combinar ambos evita repeticiones.",
     "regla": "hiperónimo = general | hipónimo = específico | sustituir uno por otro",
     "ejemplo_correcto": "Visitamos el Prado. El museo estaba lleno.",
     "ejemplo_incorrecto": "Visitamos el Prado. El Prado estaba lleno. (repetición, mejor 'el museo')"},

    {"numero": 723, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Cohesión gramatical: pronombres anafóricos",
     "teoria": "Los pronombres anafóricos remiten a un elemento ya mencionado (antecedente). Son clave para evitar repeticiones.",
     "explicacion": "Ej: 'Compré un libro. Lo leí en dos días' (lo = el libro). 'María llegó tarde. Ella no avisó'. 'Los alumnos estudiaron; ellos aprobaron'. Los pronombres (lo, la, los, las, él, ella, ellos, su, este, ese, aquel) mantienen la cadena referencial.",
     "regla": "pronombre anafórico remite al antecedente (evita repetición)",
     "ejemplo_correcto": "Juan compró un coche y lo estrenó el mismo día.",
     "ejemplo_incorrecto": "Juan compró un coche y estrenó un coche el mismo día. (repetición, mejor 'lo')"},

    {"numero": 724, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Cohesión gramatical: elipsis",
     "teoria": "La elipsis omite elementos ya mencionados porque el contexto los sobreentiende. Evita repeticiones y agiliza el texto.",
     "explicacion": "Ej: 'Juan estudia derecho; María, medicina' (elipsis de 'estudia'). 'Unos prefieren el cine; otros, el teatro' (elipsis de 'prefieren'). 'Yo fui al cine y (yo) volví tarde'. La elipsis es frecuente en coordinadas y comparaciones.",
     "regla": "elipsis = omitir lo sobreentendido",
     "ejemplo_correcto": "Pedro lee novelas; Ana, poesía.",
     "ejemplo_incorrecto": "Pedro lee novelas; Ana lee poesía. (correcto pero sin elipsis)"},

    {"numero": 725, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Cohesión: sustitución léxica con verbos comodín",
     "teoria": "Los verbos comodín (hacer, tener, dar, poner, pasar) y los sustantivos comodín (cosa, hecho) sustituyen a otros términos ya mencionados.",
     "explicacion": "Ej: 'Escribió la carta y lo hizo con cuidado' (hizo = escribir la carta). 'Aprobó el examen y eso le dio confianza' (eso = aprobar el examen). Los comodines son cohesionadores, pero abusar de ellos empobrece el texto.",
     "regla": "verbo comodín (hacer, dar, tener) + referencia a lo anterior",
     "ejemplo_correcto": "Pintó el cuadro y lo hizo con paciencia.",
     "ejemplo_incorrecto": "Pintó el cuadro y lo pintó con paciencia. (repetición, mejor 'lo hizo')"},

    {"numero": 726, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Conectores de reformulación avanzada",
     "teoria": "Reformulan lo dicho: explicación (esto es, es decir), corrección (mejor dicho, más bien), resumen (en resumen, en síntesis), ejemplificación (por ejemplo, así).",
     "explicacion": "Ej: 'Es un texto técnico; esto es, requiere conocimientos previos'. 'Llegó tarde; mejor dicho, no llegó'. 'En resumen, la propuesta es viable'. 'Los idiomas, por ejemplo el francés, son útiles'. Cada conector tiene una función específica.",
     "regla": "esto es / es decir (explicación) | mejor dicho / más bien (corrección) | en resumen / en síntesis (resumen) | por ejemplo / así (ejemplificación)",
     "ejemplo_correcto": "No es tonto; más bien, es distraído.",
     "ejemplo_incorrecto": "No es tonto; por ejemplo, es distraído. (por ejemplo no es corrección)"},

    {"numero": 727, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Progresión temática: tema-rema",
     "teoria": "El tema es la información conocida (inicio de la oración). El rema es la información nueva (final). La progresión temática asegura el avance del texto.",
     "explicacion": "Ej: 'El gato (tema) duerme en el sofá (rema). El sofá (tema) es de terciopelo (rema)'. Cada rema se convierte en tema de la siguiente oración. Así avanza la información sin perder el hilo. Si no hay progresión, el texto se estanca o se rompe.",
     "regla": "tema (conocido) → rema (nuevo) → nuevo tema (el rema anterior)",
     "ejemplo_correcto": "La casa era grande. La grandeza, sin embargo, no la hacía acogedora.",
     "ejemplo_incorrecto": "La casa era grande. El perro ladraba. (sin conexión temática)"},

    {"numero": 728, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Coherencia global: unidad temática",
     "teoria": "La coherencia global exige que todo el texto gire en torno a una idea central, sin digresiones que rompan la unidad.",
     "explicacion": "Ej: si el ensayo es sobre 'la IA en educación', todos los párrafos deben apoyar la tesis, no hablar de 'la IA en medicina' o de 'la historia de internet'. Las digresiones se eliminan o se subordinan al tema. La coherencia es la idea global; la cohesión son los mecanismos locales.",
     "regla": "coherencia = unidad temática global | cohesión = mecanismos locales",
     "ejemplo_correcto": "Todos los párrafos contribuyen a la tesis sobre la IA en educación.",
     "ejemplo_incorrecto": "El ensayo sobre IA en educación dedica dos párrafos a la historia del teléfono. (digresión)"},

    {"numero": 729, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Marcadores discursivos y modalización",
     "teoria": "Los marcadores discursivos estructuran el texto. La modalización expresa la posición del hablante (certeza, duda, posibilidad).",
     "explicacion": "Marcadores: 'en primer lugar', 'por último', 'en consecuencia', 'sin embargo'. Modalización: 'sin duda', 'quizás', 'ciertamente', 'a mi juicio', 'probablemente'. Combinar ambos da riqueza argumentativa al texto. En un ensayo académico se usan con frecuencia.",
     "regla": "marcadores = estructuran | modalizadores = posición del hablante",
     "ejemplo_correcto": "En primer lugar, es necesario revisar los datos. Sin duda, la conclusión es compleja.",
     "ejemplo_incorrecto": "Los datos son así y ya está. (sin marcadores ni modalización)"},

    {"numero": 730, "bloque": "C", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Repaso integrador C (cohesión y coherencia)",
     "teoria": "Repaso: cohesión léxica (sinónimos, antónimos, hiperónimos, hipónimos), cohesión gramatical (pronombres, elipsis, sustitución), conectores de reformulación, progresión temática, coherencia global, marcadores discursivos y modalización.",
     "explicacion": "Ejemplo integrador: 'El proyecto tiene varias ventajas. En primer lugar, es viable. En resumen, la propuesta es sólida. Sin duda, requiere ajustes, pero los beneficios son claros. En definitiva, procedamos'.",
     "regla": "cohesión (léxica + gramatical) + conectores + progresión + coherencia + marcadores",
     "ejemplo_correcto": "En primer lugar, la propuesta es viable. En resumen, requiere ajustes, pero los beneficios son claros.",
     "ejemplo_incorrecto": "La propuesta es viable. Los beneficios son claros. Hay ajustes. (sin conectores ni progresión)"},
]

EJERCICIOS_721_730 = {
    721: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«El problema es grave. La dificultad radica en...» usa:",
        "opciones": [
            {"id": "a", "texto": "sinónimos como cohesión", "correcta": True, "razon": "problema → dificultad."},
            {"id": "b", "texto": "antónimos", "correcta": False, "razon": "No son contrarios."},
            {"id": "c", "texto": "elipsis", "correcta": False, "razon": "No se omite nada."},
        ], "justificacion_obligatoria": False, "regla": "cohesión léxica (sinónimos)"}}],
    722: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Visitamos el Prado. El museo estaba lleno». «Museo» sustituye a «Prado» como:",
        "opciones": [
            {"id": "a", "texto": "hiperónimo (museo es general)", "correcta": True, "razon": "Prado es un tipo de museo."},
            {"id": "b", "texto": "hipónimo", "correcta": False, "razon": "Al revés."},
            {"id": "c", "texto": "antónimo", "correcta": False, "razon": "No son contrarios."},
        ], "justificacion_obligatoria": False, "regla": "hiperónimo sustituye al hipónimo"}}],
    723: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Compré un libro. Lo leí en dos días». «Lo» es:",
        "opciones": [
            {"id": "a", "texto": "pronombre anafórico", "correcta": True, "razon": "Remite a 'un libro'."},
            {"id": "b", "texto": "hiperónimo", "correcta": False, "razon": "No es sustantivo."},
            {"id": "c", "texto": "elipsis", "correcta": False, "razon": "No se omite."},
        ], "justificacion_obligatoria": False, "regla": "pronombre anafórico"}}],
    724: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Pedro lee novelas; Ana, poesía» es un ejemplo de:",
        "opciones": [
            {"id": "a", "texto": "elipsis (de 'lee')", "correcta": True, "razon": "Se omite el verbo repetido."},
            {"id": "b", "texto": "sinónimo", "correcta": False, "razon": "No hay sustitución."},
            {"id": "c", "texto": "pronombre", "correcta": False, "razon": "No hay pronombre."},
        ], "justificacion_obligatoria": False, "regla": "elipsis"}}],
    725: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Escribió la carta y lo hizo con cuidado». «Lo hizo» sustituye a:",
        "opciones": [
            {"id": "a", "texto": "escribir la carta (verbo comodín)", "correcta": True, "razon": "hacer = comodín."},
            {"id": "b", "texto": "la carta", "correcta": False, "razon": "No es solo el objeto."},
            {"id": "c", "texto": "con cuidado", "correcta": False, "razon": "Es el modo."},
        ], "justificacion_obligatoria": False, "regla": "verbo comodín"}}],
    726: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué conector es de corrección?",
        "opciones": [
            {"id": "a", "texto": "mejor dicho", "correcta": True, "razon": "Reformula corrigiendo."},
            {"id": "b", "texto": "por ejemplo", "correcta": False, "razon": "Ejemplificación."},
            {"id": "c", "texto": "en resumen", "correcta": False, "razon": "Resumen."},
        ], "justificacion_obligatoria": False, "regla": "mejor dicho = corrección"}}],
    727: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En «El gato duerme en el sofá», ¿cuál es el rema?",
        "opciones": [
            {"id": "a", "texto": "duerme en el sofá", "correcta": True, "razon": "Información nueva."},
            {"id": "b", "texto": "el gato", "correcta": False, "razon": "Eso es el tema."},
            {"id": "c", "texto": "duerme", "correcta": False, "razon": "Parte del rema."},
        ], "justificacion_obligatoria": False, "regla": "rema = información nueva"}}],
    728: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué es la coherencia global?",
        "opciones": [
            {"id": "a", "texto": "Unidad temática de todo el texto", "correcta": True, "razon": "Definición."},
            {"id": "b", "texto": "Uso de pronombres", "correcta": False, "razon": "Es cohesión."},
            {"id": "c", "texto": "Los conectores", "correcta": False, "razon": "Son cohesión."},
        ], "justificacion_obligatoria": False, "regla": "coherencia = unidad global"}}],
    729: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Sin duda, la conclusión es compleja». «Sin duda» es:",
        "opciones": [
            {"id": "a", "texto": "marcador modalizador", "correcta": True, "razon": "Expresa certeza."},
            {"id": "b", "texto": "conector de reformulación", "correcta": False, "razon": "No reformula."},
            {"id": "c", "texto": "pronombre anafórico", "correcta": False, "razon": "No es pronombre."},
        ], "justificacion_obligatoria": False, "regla": "modalizador = posición"}}],
    730: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál combina cohesión y coherencia correctamente?",
        "opciones": [
            {"id": "a", "texto": "En primer lugar, la propuesta es viable. En resumen, requiere ajustes, pero los beneficios son claros.", "correcta": True, "razon": "Marcadores + conectores + progresión."},
            {"id": "b", "texto": "La propuesta es viable. Los beneficios son claros. Hay ajustes.", "correcta": False, "razon": "Sin conectores."},
            {"id": "c", "texto": "Vi un perro. El espacio es infinito. (digresión)", "correcta": False, "razon": "Sin coherencia."},
        ], "justificacion_obligatoria": False, "regla": "cohesión + coherencia"}}],
}
