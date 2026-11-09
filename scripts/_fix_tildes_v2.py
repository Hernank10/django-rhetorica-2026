"""_fix_tildes_v2.py - Fix quirurgico con whitelist.

Solo corrige campos de contenido pedagogico. NO toca:
- Enums (categoria, tipo, nivel, estado)
- URLs (url_destino, archivo_origen)
- Slugs y metadata
- ContenidoJSON.datos (dudoso, excluido hasta verificar)

JSONField: walk recursivo, solo valores str, NUNCA keys.
"""
import os, sys, re, json, argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps
from django.db import transaction

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
    "peticion": "petición",
    "oracion": "oración",
    "entonacion": "entonación",
    "explicacion": "explicación",
}

# Whitelist: solo contenido pedagogico. NUNCA enums, URLs, slugs.
WHITELIST = {
    "TecnicaGramatical":  ["titulo", "teoria", "explicacion", "regla",
                           "ejemplo_correcto", "ejemplo_incorrecto", "bloque"],
    "TecnicaSintactica":  ["titulo", "teoria", "explicacion", "regla",
                           "ejemplo_correcto", "ejemplo_incorrecto", "bloque"],
    "TecnicaLectura":     ["titulo", "teoria", "explicacion", "regla",
                           "ejemplo_correcto", "ejemplo_incorrecto"],
    "EjercicioGramatical":  ["payload"],   # JSONField
    "EjercicioTecnica":     ["payload"],   # JSONField
    "EjercicioLectura":     ["payload", "enunciado"],
    "EjercicioLinguistico": ["contenido"], # JSONField
    "Texto":              ["titulo", "cuerpo"],
    "Leccion":            ["titulo", "contenido"],
    "Curso":              ["titulo", "descripcion", "objetivo"],
    "Modulo":             ["titulo", "descripcion"],
    "Flashcard":          ["frente", "reverso", "explicacion", "ejemplo",
                           "ejercicio", "respuesta_ejercicio"],
    "Certificacion":      ["nombre", "descripcion"],
    "Logro":              ["nombre", "descripcion"],
    "TecnicaLinguistica": ["nombre", "descripcion"],
    "PreguntaEvaluacion": ["enunciado", "opciones", "respuesta_correcta"],
    # ContenidoJSON.datos: EXCLUIDO. 1309 hallazgos, contenido dudoso.
}

def fix_text(text):
    if not isinstance(text, str) or not text:
        return text, 0
    cambios = 0
    for wrong, right in PALABRAS.items():
        pat = re.compile(rf"\b{re.escape(wrong)}\b", re.IGNORECASE)
        def repl(m):
            nonlocal cambios
            orig = m.group(0)
            r = (right[0].upper() + right[1:]) if orig[0].isupper() else right
            cambios += 1
            return r
        text = pat.sub(repl, text)
    return text, cambios

def fix_json(obj, counter):
    """Recursivo. Solo procesa VALORES str, nunca KEYS."""
    if isinstance(obj, str):
        new, n = fix_text(obj)
        if n:
            counter[0] += n
        return new
    elif isinstance(obj, dict):
        # NO procesar keys, solo values
        return {k: fix_json(v, counter) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [fix_json(v, counter) for v in obj]
    else:
        return obj

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", "PLAN (whitelist)")
plan = []
for model_name, campos in WHITELIST.items():
    try:
        M = apps.get_model("core", model_name)
    except LookupError:
        continue
    exists = {f.name for f in M._meta.get_fields() if hasattr(f, "name")}
    campos_ok = [c for c in campos if c in exists]
    if not campos_ok:
        continue
    n_reg = 0
    for obj in M.objects.all():
        cambios = {}
        for fname in campos_ok:
            old = getattr(obj, fname, None)
            if old is None:
                continue
            f = M._meta.get_field(fname)
            ftype = f.get_internal_type()
            if ftype == "JSONField":
                cnt = [0]
                new = fix_json(old, cnt)
                if cnt[0]:
                    cambios[fname] = (old, new, cnt[0], "JSON")
            elif isinstance(old, str):
                new, n = fix_text(old)
                if n:
                    cambios[fname] = (old, new, n, "text")
        if cambios:
            plan.append((M, obj, cambios))
            n_reg += 1
    if n_reg:
        print(f"  {model_name:<24} {n_reg:>4} registros con cambios")

total = sum(c[2] for _,_,cs in plan for _,_,n,_ in cs.values() for c in [("","",n,"")] )
print(f"\n  Objetos a modificar: {len(plan)}")
print(f"  Total sustituciones: {sum(n for _,_,cs in plan for _,_,n,_ in cs.values())}")

header("B", "MUESTRA (primeros 8)")
for M, obj, cambios in plan[:8]:
    print(f"\n  {M.__name__}#{obj.pk}")
    for fname, (old, new, n, kind) in cambios.items():
        print(f"    {fname} ({kind}, {n} cambio(s))")
        if kind == "text":
            for wrong in PALABRAS:
                pat = re.compile(rf"\b{re.escape(wrong)}\b", re.IGNORECASE)
                if pat.search(old):
                    m = pat.search(old)
                    s = max(0, m.start()-30); e = min(len(old), m.end()+30)
                    print(f"      ANTES:   ...{old[s:e]}...")
                    print(f"      DESPUES: ...{new[s:e]}...")
                    break
        else:
            print(f"      JSON: {n} sustituciones (walk recursivo)")

header("C", "APLICAR" if args.apply else "DRY-RUN")
if not args.apply:
    print("  DRY-RUN. Nada modificado. Revisa la muestra.")
    print("  Si todo OK: --apply (con backup previo)")
    sys.exit(0)

with transaction.atomic():
    for M, obj, cambios in plan:
        for fname, (old, new, n, kind) in cambios.items():
            setattr(obj, fname, new)
        obj.save(update_fields=list(cambios.keys()))
    print(f"  [OK] {len(plan)} objetos actualizados")

header("D", "VERIFICAR")
import subprocess
r = subprocess.run([sys.executable, str(ROOT/"scripts"/"_diag_tildes_v2.py")],
                   capture_output=True, text=True)
for line in r.stdout.split("\n"):
    if "Total hallazgos" in line or "[OK] Sin errores" in line:
        print(f"  {line.strip()}")