import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

# Conservar: 954, 1665, 1667, 1669, 1671, 1673, 1674, 1675, 1676, 1678, 1679, 1680, 1681, 388, 1737
# Eliminar duplicados:
borrar = [
    1662, 808,    # argumento principal (conservar 1662? o 808?) -> conservar 1662, borrar 808
    1666, 384,    # antónimos -> conservar 1666, borrar 384
    1669, 387,    # cita textual -> conservar 1669, borrar 387
    1671, 389,    # evidencia empírica -> conservar 1671, borrar 389
    1673, 391,    # adjetivo valorativo -> conservar 1673, borrar 391
    1675, 393,    # palabra clave -> conservar 1675, borrar 393
    1676, 394,    # título anticipa -> conservar 1676, borrar 394
    1663,         # duplicado de 954
    1667,         # duplicado de 385? NO: 1667 vs 385, conservar 1667, borrar 385
    1674,         # duplicado de 392? conservar 1674, borrar 392
    1678,         # duplicado de 396? conservar 1678, borrar 396
    1681,         # duplicado de 956? conservar 1681, borrar 956
    1702,         # duplicado de 420? conservar 1702, borrar 420
]
# Ajuste: los pares son (conservar, borrar):
# 1662 vs 808 -> conservar 1662, borrar 808
# 1666 vs 384 -> conservar 1666, borrar 384
# 1669 vs 387 -> conservar 1669, borrar 387
# 1671 vs 389 -> conservar 1671, borrar 389
# 1673 vs 391 -> conservar 1673, borrar 391
# 1675 vs 393 -> conservar 1675, borrar 393
# 1676 vs 394 -> conservar 1676, borrar 394
# 954 vs 1663 -> conservar 954, borrar 1663
# 1665 vs 383 -> conservar 1665, borrar 383
# 1667 vs 385 -> conservar 1667, borrar 385
# 1674 vs 392 -> conservar 1674, borrar 392
# 1678 vs 396 -> conservar 1678, borrar 396
# 1681 vs 956 -> conservar 1681, borrar 956
# 1702 vs 420 -> conservar 1702, borrar 420

borrar = [808, 384, 387, 389, 391, 393, 394, 1663, 383, 385, 392, 396, 956, 420]

for ej_id in borrar:
    try:
        ej = EJ.objects.get(id=ej_id)
        print(f"DELETE ej.id={ej_id}  Q: {(ej.enunciado or '')[:60]}")
        ej.delete()
    except EJ.DoesNotExist:
        print(f"SKIP ej.id={ej_id} NO EXISTE")
print("OK dedup")