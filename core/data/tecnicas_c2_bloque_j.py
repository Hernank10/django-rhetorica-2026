"""Bloque J del modulo C2: sintesis maestra y cierre MCER."""

TECNICAS_891_900 = [
    {"numero": 891, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "Síntesis maestra: integrar todos los registros",
     "teoria": "El texto de nivel maestría integra registro académico, literario, analítico y oral en un mismo discurso coherente, sin que ninguno chirríe.",
     "explicacion": "Ejemplo: un ensayo que cita a un filósofo (académico), describe una escena con imágenes precisas (literario), analiza la ideología de esa escena (análisis crítico) y cierra con una pregunta provocadora (oral). La maestría no consiste en usar todos los registros, sino en alternarlos con naturalidad, sin costuras visibles. El lector no debe notar el cambio de registro: debe sentir que el texto respira.",
     "regla": "síntesis = integración natural de registros | sin costuras visibles",
     "ejemplo_correcto": "«Como señala Benjamin (1936), la obra de arte pierde su aura al reproducirse; basta mirar una postal de la Gioconda colgada en una oficina para sentir esa pérdida. ¿Qué queda del original cuando cualquiera puede tenerlo en su bolsillo?».",
     "ejemplo_incorrecto": "Introducir tres párrafos académicos y de golpe uno poético sin transición. (costura visible)"},

    {"numero": 892, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "El texto total: literatura + ensayo + análisis",
     "teoria": "El texto total es aquel que combina la densidad del ensayo, la plasticidad de la literatura y el rigor del análisis. Es el género imposible: ninguno de los tres por separado.",
     "explicacion": "Referentes: 'El arco y la lira' de Octavio Paz (ensayo + poética), 'La ciudad y los perros' de Vargas Llosa (novela + análisis social), 'Los detectives salvajes' (novela + ensayo + crónica). El texto total no renuncia a nada: usa la metáfora donde ilumina, el dato donde precisa, la escena donde conmueve. Exige un lector competente en varios registros a la vez.",
     "regla": "texto total = ensayo + literatura + análisis | nada sobra, nada falta",
     "ejemplo_correcto": "«La novela de Bolaño es a la vez relato de aventuras, ensayo sobre la literatura y radiografía de una generación perdida».",
     "ejemplo_incorrecto": "Ensayo que renuncia a la imagen por miedo a la literatura. (texto parcial)"},

    {"numero": 893, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "Reescritura y autocrítica: pulir el estilo",
     "teoria": "La reescritura es el verdadero acto de escritura. El primer borrador es materia prima; el texto final nace de la revisión sistemática.",
     "explicacion": "Estrategias: leer en voz alta (detectar ritmo y muletillas), distanciarse del texto (dejar reposar días), revisar por capas (1. contenido, 2. estructura, 3. párrafo, 4. frase, 5. palabra), eliminar repeticiones, verificar transiciones. Referentes: Hemingway reescribía 39 veces el final de 'Adiós a las armas'; Borges corregía con obsesión; García Márquez reescribió 'Cien años' tres veces. La autocrítica honesta es el motor del estilo.",
     "regla": "reescritura = materia prima → revisión por capas → texto final",
     "ejemplo_correcto": "Después de tres revisiones, el ensayo pasó de 5000 a 3800 palabras: más claro, más fuerte.",
     "ejemplo_incorrecto": "Publicar el primer borrador sin revisar. (error de principiante)"},

    {"numero": 894, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "El proyecto de escritura largo",
     "teoria": "Un proyecto de escritura largo (novela, ensayo de libro, tesis, poemario) exige planificación, disciplina y tolerancia a la incertidumbre.",
     "explicacion": "Fases: 1. definición del proyecto (pregunta central, público), 2. documentación (lecturas, fuentes), 3. esquema (no rígido: mapa flexible), 4. escritura diaria (mínimo 500 palabras/día), 5. pausas programadas, 6. reescritura. Referentes: 'París era una fiesta' (Hemingway sobre su proceso), 'Mientras escribo' (Stephen King), 'El oficio de escritor' (entrevistas de Paris Review). El proyecto largo no se termina por inspiración: se termina por constancia.",
     "regla": "proyecto largo = definición + documentación + esquema + constancia + reescritura",
     "ejemplo_correcto": "Novela escrita en 18 meses: 500 palabras/día, esquema flexible, tres borradores.",
     "ejemplo_incorrecto": "Esperar la inspiración para escribir un capítulo. (no hay proyecto)"},

    {"numero": 895, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "La voz propia: encontrar el estilo",
     "teoria": "La voz propia no es un don: es el resultado de leer mucho, escribir mucho y revisar con honestidad. No se busca: se encuentra cuando se deja de buscar.",
     "explicacion": "Vías para encontrarla: 1. imitar conscientemente a los maestros (Borges, Cortázar, Woolf) para luego olvidarlos, 2. escribir sobre lo que solo tú puedes escribir (tu experiencia, tu mirada), 3. leer en voz alta para oírte, 4. no complacer al mercado, 5. aceptar los defectos propios como firma. Referentes: 'El escritor y sus fantasmas' (Sabato), 'Cartas a un joven poeta' (Rilke: 'No escriba versos de amor; huya de los temas más obvios').",
     "regla": "voz propia = leer mucho + escribir mucho + revisar honestamente | no se busca: se encuentra",
     "ejemplo_correcto": "Tras años imitando a Cortázar, el autor encontró su voz al escribir sobre su pueblo natal.",
     "ejemplo_incorrecto": "Forzar un estilo 'original' sin haber leído a los clásicos. (superficialidad)"},

    {"numero": 896, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "Del borrador al texto final",
     "teoria": "El paso del borrador al texto final exige separar la escritura (generar) de la edición (seleccionar y pulir). Son dos operaciones mentales distintas.",
     "explicacion": "Fases del borrador: 1. borrador cero (escribir sin corregir), 2. primer borrador (estructura visible), 3. segundo borrador (pulir párrafos y frases), 4. texto final (revisión palabra por palabra). Regla de oro: no corregir mientras se escribe. Hemingway: 'Escribe borracho, corrige sobrio' (metáfora). El texto final no es el borrador más largo ni más corto: es el borrador más preciso.",
     "regla": "borrador ≠ texto final | escribir sin corregir → corregir sin escribir",
     "ejemplo_correcto": "El primer borrador tenía 8000 palabras; el texto final, 4200: no se eliminó nada esencial.",
     "ejemplo_incorrecto": "Corregir cada frase mientras se escribe. (bloquea el flujo)"},

    {"numero": 897, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "La edición: revisar con distancia",
     "teoria": "La edición profesional es la última capa de la escritura: revisar el texto como si fuera de otro. La distancia emocional es la condición del rigor.",
     "explicacion": "Estrategias: 1. imprimir el texto (leer en papel revela errores que la pantalla oculta), 2. leer en voz alta, 3. pedir lectura a un lector crítico, 4. revisar por categorías (repeticiones, transiciones, muletillas, adjetivación, coordinación), 5. eliminar adverbios en -mente innecesarios, 6. verificar cada cita. Referentes: editores de oficio (Max Perkins con Fitzgerald, Carmen Balcells con García Márquez). El editor no es enemigo: es el primer lector honesto.",
     "regla": "edición = distancia + papel + lector crítico + revisión por categorías",
     "ejemplo_correcto": "Tras la lectura crítica, el editor señaló transiciones bruscas y repeticiones que el autor no veía.",
     "ejemplo_incorrecto": "Enviar el texto sin revisión externa. (errores previsibles)"},

    {"numero": 898, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "Del texto al mundo: publicar, difundir",
     "teoria": "Un texto existe cuando encuentra lectores. La publicación (editorial, revista, web, autopublicación) es el último paso del proyecto, no el primero.",
     "explicacion": "Vías: 1. editorial tradicional (prestigio, distribución, lento), 2. revista literaria (visibilidad, comunidad), 3. autopublicación (control, exige marketing), 4. blog/newsletter (audiencia propia), 5. redes (difusión, no publicación). Cada vía exige un tipo de texto y un pacto de lectura distinto. Referente: la historia de rechazos célebres ('Cien años' rechazada por varias editoriales). El rechazo no define la calidad: define el mercado en ese momento.",
     "regla": "publicar = encontrar lectores | cada vía tiene su pacto de lectura",
     "ejemplo_correcto": "La autora autopublicó y vendió 5000 copias con newsletter propio antes de firmar con editorial.",
     "ejemplo_incorrecto": "Esperar la llamada de una editorial sin enviar el manuscrito. (no hay publicación)"},

    {"numero": 899, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "Cierre MCER: del nivel maestría al dominio",
     "teoria": "C2 es el nivel de maestría, no de perfección. El dominio del español no termina: continúa con la lectura, la escritura y la vida.",
     "explicacion": "El MCER distingue C2 como 'dominio operativo efectivo' (no 'nativo'): el hablante C2 comprende con facilidad todo lo que lee o escucha, se expresa con fluidez y precisión, diferencia matices finos en textos complejos. Pero ningún hablante —tampoco el nativo— lo domina todo: la lengua es infinita. Tras C2 vienen: la lectura de los clásicos, la escritura creativa, la traducción, la docencia, la investigación. El MCER es un mapa, no un territorio.",
     "regla": "C2 = dominio operativo efectivo | el aprendizaje continúa siempre",
     "ejemplo_correcto": "Un hablante C2 lee a Borges en original, escribe ensayos con voz propia y discierne matices dialectales.",
     "ejemplo_incorrecto": "«Ya lo sé todo del español». (ningún hablante lo sabe todo, ni el nativo)"},

    {"numero": 900, "bloque": "J", "nivel": "maestria", "modulo": "c2",
     "titulo": "Repaso maestro + cierre C2 + MCER completo",
     "teoria": "Repaso del bloque J y cierre de todo el MCER (A1-C2). Has completado el viaje del español como lengua extranjera: del nivel inicial al de maestría.",
     "explicacion": "Has recorrido: A1 (100) → A2 (100) → B1 (110) → B2 (100) → C1 (100) → C2 (100) = 610 técnicas en los 6 niveles MCER + 200 técnicas base (gramática y generativa) = 810 técnicas en total. Ahora puedes leer, escribir, hablar y escuchar en español con dominio operativo efectivo. El viaje no termina: comienza la etapa de la práctica vital, la lectura por placer, la escritura por necesidad, la conversación sin miedo.",
     "regla": "MCER completo = A1 + A2 + B1 + B2 + C1 + C2 | 610 técnicas + 200 base = 810",
     "ejemplo_correcto": "«He completado el MCER. Ahora empieza lo de verdad: la lengua en la vida».",
     "ejemplo_incorrecto": "«Ya soy C2, no necesito seguir aprendiendo». (contradice el propio MCER)"},
]

