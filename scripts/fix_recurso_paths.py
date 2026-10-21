"""Arregla Recurso.archivo: prepend 'ejercicios_completos-lengua-castellana/' a 564 rotos.

DRY_RUN = True por defecto. Para aplicar: POPULATE_APPLY=1 en env.
"""
import os
from pathlib import Path
from django.apps import apps

APPLY = os.environ.get("POPULATE_APPLY", "0") == "1"

Recurso = apps.get_model("core", "Recurso")
base = Path(r"E:\02_proyectos\django-rhetorica")
prefix = "ejercicios_completos-lengua-castellana/"

a_arreglar = []
huerfanos = []
for r in Recurso.objects.all():
    arch = r.archivo
    if (base / arch).exists():
        continue
    if (base / prefix / arch).exists():
        a_arreglar.append(r)
    else:
        huerfanos.append(r)

print(f"Recursos totales: {Recurso.objects.count()}")
print(f"A arreglar (prepend '{prefix}'): {len(a_arreglar)}")
print(f"Huerfanos (no recuperables): {len(huerfanos)}")

if a_arreglar:
    print("\n=== 5 samples a arreglar ===")
    for r in a_arreglar[:5]:
        print(f"  ID={r.id} | {r.archivo[:80]}")

if huerfanos:
    print("\n=== 5 huerfanos (ignorados) ===")
    for r in huerfanos[:5]:
        print(f"  ID={r.id} | {r.archivo[:80]}")

if not APPLY:
    print(f"\n[DRY_RUN] Sin cambios. Para aplicar: $env:POPULATE_APPLY='1'; ...")
else:
    for r in a_arreglar:
        r.archivo = prefix + r.archivo
        r.save(update_fields=["archivo"])
    print(f"\n[OK] {len(a_arreglar)} paths arreglados")