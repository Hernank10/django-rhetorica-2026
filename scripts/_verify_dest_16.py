# scripts/_verify_dest_16.py
# Verifica destinos de ejercicios contaminados del texto 16 antes de reasignar.
# Uso: python scripts\_verify_dest_16.py

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

# ej_id -> texto_destino_id propuesto (ajusta tras revisar la salida)
DESTINOS = {
    772: 9,    # "El gato saltó del muro" -> A2 #9 "El gato que hablaba"
    871: 16,   # "huevo/gallina/maíz" -> revisar (puede ser del propio 16 o duplicado)
    272: 16,   # "el reloj corría" -> revisar
    275: 16,   # refrán "Al mal tiempo, buena cara" -> revisar (vino del 51)
    1428: 16,  # "el perro / los perros" -> revisar
    276: 16,   # "vacas blanco y negro" -> candidato a reformular, no reasignar
    875: 16,   # metalingüístico -> reformular
    880: 16,   # metalingüístico -> reformular
    876: 16,   # metalingüístico -> reformular
}


def main():
    print(f"Verificando destinos para ejercicios del texto {ORIGEN_ID}\n")
    for ej_id, dest_id in DESTINOS.items():
        try:
            ej = EJ.objects.select_related("texto").get(id=ej_id)
        except EJ.DoesNotExist:
            print(f"[WARN] ej.id={ej_id} NO existe")
            continue
        origen_ok = ej.texto_id == ORIGEN_ID
        try:
            dest = TX.objects.get(id=dest_id)
            dest_ok = True
        except TX.DoesNotExist:
            print(f"[WARN] ej.id={ej_id} -> texto destino {dest_id} NO existe")
            continue

        # ¿Ya hay un ej con el mismo enunciado en el destino?
        dup = EJ.objects.filter(texto_id=dest_id, enunciado=ej.enunciado).exclude(id=ej.id).first()
        dup_txt = f"DUPLICADO con ej.id={dup.id}" if dup else "sin duplicado"

        flag = "OK" if (origen_ok and dest_ok and not dup) else "WARN"
        print(f"[{flag}] ej.id={ej_id} actual_tx={ej.texto_id} -> destino={dest_id} ({dest.titulo[:40]}) | {dup_txt}")
        print(f"       Q: {(ej.enunciado or '')[:80]}")


if __name__ == "__main__":
    main()