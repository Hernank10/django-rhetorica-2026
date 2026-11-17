import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")
TL = apps.get_model("core", "TecnicaLectura")
TX = apps.get_model("core", "Texto")

print("=" * 70)
print("  TECNICAS B1 HUERFANAS (sin ejercicios)")
print("=" * 70)

tecnicas_b1 = TL.objects.filter(nivel_mcer="B1").order_by("numero")
huerfanas = []
for tec in tecnicas_b1:
    n = EJ.objects.filter(tecnica=tec).count()
    if n == 0:
        huerfanas.append(tec)
        print(f"  #{tec.numero:>3}  usos=0  {tec.titulo}")

print(f"\nTotal tecnicas B1: {tecnicas_b1.count()}")
print(f"Tecnicas B1 huerfanas: {len(huerfanas)}")
print()

# Detalle: qué textos B1 usan cada técnica huérfana (si alguno)
for tec in huerfanas:
    textos = TX.objects.filter(nivel_mcer="B1", ejercicios__tecnica=tec).distinct()
    if textos:
        print(f"  #{tec.numero}: usada en textos {[t.id for t in textos]}")
    else:
        print(f"  #{tec.numero}: no usada en ningún texto B1")

print("\n" + "=" * 70)
print("  FIN")
print("=" * 70)