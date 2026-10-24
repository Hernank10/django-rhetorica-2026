"""Carga idempotente de técnicas sintácticas y sus ejercicios."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")

import django
django.setup()

from core.models_sintaxis import TecnicaSintactica, EjercicioTecnica
from core.data.tecnicas_sintaxis import TECNICAS, EJERCICIOS


def main():
    print(f"[SEED] {len(TECNICAS)} técnicas a cargar")
    creadas = 0
    actualizadas = 0

    for t in TECNICAS:
        _, created = TecnicaSintactica.objects.update_or_create(
            numero=t["numero"],
            defaults={k: v for k, v in t.items() if k != "numero"},
        )
        if created:
            creadas += 1
        else:
            actualizadas += 1

    print(f"[OK] Técnicas: {creadas} creadas, {actualizadas} actualizadas")
    print(f"[INFO] Total técnicas en DB: {TecnicaSintactica.objects.count()}")

    ej_creados = 0
    ej_actualizados = 0
    for numero, ejs in EJERCICIOS.items():
        try:
            tecnica = TecnicaSintactica.objects.get(numero=numero)
        except TecnicaSintactica.DoesNotExist:
            print(f"[!] Técnica {numero} no existe, skip ejercicios")
            continue
        for ej in ejs:
            _, created = EjercicioTecnica.objects.update_or_create(
                tecnica=tecnica,
                orden=ej["orden"],
                defaults={"tipo": ej["tipo"], "payload": ej["payload"]},
            )
            if created:
                ej_creados += 1
            else:
                ej_actualizados += 1

    print(f"[OK] Ejercicios: {ej_creados} creados, {ej_actualizados} actualizados")
    print(f"[INFO] Total ejercicios en DB: {EjercicioTecnica.objects.count()}")

    print("\n[DIST] Por bloque:")
    for bloque in ["A", "B", "C", "D", "E", "F", "G"]:
        n = TecnicaSintactica.objects.filter(bloque=bloque).count()
        if n > 0:
            print(f"  Bloque {bloque}: {n} técnicas")

    print("\n[DIST] Por tipo de ejercicio:")
    for tipo, nombre in EjercicioTecnica.TIPOS:
        n = EjercicioTecnica.objects.filter(tipo=tipo).count()
        if n > 0:
            print(f"  Tipo {tipo} ({nombre[:30]}): {n}")


if __name__ == "__main__":
    main()