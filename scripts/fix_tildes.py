"""
fix_tildes.py v4 - Restaura tildes y ñ en los JSON de lectura.
Diccionario ampliado + case-insensitive + regex -cion/-sion.
"""
import json
import re
import sys
from pathlib import Path

# ══════════════════════════════════════════════════════════════════
# DICCIONARIO
# ══════════════════════════════════════════════════════════════════
WORDS = {
    # ñ
    "anos": "años", "ano": "año", "cumpleanos": "cumpleaños",
    "Espana": "España", "espana": "España",
    "espanol": "español", "espanola": "española",
    "espanoles": "españoles", "espanolas": "españolas",
    "manana": "mañana", "mananas": "mañanas",
    "pequeno": "pequeño", "pequena": "pequeña",
    "pequenos": "pequeños", "pequenas": "pequeñas",
    "pequenez": "pequeñez",
    "nino": "niño", "nina": "niña", "ninos": "niños", "ninas": "niñas",
    "senor": "señor", "senora": "señora", "senores": "señores", "senoras": "señoras",
    "compania": "compañía", "companias": "compañías",
    "companero": "compañero", "companera": "compañera",
    "companeros": "compañeros", "companeras": "compañeras",
    "sueno": "sueño", "suenos": "sueños",
    "carino": "cariño", "montana": "montaña", "montanas": "montañas",
    "bano": "baño", "banos": "baños", "otono": "otoño",
    "ensenar": "enseñar", "ensenanza": "enseñanza",
    "disenar": "diseñar", "diseno": "diseño",
    "engano": "engaño", "enganar": "engañar",
    "extrano": "extraño", "extrana": "extraña",
    "senal": "señal", "senalar": "señalar",
    "muneca": "muñeca", "dueno": "dueño", "duena": "dueña",
    "tamano": "tamaño", "tamanos": "tamaños",
    "anadir": "añadir", "anadido": "añadido",
    "anadida": "añadida", "anadidas": "añadidas", "anadidos": "añadidos",
    "ninera": "niñera", "champinon": "champiñón", "sabana": "sábana",

    # palabras frecuentes
    "tambien": "también", "despues": "después", "asi": "así",
    "dia": "día", "dias": "días", "pais": "país", "paises": "países",
    "raiz": "raíz", "raices": "raíces",
    "aqui": "aquí", "alli": "allí", "ahi": "ahí",
    "ademas": "además", "quizas": "quizás", "quiza": "quizá",
    "rapido": "rápido", "rapida": "rápida",
    "rapidos": "rápidos", "rapidas": "rápidas", "rapidamente": "rápidamente",
    "marron": "marrón", "marrones": "marrones",
    "detras": "detrás", "ningun": "ningún", "ninguno": "ninguno",
    "algun": "algún", "alguno": "alguno",

    # -ía (imperfecto)
    "habia": "había", "habian": "habían", "habias": "habías",
    "tenia": "tenía", "tenian": "tenían", "teniamos": "teníamos",
    "venia": "venía", "venian": "venían",
    "salia": "salía", "vivia": "vivía", "comia": "comía",
    "leia": "leía", "oia": "oía", "reia": "reía", "caia": "caía",
    "traia": "traía", "podia": "podía", "queria": "quería",
    "sabia": "sabía", "decia": "decía", "hacia": "hacía",
    "escribia": "escribía", "creia": "creía", "veia": "veía",
    "dormia": "dormía", "sentia": "sentía", "preferia": "prefería",
    "abria": "abría", "descubria": "descubría", "sufria": "sufría",
    "exigia": "exigía", "corregia": "corregía", "protegia": "protegía",
    "recogia": "recogía", "cogia": "cogía", "elegia": "elegía",
    "fingia": "fingía", "reunia": "reunía", "sonreia": "sonreía",
    "contribuia": "contribuía", "sustituia": "sustituía",
    "comprendia": "comprendía", "aprendia": "aprendía",
    "respondia": "respondía", "existia": "existía",
    "resistia": "resistía", "consistia": "consistía",
    "insistia": "insistía", "asistia": "asistía", "subia": "subía",
    "surgia": "surgía", "dirigia": "dirigía",
    "corria": "corría", "hervia": "hervía", "servia": "servía",
    "vestia": "vestía", "mentia": "mentía", "advertia": "advertía",
    "convertia": "convertía",

    # pasado 3ª persona (-ó)
    "hablo": "habló", "salio": "salió", "llego": "llegó",
    "encontro": "encontró", "busco": "buscó", "pregunto": "preguntó",
    "respondio": "respondió", "volvio": "volvió", "aprendio": "aprendió",
    "abrazo": "abrazó", "empezo": "empezó", "termino": "terminó",
    "comenzo": "comenzó", "acepto": "aceptó", "dejo": "dejó",
    "paso": "pasó", "tomo": "tomó", "llamo": "llamó",
    "miro": "miró", "cambio": "cambió", "estudio": "estudió",
    "trabajo": "trabajó", "publico": "publicó", "aprobo": "aprobó",
    "entro": "entró", "salto": "saltó", "paro": "paró",
    "quedo": "quedó", "llevo": "llevó", "compro": "compró",
    "toco": "tocó", "canto": "cantó", "bailo": "bailó",
    "jugo": "jugó", "mando": "mandó", "noto": "notó",
    "mostro": "mostró", "presento": "presentó", "penso": "pensó",
    "recordo": "recordó", "olvido": "olvidó", "perdono": "perdonó",
    "gano": "ganó", "perdio": "perdió", "corrio": "corrió",
    "sintio": "sintió", "siguio": "siguió", "pidio": "pidió",
    "murio": "murió", "subio": "subió", "surgio": "surgió",
    "decidio": "decidió", "definio": "definió", "admitio": "admitió",
    "exigio": "exigió", "escribio": "escribió", "describio": "describió",
    "recibio": "recibió", "subrayo": "subrayó", "analizo": "analizó",
    "explico": "explicó", "comunico": "comunicó", "practico": "practicó",
    "establecio": "estableció", "dedico": "dedicó", "identifico": "identificó",
    "clasifico": "clasificó", "justifico": "justificó",
    "modifico": "modificó", "verifico": "verificó",
    "significo": "significó", "aplico": "aplicó",
    "apoyo": "apoyó", "callo": "calló", "envio": "envió",
    "confio": "confió", "copio": "copió", "animo": "animó",
    "calmo": "calmó", "limito": "limitó", "quito": "quitó",
    "mato": "mató", "ahogo": "ahogó",

    # esdrújulas / llanas
    "album": "álbum", "cancer": "cáncer", "deficit": "déficit",
    "habitat": "hábitat", "laser": "láser", "master": "máster",
    "regimen": "régimen", "dificil": "difícil", "facil": "fácil",
    "movil": "móvil", "util": "útil", "arbol": "árbol",
    "angel": "ángel", "azucar": "azúcar", "carcel": "cárcel",
    "analisis": "análisis", "sintesis": "síntesis",
    "hipotesis": "hipótesis", "parentesis": "paréntesis",
    "area": "área", "exito": "éxito", "oxigeno": "oxígeno",
    "ultimo": "último", "unico": "único", "numero": "número",
    "prestamo": "préstamo", "metodo": "método", "caracter": "carácter",
    "marmol": "mármol", "fertil": "fértil", "agil": "ágil",
    "fragil": "frágil", "habil": "hábil", "debil": "débil",
    "titulo": "título", "articulo": "artículo",
    "mayuscula": "mayúscula", "minuscula": "minúscula",
    "pagina": "página", "parrafo": "párrafo", "capitulo": "capítulo",

    # adjetivos académicos
    "medico": "médico", "medica": "médica",
    "publico": "público", "publica": "pública",
    "politica": "política", "politico": "político",
    "academico": "académico", "academica": "académica",
    "critica": "crítica", "critico": "crítico",
    "logica": "lógica", "logico": "lógico",
    "estetica": "estética", "musica": "música",
    "filosofico": "filosófico", "filosofica": "filosófica",
    "pragmatico": "pragmático", "hipotetico": "hipotético",
    "epico": "épico", "historico": "histórico",
    "tipico": "típico", "basico": "básico",
    "practico": "práctico", "practica": "práctica",
    "tecnico": "técnico", "tecnica": "técnica",
    "simbolico": "simbólico", "ironico": "irónico",
    "catastrofico": "catastrófico",
    "caracteristica": "característica",
    "multiple": "múltiple", "seleccion": "selección",
    "puntuacion": "puntuación", "oracion": "oración",
    "exclamacion": "exclamación", "negacion": "negación",
    "afirmacion": "afirmación", "preposicion": "preposición",
    "gramatico": "gramático", "gramatica": "gramática",
    "comprension": "comprensión", "expresion": "expresión",
    "entonacion": "entonación", "narracion": "narración",
    "descripcion": "descripción",

    # tiendas -eria
    "panaderia": "panadería", "libreria": "librería",
    "cafeteria": "cafetería", "joyeria": "joyería",
    "zapateria": "zapatería", "carniceria": "carnicería",
    "pasteleria": "pastelería", "peluqueria": "peluquería",
    "ferreteria": "ferretería", "heladeria": "heladería",
    "pescaderia": "pescadería", "fruteria": "frutería",

    # -ia conceptos
    "polemica": "polémica", "retorica": "retórica",
    "ironia": "ironía", "teoria": "teoría",
    "energia": "energía", "alegria": "alegría",
    "biologia": "biología", "tecnologia": "tecnología",
    "psicologia": "psicología", "sociologia": "sociología",
    "filosofia": "filosofía", "economia": "economía",
    "autonomia": "autonomía", "categoria": "categoría",
    "biografia": "biografía", "ortografia": "ortografía",
    "fotografia": "fotografía", "geografia": "geografía",
    "caligrafia": "caligrafía", "poesia": "poesía",
    "fantasia": "fantasía", "alegoria": "alegoría",
    "anafora": "anáfora", "metafora": "metáfora",
    "hiperbole": "hipérbole", "metrica": "métrica",
    "estilistica": "estilística", "semantica": "semántica",
    "diacritica": "diacrítica", "diacritico": "diacrítico",
    "ortografico": "ortográfico", "ortografica": "ortográfica",
    "silaba": "sílaba", "tonica": "tónica",
    "atona": "átona", "esdrujula": "esdrújula",

    # nombres propios
    "Martinez": "Martínez", "Garcia": "García", "Lopez": "López",
    "Perez": "Pérez", "Gonzalez": "González",
    "Fernandez": "Fernández", "Rodriguez": "Rodríguez",
    "Sanchez": "Sánchez", "Mexico": "México", "Peru": "Perú",
    "Bogota": "Bogotá", "Cordoba": "Córdoba", "Malaga": "Málaga",
    "Paris": "París", "Lucia": "Lucía", "Sofia": "Sofía",
    "Maria": "María", "Rocio": "Rocío", "Monica": "Mónica",
}


