import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

# Ajusta segun _verify_dest_51.py: si hay duplicado -> delete, si no -> reassign
reassign = {1413: 48, 1351: 47, 1360: 13, 275: 16}
for ej_id, tx_id in reassign.items():
    try:
        ej = EJ.objects.get(id=ej_id)
    except EJ.DoesNotExist:
        print(f"SKIP ej.id={ej_id} NO EXISTE"); continue
    if ej.texto_id == tx_id:
        print(f"SKIP ej.id={ej_id} ya en tx {tx_id}"); continue
    print(f"REASIGN ej.id={ej_id}  tx {ej.texto_id} -> {tx_id}  Q: {(ej.enunciado or '')[:60]}")
    ej.texto_id = tx_id
    ej.save(update_fields=["texto_id"])
print("OK reasignacion")