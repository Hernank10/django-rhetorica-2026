"""Carga idempotente de tecnicas gramaticales (modulo 11)."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")

import django
django.setup()

from core.models_gramatica import TecnicaGramatical, EjercicioGramatical
from core.data.tecnicas_gramatica import TECNICAS, EJERCICIOS


def main():
    print(f"[SEED] {len(TECNICAS)} tecnicas gramaticales")
    creadas = actualizadas = 0
    for t in TECNICAS:
        _, created = TecnicaGramatical.objects.update_or_create(
            numero=t["numero"],
            defaults={k: v for k, v in t.items() if k != "numero"},
        )
        creadas += 1 if created else 0
        actualizadas += 0 if created else 1
    print(f"[OK] Tecnicas: {creadas} creadas, {actualizadas} actualizadas")
    print(f"[INFO] Total en DB: {TecnicaGramatical.objects.count()}")

    ej_c = ej_a = 0
    for numero, ejs in EJERCICIOS.items():
        try:
            tecnica = TecnicaGramatical.objects.get(numero=numero)
        except TecnicaGramatical.DoesNotExist:
            print(f"[!] Tecnica {numero} no existe, skip")
            continue
        for ej in ejs:
            _, created = EjercicioGramatical.objects.update_or_create(
                tecnica=tecnica, orden=ej["orden"],
                defaults={"tipo": ej["tipo"], "payload": ej["payload"]},
            )
            ej_c += 1 if created else 0
            ej_a += 0 if created else 1
    print(f"[OK] Ejercicios: {ej_c} creados, {ej_a} actualizados")
    print(f"[INFO] Total en DB: {EjercicioGramatical.objects.count()}")

    print("\n[DIST] Por bloque:")
    for bloque in "ABCDEFG":
        n = TecnicaGramatical.objects.filter(bloque=bloque).count()
        if n > 0:
            print(f"  Bloque {bloque}: {n}")


if __name__ == "__main__":
    main()