# ══════════════════════════════════════════════════════════════════
# WORDS_V5: anadidos en v5 (verbos B1, imperfecto, -eria, futuro)
# ══════════════════════════════════════════════════════════════════
WORDS_V5 = {
    # verbos pasado 3a persona nuevos
    "empujo": "empujó", "empujaron": "empujaron",
    "descubrio": "descubrió", "descubrieron": "descubrieron",
    "reabriria": "reabriría", "reabririan": "reabrirían",
    "anunciaba": "anunciaba", "anuncio": "anunció",
    "sintio": "sintió", "sintieron": "sintieron",
    "fijo": "fijó", "fijaron": "fijaron",
    "dudo": "dudó", "dudaron": "dudaron",
    "empujo": "empujó",
    "levanto": "levantó", "levantaron": "levantaron",
    "sonrio": "sonrió", "sonrieron": "sonrieron",
    "explico": "explicó", "explicaron": "explicaron",
    "conto": "contó", "contaron": "contaron",
    "leyo": "leyó", "leyeron": "leyeron",
    "cerro": "cerró", "cerraron": "cerraron",
    "volvio": "volvió", "volvieron": "volvieron",
    "oyo": "oyó", "oyeron": "oyeron",
    "creyo": "creyó", "creyeron": "creyeron",
    "construyo": "construyó", "destruyo": "destruyó",
    "incluyo": "incluyó", "excluyo": "excluyó",
    "influyo": "influyó", "sustituyo": "sustituyó",
    "distribuyo": "distribuyó", "contribuyo": "contribuyó",
    "huyo": "huyó", "cayo": "cayó",
    "trajo": "trajo", "atrajo": "atrajo", "contrajo": "contrajo",
    "mantuvo": "mantuvo", "obtuvo": "obtuvo",
    "retuvo": "retuvo", "contuvo": "contuvo",
    "anduvo": "anduvo", "estuvo": "estuvo",
    "hubo": "hubo", "tuvo": "tuvo", "pudo": "pudo",
    "puso": "puso", "supo": "supo", "quiso": "quiso",
    "vino": "vino", "hizo": "hizo", "dijo": "dijo",
    "fue": "fue", "vio": "vio",

    # imperfecto -ia
    "seguia": "seguía", "seguian": "seguían",
    "salia": "salía", "salian": "salían",
    "llevaba": "llevaba", "volvia": "volvía",
    "olia": "olía", "olian": "olían",
    "subian": "subían", "subia": "subía",
    "debian": "debían", "debia": "debía",
    "tenian": "tenían", "venian": "venían",
    "creian": "creían", "veian": "veían",
    "leian": "leían", "oian": "oían",
    "reian": "reían", "caian": "caían",
    "traian": "traían", "vivian": "vivían",
    "comian": "comían", "escribian": "escribían",
    "dormian": "dormían", "sentian": "sentían",
    "preferian": "preferían", "abrian": "abrían",
    "sufrian": "sufrían", "exigian": "exigían",
    "sonreian": "sonreían", "reunian": "reunían",
    "podia": "podía", "podian": "podían",

    # futuro / condicional
    "dare": "daré", "daras": "darás", "dara": "dará",
    "hare": "haré", "haras": "harás", "hara": "hará",
    "pondre": "pondré", "tendre": "tendré",
    "sabre": "sabré", "podre": "podré",
    "dire": "diré", "diras": "dirás", "dira": "dirá",
    "pedire": "pediré", "pediras": "pedirás", "pedira": "pedirá",
    "volvere": "volveré", "volveras": "volverás", "volvera": "volverá",

    # palabras B1 del texto "La biblioteca secreta"
    "corazon": "corazón", "corazones": "corazones",
    "estanteria": "estantería", "estanterias": "estanterías",
    "librero": "librero", "libreria": "librería",
    "ferreteria": "ferretería", "panaderia": "panadería",
    "insaciable": "insaciable",
    "descuidada": "descuidada", "descuidado": "descuidado",
    "dorado": "dorado", "dorada": "dorada",
    "gastados": "gastados", "gastadas": "gastadas",
    "apretado": "apretado", "apretada": "apretada",
    "muda": "muda", "mudo": "mudo",
}


