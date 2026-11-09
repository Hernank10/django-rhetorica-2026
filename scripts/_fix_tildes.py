"""_fix_tildes.py - Corrige tildes faltantes en TecnicaGramatical.

DRY-RUN por defecto. --apply para escribir.
Solo actúa sobre TecnicaGramatical (146 registros, 169 hallazgos).
NO toca Flashcard (M3 congelado, 0 errores), Modulo, Curso, TecnicaLectura, Texto.

Las palabras del diccionario son las que SIEMPRE llevan tilde en español
(sin excepción contextual). No incluye 'aun/aún', 'solo/sólo', 'este/éste'
porque dependen del contexto y requieren análisis semántico.
"""
import os, sys, re, argparse
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

PALABRAS = {
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
    "morfologia": "morfología",
    "semantica": "semántica",
    "pragmatica": "pragmática",
    "fonetica": "fonética",
}

def fix_text(text):
    """Devuelve (texto_corregido, num_cambios). Preserva capitalización inicial."""
    if not text:
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

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

# Solo TecnicaGramatical. Flashcard congelado (M3), el resto tiene 0 errores.
M = apps.get_model("core", "TecnicaGramatical")
CAMPOS = ["titulo", "teoria", "regla", "explicacion"]
existentes = [f.name for f in M._meta.get_fields() if hasattr(f, "name")]
CAMPOS_OK = [c for c in CAMPOS if c in existentes]

header("A", "PLAN (TecnicaGramatical)")
print(f"  Campos a revisar: {CAMPOS_OK}")
print(f"  Total registros: {M.objects.count()}")

plan = []
for obj in M.objects.all():
    cambios_obj = {}
    for fname in CAMPOS_OK:
        old = getattr(obj, fname, "") or ""
        new, n = fix_text(str(old))
        if n > 0:
            cambios_obj[fname] = (old, new, n)
    if cambios_obj:
        plan.append((obj, cambios_obj))

total_cambios = sum(n for _, c in plan for _, _, n in c.values())
print(f"\n  Objetos a modificar: {len(plan)}")
print(f"  Total sustituciones: {total_cambios}")

print(f"\n  Primeros 10 (ANTES / DESPUÉS):")
for obj, cambios in plan[:10]:
    print(f"\n  id={obj.pk}  {obj.titulo[:60]}")
    for fname, (old, new, n) in cambios.items():
        print(f"    {fname}: {n} cambio(s)")
        # Mostrar solo el fragmento que cambia
        for wrong, right in PALABRAS.items():
            pat = re.compile(rf"\b{re.escape(wrong)}\b", re.IGNORECASE)
            if pat.search(old):
                m = pat.search(old)
                s = max(0, m.start() - 25); e = min(len(old), m.end() + 25)
                print(f"      ANTES:    ...{old[s:e]}...")
                break
        print(f"      DESPUÉS:  {new[:120]}")

header("B", "APLICAR" if args.apply else "DRY-RUN")
if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print("  Revisa los 10 ejemplos de arriba.")
    print("  Si todo es correcto: --apply")
    sys.exit(0)

from django.db import transaction
with transaction.atomic():
    for obj, cambios in plan:
        for fname, (old, new, n) in cambios.items():
            setattr(obj, fname, new)
        obj.save(update_fields=list(cambios.keys()))
    print(f"  [OK] {len(plan)} registros actualizados, {total_cambios} sustituciones")

header("C", "VERIFICAR")
restantes = 0
for obj in M.objects.all():
    for fname in CAMPOS_OK:
        old = getattr(obj, fname, "") or ""
        _, n = fix_text(str(old))
        restantes += n
print(f"  Tildes pendientes tras fix: {restantes}")
if restantes == 0:
    print("  [OK] Todas las tildes del diccionario corregidas")
else:
    print("  [WARN] Quedan errores fuera del diccionario (revisar)")