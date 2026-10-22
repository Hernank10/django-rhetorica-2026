"""Elimina Recursos con archivo inexistente (huerfanos)."""
import os
from pathlib import Path
from django.apps import apps

APPLY = os.environ.get("CLEAN_APPLY", "0") == "1"
Recurso = apps.get_model("core", "Recurso")
base = Path(r"E:\02_proyectos\django-rhetorica")

a_borrar = [r for r in Recurso.objects.all() if not (base / r.archivo).exists()]

print(f"Recursos totales: {Recurso.objects.count()}")
print(f"A borrar (archivo no existe): {len(a_borrar)}")

if a_borrar:
    print("\n=== 5 muestras ===")
    for r in a_borrar[:5]:
        print(f"  ID={r.id} | {r.archivo}")

if APPLY:
    ids = [r.id for r in a_borrar]
    Recurso.objects.filter(id__in=ids).delete()
    print(f"\n[OK] {len(ids)} recursos eliminados")
    print(f"Recursos despues: {Recurso.objects.count()}")
else:
    print("\n[DRY_RUN] Aplicar: $env:CLEAN_APPLY='1'")