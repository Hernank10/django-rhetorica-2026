"""Data del modulo B2: Lengua Castellana B2 (100 técnicas, 10 bloques A-J)."""

TECNICAS = [
    {"numero": 601, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Formación del imperfecto de subjuntivo (-ra / -se)",
     "teoria": "El imperfecto de subjuntivo se forma a partir de la 3ª persona plural del pretérito indefinido: se quita -ron y se añade -ra/-se. hablar → hablaron → hablara/hablase.",
     "explicacion": "Dos formas equivalentes: -ra (hablara, comiera, viviera) y -se (hablase, comiese, viviese). En España se usan ambas; en Hispanoamérica domina -ra. No cambian el significado.",
     "regla": "3ª plur indefinido - ron + -ra/-se: hablaron → hablara/hablase",
     "ejemplo_correcto": "Si hablara/hablase más despacio, te entendería.",
     "ejemplo_incorrecto": "Si hablaba más despacio, te entendería. (imperfecto de indicativo no forma el condicional tipo 2)"},

    {"numero": 602, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Imperfecto de subjuntivo irregular (fuera, tuviera, hiciera…)",
     "teoria": "Los verbos irregulares en pretérito indefinido mantienen la misma raíz irregular en imperfecto de subjuntivo: ser/ir → fuera, tener → tuviera, hacer → hiciera, decir → dijera, poder → pudiera, querer → quisiera, venir → viniera, poner → pusiera, traer → trajera.",
     "explicacion": "Regla mnemotécnica: la raíz es la misma del indefinido irregular. tuve → tuviera, hice → hiciera, dije → dijera. Los compuestos siguen el patrón (proponer → propusiera).",
     "regla": "tuve→tuviera/tuviese | hice→hiciera/hiciese | dije→dijera/dijese | puse→pusiera/pusiese",
     "ejemplo_correcto": "Quisiera que vinieras a la fiesta.",
     "ejemplo_incorrecto": "Quisiera que vienieras a la fiesta. (raíz vin-, no vien-)"},

    {"numero": 603, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Correlación temporal: pasado + imperfecto de subjuntivo",
     "teoria": "Cuando el verbo principal está en pasado o condicional, la subordinada que expresa deseo, duda, emoción o valoración va en imperfecto de subjuntivo.",
     "explicacion": "Ej: 'Quería que vinieras' (quería → pasado + vinieras). 'Me gustaría que estudiaras más' (gustaría → condicional + estudiaras). La regla de correlación es obligatoria en español formal.",
     "regla": "verbo principal en pasado/condicional + subjuntivo imperfecto en la subordinada",
     "ejemplo_correcto": "Esperaba que llegaras antes de las 8.",
     "ejemplo_incorrecto": "Esperaba que llegues antes de las 8. (pasado + subjuntivo presente es incoherente)"},

    {"numero": 604, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Deseos pasados: quería que + imperfecto de subjuntivo",
     "teoria": "Para expresar un deseo referido al pasado, se usa querer en imperfecto/indefinido + que + imperfecto de subjuntivo.",
     "explicacion": "Ej: 'Quería que vinieras' = yo quería (en el pasado) que tú vinieras. 'Quise que me lo dijeras' = en un momento concreto del pasado quise. La estructura es la misma; el matiz cambia con el tiempo de querer.",
     "regla": "quería/quería que + imperfecto de subjuntivo (deseo pasado)",
     "ejemplo_correcto": "Quería que me llamaras cuando llegaras.",
     "ejemplo_incorrecto": "Quería que me llamas cuando llegas. (pasado + subjuntivo imperfecto)"},

    {"numero": 605, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Hipótesis irreal: como si + imperfecto de subjuntivo",
     "teoria": "'Como si' introduce una comparación hipotética irreal; siempre va con imperfecto de subjuntivo cuando se refiere al presente/pasado simultáneo.",
     "explicacion": "Ej: 'Habla como si fuera el jefe' (no lo es). 'Me miró como si no me conociera' (sí me conocía). 'Como si' + imperfecto = comparación irreal. Si la acción es pasada anterior, se usa pluscuamperfecto de subjuntivo ('como si hubiera visto').",
     "regla": "como si + imperfecto de subjuntivo (irreal presente/pasado)",
     "ejemplo_correcto": "Gasta dinero como si fuera millonario.",
     "ejemplo_incorrecto": "Gasta dinero como si es millonario. (como si = subjuntivo)"},

    {"numero": 606, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Deseos improbables: ojalá + imperfecto de subjuntivo",
     "teoria": "'Ojalá' + imperfecto de subjuntivo expresa un deseo poco probable o contrario a la realidad presente.",
     "explicacion": "Ej: 'Ojalá lloviera' (no llueve, deseo improbable). 'Ojalá tuviera más tiempo' (no lo tengo). Con 'ojalá' + presente de subjuntivo el deseo es más realista ('ojalá llueva'). Con imperfecto, es hipotético.",
     "regla": "ojalá + imperfecto de subjuntivo (deseo improbable/irreal)",
     "ejemplo_correcto": "Ojalá pudiera viajar más.",
     "ejemplo_incorrecto": "Ojalá puedo viajar más. (ojalá = subjuntivo)"},

    {"numero": 607, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Concesivas hipotéticas: aunque + imperfecto de subjuntivo",
     "teoria": "'Aunque' + imperfecto de subjuntivo expresa una concesión hipotética referida al pasado o a una situación irreal.",
     "explicacion": "Ej: 'Aunque lloviera, saldríamos' (hipótesis). 'Aunque me lo pidiera de rodillas, no lo haría'. Indicativo → hecho real; imperfecto de subjuntivo → hipótesis. La elección cambia el significado.",
     "regla": "aunque + imperfecto de subjuntivo = concesión hipotética",
     "ejemplo_correcto": "Aunque me lo pidieras, no cambiaría de opinión.",
     "ejemplo_incorrecto": "Aunque me lo pedías, no cambiaría. (concesión hipotética = subjuntivo imperfecto)"},

    {"numero": 608, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Temporales pasadas: antes de que + imperfecto de subjuntivo",
     "teoria": "Las oraciones temporales que expresan una acción futura respecto a otra pasada usan imperfecto de subjuntivo.",
     "explicacion": "Ej: 'Me fui antes de que llegara' (primero me fui, luego llegó). 'Te llamé antes de que salieras'. 'Antes de que' siempre va con subjuntivo (presente o imperfecto según correlación).",
     "regla": "antes de que + imperfecto de subjuntivo (temporal pasada)",
     "ejemplo_correcto": "Salí antes de que empezara a llover.",
     "ejemplo_incorrecto": "Salí antes de que empezó a llover. (antes de que = subjuntivo)"},

    {"numero": 609, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Finales pasadas: para que + imperfecto de subjuntivo",
     "teoria": "Las oraciones finales con sujetos distintos que expresan propósito pasado usan imperfecto de subjuntivo.",
     "explicacion": "Ej: 'Te lo dije para que lo supieras' (sujetos distintos, pasado). 'Le presté el libro para que lo leyera'. 'Para que' + imperfecto si el verbo principal está en pasado.",
     "regla": "para que + imperfecto de subjuntivo (final pasada, sujetos distintos)",
     "ejemplo_correcto": "Te lo expliqué para que lo entendieras.",
     "ejemplo_incorrecto": "Te lo expliqué para que lo entiendas. (pasado + subjuntivo imperfecto)"},

    {"numero": 610, "bloque": "A", "nivel": "avanzado", "modulo": "b2",
     "titulo": "Repaso integrador A (B2)",
     "teoria": "Repaso del bloque A: formación del imperfecto de subjuntivo (-ra/-se), irregulares (fuera, tuviera, hiciera, dijera, pudiera, quisiera), correlación temporal (pasado + imperfecto de subjuntivo), y usos específicos (quería que, como si, ojalá, aunque, antes de que, para que).",
     "explicacion": "Ejemplo integrador: 'Quería que vinieras a la fiesta, aunque no pudieras quedarte mucho. Te lo dije antes de que te fueras para que lo supieras. Ojalá hubieras venido antes, pero como si no hubiera pasado nada'.",
     "regla": "imperfecto de subjuntivo: -ra/-se + correlación temporal",
     "ejemplo_correcto": "Quería que vinieras, aunque no pudieras quedarte mucho.",
     "ejemplo_incorrecto": "Quería que vengas, aunque no puedas quedarte. (pasado + subjuntivo imperfecto)"},
]

