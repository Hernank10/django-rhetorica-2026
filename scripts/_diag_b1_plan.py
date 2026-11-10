"""_diag_b1_plan.py - Diagnostico completo del nivel + plan de sprint automatico.

Read-only. Mide todo lo necesario para decidir el tipo de sprint:
  - Textos en rango / fuera
  - Coherencia real (con whitelist de meta-preguntas)
  - Payload: opciones, correcta, explicacion
  - Tildes / ñ / ¿
  - Sobrecargas
  - Rubrica v2 desglosada

Genera un plan JSON con las fases necesarias y un veredicto:
  LIGERO  = solo tildes + explicacion
  MEDIO   = F1 + F2 + F3a + F3b + tildes
  DURO    = reset completo (como A2)

Uso:
    python scripts/_diag_b1_plan.py                    # default B1
    python scripts/_diag_b1_plan.py --nivel B2
    python scripts/_diag_b1_plan.py --nivel B1 --json  # guarda docs/plan_b1.json
"""
import os, sys, re, json, argparse
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--nivel", default="B1")
parser.add_argument("--json", action="store_true", help="Guardar JSON en docs/")
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

RANGOS = {
    "A1": (60, 100), "A2": (100, 200), "B1": (180, 350),
    "B2": (300, 500), "C1": (450, 700), "C2": (700, 1200),
}

# ─── Helpers ────────────────────────────────────────────────

def wc(text):
    if not text: return 0
    text = re.sub(r"<[^>]+>", " ", str(text))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

def tiene_tildes(text):
    if not text: return False
    return any(c in text for c in "áéíóúñÁÉÍÓÚÑ¿¡")

STOPWORDS = {
    "para","como","porque","cuando","donde","sobre","entre","desde","hasta",
    "segun","texto","oracion","frase","palabra","palabras","siguiente",
    "correcta","incorrecta","verdadera","falsa","dice","menciona","aparece",
    "indica","significa","cual","como","que","quien","donde","cuando","por",
    "con","los","las","una","uno","del","este","esta","estos","estas","mas",
    "pero","hace","hizo","sido","tiene","tenia",
}

def tokens(text):
    if not text: return set()
    text = str(text).lower()
    words = re.findall(r"\b[a-záéíóúñü]+\b", text)
    return {w for w in words if len(w) > 4 and w not in STOPWORDS}

META_PATTERNS = [
    r"en el texto", r"del texto", r"seg[uú]n el texto",
    r"el texto (es|tiene|dice|trata|presenta|sigue|esta|usa|menciona)",
    r"(cu[aá]l es|cu[aá]les son) (el|la|los|las) (tema|t[ií]tulo|idea|conclusi[oó]n|estructura|prop[oó]sito|tesis|argumento|tono|narrador|escenario|funci[oó]n|papel|marcador)",
    r"de qu[eé] trata", r"qu[eé] tipo de (texto|estructura|lenguaje)",
    r"cu[aá]l de estas (frases|palabras|afirmaciones|opciones|parejas)",
    r"como (esta|se) (organizada|estructura|narra|comunica|relacionan)",
    r"que (marcador|palabras|elementos|frases)",
    r"hay (alguna|algun|conflicto|ironia|dialogo|personificacion|dialogos|ironias)",
    r"(para qu[eé]|con qu[eé] (prop[oó]sito|intenci[oó]n|finalidad))",
    r"(cu[aá]l es el prop[oó]sito|cu[aá]l es la intenci[oó]n)",
    r"cu[aá]l de estos",
    r"(cu[aá]l es|cu[aá]les son) (el|la|los|las) ",
]

def es_meta_pregunta(enun):
    if not enun: return False
    e = enun.lower()
    return any(re.search(p, e) for p in META_PATTERNS)

def coherencia_metrica(ej):
    if not ej.texto_id or not ej.enunciado:
        return 0, 0
    tx = TX.objects.filter(id=ej.texto_id).first()
    if not tx: return 0, 0
    if es_meta_pregunta(ej.enunciado):
        return 2, 2  # forzar coherente
    tx_tokens = tokens(tx.cuerpo)
    enun_tokens = tokens(ej.enunciado)
    expl_tokens = tokens(ej.payload.get("explicacion", "") if isinstance(ej.payload, dict) else "")
    combined = enun_tokens | expl_tokens
    return len(tx_tokens & combined), len(tx_tokens)

# ─── Rúbrica v2 ─────────────────────────────────────────────

