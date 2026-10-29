"""Bloque I del modulo A2: pronombres personales."""

TECNICAS_581_590 = [
    {"numero": 581, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Pronombres de objeto directo (lo, la, los, las)",
     "teoria": "Los pronombres de OD sustituyen al objeto directo: lo (masc sing), la (fem sing), los (masc plur), las (fem plur).",
     "explicacion": "Ej: 'Compré el libro' → 'Lo compré'. 'Compré la casa' → 'La compré'. 'Compré los libros' → 'Los compré'. 'Compré las casas' → 'Las compré'. El pronombre va antes del verbo conjugado.",
     "regla": "OD: lo / la / los / las (antes del verbo)",
     "ejemplo_correcto": "¿El libro? Sí, lo compré ayer.",
     "ejemplo_incorrecto": "¿El libro? Sí, compré lo ayer. (pronombre antes del verbo)"},

    {"numero": 582, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Pronombres de objeto indirecto (me, te, le, nos, os, les)",
     "teoria": "Los pronombres de OI sustituyen al objeto indirecto: me, te, le (sing), nos, os, les (plur).",
     "explicacion": "Ej: 'Di el libro a Juan' → 'Le di el libro' (le = a Juan). 'Escribí a mis padres' → 'Les escribí'. 'Me dio el regalo' (me = a mí). El OI responde a '¿a quién?'.",
     "regla": "OI: me / te / le / nos / os / les",
     "ejemplo_correcto": "Le di el regalo a mi madre.",
     "ejemplo_incorrecto": "Di el regalo a ella → 'Le di el regalo' (le, no 'ella')"},

    {"numero": 583, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "OD + OI combinados: me lo, te la, se lo",
     "teoria": "Cuando hay dos pronombres, el OI va primero y el OD después: me lo, te la, se los, nos las.",
     "explicacion": "Ej: 'Me dio el libro' → 'Me lo dio'. 'Te compré flores' → 'Te las compré'. Cuando el OI es 'le/les' y hay OD, cambia a 'se': 'Le di el libro a Juan' → 'Se lo di' (nunca 'le lo di').",
     "regla": "OI + OD: me lo / te la / se los / nos las | le/les → se cuando hay OD",
     "ejemplo_correcto": "¿El libro a Juan? Se lo di ayer.",
     "ejemplo_incorrecto": "¿El libro a Juan? Le lo di ayer. (le+lo → se lo)"},

    {"numero": 584, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Regla de 'se' por 'le/les' (le lo → se lo)",
     "teoria": "Cuando el OI 'le' o 'les' precede a un OD 'lo/la/los/las', se transforma en 'se'.",
     "explicacion": "Ej: 'Le di el libro' → 'Se lo di' (no 'le lo di'). 'Les mandé las cartas' → 'Se las mandé'. Es la regla más importante de pronombres combinados. Solo se aplica con le/les, no con me/te/nos/os.",
     "regla": "le/les + lo/la/los/las → se + lo/la/los/las",
     "ejemplo_correcto": "Se lo dije a María (decir algo a alguien).",
     "ejemplo_incorrecto": "Le lo dije a María. (le+lo → se lo)"},

    {"numero": 585, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Posición de los pronombres: antes del verbo",
     "teoria": "Con verbo conjugado, los pronombres van antes: lo vi, me lo dio, te la compré.",
     "explicacion": "Con infinitivo, gerundio o imperativo afirmativo, van después y pegados: 'verlo', 'dándomelo', 'dímelo'. Con futuro y condicional, van antes: 'lo veré', 'me lo daría'.",
     "regla": "conjugado: antes (lo vi) | infinitivo/gerundio/imperativo+: después pegado (verlo, dándolo, dímelo)",
     "ejemplo_correcto": "Quiero verlo. Me lo dio. Dímelo.",
     "ejemplo_incorrecto": "Quiero lo ver. Me lo dio bien, pero 'quiero verlo'."},

    {"numero": 586, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Redundancia con OI: 'Le dije a Juan'",
     "teoria": "El OI puede aparecer duplicado: el pronombre 'le/les' + el sintagma 'a + persona'. Es lo normal.",
     "explicacion": "Ej: 'Le dije a Juan que viniera' (le + a Juan). 'Les compré flores a mis padres'. La duplicación es correcta y frecuente en español. Con OD también: 'Lo vi a Juan' (menos frecuente pero válido).",
     "regla": "le/les + a + persona (redundancia normal)",
     "ejemplo_correcto": "Le dije a Juan que viniera.",
     "ejemplo_incorrecto": "Dije a Juan que viniera (sin 'le', menos natural)"},

    {"numero": 587, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Se impersonal (se vende, se habla)",
     "teoria": "El 'se' impersonal acompaña a un verbo en 3ª persona y expresa acciones sin sujeto concreto: 'Se habla español', 'Se vende pan'.",
     "explicacion": "Se usa en carteles, anuncios y descripciones generales. 'Se vende casa' (alguien la vende). 'Se habla inglés en esta tienda'. 'Aquí se trabaja mucho'. El verbo va siempre en 3ª persona.",
     "regla": "se + verbo 3ª persona (sing o plur): se vende, se venden, se habla, se hablan",
     "ejemplo_correcto": "Se venden libros antiguos en esta tienda.",
     "ejemplo_incorrecto": "Se vendo libros antiguos. (se impersonal: 3ª persona 'venden')"},

    {"numero": 588, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Se pasivo reflejo: 'Se construyó el puente'",
     "teoria": "El 'se' pasivo reflejo expresa una acción pasiva sin agente explícito, con verbo en 3ª persona que concuerda con el sujeto.",
     "explicacion": "Ej: 'Se construyó el puente en 1990' (= el puente fue construido). 'Se vendieron las casas'. Concuerda con el sujeto: 'Se construyó' (sing) / 'Se construyeron' (plur). Se diferencia del impersonal en que aquí el sujeto es claro.",
     "regla": "se + verbo 3ª persona concordando con el sujeto: se construyó / se construyeron",
     "ejemplo_correcto": "Se construyeron dos puentes nuevos.",
     "ejemplo_incorrecto": "Se construyó dos puentes. (concordancia plural: construyeron)"},

    {"numero": 589, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Preposiciones por vs para",
     "teoria": "Por: causa, medio, tiempo aproximado, lugar aproximado. Para: finalidad, destino, plazo, destinatario.",
     "explicacion": "Ej: 'Estudio por aprender' (causa) vs 'Estudio para aprobar' (finalidad). 'Voy por Madrid' (lugar aprox) vs 'Voy para Madrid' (destino). 'Un regalo para ti' (destinatario). 'Por la mañana' (tiempo aprox). Es una de las preposiciones más difíciles de A2.",
     "regla": "por: causa/medio/aprox | para: finalidad/destino/destinatario",
     "ejemplo_correcto": "Estudio por aprender, no para aprobar.",
     "ejemplo_incorrecto": "Estudio para aprender (posible pero 'por' es más preciso para causa)"},

    {"numero": 590, "bloque": "I", "nivel": "intermedio", "modulo": "a2",
     "titulo": "Repaso integrador I",
     "teoria": "Repaso: OD (lo/la/los/las), OI (me/te/le/nos/os/les), combinados (me lo, te la, se lo), 'se' impersonal y pasivo, posición, por/para.",
     "explicacion": "Ejemplo integrador: 'Se venden flores. ¿A ti te las dieron? Sí, me las dieron ayer por la mañana en la tienda para mi cumpleaños'.",
     "regla": "OD + OI: me lo / te la / se lo | se impersonal: se vende | se pasivo: se construyó",
     "ejemplo_correcto": "¿Los libros? Se los di a Juan por la mañana para que los leyera.",
     "ejemplo_incorrecto": "¿Los libros? Le los di a Juan. (le+los → se los)"},
]

