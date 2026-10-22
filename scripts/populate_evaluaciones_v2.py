"""populate_evaluaciones_v2: reemplaza placeholders con contenido real del pool data/*.json.

Placeholders detectados (regex):
    Pregunta N de/del/en/para/sobre ...
    Pregunta N / Pregunta N? / ¿Pregunta N?
    Respuesta N
    a, b, c, d (una sola letra)

DRY_RUN por defecto. Aplicar: POPULATE_APPLY=1
"""
import json
import os
import random
import re
from collections import defaultdict
from pathlib import Path

from django.apps import apps

APPLY = os.environ.get("POPULATE_APPLY", "0") == "1"

PATRONES_ENUNCIADO = [
    re.compile(r"^Pregunta \d+ (de|del|en|para|sobre)\b"),
    re.compile(r"^Pregunta \d+\s*[?.]?\s*$"),
    re.compile(r"^¿Pregunta \d+\?$"),
]
PATRONES_RESPUESTA = [
    re.compile(r"^Respuesta \d+$"),
    re.compile(r"^[a-dA-D]$"),
    re.compile(r"^\s*$"),
]

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


def es_placeholder_enunciado(t):
    if not t:
        return True
    t = t.strip()
    return any(p.match(t) for p in PATRONES_ENUNCIADO)


def es_placeholder_respuesta(t):
    if not t:
        return True
    t = t.strip()
    return any(p.match(t) for p in PATRONES_RESPUESTA)


def categoria_para_curso(titulo):
    tl = (titulo or "").lower()
    for key, cat in CATEGORIA_POR_CURSO.items():
        if key in tl:
            return cat
    return "gramatica"


# === Cargar pool ===
data_dir = Path(r"E:\02_proyectos\django-rhetorica\data")
pool = defaultdict(list)
ok, err = 0, 0
for jf in sorted(data_dir.glob("*.json")):
    try:
        data = json.loads(jf.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            continue
        cat = jf.stem
        for item in data:
            if not isinstance(item, dict):
                continue
            p = item.get("ejercicio") or item.get("exercise")
            r = item.get("suggestedAnswer")
            if not p or not r:
                continue
            pool[cat].append({"pregunta": p, "respuesta": r, "fuente": jf.name})
        ok += 1
    except Exception as e:
        err += 1
        print(f"[ERR] {jf.name}: {e}")

print("=" * 60)
print("POOL CARGADO")
print("=" * 60)
print(f"JSONs OK: {ok}  |  errores: {err}")
for cat, items in sorted(pool.items()):
    print(f"  {cat:22s} {len(items)}")
print(f"  TOTAL                {sum(len(v) for v in pool.values())}")

# === Detectar placeholders ===
PreguntaEvaluacion = apps.get_model("core", "PreguntaEvaluacion")
todas = PreguntaEvaluacion.objects.select_related("evaluacion__curso").all()
a_arreglar = [
    pe for pe in todas
    if es_placeholder_enunciado(pe.enunciado) or es_placeholder_respuesta(pe.respuesta_correcta)
]

print("\n" + "=" * 60)
print("PLACEHOLDERS DETECTADOS")
print("=" * 60)
print(f"Total PE: {todas.count()}")
print(f"Placeholders: {len(a_arreglar)}")

by_curso = defaultdict(int)
for pe in a_arreglar:
    titulo = pe.evaluacion.curso.titulo if pe.evaluacion and pe.evaluacion.curso else "(sin curso)"
    by_curso[titulo] += 1

print(f"\nPor curso:")
for titulo, n in sorted(by_curso.items()):
    cat = categoria_para_curso(titulo)
    pool_size = len(pool.get(cat, []))
    print(f"  {titulo[:45]:45s} n={n:3d}  cat={cat:18s} pool={pool_size}")

# === Generar updates ===
random.seed(42)
used = defaultdict(int)
updates = []
for pe in a_arreglar:
    titulo = pe.evaluacion.curso.titulo if pe.evaluacion and pe.evaluacion.curso else ""
    cat = categoria_para_curso(titulo)
    items = pool.get(cat) or pool.get("gramatica") or []
    if not items:
        continue
    idx = used[cat] % len(items)
    item = items[idx]
    used[cat] += 1

    opciones = []
    if pe.tipo in ("multiple", "multiple_choice"):
        wrongs = [x["respuesta"] for x in items if x["respuesta"] != item["respuesta"]]
        random.shuffle(wrongs)
        opciones = [item["respuesta"]] + wrongs[:3]
        random.shuffle(opciones)

    updates.append({
        "pe": pe, "cat": cat, "curso": titulo,
        "nuevo_enunciado": item["pregunta"],
        "nueva_respuesta": item["respuesta"],
        "nuevas_opciones": opciones,
        "fuente": item["fuente"],
    })

print("\n" + "=" * 60)
print(f"UPDATES GENERADOS: {len(updates)}")
print("=" * 60)
for u in updates[:5]:
    print(f"\n  PE id={u['pe'].id} tipo={u['pe'].tipo} curso={u['curso'][:30]}")
    print(f"    OLD enunciado:  {u['pe'].enunciado[:65]}")
    print(f"    NEW enunciado:  {u['nuevo_enunciado'][:65]}")
    print(f"    NEW respuesta:  {u['nueva_respuesta'][:65]}")
    if u['nuevas_opciones']:
        print(f"    opciones:       {len(u['nuevas_opciones'])}  -> {u['nuevas_opciones'][:2]}")
    print(f"    fuente:         {u['fuente']}")

if APPLY:
    for u in updates:
        pe = u["pe"]
        pe.enunciado = u["nuevo_enunciado"]
        pe.respuesta_correcta = u["nueva_respuesta"]
        if u["nuevas_opciones"]:
            pe.opciones = u["nuevas_opciones"]
        pe.save(update_fields=["enunciado", "respuesta_correcta", "opciones"])
    print(f"\n[OK] {len(updates)} PreguntasEvaluacion actualizadas")
else:
    print(f"\n[DRY_RUN] Sin cambios.")
    print(f"  Para aplicar:")
    print(f"    $env:POPULATE_APPLY='1'")
    print(f"    python manage.py shell -c \"exec(open('scripts/populate_evaluaciones_v2.py', encoding='utf-8').read())\"")
    print(f"    $env:POPULATE_APPLY='0'")