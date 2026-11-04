"""
fix_tildes.py v2 - Restaura tildes y ñ en los JSON de lectura.
Diccionario masivo + regex seguras.
"""
import json
import re
import sys
from pathlib import Path

# ══════════════════════════════════════════════════════════════════
# DICCIONARIO MASIVO
# ══════════════════════════════════════════════════════════════════
WORDS = {
    # ───── ñ ─────
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
    "higuera": "higuera", "ninera": "niñera", "champinon": "champiñón",
    "sabana": "sábana",

    # ───── Tildes - palabras frecuentes ─────
    "tambien": "también", "despues": "después", "asi": "así",
    "dia": "día", "dias": "días", "pais": "país", "paises": "países",
    "raiz": "raíz", "raices": "raíces",
    "aqui": "aquí", "alli": "allí", "ahi": "ahí",
    "ademas": "además", "quizas": "quizás", "quiza": "quizá",
    "rapido": "rápido", "rapida": "rápida",
    "rapidos": "rápidos", "rapidas": "rápidas",
    "rapidamente": "rápidamente",
    "marron": "marrón", "marrones": "marrones",

    # ───── -ía (imperfecto) ─────
    "habia": "había", "habian": "habían", "habias": "habías",
    "tenia": "tenía", "tenian": "tenían", "teniamos": "teníamos",
    "venia": "venía", "venian": "venían",
    "salia": "salía", "salían": "salían",
    "vivia": "vivía", "vivian": "vivían",
    "comia": "comía", "comian": "comían",
    "leia": "leía", "leian": "leían",
    "oia": "oía", "oian": "oían",
    "reia": "reía", "reian": "reían",
    "caia": "caía", "caian": "caían",
    "traia": "traía", "traian": "traían",
    "podia": "podía", "podian": "podían",
    "queria": "quería", "querian": "querían",
    "sabia": "sabía", "sabian": "sabían",
    "decia": "decía", "decian": "decían",
    "hacia": "hacía", "hacian": "hacían",
    "escribia": "escribía", "escribian": "escribían",
    "creia": "creía", "creian": "creían",
    "veia": "veía", "veian": "veían",
    "dormia": "dormía", "dormian": "dormían",
    "sentia": "sentía", "sentian": "sentían",
    "preferia": "prefería", "preferian": "preferían",
    "abria": "abría", "abrian": "abrías",
    "descubria": "descubría", "descubrian": "descubrían",
    "sufria": "sufría", "sufrian": "sufrían",
    "exigia": "exigía", "exigian": "exigían",
    "corregia": "corregía", "corregian": "corregían",
    "protegia": "protegía", "protegian": "protegían",
    "recogia": "recogía", "recogian": "recogían",
    "cogia": "cogía", "cogian": "cogían",
    "elegia": "elegía", "elegian": "elegían",
    "fingia": "fingía", "fingian": "fingían",
    "reunia": "reunía", "sonreia": "sonreía",
    "contribuia": "contribuía", "sustituia": "sustituía",
    "influia": "influía",
    "pedia": "pedía", "pensaba": "pensaba",
    "comprendia": "comprendía", "aprendia": "aprendía",
    "respondia": "respondía", "existia": "existía",
    "resistia": "resistía", "consistia": "consistía",
    "insistia": "insistía", "persistia": "persistía",
    "asistia": "asistía", "subia": "subía",
    "surgia": "surgía", "dirigia": "dirigía",
    "corria": "corría", "moría": "moría",
    "hervia": "hervía", "servia": "servía",
    "vestia": "vestía", "mentia": "mentía",
    "advertia": "advertía", "convertia": "convertía",

    # ───── Pasado 3ª persona (-ó) verbos -ar ─────
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
    "jugo": "jugó", "llego": "llegó", "mando": "mandó",
    "noto": "notó", "mostro": "mostró", "presento": "presentó",
    "penso": "pensó", "recordó": "recordó", "recordo": "recordó",
    "olvido": "olvidó", "perdono": "perdonó", "gano": "ganó",
    "perdio": "perdió", "corrio": "corrió", "sintio": "sintió",
    "siguio": "siguió", "pidio": "pidió", "midio": "midió",
    "murio": "murió", "subio": "subió", "surgio": "surgió",
    "decidio": "decidió", "definio": "definió", "anadio": "añadió",
    "admitio": "admitió", "exigio": "exigió", "surgió": "surgió",
    "escribio": "escribió", "describio": "describió",
    "recibio": "recibió", "subrayo": "subrayó",
    "analizo": "analizó", "explico": "explicó",
    "comunico": "comunicó", "practico": "practicó",
    "establecio": "estableció", "definio": "definió",
    "dedico": "dedicó", "identifico": "identificó",
    "clasifico": "clasificó", "justifico": "justificó",
    "modifico": "modificó", "verifico": "verificó",
    "significo": "significó", "multiplico": "multiplicó",
    "complico": "complicó", "duplico": "duplicó",
    "indico": "indicó", "predico": "predicó",
    "dedico": "dedicó", "aplico": "aplicó",
    "apoyo": "apoyó", "callo": "calló", "crio": "crió",
    "envio": "envió", "frio": "frió", "guio": "guió",
    "rio": "rió", "confio": "confió", "vario": "varió",
    "copio": "copió", "estudio": "estudió",
    "animo": "animó", "calmo": "calmó",
    "limito": "limitó", "quito": "quitó",
    "mato": "mató", "ahogo": "ahogó",

    # ───── Esdrújulas / llanas con tilde ─────
    "album": "álbum", "albumes": "álbumes",
    "cancer": "cáncer", "deficit": "déficit",
    "habitat": "hábitat", "laser": "láser", "master": "máster",
    "regimen": "régimen", "regimenes": "regímenes",
    "dificil": "difícil", "dificiles": "difíciles",
    "facil": "fácil", "faciles": "fáciles",
    "movil": "móvil", "moviles": "móviles",
    "util": "útil", "utiles": "útiles",
    "arbol": "árbol", "arboles": "árboles",
    "angel": "ángel", "angeles": "ángeles",
    "azucar": "azúcar", "carcel": "cárcel",
    "analisis": "análisis", "sintesis": "síntesis",
    "hipotesis": "hipótesis", "parentesis": "paréntesis",
    "area": "área", "areas": "áreas",
    "exito": "éxito", "exitos": "éxitos",
    "oxigeno": "oxígeno",
    "ultimo": "último", "ultima": "última",
    "ultimos": "últimos", "ultimas": "últimas",
    "unico": "único", "unica": "única",
    "unicos": "únicos", "unicas": "únicas",
    "numero": "número", "numeros": "números",
    "prestamo": "préstamo", "prestamos": "préstamos",
    "metodo": "método", "metodos": "métodos",
    "caracter": "carácter", "marmol": "mármol",
    "fertil": "fértil", "agil": "ágil", "fragil": "frágil",
    "habil": "hábil", "debil": "débil", "debiles": "débiles",
    "titulo": "título", "titulos": "títulos",
    "articulo": "artículo", "articulos": "artículos",
    "mayuscula": "mayúscula", "mayusculas": "mayúsculas",
    "minuscula": "minúscula", "minusculas": "minúsculas",
    "pagina": "página", "paginas": "páginas",
    "parrafo": "párrafo", "parrafos": "párrafos",
    "capitulo": "capítulo", "capitulos": "capítulos",
    "medico": "médico", "medica": "médica",
    "medicos": "médicos", "medicas": "médicas",
    "publico": "público", "publica": "pública",
    "publicos": "públicos", "publicas": "públicas",
    "politica": "política", "politico": "político",
    "politicas": "políticas", "politicos": "políticos",
    "academico": "académico", "academica": "académica",
    "academicos": "académicos", "academicas": "académicas",
    "critica": "crítica", "critico": "crítico",
    "criticas": "críticas", "criticos": "críticos",
    "logica": "lógica", "logico": "lógico",
    "estetica": "estética", "estetico": "estético",
    "musica": "música", "musico": "músico",
    "filosofico": "filosófico", "filosofica": "filosófica",
    "pragmatico": "pragmático", "pragmatica": "pragmática",
    "hipotetico": "hipotético", "hipotetica": "hipotética",
    "epico": "épico", "epica": "épica",
    "historico": "histórico", "historica": "histórica",
    "tipico": "típico", "tipica": "típica",
    "basico": "básico", "basica": "básica",
    "practico": "práctico", "practica": "práctica",
    "practicas": "prácticas", "practicos": "prácticos",
    "tecnico": "técnico", "tecnica": "técnica",
    "tecnicas": "técnicas", "tecnicos": "técnicos",
    "simbolico": "simbólico", "simbolica": "simbólica",
    "ironico": "irónico", "ironica": "irónica",
    "catastrofico": "catastrófico", "catastrofica": "catastrófica",
    "caracteristica": "característica",
    "caracteristicas": "características",
    "ejercicio": "ejercicio", "ejercicios": "ejercicios",
    "multiple": "múltiple", "seleccion": "selección",
    "puntuacion": "puntuación", "oracion": "oración",
    "exclamacion": "exclamación", "negacion": "negación",
    "afirmacion": "afirmación", "preposicion": "preposición",
    "proposicion": "proposición", "exposicion": "exposición",
    "disposicion": "disposición", "composicion": "composición",
    "oposicion": "oposición", "posicion": "posición",

    # ───── Adjetivos específicos ─────
    "adjetivo": "adjetivo",
    "calificativo": "calificativo",
    "gramatico": "gramático",
    "gramatica": "gramática",
    "comprension": "comprensión",
    "lectura": "lectura",
    "expresion": "expresión",
    "entonacion": "entonación",
    "narracion": "narración",
    "descripcion": "descripción",
    "narrador": "narrador",

    # ───── Nombres propios ─────
    "Martinez": "Martínez", "Garcia": "García", "Lopez": "López",
    "Perez": "Pérez", "Gonzalez": "González",
    "Fernandez": "Fernández", "Rodriguez": "Rodríguez",
    "Sanchez": "Sánchez", "Mexico": "México", "Peru": "Perú",
    "Panama": "Panamá", "Bogota": "Bogotá", "Medellin": "Medellín",
    "Cordoba": "Córdoba", "Malaga": "Málaga", "Canada": "Canadá",
    "Paris": "París", "Munich": "Múnich", "Milan": "Milán",
    "Lucia": "Lucía", "Sofia": "Sofía", "Maria": "María",
    "Rocio": "Rocío", "Monica": "Mónica", "Irene": "Irene",
    "detras": "detrás", "detras_de": "detrás de",
    "ningun": "ningún", "ninguna": "ninguna",
    "algun": "algún", "alguna": "alguna",
    "ninguno": "ninguno", "alguno": "alguno",
    "tampoco": "tampoco",
}

