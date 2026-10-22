"""Cleanup: elimina 1400 ejercicios placeholder 'item N'.

Diagnostico previo confirmo 0 referencias (PE, ER, M2M Leccion, Recurso).
Borrado directo + backup JSON de IDs eliminados.
"""
import json
import os
from pathlib import Path

from django.apps import apps

APPLY = os.environ.get("CLEANUP_APPLY", "0") == "1"

E = apps.get_model("core", "EjercicioLinguistico")
backup_path = Path(r"E:\02_proyectos\django-rhetorica\scripts\_backup_placeholders.json")

# IDs a borrar
placeholders = E.objects.filter(titulo__iregex=r"^item [0-9]+$")
placeholder_ids = list(placeholders.values_list("id", flat=True))

print(f"Ejercicios totales: {E.objects.count()}")
print(f"Placeholders a borrar: {len(placeholder_ids)}")
print(f"Ejercicios reales que quedarian: {E.objects.count() - len(placeholder_ids)}")

# Detalle por titulo
from collections import Counter
titulos = Counter(placeholders.values_list("titulo", flat=True))
print(f"\nTitulos unicos: {len(titulos)}")
print("Primeros 5:")
for t, n in list(titulos.items())[:5]:
    print(f"  '{t}' x{n}")

if APPLY:
    # Backup
    backup_data = [
        {"id": ej.id, "titulo": ej.titulo, "categoria": ej.categoria}
        for ej in placeholders
    ]
    backup_path.write_text(
        json.dumps(backup_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n[BACKUP] {backup_path.name} ({len(backup_data)} registros)")

    # Delete
    n_deleted, _ = E.objects.filter(titulo__iregex=r"^item [0-9]+$").delete()
    print(f"[OK] {n_deleted} filas eliminadas (incluye M2M auto si habia)")

    # Verificar
    restantes = E.objects.count()
    placeholders_restantes = E.objects.filter(titulo__iregex=r"^item [0-9]+$").count()
    print(f"\n[VERIFY] Ejercicios restantes: {restantes}")
    print(f"[VERIFY] Placeholders restantes: {placeholders_restantes}")

    # Distribucion por categoria
    print("\n=== Distribucion por categoria ===")
    from django.db.models import Count
    for cat in E.objects.values("categoria").annotate(n=Count("id")).order_by("-n")[:15]:
        print(f"  {cat['categoria'] or '(sin)':25s} {cat['n']}")
else:
    print("\n[DRY_RUN] Aplicar: $env:CLEANUP_APPLY='1'")