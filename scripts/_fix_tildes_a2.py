"""_fix_tildes_a2.py - Corrige tildes, ñ y redaccion en ejercicios A2.

Que corrige:
  1. Interrogativas tras ¿ y en preguntas (¿que -> ¿qué)
  2. Palabras con ñ (anos->años, ninos->niños, compania->compañía)
  3. Acentos seguros (mas->más, segun->según, por que->por qué)
  4. Redaccion: añade ¿ faltante, colapsa espacios, limpia puntuacion

Que NO corrige (ambiguo, requiere revision manual):
  - esta/está, tu/tú, el/él, mi/mí (depende de contexto)
  - solo/sólo (RAE ya no exige tilde)

Aplica a: enunciado, payload.opciones[], payload.explicacion.
NO toca los textos del corpus (ya tienen tildes).

DRY-RUN por defecto. --apply para escribir.
"""
import os, sys, re, argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
parser.add_argument("--nivel", default="A2")
parser.add_argument("--include-textos", action="store_true",
                    help="Tambien corregir textos del corpus (default: no)")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps
from django.db import transaction

EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

# ─── Diccionarios ────────────────────────────────────────────

# Interrogativas que SIEMPRE llevan tilde cuando son pregunta
INTERROGATIVAS = {
    "que": "qué", "quien": "quién", "quienes": "quiénes",
    "cual": "cuál", "cuales": "cuáles",
    "donde": "dónde", "cuando": "cuándo", "como": "cómo",
    "cuanto": "cuánto", "cuanta": "cuánta",
    "cuantos": "cuántos", "cuantas": "cuántas",
}

# Palabras con ñ (reemplazo word-boundary, sin ambiguedad en A2)
N_WORDS = {
    "anos": "años", "ano": "año",
    "nino": "niño", "ninos": "niños",
    "nina": "niña", "ninas": "niñas",
    "compania": "compañía", "companias": "compañías",
    "senor": "señor", "senora": "señora",
    "senores": "señores", "senoras": "señoras",
    "manana": "mañana", "mananas": "mañanas",
    "espanol": "español", "espanola": "española",
    "espanoles": "españoles", "espanolas": "españolas",
    "pequeno": "pequeño", "pequena": "pequeña",
    "pequenos": "pequeños", "pequenas": "pequeñas",
    "muneca": "muñeca", "munecas": "muñecas",
    "sueno": "sueño", "suenos": "sueños",
    "montana": "montaña", "montanas": "montañas",
    "dueno": "dueño", "duena": "dueña",
    "duenos": "dueños", "duenas": "dueñas",
    "extrano": "extraño", "extrana": "extraña",
    "extranos": "extraños", "extranas": "extrañas",
    "engano": "engaño", "enganos": "engaños",
    "cana": "caña", "canas": "cañas",
    "canon": "cañón", "canones": "cañones",
    "banar": "bañar", "bano": "baño", "banos": "baños",
    "sabana": "sábana", "sabanas": "sábanas",
    "pestana": "pestaña", "pestanas": "pestañas",
    "champinon": "champiñón", "champinones": "champiñones",
    "acampanar": "acampanar",  # placeholder, no tocar
    "mullido": "mullido",  # ya tiene
    # NO: pena/peña, ano/ano (ambiguo en otros contextos),
    #     sino/sinonimo (ambiguo)
}
N_WORDS = {k: v for k, v in N_WORDS.items() if k != v}  # limpiar placeholders

# Acentos muy seguros en A2
SAFE_ACCENTS = {
    "mas": "más",      # "mas"=but es rarisimo en A2
    "segun": "según",
    "despues": "después",
    "ademas": "además",
    "tambien": "también",
    "aqui": "aquí", "alli": "allí", "asi": "así",
    "facil": "fácil", "dificil": "difícil",
    "util": "útil", "utiles": "útiles",
    "arbol": "árbol", "arboles": "árboles",
    "azucar": "azúcar",
    "telefono": "teléfono",
    "pagina": "página", "paginas": "páginas",
    "proximo": "próximo", "proxima": "próxima",
    "ultimo": "último", "ultima": "última",
    "siguiente": "siguiente",  # ya tiene
    "numero": "número", "numeros": "números",
    "practico": "práctico", "practica": "práctica",
    "publico": "público", "publica": "pública",
    "musica": "música",
    "medico": "médico", "medica": "médica",
    "logico": "lógico", "logica": "lógica",
    "rapido": "rápido", "rapida": "rápida",
    "comodo": "cómodo", "comoda": "cómoda",
}