# ───── Patrones regex (se aplican DESPUÉS del diccionario) ─────
INTERROGATIVE_PATTERNS = [
    (r'([¿¡]\s*)([Cc])omo\b', r'\1\2ómo'),
    (r'([¿¡]\s*)([Qq])ue\b', r'\1\2ué'),
    (r'([¿¡]\s*)([Qq])uien\b', r'\1\2uién'),
    (r'([¿¡]\s*)([Qq])uienes\b', r'\1\2uiénes'),
    (r'([¿¡]\s*)([Cc])ual\b', r'\1\2uál'),
    (r'([¿¡]\s*)([Cc])uales\b', r'\1\2uáles'),
    (r'([¿¡]\s*)([Cc])uando\b', r'\1\2uándo'),
    (r'([¿¡]\s*)([Dd])onde\b', r'\1\2ónde'),
    (r'([¿¡]\s*)([Aa])donde\b', r'\1\2dónde'),
    (r'([¿¡]\s*)([Cc])uanto\b', r'\1\2uánto'),
    (r'([¿¡]\s*)([Cc])uanta\b', r'\1\2uánta'),
    (r'([¿¡]\s*)([Cc])uantos\b', r'\1\2uántos'),
    (r'([¿¡]\s*)([Cc])uantas\b', r'\1\2uántas'),
    (r'([¿¡]\s*)([Pp])or que\b', r'\1\2or qué'),
    (r'([¿¡]\s*)([Pp])orque\b', r'\1\2orqué'),
    (r'([¿¡]\s*)([Cc])omo\b', r'\1\2ómo'),
]

