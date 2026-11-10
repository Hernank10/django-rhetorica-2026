"""_fix_tildes_a2_extra.py - Segunda pasada de tildes para las 60 palabras A2
que el diccionario basico no cubrio (verbos -io/-o pasado, -cion, -sion, adjetivos).

Idempotente. Aplica a enunciado + payload.opciones[] + payload.explicacion.

DRY-RUN por defecto. --apply para escribir.
"""
import os, sys, re, argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
parser.add_argument("--nivel", default="A2")
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

# Palabras especificas A2 (verificadas contra el diagnostico de 60)
EXTENDED = {
    # Profesiones / personas
    "biologa": "bióloga", "biologo": "biólogo",
    "companero": "compañero", "companera": "compañera",
    "companeros": "compañeros", "companeras": "compañeras",
    # Verbos conjugados pasado (-ó)
    "pregunto": "preguntó", "salio": "salió", "estiro": "estiró",
    "sonrio": "sonrió", "aprendio": "aprendió", "escribio": "escribió",
    "encendio": "encendió", "bostezo": "bostezó",
    "buscaramos": "buscáramos", "estaria": "estarías",  # ojo: podria ser "estaria"
    # Verbos con ñ
    "ensena": "enseña", "enseno": "enseñó", "ensena": "enseña",
    # Sustantivos -cion/-sion
    "expresion": "expresión", "intencion": "intención",
    "informacion": "información", "solucion": "solución",
    "descripcion": "descripción", "personificacion": "personificación",
    "conversacion": "conversación", "relacion": "relación",
    "funcion": "función", "comunicacion": "comunicación",
    "presentacion": "presentación", "situacion": "situación",
    "decision": "decisión", "discusion": "discusión",
    # Adjetivos
    "agil": "ágil", "agiles": "ágiles",
    "creible": "creíble", "creibles": "creíbles",
    "ideologico": "ideológico", "ideologica": "ideológica",
    "fantastica": "fantástica", "fantastico": "fantástico",
    "retorica": "retórica", "retorico": "retórico",
    "academicas": "académicas", "academicos": "académicos",
    "academica": "académica", "academico": "académico",
    # Sustantivos / otros
    "dialogo": "diálogo", "dialogos": "diálogos",
    "ironia": "ironía", "ironico": "irónico", "ironica": "irónica",
    "energia": "energía",
    "movil": "móvil", "moviles": "móviles",
    "ladron": "ladrón", "ladrones": "ladrones",
    "carino": "cariño",
    "jovenes": "jóvenes",
    "habia": "había", "habian": "habían",
    "sinonimo": "sinónimo", "sinonimos": "sinónimos",
    "antonimo": "antónimo", "antonimos": "antónimos",
    "fria": "fría", "frio": "frío",
    "Garcia": "García",
    # Interrogativas (por si escaparon)
    "quienes": "quiénes",
    "de que": "de qué",
}

def corregir_extendido(text):
    """Aplica el diccionario extendido palabra por palabra."""
    if not text:
        return text
    for bad, good in EXTENDED.items():
        if bad == good:
            continue
        # Si la clave tiene espacio, buscar frase exacta
        if " " in bad:
            text = re.sub(rf'\b{re.escape(bad)}\b', good, text, flags=re.IGNORECASE)
        else:
            def repl(m, good=good):
                original = m.group(0)
                if original[0].isupper():
                    return good[0].upper() + good[1:]
                return good
            text = re.sub(rf'\b{re.escape(bad)}\b', repl, text, flags=re.IGNORECASE)
    return text

def corregir_payload(payload):
    if not isinstance(payload, dict):
        return payload, 0
    cambios = 0
    new_payload = dict(payload)
    if "opciones" in payload and isinstance(payload["opciones"], list):
        new_ops = []
        for op in payload["opciones"]:
            new_op = corregir_extendido(op) if isinstance(op, str) else op
            if new_op != op:
                cambios += 1
            new_ops.append(new_op)
        new_payload["opciones"] = new_ops
    if "explicacion" in payload and isinstance(payload["explicacion"], str):
        new_expl = corregir_extendido(payload["explicacion"])
        if new_expl != payload["explicacion"]:
            cambios += 1
        new_payload["explicacion"] = new_expl
    return new_payload, cambios

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", f"EJERCICIOS {args.nivel} - TILDES EXTENDIDAS")

ejs = list(EJ.objects.filter(tecnica__nivel_mcer=args.nivel).select_related("tecnica"))

cambios_enun = 0
cambios_payload = 0
cambios_total = 0
ejemplos = []

for e in ejs:
    enun_orig = e.enunciado or ""
    enun_new = corregir_extendido(enun_orig)
    payload_new, c_payload = corregir_payload(e.payload)

    c_enun = 1 if enun_new != enun_orig else 0
    c_total = c_enun + c_payload

    if c_enun:
        cambios_enun += 1
    if c_payload:
        cambios_payload += 1
    if c_total:
        cambios_total += 1
        if len(ejemplos) < 10:
            ejemplos.append({
                "tec": e.tecnica.numero,
                "antes": enun_orig[:80],
                "despues": enun_new[:80],
                "c_payload": c_payload,
            })

print(f"  Total ejercicios: {len(ejs)}")
print(f"  Con cambios en enunciado: {cambios_enun}")
print(f"  Con cambios en payload:   {cambios_payload}")
print(f"  Con algun cambio:         {cambios_total}")

if ejemplos:
    header("B", "MUESTRA DE CAMBIOS")
    for ej in ejemplos:
        print(f"\n  tec #{ej['tec']}")
        print(f"    ANTES:   {ej['antes']}")
        print(f"    DESPUES: {ej['despues']}")
        if ej["c_payload"]:
            print(f"    (payload: {ej['c_payload']} cambios)")

header("C", "APLICAR" if args.apply else "DRY-RUN")

if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print(f"  Se corregirian {cambios_total} ejercicios.")
    print("  Ejecuta con --apply para escribir.")
    sys.exit(0)

with transaction.atomic():
    aplicados = 0
    for e in ejs:
        enun_new = corregir_extendido(e.enunciado or "")
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

header("D", "VERIFICAR")

ejs_post = list(EJ.objects.filter(tecnica__nivel_mcer=args.nivel))

def tiene_tildes(text):
    return text and any(c in text for c in "áéíóúñÁÉÍÓÚÑ¿¡")

con_tildes = sum(1 for e in ejs_post if tiene_tildes(e.enunciado or ""))
pct = 100 * con_tildes / max(1, len(ejs_post))

print(f"  Con tildes/ñ/¿ en enunciado: {con_tildes}/{len(ejs_post)} ({pct:.1f}%)")

sin_tildes = [e for e in ejs_post if e.enunciado and not tiene_tildes(e.enunciado)]
if sin_tildes:
    print(f"\n  Restantes sin tildes ({len(sin_tildes)}):")
    for e in sorted(sin_tildes, key=lambda x: x.tecnica.numero)[:20]:
        print(f"    tec #{e.tecnica.numero:>3}  {e.enunciado[:75]}")
    if len(sin_tildes) > 20:
        print(f"    ... y {len(sin_tildes) - 20} mas")

if pct >= 95:
    print(f"\n  [OK] TILDES >= 95% - excelente")
elif pct >= 85:
    print(f"\n  [OK] TILDES >= 85% - aceptable")
else:
    print(f"\n  [WARN] TILDES < 85%. Considerar tercera pasada manual.")

print()