# ─── Funciones de correccion ────────────────────────────────

def corregir_interrogativas(text):
    """Añade tilde a interrogativas tras ¿ y en primera palabra de preguntas."""
    if not text:
        return text

    # 1. Tras ¿
    def repl_after_quest(m):
        prefix = m.group(1)  # "¿" o "¿ "
        word = m.group(2).lower()
        accented = INTERROGATIVAS.get(word, word)
        # mantener mayuscula inicial si la tenia
        if m.group(2)[0].isupper():
            accented = accented[0].upper() + accented[1:]
        return prefix + accented

    text = re.sub(r'(¿\s*)([A-Za-zÁÉÍÓÚÑáéíóúñ]+)', repl_after_quest, text)

    # 2. Si el texto completo (o una oracion) termina en ? y empieza con interrogativa
    #    sin ¿, arreglamos la primera palabra + añadimos ¿
    stripped = text.strip()
    if "?" in stripped and "¿" not in stripped:
        # Añadir ¿ al principio si la primera palabra es interrogativa
        first_word_match = re.match(r'^([A-Za-zÁÉÍÓÚÑáéíóúñ]+)', stripped)
        if first_word_match:
            first_word = first_word_match.group(1)
            lower = first_word.lower()
            if lower in INTERROGATIVAS:
                accented = INTERROGATIVAS[lower]
                if first_word[0].isupper():
                    accented = accented[0].upper() + accented[1:]
                text = "¿" + accented + stripped[len(first_word):]

    # 3. "por que" -> "por qué" (siempre, en preguntas)
    text = re.sub(r'\bpor que\b', 'por qué', text, flags=re.IGNORECASE)
    text = re.sub(r'\bPor que\b', 'Por qué', text)

    return text


def corregir_n(text):
    """Sustituye palabras sin ñ por sus versiones correctas."""
    if not text:
        return text
    for bad, good in N_WORDS.items():
        # Word boundary case-insensitive, preservar capitalizacion
        def repl(m, good=good):
            original = m.group(0)
            if original[0].isupper():
                return good[0].upper() + good[1:]
            return good
        text = re.sub(rf'\b{re.escape(bad)}\b', repl, text, flags=re.IGNORECASE)
    return text


def corregir_acentos(text):
    """Acentos seguros."""
    if not text:
        return text
    for bad, good in SAFE_ACCENTS.items():
        if bad == good:
            continue
        def repl(m, good=good):
            original = m.group(0)
            if original[0].isupper():
                return good[0].upper() + good[1:]
            return good
        text = re.sub(rf'\b{re.escape(bad)}\b', repl, text, flags=re.IGNORECASE)
    return text


def corregir_redaccion(text):
    """Redaccion safe: espacios, puntuacion."""
    if not text:
        return text
    # Colapsar espacios multiples
    text = re.sub(r' +', ' ', text)
    # Quitar espacio antes de puntuacion
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    # Quitar espacios al inicio/final
    text = text.strip()
    return text


def corregir_texto(text):
    """Pipeline completo."""
    if not isinstance(text, str) or not text.strip():
        return text
    original = text
    text = corregir_interrogativas(text)
    text = corregir_n(text)
    text = corregir_acentos(text)
    text = corregir_redaccion(text)
    return text


def corregir_payload(payload):
    """Corrige payload.opciones[] y payload.explicacion."""
    if not isinstance(payload, dict):
        return payload, 0
    cambios = 0
    new_payload = dict(payload)

    if "opciones" in payload and isinstance(payload["opciones"], list):
        new_ops = []
        for op in payload["opciones"]:
            new_op = corregir_texto(op) if isinstance(op, str) else op
            if new_op != op:
                cambios += 1
            new_ops.append(new_op)
        new_payload["opciones"] = new_ops

    if "explicacion" in payload and isinstance(payload["explicacion"], str):
        new_expl = corregir_texto(payload["explicacion"])
        if new_expl != payload["explicacion"]:
            cambios += 1
        new_payload["explicacion"] = new_expl

    return new_payload, cambios


def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)


# ─── Diagnostico ────────────────────────────────────────────