def score_align(tx_id, nivel):
    tx = TX.objects.filter(id=tx_id).first() if tx_id else None
    if not tx: return 1
    w = wc(tx.cuerpo)
    lo, hi = RANGOS.get(nivel, (60, 100))
    if lo <= w <= hi: return 5
    if lo * 0.7 <= w < lo or hi < w <= hi * 1.3: return 3
    return 2

def score_clarity(enun):
    if not enun: return 1
    e = enun.lower(); largo = len(enun)
    verbos = {"localiza","identifica","infiere","deduce","reconoce","distingue",
              "diferencia","clasifica","busca","encuentra","compara","analiza",
              "explica","justifica","interpreta","evalua","relaciona"}
    tiene_verbo = any(v in e for v in verbos)
    genericos = ["¿el texto es claro?", "¿qué opina?"]
    es_generico = any(g in e for g in genericos)
    pregunta_concreta = any(e.startswith(p) for p in [
        "¿por qué","¿quién","¿qué significa","¿dónde","¿cuándo","¿cómo",
        "¿cuál","¿qué se puede inferir","¿qué intención",
    ])
    if es_generico and not tiene_verbo: return 2
    if tiene_verbo and 30 <= largo <= 250: return 5
    if pregunta_concreta and 20 <= largo <= 250: return 4
    if largo < 20: return 2
    return 3

def score_distractors(payload):
    if not isinstance(payload, dict) or "opciones" not in payload: return 1
    ops = payload.get("opciones", [])
    if len(ops) not in (3, 4): return 2
    largos = [len(str(o)) for o in ops]
    diff = max(largos) - min(largos)
    if diff <= 30: return 5
    if diff <= 60: return 4
    return 2

def score_justification(payload):
    if not isinstance(payload, dict): return 1
    return 5 if payload.get("explicacion") else 2

# ─── Diagnóstico ────────────────────────────────────────────

nivel = args.nivel
lo, hi = RANGOS.get(nivel, (60, 100))

textos = list(TX.objects.filter(nivel_mcer=nivel).order_by("id"))
tecnicas = list(TL.objects.filter(nivel_mcer=nivel))
ejs = list(EJ.objects.filter(tecnica__nivel_mcer=nivel).select_related("tecnica", "texto"))

# 1. Textos
textos_info = []
en_rango_count = 0
for t in textos:
    w = wc(t.cuerpo)
    ok = lo <= w <= hi
    if ok: en_rango_count += 1
    textos_info.append({
        "id": t.id, "titulo": t.titulo, "palabras": w, "en_rango": ok,
        "accion": None if ok else ("reescribir_acortar" if w > hi else "reescribir_ampliar"),
    })

# 2. Ejercicios por técnica
tec_count = Counter(e.tecnica_id for e in ejs)
tec_0 = sum(1 for t in tecnicas if tec_count.get(t.id, 0) == 0)
tec_1 = sum(1 for t in tecnicas if tec_count.get(t.id, 0) == 1)
tec_2m = sum(1 for t in tecnicas if tec_count.get(t.id, 0) >= 2)
ratio = len(ejs) / max(1, len(tecnicas))

# 3. Coherencia
coherentes = 0
incoherentes_lista = []
for e in ejs:
    n_match, n_tx = coherencia_metrica(e)
    if n_match >= 1:
        coherentes += 1
    else:
        incoherentes_lista.append({
            "id": e.id, "tec": e.tecnica.numero, "proceso": e.tecnica.proceso,
            "enun": (e.enunciado or "")[:70],
            "texto": e.texto.titulo[:30] if e.texto else None,
        })
pct_coh = 100 * coherentes / max(1, len(ejs))

# 4. Payload
con_opciones = sum(1 for e in ejs if isinstance(e.payload, dict) and "opciones" in e.payload)
con_correcta = sum(1 for e in ejs if isinstance(e.payload, dict) and e.payload.get("correcta"))
con_explicacion = sum(1 for e in ejs if isinstance(e.payload, dict) and e.payload.get("explicacion"))

# 5. Tildes
con_tildes = sum(1 for e in ejs if tiene_tildes(e.enunciado or ""))
sin_tildes_lista = [
    {"tec": e.tecnica.numero, "enun": (e.enunciado or "")[:60]}
    for e in ejs if e.enunciado and not tiene_tildes(e.enunciado)
]

# 6. Sobrecargas
tec_por_texto = defaultdict(set)
for e in ejs:
    if e.texto_id:
        tec_por_texto[e.texto_id].add(e.tecnica_id)
sobrecargados = sum(1 for s in tec_por_texto.values() if len(s) > 15)
textos_vacios = [t.id for t in textos if len(tec_por_texto.get(t.id, set())) == 0]

