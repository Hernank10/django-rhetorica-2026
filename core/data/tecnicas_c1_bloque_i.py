"""Bloque I del modulo C1: análisis crítico del discurso."""

TECNICAS_781_790 = [
    {"numero": 781, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Análisis crítico del discurso (ACD): qué es",
     "teoria": "El ACD estudia cómo el discurso construye y reproduce relaciones de poder, ideología e identidad. No es neutral: analiza el sesgo y la manipulación.",
     "explicacion": "El ACD examina: selección léxica (¿'régimen' o 'gobierno'?), estructura sintáctica (¿quién es agente y quién paciente?), uso de metáforas, citas, silencios (lo que no se dice). Figuras clave: Fairclough, Van Dijk, Wodak. Objetivo: deconstruir el discurso para ver su ideología.",
     "regla": "ACD = discurso + poder + ideología + identidad | no es neutral",
     "ejemplo_correcto": "El titular 'el régimen reprimió' usa un léxico cargado que construye una valoración negativa.",
     "ejemplo_incorrecto": "El titular es objetivo porque informa. (ACD cuestiona esa supuesta objetividad)"},

    {"numero": 782, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Léxico cargado: selección y connotación",
     "teoria": "La selección léxica no es neutral: cada palabra trae connotaciones. 'Régimen' vs 'gobierno', 'manifestantes' vs 'disturbios', 'ajuste' vs 'recorte'.",
     "explicacion": "Ejemplos: 'Libertad de expresión' vs 'libertinaje' (el mismo hecho, valorado opuesto). 'Migrantes' vs 'inmigrantes' vs 'ilegales'. 'Conflicto' vs 'guerra'. El análisis crítico identifica la carga ideológica de cada elección léxica. Las connotaciones reproducen visiones del mundo.",
     "regla": "léxico cargado: connotación ideológica en la selección de palabras",
     "ejemplo_correcto": "El uso de 'ajuste' por 'recorte' suaviza la medida económica.",
     "ejemplo_incorrecto": "Las palabras son neutras por definición. (el ACD lo cuestiona)"},

    {"numero": 783, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Falacias argumentativas: tipos frecuentes",
     "teoria": "Las falacias son razonamientos aparentemente válidos pero lógicamente defectuosos. Tipos: ad hominem, ad populum, falsa dicotomía, hombre de paja, pendiente resbaladiza.",
     "explicacion": "Ad hominem: atacar a la persona, no al argumento. Ad populum: apelar a la mayoría ('todo el mundo lo hace'). Falsa dicotomía: 'o conmigo o contra mí'. Hombre de paja: distorsionar el argumento del otro. Pendiente resbaladiza: predecir consecuencias extremas sin base. Detectarlas es parte del análisis crítico.",
     "regla": "falacia = razonamiento aparentemente válido pero defectuoso",
     "ejemplo_correcto": "Su propuesta es mala porque él es joven. (ad hominem)",
     "ejemplo_incorrecto": "Su propuesta tiene datos erróneos, por eso es mala. (argumento válido, no falacia)"},

    {"numero": 784, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Hombre de paja: distorsionar el argumento contrario",
     "teoria": "El 'hombre de paja' (straw man) consiste en exagerar o distorsionar el argumento del adversario para refutarlo más fácilmente.",
     "explicacion": "Ejemplo: A dice: 'Deberíamos revisar el presupuesto de defensa'. B responde: '¿Así que quieres dejar el país indefenso?'. B distorsionó la propuesta (revisar ≠ eliminar). Otra forma: atribuir al adversario una postura que no defendió. Detectar el hombre de paja es esencial en el análisis crítico.",
     "regla": "hombre de paja = distorsionar + refutar la distorsión (no el argumento real)",
     "ejemplo_correcto": "Nadie ha propuesto eliminar la defensa; solo revisar el presupuesto.",
     "ejemplo_incorrecto": "Entonces quieres dejar el país indefenso. (distorsión)"},

    {"numero": 785, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Falsa dicotomía: 'o conmigo o contra mí'",
     "teoria": "La falsa dicotomía presenta solo dos opciones cuando hay más. Es una manipulación frecuente en el discurso político.",
     "explicacion": "Ejemplos: 'O estás con la patria o estás contra ella'. 'O aceptas el acuerdo o quieres el caos'. 'O eres emprendedor o eres fracasado'. En realidad hay matices, terceras vías y posiciones intermedias. La falsa dicotomía simplifica y polariza, excluyendo la reflexión.",
     "regla": "falsa dicotomía: solo dos opciones cuando hay más",
     "ejemplo_correcto": "Podemos rechazar el acuerdo y proponer otro; no es 'caos'.",
     "ejemplo_incorrecto": "O aceptas o quieres el caos. (falsa dicotomía)"},

    {"numero": 786, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Eufemismos y disfemismos: la valoración oculta",
     "teoria": "Los eufemismos suavizan una realidad incómoda; los disfemismos la agravan. Ambos revelan una postura ideológica.",
     "explicacion": "Eufemismos: 'ajuste de plantilla' por 'despidos', 'daño colateral' por 'víctimas civiles', 'flexibilidad laboral' por 'precariedad'. Disfemismos: 'manada' por 'grupo', 'chupóptero' por 'funcionario'. Los medios eligen uno u otro según su línea editorial. El ACD desenmascara esa elección.",
     "regla": "eufemismo = suavizar | disfemismo = agravar | ambos revelan ideología",
     "ejemplo_correcto": "El eufemismo 'ajuste de plantilla' oculta los despidos reales.",
     "ejemplo_incorrecto": "Todos los términos son igual de neutros. (el ACD lo cuestiona)"},

    {"numero": 787, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Quién es agente y quién paciente: la sintaxis como ideología",
     "teoria": "La voz activa o pasiva, el sujeto explícito o elidido, la nominalización: todos construyen responsabilidad y agencia.",
     "explicacion": "Ejemplo: 'La policía reprimió a los manifestantes' (agente explícito) vs 'Hubo disturbios y murieron tres personas' (sin agente, responsabilidad diluida). La pasiva sin agente ('fueron detenidos') oculta quién detuvo. La nominalización ('la destrucción de empleo') convierte un proceso en cosa, borrando responsables. El ACD analiza esa sintaxis.",
     "regla": "agente/paciente + voz + nominalización = responsabilidad construida",
     "ejemplo_correcto": "La pasiva 'fueron detenidos' oculta quién detuvo.",
     "ejemplo_incorrecto": "La sintaxis es solo gramática, no tiene ideología. (el ACD lo cuestiona)"},

    {"numero": 788, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Intertextualidad y citas: legitimación por autoridad",
     "teoria": "Citar a un experto, a una institución o a un texto previo legitima un argumento (o lo descalifica, si la cita es crítica).",
     "explicacion": "Ejemplos: 'Según el FMI...', 'Como dijo Einstein...', 'Los estudios demuestran...'. Las citas pueden ser selectivas (solo lo que apoya la tesis), descontextualizadas (fuera de su marco) o apócrifas (atribuidas falsamente). El análisis crítico verifica la fuente y el contexto.",
     "regla": "intertextualidad: citar legitima | verificar fuente y contexto",
     "ejemplo_correcto": "La cita está sacada de contexto y cambia el sentido original.",
     "ejemplo_incorrecto": "Si lo dijo Einstein, es verdad. (falacia de autoridad)"},

    {"numero": 789, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Lo que no se dice: silencios y ausencias",
     "teoria": "El silencio también construye significado. Lo que no se menciona, lo que se omite, revela una postura ideológica.",
     "explicacion": "Ejemplos: un informe económico que no menciona la desigualdad. Una noticia sobre inmigración que no incluye testimonios de migrantes. Un debate sobre educación sin docentes. El análisis crítico pregunta: ¿qué voces faltan? ¿qué datos no se dan? ¿qué perspectivas se excluyen? El silencio es una elección discursiva.",
     "regla": "silencio discursivo = ausencia reveladora | ¿qué voces faltan?",
     "ejemplo_correcto": "El informe omite la perspectiva de los afectados, lo que revela una postura.",
     "ejemplo_incorrecto": "Lo que no se dice no significa nada. (el ACD lo cuestiona)"},

    {"numero": 790, "bloque": "I", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Repaso integrador I (análisis crítico)",
     "teoria": "Repaso: ACD, léxico cargado, falacias, hombre de paja, falsa dicotomía, eufemismos, sintaxis ideológica, intertextualidad, silencios.",
     "explicacion": "Ejemplo integrador: 'El titular usa un eufemismo (ajuste) para ocultar despidos. La pasiva sin agente diluye la responsabilidad. Presenta una falsa dicotomía: o ajuste o caos. Omite la voz de los trabajadores. El análisis crítico desmonta esa construcción'.",
     "regla": "ACD = léxico + sintaxis + falacias + eufemismos + intertextualidad + silencios",
     "ejemplo_correcto": "El análisis crítico revela la ideología en el léxico, la sintaxis y los silencios.",
     "ejemplo_incorrecto": "El texto es objetivo porque no dice mentiras explícitas. (la ideología puede ser implícita)"},
]

