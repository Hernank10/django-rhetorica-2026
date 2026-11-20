# scripts/_fix_meta_16.py
# Reformula meta-preguntas del texto 16 ancladas al cuerpo nuevo de 4 párrafos.
# Uso:
#   python scripts\_fix_meta_16.py            # dry-run
#   python scripts\_fix_meta_16.py --apply    # aplica

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

TEXTO_ID = 16

# ej_id -> dict con nuevo enunciado + payload
CAMBIOS = {
    875: {
        "enunciado": "¿Qué opina Marta sobre los cerdos?",
        "payload": {
            "opciones": [
                "Que son divertidos.",
                "Que son peligrosos.",
                "Que son aburridos.",
            ],
            "correcta": "A",
            "explicacion": "El cuarto párrafo dice que Marta dice que los cerdos son divertidos.",
        },
    },
    880: {
        "enunciado": "¿Qué se presenta en el primer párrafo?",
        "payload": {
            "opciones": [
                "La granja del abuelo y los animales que viven en ella.",
                "La rutina de la noche en la granja.",
                "Las vacaciones de Marta en la playa.",
            ],
            "correcta": "A",
            "explicacion": "El primer párrafo presenta la granja, el abuelo y los animales.",
        },
    },
    876: {
        "enunciado": "¿Cuántas vacas hay en la granja?",
        "payload": {
            "opciones": [
                "Cinco vacas.",
                "Diez vacas.",
                "Dos vacas.",
            ],
            "correcta": "A",
            "explicacion": "El segundo párrafo dice: 'Hay cinco vacas y producen leche cada día'.",
        },
    },
    # 276 ya ancla al cuerpo nuevo; lo dejamos tal cual.
}


def main():
    aplicar = "--apply" in sys.argv
    print(f"Reformulando meta del texto {TEXTO_ID}\n")
    for ej_id, cambio in CAMBIOS.items():
        try:
            ej = EJ.objects.get(id=ej_id)
        except EJ.DoesNotExist:
            print(f"[SKIP] ej.id={ej_id} no existe")
            continue
        if ej.texto_id != TEXTO_ID:
            print(f"[SKIP] ej.id={ej_id} ya no está en tx={TEXTO_ID} (tx={ej.texto_id})")
            continue

        ya_ok = (ej.enunciado or "") == cambio["enunciado"]
        if ya_ok:
            print(f"[SKIP] ej.id={ej_id} ya reformulado")
            continue

        if not aplicar:
            print(f"[DRY] ej.id={ej_id}  Q_antes: {(ej.enunciado or '')[:60]}")
            print(f"                    Q_nuevo: {cambio['enunciado']}")
            continue

        ej.enunciado = cambio["enunciado"]
        ej.payload = cambio["payload"]
        ej.tipo = "multiple_choice"
        ej.save(update_fields=["enunciado", "payload", "tipo"])
        print(f"[OK] ej.id={ej_id} reformulado -> {cambio['enunciado']}")

    if not aplicar:
        print("\n[DRY-RUN] Ejecuta con --apply para aplicar.")


if __name__ == "__main__":
    main()