"""Bloque C del modulo B2: secuencia de tiempos con subjuntivo."""

TECNICAS_621_630 = [
    {"numero": 621, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Subjuntivo presente tras verbo principal presente",
     "teoria": "Si el verbo principal (querer, esperar, dudar) está en presente/futuro/imperativo, la subordinada va en subjuntivo presente.",
     "explicacion": "Ej: 'Quiero que vengas' (quiero-presente → vengas-presente subjuntivo). 'Espero que llegues temprano'. 'Dudo que lo sepas'. La concordancia de tiempos es obligatoria.",
     "regla": "verbo principal presente/futuro + subjuntivo presente en subordinada",
     "ejemplo_correcto": "Espero que te guste la sorpresa.",
     "ejemplo_incorrecto": "Espero que te gustara la sorpresa. (aunque posible si te refieres al pasado, si es futuro → presente)"},

    {"numero": 622, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Subjuntivo imperfecto tras verbo principal pasado/condicional",
     "teoria": "Si el verbo principal está en pasado o condicional, la subordinada va en imperfecto de subjuntivo.",
     "explicacion": "Ej: 'Quería que vinieras' (quería-pasado → vinieras-imperfecto). 'Esperaba que llegara temprano'. 'Dudaba que lo supiera'. Es el error más frecuente en estudiantes: 'quería que vengas' (incorrecto).",
     "regla": "verbo principal pasado/condicional + subjuntivo imperfecto",
     "ejemplo_correcto": "Esperaba que te gustara la sorpresa.",
     "ejemplo_incorrecto": "Esperaba que te guste la sorpresa. (pasado + subjuntivo presente)"},

    {"numero": 623, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Subjuntivo perfecto (haya + participio) en presente",
     "teoria": "El pretérito perfecto de subjuntivo (haya hablado/comido/vivido) expresa una acción pasada ya completada en una subordinada con verbo principal presente.",
     "explicacion": "Ej: 'Espero que hayas terminado' (aún no sé, pero deberías haber terminado). 'Dudo que haya llegado todavía'. Forma: haya/hayas/haya/hayamos/hayáis/hayan + participio.",
     "regla": "verbo principal presente + haya + participio (acción pasada)",
     "ejemplo_correcto": "Espero que hayas estudiado para el examen.",
     "ejemplo_incorrecto": "Espero que estudies para el examen (hoy ya pasó). (acción pasada: hayas estudiado)"},

    {"numero": 624, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Subjuntivo pluscuamperfecto (hubiera + participio) en pasado",
     "teoria": "El pluscuamperfecto de subjuntivo (hubiera/hubiese + participio) expresa una acción pasada ya completada en subordinada con verbo principal pasado.",
     "explicacion": "Ej: 'Esperaba que hubieras terminado' (en el pasado, esperaba que ya estuviera hecho). 'Dudaba que hubiera llegado'. Forma: hubiera/hubiese + participio.",
     "regla": "verbo principal pasado + hubiera + participio (acción anterior)",
     "ejemplo_correcto": "Esperaba que hubieras estudiado para el examen.",
     "ejemplo_incorrecto": "Esperaba que hayas estudiado. (pasado + haya → hubieras)"},

    {"numero": 625, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Correlación en 'ojalá': presente vs imperfecto vs perfecto",
     "teoria": "'Ojalá' + presente de subjuntivo (deseo realizable), imperfecto (deseo improbable), perfecto (deseo sobre pasado reciente), pluscuamperfecto (deseo sobre pasado irreal).",
     "explicacion": "Ej: 'Ojalá llueva mañana' (realizable). 'Ojalá lloviera ahora' (improbable). 'Ojalá haya llegado ya' (no sé, espero que sí). 'Ojalá hubiera estudiado más' (ya no puedo cambiar).",
     "regla": "ojalá + pres. subj (realizable) | imp. subj (improbable) | haya + part (esperanza pasada) | hubiera + part (arrepentimiento)",
     "ejemplo_correcto": "Ojalá hubiera comprado ese billete cuando era barato.",
     "ejemplo_incorrecto": "Ojalá compraba ese billete. (ojalá nunca con indicativo)"},

    {"numero": 626, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Correlación en 'como si': imperfecto vs pluscuamperfecto",
     "teoria": "'Como si' + imperfecto de subjuntivo si la comparación es presente/pasada simultánea; pluscuamperfecto si es anterior.",
     "explicacion": "Presente: 'Habla como si fuera el jefe' (él no es jefe ahora). Pasado: 'Habló como si hubiera sido el jefe' (habla ahora sobre el pasado). Anterior: 'Me miró como si le hubiera visto antes'.",
     "regla": "como si + imp. subj (simultáneo) | como si + plusc. subj (anterior)",
     "ejemplo_correcto": "Me habló como si no me conociera de nada.",
     "ejemplo_incorrecto": "Me habló como si no me conocía. (como si + subjuntivo)"},

    {"numero": 627, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Subjuntivo en relativas: 'busco a alguien que...'",
     "teoria": "Las oraciones relativas llevan subjuntivo cuando el antecedente es inespecífico o inexistente. Indicativo cuando el antecedente es conocido.",
     "explicacion": "Subjuntivo: 'Busco a alguien que hable francés' (no sé si existe). Indicativo: 'Busco a Juan, que habla francés' (existe). 'Necesito un piso que tenga terraza' (no sé si lo hay) vs 'He visto el piso que tiene terraza'.",
     "regla": "antecedente desconocido/inexistente + subjuntivo | conocido + indicativo",
     "ejemplo_correcto": "Busco un libro que explique bien la gramática.",
     "ejemplo_incorrecto": "Busco un libro que explica bien la gramática. (si no lo conozco, subjuntivo)"},

    {"numero": 628, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Subjuntivo en temporales futuras: 'cuando llegues'",
     "teoria": "Las oraciones temporales que se refieren al futuro llevan subjuntivo: cuando, mientras, hasta que, antes de que, en cuanto, después de que.",
     "explicacion": "Ej: 'Cuando llegues, llámame'. 'Mientras estés aquí, no fumes'. 'Hasta que termines, no saldrás'. Regla mnemotécnica: si la acción no ha ocurrido (futuro), subjuntivo. Si ya ocurrió o es habitual: indicativo.",
     "regla": "cuando / mientras / hasta que / antes de que + subjuntivo (futuro)",
     "ejemplo_correcto": "En cuanto termines el trabajo, avísame.",
     "ejemplo_incorrecto": "En cuanto terminarás el trabajo, avísame. (cuando + futuro = subjuntivo)"},

    {"numero": 629, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Indicativo vs subjuntivo: 'pienso que' vs 'no pienso que'",
     "teoria": "Verbos de opinión (pensar, creer, parecer) en afirmativo llevan indicativo. En negativo o interrogativo, subjuntivo.",
     "explicacion": "Afirmativo: 'Pienso que es buena idea' (indicativo). Negativo: 'No pienso que sea buena idea' (subjuntivo). Interrogativo: '¿Crees que sea / es buena idea?' (ambas válidas, subjuntivo más dubitativo).",
     "regla": "creo/pienso + indicativo | no creo/no pienso + subjuntivo",
     "ejemplo_correcto": "No creo que sea tan difícil.",
     "ejemplo_incorrecto": "No creo que es tan difícil. (negación = subjuntivo)"},

    {"numero": 630, "bloque": "C", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Repaso integrador C (secuencia de tiempos)",
     "teoria": "Repaso: presente→pres. subj, pasado→imp. subj, presente→haya + part, pasado→hubiera + part, ojalá, como si, relativas, temporales, opinión.",
     "explicacion": "Ejemplo integrador: 'Espero que hayas terminado. Quería que vinieras. Ojalá hubiera sabido. Busco a alguien que me ayude. Cuando llegues, avísame'.",
     "regla": "regla de correlación temporal según el verbo principal",
     "ejemplo_correcto": "Espero que hayas terminado. Cuando llegues, llámame.",
     "ejemplo_incorrecto": "Esperaba que hayas terminado. (pasado + haya → hubieras)"},
]

