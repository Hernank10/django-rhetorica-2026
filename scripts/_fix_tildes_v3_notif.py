"""_fix_tildes_v3_notif.py - SOLO notificaciones. 100% seguro."""
import os, sys, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps
from django.db import transaction

APPLY = "--apply" in sys.argv

N = apps.get_model("core", "Notificacion")
CAMBIOS = {"basico": "básico", "gramatica": "gramática", "teorica": "teórica"}

plan = []
for obj in N.objects.all():
    if not obj.mensaje:
        continue
    old = obj.mensaje
    new = old
    for w, r in CAMBIOS.items():
        new = re.sub(rf"\bnivel {w}\b", f"nivel {r}", new)
    if new != old:
        plan.append((obj, old, new))

print(f"\nNotificaciones a modificar: {len(plan)}")
for obj, old, new in plan:
    print(f"  #{obj.pk}")
    print(f"    ANTES:   ...{old[-60:]}")
    print(f"    DESPUES: ...{new[-60:]}")

if not APPLY:
    print("\nDRY-RUN. Nada modificado. --apply para ejecutar.")
    sys.exit(0)

with transaction.atomic():
    for obj, old, new in plan:
        obj.mensaje = new
        obj.save(update_fields=["mensaje"])
print(f"\n[OK] {len(plan)} notificaciones actualizadas")