# ══════════════════════════════════════════════════════════════════
# WORDS_V6: verbos B1 + palabras C2 + generales
# ══════════════════════════════════════════════════════════════════
WORDS_V6 = {
    # verbos B1 "La biblioteca secreta"
    "empujo": "empujó", "descubrio": "descubrió",
    "reabriria": "reabriría", "corazon": "corazón",
    "volvia": "volvía", "fijo": "fijó", "dudo": "dudó",
    "olia": "olía", "estanterias": "estanterías",
    "subian": "subían", "levanto": "levantó",
    "seguia": "seguía", "conto": "contó",
    "debian": "debían", "dare": "daré", "leyo": "leyó",
    "sonrio": "sonrió", "explico": "explicó", "sintio": "sintió",

    # palabras C2 "Para que sirve la critica"
    "valida": "válida", "validas": "válidas",
    "valido": "válido", "validos": "válidos",
    "hermeneutica": "hermenéutica", "hermeneutico": "hermenéutico",
    "categorias": "categorías", "categoria": "categoría",
    "desconfia": "desconfía",
    "ideologia": "ideología", "ideologias": "ideologías",
    "etica": "ética", "etico": "ético",
    "podrian": "podrían", "podria": "podría",
    "epistemica": "epistémica", "epistemicas": "epistémicas",
    "epistemico": "epistémico", "epistemicos": "epistémicos",
    "jerarquias": "jerarquías", "jerarquia": "jerarquía",
    "genealogica": "genealógica", "genealogico": "genealógico",
    "genealogia": "genealogía",
    "solido": "sólido", "solida": "sólida",
    "solidos": "sólidos", "solidas": "sólidas",
    "psicoanalitica": "psicoanalítica",
    "psicoanalitico": "psicoanalítico",
    "ecologica": "ecológica", "ecologico": "ecológico",
    "ecocritica": "ecocrítica",
    "razon": "razón",
    "espectaculo": "espectáculo",
    "mercancia": "mercancía", "mercancias": "mercancías",
    "biopolitica": "biopolítica", "biopolitico": "biopolítico",
    "limites": "límites", "limite": "límite",
    "condicion": "condición",
    "trascendental": "trascendental",
    "deduccion": "deducción",
    "alteridad": "alteridad",
    "traduccion": "traducción",
    "interpretacion": "interpretación",
    "reproduccion": "reproducción",
    "dominacion": "dominación",
    "esencialismo": "esencialismo",
    "esencializar": "esencializar",
    "deconstruccion": "deconstrucción",
    "poscolonial": "poscolonial",
    "postcolonial": "postcolonial",
    "performatividad": "performatividad",
    "binarismo": "binarismo",
    "contemporaneas": "contemporáneas",
    "contemporanea": "contemporánea",
    "indiscriminado": "indiscriminado",
    "infalible": "infalible",
    "rigurosa": "rigurosa",
    "saturado": "saturado",
    "coaccion": "coacción",
    "coacciones": "coacciones",
    "desobediencia": "desobediencia",
    "intercultural": "intercultural",
    "colonialismo": "colonialismo",
    "marxista": "marxista",
    "produccion": "producción",
    "ilustrada": "ilustrada",
    "poblaciones": "poblaciones",
    "descalificacion": "descalificación",
}

# ───── Patrones para enunciados interrogativos ─────
INTERROG_TILDE = {
    "que": "qué", "como": "cómo", "cuando": "cuándo",
    "donde": "dónde", "quien": "quién", "cual": "cuál",
    "cuanto": "cuánto", "cuanta": "cuánta",
    "cuantos": "cuántos", "cuantas": "cuántas",
    "por que": "por qué",
}


def fix_enunciado_interrogativo(text):
    """Anade ¿ y tilda interrogativos en enunciados que son pregunta."""
    if not isinstance(text, str) or not text.endswith("?"):
        return text
    if text.startswith("¿"):
        return text
    if text.lower().startswith("por que"):
        if text[0].isupper():
            return "¿Por qué" + text[len("por que"):]
        return "¿por qué" + text[len("por que"):]
    first_word = text.split(" ", 1)[0] if " " in text else text[:-1]
    first_lower = first_word.lower()
    if first_lower in INTERROG_TILDE:
        repl = INTERROG_TILDE[first_lower]
        if first_word[0].isupper():
            repl = repl[0].upper() + repl[1:]
        rest = text[len(first_word):]
        return "¿" + repl + rest
    return text


# Regex: "que este" -> "que esté" (subjuntivo)
REGEX_ESTE_SUBJ = re.compile(r'\b(que|cuando|aunque|si|ojala|ojalá)\s+este\b', re.IGNORECASE)
# Regex: "para que sirve" -> "para qué sirve" (interrogativo implicito)
REGEX_PARA_QUE_SIRVE = re.compile(r'\b([Pp])ara que sirve\b')