# 7. Rúbrica
reales = ejs  # sin placeholders detectados en B1, asumir todos reales
sc_al = [score_align(e.texto_id, nivel) for e in reales]
sc_cl = [score_clarity(e.enunciado) for e in reales]
sc_di = [score_distractors(e.payload) for e in reales]
sc_ju = [score_justification(e.payload) for e in reales]
prom = lambda lst: sum(lst)/len(lst) if lst else 0
prom_global = (prom(sc_al)+prom(sc_cl)+prom(sc_di)+prom(sc_ju))/4
bajos = sum(1 for i in range(len(reales))
            if (sc_al[i]+sc_cl[i]+sc_di[i]+sc_ju[i])/4 < 3.5)

# 8. Plan
plan = {
    "f1_textos": {
        "necesario": len(textos) < 10 or en_rango_count < len(textos),
        "textos_actuales": len(textos),
        "en_rango": en_rango_count,
        "fuera": [{"id": t["id"], "palabras": t["palabras"], "accion": t["accion"]}
                  for t in textos_info if not t["en_rango"]],
        "faltantes_para_10": max(0, 10 - len(textos)),
    },
    "f2_mapeo": {
        "necesario": sobrecargados > 0 or len(textos_vacios) > 0,
        "sobrecargados": sobrecargados,
        "vacios": textos_vacios,
    },
    "f3a_explicacion": {
        "necesario": con_explicacion < len(ejs),
        "faltan": len(ejs) - con_explicacion,
    },
    "f3b_densificar": {
        "necesario": ratio < 2.0,
        "ratio_actual": round(ratio, 2),
        "ejercicios_actuales": len(ejs),
        "faltan_para_2.00": max(0, len(tecnicas) * 2 - len(ejs)),
    },
    "f3c_tildes": {
        "necesario": con_tildes < len(ejs) * 0.95,
        "con_tildes": con_tildes,
        "sin_tildes": len(ejs) - con_tildes,
    },
    "f4_rubrica": {
        "actual": round(prom_global, 2),
        "objetivo": 4.0,
        "bajos_3_5": bajos,
    },
}

# 9. Veredicto
if pct_coh < 70:
    tipo_sprint = "DURO"
    razon = f"Coherencia {pct_coh:.0f}% < 70% -> reset completo (como A2)"
elif pct_coh >= 85 and en_rango_count >= 8 and ratio >= 1.8:
    tipo_sprint = "LIGERO"
    razon = f"Coherencia {pct_coh:.0f}% alta, textos OK, ratio OK -> solo tildes + explicacion"
else:
    tipo_sprint = "MEDIO"
    razon = f"Coherencia {pct_coh:.0f}%, {en_rango_count}/{len(textos)} textos OK, ratio {ratio:.2f} -> F1+F2+F3a+F3b+tildes"

# ─── Print ──────────────────────────────────────────────────

def header(t):
    print(); print("=" * 78); print(f"  {t}"); print("=" * 78)

print()
print("=" * 78)
print(f"  DIAGNOSTICO {nivel} - PLAN DE SPRINT")
print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 78)

header(f"1. TEXTOS ({len(textos)} total, rango {lo}-{hi} palabras)")
for t in textos_info:
    icon = "OK " if t["en_rango"] else "FUERA"
    accion = f" -> {t['accion']}" if t["accion"] else ""
    print(f"  [{icon}] id={t['id']:>3}  {t['palabras']:>4}w  {t['titulo'][:45]}{accion}")
print(f"\n  En rango: {en_rango_count}/{len(textos)}")

header(f"2. EJERCICIOS Y RATIO")
print(f"  Total ejercicios: {len(ejs)}")
print(f"  Tecnicas: {len(tecnicas)}")
print(f"  Con 0 ej: {tec_0}  Con 1 ej: {tec_1}  Con 2+: {tec_2m}")
print(f"  Ratio: {ratio:.2f}  (objetivo 2.00)")

header(f"3. COHERENCIA (con whitelist)")
print(f"  Coherentes: {coherentes}/{len(ejs)} ({pct_coh:.1f}%)")
print(f"  Incoherentes: {len(incoherentes_lista)}")
if incoherentes_lista[:5]:
    print(f"\n  Primeros 5 incoherentes reales:")
    for inc in incoherentes_lista[:5]:
        print(f"    tec #{inc['tec']:>3} [{inc['proceso']}] {inc['enun']}")
        print(f"           texto: {inc['texto']}")

header(f"4. PAYLOAD")
print(f"  Con 'opciones':    {con_opciones}/{len(ejs)}")
print(f"  Con 'correcta':    {con_correcta}/{len(ejs)}")
print(f"  Con 'explicacion': {con_explicacion}/{len(ejs)}")

