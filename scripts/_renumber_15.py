# scripts/_renumber_15.py
import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")
TEXTO_ID = 15


def main():
    aplicar = "--apply" in sys.argv
    ejs = list(EJ.objects.filter(texto_id=TEXTO_ID).order_by("orden", "id"))
    print(f"Texto {TEXTO_ID}: {len(ejs)} ejercicios")
    cambios = 0
    for i, ej in enumerate(ejs, start=1):
        if ej.orden == i:
            continue
        cambios += 1
        if not aplicar:
            print(f"[DRY] ej.id={ej.id} orden {ej.orden} -> {i}"); continue
        ej.orden = i
        ej.save(update_fields=["orden"])
        print(f"[OK] ej.id={ej.id} orden -> {i}")
    if cambios == 0:
        print("[SKIP] Ya está renumerado 1..N.")
    elif not aplicar:
        print(f"\n[DRY-RUN] {cambios} cambios. Ejecuta con --apply para aplicar.")


if __name__ == "__main__":
    main()