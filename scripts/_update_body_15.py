# scripts/_update_body_15.py
# Cierre texto 15 "La fiesta de cumpleaños" (A1): cuerpo 1 párrafo -> 4 párrafos (~205 palabras).
# Uso:
#   python scripts\_update_body_15.py            # dry-run
#   python scripts\_update_body_15.py --apply    # aplica
# Idempotente: si el cuerpo ya es el objetivo, SKIP.

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

TX = apps.get_model("core", "Texto")

TEXTO_ID = 15

NUEVO_CUERPO = (
    "Elena cumple ocho años hoy. Su abuela ha organizado una fiesta en el jardín de su casa. "
    "Hay globos de colores rojos, azules y amarillos. Todos los amigos de Elena están invitados: "
    "Pablo, Lucía, Marta y los gemelos del tercero. La fiesta empieza a las cinco de la tarde.\n\n"
    "En el centro de la mesa hay una tarta de chocolate muy grande. La abuela la ha hecho con "
    "mucha harina, bastante azúcar y un poco de nata. Encima hay ocho velas de colores. "
    "Elena sopla las velas y todos cantan «Cumpleaños feliz». Su madre corta la tarta y reparte los platos.\n\n"
    "Después de comer, los niños juegan en el patio. Juegan al escondite y a la pelota. "
    "Pablo dice: «¡Qué bien lo pasamos en el patio!». Elena se ríe mucho con sus amigos. "
    "Luego, Elena abre los regalos: un libro, una pulsera y un juego de mesa. Le gustan todos.\n\n"
    "Al final de la tarde, Elena está muy contenta. Dice que es el mejor cumpleaños de su vida. "
    "Su abuela sonríe y le da un abrazo. Todos los invitados se van a casa con una bolsa de chuches. "
    "Para Elena, el mejor regalo es tener a su familia y a sus amigos."
)


def contar_parrafos(texto):
    if not texto:
        return 0
    return len([p for p in texto.split("\n\n") if p.strip()])


def main():
    aplicar = "--apply" in sys.argv
    try:
        tx = TX.objects.get(id=TEXTO_ID)
    except TX.DoesNotExist:
        print(f"[ERROR] No existe Texto id={TEXTO_ID}")
        return 1

    antes_pal = len((tx.cuerpo or "").split())
    antes_par = contar_parrafos(tx.cuerpo)
    nuevo_pal = len(NUEVO_CUERPO.split())
    nuevo_par = contar_parrafos(NUEVO_CUERPO)

    print(f"Texto {TEXTO_ID}: {tx.titulo} [{tx.nivel_mcer}]")
    print(f"ANTES: {antes_pal} palabras, {antes_par} párrafos")
    print(f"NUEVO: {nuevo_pal} palabras, {nuevo_par} párrafos")

    if (tx.cuerpo or "") == NUEVO_CUERPO:
        print("[SKIP] El cuerpo ya es el objetivo.")
        return 0
    if not aplicar:
        print("[DRY-RUN] Ejecuta con --apply para guardar.")
        return 0
    tx.cuerpo = NUEVO_CUERPO
    tx.save(update_fields=["cuerpo"])
    print("[OK] Cuerpo actualizado.")
    tx.refresh_from_db()
    print(f"VERIFICADO: {len((tx.cuerpo or '').split())} palabras, {contar_parrafos(tx.cuerpo)} párrafos")
    return 0


if __name__ == "__main__":
    sys.exit(main())