header("A", f"EJERCICIOS {args.nivel} - TILDES Y REDACCION")

ejs = list(EJ.objects.filter(tecnica__nivel_mcer=args.nivel).select_related("tecnica"))

cambios_enunciado = 0
cambios_payload = 0
cambios_total = 0
ejemplos = []

for e in ejs:
    enun_orig = e.enunciado or ""
    enun_new = corregir_texto(enun_orig)
    payload_new, c_payload = corregir_payload(e.payload)

    c_enun = 1 if enun_new != enun_orig else 0
    c_total = c_enun + c_payload

    if c_enun:
        cambios_enunciado += 1
    if c_payload:
        cambios_payload += 1
    if c_total:
        cambios_total += 1
        if len(ejemplos) < 8:
            ejemplos.append({
                "tec": e.tecnica.numero,
                "antes_enun": enun_orig[:80],
                "despues_enun": enun_new[:80],
                "c_payload": c_payload,
            })

print(f"  Total ejercicios: {len(ejs)}")
print(f"  Con cambios en enunciado: {cambios_enunciado}")
print(f"  Con cambios en payload:   {cambios_payload}")
print(f"  Con algun cambio:         {cambios_total}")

if ejemplos:
    header("B", "MUESTRA DE CAMBIOS")
    for ej in ejemplos:
        print(f"\n  tec #{ej['tec']}")
        print(f"    ANTES:   {ej['antes_enun']}")
        print(f"    DESPUES: {ej['despues_enun']}")
        if ej["c_payload"]:
            print(f"    (payload: {ej['c_payload']} cambios)")

# ─── Textos (opcional) ──────────────────────────────────────

if args.include_textos:
    header("C", "TEXTOS (opcional)")
    textos = list(TX.objects.filter(nivel_mcer=args.nivel))
    print(f"  Textos a revisar: {len(textos)}")
    for tx in textos:
        cuerpo_new = corregir_texto(tx.cuerpo or "")
        if cuerpo_new != tx.cuerpo:
            print(f"  [CAMBIO] id={tx.id} '{tx.titulo[:40]}'")

# ─── Aplicar ────────────────────────────────────────────────

header("D", "APLICAR" if args.apply else "DRY-RUN")

if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print(f"  Se corregirian {cambios_total} ejercicios.")
    print("  Ejecuta con --apply para escribir.")
    sys.exit(0)

with transaction.atomic():
    aplicados = 0
    for e in ejs:
        enun_new = corregir_texto(e.enunciado or "")
        payload_new, _ = corregir_payload(e.payload)

        campos = []
        if enun_new != e.enunciado:
            e.enunciado = enun_new
            campos.append("enunciado")
        if payload_new != e.payload:
            e.payload = payload_new
            campos.append("payload")

        if campos:
            e.save(update_fields=campos)
            aplicados += 1

    print(f"\n  [OK] {aplicados} ejercicios corregidos")

# ─── Verificar ─────────────────────────────────────────────

header("E", "VERIFICAR")

ejs_post = list(EJ.objects.filter(tecnica__nivel_mcer=args.nivel))

# Contar tildes/ñ presentes ahora
con_tildes = sum(1 for e in ejs_post
                  if e.enunciado and ("á" in e.enunciado or "é" in e.enunciado
                                       or "í" in e.enunciado or "ó" in e.enunciado
                                       or "ú" in e.enunciado or "ñ" in e.enunciado
                                       or "¿" in e.enunciado or "¡" in e.enunciado))
pct = 100 * con_tildes / max(1, len(ejs_post))

print(f"  Ejercicios con tildes/ñ/¿: {con_tildes}/{len(ejs_post)} ({pct:.1f}%)")

# Muestras para sanity check
print(f"\n  Muestras (primeros 5 con tildes):")
mostrados = 0
for e in ejs_post:
    if e.enunciado and ("á" in e.enunciado or "é" in e.enunciado or "ñ" in e.enunciado
                         or "¿" in e.enunciado):
        print(f"    tec #{e.tecnica.numero}: {e.enunciado[:75]}")
        mostrados += 1
        if mostrados >= 5:
            break

if pct >= 90:
    print(f"\n  [OK] TILDES COMPLETAS")
else:
    print(f"\n  [WARN] {100 - pct:.0f}% aun sin tildes. Revisar manualmente.")

print()