"""_enrich_payloads.py - Añade explicacion al payload desde TecnicaLectura.

Sin escribir contenido: usa el campo 'explicacion' que ya existe en el modelo.
Read-only por defecto. --apply para escribir.

Uso:
    python scripts/_enrich_payloads.py            # DRY-RUN
    python scripts/_enrich_payloads.py --apply    # Aplicar
"""
import os, sys, argparse
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
TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")

import re as _re
_PLACEHOLDER_RE = [
    r"\(repaso\)",
    r"^¿A qué técnica corresponde",
    r"corresponde esta descripción",
]
def is_placeholder(enunciado):
    if not enunciado:
        return True
    for pat in _PLACEHOLDER_RE:
        if _re.search(pat, enunciado, _re.IGNORECASE):
            return True
    return False

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

header("A", "ESTADO")
a1_ids = list(TL.objects.filter(nivel_mcer="A1").values_list("id", flat=True))
ej_a1 = EJ.objects.filter(tecnica_id__in=a1_ids).select_related("tecnica")
total = ej_a1.count()
sin_expl = sum(1 for ej in ej_a1 if not (isinstance(ej.payload, dict) and ej.payload.get("explicacion")))
print(f"  Ejercicios A1: {total}")
print(f"  Sin explicacion: {sin_expl}")

if sin_expl == 0:
    print("  [OK] Todos ya tienen explicacion. Nada que hacer.")
    sys.exit(0)

header("B", "PLAN")
plan = []
for ej in ej_a1:
    p = ej.payload if isinstance(ej.payload, dict) else {}
    if p.get("explicacion"):
        continue
    if is_placeholder(ej.enunciado):
        continue
    expl = (getattr(ej.tecnica, "explicacion", "") or "").strip()
    if not expl:
        expl = f"Aplica la tecnica: {ej.tecnica.titulo}."
    p["explicacion"] = expl[:250]
    plan.append((ej, p))

print(f"  A enriquecer: {len(plan)}")
for ej, p in plan[:3]:
    print(f"    id={ej.id}  expl='{p['explicacion'][:80]}...'")

header("C", "APLICAR" if args.apply else "DRY-RUN")
if not args.apply:
    print(f"  DRY-RUN. Nada modificado. --apply para ejecutar.")
    sys.exit(0)

from django.db import transaction
with transaction.atomic():
    for ej, p in plan:
        ej.payload = p
        ej.save(update_fields=["payload"])
    print(f"  [OK] Actualizados: {len(plan)}")

header("D", "VERIFICAR")
sin_expl2 = sum(1 for ej in ej_a1 if not (isinstance(ej.payload, dict) and ej.payload.get("explicacion")))
print(f"  Sin explicacion: {sin_expl2}")
print()
print("  Ahora corre de nuevo: python scripts/_diag_contenido_a1.py")
print("  Rubrica esperada: ~3.4-3.6 (sin explicacion baja a 5/5 en justificacion)")