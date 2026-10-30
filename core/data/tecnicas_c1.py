"""Data del modulo C1: Lengua Castellana C1 (100 técnicas, 10 bloques A-J)."""

TECNICAS = [
    {"numero": 701, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Estructura del ensayo académico",
     "teoria": "El ensayo académico tiene tres partes: introducción (contextualiza y presenta la tesis), desarrollo (argumentos con evidencia) y conclusión (síntesis y proyección).",
     "explicacion": "Introducción: 1-2 párrafos que sitúan el tema y formulan la tesis. Desarrollo: 3-5 párrafos, uno por argumento, con evidencia. Conclusión: recapitula y abre nuevas preguntas. Cada párrafo del desarrollo tiene idea principal + evidencia + análisis.",
     "regla": "introducción (tesis) + desarrollo (argumentos + evidencia) + conclusión (síntesis)",
     "ejemplo_correcto": "El ensayo aborda la crisis climática desde tres perspectivas: científica, económica y ética.",
     "ejemplo_incorrecto": "El ensayo empieza con la conclusión y termina con la introducción."},

    {"numero": 702, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "La tesis: formulación clara y discutible",
     "teoria": "La tesis es la afirmación central del ensayo. Debe ser clara, específica y discutible (no una obviedad).",
     "explicacion": "Una tesis fuerte: 'El teletrabajo aumenta la productividad pero deteriora la cohesión del equipo'. Una tesis débil: 'El teletrabajo es un tema importante'. La tesis debe poder defenderse con argumentos y admitir refutación.",
     "regla": "tesis = afirmación clara + específica + discutible + defendible con evidencia",
     "ejemplo_correcto": "La IA generativa transforma la educación superior, pero exige nuevos marcos éticos y pedagógicos.",
     "ejemplo_incorrecto": "La IA es importante para la educación. (vaga, no discutible)"},

    {"numero": 703, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Argumentación deductiva vs inductiva",
     "teoria": "La argumentación deductiva va de lo general a lo particular (silogismo). La inductiva va de casos particulares a una generalización.",
     "explicacion": "Deductiva: 'Todos los seres humanos son mortales; Sócrates es humano; luego Sócrates es mortal'. Inductiva: 'El 90 % de los fumadores encuestados tiene problemas respiratorios; por tanto, fumar causa problemas respiratorios'. Ambas tienen fortalezas y límites.",
     "regla": "deducción: general → particular | inducción: particular → general",
     "ejemplo_correcto": "Si toda la evidencia apunta a que X, entonces X es probable (inducción).",
     "ejemplo_incorrecto": "Todos los X son Y porque sí. (falta premisa universal)"},

    {"numero": 704, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Tipos de evidencia: datos, citas, ejemplos",
     "teoria": "La evidencia sostiene los argumentos. Puede ser cuantitativa (datos), autorizada (citas de expertos) o ilustrativa (ejemplos).",
     "explicacion": "Datos: 'Según el INE, el paro bajó un 3 % en 2024'. Citas: 'Como señala Habermas (1981), la acción comunicativa...'. Ejemplos: 'Un caso paradigmático es el de la Wikipedia'. Combinar tipos fortalece el argumento.",
     "regla": "datos (cuantitativos) + citas (autoridad) + ejemplos (ilustración)",
     "ejemplo_correcto": "Según el Informe PISA 2022, el 25 % del alumnado español tiene bajo rendimiento en lectura.",
     "ejemplo_incorrecto": "Mucha gente dice que es malo. (evidencia vaga)"},

    {"numero": 705, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Contraargumentación: anticipar objeciones",
     "teoria": "La contraargumentación reconoce y responde a las objeciones posibles. Refuerza la credibilidad del ensayo.",
     "explicacion": "Estructura: 'Podría objetarse que... Sin embargo, ...'. Ej: 'Podría objetarse que la IA elimina empleos. No obstante, también crea nuevos perfiles profesionales'. Anticipar la objeción demuestra rigor.",
     "regla": "podría objetarse que X + sin embargo/no obstante Y",
     "ejemplo_correcto": "Podría aducirse que la medida es costosa; sin embargo, el retorno a medio plazo la justifica.",
     "ejemplo_incorrecto": "Nadie puede estar en contra de mi idea. (falta contraargumentación)"},

    {"numero": 706, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Conectores académicos de precisión",
     "teoria": "Los conectores académicos articulan el razonamiento. Los más frecuentes: en consecuencia, en virtud de, cabe destacar, en la medida en que, a tenor de.",
     "explicacion": "En consecuencia (consecuencia formal). En virtud de (causa jurídica o formal). Cabe destacar que (énfasis). En la medida en que (condición/proporción). A tenor de (según). Registro culto, típico de la escritura académica.",
     "regla": "en consecuencia / en virtud de / cabe destacar / en la medida en que / a tenor de",
     "ejemplo_correcto": "A tenor de los datos, cabe destacar un incremento del 20 % en la matrícula.",
     "ejemplo_incorrecto": "Por eso y esas cosas, destacamos. (registro coloquial)"},

    {"numero": 707, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Registro formal: precisión léxica",
     "teoria": "El registro académico exige precisión léxica: evitar coloquialismos, muletillas, vaguedades y repeticiones.",
     "explicacion": "En lugar de 'un montón de', usar 'numerosos'. En lugar de 'cosa', usar el término específico. En lugar de 'muy importante', usar 'fundamental/crucial'. Evitar 'o sea', 'pues', 'bueno' como muletillas. Sustituir 'pero' por 'no obstante/sin embargo'.",
     "regla": "léxico preciso + sin muletillas + sin coloquialismos + sin vaguedades",
     "ejemplo_correcto": "Los resultados son concluyentes y permiten inferir una tendencia clara.",
     "ejemplo_incorrecto": "Los resultados son un montón de buenos y eso."},

    {"numero": 708, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Citas y referencias: integración en el texto",
     "teoria": "Las citas pueden ser directas (con comillas) o indirectas (paráfrasis). Siempre requieren referencia. La integración debe ser fluida.",
     "explicacion": "Cita directa corta: 'Como afirma Eco (1986: 12), \"el lector modelo...\"'. Cita indirecta: 'Eco (1986) sostiene que el lector modelo...'. Cita en bloque: cuando supera 3 líneas, en párrafo aparte y sangrado. Referencia completa al final o en nota.",
     "regla": "cita directa (comillas) | indirecta (paráfrasis) | referencia siempre",
     "ejemplo_correcto": "Como afirma Eco (1986: 12), el lector modelo no es un lector real, sino una estrategia textual.",
     "ejemplo_incorrecto": "Eco dijo que hay un lector modelo. (sin referencia completa)"},

    {"numero": 709, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Cohesión del párrafo académico",
     "teoria": "El párrafo académico tiene una idea principal, evidencia y análisis. Los conectores internos y la referencia anafórica aseguran cohesión.",
     "explicacion": "Estructura: oración temática (idea principal) + oraciones de desarrollo (evidencia) + oración de cierre (análisis). Evitar párrafos de una sola oración, o párrafos de 10 oraciones sin foco. Cohesión: pronombres, sinónimos, elipsis.",
     "regla": "oración temática + evidencia + análisis + cierre",
     "ejemplo_correcto": "El teletrabajo reduce desplazamientos. Según el estudio, un 40 % menos. Esto implica menor huella de carbono.",
     "ejemplo_incorrecto": "El teletrabajo. Reduce desplazamientos. Muchos estudios. Es bueno."},

    {"numero": 710, "bloque": "A", "nivel": "avanzado", "modulo": "c1",
     "titulo": "Repaso integrador A (discurso académico)",
     "teoria": "Repaso: estructura del ensayo, tesis, argumentación deductiva/inductiva, evidencia, contraargumentación, conectores, registro, citas, cohesión.",
     "explicacion": "Ejemplo integrador: 'Este ensayo sostiene que la IA transforma la educación superior. En primer lugar, evidencias recientes lo confirman. Podría objetarse que..., sin embargo... En consecuencia, cabe concluir que se requiere un marco ético'.",
     "regla": "tesis + argumentos + contraargumentos + conectores formales + conclusión",
     "ejemplo_correcto": "En primer lugar, la evidencia lo respalda; no obstante, cabe matizar algunos casos. En consecuencia, la propuesta requiere ajustes.",
     "ejemplo_incorrecto": "Esto es muy importante y hay muchas cosas que decir. (sin estructura académica)"},
]

