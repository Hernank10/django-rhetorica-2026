"""Bloque E del modulo C2: argumentación compleja."""

TECNICAS_841_850 = [
    {"numero": 841, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Silogismo: estructura y validez",
     "teoria": "El silogismo es un razonamiento deductivo con dos premisas y una conclusión. Su validez depende de la forma, no del contenido.",
     "explicacion": "Estructura: premisa mayor (universal) + premisa menor (particular) + conclusión. Ejemplo: 'Todos los humanos son mortales; Sócrates es humano; luego Sócrates es mortal'. Válido ≠ verdadero: 'Todos los gatos vuelan; Micifuz es gato; luego Micifuz vuela' es válido formalmente (aunque falso materialmente). Falacias silogísticas: término medio no distribuido, cuatro términos, premisas negativas.",
     "regla": "silogismo = premisa mayor + premisa menor + conclusión | válido ≠ verdadero",
     "ejemplo_correcto": "Todos los seres vivos mueren; las plantas son seres vivos; luego las plantas mueren.",
     "ejemplo_incorrecto": "Todos los pájaros vuelan; los pingüinos son pájaros; luego los pingüinos vuelan. (premisa mayor falsa)"},

    {"numero": 842, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Falacias de segundo orden: meta-falacias",
     "teoria": "Las falacias de segundo orden no atacan el argumento, sino la forma de argumentar o la legitimidad del oponente para argumentar.",
     "explicacion": "Tipos: 'argumentum ad hominem' (atacar a la persona), 'argumentum ad verecundiam' mal usado (autoridad ilegítima), 'argumentum ad populum' (mayoría), 'argumentum ad baculum' (amenaza), 'argumentum ad misericordiam' (lástima), 'tu quoque' (tú también). Se llaman de segundo orden porque desplazan el foco del contenido al contexto. Detectar la falacia es el primer paso de la refutación.",
     "regla": "falacia 2º orden = ataque al contexto/persona, no al argumento",
     "ejemplo_correcto": "«Su propuesta es falsa porque usted no es experto». Es un ad hominem.",
     "ejemplo_incorrecto": "Refutar el dato con otro dato. (eso no es falacia, es argumentación)"},

    {"numero": 843, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Dialéctica hegeliana: tesis, antítesis, síntesis",
     "teoria": "La dialéctica hegeliana avanza por contradicción: una tesis genera su antítesis, y de su tensión surge una síntesis que las supera.",
     "explicacion": "Ejemplo: tesis ('el conocimiento proviene de la experiencia') → antítesis ('hay ideas innatas') → síntesis ('hay estructuras a priori que organizan la experiencia'). La síntesis no es un punto medio: es una superación (Aufhebung) que conserva lo verdadero de ambas y las eleva. Aplicable a debates, ensayos y resolución de conflictos.",
     "regla": "dialéctica = tesis + antítesis + síntesis (superación, no promedio)",
     "ejemplo_correcto": "Tesis: la IA crea empleo. Antítesis: la IA destruye empleo. Síntesis: transforma el empleo (nuevos perfiles, pérdida de otros).",
     "ejemplo_incorrecto": "Tesis + antítesis = quedarse con la mitad de cada una. (no es síntesis)"},

    {"numero": 844, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Retórica clásica: ethos, pathos, logos",
     "teoria": "Aristóteles distingue tres modos de persuasión: ethos (autoridad moral del orador), pathos (emoción del auditorio) y logos (argumento racional).",
     "explicacion": "Ethos: 'como médico con 30 años de experiencia...'. Pathos: apelar a la empatía ('imaginemos a una familia que...'). Logos: datos, silogismos, estadísticas. La persuasión eficaz combina los tres. La publicidad abusa del pathos; la ciencia del logos; el liderazgo del ethos. El análisis crítico evalúa el equilibrio.",
     "regla": "persuasión = ethos (autoridad) + pathos (emoción) + logos (razón)",
     "ejemplo_correcto": "El discurso combinó datos (logos) con la autoridad del orador (ethos) y una historia conmovedora (pathos).",
     "ejemplo_incorrecto": "Solo datos, sin emoción ni autoridad. (persuasión débil)"},

    {"numero": 845, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Argumentación multimodal: imagen + palabra",
     "teoria": "La argumentación multimodal integra palabra, imagen, sonido y gesto. En publicidad, política y redes, la imagen argumenta tanto como el texto.",
     "explicacion": "Ejemplo: un cartel contra el cambio climático con un oso polar en un témpano diminuto. La imagen argumenta (pathos) y el texto cierra el logos ('el planeta se derrite'). Recursos: metáfora visual, contraste, testimonio gráfico. En análisis crítico, hay que leer ambos códigos: qué dice el texto y qué dice la imagen.",
     "regla": "argumentación multimodal = palabra + imagen + sonido + gesto (todos argumentan)",
     "ejemplo_correcto": "El cartel usa la imagen para conmover y el eslogan para argumentar.",
     "ejemplo_incorrecto": "Solo leer el texto e ignorar la imagen. (análisis incompleto)"},

    {"numero": 846, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Reducción al absurdo (reductio ad absurdum)",
     "teoria": "La reducción al absurdo refuta una tesis mostrando que sus consecuencias lógicas son absurdas, contradictorias o inaceptables.",
     "explicacion": "Estructura: se asume la tesis contraria, se deduce una contradicción y se concluye que la tesis es falsa. Ejemplo: 'Supongamos que todo vale. Entonces también vale asesinar. Nadie acepta eso. Por tanto, no todo vale'. Es una de las formas más elegantes de refutación. Requiere que la deducción sea rigurosa.",
     "regla": "reducción al absurdo = asumir tesis + deducir contradicción + negar tesis",
     "ejemplo_correcto": "Si todos pudieran decidir qué es verdad, la verdad no existiría: absurdo.",
     "ejemplo_incorrecto": "«Eso es absurdo porque a mí me lo parece». (no es reducción)"},

    {"numero": 847, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Argumento de autoridad vs ad hominem",
     "teoria": "El argumento de autoridad (ad verecundiam) apela a una fuente legítima; el ad hominem ataca a la persona. Distinguirlos es esencial.",
     "explicacion": "Autoridad legítima: 'según el IPCC, el clima se calienta' (fuente experta en el tema). Autoridad ilegítima: 'según mi vecino, las vacunas son malas' (sin competencia). Ad hominem: 'no le hagas caso porque es joven'. En el análisis crítico: verificar (1) competencia del experto, (2) consenso del campo, (3) ausencia de conflicto de interés.",
     "regla": "autoridad = fuente competente | ad hominem = ataque a la persona",
     "ejemplo_correcto": "«Según la OMS, la vacuna es segura» es autoridad legítima.",
     "ejemplo_incorrecto": "«No le hagas caso porque es joven» es ad hominem."},

    {"numero": 848, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Contraargumentación estratégica: concesión y refutación",
     "teoria": "La contraargumentación eficaz concede lo verdadero del adversario antes de refutar lo falso. Genera credibilidad y desarma la defensa.",
     "explicacion": "Estructura: 'Es cierto que X... Sin embargo, Y...'. Ejemplo: 'Es cierto que la medida es costosa. No obstante, los estudios de costo-beneficio muestran que se amortiza en cinco años'. La concesión no es debilidad: es estrategia. Permite que el adversario baje la guardia y aumenta la fuerza de la refutación.",
     "regla": "contraargumentación = concesión + refutación (credibilidad + eficacia)",
     "ejemplo_correcto": "Acepto que el plan tiene riesgos; sin embargo, los beneficios superan esos riesgos.",
     "ejemplo_incorrecto": "«Todo lo que dices es falso». (sin concesión, pierde credibilidad)"},

    {"numero": 849, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Síntesis dialéctica: integrar sin promediar",
     "teoria": "La síntesis dialéctica integra lo verdadero de tesis y antítesis en un nivel superior. No es un promedio: es una superación cualitativa.",
     "explicacion": "Ejemplo: tesis ('la libertad es absoluta') + antítesis ('todo está determinado') → síntesis ('la libertad es una conquista parcial en condiciones determinadas'). Otra: tesis ('la tecnología nos libera') + antítesis ('la tecnología nos esclaviza') → síntesis ('la tecnología amplifica lo que ya somos'). La síntesis exige un tercer concepto que reorganice el debate.",
     "regla": "síntesis = superación cualitativa (no promedio de tesis y antítesis)",
     "ejemplo_correcto": "La síntesis supera el debate libertad/determinismo con el concepto de autonomía situada.",
     "ejemplo_incorrecto": "Mitad y mitad: «somos medio libres, medio determinados». (promedio, no síntesis)"},

    {"numero": 850, "bloque": "E", "nivel": "maestria", "modulo": "c2",
     "titulo": "Repaso integrador E (argumentación compleja)",
     "teoria": "Repaso: silogismo, falacias de segundo orden, dialéctica hegeliana, ethos/pathos/logos, argumentación multimodal, reducción al absurdo, autoridad vs ad hominem, contraargumentación, síntesis.",
     "explicacion": "Ejemplo integrador: 'El ensayo construye un silogismo (logos) con autoridad experta (ethos) y un ejemplo conmovedor (pathos). Anticipa objeciones (contraargumentación), refuta una por reducción al absurdo y cierra con una síntesis dialéctica que integra las críticas. La imagen del cartel refuerza visualmente la tesis (multimodal)'. Cada recurso tiene su función.",
     "regla": "argumentación compleja = silogismo + ethos/pathos/logos + contraargumentación + síntesis",
     "ejemplo_correcto": "El ensayo combina logos, ethos y pathos, refuta por absurdo y cierra con síntesis.",
     "ejemplo_incorrecto": "Solo opinión sin estructura. (no es argumentación compleja)"},
]

