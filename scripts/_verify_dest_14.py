import os, sys, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

reassign = {
    276: 16, 1433: 13, 871: 16, 1409: 52, 834: 47,
    836: 47, 837: 47, 1442: 13, 1374: 47, 1345: 47,
}

def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())

for ej_id, tx_id in reassign.items():
    try:
        ej = EJ.objects.get(id=ej_id)
    except EJ.DoesNotExist:
        print(f"[SKIP] ej.id={ej_id} NO EXISTE"); continue
    try:
        tx = TX.objects.get(id=tx_id)
    except TX.DoesNotExist:
        print(f"[ERROR] tx.id={tx_id} NO EXISTE"); continue
    dup = EJ.objects.filter(texto_id=tx_id).exclude(id=ej_id)
    dup = [d for d in dup if norm(d.enunciado) == norm(ej.enunciado)]
    if dup:
        print(f"[WARN] ej.id={ej_id} -> tx {tx_id} ({tx.titulo}): DUPLICADO con {[d.id for d in dup]} -> delete()")
    else:
        print(f"[OK]   ej.id={ej_id} -> tx {tx_id} ({tx.titulo}) sin duplicado")