EJERCICIOS_891_900 = {
    891: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La síntesis maestra de registros se reconoce por:",
        "opciones": [
            {"id": "a", "texto": "integración natural, sin costuras visibles", "correcta": True, "razon": "Maestría estilística."},
            {"id": "b", "texto": "usar todos los registros a la vez", "correcta": False, "razon": "Sobrecarga."},
            {"id": "c", "texto": "elegir solo el registro académico", "correcta": False, "razon": "Incompleto."},
        ], "justificacion_obligatoria": False, "regla": "síntesis = integración natural"}}],
    892: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El 'texto total' combina:",
        "opciones": [
            {"id": "a", "texto": "ensayo + literatura + análisis", "correcta": True, "razon": "Los tres a la vez."},
            {"id": "b", "texto": "solo ensayo", "correcta": False, "razon": "Incompleto."},
            {"id": "c", "texto": "solo literatura", "correcta": False, "razon": "Incompleto."},
        ], "justificacion_obligatoria": False, "regla": "texto total = tres géneros"}}],
    893: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La reescritura se organiza por:",
        "opciones": [
            {"id": "a", "texto": "capas: contenido → estructura → párrafo → frase → palabra", "correcta": True, "razon": "Revisión sistemática."},
            {"id": "b", "texto": "un solo repaso rápido", "correcta": False, "razon": "Insuficiente."},
            {"id": "c", "texto": "solo ortografía", "correcta": False, "razon": "Superficial."},
        ], "justificacion_obligatoria": False, "regla": "reescritura por capas"}}],
    894: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Un proyecto de escritura largo se termina por:",
        "opciones": [
            {"id": "a", "texto": "constancia (escritura diaria)", "correcta": True, "razon": "Disciplina > inspiración."},
            {"id": "b", "texto": "inspiración divina", "correcta": False, "razon": "Falso."},
            {"id": "c", "texto": "esperar el momento perfecto", "correcta": False, "razon": "Nunca llega."},
        ], "justificacion_obligatoria": False, "regla": "constancia"}}],
    895: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La voz propia se encuentra:",
        "opciones": [
            {"id": "a", "texto": "leyendo mucho + escribiendo mucho + revisando honestamente", "correcta": True, "razon": "Proceso largo."},
            {"id": "b", "texto": "forzando un estilo original", "correcta": False, "razon": "Superficialidad."},
            {"id": "c", "texto": "copiando a un autor de moda", "correcta": False, "razon": "Sin voz propia."},
        ], "justificacion_obligatoria": False, "regla": "voz propia"}}],
    896: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué regla de oro separa escritura de edición?",
        "opciones": [
            {"id": "a", "texto": "escribir sin corregir → corregir sin escribir", "correcta": True, "razon": "Dos operaciones mentales."},
            {"id": "b", "texto": "corregir mientras se escribe", "correcta": False, "razon": "Bloquea el flujo."},
            {"id": "c", "texto": "escribir y publicar directo", "correcta": False, "razon": "Error de principiante."},
        ], "justificacion_obligatoria": False, "regla": "escritura ≠ edición"}}],
    897: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La edición profesional requiere:",
        "opciones": [
            {"id": "a", "texto": "distancia + papel + lector crítico", "correcta": True, "razon": "Rigor."},
            {"id": "b", "texto": "revisar solo la ortografía", "correcta": False, "razon": "Superficial."},
            {"id": "c", "texto": "no mostrar el texto a nadie", "correcta": False, "razon": "Sin distancia externa."},
        ], "justificacion_obligatoria": False, "regla": "edición con distancia"}}],
    898: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La publicación es:",
        "opciones": [
            {"id": "a", "texto": "encontrar lectores", "correcta": True, "razon": "El texto existe cuando se lee."},
            {"id": "b", "texto": "escribir más", "correcta": False, "razon": "No es publicar."},
            {"id": "c", "texto": "olvidar el texto", "correcta": False, "razon": "Contrario."},
        ], "justificacion_obligatoria": False, "regla": "publicar = lectores"}}],
    899: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "El MCER define C2 como:",
        "opciones": [
            {"id": "a", "texto": "dominio operativo efectivo (no perfección)", "correcta": True, "razon": "Matiz importante."},
            {"id": "b", "texto": "perfección absoluta", "correcta": False, "razon": "Nadie lo alcanza."},
            {"id": "c", "texto": "nivel nativo", "correcta": False, "razon": "El MCER no lo define así."},
        ], "justificacion_obligatoria": False, "regla": "C2 = dominio operativo"}}],
    900: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Has completado el MCER?",
        "opciones": [
            {"id": "a", "texto": "Sí: A1+A2+B1+B2+C1+C2 = 810 técnicas. Comienza lo de verdad.", "correcta": True, "razon": "¡Enhorabuena!"},
            {"id": "b", "texto": "No, me faltan niveles.", "correcta": False, "razon": "Ya están los 6."},
            {"id": "c", "texto": "El MCER no termina nunca.", "correcta": False, "razon": "El programa sí termina: 810 técnicas completas."},
        ], "justificacion_obligatoria": False, "regla": "MCER completo"}}],
}
