# scripts/_update_body_16.py
# Cierre texto 16 "Los animales de la granja" (A1): cuerpo 1 párrafo -> 4 párrafos (~195 palabras).
# Uso:
#   python scripts\_update_body_16.py            # dry-run
#   python scripts\_update_body_16.py --apply    # aplica
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

TEXTO_ID = 16

NUEVO_CUERPO = (
    "El abuelo de Marta tiene una granja pequeña cerca del pueblo. En la granja viven muchos animales: "
    "vacas, gallinas, cerdos, ovejas y un perro. La granja tiene un corral grande, un establo de madera y "
    "un huerto con tomates. Marta va a la granja todos los sábados por la mañana con su padre.\n\n"
    "Las vacas son grandes y de color blanco y negro. Hay cinco vacas y producen leche cada día. "
    "Las diez gallinas ponen huevos por la mañana y el gallo canta muy temprano. Los cerdos son rosados "
    "y siempre tienen hambre. Las ovejas son blancas y dan lana en primavera.\n\n"
    "El abuelo se levanta a las seis y da de comer a los animales. Primero va al establo y luego al corral. "
    "Marta le ayuda a llenar los cubos de agua y a recoger los huevos. El perro ladra cuando llega un coche. "
    "El gato duerme en el tejado y el reloj de la cocina marca las horas.\n\n"
    "A Marta le gusta mucho la granja. Dice que los cerdos son divertidos y que el gallo es el jefe del corral. "
    "Para ella, el mejor momento es cuando el abuelo le cuenta historias de cuando era joven. "
    "La granja es un lugar tranquilo y feliz."
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