EJERCICIOS = {
    701: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es el orden correcto de un ensayo académico?",
        "opciones": [
            {"id": "a", "texto": "Introducción (tesis) → desarrollo (argumentos) → conclusión (síntesis)", "correcta": True, "razon": "Estructura estándar del ensayo."},
            {"id": "b", "texto": "Conclusión → introducción → desarrollo", "correcta": False, "razon": "Invertido."},
            {"id": "c", "texto": "Desarrollo → tesis → cierre sin conclusión", "correcta": False, "razon": "Sin tesis clara."},
        ], "justificacion_obligatoria": False, "regla": "intro + desarrollo + conclusión"}}],
    702: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es una tesis académica fuerte?",
        "opciones": [
            {"id": "a", "texto": "La IA generativa transforma la educación superior, pero exige nuevos marcos éticos.", "correcta": True, "razon": "Específica y discutible."},
            {"id": "b", "texto": "La IA es importante para la educación.", "correcta": False, "razon": "Vaga."},
            {"id": "c", "texto": "La educación es un tema fundamental.", "correcta": False, "razon": "Obviedad."},
        ], "justificacion_obligatoria": False, "regla": "tesis clara + discutible"}}],
    703: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué tipo de argumentación va de lo general a lo particular?",
        "opciones": [
            {"id": "a", "texto": "Deductiva", "correcta": True, "razon": "General → particular."},
            {"id": "b", "texto": "Inductiva", "correcta": False, "razon": "Particular → general."},
            {"id": "c", "texto": "Analógica", "correcta": False, "razon": "Por semejanza."},
        ], "justificacion_obligatoria": False, "regla": "deducción: general → particular"}}],
    704: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "«Según el Informe PISA 2022...» es un ejemplo de:",
        "opciones": [
            {"id": "a", "texto": "evidencia con datos", "correcta": True, "razon": "Datos de fuente autorizada."},
            {"id": "b", "texto": "contraargumentación", "correcta": False, "razon": "No refuta."},
            {"id": "c", "texto": "tesis", "correcta": False, "razon": "No es la idea central."},
        ], "justificacion_obligatoria": False, "regla": "tipo de evidencia"}}],
    705: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es una buena contraargumentación?",
        "opciones": [
            {"id": "a", "texto": "Podría objetarse que la medida es costosa; sin embargo, el retorno la justifica.", "correcta": True, "razon": "Reconoce objeción + responde."},
            {"id": "b", "texto": "Nadie puede estar en contra de mi idea.", "correcta": False, "razon": "Sin contraargumentación."},
            {"id": "c", "texto": "Estoy seguro de que tengo razón.", "correcta": False, "razon": "Falta rigor."},
        ], "justificacion_obligatoria": False, "regla": "podría objetarse que X + sin embargo Y"}}],
    706: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué conector es de registro académico formal?",
        "opciones": [
            {"id": "a", "texto": "En virtud de", "correcta": True, "razon": "Formal, típico académico."},
            {"id": "b", "texto": "Por eso", "correcta": False, "razon": "Coloquial."},
            {"id": "c", "texto": "Y esas cosas", "correcta": False, "razon": "Coloquial."},
        ], "justificacion_obligatoria": False, "regla": "conectores académicos"}}],
    707: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es la versión de registro formal?",
        "opciones": [
            {"id": "a", "texto": "Los resultados son concluyentes y permiten inferir una tendencia clara.", "correcta": True, "razon": "Léxico preciso, sin coloquialismos."},
            {"id": "b", "texto": "Los resultados son un montón de buenos.", "correcta": False, "razon": "Coloquial."},
            {"id": "c", "texto": "Los resultados molan.", "correcta": False, "razon": "Coloquial."},
        ], "justificacion_obligatoria": False, "regla": "registro formal"}}],
    708: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál integra correctamente una cita directa?",
        "opciones": [
            {"id": "a", "texto": "Como afirma Eco (1986: 12), «el lector modelo...».", "correcta": True, "razon": "Cita + referencia."},
            {"id": "b", "texto": "Eco dijo que hay un lector modelo.", "correcta": False, "razon": "Sin referencia completa."},
            {"id": "c", "texto": "Un autor dijo que hay un lector modelo.", "correcta": False, "razon": "Sin identificar."},
        ], "justificacion_obligatoria": False, "regla": "cita directa + referencia"}}],
    709: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Qué estructura tiene un párrafo académico bien construido?",
        "opciones": [
            {"id": "a", "texto": "Oración temática + evidencia + análisis + cierre", "correcta": True, "razon": "Estructura estándar."},
            {"id": "b", "texto": "Una sola oración larga", "correcta": False, "razon": "Sin foco."},
            {"id": "c", "texto": "10 oraciones sin idea principal", "correcta": False, "razon": "Sin foco."},
        ], "justificacion_obligatoria": False, "regla": "temática + evidencia + análisis"}}],
    710: [{"tipo": 1, "orden": 1, "payload": {
        "enunciado": "¿Cuál es la integración más académica?",
        "opciones": [
            {"id": "a", "texto": "En primer lugar, la evidencia lo respalda; no obstante, cabe matizar algunos casos. En consecuencia, la propuesta requiere ajustes.", "correcta": True, "razon": "Estructura + conectores formales."},
            {"id": "b", "texto": "Esto es muy importante y hay muchas cosas que decir.", "correcta": False, "razon": "Sin estructura."},
            {"id": "c", "texto": "Básicamente, pues sí, porque es así.", "correcta": False, "razon": "Coloquial."},
        ], "justificacion_obligatoria": False, "regla": "repaso integrador"}}],
}