EJERCICIOS_581_590 = {
    581: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿El libro? Sí, ___ compré ayer. (comprar, yo)",
        "opciones": [
            {"id": "a", "texto": "lo", "correcta": True, "razon": "OD masc sing: lo."},
            {"id": "b", "texto": "la", "correcta": False, "razon": "Femenino."},
            {"id": "c", "texto": "le", "correcta": False, "razon": "OI, no OD."},
        ], "justificacion_obligatoria": False, "regla": "OD el libro -> lo"}}],
    582: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "___ di el regalo a mi madre. (dar, yo)",
        "opciones": [
            {"id": "a", "texto": "Le", "correcta": True, "razon": "OI a mi madre: le."},
            {"id": "b", "texto": "La", "correcta": False, "razon": "OD femenino."},
            {"id": "c", "texto": "Lo", "correcta": False, "razon": "OD masculino."},
        ], "justificacion_obligatoria": False, "regla": "OI -> le"}}],
    583: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿El libro a Juan? ___ di ayer. (dar)",
        "opciones": [
            {"id": "a", "texto": "Se lo", "correcta": True, "razon": "le+lo -> se lo."},
            {"id": "b", "texto": "Le lo", "correcta": False, "razon": "le+lo no es válido."},
            {"id": "c", "texto": "Lo le", "correcta": False, "razon": "Orden incorrecto."},
        ], "justificacion_obligatoria": False, "regla": "le+lo -> se lo"}}],
    584: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "___ dije a María (decir algo a alguien).",
        "opciones": [
            {"id": "a", "texto": "Se lo", "correcta": True, "razon": "le+lo -> se lo."},
            {"id": "b", "texto": "Le lo", "correcta": False, "razon": "No válido."},
            {"id": "c", "texto": "Lo le", "correcta": False, "razon": "Orden incorrecto."},
        ], "justificacion_obligatoria": False, "regla": "le+lo -> se lo"}}],
    585: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es correcta? (infinitivo)",
        "opciones": [
            {"id": "a", "texto": "Quiero verlo.", "correcta": True, "razon": "Infinitivo + pronombre pegado."},
            {"id": "b", "texto": "Quiero lo ver.", "correcta": False, "razon": "Con infinitivo va pegado."},
            {"id": "c", "texto": "Lo quiero ver.", "correcta": False, "razon": "Posible pero 'verlo' es lo natural con querer."},
        ], "justificacion_obligatoria": False, "regla": "infinitivo + pronombre pegado"}}],
    586: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "___ dije a Juan que viniera.",
        "opciones": [
            {"id": "a", "texto": "Le", "correcta": True, "razon": "Redundancia le + a Juan."},
            {"id": "b", "texto": "Lo", "correcta": False, "razon": "OD, no OI."},
            {"id": "c", "texto": "La", "correcta": False, "razon": "OD femenino."},
        ], "justificacion_obligatoria": False, "regla": "le + a Juan (redundancia)"}}],
    587: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "___ libros antiguos en esta tienda. (vender)",
        "opciones": [
            {"id": "a", "texto": "Se venden", "correcta": True, "razon": "Se impersonal + concordancia plural."},
            {"id": "b", "texto": "Se vende", "correcta": False, "razon": "Concordancia singular incorrecta."},
            {"id": "c", "texto": "Se vendo", "correcta": False, "razon": "1ª persona, no impersonal."},
        ], "justificacion_obligatoria": False, "regla": "se + 3ª persona"}}],
    588: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "___ dos puentes nuevos. (construir)",
        "opciones": [
            {"id": "a", "texto": "Se construyeron", "correcta": True, "razon": "Se pasivo + concordancia plural."},
            {"id": "b", "texto": "Se construyó", "correcta": False, "razon": "Concordancia singular incorrecta."},
            {"id": "c", "texto": "Se construí", "correcta": False, "razon": "1ª persona."},
        ], "justificacion_obligatoria": False, "regla": "se pasivo reflejo"}}],
    589: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Estudio ___ aprender, no ___ aprobar. (por / para)",
        "opciones": [
            {"id": "a", "texto": "por ... para", "correcta": True, "razon": "Causa (por) + finalidad (para)."},
            {"id": "b", "texto": "para ... por", "correcta": False, "razon": "Invertido."},
            {"id": "c", "texto": "por ... por", "correcta": False, "razon": "Falta finalidad (para)."},
        ], "justificacion_obligatoria": False, "regla": "por (causa) vs para (finalidad)"}}],
    590: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Los libros? ___ di a Juan ___ la mañana. (dar, yo)",
        "opciones": [
            {"id": "a", "texto": "Se los ... por", "correcta": True, "razon": "le+los -> se los | por la mañana."},
            {"id": "b", "texto": "Le los ... para", "correcta": False, "razon": "le+los no válido, para la mañana no natural."},
            {"id": "c", "texto": "Los le ... por", "correcta": False, "razon": "Orden incorrecto."},
        ], "justificacion_obligatoria": False, "regla": "se los + por la mañana"}}],
}