EJERCICIOS = {
    601: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Si ___ más despacio, te entendería. (hablar, yo)",
        "opciones": [
            {"id": "a", "texto": "hablara", "correcta": True, "razon": "Imperfecto subjuntivo -ra."},
            {"id": "b", "texto": "hablaba", "correcta": False, "razon": "Imperfecto indicativo."},
            {"id": "c", "texto": "hablaría", "correcta": False, "razon": "Condicional (nunca en la prótasis)."},
        ], "justificacion_obligatoria": False, "regla": "si + imperfecto subjuntivo"}}],
    602: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Quisiera que ___ a la fiesta. (venir, tú)",
        "opciones": [
            {"id": "a", "texto": "vinieras", "correcta": True, "razon": "Raíz vin- + -iera."},
            {"id": "b", "texto": "vienieras", "correcta": False, "razon": "Raíz incorrecta."},
            {"id": "c", "texto": "vendrías", "correcta": False, "razon": "Condicional."},
        ], "justificacion_obligatoria": False, "regla": "venir -> vinieras"}}],
    603: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Esperaba que ___ antes de las 8. (llegar, tú)",
        "opciones": [
            {"id": "a", "texto": "llegaras", "correcta": True, "razon": "Pasado + imperfecto subjuntivo."},
            {"id": "b", "texto": "llegues", "correcta": False, "razon": "Presente subjuntivo (incoherente con pasado)."},
            {"id": "c", "texto": "llegarás", "correcta": False, "razon": "Futuro."},
        ], "justificacion_obligatoria": False, "regla": "pasado + imperfecto subjuntivo"}}],
    604: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Quería que me ___ cuando llegaras. (llamar, tú)",
        "opciones": [
            {"id": "a", "texto": "llamaras", "correcta": True, "razon": "Deseo pasado + imperfecto subjuntivo."},
            {"id": "b", "texto": "llamas", "correcta": False, "razon": "Presente indicativo."},
            {"id": "c", "texto": "llames", "correcta": False, "razon": "Presente subjuntivo."},
        ], "justificacion_obligatoria": False, "regla": "quería que + imperfecto subjuntivo"}}],
    605: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Gasta dinero como si ___ millonario. (ser, él)",
        "opciones": [
            {"id": "a", "texto": "fuera", "correcta": True, "razon": "como si + imperfecto subjuntivo (irreal)."},
            {"id": "b", "texto": "es", "correcta": False, "razon": "Indicativo, no hipótesis."},
            {"id": "c", "texto": "sería", "correcta": False, "razon": "Condicional."},
        ], "justificacion_obligatoria": False, "regla": "como si + imperfecto subjuntivo"}}],
    606: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Ojalá ___ viajar más. (poder, yo)",
        "opciones": [
            {"id": "a", "texto": "pudiera", "correcta": True, "razon": "Deseo improbable = imperfecto subjuntivo."},
            {"id": "b", "texto": "puedo", "correcta": False, "razon": "Indicativo."},
            {"id": "c", "texto": "podría", "correcta": False, "razon": "Condicional."},
        ], "justificacion_obligatoria": False, "regla": "ojalá + imperfecto subjuntivo"}}],
    607: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Aunque me lo ___, no cambiaría de opinión. (pedir, él)",
        "opciones": [
            {"id": "a", "texto": "pidiera", "correcta": True, "razon": "Concesiva hipotética = imperfecto subjuntivo."},
            {"id": "b", "texto": "pide", "correcta": False, "razon": "Indicativo (hecho real)."},
            {"id": "c", "texto": "pediría", "correcta": False, "razon": "Condicional."},
        ], "justificacion_obligatoria": False, "regla": "aunque + imperfecto subjuntivo"}}],
    608: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Salí antes de que ___ a llover. (empezar, él)",
        "opciones": [
            {"id": "a", "texto": "empezara", "correcta": True, "razon": "antes de que + imperfecto subjuntivo."},
            {"id": "b", "texto": "empezó", "correcta": False, "razon": "Indefinido (antes de que = subjuntivo)."},
            {"id": "c", "texto": "empezará", "correcta": False, "razon": "Futuro."},
        ], "justificacion_obligatoria": False, "regla": "antes de que + imperfecto subjuntivo"}}],
    609: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Te lo expliqué para que lo ___. (entender, tú)",
        "opciones": [
            {"id": "a", "texto": "entendieras", "correcta": True, "razon": "para que + imperfecto subjuntivo (pasado)."},
            {"id": "b", "texto": "entiendas", "correcta": False, "razon": "Presente subjuntivo (incoherente con pasado)."},
            {"id": "c", "texto": "entendiste", "correcta": False, "razon": "Indefinido."},
        ], "justificacion_obligatoria": False, "regla": "para que + imperfecto subjuntivo"}}],
    610: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál integra correctamente B2-A?",
        "opciones": [
            {"id": "a", "texto": "Quería que vinieras, aunque no pudieras quedarte mucho.", "correcta": True, "razon": "Pasado + imperfecto subjuntivo en todos los casos."},
            {"id": "b", "texto": "Quería que vengas, aunque no puedas quedarte mucho.", "correcta": False, "razon": "Presente subjuntivo con pasado."},
            {"id": "c", "texto": "Quería que vendrías, aunque no podrías quedarte mucho.", "correcta": False, "razon": "Condicional en subordinada (incorrecto)."},
        ], "justificacion_obligatoria": False, "regla": "correlación temporal completa"}}],
}

