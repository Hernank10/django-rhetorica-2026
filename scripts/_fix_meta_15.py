# scripts/_fix_meta_15.py
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

CAMBIOS = {
    255: {
        "enunciado": "¿Cómo empieza el cuento?",
        "payload": {
            "opciones": ["Con la fiesta en el jardín.", "Con Elena en la cama.", "Con la abuela en el mercado."],
            "correcta": "A",
            "explicacion": "El primer párrafo dice que la fiesta es en el jardín de casa.",
        },
    },
    256: {
        "enunciado": "¿Quién es la protagonista de la fiesta?",
        "payload": {
            "opciones": ["Elena.", "La abuela.", "Pablo."],
            "correcta": "A",
            "explicacion": "El primer párrafo dice que Elena cumple ocho años y es la protagonista.",
        },
    },
    257: {
        "enunciado": "¿Dónde se celebra la fiesta?",
        "payload": {
            "opciones": ["En el jardín de su casa.", "En el colegio.", "En el parque del pueblo."],
            "correcta": "A",
            "explicacion": "El primer párrafo dice que la abuela ha organizado la fiesta en el jardín.",
        },
    },
    268: {
        "enunciado": "¿Qué hace Elena primero?",
        "payload": {
            "opciones": ["Sopla las velas de la tarta.", "Abre los regalos.", "Juega al escondite en el patio."],
            "correcta": "A",
            "explicacion": "El segundo párrafo dice que Elena sopla las velas antes de jugar y abrir regalos.",
        },
    },
}


def main():
    aplicar = "--apply" in sys.argv
    print(f"Reformulando meta del texto {TEXTO_ID}\n")
    for ej_id, cambio in CAMBIOS.items():
        try:
            ej = EJ.objects.get(id=ej_id)
        except EJ.DoesNotExist:
            print(f"[SKIP] ej.id={ej_id} no existe"); continue
        if ej.texto_id != TEXTO_ID:
            print(f"[SKIP] ej.id={ej_id} ya no está en tx={TEXTO_ID} (tx={ej.texto_id})"); continue
        if (ej.enunciado or "") == cambio["enunciado"]:
            print(f"[SKIP] ej.id={ej_id} ya reformulado"); continue
        if not aplicar:
            print(f"[DRY] ej.id={ej_id} Q_antes: {(ej.enunciado or '')[:60]}")
            print(f"                Q_nuevo: {cambio['enunciado']}")
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