# -ción / -sión (SOLO singular; -ciones/-siones plural NO lleva tilde)
REGEX_CION = re.compile(r'\b([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)cion\b')
REGEX_SION = re.compile(r'\b([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)sion\b')

# "esta" verb (no esta aquí) → está. Solo si está entre "no " y espacio/punto
REGEX_ESTA_VERB = re.compile(r'\b(no|sí|si|aún|aun|todavía|todavia)\s+esta\b')
# "estas" verb (¿Dónde estás?) → estás. Solo detrás de ¿... Dónde/etc.
REGEX_ESTAS_VERB = re.compile(r'([¿]\s*\w+\s+)estas\b')
# "Si," afirmativo al inicio → "Sí,"
REGEX_SI_AFIRM = re.compile(r'(^|[.!?]\s+)Si\s*,')

def fix_text(text):
    if not isinstance(text, str):
        return text
    # 1. Diccionario (con word boundary)
    for old, new in WORDS.items():
        text = re.sub(r'\b' + re.escape(old) + r'\b', new, text)
    # 2. -ción / -sión singular
    text = REGEX_CION.sub(r'\1ción', text)
    text = REGEX_SION.sub(r'\1sión', text)
    # 3. "esta" como verbo
    text = REGEX_ESTA_VERB.sub(lambda m: f"{m.group(1)} está", text)
    # 4. "estas" en preguntas
    text = REGEX_ESTAS_VERB.sub(r'\1estás', text)
    # 5. "Si," afirmativo
    text = REGEX_SI_AFIRM.sub(r'\1Sí,', text)
    # 6. Interrogativos
    for pattern, replacement in INTERROGATIVE_PATTERNS:
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
        if "titulo" in t:
            new = fix_text(t["titulo"])
            if new != t["titulo"]:
                t["titulo"] = new
                changes += 1
        if "cuerpo" in t:
            new = fix_text(t["cuerpo"])
            if new != t["cuerpo"]:
                t["cuerpo"] = new
                changes += 1
        for ej in t.get("ejercicios", []):
            if "enunciado" in ej:
                new = fix_text(ej["enunciado"])
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