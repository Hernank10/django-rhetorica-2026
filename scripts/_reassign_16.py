# scripts/_reassign_16.py
# Reasigna contaminados del texto 16 a su texto real y borra duplicados.
# Uso:
#   python scripts\_reassign_16.py            # dry-run
#   python scripts\_reassign_16.py --apply    # aplica

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")

import django
django.setup()

from django.apps import apps

EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

ORIGEN_ID = 16

# ej_id -> texto_destino_id
REASIGNAR = {
    772: 9,    # "El gato saltó del muro" -> A2 #9 "El gato que hablaba"
    871: 13,   # "huevo/gallina/maíz" -> A1 #13 "El perro perdido" (ajusta si no encaja)
    272: 47,   # "el reloj corría" -> A1 #47 "Un día en la vida de Ana"
    275: 13,   # refrán "Al mal tiempo, buena cara" -> A1 #13 (o borrar si no encaja)
    1428: 13,  # "el perro / los perros" (gramatical) -> A1 #13 "El perro perdido"
}
# ej_id -> texto_destino_id
# ej_ids a borrar (duplicados funcionales o sin destino claro)
BORRAR = [871, 272, 275]
# ej_ids a borrar (duplicados o sin destino claro)
BORRAR = []


def main():
    aplicar = "--apply" in sys.argv

    print(f"Reasignando desde texto {ORIGEN_ID}\n")

    for ej_id, dest_id in REASIGNAR.items():
        try:
            ej = EJ.objects.get(id=ej_id)
        except EJ.DoesNotExist:
            print(f"[SKIP] ej.id={ej_id} no existe")
            continue
        if ej.texto_id != ORIGEN_ID:
            print(f"[SKIP] ej.id={ej_id} ya está en tx={ej.texto_id}")
            continue
        try:
            dest = TX.objects.get(id=dest_id)
        except TX.DoesNotExist:
            print(f"[WARN] ej.id={ej_id} destino {dest_id} no existe")
            continue
        dup = EJ.objects.filter(texto_id=dest_id, enunciado=ej.enunciado).exclude(id=ej.id).first()
        if dup:
            print(f"[WARN] ej.id={ej_id} DUPLICADO de ej.id={dup.id} en tx={dest_id} -> borrar en vez de reasignar")
            continue
        if not aplicar:
            print(f"[DRY] ej.id={ej_id} -> tx={dest_id} ({dest.titulo[:40]})")
            continue
        ej.texto_id = dest_id
        ej.save(update_fields=["texto"])
        print(f"[OK] ej.id={ej_id} -> tx={dest_id}")

    for ej_id in BORRAR:
        try:
            ej = EJ.objects.get(id=ej_id)
        except EJ.DoesNotExist:
            print(f"[SKIP] borrar ej.id={ej_id} no existe")
            continue
        if not aplicar:
            print(f"[DRY] borrar ej.id={ej_id}")
            continue
        ej.delete()
        print(f"[OK] borrado ej.id={ej_id}")

    if not aplicar:
        print("\n[DRY-RUN] Ejecuta con --apply para aplicar.")


if __name__ == "__main__":
    main()