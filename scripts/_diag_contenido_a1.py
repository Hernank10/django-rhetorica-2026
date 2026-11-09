"""_diag_contenido_a1.py - Auditoria del plan de contenido real A1 (ensayo instructivo).

Read-only. No modifica nada.
Cubre:
  A. Estado general A1
  B. Fase 1 - Curaduria de textos (10-12 textos, 60-100 palabras)
  C. Fase 2 - Mapeo texto <-> tecnica (sin sobrecarga)
  D. Fase 3 - Ejercicios reales vs placeholders
  E. Fase 4 - Rubrica automatica (parcial, con aviso de limites)
  F. KPIs del ensayo (seccion VII)
  G. Workflow CSV maestro (seccion VIII)
  H. Pilot + blindaje
  I. Riesgos del ensayo (seccion X)
  J. Veredicto: que fase esta completa, cual sigue
"""
import os, sys, re, json, argparse
from pathlib import Path
from collections import Counter, defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--log", default=None)
parser.add_argument("--sample", type=int, default=5, help="Ejercicios a puntuar en rubrica")
args, _ = parser.parse_known_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    for cand in ("django_retorica.settings.dev",
                 "django_retorica.settings.production",
                 "django_retorica.settings"):
        try:
            __import__(cand)
            os.environ["DJANGO_SETTINGS_MODULE"] = cand
            break
        except ImportError:
            continue

import django
django.setup()

from django.apps import apps
from django.conf import settings

OK, WARN, FAILS, INFO, TODO = [], [], [], [], []

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

def safe_get(name):
    try:
        return apps.get_model("core", name)
    except LookupError:
        return None

TL = safe_get("TecnicaLectura")
EJ = safe_get("EjercicioLectura")
TX = safe_get("Texto")

if not TL or not EJ or not TX:
    print("  [FAIL] modelos MCER incompletos"); sys.exit(1)

# ── Introspeccion defensiva ──────────────────────────────
tl_fields = {f.name: type(f).__name__ for f in TL._meta.get_fields() if hasattr(f, "name")}
tx_fields = {f.name: type(f).__name__ for f in TX._meta.get_fields() if hasattr(f, "name")}

# Detectar campo de contenido en Texto
def tx_content_field():
    for cand in ("contenido", "texto", "cuerpo", "contenido_texto", "cuerpo_texto"):
        if cand in tx_fields:
            return cand
    return None
TX_CONTENT = tx_content_field()

print(f"  TecnicaLectura fields: {list(tl_fields.keys())[:12]}")
print(f"  Texto fields:          {list(tx_fields.keys())[:12]}")
print(f"  Texto.contenido field: {TX_CONTENT or '[NO DETECTADO]'}")

# ═══════════════════════════════════════════════════════════
header("A", "ESTADO GENERAL A1")
# ═══════════════════════════════════════════════════════════
a1_tec_ids = list(TL.objects.filter(nivel_mcer="A1").values_list("id", flat=True))
a1_tec = list(TL.objects.filter(id__in=a1_tec_ids).order_by("numero"))
a1_ej_ids = list(EJ.objects.filter(tecnica_id__in=a1_tec_ids).values_list("id", flat=True))
a1_textos = list(TX.objects.filter(nivel_mcer="A1").order_by("id"))

print(f"  Tecnicas A1:   {len(a1_tec_ids)}")
print(f"  Ejercicios A1: {len(a1_ej_ids)}")
print(f"  Textos A1:     {len(a1_textos)}")

if a1_tec_ids:
    ratio = len(a1_ej_ids) / len(a1_tec_ids)
    print(f"  Ratio:         {ratio:.2f} ej/tec")

por_proceso = Counter(t.proceso for t in a1_tec)
print(f"  Por proceso:   {dict(por_proceso)}")

# ═══════════════════════════════════════════════════════════
header("B", "FASE 1 - CURADURIA DE TEXTOS (ensayo seccion III)")
# ═══════════════════════════════════════════════════════════
print(f"  Objetivo del ensayo: 10-12 textos, 60-100 palabras cada uno\n")
print(f"  Textos A1 actuales: {len(a1_textos)}")

def word_count(t):
    if not TX_CONTENT:
        return None
    raw = getattr(t, TX_CONTENT, "") or ""
    raw = re.sub(r"<[^>]+>", " ", raw)  # strip HTML si lo hay
    words = re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", raw)
    return len(words)