# ══════════════════════════════════════════════════════════════════
# WORDS_V7: C2 "El sujeto atrapado" + ejercicios
# ══════════════════════════════════════════════════════════════════
WORDS_V7 = {
    # texto C2
    "contemporaneo": "contemporáneo",
    "contemporanea": "contemporánea",
    "contemporaneos": "contemporáneos",
    "psicoanalisis": "psicoanálisis",
    "ideologico": "ideológico",
    "ideologicos": "ideológicos",
    "practicas": "prácticas",
    "practicos": "prácticos",
    "imagenes": "imágenes",
    "espectaculos": "espectáculos",
    "campanas": "campañas",
    "economico": "económico",
    "economica": "económica",
    "simbolicos": "simbólicos",
    "simbolicas": "simbólicas",
    "merito": "mérito",
    "metaforas": "metáforas",
    "sintomas": "síntomas",
    "deposito": "depósito",
    "demografia": "demografía",
    "desvia": "desvía",
    "artisticos": "artísticos",
    "artisticas": "artísticas",
    "religion": "religión",
    "religiones": "religiones",
    "dialectica": "dialéctica",
    "dialectico": "dialéctico",
    "jerarquico": "jerárquico",
    "jerarquicos": "jerárquicos",
    "fabrica": "fábrica",
    "dociles": "dóciles",
    "especificos": "específicos",
    "especificas": "específicas",
    "panoptico": "panóptico",
    "panoptica": "panóptica",
    "biologica": "biológica",
    "biologicas": "biológicas",
    "biopolitica": "biopolítica",
    "biopolitico": "biopolítico",

    # ejercicios C2
    "segun": "según",
    "emocion": "emoción",
    "eleccion": "elección",
    "biologico": "biológico",
    "linguistica": "lingüística",
    "busqueda": "búsqueda",
    "perdida": "pérdida",
    "division": "división",
    "fabula": "fábula",
    "desvio": "desvío",
    "alucinacion": "alucinación",
    "narrración": "narración",
    "narracion": "narración",

    # generales sueltos
    "dialogo": "diálogo",
    "dialogos": "diálogos",
    "estructura": "estructura",
    "estructuras": "estructuras",
    "escenario": "escenario",
    "misterio": "misterio",
    "genero": "género",
    "generos": "géneros",
    "poetico": "poético",
    "narrativo": "narrativo",
    "desenlace": "desenlace",
    "personajes": "personajes",
    "argumento": "argumento",
    "argumentos": "argumentos",
    "parrafo": "párrafo",
    "parrafos": "párrafos",
    "muletillas": "muletillas",
    "formal": "formal",
    "informal": "informal",
    "registro": "registro",
    "sintesis": "síntesis",
    "analogia": "analogía",
    "ejemplos": "ejemplos",
    "evidencia": "evidencia",
    "autoridad": "autoridad",
}

# ───── FALSE POSITIVES de v6: reversion con contexto ─────
REGEX_FALSE_POSITIVES = [
    # "a cambió" → "a cambio" (sustantivo)
    (r'\b([Aa])\s+cambió\b', r'\1 cambio'),
    (r'\b([Ee])l\s+cambió\b', r'\1l cambio'),
    (r'\b([Uu]n)\s+cambió\b', r'\1 cambio'),
    (r'\b([Dd])el\s+cambió\b', r'\1el cambio'),
    (r'\b([Ee]ste)\s+cambió\b', r'\1 cambio'),
    (r'\b([Ee]se)\s+cambió\b', r'\1 cambio'),
    # "hacía fines/el/la/los/las" → "hacia ..." (preposicion)
    (r'\bhacía\s+(fines|objetivos?|el|la|los|las|un|una|del|de)\b', r'hacia \1'),
    # "el trabajó" → "el trabajo" (sustantivo)
    (r'\b([Ee])l\s+trabajó\b', r'\1l trabajo'),
    (r'\b([Uu]n)\s+trabajó\b', r'\1 trabajo'),
    (r'\b([Dd])el\s+trabajó\b', r'\1el trabajo'),
    (r'\b([Pp])or\s+el\s+trabajó\b', r'\1or el trabajo'),
    (r'\bmediante\s+el\s+trabajó\b', r'mediante el trabajo'),
    (r'\b([Ee])n\s+el\s+trabajó\b', r'\1n el trabajo'),
    # "el estudio" → "el estudio" (sustantivo, si aparece)
    (r'\b([Ee])l\s+estudió\b', r'\1l estudio'),
    (r'\b([Uu]n)\s+estudió\b', r'\1 estudio'),
    # "el publico" → "el público" (sustantivo/adjetivo) - mas ambiguo
    # lo dejamos como publicó (verbo) porque es menos frecuente como sustantivo
]


# ══════════════════════════════════════════════════════════════════
# WORDS_V8: C2 "El archivo de los espejos" + generales
# ══════════════════════════════════════════════════════════════════
WORDS_V8 = {
    "salon": "salón", "sere": "seré",
    "fotografias": "fotografías", "periodico": "periódico",
    "sintoma": "síntoma", "sintomas": "síntomas",
    "envejeceria": "envejecería", "moriria": "moriría",
    "rompi": "rompí", "proposito": "propósito",
    "heterotopia": "heterotopía", "heterotopias": "heterotopías",
    "deberia": "debería", "parecia": "parecía",
    "entendia": "entendía", "atras": "atrás",
    "borro": "borró", "enseno": "enseñó",
    "subvertia": "subvertía", "rompia": "rompía",
    "encontre": "encontré", "senti": "sentí",
    "linea": "línea", "lineas": "líneas",
    "jardin": "jardín",
    "maquina": "máquina", "maquinas": "máquinas",
    "nomada": "nómada", "nomadas": "nómadas",
    "devolvia": "devolvía",
    "organos": "órganos",
    "producian": "producían",
    "mia": "mía", "mias": "mías",
    "cuantos": "cuántos", "cuantas": "cuántas",
    "sintomatica": "sintomática",
    "panoptico": "panóptico", "panopticos": "panópticos",
    "logicas": "lógicas",
    "traduccion": "traducción",
    "genetico": "genético", "genetica": "genética",
    "fisico": "físico", "fisica": "física",
    "fisicos": "físicos", "fisicas": "físicas",
}

