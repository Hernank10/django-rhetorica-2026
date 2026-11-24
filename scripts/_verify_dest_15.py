import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

for ej_id, dest_id in [(1403, 13)]:
    try:
        ej = EJ.objects.select_related("texto").get(id=ej_id)
    except EJ.DoesNotExist:
        print(f"[WARN] ej.id={ej_id} NO existe"); continue
    dest = TX.objects.get(id=dest_id)
    dup = EJ.objects.filter(texto_id=dest_id, enunciado=ej.enunciado).exclude(id=ej.id).first()
    print(f"ej.id={ej_id} actual_tx={ej.texto_id} -> destino={dest_id} ({dest.titulo[:40]})")
    print(f"  Q: {(ej.enunciado or '')[:80]}")
    print(f"  {'DUPLICADO con ej.id='+str(dup.id) if dup else 'sin duplicado'}")