textos_info = []
for tx in a1_textos:
    wc = word_count(tx)
    status = "?"
    if wc is not None:
        if 60 <= wc <= 100:   status = "OK (rango)"
        elif wc < 60:         status = "CORTO (<60)"
        elif wc <= 130:       status = "LARGO (100-130)"
        else:                 status = "MUY LARGO (>130)"
    textos_info.append((tx.id, tx.titulo, wc, status))
    print(f"    id={tx.id:>3}  {tx.titulo[:50]:<50}  {str(wc):>4} palabras  [{status}]")

n_ok = sum(1 for _,_,_,s in textos_info if s.startswith("OK"))
print(f"\n  Textos en rango 60-100 palabras: {n_ok}/{len(a1_textos)}")

if len(a1_textos) < 10:
    faltan_txt = 10 - len(a1_textos)
    WARN.append(f"Fase 1 incompleta: faltan {faltan_txt} textos (objetivo 10-12)")
    TODO.append(f"Fase 1: escribir {faltan_txt} textos A1 mas (60-100 palabras cada uno)")
else:
    OK.append(f"Fase 1: {len(a1_textos)} textos (>= 10)")

if n_ok < len(a1_textos) * 0.7:
    WARN.append(f"Solo {n_ok}/{len(a1_textos)} textos en rango 60-100 palabras")

# ═══════════════════════════════════════════════════════════
header("C", "FASE 2 - MAPEO TEXTO <-> TECNICA (ensayo seccion IV.2)")
# ═══════════════════════════════════════════════════════════
print(f"  Objetivo: cada tecnica soportada por al menos 1 texto")
print(f"            ningun texto soporta mas de 15 tecnicas\n")

tec_por_texto = defaultdict(set)
texto_por_tec = defaultdict(set)
for ej in EJ.objects.filter(tecnica_id__in=a1_tec_ids).values("tecnica_id", "texto_id"):
    tid, txid = ej["tecnica_id"], ej["texto_id"]
    if txid:
        tec_por_texto[txid].add(tid)
        texto_por_tec[tid].add(txid)

print(f"  Texto  ->  #tecnicas distintas:")
for tx in a1_textos:
    n = len(tec_por_texto.get(tx.id, set()))
    marca = "OK" if n <= 15 else f"SOBRECARGA ({n})"
    print(f"    id={tx.id:>3}  {tx.titulo[:45]:<45}  {n:>3} tecnicas  [{marca}]")

tec_sin_texto = [t for t in a1_tec if t.id not in texto_por_tec]
print(f"\n  Tecnicas sin texto asociado: {len(tec_sin_texto)}")
if tec_sin_texto:
    for t in tec_sin_texto[:8]:
        print(f"    #{t.numero:>3}  {t.titulo[:60]}")
    if len(tec_sin_texto) > 8:
        print(f"    ... y {len(tec_sin_texto) - 8} mas")

if tec_sin_texto:
    WARN.append(f"Fase 2 incompleta: {len(tec_sin_texto)} tecnicas sin texto")
    TODO.append(f"Fase 2: mapear {len(tec_sin_texto)} tecnicas a textos del corpus")

sobrecargados = [(txid, len(tec_ids)) for txid, tec_ids in tec_por_texto.items() if len(tec_ids) > 15]
if sobrecargados:
    WARN.append(f"{len(sobrecargados)} textos soportan >15 tecnicas (sobrecarga)")

# ═══════════════════════════════════════════════════════════
header("D", "FASE 3 - EJERCICIOS REALES vs PLACEHOLDERS (ensayo seccion IV.3)")
# ═══════════════════════════════════════════════════════════
PLACEHOLDER_PATTERNS = [
    r"\(repaso\)",
    r"^¿A qué técnica corresponde",
    r"corresponde esta descripción",
    r"^¿Qué haces para",
    r"^En «.*», «.*» significa:",
]

def is_placeholder(enunciado):
    if not enunciado:
        return True
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, enunciado, re.IGNORECASE):
            return True
    return False

reales = 0
placeholders = 0
por_proceso_real = Counter()
por_proceso_ph = Counter()
for ej in EJ.objects.filter(tecnica_id__in=a1_tec_ids).select_related("tecnica"):
    proceso = ej.tecnica.proceso if ej.tecnica else "?"
    if is_placeholder(ej.enunciado):
        placeholders += 1
        por_proceso_ph[proceso] += 1
    else:
        reales += 1
        por_proceso_real[proceso] += 1

print(f"  Ejercicios reales:      {reales}")
print(f"  Placeholders:           {placeholders}")
print(f"  Total A1:               {reales + placeholders}")
if reales + placeholders > 0:
    pct = 100 * reales / (reales + placeholders)
    print(f"  Ratio de contenido real: {pct:.1f}%")

