"""Carga tecnicas de Lengua Castellana C2."""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django
django.setup()
from core.models_gramatica import TecnicaGramatical, EjercicioGramatical
from core.data.tecnicas_c2 import TECNICAS, EJERCICIOS


def main():
    print(f"[SEED] {len(TECNICAS)} tecnicas C2")
    for t in TECNICAS:
        TecnicaGramatical.objects.update_or_create(
            numero=t["numero"],
            defaults={k: v for k, v in t.items() if k != "numero"},
        )
    total = TecnicaGramatical.objects.filter(modulo="c2").count()
    print(f"[OK] Total C2: {total}")
    ej_c = 0
    for numero, ejs in EJERCICIOS.items():
        try:
            tecnica = TecnicaGramatical.objects.get(numero=numero, modulo="c2")
        except TecnicaGramatical.DoesNotExist:
            print(f"[!] tec {numero} no existe")
            continue
        for ej in ejs:
            _, created = EjercicioGramatical.objects.update_or_create(
                tecnica=tecnica, orden=ej["orden"],
                defaults={"tipo": ej["tipo"], "payload": ej["payload"]},
            )
            ej_c += 1 if created else 0
    print(f"[OK] Ejercicios creados: {ej_c}")


if __name__ == "__main__":
    main()
