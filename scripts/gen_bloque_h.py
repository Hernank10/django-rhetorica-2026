# scripts/gen_bloque_d.py
from pathlib import Path

content = '''"""Bloque H del modulo B1: subjuntivo imperfecto y condicionales 2/3."""

TECNICAS_401_410 = [
    {"numero": 401, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Subjuntivo imperfecto regular (-ra)",
     "teoria": "El imperfecto de subjuntivo se forma a partir de la 3a persona del plural del pretérito indefinido, quitando '-ron' y añadiendo: -ra, -ras, -ra, -ramos, -rais, -ran.",
     "explicacion": "hablaron -> hablara, hablaras, hablara, habláramos, hablarais, hablaran. Se usa en oraciones subordinadas que dependen de un verbo en pasado ('Quería que hablaras'), en condicionales irreales ('Si hablaras, te entendería') y en cortesía ('Quisiera un café').",
     "regla": "hablar -> hablara, hablaras, hablara, habláramos, hablarais, hablaran",
     "ejemplo_correcto": "Quería que hablaras conmigo ayer.",
     "ejemplo_incorrecto": "Quería que hablabas conmigo ayer. (subordinada en pasado requiere subjuntivo)"},
    {"numero": 402, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Subjuntivo imperfecto regular (-se)",
     "teoria": "Variante de -ra. Se forma igual: hablasen -> hablase, hablases, hablase, hablásemos, hablaseis, hablasen.",
     "explicacion": "Es sinónimo de -ra; -se se prefiere en España escrita y en registros formales. En Hispanoamérica domina -ra. No cambia el significado.",
     "regla": "hablar -> hablase, hablases, hablase, hablásemos, hablaseis, hablasen",
     "ejemplo_correcto": "Si hablase más despacio, te entendería mejor.",
     "ejemplo_incorrecto": "Si hablaría despacio, te entendería. (condicional no va en la prótasis)"},
    {"numero": 403, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Subjuntivo imperfecto irregular: fuera, tuviera, hiciera",
     "teoria": "Los verbos irregulares en indefinido (ser/ir, tener, hacer, poder, querer, venir, decir, poner) mantienen su raíz irregular en imperfecto de subjuntivo.",
     "explicacion": "ser/ir -> fuera; tener -> tuviera; hacer -> hiciera; poder -> pudiera; querer -> quisiera; venir -> viniera; decir -> dijera; poner -> pusiera. La raíz viene del indefinido: tuve -> tuviera, hice -> hiciera.",
     "regla": "tuve -> tuviera; hice -> hiciera; pude -> pudiera; quise -> quisiera",
     "ejemplo_correcto": "Si tuviera tiempo, viajaría más.",
     "ejemplo_incorrecto": "Si tendría tiempo, viajaría más. (no se usa condicional en la prótasis)"},
    {"numero": 404, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Oraciones condicionales tipo 2 (irreal presente)",
     "teoria": "Si + imperfecto de subjuntivo -> condicional simple. Expresa una hipótesis irreal o poco probable en el presente o futuro.",
     "explicacion": "Ej: 'Si tuviera dinero, compraría una casa' (no tengo dinero ahora). El condicional va en la apódosis (la consecuencia), nunca en la prótasis (el 'si').",
     "regla": "Si + imp. subjuntivo, condicional simple.",
     "ejemplo_correcto": "Si estudiara más, aprobaría el examen.",
     "ejemplo_incorrecto": "Si estudiaría más, aprobaría el examen. (nunca 'si' + condicional)"},
    {"numero": 405, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Oraciones condicionales tipo 3 (irreal pasado)",
     "teoria": "Si + pluscuamperfecto de subjuntivo -> condicional compuesto. Expresa una hipótesis irreal sobre el pasado, con consecuencia también pasada.",
     "explicacion": "Ej: 'Si hubiera estudiado, habría aprobado' (no estudié, no aprobé). El pluscuamperfecto de subjuntivo se forma con 'hubiera/hubiese + participio'; el condicional compuesto con 'habría + participio'.",
     "regla": "Si + hubiera/hubiese + participio, habría + participio.",
     "ejemplo_correcto": "Si hubiera sabido que venías, habría preparado algo.",
     "ejemplo_incorrecto": "Si habría sabido que venías, habría preparado algo. (nunca 'si' + condicional compuesto)"},
    {"numero": 406, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Conectores condicionales con subjuntivo: a menos que, con tal de que",
     "teoria": "Además de 'si', hay conectores que siempre llevan subjuntivo cuando la oración expresa condición hipotética: a menos que, con tal de que, a condición de que, siempre que, en caso de que, salvo que.",
     "explicacion": "Todos piden subjuntivo porque plantean una condición no realizada. 'Iré a menos que llueva' = si no llueve, iré. No se usa indicativo con ellos en este sentido.",
     "regla": "a menos que / con tal de que / siempre que + subjuntivo",
     "ejemplo_correcto": "Voy contigo con tal de que no conduzcas rápido.",
     "ejemplo_incorrecto": "Voy contigo con tal de que no conduces rápido. (subjuntivo obligatorio)"},
    {"numero": 407, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Oraciones concesivas: aunque + subjuntivo vs + indicativo",
     "teoria": "'Aunque' puede ir con indicativo (hecho real) o con subjuntivo (hipótesis o desconocimiento).",
     "explicacion": "Indicativo: 'Aunque llueve, salgo' (es un hecho que llueve). Subjuntivo: 'Aunque llueva, saldré' (no sé si lloverá). El subjuntivo marca la información como no verificada.",
     "regla": "aunque + indicativo (real) | aunque + subjuntivo (hipotético)",
     "ejemplo_correcto": "Aunque llueva mañana, iremos al parque.",
     "ejemplo_incorrecto": "Aunque lloverá mañana, iremos al parque. (futuro hipotético pide subjuntivo)"},
    {"numero": 408, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Temporales con subjuntivo: cuando + subj, antes de que",
     "teoria": "Las oraciones temporales que se refieren al futuro o a un momento no realizado llevan subjuntivo: cuando, antes de que, hasta que, en cuanto, mientras.",
     "explicacion": "'Cuando llegues, llámame' (futuro no realizado -> subjuntivo). 'Cuando llegaste, me llamaste' (pasado real -> indicativo). 'Antes de que' siempre lleva subjuntivo.",
     "regla": "cuando / antes de que / hasta que + subjuntivo (futuro no realizado)",
     "ejemplo_correcto": "Cuando termines la tarea, avísame.",
     "ejemplo_incorrecto": "Cuando terminarás la tarea, avísame. (futuro no realizado pide subjuntivo)"},
    {"numero": 409, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Oraciones finales con subjuntivo: para que, a fin de que",
     "teoria": "Las oraciones finales que expresan propósito con sujetos distintos llevan subjuntivo: para que, a fin de que, con el propósito de que, con la intención de que.",
     "explicacion": "Con sujeto distinto -> 'para que + subjuntivo': 'Te lo digo para que lo sepas'. Con sujeto idéntico -> 'para + infinitivo': 'Estudio para aprender'.",
     "regla": "para que / a fin de que + subjuntivo (sujetos distintos)",
     "ejemplo_correcto": "Te presto el libro para que lo leas.",
     "ejemplo_incorrecto": "Te presto el libro para que lo lees. (subjuntivo obligatorio con sujeto distinto)"},
    {"numero": 410, "bloque": "H", "nivel": "intermedio", "modulo": "b1",
     "titulo": "Repaso integrador B1",
     "teoria": "Repaso de las estructuras B1: pasados (indefinido, imperfecto, perfecto, pluscuamperfecto), futuro, condicional, subjuntivo presente e imperfecto, condicionales 1/2/3, estilo indirecto y conectores avanzados.",
     "explicacion": "Consolida el nivel B1 completo. Ejemplo integrador: 'Si hubiera sabido que venías, habría preparado algo, y ahora estaríamos celebrando.' (tipo 3 + consecuencia presente).",
     "regla": "Integración: si + plusc. subj, condicional compuesto | si + imp. subj, condicional simple",
     "ejemplo_correcto": "Si hubiera estudiado más, ahora tendría un mejor trabajo.",
     "ejemplo_incorrecto": "Si habría estudiado más, ahora tendría un mejor trabajo. (nunca 'si' + condicional)"},
]

EJERCICIOS_401_410 = {
    401: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Quería que ___ conmigo ayer (hablar, tú).",
        "opciones": [
            {"id": "a", "texto": "hablaras", "correcta": True, "razon": "Subordinada en pasado -> imperfecto de subjuntivo."},
            {"id": "b", "texto": "hablabas", "correcta": False, "razon": "Indicativo, no admite subordinada dependiente en pasado."},
            {"id": "c", "texto": "hablarías", "correcta": False, "razon": "Condicional no va en subordinada de 'querer'."},
        ], "justificacion_obligatoria": False, "regla": "querer que + imperfecto de subjuntivo"}}],
    402: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Si ___ más despacio, te entendería.",
        "opciones": [
            {"id": "a", "texto": "hablases", "correcta": True, "razon": "Variante -se del imperfecto de subjuntivo."},
            {"id": "b", "texto": "hablarías", "correcta": False, "razon": "Condicional no va en la prótasis."},
            {"id": "c", "texto": "hablabas", "correcta": False, "razon": "Indicativo no forma condicional tipo 2."},
        ], "justificacion_obligatoria": False, "regla": "si + imperfecto de subjuntivo"}}],
    403: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Si ___ tiempo, viajaría más.",
        "opciones": [
            {"id": "a", "texto": "tuviera", "correcta": True, "razon": "Raíz irregular tuv- + -iera."},
            {"id": "b", "texto": "tendría", "correcta": False, "razon": "Condicional no va en la prótasis."},
            {"id": "c", "texto": "tenía", "correcta": False, "razon": "Imperfecto de indicativo no forma condicional tipo 2."},
        ], "justificacion_obligatoria": False, "regla": "si + tuviera"}}],
    404: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es correcta (condicional tipo 2)?",
        "opciones": [
            {"id": "a", "texto": "Si estudiara más, aprobaría el examen.", "correcta": True, "razon": "Si + imp. subj + condicional simple."},
            {"id": "b", "texto": "Si estudiaría más, aprobaría el examen.", "correcta": False, "razon": "Nunca 'si + condicional'."},
            {"id": "c", "texto": "Si estudiaba más, aprobaría el examen.", "correcta": False, "razon": "Imperfecto de indicativo no."},
        ], "justificacion_obligatoria": False, "regla": "si + imp. subj, condicional"}}],
    405: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Si ___ que venías, habría preparado algo.",
        "opciones": [
            {"id": "a", "texto": "hubiera sabido", "correcta": True, "razon": "Pluscuamperfecto de subjuntivo en la prótasis."},
            {"id": "b", "texto": "habría sabido", "correcta": False, "razon": "Condicional compuesto no va en la prótasis."},
            {"id": "c", "texto": "había sabido", "correcta": False, "razon": "Pluscuamperfecto de indicativo no forma tipo 3."},
        ], "justificacion_obligatoria": False, "regla": "si + hubiera + part., habría + part."}}],
    406: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Voy contigo con tal de que no ___ rápido.",
        "opciones": [
            {"id": "a", "texto": "conduzcas", "correcta": True, "razon": "Conector condicional + subjuntivo."},
            {"id": "b", "texto": "conduces", "correcta": False, "razon": "Indicativo no con 'con tal de que'."},
            {"id": "c", "texto": "conducirás", "correcta": False, "razon": "Futuro no."},
        ], "justificacion_obligatoria": False, "regla": "con tal de que + subjuntivo"}}],
    407: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es correcta (hipotético futuro)?",
        "opciones": [
            {"id": "a", "texto": "Aunque llueva, iremos al parque.", "correcta": True, "razon": "Aunque + subjuntivo = hipótesis."},
            {"id": "b", "texto": "Aunque lloverá, iremos al parque.", "correcta": False, "razon": "No se usa futuro tras 'aunque'."},
            {"id": "c", "texto": "Aunque llueve, iremos al parque.", "correcta": False, "razon": "Indicativo marca hecho real, no futuro hipotético."},
        ], "justificacion_obligatoria": False, "regla": "aunque + subjuntivo (hipotético)"}}],
    408: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Cuando ___ la tarea, avísame.",
        "opciones": [
            {"id": "a", "texto": "termines", "correcta": True, "razon": "Futuro no realizado -> subjuntivo."},
            {"id": "b", "texto": "terminarás", "correcta": False, "razon": "Futuro no tras 'cuando'."},
            {"id": "c", "texto": "terminas", "correcta": False, "razon": "Indicativo expresa hábito, no futuro puntual."},
        ], "justificacion_obligatoria": False, "regla": "cuando + subjuntivo (futuro)"}}],
    409: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "Te presto el libro para que lo ___.",
        "opciones": [
            {"id": "a", "texto": "leas", "correcta": True, "razon": "Sujetos distintos -> subjuntivo."},
            {"id": "b", "texto": "lees", "correcta": False, "razon": "Indicativo, no forma final con sujeto distinto."},
            {"id": "c", "texto": "leerás", "correcta": False, "razon": "Futuro no."},
        ], "justificacion_obligatoria": False, "regla": "para que + subjuntivo"}}],
    410: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál integra correctamente B1?",
        "opciones": [
            {"id": "a", "texto": "Si hubiera estudiado más, ahora tendría mejor trabajo.", "correcta": True, "razon": "Tipo 3 con consecuencia presente."},
            {"id": "b", "texto": "Si habría estudiado más, ahora tendría mejor trabajo.", "correcta": False, "razon": "Nunca 'si + condicional'."},
            {"id": "c", "texto": "Si estudiaba más, ahora tendría mejor trabajo.", "correcta": False, "razon": "Imperfecto de indicativo no forma tipo 3."},
        ], "justificacion_obligatoria": False, "regla": "si + plusc. subj, condicional"}}],
}
'''

Path("core/data/tecnicas_b1_bloque_h.py").write_text(content, encoding="utf-8")
print(f"[OK] Escrito core/data/tecnicas_b1_bloque_h.py ({len(content)} bytes)")