# Bloques B y C (711-730): registro literario + cohesión avanzada
from .tecnicas_c1_bloque_b import TECNICAS_711_720, EJERCICIOS_711_720
from .tecnicas_c1_bloque_c import TECNICAS_721_730, EJERCICIOS_721_730
TECNICAS.extend(TECNICAS_711_720)
TECNICAS.extend(TECNICAS_721_730)
EJERCICIOS.update(EJERCICIOS_711_720)
EJERCICIOS.update(EJERCICIOS_721_730)

# Bloques D y E (731-750): expresiones idiomáticas + matices aspectuales/modales
from .tecnicas_c1_bloque_d import TECNICAS_731_740, EJERCICIOS_731_740
from .tecnicas_c1_bloque_e import TECNICAS_741_750, EJERCICIOS_741_750
TECNICAS.extend(TECNICAS_731_740)
TECNICAS.extend(TECNICAS_741_750)
EJERCICIOS.update(EJERCICIOS_731_740)
EJERCICIOS.update(EJERCICIOS_741_750)

# Bloques F y G (751-770): léxico especializado + sintaxis compleja
from .tecnicas_c1_bloque_f import TECNICAS_751_760, EJERCICIOS_751_760
from .tecnicas_c1_bloque_g import TECNICAS_761_770, EJERCICIOS_761_770
TECNICAS.extend(TECNICAS_751_760)
TECNICAS.extend(TECNICAS_761_770)
EJERCICIOS.update(EJERCICIOS_751_760)
EJERCICIOS.update(EJERCICIOS_761_770)

# Bloques H y I (771-790): discurso oral formal + análisis crítico
from .tecnicas_c1_bloque_h import TECNICAS_771_780, EJERCICIOS_771_780
from .tecnicas_c1_bloque_i import TECNICAS_781_790, EJERCICIOS_781_790
TECNICAS.extend(TECNICAS_771_780)
TECNICAS.extend(TECNICAS_781_790)
EJERCICIOS.update(EJERCICIOS_771_780)
EJERCICIOS.update(EJERCICIOS_781_790)
