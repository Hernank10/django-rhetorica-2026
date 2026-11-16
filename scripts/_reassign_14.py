import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

# 9 reasignaciones + 1 borrado (1442 es duplicado de 1419 en el 13)
reasignar = {
    276: 16,   # vacas / granja
    1345: 47,  # Ana trabaja
    1433: 13,  # perro perdido Lucía/Toby
    871: 16,   # huevo/gallina
    1409: 52,  # cafetería
    834: 47,   # Ana oficio
    836: 47,   # Ana niños entran
    837: 47,   # Ana tarde
    1374: 47,  # Ana feliz
}
borrar = [1442]  # duplicado de 1419 en el 13

for ej_id, tx_id in reasignar.items():
    try:
        ej = EJ.objects.get(id=ej_id)
    except EJ.DoesNotExist:
        print(f"SKIP ej.id={ej_id} NO EXISTE"); continue
    if ej.texto_id == tx_id:
        print(f"SKIP ej.id={ej_id} ya en tx {tx_id}"); continue
    print(f"REASIGN ej.id={ej_id}  tx {ej.texto_id} -> {tx_id}  Q: {(ej.enunciado or '')[:60]}")
    ej.texto_id = tx_id
    ej.save(update_fields=["texto_id"])

for ej_id in borrar:
    try:
        ej = EJ.objects.get(id=ej_id)
    except EJ.DoesNotExist:
        print(f"SKIP-BORRAR ej.id={ej_id} NO EXISTE"); continue
    print(f"DELETE ej.id={ej_id} (duplicado de 1419 en tx 13)  Q: {(ej.enunciado or '')[:60]}")
    ej.delete()

print("OK reasignacion + borrado")