# ───── FALSE POSITIVES contextuales (v8) ─────
REGEX_FALSE_POS_V8 = [
    # "es fijó" -> "es fijo" (adjetivo)
    (r'\bes\s+fijó\b', r'es fijo'),
    (r'\bsea\s+fijó\b', r'sea fijo'),
    # "el pasó del tiempo" -> "el paso del tiempo" (sustantivo)
    (r'\bel\s+pasó\s+del\b', r'el paso del'),
    (r'\bun\s+pasó\s+del\b', r'un paso del'),
    # "Te preguntó" (1a persona) -> "Te pregunto"
    (r'\bTe\s+preguntó\b', r'Te pregunto'),
    # "Te llamó a" (1a persona) -> "Te llamo a"
    (r'\bTe\s+llamó\s+a\b', r'Te llamo a'),
    # "Miró por la ventana" (1a narrativa) -> "Miro por la ventana"
    (r'\bMiró\s+por\s+la\s+ventana\b', r'Miro por la ventana'),
    # "No se que significa" -> "No sé qué significa"
    (r'\bNo\s+se\s+que\s+significa\b', r'No sé qué significa'),
    # "madre silencio" (verbo) -> "madre silenció"
    (r'\blo\s+que\s+la\s+madre\s+silencio\b', r'lo que la madre silenció'),
    # "porque esta" -> "porque está" (verbo)
    (r'\b([Pp])orque\s+esta\b', r'\1orque está'),
    # "mi misma" / "mi mismo" -> "mí misma" (pronombre reflexivo)
    (r'\bmi\s+misma\b', r'mí misma'),
    (r'\bmi\s+mismo\b', r'mí mismo'),
    (r'\bmi\s+mismas\b', r'mí mismas'),
    (r'\bmi\s+mismos\b', r'mí mismos'),
    # "a mi," / "en mi." / "a mi?" -> "mí" (pronombre tónico)
    (r'\b(a|en|de|para|por|sin|sobre|entre|según)\s+mi\b(?=\s*[,;:?.!]|\s*$)', r'\1 mí'),
    # "tu, lector" -> "tú, lector"
    (r'\btu,\s+lector\b', r'tú, lector'),
    # "eres tu?" -> "eres tú?"
    (r'\beres\s+tu\b(?=\s*[?.,;:]|\s*$)', r'eres tú'),
    # "ni en la mia" -> "ni en la mía" (ya cubierto por dict mia, pero por seguridad)
    (r'\bni\s+en\s+la\s+mia\b', r'ni en la mía'),
]


# ══════════════════════════════════════════════════════════════════
# REGEX_V9: pronombres tonicos + esta verbo + no se que + paso del
# ══════════════════════════════════════════════════════════════════
REGEX_V9 = [
    # "a el." -> "a él."
    (r'\ba\s+el\b(?=\s*[.,;:!?]|\s*$)', r'a él'),
    # "de el." -> "de él."
    (r'\bde\s+el\b(?=\s*[.,;:!?]|\s*$)', r'de él'),
    # "para/por/sobre/en el." -> "...él."
    (r'\b(para|por|sobre|en|con|sin|hacia|hasta)\s+el\b(?=\s*[.,;:!?]|\s*$)', r'\1 él'),
    # "esta en/con/por/..." -> "está ..."
    (r'\besta\s+(en|con|por|para|sobre|entre|dentro|fuera)\b', r'está \1'),
    # "que esta en/..." -> "que está en/..."
    (r'\bque\s+esta\b(?=\s+(?:en|con|por|para|sobre|entre|dentro|fuera|bien|mal|claro|listo)\b)', r'que está'),
    # "no se que/como/cuando/donde" -> "no sé ..."
    (r'\bno\s+se\s+que\b', r'no sé qué'),
    (r'\bno\s+se\s+como\b', r'no sé cómo'),
    (r'\bno\s+se\s+cuando\b', r'no sé cuándo'),
    (r'\bno\s+se\s+donde\b', r'no sé dónde'),
    (r'\bno\s+se\s+si\b', r'no sé si'),
    # "El/el pasó del" -> "El/el paso del" (sustantivo)
    (r'\b([Ee])l\s+pasó\s+del\b', r'\1l paso del'),
    (r'\b([Uu])n\s+pasó\s+del\b', r'\1n paso del'),
]


# ══════════════════════════════════════════════════════════════════
# WORDS_V11: C2 "El cuerpo como mercancia"
# ══════════════════════════════════════════════════════════════════
WORDS_V11 = {
    "teorico": "teórico", "teorica": "teórica",
    "teoricos": "teóricos", "teoricas": "teóricas",
    "traves": "través",
    "seras": "serás", "seran": "serán",
    "antitesis": "antítesis",
    "jerarquicas": "jerárquicas", "jerarquicos": "jerárquicos",
    "alla": "allá",
    "dialecticamente": "dialécticamente",
    "ideologica": "ideológica", "ideologicas": "ideológicas",
    "hegemonia": "hegemonía",
    "terminos": "términos",
    "tipografia": "tipografía",
    "multiples": "múltiples",
    "epoca": "época", "epocas": "épocas",
    "formulas": "fórmulas",
    "estrategica": "estratégica", "estrategicas": "estratégicas",
    "estrategico": "estratégico", "estrategicos": "estratégicos",
    "haran": "harán",
    "electronico": "electrónico", "electronica": "electrónica",
    "heterogenea": "heterogénea", "heterogeneo": "heterogéneo",
    "habito": "hábito", "habitos": "hábitos",
    "autobiografico": "autobiográfico", "autobiografica": "autobiográfica",
    "actua": "actúa", "actuan": "actúan",
    "cosmetica": "cosmética",
}

REGEX_V11_FALSE_POS = [
    # "aplicó un marco" -> "aplico un marco" (1a persona)
    (r"\baplicó\s+un\s+marco\b", "aplico un marco"),
    # "primer terminó" -> "primer término"
    (r"\bprimer\s+terminó\b", "primer término"),
    # "el terminó 'superior'" (comillas)
    (r"\bel\s+terminó\b(?=\s*['\u2018\u2019\u201c\u201d])", "el término"),
    # "cada anunció" -> "cada anuncio"
    (r"\bcada\s+anunció\b", "cada anuncio"),
    # "el anunció se" -> "el anuncio se"
    (r"\bel\s+anunció\b(?=\s+se\b)", "el anuncio"),
    # "Un anunció de" / "un anunció" -> "Un anuncio de"
    (r"\b([Uu])n\s+anunció\b", r"\1 anuncio"),
    # "en cambió," -> "en cambio,"
    (r"\ben\s+cambió\b", "en cambio"),
    # "esta atravesado/mediada/..." -> "está ..."
    (r"\besta\s+(mediada|mediado|atravesada|atravesado|construida|construido|basada|basado|anclada|anclado|marcada|marcado|insertada|insertado)\b", r"está \1"),
    # "porque tu lo vales" -> "porque tú lo vales"
    (r"\bporque\s+tu\s+lo\s+vales\b", "porque tú lo vales"),
    # "tu lo mereces" -> "tú lo mereces"
    (r"\b([Tt])u\s+lo\s+mereces\b", r"\1ú lo mereces"),
    # "Tu vales mucho" -> "Tú vales mucho"
    (r"\b([Tt])u\s+vales\s+mucho\b", r"\1ú vales mucho"),
    # "determina que se" -> "determina qué se" (interrogativo indirecto)
    (r"\bdetermina\s+que\s+se\b", "determina qué se"),
    # "y quien puede decirlo" -> "y quién puede decirlo"
    (r"\by\s+quien\s+puede\s+decirlo\b", "y quién puede decirlo"),
    # "desde que posición" -> "desde qué posición"
    (r"\bdesde\s+que\s+posición\b", "desde qué posición"),
    # "En el se articulan" -> "En él se articulan"
    (r"\bEn\s+el\s+se\b", "En él se"),
    # "que estructura dialéctica" (interrogativo tras coma) -> "qué estructura"
    (r",\s+que\s+(estructura|caracteriza|significa|es|hace|ocurre|pasa|hay|se\s+describe|se\s+produce)\b", r", qué \1"),
]


