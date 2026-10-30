"""Bloque E del modulo B2: estilo indirecto avanzado."""

TECNICAS_641_650 = [
    {"numero": 641, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Estilo directo vs indirecto: repaso",
     "teoria": "Directo: reproduce las palabras exactas ('Voy al cine'). Indirecto: introduce un verbo de habla ('Dijo que iba al cine'). Cambian pronombres, tiempos y marcadores.",
     "explicacion": "Ej: 'Vengo mañana' (directo) → 'Dijo que vendría al día siguiente' (indirecto). Los tres cambios obligatorios: pronombres, tiempos y marcadores temporales/espaciales.",
     "regla": "directo: comillas, palabras literales | indirecto: verbo de habla + que + cambios",
     "ejemplo_correcto": "Dijo que vendría al día siguiente.",
     "ejemplo_incorrecto": "Dijo que vendrá mañana. (si el momento ya pasó: vendría / al día siguiente)"},

    {"numero": 642, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Cambios de tiempo verbal en pasado",
     "teoria": "Si el verbo introductor está en pasado, los tiempos retroceden: presente → imperfecto; pretérito → pluscuamperfecto; futuro/condicional → condicional.",
     "explicacion": "Presente → imperfecto: 'Estoy cansado' → 'Dijo que estaba cansado'. Indefinido → pluscuamperfecto: 'Fui al cine' → 'Dijo que había ido al cine'. Futuro → condicional: 'Vendré' → 'Dijo que vendría'.",
     "regla": "presente→imperfecto | indefinido→pluscuamperfecto | futuro→condicional",
     "ejemplo_correcto": "Dijo que había terminado el trabajo.",
     "ejemplo_incorrecto": "Dijo que terminó el trabajo. (retroceso: había terminado)"},

    {"numero": 643, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Cambios de pronombres y posesivos",
     "teoria": "Los pronombres personales y posesivos cambian según el punto de vista del hablante original y del que reproduce.",
     "explicacion": "Ej: 'Yo tengo mi libro' (dice Juan) → 'Juan dijo que él tenía su libro'. 'Mi madre está enferma' (dice Ana) → 'Ana dijo que su madre estaba enferma'. El posesivo concuerda con el nuevo sujeto.",
     "regla": "yo→él/ella | mío→suyo | tú→él/ella (o se mantiene si es el interlocutor)",
     "ejemplo_correcto": "María dijo que su hermano estaba de viaje.",
     "ejemplo_incorrecto": "María dijo que mi hermano estaba de viaje. (posesivo: su, no mi)"},

    {"numero": 644, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Cambios de marcadores temporales y espaciales",
     "teoria": "Los marcadores temporales y espaciales se ajustan al nuevo punto de referencia: hoy → ese día; mañana → al día siguiente; aquí → allí.",
     "explicacion": "Ej: 'Hoy hace frío' (dice Juan) → 'Dijo que ese día hacía frío'. 'Vendré mañana' → 'Dijo que vendría al día siguiente'. 'Estoy aquí' → 'Dijo que estaba allí'. Son cambios sistemáticos.",
     "regla": "hoy→ese día | mañana→al día siguiente | ayer→el día anterior | aquí→allí | ahora→entonces",
     "ejemplo_correcto": "Dijo que vendría al día siguiente.",
     "ejemplo_incorrecto": "Dijo que vendría mañana. (si es pasado: al día siguiente)"},

    {"numero": 645, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Preguntas indirectas: sí/no y wh-",
     "teoria": "Pregunta directa sí/no → 'si + verbo'. Pregunta wh- → mismo interrogativo + verbo. Sin signos de interrogación.",
     "explicacion": "Sí/no: '¿Vienes?' → 'Preguntó si venía'. Wh-: '¿Dónde vives?' → 'Preguntó dónde vivía'. '¿Cuándo llegaste?' → 'Preguntó cuándo había llegado'. Sin '¿?' al final.",
     "regla": "sí/no: preguntar si + verbo | wh-: preguntar + interrogativo + verbo",
     "ejemplo_correcto": "Me preguntó si había terminado el trabajo.",
     "ejemplo_incorrecto": "Me preguntó que si había terminado. (nunca 'que si'; solo 'si')"},

    {"numero": 646, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Imperativo en estilo indirecto",
     "teoria": "El imperativo cambia a subjuntivo o a perífrasis de obligación: 'Hazlo' → 'Dijo que lo hiciera' o 'Me pidió que lo hiciera'.",
     "explicacion": "Ej: 'Ven aquí' (directo) → 'Me pidió que fuera allí' / 'Me dijo que fuera'. 'No lo hagas' → 'Me dijo que no lo hiciera'. Depende del verbo introductor (pedir, ordenar, decir, aconsejar).",
     "regla": "imperativo → subjuntivo (con cambio de tiempo si introductor es pasado)",
     "ejemplo_correcto": "Me pidió que cerrara la puerta.",
     "ejemplo_incorrecto": "Me pidió que cierra la puerta. (pasado + subjuntivo: cerrara)"},

    {"numero": 647, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Discurso indirecto libre (narrativa)",
     "teoria": "El discurso indirecto libre mezcla la voz del narrador y del personaje sin marcas explícitas (sin 'dijo que'). Muy usado en literatura.",
     "explicacion": "Ej: 'Marta miró el reloj. Iba a llegar tarde. ¿Por qué siempre le pasaba lo mismo?'. No hay 'pensó que' o 'dijo que', pero el lector entiende que son los pensamientos de Marta. Combina tercera persona con subjetividad del personaje.",
     "regla": "sin verbo introductor + tercera persona + subjetividad del personaje",
     "ejemplo_correcto": "Juan miró la carta. No podía ser verdad. ¿Quién se la habría enviado?",
     "ejemplo_incorrecto": "Juan dijo que no podía ser verdad y preguntó quién se la habría enviado. (eso es indirecto normal, no libre)"},

    {"numero": 648, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Verbos introductorios: decir, preguntar, exclamar, añadir",
     "teoria": "El verbo introductor matiza el tono: decir (neutro), preguntar (interrogación), exclamar (emoción), añadir (información extra), explicar (clarificación), gritar (volumen).",
     "explicacion": "Ej: '¡Qué bonito!' (directo) → 'Exclamó que era muy bonito' (exclamar). 'Además, no tengo tiempo' → 'Añadió que además no tenía tiempo'. El verbo introductor cambia el matiz.",
     "regla": "decir / preguntar / exclamar / añadir / explicar / gritar + que",
     "ejemplo_correcto": "Exclamó que era una idea brillante.",
     "ejemplo_incorrecto": "Exclamó que es una idea brillante. (pasado + imperfecto: era)"},

    {"numero": 649, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Estilo indirecto con verbos de mandato",
     "teoria": "Verbos como pedir, ordenar, aconsejar, prohibir, sugerir rigen subjuntivo en la subordinada.",
     "explicacion": "Ej: 'Cierra la puerta' (directo) → 'Me pidió que cerrara la puerta'. 'No fumes aquí' → 'Me prohibió que fumara allí'. 'Deberías descansar' → 'Me aconsejó que descansara'. Todos con subjuntivo.",
     "regla": "pedir/ordenar/aconsejar/prohibir + que + subjuntivo",
     "ejemplo_correcto": "Me aconsejó que descansara más.",
     "ejemplo_incorrecto": "Me aconsejó que descanso más. (subjuntivo: descansara)"},

    {"numero": 650, "bloque": "E", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Repaso integrador E (estilo indirecto)",
     "teoria": "Repaso: cambios de tiempo, pronombres, marcadores, preguntas indirectas, imperativo, discurso libre, verbos introductorios.",
     "explicacion": "Ejemplo integrador: 'Dijo: «Hoy voy a venir con mi hermano. ¿Puedes preparar la cena?». → Dijo que ese día iba a ir con su hermano y me preguntó si podía preparar la cena'.",
     "regla": "retroceso temporal + pronombres + marcadores + subjuntivo en mandatos",
     "ejemplo_correcto": "Dijo que ese día iba a venir con su hermano y me preguntó si podía preparar la cena.",
     "ejemplo_incorrecto": "Dijo que hoy viene con mi hermano y preguntó si puedo preparar la cena. (sin retroceso)"},
]

