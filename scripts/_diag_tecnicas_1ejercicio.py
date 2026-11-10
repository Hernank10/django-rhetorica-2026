"""_diag_tecnicas_1ejercicio.py - Lista técnicas A1 con solo 1 ejercicio."""
import os, sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")

print("=" * 78)
print("TÉCNICAS A1 CON 1 SOLO EJERCICIO (necesitan segundo)")
print("=" * 78)

# Contar ejercicios por técnica
contador = Counter(EJ.objects.filter(tecnica__nivel_mcer="A1").values_list("tecnica_id", flat=True))

tecnicas_1ej = []
tecnicas_0ej = []
for t in TL.objects.filter(nivel_mcer="A1").order_by("numero"):
    n = contador.get(t.id, 0)
    if n == 0:
        tecnicas_0ej.append(t)
    elif n == 1:
        tecnicas_1ej.append(t)

print(f"\n  Técnicas sin ejercicio:  {len(tecnicas_0ej)}")
print(f"  Técnicas con 1 ejercicio: {len(tecnicas_1ej)}")
print(f"  Técnicas con 2 ejercicios: {sum(1 for n in contador.values() if n >= 2)}")

print(f"\n  TÉCNICAS CON 1 EJERCICIO:")
for t in tecnicas_1ej:
    print(f"    #{t.numero:>3} [{t.proceso}]  {t.titulo[:60]}")

if tecnicas_0ej:
    print(f"\n  TÉCNICAS SIN NINGÚN EJERCICIO (grave):")
    for t in tecnicas_0ej:
        print(f"    #{t.numero:>3} [{t.proceso}]  {t.titulo[:60]}")

# Resumen por proceso
from collections import Counter as C2
por_proc = C2(t.proceso for t in tecnicas_1ej)
print(f"\n  Por proceso:")
for proc in ("P1", "P2", "P3", "P4"):
    n = por_proc.get(proc, 0)
    if n > 0:
        print(f"    {proc}: {n} técnicas con 1 ejercicio")