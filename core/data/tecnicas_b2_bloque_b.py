"""Bloque B del modulo B2: condicionales 2/3 y mixtos."""

TECNICAS_611_620 = [
    {"numero": 611, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicional tipo 2: si + imperfecto de subjuntivo + condicional simple",
     "teoria": "Hipótesis irreal en el presente/futuro: si + imperfecto subjuntivo, condicional simple. Expresa algo que no es real o es improbable.",
     "explicacion": "Ej: 'Si tuviera dinero, viajaría' (no tengo dinero ahora). 'Si estudiaras más, aprobarías'. La prótasis (si...) lleva subjuntivo imperfecto; la apódosis (resultado) lleva condicional simple. NUNCA 'si + condicional'.",
     "regla": "si + imperfecto subjuntivo + condicional simple",
     "ejemplo_correcto": "Si viviera cerca, iría a verte todos los días.",
     "ejemplo_incorrecto": "Si viviría cerca, iría a verte. (nunca si + condicional)"},

    {"numero": 612, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicional tipo 3: si + pluscuamperfecto subjuntivo + condicional compuesto",
     "teoria": "Hipótesis irreal en el pasado: si + hubiera/hubiese + participio, habría + participio. Expresa algo que no ocurrió y su consecuencia también irreal.",
     "explicacion": "Ej: 'Si hubiera estudiado, habría aprobado' (no estudié, no aprobé). 'Si hubiéramos salido antes, no habríamos perdido el tren'. Todo el evento está en el pasado y ninguno de los dos ocurrió.",
     "regla": "si + hubiera + participio + habría + participio",
     "ejemplo_correcto": "Si hubiera sabido que venías, habría preparado algo.",
     "ejemplo_incorrecto": "Si habría sabido que venías, habría preparado algo. (nunca si + habría)"},

    {"numero": 613, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicional mixto (pasado + presente): si + plusc. + condicional simple",
     "teoria": "Hipótesis mixta: la condición es pasada (no ocurrió) pero la consecuencia es presente (real ahora).",
     "explicacion": "Ej: 'Si hubiera estudiado medicina, ahora sería médico' (no estudié medicina → ahora no soy médico). La prótasis es pasada, la apódosis es presente. Combina tipo 3 + tipo 2.",
     "regla": "si + hubiera + participio + condicional simple (presente)",
     "ejemplo_correcto": "Si hubiera aceptado el trabajo, ahora viviría en Madrid.",
     "ejemplo_incorrecto": "Si aceptara el trabajo, ahora viviría en Madrid. (si es pasado irreal, debe ser hubiera aceptado)"},

    {"numero": 614, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicional mixto (presente + pasado): si + imp. subj. + condicional compuesto",
     "teoria": "Hipótesis mixta inversa: la condición es presente (estado actual) pero la consecuencia es pasada.",
     "explicacion": "Ej: 'Si fuera más responsable, no habría perdido el trabajo' (no soy responsable ahora → perdí el trabajo en el pasado). Menos frecuente pero válido. La clave es la coherencia temporal.",
     "regla": "si + imperfecto subjuntivo + condicional compuesto (pasado)",
     "ejemplo_correcto": "Si no fuera tan despistado, no habría olvidado la cita.",
     "ejemplo_incorrecto": "Si no era tan despistado, no habría olvidado la cita. (estado actual = subjuntivo)"},

    {"numero": 615, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicionales con 'como si' + pluscuamperfecto subjuntivo",
     "teoria": "'Como si' puede llevar imperfecto de subjuntivo (presente) o pluscuamperfecto de subjuntivo (pasado), según el momento de la comparación hipotética.",
     "explicacion": "Presente: 'Habla como si fuera el jefe'. Pasado: 'Habló como si hubiera sido el jefe'. La elección depende de si la comparación irreal se refiere al presente o al pasado.",
     "regla": "como si + imperfecto subjuntivo (presente) | como si + plusc. subjuntivo (pasado)",
     "ejemplo_correcto": "Me miró como si hubiera visto un fantasma.",
     "ejemplo_incorrecto": "Me miró como si viera un fantasma. (si es pasado anterior, hubiera visto)"},

    {"numero": 616, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicionales con 'a no ser que' / 'a menos que'",
     "teoria": "Conectores condicionales negativos que siempre llevan subjuntivo: a no ser que, a menos que, salvo que, excepto que.",
     "explicacion": "Ej: 'Iremos al parque a menos que llueva'. 'A no ser que me avises, no iré'. Son condiciones que se excluyen. Pueden combinarse con cualquier tiempo principal, pero el subjuntivo en la subordinada es obligatorio.",
     "regla": "a menos que / a no ser que / salvo que + subjuntivo (presente o imperfecto)",
     "ejemplo_correcto": "A menos que llueva, saldremos a caminar.",
     "ejemplo_incorrecto": "A menos que llueve, saldremos. (conectores condicionales negativos = subjuntivo)"},

    {"numero": 617, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicionales concesivas: 'aunque' + subjuntivo/indicativo",
     "teoria": "'Aunque' puede ir con subjuntivo (hipótesis) o indicativo (hecho real). El matiz cambia.",
     "explicacion": "Hipótesis: 'Aunque llueva, saldremos' (no sé si lloverá). Real: 'Aunque llueve, salimos' (está lloviendo). Con subjuntivo imperfecto, hipótesis pasada o irreal: 'Aunque lloviera, saldríamos'.",
     "regla": "aunque + indicativo (real) | aunque + subjuntivo (hipótesis)",
     "ejemplo_correcto": "Aunque me lo pidas mil veces, no lo haré.",
     "ejemplo_incorrecto": "Aunque me lo pides mil veces, no lo haré. (si es hipótesis, subjuntivo)"},

    {"numero": 618, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicionales con 'de + infinitivo' (coloquial)",
     "teoria": "Estructura coloquial equivalente a 'si + imperfecto subjuntivo': de + infinitivo, condicional.",
     "explicacion": "Ej: 'De haberlo sabido, habría venido' (= si lo hubiera sabido). 'De tener tiempo, iría' (= si tuviera tiempo). Más formal o literario. No admite sujeto explícito ('de yo tener' NO).",
     "regla": "de + infinitivo compuesto + condicional compuesto | de + infinitivo + condicional simple",
     "ejemplo_correcto": "De haberlo sabido antes, habría actuado diferente.",
     "ejemplo_incorrecto": "De saberlo antes, habría actuado. (posible, pero 'haberlo sabido' es más claro)"},

    {"numero": 619, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Condicionales de cortesía avanzada",
     "teoria": "El condicional simple expresa cortesía en peticiones formales. El condicional compuesto expresa arrepentimiento o reproche suave.",
     "explicacion": "Cortesía: '¿Podrías ayudarme?', 'Me gustaría reservar'. Arrepentimiento: 'Habría preferido no enterarme'. Reproche: 'Deberías habérmelo dicho' (con deber en condicional compuesto).",
     "regla": "condicional simple (cortesía) | condicional compuesto (arrepentimiento/reproche)",
     "ejemplo_correcto": "Deberías haberme avisado antes.",
     "ejemplo_incorrecto": "Deberías haberme avisado antes, si podrías. (frase mal construida)"},

    {"numero": 620, "bloque": "B", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Repaso integrador B (condicionales)",
     "teoria": "Repaso: tipos 2, 3, mixtos, como si, a menos que, aunque, de + infinitivo, cortesía avanzada.",
     "explicacion": "Ejemplo integrador: 'Si hubiera estudiado más, ahora tendría un mejor trabajo. Aunque me lo pidieras, no cambiaría de opinión. De haberlo sabido, habría actuado antes'.",
     "regla": "tipo 2: si + imp. subj + condicional | tipo 3: si + plusc. subj + condicional compuesto | mixtos",
     "ejemplo_correcto": "Si hubiera aceptado, ahora estaría en Madrid. Aunque me lo pidieras, no cambiaría.",
     "ejemplo_incorrecto": "Si habría aceptado, ahora estaría en Madrid. (nunca si + habría)"},
]