header(f"5. TILDES / ñ / ¿")
print(f"  Con tildes: {con_tildes}/{len(ejs)} ({100*con_tildes/max(1,len(ejs)):.1f}%)")
if sin_tildes_lista[:5]:
    print(f"\n  Primeros 5 sin tildes:")
    for s in sin_tildes_lista[:5]:
        print(f"    tec #{s['tec']:>3}  {s['enun']}")

header(f"6. SOBRECARGAS Y MAPEO")
print(f"  Textos sobrecargados (>15 tec): {sobrecargados}")
print(f"  Textos vacios (0 tec): {len(textos_vacios)}")
if textos_vacios:
    print(f"    IDs: {textos_vacios}")

header(f"7. RUBRICA v2")
print(f"  A1_align:      {prom(sc_al):.2f}/5")
print(f"  claridad:      {prom(sc_cl):.2f}/5")
print(f"  distractores:  {prom(sc_di):.2f}/5")
print(f"  justificacion: {prom(sc_ju):.2f}/5")
print(f"  PROMEDIO:      {prom_global:.2f}/5  (objetivo >= 4.0)")
print(f"  Ejercicios < 3.5: {bajos}/{len(ejs)}")

header("PLAN DE SPRINT")
f1 = plan["f1_textos"]; f2 = plan["f2_mapeo"]; f3a = plan["f3a_explicacion"]
f3b = plan["f3b_densificar"]; f3c = plan["f3c_tildes"]
print(f"  F1 textos:        {'NECESARIO' if f1['necesario'] else 'skip'}  "
      f"({f1['textos_actuales']} actuales, {f1['en_rango']} en rango, +{f1['faltantes_para_10']} faltan)")
print(f"  F2 mapeo:         {'NECESARIO' if f2['necesario'] else 'skip'}  "
      f"({f2['sobrecargados']} sobrecargados, {len(f2['vacios'])} vacios)")
print(f"  F3a explicacion:  {'NECESARIO' if f3a['necesario'] else 'skip'}  "
      f"(faltan {f3a['faltan']})")
print(f"  F3b densificar:   {'NECESARIO' if f3b['necesario'] else 'skip'}  "
      f"(ratio {f3b['ratio_actual']} -> 2.00, faltan {f3b['faltan_para_2.00']})")
print(f"  F3c tildes:       {'NECESARIO' if f3c['necesario'] else 'skip'}  "
      f"(sin tildes: {f3c['sin_tildes']})")
print(f"  F4 rubrica:       {plan['f4_rubrica']['actual']} -> 4.0")

header(f"VEREDICTO: SPRINT {tipo_sprint}")
print(f"  {razon}")
print()

# ─── JSON ──────────────────────────────────────────────────

resultado = {
    "nivel": nivel,
    "fecha": datetime.now().isoformat(),
    "rango": f"{lo}-{hi}",
    "textos": {"total": len(textos), "en_rango": en_rango_count, "info": textos_info},
    "ejercicios": {
        "total": len(ejs), "tecnicas": len(tecnicas),
        "tec_0": tec_0, "tec_1": tec_1, "tec_2m": tec_2m,
        "ratio": round(ratio, 2),
    },
    "coherencia": {
        "coherentes": coherentes, "pct": round(pct_coh, 1),
        "incoherentes": incoherentes_lista[:50],  # limitar a 50
    },
    "payload": {
        "con_opciones": con_opciones, "con_correcta": con_correcta,
        "con_explicacion": con_explicacion,
    },
    "tildes": {"con_tildes": con_tildes, "sin_tildes": len(ejs) - con_tildes},
    "sobrecargas": {"sobrecargados": sobrecargados, "vacios": textos_vacios},
    "rubrica": {
        "a1_align": round(prom(sc_al), 2),
        "claridad": round(prom(sc_cl), 2),
        "distractores": round(prom(sc_di), 2),
        "justificacion": round(prom(sc_ju), 2),
        "promedio": round(prom_global, 2),
        "bajos_3_5": bajos,
    },
    "plan": plan,
    "veredicto": {"tipo_sprint": tipo_sprint, "razon": razon},
}

if args.json:
    path = ROOT / "docs" / f"plan_{nivel.lower()}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    print(f"  [OK] JSON guardado: {path}")
    print(f"  Siguiente: el maestro leera este JSON para orquestar fases.")
    print()
else:
    print("  Para guardar JSON: python scripts/_diag_b1_plan.py --nivel B1 --json")
    print()