"""Reasigna ejercicios_relacionados con offset rotativo (evita repetir)."""
import os
from collections import defaultdict

from django.apps import apps

APPLY = os.environ.get("OFFSET_APPLY", "0") == "1"

Leccion = apps.get_model("core", "Leccion")
Ejercicio = apps.get_model("core", "EjercicioLinguistico")

# Agrupar por categoria
CATEGORIA_POR_CURSO = {
    "sintaxis": "sintaxis", "morfolog": "gramatica", "ortograf": "gramatica",
    "gramatic": "gramatica", "literatur": "literatura", "poes": "literatura",
    "retoric": "retorica", "oratori": "retorica", "argumenta": "retorica",
    "enso": "literatura", "comprensi": "linguistica", "lectura": "linguistica",
    "etimolog": "etimologia", "filolog": "etimologia",
    "fonet": "fonetica", "fonolog": "fonologia",
    "semantic": "semantica", "lexicograf": "lexicografia",
    "sociolinguist": "sociolinguistica", "psicolinguist": "psicolinguistica",
    "semiotic": "semiotica", "antropolinguist": "antropolinguistica",
    "historia": "historia_castellano", "periodis": "periodismo",
    "linguist": "linguistica",
}


def categoria_para_curso(titulo):
    tl = (titulo or "").lower()
    for key, cat in CATEGORIA_POR_CURSO.items():
        if key in tl:
            return cat
    return "gramatica"


# Todos los ejercicios por categoria
ejs_por_cat = defaultdict(list)
for ej in Ejercicio.objects.order_by("id"):
    ejs_por_cat[ej.categoria].append(ej)

print("Ejercicios por categoria (top 10):")
for cat, items in list(ejs_por_cat.items())[:10]:
    print(f"  {cat:22s} {len(items)}")

# Iterar lecciones ordenadas por (curso, modulo, orden)
lecciones = Leccion.objects.select_related("modulo__curso").order_by(
    "modulo__curso_id", "modulo__orden", "orden"
)

used = defaultdict(int)  # cat -> offset actual
updates = []

for lec in lecciones:
    cat = categoria_para_curso(lec.modulo.curso.titulo)
    pool = ejs_por_cat.get(cat, [])
    if not pool:
        continue

    offset = used[cat]
    # Tomar 3 con wraparound
    triple = []
    for i in range(3):
        triple.append(pool[(offset + i) % len(pool)])
    used[cat] = (offset + 3) % len(pool)

    ids = tuple(e.id for e in triple)
    actuales = tuple(lec.ejercicios_relacionados.values_list("id", flat=True))
    if ids != actuales:
        updates.append((lec, triple, cat, offset))

print(f"\nLecciones a actualizar: {len(updates)}")

if updates:
    print("\n=== 5 muestras ===")
    for lec, triple, cat, offset in updates[:5]:
        actuales = tuple(lec.ejercicios_relacionados.values_list("id", flat=True)[:3])
        print(f"  LEC id={lec.id} | {lec.titulo[:40]}")
        print(f"    cat={cat:18s} offset={offset:3d}")
        print(f"    antes: {actuales}")
        print(f"    nuevo: {tuple(e.id for e in triple)}")

if APPLY:
    for lec, triple, _, _ in updates:
        lec.ejercicios_relacionados.set(triple)
    print(f"\n[OK] {len(updates)} lecciones actualizadas con offset rotativo")
else:
    print("\n[DRY_RUN] Aplicar: $env:OFFSET_APPLY='1'")