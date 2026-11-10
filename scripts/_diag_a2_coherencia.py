"""_diag_a2_coherencia.py - Mide coherencia semantica enunciado<->texto asignado.

Heuristica: extrae palabras significativas (>4 chars) del texto, cuenta cuantas
aparecen en el enunciado del ejercicio. Score 0 = probable incoherencia.
"""
import os, sys, re, argparse
from pathlib import Path
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--nivel", default="A2")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps

EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

STOPWORDS = {
    "para", "como", "porque", "cuando", "donde", "sobre", "entre", "desde",
    "hasta", "según", "según", "texto", "oración", "frase", "palabra", "palabras",
    "siguiente", "siguientes", "correcta", "incorrecta", "verdadera", "falsa",
    "dice", "menciona", "aparece", "indica", "significa", "cuál", "cómo",
    "qué", "quién", "dónde", "cuándo", "por", "con", "los", "las", "una",
    "uno", "del", "que", "este", "esta", "estos", "estas", "más", "pero",
}

def tokens(text):
    if not text: return set()
    text = str(text).lower()
    words = re.findall(r"\b[a-záéíóúñü]+\b", text)
    return {w for w in words if len(w) > 4 and w not in STOPWORDS}

def coherencia(ej):
    """Score 0-N de tokens del texto que aparecen en el enunciado."""
    if not ej.texto_id or not ej.enunciado:
        return 0, 0
    tx = TX.objects.filter(id=ej.texto_id).first()
    if not tx: return 0, 0
    tx_tokens = tokens(tx.cuerpo)
    enun_tokens = tokens(ej.enunciado)
    matches = tx_tokens & enun_tokens
    return len(matches), len(tx_tokens)

# ── Diagnostico ──
ejs = list(EJ.objects.filter(tecnica__nivel_mcer=args.nivel)
           .select_related("tecnica", "texto")
           .order_by("tecnica__numero", "orden"))

print(f"=== COHERENCIA {args.nivel}: {len(ejs)} ejercicios ===\n")

buckets = {"incoherente": [], "debil": [], "ok": []}
for e in ejs:
    n_match, n_tx = coherencia(e)
    if n_match == 0:
        buckets["incoherente"].append((e, n_match, n_tx))
    elif n_match <= 1:
        buckets["debil"].append((e, n_match, n_tx))
    else:
        buckets["ok"].append((e, n_match, n_tx))

print(f"  Incoherentes (0 matches):    {len(buckets['incoherente']):>3}")
print(f"  Debiles (1 match):           {len(buckets['debil']):>3}")
print(f"  Coherentes (2+ matches):     {len(buckets['ok']):>3}")
print(f"  TOTAL:                       {len(ejs):>3}")

if args.verbose:
    for cat in ("incoherente", "debil"):
        print(f"\n--- {cat.upper()} ({len(buckets[cat])}) ---")
        for e, m, t in buckets[cat][:20]:
            tx_titulo = e.texto.titulo[:30] if e.texto else "(sin texto)"
            print(f"  #{e.tecnica.numero:>3} texto={tx_titulo}")
            print(f"       enunciado: {e.enunciado[:70]}")
            print(f"       matches={m}/{t}")

# Muestra de los primeros 10 incoherentes (siempre)
print(f"\n=== MUESTRA DE INCOHERENTES (primeros 10) ===")
for e, m, t in buckets["incoherente"][:10]:
    tx_titulo = e.texto.titulo[:30] if e.texto else "(sin texto)"
    print(f"\n  tec #{e.tecnica.numero:>3} [{e.tecnica.proceso}] texto='{tx_titulo}'")
    print(f"    enunciado: {e.enunciado[:80]}")

print(f"\n  Proximo paso sugerido:")
n_incoh = len(buckets["incoherente"]) + len(buckets["debil"])
if n_incoh == 0:
    print(f"    Todo coherente. Puedes densificar.")
elif n_incoh < 20:
    print(f"    {n_incoh} ejercicios a reescribir. Factible.")
else:
    print(f"    {n_incoh} ejercicios rotos. Considera rehacer A2 desde cero.")