# Bloques B y C (611-630): condicionales 2/3 + secuencia de tiempos
from .tecnicas_b2_bloque_b import TECNICAS_611_620, EJERCICIOS_611_620
from .tecnicas_b2_bloque_c import TECNICAS_621_630, EJERCICIOS_621_630
TECNICAS.extend(TECNICAS_611_620)
TECNICAS.extend(TECNICAS_621_630)
EJERCICIOS.update(EJERCICIOS_611_620)
EJERCICIOS.update(EJERCICIOS_621_630)

# Bloques D, E, F (631-660): pasiva + estilo indirecto + perífrasis
from .tecnicas_b2_bloque_d import TECNICAS_631_640, EJERCICIOS_631_640
from .tecnicas_b2_bloque_e import TECNICAS_641_650, EJERCICIOS_641_650
from .tecnicas_b2_bloque_f import TECNICAS_651_660, EJERCICIOS_651_660
TECNICAS.extend(TECNICAS_631_640)
TECNICAS.extend(TECNICAS_641_650)
TECNICAS.extend(TECNICAS_651_660)
EJERCICIOS.update(EJERCICIOS_631_640)
EJERCICIOS.update(EJERCICIOS_641_650)
EJERCICIOS.update(EJERCICIOS_651_660)

# Bloques G y H (661-680): subordinadas complejas + conectores avanzados
from .tecnicas_b2_bloque_g import TECNICAS_661_670, EJERCICIOS_661_670
from .tecnicas_b2_bloque_h import TECNICAS_671_680, EJERCICIOS_671_680
TECNICAS.extend(TECNICAS_661_670)
TECNICAS.extend(TECNICAS_671_680)
EJERCICIOS.update(EJERCICIOS_661_670)
EJERCICIOS.update(EJERCICIOS_671_680)