EJERCICIOS_611_620 = {
    611: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Si ___ cerca, iría a verte todos los días. (vivir, yo)",
        "opciones": [
            {"id": "a", "texto": "viviera", "correcta": True, "razon": "Tipo 2: si + imperfecto subjuntivo."},
            {"id": "b", "texto": "viviría", "correcta": False, "razon": "Condicional en prótasis (nunca)."},
            {"id": "c", "texto": "vivo", "correcta": False, "razon": "Indicativo presente."},
        ], "justificacion_obligatoria": False, "regla": "si + imperfecto subjuntivo"}}],
    612: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Si ___ que venías, habría preparado algo. (saber, yo)",
        "opciones": [
            {"id": "a", "texto": "hubiera sabido", "correcta": True, "razon": "Tipo 3: si + plusc. subjuntivo."},
            {"id": "b", "texto": "habría sabido", "correcta": False, "razon": "Condicional compuesto en prótasis (nunca)."},
            {"id": "c", "texto": "supiera", "correcta": False, "razon": "Imperfecto subjuntivo (no para tipo 3)."},
        ], "justificacion_obligatoria": False, "regla": "si + hubiera + part."}}],
    613: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Si ___ aceptado el trabajo, ahora viviría en Madrid. (aceptar, yo)",
        "opciones": [
            {"id": "a", "texto": "hubiera", "correcta": True, "razon": "Mixto: pasado + consecuencia presente."},
            {"id": "b", "texto": "habría", "correcta": False, "razon": "Nunca si + habría."},
            {"id": "c", "texto": "aceptara", "correcta": False, "razon": "Presente hipotético, no pasado."},
        ], "justificacion_obligatoria": False, "regla": "si + hubiera + part., condicional simple"}}],
    614: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Si no ___ tan despistado, no habría olvidado la cita. (ser, yo)",
        "opciones": [
            {"id": "a", "texto": "fuera", "correcta": True, "razon": "Mixto: presente + pasado."},
            {"id": "b", "texto": "hubiera sido", "correcta": False, "razon": "Pasado puro, no mixto."},
            {"id": "c", "texto": "era", "correcta": False, "razon": "Indicativo."},
        ], "justificacion_obligatoria": False, "regla": "si + imperfecto subjuntivo + condicional compuesto"}}],
    615: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Me miró como si ___ un fantasma. (ver, él)",
        "opciones": [
            {"id": "a", "texto": "hubiera visto", "correcta": True, "razon": "Comparación irreal pasada: plusc. subjuntivo."},
            {"id": "b", "texto": "viera", "correcta": False, "razon": "Presente hipotético, no pasado."},
            {"id": "c", "texto": "había visto", "correcta": False, "razon": "Indicativo (no como si)."},
        ], "justificacion_obligatoria": False, "regla": "como si + plusc. subjuntivo (pasado)"}}],
    616: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "A menos que ___, saldremos a caminar. (llover)",
        "opciones": [
            {"id": "a", "texto": "llueva", "correcta": True, "razon": "Conector condicional negativo = subjuntivo."},
            {"id": "b", "texto": "llueve", "correcta": False, "razon": "Indicativo."},
            {"id": "c", "texto": "lloverá", "correcta": False, "razon": "Futuro."},
        ], "justificacion_obligatoria": False, "regla": "a menos que + subjuntivo"}}],
    617: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Aunque me lo ___ mil veces, no lo haré. (pedir, tú)",
        "opciones": [
            {"id": "a", "texto": "pidas", "correcta": True, "razon": "Aunque + subjuntivo (hipótesis)."},
            {"id": "b", "texto": "pides", "correcta": False, "razon": "Indicativo (hecho real)."},
            {"id": "c", "texto": "pedirás", "correcta": False, "razon": "Futuro."},
        ], "justificacion_obligatoria": False, "regla": "aunque + subjuntivo (hipótesis)"}}],
    618: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "De ___ sabido antes, habría actuado diferente. (haber, yo)",
        "opciones": [
            {"id": "a", "texto": "haberlo", "correcta": True, "razon": "de + infinitivo compuesto + condicional compuesto."},
            {"id": "b", "texto": "habría", "correcta": False, "razon": "No 'de habría'."},
            {"id": "c", "texto": "hubiera", "correcta": False, "razon": "No 'de hubiera sabido antes'."},
        ], "justificacion_obligatoria": False, "regla": "de + inf. compuesto + condicional compuesto"}}],
    619: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "___ haberme avisado antes. (deber, tú)",
        "opciones": [
            {"id": "a", "texto": "Deberías", "correcta": True, "razon": "Condicional de reproche."},
            {"id": "b", "texto": "Debes", "correcta": False, "razon": "Presente, no reproche."},
            {"id": "c", "texto": "Deberás", "correcta": False, "razon": "Futuro."},
        ], "justificacion_obligatoria": False, "regla": "deberías + inf. compuesto"}}],
    620: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es correcta? (mixto)",
        "opciones": [
            {"id": "a", "texto": "Si hubiera aceptado, ahora estaría en Madrid.", "correcta": True, "razon": "Mixto: pasado irreal + presente real."},
            {"id": "b", "texto": "Si habría aceptado, ahora estaría en Madrid.", "correcta": False, "razon": "Nunca si + habría."},
            {"id": "c", "texto": "Si aceptara, ahora estaría en Madrid.", "correcta": False, "razon": "Presente hipotético, no pasado."},
        ], "justificacion_obligatoria": False, "regla": "condicional mixto"}}],
}
