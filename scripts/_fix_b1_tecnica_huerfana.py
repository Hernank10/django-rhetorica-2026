"""_fix_b1_tecnica_huerfana.py"""
import os, sys
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")

tec_count = Counter(EJ.objects.filter(tecnica__nivel_mcer="B1").values_list("tecnica_id", flat=True))
huerfanas = [t for t in TL.objects.filter(nivel_mcer="B1") if tec_count.get(t.id, 0) == 1]

print(f"Técnicas con 1 ej: {len(huerfanas)}")
for t in huerfanas:
    ej = EJ.objects.filter(tecnica=t).first()
    print(f"  tec #{t.numero}: {t.titulo}")
    print(f"    enunciado: {ej.enunciado[:80] if ej else '?'}")
    print(f"    payload: {type(ej.payload).__name__ if ej else '?'}")
    if ej:
        print(f"    keys: {list(ej.payload.keys()) if isinstance(ej.payload, dict) else 'N/A'}")