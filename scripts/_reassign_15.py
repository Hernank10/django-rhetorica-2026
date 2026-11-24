# scripts/_reassign_15.py
import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

ORIGEN_ID = 15
REASIGNAR = {1403: 13}   # idea principal de "El perro perdido" -> tx 13
BORRAR = [1426]          # Nebrija/Gramática 1492 -> no encaja en ningún texto A1


def main():
    aplicar = "--apply" in sys.argv
    print(f"Reasignando desde texto {ORIGEN_ID}\n")
    for ej_id, dest_id in REASIGNAR.items():
        try:
            ej = EJ.objects.get(id=ej_id)
        except EJ.DoesNotExist:
            print(f"[SKIP] ej.id={ej_id} no existe"); continue
        if ej.texto_id != ORIGEN_ID:
            print(f"[SKIP] ej.id={ej_id} ya está en tx={ej.texto_id}"); continue
        if not aplicar:
            print(f"[DRY] ej.id={ej_id} -> tx={dest_id}"); continue
        ej.texto_id = dest_id
        ej.save(update_fields=["texto"])
        print(f"[OK] ej.id={ej_id} -> tx={dest_id}")
    for ej_id in BORRAR:
        try:
            ej = EJ.objects.get(id=ej_id)
        except EJ.DoesNotExist:
            print(f"[SKIP] borrar ej.id={ej_id} no existe"); continue
        if not aplicar:
            print(f"[DRY] borrar ej.id={ej_id}"); continue
        ej.delete()
        print(f"[OK] borrado ej.id={ej_id}")
    if not aplicar:
        print("\n[DRY-RUN] Ejecuta con --apply para aplicar.")


if __name__ == "__main__":
    main()