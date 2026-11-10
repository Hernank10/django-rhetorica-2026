"""_diag_fases_contenido_v2.py - Diagnostico de contenido con rubric multi-nivel.

Reemplaza _diag_fases_contenido.py corrigiendo 2 sesgos:
  1. A1_align usa rangos reales por nivel (no 60-100 para todos)
  2. distractores acepta 3 O 4 opciones (A2-C2 usan 4)
  3. claridad premia verbos de proceso y penaliza genericos

Uso:
    python scripts/_diag_fases_contenido_v2.py
    python scripts/_diag_fases_contenido_v2.py --solo A2
    python scripts/_diag_fases_contenido_v2.py --todos
"""
import os, sys, re, argparse
from pathlib import Path
from collections import Counter, defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--solo", default=None, help="Diagnosticar solo un nivel (A1..C2)")
parser.add_argument("--todos", action="store_true", help="Diagnosticar los 6 niveles")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

# Rangos de palabras por nivel MCER
RANGOS = {
    "A1": (60, 100),
    "A2": (100, 200),
    "B1": (180, 350),
    "B2": (300, 500),
    "C1": (450, 700),
    "C2": (700, 1200),
}

if args.todos:
    NIVELES = ["A1", "A2", "B1", "B2", "C1", "C2"]
elif args.solo:
    if args.solo not in RANGOS:
        print(f"[ERROR] Nivel invalido: {args.solo}. Validos: {list(RANGOS.keys())}")
        sys.exit(1)
    NIVELES = [args.solo]
else:
    NIVELES = ["A2"]  # default: solo A2 (el nivel del sprint actual)

PLACEHOLDER_PATTERNS = [
    r"\(repaso\)",
    r"^¿A qué técnica corresponde",
    r"corresponde esta descripción",
]

def es_placeholder(enunciado):
    if not enunciado:
        return False
    return any(re.search(p, enunciado, re.I) for p in PLACEHOLDER_PATTERNS)

def wc(text):
    if not text:
        return 0
    text = re.sub(r"<[^>]+>", " ", str(text))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

# ─── SCORING v2 ─────────────────────────────────────────────

def score_align(tx_id, nivel):
    """A1_align con rango real por nivel."""
    tx = TX.objects.filter(id=tx_id).first() if tx_id else None
    if not tx: return 1
    w = wc(tx.cuerpo)
    lo, hi = RANGOS[nivel]
    if lo <= w <= hi: return 5
    if lo * 0.7 <= w < lo or hi < w <= hi * 1.3: return 3
    return 2

def score_clarity(enunciado):
    """Claridad: premia verbos de proceso, penaliza genericos."""
    if not enunciado: return 1
    e = enunciado.lower()
    largo = len(enunciado)

    # Verbos especificos de tarea
    verbos_especificos = {
        "localiza", "localizar", "identifica", "identificar",
        "infiere", "inferir", "deduce", "deducir",
        "reconoce", "reconocer", "distingue", "distinguir",
        "diferencia", "diferenciar", "clasifica", "clasificar",
        "busca", "buscar", "encuentra", "encontrar",
        "compara", "comparar", "analiza", "analizar",
        "explica", "explicar", "justifica", "justificar",
    }
    tiene_verbo = any(v in e for v in verbos_especificos)

    # Penalizacion por genericos
    genericos = ["¿el texto es claro?", "¿qué opina?", "según el texto,"]
    es_generico = any(g in e for g in genericos)

    # Enunciados que preguntan algo concreto (con 'por qué', 'quién', 'dónde', etc.)
    pregunta_concreta = any(e.startswith(p) for p in [
        "¿por qué", "¿quién", "¿qué significa", "¿dónde", "¿cuándo",
        "¿cómo", "¿cuál", "¿qué se puede inferir", "¿qué intención",
    ])

    if es_generico and not tiene_verbo:
        return 2
    if tiene_verbo and 30 <= largo <= 250:
        return 5
    if pregunta_concreta and 20 <= largo <= 250:
        return 4
    if largo < 20:
        return 2
    return 3

def score_distractors(payload):
    """Acepta 3 O 4 opciones bien formadas."""
    if not isinstance(payload, dict) or "opciones" not in payload:
        return 1
    ops = payload.get("opciones", [])
    n = len(ops)
    if n not in (3, 4):
        return 2
    largos = [len(str(o)) for o in ops]
    diff = max(largos) - min(largos)
    # A2-C2 aceptan opciones mas largas (frases), umbral mas generoso
    if diff <= 30: return 5
    if diff <= 60: return 4
    return 2

def score_justification(payload):
    if not isinstance(payload, dict): return 1
    return 5 if payload.get("explicacion") else 2

# ─── DIAGNOSTICO ────────────────────────────────────────────

resumen = {}