EJERCICIOS_781_790 = {
    781: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El análisis crítico del discurso estudia:",
        "opciones": [
            {"id": "a", "texto": "discurso, poder e ideología", "correcta": True, "razon": "Definición del ACD."},
            {"id": "b", "texto": "solo gramática", "correcta": False, "razon": "Incompleto."},
            {"id": "c", "texto": "solo literatura", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "ACD = discurso + poder"}}],
    782: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Ajuste» por «recorte» es un caso de:",
        "opciones": [
            {"id": "a", "texto": "eufemismo", "correcta": True, "razon": "Suaviza la realidad."},
            {"id": "b", "texto": "disfemismo", "correcta": False, "razon": "Opuesto."},
            {"id": "c", "texto": "falacia", "correcta": False, "razon": "No es razonamiento."},
        ], "justificacion_obligatoria": False, "regla": "eufemismo"}}],
    783: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Su propuesta es mala porque él es joven». Es una falacia:",
        "opciones": [
            {"id": "a", "texto": "ad hominem", "correcta": True, "razon": "Ataca a la persona, no al argumento."},
            {"id": "b", "texto": "ad populum", "correcta": False, "razon": "No apela a la mayoría."},
            {"id": "c", "texto": "pendiente resbaladiza", "correcta": False, "razon": "No predice extremos."},
        ], "justificacion_obligatoria": False, "regla": "ad hominem"}}],
    784: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«¿Así que quieres dejar el país indefenso?». Es un ejemplo de:",
        "opciones": [
            {"id": "a", "texto": "hombre de paja", "correcta": True, "razon": "Distorsiona el argumento."},
            {"id": "b", "texto": "ad hominem", "correcta": False, "razon": "No ataca a la persona."},
            {"id": "c", "texto": "falsa dicotomía", "correcta": False, "razon": "No hay dicotomía explícita."},
        ], "justificacion_obligatoria": False, "regla": "hombre de paja"}}],
    785: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«O estás con la patria o estás contra ella» es:",
        "opciones": [
            {"id": "a", "texto": "falsa dicotomía", "correcta": True, "razon": "Solo dos opciones cuando hay más."},
            {"id": "b", "texto": "eufemismo", "correcta": False, "razon": "No."},
            {"id": "c", "texto": "hombre de paja", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "falsa dicotomía"}}],
    786: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Daño colateral» por «víctimas civiles» es:",
        "opciones": [
            {"id": "a", "texto": "eufemismo", "correcta": True, "razon": "Suaviza la gravedad."},
            {"id": "b", "texto": "disfemismo", "correcta": False, "razon": "Opuesto."},
            {"id": "c", "texto": "falacia", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "eufemismo"}}],
    787: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Hubo disturbios y murieron tres personas» oculta:",
        "opciones": [
            {"id": "a", "texto": "el agente responsable", "correcta": True, "razon": "Sintaxis sin agente."},
            {"id": "b", "texto": "las víctimas", "correcta": False, "razon": "Sí aparecen."},
            {"id": "c", "texto": "el lugar", "correcta": False, "razon": "Puede no ser relevante."},
        ], "justificacion_obligatoria": False, "regla": "sintaxis ideológica"}}],
    788: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Citar una fuente de forma selectiva puede ser:",
        "opciones": [
            {"id": "a", "texto": "intertextualidad manipuladora", "correcta": True, "razon": "Solo lo que apoya la tesis."},
            {"id": "b", "texto": "rigor académico", "correcta": False, "razon": "Solo si es completa."},
            {"id": "c", "texto": "falacia de autoridad", "correcta": False, "razon": "No siempre."},
        ], "justificacion_obligatoria": False, "regla": "intertextualidad selectiva"}}],
    789: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Que un informe sobre economía no mencione la desigualdad es un ejemplo de:",
        "opciones": [
            {"id": "a", "texto": "silencio discursivo", "correcta": True, "razon": "Ausencia reveladora."},
            {"id": "b", "texto": "falacia", "correcta": False, "razon": "No es razonamiento."},
            {"id": "c", "texto": "latinismo", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "silencio discursivo"}}],
    790: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué hace el análisis crítico del discurso?",
        "opciones": [
            {"id": "a", "texto": "Revela ideología en léxico, sintaxis y silencios", "correcta": True, "razon": "Definición completa."},
            {"id": "b", "texto": "Solo cuenta palabras", "correcta": False, "razon": "Insuficiente."},
            {"id": "c", "texto": "Solo analiza metáforas", "correcta": False, "razon": "Incompleto."},
        ], "justificacion_obligatoria": False, "regla": "ACD completo"}}],
}