EJERCICIOS_841_850 = {
    841: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué hace válido a un silogismo?",
        "opciones": [
            {"id": "a", "texto": "su forma lógica", "correcta": True, "razon": "Validez formal ≠ verdad material."},
            {"id": "b", "texto": "la verdad de sus premisas", "correcta": False, "razon": "Eso es verdad material."},
            {"id": "c", "texto": "la intención del autor", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "validez = forma"}}],
    842: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Su propuesta es mala porque usted no es experto» es una falacia:",
        "opciones": [
            {"id": "a", "texto": "ad hominem", "correcta": True, "razon": "Ataca a la persona."},
            {"id": "b", "texto": "ad populum", "correcta": False, "razon": "No apela a mayoría."},
            {"id": "c", "texto": "ad baculum", "correcta": False, "razon": "No amenaza."},
        ], "justificacion_obligatoria": False, "regla": "ad hominem"}}],
    843: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "La síntesis hegeliana es:",
        "opciones": [
            {"id": "a", "texto": "una superación cualitativa", "correcta": True, "razon": "Aufhebung, no promedio."},
            {"id": "b", "texto": "el promedio de tesis y antítesis", "correcta": False, "razon": "Falso."},
            {"id": "c", "texto": "la elección de la tesis", "correcta": False, "razon": "No es dialéctica."},
        ], "justificacion_obligatoria": False, "regla": "síntesis = superación"}}],
    844: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Apelar a la experiencia del orador es:",
        "opciones": [
            {"id": "a", "texto": "ethos", "correcta": True, "razon": "Autoridad moral."},
            {"id": "b", "texto": "pathos", "correcta": False, "razon": "Emoción."},
            {"id": "c", "texto": "logos", "correcta": False, "razon": "Razón."},
        ], "justificacion_obligatoria": False, "regla": "ethos = autoridad"}}],
    845: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Un cartel con oso polar y eslogan climático es argumentación:",
        "opciones": [
            {"id": "a", "texto": "multimodal", "correcta": True, "razon": "Imagen + texto argumentan."},
            {"id": "b", "texto": "solo textual", "correcta": False, "razon": "Ignora la imagen."},
            {"id": "c", "texto": "solo visual", "correcta": False, "razon": "Ignora el texto."},
        ], "justificacion_obligatoria": False, "regla": "multimodal"}}],
    846: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Si todo vale, entonces vale asesinar; eso es inaceptable, luego no todo vale» es:",
        "opciones": [
            {"id": "a", "texto": "reducción al absurdo", "correcta": True, "razon": "Deducción de contradicción."},
            {"id": "b", "texto": "falacia ad hominem", "correcta": False, "razon": "No."},
            {"id": "c", "texto": "argumento de autoridad", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "reducción al absurdo"}}],
    847: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Según el IPCC, el clima se calienta» es:",
        "opciones": [
            {"id": "a", "texto": "argumento de autoridad legítima", "correcta": True, "razon": "Fuente competente."},
            {"id": "b", "texto": "falacia ad hominem", "correcta": False, "razon": "No."},
            {"id": "c", "texto": "falacia ad populum", "correcta": False, "razon": "No."},
        ], "justificacion_obligatoria": False, "regla": "autoridad legítima"}}],
    848: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Acepto que el plan tiene riesgos; sin embargo, los beneficios los superan» es:",
        "opciones": [
            {"id": "a", "texto": "contraargumentación con concesión", "correcta": True, "razon": "Concede + refuta."},
            {"id": "b", "texto": "falacia", "correcta": False, "razon": "Es argumentación válida."},
            {"id": "c", "texto": "ad hominem", "correcta": False, "razon": "No ataca persona."},
        ], "justificacion_obligatoria": False, "regla": "concesión + refutación"}}],
    849: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué es una síntesis dialéctica?",
        "opciones": [
            {"id": "a", "texto": "superación cualitativa de tesis y antítesis", "correcta": True, "razon": "No es promedio."},
            {"id": "b", "texto": "un promedio entre ambas", "correcta": False, "razon": "Falso."},
            {"id": "c", "texto": "elegir la tesis inicial", "correcta": False, "razon": "No es dialéctica."},
        ], "justificacion_obligatoria": False, "regla": "síntesis = superación"}}],
    850: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál combina argumentación compleja?",
        "opciones": [
            {"id": "a", "texto": "El ensayo usa logos, ethos, pathos, refuta por absurdo y cierra con síntesis.", "correcta": True, "razon": "Todos los recursos."},
            {"id": "b", "texto": "Solo da una opinión personal.", "correcta": False, "razon": "Insuficiente."},
            {"id": "c", "texto": "Repite la misma idea tres veces.", "correcta": False, "razon": "No es argumentación."},
        ], "justificacion_obligatoria": False, "regla": "repaso E"}}],
}