# ══════════════════════════════════════════════════════════════════
# REGEX_V12: interrogativas indirectas + enumeraciones con qué
# ══════════════════════════════════════════════════════════════════
REGEX_V12 = [
    # "que es bello, qué es sano" -> todo "qué" (unificar enumeracion)
    (r"\bque\s+es\s+bello,\s+qué\s+es\s+sano", r"qué es bello, qué es sano"),
    # "revela como se" -> "revela cómo se"
    (r"\brevela\s+como\s+se\b", "revela cómo se"),
    # "y quien puede decirlo" -> "y quién puede decirlo"
    (r"\by\s+quien\s+puede\s+decirlo\b", "y quién puede decirlo"),
    # "Según el texto, como opera" -> "Según el texto, cómo opera"
    (r"\btexto,\s+como\s+opera\b", "texto, cómo opera"),
    # "saussureanos, que relación" -> "saussureanos, qué relación"
    (r"\bsaussureanos,\s+que\s+relación\b", "saussureanos, qué relación"),
    # "Tú lo mereces', que interpelación" -> "...qué interpelación"
    (r"\bmereces',\s+que\s+interpelación\b", "mereces', qué interpelación"),
]


# ══════════════════════════════════════════════════════════════════
# WORDS_V13: C1 "El cuento que se escribia solo"
# ══════════════════════════════════════════════════════════════════
WORDS_V13 = {
    # cuerpo del texto
    "cajon": "cajón", "abrio": "abrió",
    "reconocio": "reconoció", "galerias": "galerías",
    "escalofrio": "escalofrío",
    "comprendio": "comprendió",
    "escucho": "escuchó", "escucharon": "escucharon",
    "leido": "leído", "leida": "leída",
    "escribi": "escribí",
    "vertigo": "vértigo",
    "libero": "liberó",
    "seguiria": "seguiría", "seguirian": "seguirían",
    "Cortazar": "Cortázar",
    "creacion": "creación", "creaciones": "creaciones",
    # ejercicios
    "reflexion": "reflexión", "reflexiones": "reflexiones",
    "monologo": "monólogo", "monologos": "monólogos",
    "cronologico": "cronológico", "cronologica": "cronológica",
    "fantastico": "fantástico", "fantastica": "fantástica",
    "dramatica": "dramática", "dramatico": "dramático",
    "polifonia": "polifonía",
    "cuantica": "cuántica", "cuantico": "cuántico",
    "fisica": "física", "fisico": "físico",
    "descripción": "descripción",
    "categoria": "categoría",
    "funcion": "función",
}

REGEX_V13_FALSE_POS = [
    # "sonaba con un hombre" -> "soñaba con un hombre" (contexto sueño)
    (r"\bsonaba\s+con\s+un\b", "soñaba con un"),
    (r"\bque\s+sonaba\s+con\b", "que soñaba con"),
    # "Bernardo lo escucho con" -> "Bernardo lo escuchó con" (3a persona)
    (r"\b(Bernardo|Aurelio)\s+lo\s+escucho\b", r"\1 lo escuchó"),
    # "Y como termina el cuento" -> "Y cómo termina el cuento" (interrogativa)
    (r"\bY\s+como\s+termina\b", "Y cómo termina"),
    # "Y el, Aurelio" -> "Y él, Aurelio" (pronombre tónico)
    (r"\bY\s+el,\s+Aurelio\b", "Y él, Aurelio"),
    # "Y que el, Aurelio" -> "Y que él, Aurelio"
    (r"\bque\s+el,\s+Aurelio\b", "que él, Aurelio"),
    # "el tambien era" -> "él también era"
    (r"\bel\s+tambien\s+era\b", "él también era"),
    # "quizá si, y los" -> "quizá sí, y los" (afirmación)
    (r"\bquizá\s+si,\b", "quizá sí,"),
    # "Quizá tu eres" -> "Quizá tú eres" (pronombre)
    (r"\bQuizá\s+tu\s+eres\b", "Quizá tú eres"),
    (r"\bquizá\s+tu\s+eres\b", "quizá tú eres"),
    # "escribiste tu" -> "escribiste tú"
    (r"\bescribiste\s+tu\b", "escribiste tú"),
    # "a si mismo / en si mismo / de si mismo" -> "sí mismo"
    (r"\b(a|en|de|para|por|sobre|hacia)\s+si\s+mismo\b", r"\1 sí mismo"),
    (r"\b(a|en|de|para|por|sobre|hacia)\s+si\s+misma\b", r"\1 sí misma"),
    # "esta escribiendo" -> "está escribiendo" (verbo)
    (r"\besta\s+escribiendo\b", "está escribiendo"),
    # "Con que discursos" (interrogativa) -> "Con qué discursos"
    (r"\bCon\s+que\s+discursos\b", "¿Con qué discursos"),
    # "que relación" (interrogativa) -> "qué relación"
    (r"\bque\s+relación\b", "qué relación"),
    # "que función" (interrogativa) -> "qué función"
    (r"\bque\s+función\b", "qué función"),
]