print(f"\n  Por proceso:")
for proc in ("P1", "P2", "P3", "P4"):
    print(f"    {proc}: reales={por_proceso_real.get(proc,0):>3}  placeholders={por_proceso_ph.get(proc,0):>3}")

if placeholders > 0:
    TODO.append(f"Fase 3: reescribir {placeholders} placeholders con contenido real")
    WARN.append(f"{placeholders}/{reales + placeholders} ejercicios A1 son placeholder")
else:
    OK.append(f"Fase 3: {reales} ejercicios reales (0 placeholders)")

# ═══════════════════════════════════════════════════════════
header("E", "FASE 4 - RUBRICA AUTOMATICA (ensayo seccion VI)")
# ═══════════════════════════════════════════════════════════
print("  AVISO: la rubrica del ensayo tiene 5 criterios.")
print("         Solo 4 son parcialmente automatizables.")
print("         'Valor pedagogico' REQUIERE revision manual.")
print()

def score_a1_align(tx_id):
    tx = TX.objects.filter(id=tx_id).first() if tx_id else None
    if not tx:
        return 1, "sin texto"
    wc = word_count(tx)
    if wc is None:
        return 3, "sin contenido medible"
    if 60 <= wc <= 100:   return 5, f"{wc} palabras"
    if 40 <= wc < 60:     return 3, f"{wc} palabras (corto)"
    if 100 < wc <= 130:   return 3, f"{wc} palabras (largo)"
    return 2, f"{wc} palabras (fuera rango)"

OPER_VERBS = {"localizar","inferir","reconocer","distinguir","identificar",
              "buscar","encontrar","deducir","diferenciar","clasificar",
              "localiza","infiere","reconoce","distingue","identifica"}

def score_clarity(enunciado):
    if not enunciado:
        return 1, "vacio"
    largo = len(enunciado)
    tiene_verbo_op = any(v in enunciado.lower().split() for v in OPER_VERBS)
    if largo < 20:
        return 2, f"muy corto ({largo} chars)"
    if tiene_verbo_op and 30 <= largo <= 250:
        return 5, "operacion explicita"
    if tiene_verbo_op:
        return 4, "verbo ok, longitud rara"
    return 3, "sin verbo de operacion explicito"

def score_distractors(payload):
    if not isinstance(payload, dict) or "opciones" not in payload:
        return 1, "sin opciones"
    opciones = payload.get("opciones", [])
    if len(opciones) != 3:
        return 2, f"{len(opciones)} opciones (esperado 3)"
    largos = [len(o) for o in opciones]
    if max(largos) - min(largos) <= 20:
        return 5, "longitudes similares"
    if max(largos) - min(largos) <= 40:
        return 4, "longitudes razonables"
    return 2, f"longitudes muy dispares ({min(largos)}-{max(largos)})"

def score_justification(payload):
    if not isinstance(payload, dict):
        return 1, "sin payload"
    if "explicacion" in payload and payload["explicacion"]:
        return 5, "explicacion presente en payload"
    return 2, "sin explicacion en payload"

# Muestrear ejercicios (reales si hay, sino todos)
muestra = list(EJ.objects.filter(tecnica_id__in=a1_tec_ids).select_related("tecnica").order_by("id")[:args.sample])
if not muestra:
    print("  [SKIP] no hay ejercicios para muestrear")
else:
    puntuaciones = []
    for ej in muestra:
        s1, d1 = score_a1_align(ej.texto_id)
        s2, d2 = score_clarity(ej.enunciado)
        s3, d3 = score_distractors(ej.payload)
        s4, d4 = score_justification(ej.payload)
        promedio = (s1 + s2 + s3 + s4) / 4
        puntuaciones.append(promedio)
        print(f"  id={ej.id:>4}  tec=#{ej.tecnica.numero if ej.tecnica else '?':<3}  promedio={promedio:.1f}/5")
        print(f"    A1 align:    {s1}/5  ({d1})")
        print(f"    Claridad:    {s2}/5  ({d2})")
        print(f"    Distractores:{s3}/5  ({d3})")
        print(f"    Justificacion:{s4}/5 ({d4})")
        print(f"    Valor ped.:  N/A   (revision manual)")
        print()

    prom_global = sum(puntuaciones) / len(puntuaciones)
    print(f"  Promedio (4 criterios, {len(muestra)} ejercicios): {prom_global:.2f}/5")
    print(f"  Objetivo del ensayo: >= 4.0/5")

    if prom_global < 3.5:
        WARN.append(f"Fase 4: rubrica {prom_global:.2f}/5 < 3.5")
        TODO.append("Fase 4: reescribir ejercicios con puntuacion baja")
    elif prom_global < 4.0:
        WARN.append(f"Fase 4: rubrica {prom_global:.2f}/5 (cerca pero < 4.0)")
    else:
        OK.append(f"Fase 4: rubrica {prom_global:.2f}/5 (>= 4.0)")

