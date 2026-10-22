"""Crea 100 flashcards de sintaxis desde data/sintaxis.json para un usuario.

DRY_RUN: PASS_POPULATE=1 aplica.
Idempotente: (estudiante, fuente_id) unico.
Importable: populate(user, apply=False) retorna dict con counts.
"""
import json
import os
from pathlib import Path

from django.apps import apps


def populate(user, apply=False):
    Flashcard = apps.get_model("core", "Flashcard")
    data_dir = Path(r"E:\02_proyectos\django-rhetorica\data")
    src = data_dir / "sintaxis.json"
    items = json.loads(src.read_text(encoding="utf-8"))

    creados, existentes, sin_datos = 0, 0, 0
    preview = []

    for item in items:
        name = (item.get("name") or "").strip()
        teoria = (item.get("teoria") or "").strip()
        if not name or not teoria:
            sin_datos += 1
            continue

        defaults = {
            "tipo": "regla",
            "idioma": "ES",
            "frente": name,
            "reverso": teoria[:300],
            "explicacion": teoria,
            "ejemplo": (item.get("ejemplo") or "").strip(),
            "ejercicio": (item.get("ejercicio") or "").strip(),
            "respuesta_ejercicio": (item.get("suggestedAnswer") or "").strip(),
            "categoria_gramatical": (item.get("category") or "sintaxis").strip(),
        }

        if apply:
            obj, created = Flashcard.objects.get_or_create(
                estudiante=user, fuente_id=item["id"], defaults=defaults
            )
            if created:
                creados += 1
            else:
                existentes += 1
        else:
            exists = Flashcard.objects.filter(
                estudiante=user, fuente_id=item["id"]
            ).exists()
            if exists:
                existentes += 1
            else:
                creados += 1
                if len(preview) < 3:
                    preview.append(defaults)

    return {
        "total": len(items),
        "creados": creados,
        "existentes": existentes,
        "sin_datos": sin_datos,
        "preview": preview,
    }


if __name__ == "__main__":
    from django.contrib.auth.models import User

    APPLY = os.environ.get("PASS_POPULATE", "0") == "1"
    target = User.objects.filter(username="est001").first()
    if not target:
        target = User.objects.filter(groups__name="Estudiante").first()
    if not target:
        print("[!] no hay usuario estudiante")
    else:
        print(f"=== populate_flashcards_sintaxis ===")
        print(f"Usuario: {target.username}")
        print(f"Modo: {'APLICAR' if APPLY else 'DRY_RUN'}")
        r = populate(target, apply=APPLY)
        print(f"Total items: {r['total']}")
        print(f"Creados: {r['creados']}")
        print(f"Existentes: {r['existentes']}")
        print(f"Sin datos: {r['sin_datos']}")
        if r["preview"]:
            print("\n=== 3 samples ===")
            for p in r["preview"]:
                print(f"\n  frente: {p['frente'][:60]}")
                print(f"  categoria: {p['categoria_gramatical']}")
                print(f"  explicacion: {p['explicacion'][:80]}")
                print(f"  ejercicio: {p['ejercicio'][:80]}")
                print(f"  respuesta: {p['respuesta_ejercicio'][:80]}")
        if not APPLY:
            print("\n[DRY_RUN] Aplicar: $env:PASS_POPULATE='1'")