# ══════════════════════════════════════════════════════════════════
# WORDS_V14: C1 "Analisis critico del discurso institucional"
# ══════════════════════════════════════════════════════════════════
WORDS_V14 = {
    # cuerpo
    "pragmatica": "pragmática", "pragmaticas": "pragmáticas",
    "pragmatico": "pragmático", "pragmaticos": "pragmáticos",
    "deictico": "deíctico", "deicticos": "deícticos",
    "deictica": "deíctica", "deicticas": "deícticas",
    "cortesia": "cortesía", "cortesias": "cortesías",
    "lexica": "léxica", "lexicas": "léxicas",
    "lexico": "léxico", "lexicos": "léxicos",
    "sinonimo": "sinónimo", "sinonimos": "sinónimos",
    "antonimo": "antónimo", "antonimos": "antónimos",
    "hiperonimo": "hiperónimo", "hiperonimos": "hiperónimos",
    "hiponimo": "hipónimo", "hiponimos": "hipónimos",
    "anafora": "anáfora", "anaforas": "anáforas",
    "catafora": "catáfora", "cataforas": "catáforas",
    "implicita": "implícita", "implicito": "implícito",
    "implicitas": "implícitas", "implicitos": "implícitos",
    "categorico": "categórico", "categorica": "categórica",
    "categoricos": "categóricos", "categoricas": "categóricas",
    "diagnostico": "diagnóstico", "diagnosticos": "diagnósticos",
    "juridico": "jurídico", "juridica": "jurídica",
    "juridicos": "jurídicos", "juridicas": "jurídicas",
    "economico": "económico", "economica": "económica",
    "economicos": "económicos", "economicas": "económicas",
    "nostalgico": "nostálgico", "nostalgica": "nostálgica",
    "nostalgicos": "nostálgicos", "nostalgicas": "nostálgicas",
    "belica": "bélica", "belico": "bélico",
    "belicas": "bélicas", "belicos": "bélicos",
    "clasica": "clásica", "clasico": "clásico",
    "clasicas": "clásicas", "clasicos": "clásicos",
    "obstaculo": "obstáculo", "obstaculos": "obstáculos",
    "humoristica": "humorística", "humoristico": "humorístico",
    "ironia": "ironía", "ironias": "ironías",
    "fenomeno": "fenómeno", "fenomenos": "fenómenos",
    "retorica": "retórica", "retoricas": "retóricas",
    "retorico": "retórico", "retoricos": "retóricos",
    # comunes
    "analisis": "análisis",
    "critico": "crítico", "critica": "crítica",
    "titulo": "título", "titulos": "títulos",
    "articulo": "artículo",
    "sintesis": "síntesis",
    "hipotesis": "hipótesis",
}

REGEX_V14_FALSE_POS = [
    # "del anunció de la reforma" -> "del anuncio de la reforma"
    (r"\bdel\s+anunció\b", "del anuncio"),
    # "el anunció (2.500 palabras)" -> "el anuncio (2.500..."
    (r"\bel\s+anunció\s+\(", "el anuncio ("),
    # "el anunció usa" -> "el anuncio usa"
    (r"\bel\s+anunció\s+usa\b", "el anuncio usa"),
    # "el anunció construye" -> "el anuncio construye"
    (r"\bel\s+anunció\s+construye\b", "el anuncio construye"),
    # "reforma, cambió, transformación" -> "reforma, cambio, transformación"
    (r"\breforma\",\s+cambió,\s+transformación\b", "reforma, cambio, transformación"),
    # Interrogativas en enunciados de ejercicios: "que mecanismo" -> "qué mecanismo"
    (r"\bque\s+(mecanismo|presuposición|tipo|función|recurso|sección|estrategia)\b", r"qué \1"),
]


# ══════════════════════════════════════════════════════════════════
# WORDS_V15: C1 "Desinformacion: como detectar la manipulacion"
# ══════════════════════════════════════════════════════════════════
WORDS_V15 = {
    "criticamente": "críticamente",
    "deberiamos": "deberíamos",
    "mediatica": "mediática", "mediatico": "mediático",
    "cientifica": "científica", "cientifico": "científico",
    "cientificas": "científicas", "cientificos": "científicos",
    "hipocresia": "hipocresía",
    "dicotomia": "dicotomía", "dicotomias": "dicotomías",
    "estadistica": "estadística", "estadistico": "estadístico",
    "estadisticas": "estadísticas", "estadisticos": "estadísticos",
    "grafico": "gráfico", "graficos": "gráficos",
    "grafica": "gráfica", "graficas": "gráficas",
    "enganoso": "engañoso", "enganosos": "engañosos",
    "enganosa": "engañosa", "enganosas": "engañosas",
    "explicitamente": "explícitamente",
    "algoritmico": "algorítmico", "algoritmica": "algorítmica",
    "algoritmicos": "algorítmicos", "algoritmicas": "algorítmicas",
    "camaras": "cámaras", "camara": "cámara",
    "capitan": "capitán",
    "jovenes": "jóvenes",
    "logicamente": "lógicamente",
    "logica": "lógica", "logico": "lógico",
    "logicas": "lógicas", "logicos": "lógicos",
    "eticamente": "éticamente",
    "etica": "ética", "etico": "ético",
    "eticas": "éticas", "eticos": "éticos",
    "metodologia": "metodología", "metodologias": "metodologías",
    "mayoria": "mayoría", "mayorias": "mayorías",
    "antiguedad": "antigüedad",
    "calculo": "cálculo", "calculos": "cálculos",
    "sustentadas": "sustentadas",
}

REGEX_V15_FALSE_POS = [
    # Título: "como detectar" -> "cómo detectar"
    (r"\bcomo\s+detectar\b", "cómo detectar"),
    # "esta vacunado" -> "está vacunado"
    (r"\besta\s+vacunado\b", "está vacunado"),
    # Interrogativas en ejercicios: "que premisa" -> "qué premisa"
    (r"\bque\s+(premisa|estrategia|falacia|manipulación|hace|revela|define|hay\s+que\s+analizar|sección|tipo|función|recurso)\b", r"qué \1"),
    # "En 'Deberiamos" -> "En 'Deberíamos"
    (r"\bDeberiamos\b", "Deberíamos"),
]


# ══════════════════════════════════════════════════════════════════
# WORDS_V16: C1 "El ruido de las redes sociales"
# ══════════════════════════════════════════════════════════════════
WORDS_V16 = {
    "deberian": "deberían",
    "estan": "están",
    "disenadas": "diseñadas",
    "disenado": "diseñado",
    "disenada": "diseñada",
    "disenados": "diseñados",
    "implicitamente": "implícitamente",
}

REGEX_V16_FALSE_POS = [
    (r"\bel\s+filosofo\b", "el filósofo"),
    (r"\bla\s+repubblica\b", "la república"),
    (r"\bpero\s+si\s+nos\s+hacen\b", "pero sí nos hacen"),
    (r"\bcrítica\s+la\s+fe\b", "critica la fe"),
    (r"\bSi,\s+es\b", "Sí, es"),
    (r"\besta\s+(diseñad[oa]s?)\b", r"está \1"),
]