# ═══════════════════════════════════════════════════════════
header("F", "KPIs DEL ENSAYO (seccion VII)")
# ═══════════════════════════════════════════════════════════
total_a1 = reales + placeholders
kpis = {
    "Ratio contenido real":     (f"{reales}/{total_a1}" if total_a1 else "0/0", ">0 (objetivo 98/98)"),
    "Score rubrica":            (f"{prom_global:.2f}/5" if muestra else "N/A", ">= 4.0"),
    "Textos A1":                (f"{len(a1_textos)}", "10-12"),
    "Tecnicas con texto":       (f"{len(a1_tec_ids) - len(tec_sin_texto)}/{len(a1_tec_ids)}", "100%"),
    "Placeholders":             (f"{placeholders}", "0"),
}
print(f"  {'KPI':<30} {'Actual':<20} {'Target':<20}")
for k, (actual, target) in kpis.items():
    print(f"  {k:<30} {actual:<20} {target:<20}")

# ═══════════════════════════════════════════════════════════
header("G", "WORKFLOW CSV MAESTRO (seccion VIII)")
# ═══════════════════════════════════════════════════════════
csv_path = ROOT / "docs" / "plan_densificacion_A1_full.csv"
print(f"  CSV maestro: {csv_path}")
if not csv_path.exists():
    print(f"  [MISS] no existe")
    print(f"  Generar base: python scripts/_plan_densificacion.py --nivel A1 --csv {csv_path}")
    TODO.append("Workflow: generar CSV maestro con _plan_densificacion.py")
else:
    import csv as csv_mod
    with csv_path.open(encoding="utf-8") as f:
        reader = list(csv_mod.DictReader(f))
    print(f"  Filas: {len(reader)}")
    if reader:
        cols = list(reader[0].keys())
        print(f"  Columnas: {cols}")
        req = ["tecnica_id", "enunciado", "opcion_a", "opcion_b", "opcion_c", "correcta"]
        faltantes = [c for c in req if c not in cols]
        if faltantes:
            print(f"  [WARN] Faltan columnas requeridas: {faltantes}")
            WARN.append(f"CSV sin columnas: {faltantes}")
        # Filas completas vs vacias
        completas = sum(1 for r in reader
                        if r.get("enunciado","").strip() and r.get("correcta","").strip())
        print(f"  Filas completas: {completas}/{len(reader)}")
        if completas == 0:
            WARN.append("CSV maestro existe pero sin filas completas")
        elif completas < len(reader):
            INFO.append(f"CSV: {completas}/{len(reader)} completas")

# ═══════════════════════════════════════════════════════════
header("H", "PILOT + BLINDAJE")
# ═══════════════════════════════════════════════════════════
pilot = ROOT / "scripts" / "pilot_test.py"
if pilot.exists():
    pt = pilot.read_text(encoding="utf-8", errors="replace")
    checks = {
        "[11] WARNINGS":         "header(11," in pt,
        "[12] DASHBOARD":        "header(12," in pt,
        "[13] DENSIFICACION_A1": "header(13," in pt,
        "import re":             "import re" in pt,
    }
    for k, ok in checks.items():
        print(f"  {k:<30} {'[OK]' if ok else '[MISS]'}")
        if not ok:
            WARN.append(f"pilot sin {k}")
    if all(checks.values()):
        OK.append("Pilot con [11][12][13] + import re")
else:
    FAILS.append("pilot_test.py no existe")

# ═══════════════════════════════════════════════════════════
header("I", "RIESGOS DEL ENSAYO (seccion X)")
# ═══════════════════════════════════════════════════════════
riesgos = []

# Riesgo 1: contenido aburrido (detectar textos sin gancho: pocos dialogos, pocos personajes)
textos_sin_gancho = []
for tx in a1_textos:
    if not TX_CONTENT:
        break
    raw = getattr(tx, TX_CONTENT, "") or ""
    tiene_dialogo = '"' in raw or '«' in raw or "—" in raw
    tiene_personaje = bool(re.search(r"\b(se llama|nombre|Lucía|Pablo|María|el niño|la niña)\b", raw, re.I))
    if not tiene_dialogo and not tiene_personaje:
        textos_sin_gancho.append(tx.id)
