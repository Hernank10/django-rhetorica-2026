"""_diag_tildes.py - Busca tildes faltantes o mojibake en modelos con texto.

Read-only. No modifica nada.

Uso:
    python scripts/_diag_tildes.py
    python scripts/_diag_tildes.py --csv docs/tildes_report.csv
"""
import os, sys, re, argparse, csv
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--csv", default=None)
args, _ = parser.parse_known_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

# Palabras que SIEMPRE llevan tilde en español (no hay contexto que las exima)
PALABRAS_CON_TILDE = {
    "gramatica": "gramática",
    "gramatico": "gramático",
    "ortografia": "ortografía",
    "ortografico": "ortográfico",
    "ortograficas": "ortográficas",
    "ortograficos": "ortográficos",
    "retorica": "retórica",
    "retorico": "retórico",
    "espanol": "español",
    "espanola": "española",
    "ingles": "inglés",
    "frances": "francés",
    "aleman": "alemán",
    "musica": "música",
    "numero": "número",
    "lexico": "léxico",
    "lexica": "léxica",
    "silaba": "sílaba",
    "silabas": "sílabas",
    "sintaxis": None,  # "sintaxis" no lleva tilde, se queda así (regla)
    "morfologia": "morfología",
    "semantica": "semántica",
    "pragmatica": "pragmática",
    "fonetica": "fonética",
    "ortografia_": "ortografía",
}

MOJIBAKE_RE = re.compile(r"Ã[\x80-\xbf]|â€")

def find_issues(text):
    """Devuelve lista de (patron, sugerencia, contexto)."""
    if not text:
        return []
    issues = []
    lower = text.lower()
    for wrong, right in PALABRAS_CON_TILDE.items():
        if right is None:
            continue
        # buscar palabra completa (con \b)
        pat = re.compile(rf"\b{re.escape(wrong)}\b", re.IGNORECASE)
        for m in pat.finditer(text):
            # contexto de 30 chars alrededor
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 30)
            issues.append((wrong, right, "..." + text[start:end] + "..."))
    for m in MOJIBAKE_RE.finditer(text):
        start = max(0, m.start() - 20)
        end = min(len(text), m.end() + 20)
        issues.append(("MOJIBAKE", m.group(0), "..." + text[start:end] + "..."))
    return issues

# Modelos a escanear y sus campos de texto
MODELOS = [
    ("TecnicaGramatical", ["titulo", "descripcion", "teoria", "regla", "explicacion"]),
    ("Modulo",            ["titulo", "descripcion"]),
    ("Curso",             ["titulo", "descripcion", "objetivo"]),
    ("TecnicaLectura",    ["titulo", "teoria", "explicacion", "regla"]),
    ("Texto",             ["titulo"]),
    ("Flashcard",         ["frente", "reverso", "explicacion", "ejemplo"]),
]

header("A", "ESCANEO DE MODELOS")
hallazgos = []
for model_name, fields in MODELOS:
    try:
        M = apps.get_model("core", model_name)
    except LookupError:
        print(f"  [MISS] {model_name} no existe")
        continue
    existing_fields = [f.name for f in M._meta.get_fields() if hasattr(f, "name")]
    fields_ok = [f for f in fields if f in existing_fields]
    if not fields_ok:
        print(f"  [SKIP] {model_name}: ningún campo de texto encontrado (tiene: {existing_fields[:5]})")
        continue

    n_total = M.objects.count()
    n_con_issues = 0
    print(f"\n  {model_name} ({n_total} registros, campos: {fields_ok})")
    for obj in M.objects.all():
        for fname in fields_ok:
            text = getattr(obj, fname, "") or ""
            issues = find_issues(str(text))
            if issues:
                n_con_issues += 1
                for wrong, right, ctx in issues[:2]:  # max 2 por campo
                    hallazgos.append({
                        "model": model_name,
                        "id": obj.pk,
                        "field": fname,
                        "wrong": wrong,
                        "suggestion": right,
                        "context": ctx,
                    })
    print(f"    con problemas: {n_con_issues}/{n_total}")

header("B", "RESUMEN DE HALLAZGOS")
if not hallazgos:
    print("  [OK] Sin errores obvios de tildes ni mojibake")
else:
    print(f"  Total hallazgos: {len(hallazgos)}\n")
    por_modelo = {}
    for h in hallazgos:
        por_modelo.setdefault(h["model"], []).append(h)
    for m, items in por_modelo.items():
        print(f"  {m}: {len(items)}")
        for h in items[:3]:
            print(f"    id={h['id']} {h['field']}: '{h['wrong']}' → '{h['suggestion']}'")
            print(f"      ctx: {h['context'][:80]}")
        if len(items) > 3:
            print(f"    ... y {len(items) - 3} más")

header("C", "INTERPRETACIÓN")
print("""
  Si no aparecen hallazgos → los títulos están bien. El problema,
  si existe, está en:
    - El template (strings hardcoded en HTML)
    - La vista (strings en Python)
    - Un problema de encoding al RENDERIZAR (no en DB)

  Si aparecen hallazgos → hay errores reales en DB. Fix con:
    python scripts/_fix_tildes.py --apply

  Nota: Flashcard está CONGELADO (M3). Si los errores son solo
  en Flashcard, arreglarlos tiene bajo valor (no se ve en UI).
""")

if args.csv and hallazgos:
    path = Path(args.csv)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["model","id","field","wrong","suggestion","context"])
        w.writeheader()
        for h in hallazgos:
            w.writerow(h)
    print(f"\n  [OK] reporte exportado a {path}")