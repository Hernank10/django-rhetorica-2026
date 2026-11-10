"""_fix_tildes_a2_p3.py - Tercera pasada: preguntas sin ¿ inicial + que→qué contextual."""
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

# Palabras interrogativas que llevan tilde cuando introducen pregunta
INTERR = {"que": "qué", "quien": "quién", "quienes": "quiénes",
          "cual": "cuál", "cuales": "cuáles",
          "donde": "dónde", "cuando": "cuándo", "como": "cómo",
          "cuanto": "cuánto", "cuanta": "cuánta",
          "cuantos": "cuántos", "cuantas": "cuántas"}

# Verbos/palabras que faltan (del diagnostico de 21)
EXTRA = {
    "salto": "saltó", "implica": "implica",  # ya OK
    "persona": "persona",  # ya OK
    # Solo palabras que aun no estan acentuadas
    "dialogo": "diálogo",
    "movil": "móvil",
    "informacion": "información",
}

def tiene_tildes(text):
    return text and any(c in text for c in "áéíóúñÁÉÍÓÚÑ¿¡")

def corregir_p3(text):
    if not text:
        return text

    # 1. "que" aislado tras coma o al inicio de subordinada → "qué"
    #    Cubre: ", que implica", ", que sugiere", ", que se infiere",
    #           ", que palabras indican", ", que efecto tiene"
    text = re.sub(r',\s+que\b', ', qué', text)
    # Al inicio de la frase si es "que..." tras contexto
    text = re.sub(r'^(que)\b', 'qué', text, flags=re.IGNORECASE)

    # 2. Si la frase termina en ? y NO empieza por ¿ → añadir ¿
    stripped = text.strip()
    if stripped.endswith("?") and not stripped.startswith("¿"):
        # Excepcion: si ya empieza por palabra interrogativa con tilde, no tocar
        first_word = re.match(r'^([A-Za-zÁÉÍÓÚÑáéíóúñ]+)', stripped)
        if first_word:
            fw = first_word.group(1)
            # ¿Qué, ¿Cuál, ¿Cómo... ya tienen tilde → solo añadir ¿
            if fw.lower() in INTERR or fw.lower() in INTERR.values():
                text = "¿" + stripped
            else:
                # Frase tipo "El texto es claro?" → ¿ al inicio
                text = "¿" + stripped

    # 3. Palabras extra
    for bad, good in EXTRA.items():
        if bad == good:
            continue
        text = re.sub(rf'\b{re.escape(bad)}\b',
                      lambda m, g=good: g[0].upper() + g[1:] if m.group(0)[0].isupper() else g,
                      text, flags=re.IGNORECASE)

    return text

def corregir_payload(payload):
    if not isinstance(payload, dict):
        return payload, 0
    cambios = 0
    new_payload = dict(payload)
    if "opciones" in payload and isinstance(payload["opciones"], list):
        new_ops = []
        for op in payload["opciones"]:
            new_op = corregir_p3(op) if isinstance(op, str) else op
            if new_op != op:
                cambios += 1
            new_ops.append(new_op)
        new_payload["opciones"] = new_ops
    if "explicacion" in payload and isinstance(payload["explicacion"], str):
        new_expl = corregir_p3(payload["explicacion"])
        if new_expl != payload["explicacion"]:
            cambios += 1
        new_payload["explicacion"] = new_expl
    return new_payload, cambios

ejs = list(EJ.objects.filter(tecnica__nivel_mcer=args.nivel).select_related("tecnica"))
sin_tildes = [e for e in ejs if e.enunciado and not tiene_tildes(e.enunciado)]

print(f"=== P3 TILDES: {len(sin_tildes)} ejercicios a corregir ===\n")

a_migrar = []
for e in sin_tildes:
    nuevo = corregir_p3(e.enunciado)
    payload_nuevo, c_payload = corregir_payload(e.payload)
    if nuevo != e.enunciado or c_payload:
        a_migrar.append((e, nuevo, payload_nuevo, c_payload))
        print(f"  tec #{e.tecnica.numero:>3}")
        print(f"    ANTES:   {e.enunciado[:75]}")
        print(f"    DESPUES: {nuevo[:75]}")

print(f"\n  A corregir: {len(a_migrar)}")

if not args.apply:
    print("\n  DRY-RUN. --apply para escribir.")
    sys.exit(0)

with transaction.atomic():
    aplicados = 0
    for e, nuevo_enun, nuevo_payload, _ in a_migrar:
        campos = []
        if nuevo_enun != e.enunciado:
            e.enunciado = nuevo_enun
            campos.append("enunciado")
        if nuevo_payload != e.payload:
            e.payload = nuevo_payload
            campos.append("payload")
        if campos:
            e.save(update_fields=campos)
            aplicados += 1
    print(f"\n  [OK] {aplicados} ejercicios corregidos")

# Verificar final
ejs_post = list(EJ.objects.filter(tecnica__nivel_mcer=args.nivel))
con_tildes = sum(1 for e in ejs_post if tiene_tildes(e.enunciado or ""))
pct = 100 * con_tildes / max(1, len(ejs_post))
print(f"\n  Con tildes: {con_tildes}/{len(ejs_post)} ({pct:.1f}%)")

restantes = [e for e in ejs_post if e.enunciado and not tiene_tildes(e.enunciado)]
if restantes:
    print(f"  Restantes: {len(restantes)}")
    for e in restantes[:10]:
        print(f"    tec #{e.tecnica.numero}: {e.enunciado[:70]}")