"""Mejora distractores de multiple_choice agrupando por category del JSON."""
import json
import os
import random
from pathlib import Path

from django.apps import apps

APPLY = os.environ.get("DISTRACT_APPLY", "0") == "1"

PreguntaEval = apps.get_model("core", "PreguntaEvaluacion")
data_dir = Path(r"E:\02_proyectos\django-rhetorica\data")

# Cargar todos los items por categoria JSON
items_por_cat = {}
for jf in sorted(data_dir.glob("*.json")):
    try:
        d = json.loads(jf.read_text(encoding="utf-8"))
        if isinstance(d, list):
            items_por_cat[jf.stem] = d
    except Exception:
        pass

# Index: respuesta -> lista de (categoria_json, category_item)
index_por_respuesta = {}
for cat_json, items in items_por_cat.items():
    for item in items:
        resp = (item.get("suggestedAnswer") or "").strip()
        if resp:
            index_por_respuesta.setdefault(resp, []).append(
                (cat_json, (item.get("category") or "").strip(), item)
            )

random.seed(42)
updates = []

for pe in PreguntaEval.objects.filter(tipo="multiple_choice"):
    resp = (pe.respuesta_correcta or "").strip()
    if not resp:
        continue
    matches = index_por_respuesta.get(resp, [])
    if not matches:
        continue

    cat_json, category_item, item_origen = matches[0]
    pool = items_por_cat.get(cat_json, [])

    # Preferir distractores de la misma category
    misma_cat = [
        x.get("suggestedAnswer") for x in pool
        if (x.get("category") or "").strip() == category_item
        and (x.get("suggestedAnswer") or "").strip() != resp
        and x.get("suggestedAnswer")
    ]

    if len(misma_cat) >= 3:
        wrongs = misma_cat
    else:
        # Fallback: mismo JSON
        wrongs = [
            x.get("suggestedAnswer") for x in pool
            if (x.get("suggestedAnswer") or "").strip() != resp
            and x.get("suggestedAnswer")
        ]

    random.shuffle(wrongs)
    opciones = [resp] + wrongs[:3]
    random.shuffle(opciones)

    if opciones != (pe.opciones or []):
        updates.append({
            "pe": pe,
            "category": category_item,
            "antes": pe.opciones,
            "nuevo": opciones,
        })

print(f"Total multiple_choice: {PreguntaEval.objects.filter(tipo='multiple_choice').count()}")
print(f"A actualizar: {len(updates)}")

if updates:
    print("\n=== 3 muestras ===")
    for u in updates[:3]:
        print(f"\n  PE id={u['pe'].id} cat_item={u['category']}")
        print(f"    respuesta: {u['pe'].respuesta_correcta[:60]}")
        print(f"    antes: {u['antes']}")
        print(f"    nuevo: {u['nuevo']}")

if APPLY:
    for u in updates:
        u["pe"].opciones = u["nuevo"]
        u["pe"].save(update_fields=["opciones"])
    print(f"\n[OK] {len(updates)} distractores actualizados")
else:
    print("\n[DRY_RUN] Aplicar: $env:DISTRACT_APPLY='1'")