EJERCICIOS_641_650 = {
    641: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Vengo mañana» → Dijo que ___ al día siguiente. (venir, él)",
        "opciones": [
            {"id": "a", "texto": "vendría", "correcta": True, "razon": "Futuro → condicional."},
            {"id": "b", "texto": "vendrá", "correcta": False, "razon": "Sin retroceso."},
            {"id": "c", "texto": "viene", "correcta": False, "razon": "Presente."},
        ], "justificacion_obligatoria": False, "regla": "futuro → condicional"}}],
    642: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Estoy cansado» → Dijo que ___ cansado. (estar, él)",
        "opciones": [
            {"id": "a", "texto": "estaba", "correcta": True, "razon": "Presente → imperfecto."},
            {"id": "b", "texto": "está", "correcta": False, "razon": "Sin retroceso."},
            {"id": "c", "texto": "estuvo", "correcta": False, "razon": "Indefinido."},
        ], "justificacion_obligatoria": False, "regla": "presente → imperfecto"}}],
    643: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Mi madre está enferma» (dice Ana) → Ana dijo que ___ madre estaba enferma.",
        "opciones": [
            {"id": "a", "texto": "su", "correcta": True, "razon": "Posesivo ajustado al nuevo sujeto."},
            {"id": "b", "texto": "mi", "correcta": False, "razon": "Sin ajuste (mal)."},
            {"id": "c", "texto": "tu", "correcta": False, "razon": "Sin sentido."},
        ], "justificacion_obligatoria": False, "regla": "posesivo: mi → su"}}],
    644: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Hoy hace frío» → Dijo que ___ hacía frío.",
        "opciones": [
            {"id": "a", "texto": "ese día", "correcta": True, "razon": "hoy → ese día."},
            {"id": "b", "texto": "hoy", "correcta": False, "razon": "Sin ajuste."},
            {"id": "c", "texto": "mañana", "correcta": False, "razon": "Mal."},
        ], "justificacion_obligatoria": False, "regla": "hoy → ese día"}}],
    645: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«¿Vienes?» → Preguntó ___ venía.",
        "opciones": [
            {"id": "a", "texto": "si", "correcta": True, "razon": "Pregunta sí/no: si."},
            {"id": "b", "texto": "que", "correcta": False, "razon": "Mal (que si es incorrecto)."},
            {"id": "c", "texto": "cuando", "correcta": False, "razon": "Cambia el sentido."},
        ], "justificacion_obligatoria": False, "regla": "sí/no: si + verbo"}}],
    646: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Ven aquí» → Me pidió que ___ allí. (ir, yo)",
        "opciones": [
            {"id": "a", "texto": "fuera", "correcta": True, "razon": "Imperativo → subjuntivo imperfecto."},
            {"id": "b", "texto": "voy", "correcta": False, "razon": "Presente."},
            {"id": "c", "texto": "iría", "correcta": False, "razon": "Condicional."},
        ], "justificacion_obligatoria": False, "regla": "imperativo → subjuntivo"}}],
    647: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es discurso indirecto libre?",
        "opciones": [
            {"id": "a", "texto": "Juan miró la carta. No podía ser verdad. ¿Quién se la habría enviado?", "correcta": True, "razon": "Sin verbo introductor, tercera persona, subjetividad."},
            {"id": "b", "texto": "Juan dijo que no podía ser verdad y preguntó quién se la había enviado.", "correcta": False, "razon": "Indirecto normal."},
            {"id": "c", "texto": "Juan: «No puede ser verdad. ¿Quién me la habrá enviado?».", "correcta": False, "razon": "Directo."},
        ], "justificacion_obligatoria": False, "regla": "discurso indirecto libre"}}],
    648: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«¡Qué bonito!» → ___ que era muy bonito.",
        "opciones": [
            {"id": "a", "texto": "Exclamó", "correcta": True, "razon": "Verbo introductor de emoción."},
            {"id": "b", "texto": "Dijo", "correcta": False, "razon": "Posible pero menos expresivo."},
            {"id": "c", "texto": "Preguntó", "correcta": False, "razon": "No es pregunta."},
        ], "justificacion_obligatoria": False, "regla": "exclamar"}}],
    649: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Deberías descansar» → Me aconsejó que ___ más. (descansar, yo)",
        "opciones": [
            {"id": "a", "texto": "descansara", "correcta": True, "razon": "Aconsejar + subjuntivo imperfecto."},
            {"id": "b", "texto": "descanso", "correcta": False, "razon": "Indicativo."},
            {"id": "c", "texto": "descansaría", "correcta": False, "razon": "Condicional."},
        ], "justificacion_obligatoria": False, "regla": "aconsejar + subjuntivo"}}],
    650: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es correcta?",
        "opciones": [
            {"id": "a", "texto": "Dijo que ese día iba a venir con su hermano y me preguntó si podía preparar la cena.", "correcta": True, "razon": "Retroceso + pronombres + preguntas indirectas."},
            {"id": "b", "texto": "Dijo que hoy viene con mi hermano y preguntó si puedo preparar la cena.", "correcta": False, "razon": "Sin retroceso."},
            {"id": "c", "texto": "Dijo que hoy vendría con su hermano y preguntó que si podía preparar la cena.", "correcta": False, "razon": "que si (mal)."},
        ], "justificacion_obligatoria": False, "regla": "todos los cambios aplicados"}}],
}
