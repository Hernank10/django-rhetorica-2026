"""_densificar_b1.py - F3b B1: crear 100 ejercicios nuevos como variantes.

Aprovecha los 100 existentes (93% coherentes). Cada variante:
  - Reformula el enunciado (whitelist de patrones)
  - Rota las opciones (A->B, B->C, C->A)
  - Ajusta la letra correcta
  - Adapta la explicación
"""
import os, sys, re, argparse
from pathlib import Path
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
parser.add_argument("--nivel", default="B1")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps
from django.db import transaction

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")

REFORMULACIONES = [
    (r"^¿?[Cc]u[aá]l es la tesis", "¿Qué idea principal defiende el autor en este texto?"),
    (r"^¿?[Cc]u[aá]l es la idea", "¿Cuál es la idea central que plantea el texto?"),
    (r"^¿?[Cc]u[aá]l es el tema", "¿De qué trata principalmente el texto?"),
    (r"^¿?[Cc]u[aá]l es la conclusi[oó]n", "¿Qué conclusión propone el autor al final?"),
    (r"^¿?[Cc]u[aá]l es el prop[oó]sito", "¿Para qué fue escrito este texto?"),
    (r"^¿?[Cc]u[aá]l es el objetivo", "¿Qué objetivo persigue el autor con este texto?"),
    (r"^¿?[Ee]l texto es", "¿Según el texto, es correcto afirmar que es"),
    (r"^¿?[Qq]u[eé] tipo de texto", "¿A qué género o tipo textual corresponde este texto?"),
    (r"^¿?[Cc]u[aá]l es el escenario", "¿Dónde se desarrolla la acción del texto?"),
    (r"^¿?[Cc]u[aá]l es el personaje", "¿Qué personaje protagoniza el relato?"),
]

def generar_variante(ej):
    """Devuelve (enunciado, opciones, correcta, explicacion) o None si no se puede."""
    if not isinstance(ej.payload, dict):
        return None
    ops = ej.payload.get("opciones", [])
    corr = ej.payload.get("correcta", "")
    expl = ej.payload.get("explicacion", "")

    if not ops or not corr:
        return None

    e_orig = (ej.enunciado or "").strip()

    # Reformular
    enun_nuevo = None
    for pat, repl in REFORMULACIONES:
        if re.match(pat, e_orig):
            enun_nuevo = repl
            break
    if not enun_nuevo:
        # Fallback: prefijo "Según el texto, "
        base = e_orig.rstrip("?").lstrip("¿")
        enun_nuevo = f"Según el texto, ¿{base.lower() if base[0].isupper() else base}?"

    # Rotar opciones (A->B, B->C, C->A si 3; A->B->C->D->A si 4)
    n = len(ops)
    nuevas_ops = ops[1:] + ops[:1]
    try:
        idx_corr = "ABCD".index(corr.upper())
        nuevo_corr = "ABCD"[(idx_corr - 1) % n]
    except ValueError:
        nuevo_corr = corr

    # Explicación
    texto_corr = ""
    for op in ops:
        if str(op).strip().startswith(corr + ")"):
            texto_corr = re.sub(r"^[A-Z]\)\s*", "", str(op)).strip()
            break
    if expl:
        nueva_expl = f"Variante: {expl}"
    elif texto_corr:
        nueva_expl = f"La respuesta correcta es {nuevo_corr}: «{texto_corr}»."
    else:
        nueva_expl = f"La opción correcta es {nuevo_corr}, según el texto."

    return enun_nuevo, nuevas_ops, nuevo_corr, nueva_expl

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", f"F3b {args.nivel} - DENSIFICAR")

tecnicas = list(TL.objects.filter(nivel_mcer=args.nivel))
por_tec = Counter(e.tecnica_id for e in EJ.objects.filter(tecnica__nivel_mcer=args.nivel))

plan = []  # (tec, ej_base, variante)
for tec in tecnicas:
    n = por_tec.get(tec.id, 0)
    if n >= 2:
        continue
    ej_base = EJ.objects.filter(tecnica=tec).first()
    if not ej_base:
        continue
    variante = generar_variante(ej_base)
    if variante:
        plan.append((tec, ej_base, variante))

print(f"  A crear: {len(plan)}")
print(f"\n  Muestra (primeros 8):")
for tec, base, (enun, ops, corr, expl) in plan[:8]:
    print(f"\n  tec #{tec.numero:>3} [{tec.proceso}]")
    print(f"    BASE: {base.enunciado[:70]}")
    print(f"    VAR:  {enun[:70]}")

header("B", "APLICAR" if args.apply else "DRY-RUN")

if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print(f"  Se crearian {len(plan)} ejercicios nuevos.")
    sys.exit(0)

with transaction.atomic():
    creados = 0
    for tec, base, (enun, ops, corr, expl) in plan:
        EJ.objects.create(
            tecnica=tec,
            texto_id=base.texto_id,
            enunciado=enun,
            tipo="multiple_choice",
            payload={"opciones": ops, "correcta": corr, "explicacion": expl},
            orden=1,
        )
        creados += 1
    print(f"\n  [OK] {creados} ejercicios creados")

# Verificar
header("C", "VERIFICAR")
ejs = list(EJ.objects.filter(tecnica__nivel_mcer=args.nivel))
por_tec2 = Counter(e.tecnica_id for e in ejs)
tec_2 = sum(1 for v in por_tec2.values() if v >= 2)
ratio = len(ejs) / max(1, len(tecnicas))
print(f"  Total ejercicios: {len(ejs)}")
print(f"  Tecnicas con 2+:  {tec_2}/{len(tecnicas)}")
print(f"  Ratio:            {ratio:.2f}")
if ratio >= 1.95 and tec_2 == len(tecnicas):
    print(f"\n  [OK] FASE 3b {args.nivel} COMPLETA")