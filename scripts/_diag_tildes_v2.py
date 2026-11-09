"""_diag_tildes_v2.py - Diagnostico expandido.

v2:
- Diccionario 23 -> ~60 palabras
- Auto-discovery: todos los modelos con CharField/TextField/JSONField
- Escanea JSONField (contenido de ejercicios vive ahi)
- Escanea TODOS los campos de texto (bloque, ejemplo_correcto, etc.)
"""
import os, sys, re, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps

PALABRAS = {
    "gramatica": "gramática", "gramatico": "gramático",
    "ortografia": "ortografía", "ortografico": "ortográfico",
    "retorica": "retórica", "retorico": "retórico",
    "espanol": "español", "espanola": "española",
    "ingles": "inglés", "frances": "francés", "aleman": "alemán",
    "musica": "música", "numero": "número",
    "lexico": "léxico", "lexica": "léxica",
    "silaba": "sílaba", "silabas": "sílabas",
    "morfologia": "morfología", "semantica": "semántica",
    "pragmatica": "pragmática", "fonetica": "fonética",
    "latin": "latín",
    "clasico": "clásico", "clasica": "clásica",
    "clasicos": "clásicos", "clasicas": "clásicas",
    "peninsula": "península",
    "iberica": "ibérica", "iberico": "ibérico",
    "caida": "caída",
    "ciceron": "Cicerón",
    "evolucion": "evolución",
    "region": "región",
    "teoria": "teoría",
    "categoria": "categoría",
    "proximo": "próximo", "proxima": "próxima",
    "ultimo": "último", "ultima": "última",
    "unico": "único", "unica": "única",
    "practica": "práctica", "practico": "práctico",
    "rapido": "rápido", "rapida": "rápida",
    "facil": "fácil", "dificil": "difícil",
    "logica": "lógica", "logico": "lógico",
    "tecnica": "técnica", "tecnico": "técnico",
    "academico": "académico", "academica": "académica",
    "basico": "básico", "basica": "básica",
    "metodo": "método",
    "periodo": "período",
    "minimo": "mínimo", "maximo": "máximo",
    "publico": "público",
    "peticion": "petición",
    "oracion": "oración",
    "entonacion": "entonación",
    "explicacion": "explicación",
}

MOJIBAKE_RE = re.compile(r"Ã[\x80-\xbf]|â€")

def find_issues(text):
    if not text:
        return []
    issues = []
    for wrong, right in PALABRAS.items():
        pat = re.compile(rf"\b{re.escape(wrong)}\b", re.IGNORECASE)
        for m in pat.finditer(text):
            s = max(0, m.start() - 30); e = min(len(text), m.end() + 30)
            issues.append((wrong, right, "..." + text[s:e] + "..."))
    for m in MOJIBAKE_RE.finditer(text):
        s = max(0, m.start() - 20); e = min(len(text), m.end() + 20)
        issues.append(("MOJIBAKE", m.group(0), "..." + text[s:e] + "..."))
    return issues

# ═══ A. Descubrir modelos y campos ═══
print(); print("=" * 78); print("[A] MODELOS Y CAMPOS ESCANEADOS"); print("=" * 78)

modelos = []
for model in apps.get_app_config("core").get_models():
    if not hasattr(model, "objects"):
        continue
    campos_txt = []
    for f in model._meta.get_fields():
        if not hasattr(f, "get_internal_type"):
            continue
        t = f.get_internal_type()
        if t in ("CharField", "TextField", "JSONField"):
            campos_txt.append((f.name, t))
    if not campos_txt:
        continue
    try:
        n = model.objects.count()
    except Exception:
        n = 0
    modelos.append((model.__name__, campos_txt, n))
    if n > 0:
        campos_str = ", ".join(f"{n}({t})" for n, t in campos_txt[:8])
        print(f"  {model.__name__:<28} {n:>4} registros | {campos_str}")

# ═══ B. Escanear ═══
print(); print("=" * 78); print("[B] HALLAZGOS POR MODELO"); print("=" * 78)

hallazgos = []
for nombre, campos, n_total in modelos:
    if n_total == 0:
        continue
    M = apps.get_model("core", nombre)
    n_iss = 0
    for obj in M.objects.all():
        for fname, ftype in campos:
            try:
                val = getattr(obj, fname, "")
            except Exception:
                continue
            if val is None:
                continue
            if ftype == "JSONField":
                try:
                    val = json.dumps(val, ensure_ascii=False) if isinstance(val, (dict, list)) else str(val)
                except Exception:
                    val = str(val)
            elif not isinstance(val, str):
                continue
            for w, r, ctx in find_issues(val):
                n_iss += 1
                hallazgos.append({
                    "model": nombre, "id": obj.pk, "field": fname,
                    "type": ftype, "wrong": w, "right": r, "ctx": ctx,
                })
    if n_iss > 0:
        print(f"  {nombre:<28} {n_iss:>4} hallazgos")

# ═══ C. Resumen ═══
print(); print("=" * 78); print("[C] RESUMEN"); print("=" * 78)

if not hallazgos:
    print("  [OK] Sin errores en ningun modelo/campo")
    sys.exit(0)

por_m, por_w, por_campo = {}, {}, {}
for h in hallazgos:
    por_m[h["model"]] = por_m.get(h["model"], 0) + 1
    por_w[h["wrong"]] = por_w.get(h["wrong"], 0) + 1
    por_campo[(h["model"], h["field"])] = por_campo.get((h["model"], h["field"]), 0) + 1

print(f"\n  Total hallazgos: {len(hallazgos)}")
print(f"\n  Por modelo:")
for m, n in sorted(por_m.items(), key=lambda x: -x[1]):
    print(f"    {m:<28} {n:>4}")

print(f"\n  Por campo (top 15):")
for (m, f), n in sorted(por_campo.items(), key=lambda x: -x[1])[:15]:
    print(f"    {m}.{f:<24} {n:>4}")

print(f"\n  Por palabra (top 15):")
for w, n in sorted(por_w.items(), key=lambda x: -x[1])[:15]:
    print(f"    {w:<18} {n:>4}")

print(f"\n  Primeros 15 hallazgos:")
for h in hallazgos[:15]:
    print(f"    {h['model']}#{h['id']} [{h['field']}]: '{h['wrong']}' -> '{h['right']}'")
    print(f"      {h['ctx'][:80]}")

print(f"\n  Campos que faltaban en v1:")
campos_nuevos = {"bloque", "ejemplo_correcto", "ejemplo_incorrecto", "enunciado",
                "respuesta_correcta", "mensaje", "feedback", "contenido"}
for (m, f), n in sorted(por_campo.items(), key=lambda x: -x[1]):
    if f in campos_nuevos:
        print(f"    {m}.{f:<24} {n:>4}  (v1 no lo escaneaba)")