if textos_sin_gancho:
    riesgos.append(f"{len(textos_sin_gancho)} textos sin gancho narrativo (sin dialogo/personajes)")

# Riesgo 2: distractores obvios (detectar opciones muy dispares)
obvios = 0
for ej in EJ.objects.filter(tecnica_id__in=a1_tec_ids):
    p = ej.payload
    if isinstance(p, dict) and "opciones" in p:
        opciones = p["opciones"]
        if len(opciones) == 3:
            largos = [len(o) for o in opciones]
            if max(largos) - min(largos) > 50:
                obvios += 1
if obvios > 0:
    riesgos.append(f"{obvios} ejercicios con distractores de longitud muy dispar (probablemente obvios)")

# Riesgo 3: textos largos
textos_largos = sum(1 for _,_,wc,_ in textos_info if wc and wc > 130)
if textos_largos > 0:
    riesgos.append(f"{textos_largos} textos >130 palabras (fuera de A1)")

# Riesgo 4: validacion saltada
if placeholders > 0:
    riesgos.append(f"Validacion Fase 4 saltada: {placeholders} placeholders en DB")

# Riesgo 5: quedarse en A1
niveles_con_ejercicios = {}
for nv in ("A1","A2","B1","B2","C1","C2"):
    nv_ids = list(TL.objects.filter(nivel_mcer=nv).values_list("id", flat=True))
    nv_ej = EJ.objects.filter(tecnica_id__in=nv_ids).count()
    if nv_ids:
        niveles_con_ejercicios[nv] = (len(nv_ids), nv_ej, nv_ej / len(nv_ids))
print(f"\n  Ratio por nivel (deteccion de riesgo 'quedarse en A1'):")
for nv, (n_tec, n_ej, r) in niveles_con_ejercicios.items():
    print(f"    {nv}: {n_tec} tec / {n_ej} ej / ratio {r:.2f}")

# ═══════════════════════════════════════════════════════════
header("J", "VEREDICTO Y SIGUIENTE FASE")
# ═══════════════════════════════════════════════════════════
print(f"\n  OK:    {len(OK)}")
for o in OK:    print(f"    [OK]   {o}")
print(f"\n  INFO:  {len(INFO)}")
for i in INFO:  print(f"    [INFO] {i}")
print(f"\n  WARN:  {len(WARN)}")
for w in WARN:  print(f"    [??]   {w}")
print(f"\n  FAILS: {len(FAILS)}")
for f in FAILS: print(f"    [!!]   {f}")

print(f"\n  PENDIENTE / TODO ({len(TODO)}):")
for t in TODO:
    print(f"    [ ] {t}")

if riesgos:
    print(f"\n  RIESGOS ACTIVOS ({len(riesgos)}):")
    for r in riesgos:
        print(f"    [!] {r}")

print()
print("=" * 78)
print("FASES DEL ENSAYO - ESTADO")
print("=" * 78)

fases = [
    ("Fase 1 - Curaduria textos",  len(a1_textos) >= 10),
    ("Fase 2 - Mapeo completo",    len(tec_sin_texto) == 0),
    ("Fase 3 - Contenido real",    placeholders == 0 and reales > 0),
    ("Fase 4 - Rubrica >= 4.0",    muestra and prom_global >= 4.0),
    ("Fase 5 - Seed verificado",   placeholders == 0 and len(a1_ej_ids) >= len(a1_tec_ids) * 2),
]

for nombre, done in fases:
    print(f"  [{'✓' if done else ' '}] {nombre}")

primera_pendiente = next((n for n, d in fases if not d), None)
if primera_pendiente:
    print(f"\n  >>> Siguiente fase: {primera_pendiente}")
    if "Fase 1" in primera_pendiente:
        print("      Escribir textos A1 de 60-100 palabras. Objetivo: 10-12.")
    elif "Fase 2" in primera_pendiente:
        print("      Mapear cada tecnica A1 a un texto del corpus.")
    elif "Fase 3" in primera_pendiente:
        print("      Reescribir placeholders. Rellenar CSV maestro.")
        print("      Aplicar: _seed_densificacion_a1.py --mode csv --apply")
    elif "Fase 4" in primera_pendiente:
        print("      Validacion por pares + piloto con estudiantes.")
    elif "Fase 5" in primera_pendiente:
        print("      Re-seed y verificacion en pilot_test.py [13].")
else:
    print("\n  *** Todas las fases completas ***")

print()
if FAILS:
    sys.exit(1)
else:
    sys.exit(0)