import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

# Contaminados a reasignar (ajustar textos destino según corresponda)
reasignar = {
    1648: None,  # "cómo se define la IA" -> texto de IA (buscar id)
    136:  None,  # duplicado de 1648
    1686: None,  # "cómo evoluciona Marta" -> texto de Marta
    1702: None,  # "artículos 2023-2024" -> texto de IA/turismo
}
# Los IDs destino (None) hay que rellenarlos con los textos correctos.
# Si no se sabe, borrar los contaminados.

for ej_id, tx_id in reasignar.items():
    try:
        ej = EJ.objects.get(id=ej_id)
    except EJ.DoesNotExist:
        print(f"SKIP ej.id={ej_id} NO EXISTE"); continue
    if tx_id is None:
        print(f"DELETE ej.id={ej_id} (contaminado, sin destino claro)  Q: {(ej.enunciado or '')[:60]}")
        ej.delete()
    else:
        print(f"REASIGN ej.id={ej_id}  tx {ej.texto_id} -> {tx_id}")
        ej.texto_id = tx_id
        ej.save(update_fields=["texto_id"])
print("OK reassign")