# ───── Patrones regex ─────
INTERROGATIVE_PATTERNS = [
    (r'([¿¡]\s*)([Cc])omo\b', r'\1\2ómo'),
    (r'([¿¡]\s*)([Qq])ue\b', r'\1\2ué'),
    (r'([¿¡]\s*)([Qq])uien\b', r'\1\2uién'),
    (r'([¿¡]\s*)([Cc])ual\b', r'\1\2uál'),
    (r'([¿¡]\s*)([Cc])uando\b', r'\1\2uándo'),
    (r'([¿¡]\s*)([Dd])onde\b', r'\1\2ónde'),
    (r'([¿¡]\s*)([Cc])uanto\b', r'\1\2uánto'),
    (r'([¿¡]\s*)([Pp])or que\b', r'\1\2or qué'),
]

REGEX_CION = re.compile(r'\b([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)cion\b')
REGEX_SION = re.compile(r'\b([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)sion\b')
REGEX_ESTA_VERB = re.compile(r'\b(no|sí|si)\s+esta\b')
REGEX_ESTAS_VERB = re.compile(r'([¿]\s*\w+\s+)estas\b')
REGEX_SI_AFIRM = re.compile(r'(^|[.!?]\s+)Si\s*,')


def apply_word(text, old, new):
    """Reemplaza preservando mayúsculas (Dia→Día, DIA→DÍA, dia→día)."""
    def replace(m):
        matched = m.group(0)
        if matched.isupper():
            return new.upper()
        if matched and matched[0].isupper():
            return new[0].upper() + new[1:]
        return new
    return re.sub(r'\b' + re.escape(old) + r'\b', replace, text, flags=re.IGNORECASE)


def fix_text(text):
    if not isinstance(text, str):
        return text
    # 1. Diccionario case-insensitive (WORDS + WORDS_V5)
    for old, new in {**WORDS, **WORDS_V5, **WORDS_V6, **WORDS_V7, **WORDS_V8, **WORDS_V11, **WORDS_V13, **WORDS_V14, **WORDS_V15, **WORDS_V16}.items():
        text = apply_word(text, old, new)
    # 2. -ción / -sión singular
    text = REGEX_CION.sub(r'\1ción', text)
    text = REGEX_SION.sub(r'\1sión', text)
    # 3. "no esta" → "no está"
    text = REGEX_ESTA_VERB.sub(lambda m: f"{m.group(1)} está", text)
    # 4. "¿Dónde estas?" → "¿Dónde estás?"
    text = REGEX_ESTAS_VERB.sub(r'\1estás', text)
    # 5. "Si," afirmativo → "Sí,"
    text = REGEX_SI_AFIRM.sub(r'\1Sí,', text)
    # 6. Interrogativos
    for pattern, replacement in INTERROGATIVE_PATTERNS:
        text = re.sub(pattern, replacement, text)
    # 7. "que este" -> "que esté" (subjuntivo)
    text = REGEX_ESTE_SUBJ.sub(lambda m: m.group(1) + " esté", text)
    # 8. "para que sirve" -> "para qué sirve"
    text = REGEX_PARA_QUE_SIRVE.sub(lambda m: m.group(1) + "ara qué sirve", text)
    # 9. FALSE POSITIVES de v6
    for pattern, replacement in REGEX_FALSE_POSITIVES:
        text = re.sub(pattern, replacement, text)
    # 10. FALSE POSITIVES de v8 + pronombres tonicos
    for pattern, replacement in REGEX_FALSE_POS_V8:
        text = re.sub(pattern, replacement, text)
    # 11. Residuos finales v9 (pronombres tonicos, esta verbo, paso del)
    for pattern, replacement in REGEX_V9:
        text = re.sub(pattern, replacement, text)

    # 12. FALSE POSITIVES v11 (reversion contextual C2 mercancia)
    for pattern, replacement in REGEX_V11_FALSE_POS:
        text = re.sub(pattern, replacement, text)

    # 13. REGEX_V12 (interrogativas indirectas v12)
    for pattern, replacement in REGEX_V12:
        text = re.sub(pattern, replacement, text)

    # 14. REGEX_V13 (interrogativas indirectas y pronombres tonicos C1)
    for pattern, replacement in REGEX_V13_FALSE_POS:
        text = re.sub(pattern, replacement, text)

    # 15. REGEX_V14 (anuncio/cambio sustantivo + interrogativas C1)
    for pattern, replacement in REGEX_V14_FALSE_POS:
        text = re.sub(pattern, replacement, text)

    # 16. REGEX_V15 (C1 desinformacion)
    for pattern, replacement in REGEX_V15_FALSE_POS:
        text = re.sub(pattern, replacement, text)

    # 17. REGEX_V16 (C1 ruido redes sociales)
    for pattern, replacement in REGEX_V16_FALSE_POS:
        text = re.sub(pattern, replacement, text)

    return text


def process_tecnicas(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    changes = 0
    fields = ["titulo", "teoria", "explicacion", "regla",
              "ejemplo_correcto", "ejemplo_incorrecto"]
    for t in data:
        for field in fields:
            if field in t and isinstance(t[field], str):
                new = fix_text(t[field])
                if new != t[field]:
                    t[field] = new
                    changes += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return changes


def process_textos(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    changes = 0
    for t in data:
        for field in ["titulo", "cuerpo"]:
            if field in t and isinstance(t[field], str):
                new = fix_text(t[field])
                if new != t[field]:
                    t[field] = new
                    changes += 1
        for ej in t.get("ejercicios", []):
            if "enunciado" in ej:
                new = fix_text(ej["enunciado"])
                new = fix_enunciado_interrogativo(new)
                if new != ej["enunciado"]:
                    ej["enunciado"] = new
                    changes += 1
            payload = ej.get("payload", {})
            if "opciones" in payload and isinstance(payload["opciones"], list):
                new_op = [fix_text(o) for o in payload["opciones"]]
                if new_op != payload["opciones"]:
                    payload["opciones"] = new_op
                    changes += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return changes


def main():
    tech_path = Path("scripts/_lectura_tecnicas_demo.json")
    text_path = Path("scripts/_lectura_textos_demo.json")
    if not tech_path.exists() or not text_path.exists():
        print("[FAIL] Faltan JSON de lectura")
        sys.exit(1)
    print("Procesando tecnicas...")
    n_tec = process_tecnicas(tech_path)
    print(f"  [OK] {n_tec} cambios en tecnicas")
    print("Procesando textos...")
    n_txt = process_textos(text_path)
    print(f"  [OK] {n_txt} cambios en textos")
    print()
    print(f"TOTAL cambios: {n_tec + n_txt}")


if __name__ == "__main__":
    main()