EJERCICIOS_621_630 = {
    621: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Espero que te ___ la sorpresa. (gustar)",
        "opciones": [
            {"id": "a", "texto": "guste", "correcta": True, "razon": "Presente + subj. presente."},
            {"id": "b", "texto": "gustara", "correcta": False, "razon": "Imperfecto (incoherente con presente)."},
            {"id": "c", "texto": "gusta", "correcta": False, "razon": "Indicativo."},
        ], "justificacion_obligatoria": False, "regla": "presente + pres. subjuntivo"}}],
    622: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Esperaba que te ___ la sorpresa. (gustar)",
        "opciones": [
            {"id": "a", "texto": "gustara", "correcta": True, "razon": "Pasado + imperfecto subj."},
            {"id": "b", "texto": "guste", "correcta": False, "razon": "Presente (incoherente con pasado)."},
            {"id": "c", "texto": "gustaba", "correcta": False, "razon": "Indicativo."},
        ], "justificacion_obligatoria": False, "regla": "pasado + imperfecto subjuntivo"}}],
    623: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Espero que ___ para el examen. (estudiar, tú)",
        "opciones": [
            {"id": "a", "texto": "hayas estudiado", "correcta": True, "razon": "Perfecto subj.: acción pasada en subordinada presente."},
            {"id": "b", "texto": "estudies", "correcta": False, "razon": "Presente (no acción pasada)."},
            {"id": "c", "texto": "hubieras estudiado", "correcta": False, "razon": "Pluscuamperfecto (incoherente con presente)."},
        ], "justificacion_obligatoria": False, "regla": "presente + haya + participio"}}],
    624: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Esperaba que ___ para el examen. (estudiar, tú)",
        "opciones": [
            {"id": "a", "texto": "hubieras estudiado", "correcta": True, "razon": "Pluscuamperfecto subj.: pasado anterior."},
            {"id": "b", "texto": "hayas estudiado", "correcta": False, "razon": "Perfecto (incoherente con pasado)."},
            {"id": "c", "texto": "estudiaras", "correcta": False, "razon": "Imperfecto (simultáneo, no anterior)."},
        ], "justificacion_obligatoria": False, "regla": "pasado + hubiera + participio"}}],
    625: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Ojalá ___ ese billete cuando era barato. (comprar, yo)",
        "opciones": [
            {"id": "a", "texto": "hubiera comprado", "correcta": True, "razon": "Arrepentimiento pasado = pluscuamperfecto."},
            {"id": "b", "texto": "comprara", "correcta": False, "razon": "Imperfecto (no para arrepentimiento de pasado cerrado)."},
            {"id": "c", "texto": "compre", "correcta": False, "razon": "Presente (deseo realizable, no pasado)."},
        ], "justificacion_obligatoria": False, "regla": "ojalá + hubiera + part (pasado irreal)"}}],
    626: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Me habló como si no me ___ de nada. (conocer, él)",
        "opciones": [
            {"id": "a", "texto": "conociera", "correcta": True, "razon": "Comparación simultánea al pasado: imp. subj."},
            {"id": "b", "texto": "conocía", "correcta": False, "razon": "Indicativo (no como si)."},
            {"id": "c", "texto": "conozca", "correcta": False, "razon": "Presente subj."},
        ], "justificacion_obligatoria": False, "regla": "como si + imperfecto subj."}}],
    627: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Busco un libro que ___ bien la gramática. (explicar, él)",
        "opciones": [
            {"id": "a", "texto": "explique", "correcta": True, "razon": "Antecedente inespecífico = subjuntivo."},
            {"id": "b", "texto": "explica", "correcta": False, "razon": "Indicativo (solo si existe y lo conozco)."},
            {"id": "c", "texto": "explicará", "correcta": False, "razon": "Futuro."},
        ], "justificacion_obligatoria": False, "regla": "relativa inespecífica + subjuntivo"}}],
    628: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "En cuanto ___ el trabajo, avísame. (terminar, tú)",
        "opciones": [
            {"id": "a", "texto": "termines", "correcta": True, "razon": "Temporal futura = subjuntivo."},
            {"id": "b", "texto": "terminarás", "correcta": False, "razon": "Futuro (nunca después de cuando)."},
            {"id": "c", "texto": "terminas", "correcta": False, "razon": "Indicativo (habitual, no futuro puntual)."},
        ], "justificacion_obligatoria": False, "regla": "en cuanto + subjuntivo (futuro)"}}],
    629: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "No creo que ___ tan difícil. (ser)",
        "opciones": [
            {"id": "a", "texto": "sea", "correcta": True, "razon": "Negación de opinión = subjuntivo."},
            {"id": "b", "texto": "es", "correcta": False, "razon": "Indicativo (solo en afirmativo)."},
            {"id": "c", "texto": "será", "correcta": False, "razon": "Futuro."},
        ], "justificacion_obligatoria": False, "regla": "no creo que + subjuntivo"}}],
    630: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es correcta?",
        "opciones": [
            {"id": "a", "texto": "Espero que hayas terminado. Cuando llegues, llámame.", "correcta": True, "razon": "Secuencia de tiempos correcta."},
            {"id": "b", "texto": "Esperaba que hayas terminado. Cuando llegarás, llámame.", "correcta": False, "razon": "Pasado + haya (mal) + cuando + futuro (mal)."},
            {"id": "c", "texto": "Espero que termines ya. Cuando llegues, llámame.", "correcta": False, "razon": "'Ya' implica pasado completado → hayas terminado."},
        ], "justificacion_obligatoria": False, "regla": "secuencia temporal"}}],
}