for nivel in NIVELES:
    header(nivel, f"NIVEL {nivel}")

    textos = list(TX.objects.filter(nivel_mcer=nivel).order_by("id"))
    tecnicas = list(TL.objects.filter(nivel_mcer=nivel))
    ejs = list(EJ.objects.filter(tecnica__nivel_mcer=nivel).select_related("tecnica"))

    lo, hi = RANGOS[nivel]
    print(f"  Rango objetivo: {lo}-{hi} palabras")

    # Textos
    print(f"\n  --- TEXTOS ({len(textos)}) ---")
    en_rango = 0
    for t in textos:
        w = wc(t.cuerpo)
        ok = lo <= w <= hi
        en_rango += int(ok)
        print(f"  [{'OK ' if ok else 'FUERA'}] id={t.id:>3}  {t.titulo[:40]:<40}  {w:>4}w")
    print(f"  En rango {lo}-{hi}: {en_rango}/{len(textos)}")

    # Tecnicas y ejercicios
    por_tec = Counter(e.tecnica_id for e in ejs)
    tec_0 = sum(1 for t in tecnicas if por_tec.get(t.id, 0) == 0)
    tec_1 = sum(1 for t in tecnicas if por_tec.get(t.id, 0) == 1)
    tec_2m = sum(1 for t in tecnicas if por_tec.get(t.id, 0) >= 2)
    ratio = len(ejs) / max(1, len(tecnicas))

    print(f"\n  --- TECNICAS / EJERCICIOS ---")
    print(f"  Tecnicas: {len(tecnicas)}   Ejercicios: {len(ejs)}")
    print(f"  Con 0 ej: {tec_0}   Con 1 ej: {tec_1}   Con 2+ ej: {tec_2m}")
    print(f"  Ratio: {ratio:.2f}  (objetivo 2.00)")

    # Placeholders
    ph = [e for e in ejs if es_placeholder(e.enunciado)]
    reales = [e for e in ejs if not es_placeholder(e.enunciado)]
    print(f"\n  --- PLACEHOLDERS ---")
    print(f"  Reales: {len(reales)}   Placeholders: {len(ph)}")

    # Mapeo
    tec_por_texto = defaultdict(set)
    for e in ejs:
        if e.texto_id:
            tec_por_texto[e.texto_id].add(e.tecnica_id)
    sobrecargados = sum(1 for s in tec_por_texto.values() if len(s) > 15)
    print(f"\n  --- MAPEO ---")
    print(f"  Textos sobrecargados (>15 tec): {sobrecargados}")

    # Rubrica
    if reales:
        sc_al = [score_align(e.texto_id, nivel) for e in reales]
        sc_cl = [score_clarity(e.enunciado) for e in reales]
        sc_di = [score_distractors(e.payload) for e in reales]
        sc_ju = [score_justification(e.payload) for e in reales]

        prom = lambda lst: sum(lst)/len(lst) if lst else 0
        prom_global = (prom(sc_al)+prom(sc_cl)+prom(sc_di)+prom(sc_ju))/4
        bajos = sum(1 for i in range(len(reales))
                    if (sc_al[i]+sc_cl[i]+sc_di[i]+sc_ju[i])/4 < 3.5)

        print(f"\n  --- RUBRICA v2 ({len(reales)} reales) ---")
        print(f"  A1_align:      {prom(sc_al):.2f}/5  (rango {lo}-{hi})")
        print(f"  claridad:      {prom(sc_cl):.2f}/5")
        print(f"  distractores:  {prom(sc_di):.2f}/5  (acepta 3-4 opciones)")
        print(f"  justificacion: {prom(sc_ju):.2f}/5")
        print(f"  PROMEDIO:      {prom_global:.2f}/5  (objetivo >= 4.0)")
        print(f"  Ejercicios < 3.5: {bajos}")
    else:
        prom_global = 0
        bajos = 0
        print(f"\n  --- RUBRICA ---")
        print(f"  Sin ejercicios reales")

    resumen[nivel] = {
        "textos": len(textos),
        "textos_ok": en_rango,
        "tecnicas": len(tecnicas),
        "ejercicios": len(ejs),
        "reales": len(reales),
        "ph": len(ph),
        "tec_0": tec_0,
        "tec_1": tec_1,
        "tec_2m": tec_2m,
        "ratio": ratio,
        "rubrica": prom_global,
        "bajos": bajos,
        "sobrecargados": sobrecargados,
        "rango": f"{lo}-{hi}",
    }

# ─── RESUMEN ───────────────────────────────────────────────

header("RESUMEN", f"{len(NIVELES)} NIVEL(ES) - RUBRIC v2")

print(f"\n  {'NIVEL':<6} {'RANGO':>10} {'TXT':>5} {'OK':>4} {'TEC':>5} {'EJ':>5} {'PH':>4} {'RATIO':>7} {'RUBR':>6} {'BAJ':>4} {'SOBR':>5}")
print(f"  {'-'*6} {'-'*10} {'-'*5} {'-'*4} {'-'*5} {'-'*5} {'-'*4} {'-'*7} {'-'*6} {'-'*4} {'-'*5}")
for nivel in NIVELES:
    r = resumen[nivel]
    print(f"  {nivel:<6} {r['rango']:>10} {r['textos']:>5} {r['textos_ok']:>4} "
          f"{r['tecnicas']:>5} {r['ejercicios']:>5} {r['ph']:>4} "
          f"{r['ratio']:>7.2f} {r['rubrica']:>6.2f} {r['bajos']:>4} {r['sobrecargados']:>5}")

# ─── PROXIMO PASO ─────────────────────────────────────────

print()
for nivel in NIVELES:
    r = resumen[nivel]
    print(f"  [{nivel}] ", end="")
    pends = []
    if r["rubrica"] < 4.0: pends.append(f"rubrica {r['rubrica']:.2f} < 4.0")
    if r["textos_ok"] < r["textos"]: pends.append(f"{r['textos'] - r['textos_ok']} textos fuera de rango")
    if r["ratio"] < 2.0: pends.append(f"ratio {r['ratio']:.2f} < 2.00 ({int(2*100 - r['ejercicios'])} ej faltantes)")
    if r["sobrecargados"] > 0: pends.append(f"{r['sobrecargados']} textos sobrecargados")
    if r["ph"] > 0: pends.append(f"{r['ph']} placeholders")

    if not pends:
        print("COMPLETO")
    else:
        print("; ".join(pends))

print()