"""Reemplaza placeholders con contenido real de data/*.json.

- EjercicioLinguistico: contenido.pregunta == '¿Pregunta N?' -> contenido real
- PreguntaEvaluacion: enunciado == 'Pregunta N de ...' -> contenido real

DRY_RUN por defecto. POPULATE_APPLY=1 para aplicar.
"""
import json
import os
import re
from collections import defaultdict
from pathlib import Path

from django.apps import apps

APPLY = os.environ.get("POPULATE_APPLY", "0") == "1"

EjercicioLinguistico = apps.get_model("core", "EjercicioLinguistico")
PreguntaEvaluacion = apps.get_model("core", "PreguntaEvaluacion")

data_dir = Path(r"E:\02_proyectos\django-rhetorica\data")

# Regex placeholder
RE_EJ_PLACEHOLDER = re.compile(r"^¿Pregunta \d+\?$")
RE_PE_PLACEHOLDER = re.compile(r"^Pregunta \d+ de ")

# Categoría del JSON -> categoría del modelo
CAT_MAP = {
    "gramática": "gramatica", "gramatica": "gramatica",
    "sintaxis": "sintaxis", "fonética": "fonetica", "fonetica": "fonetica",
    "fonología": "fonologia", "fonologia": "fonologia",
    "semántica": "semantica", "semantica": "semantica",
    "lexicografía": "lexicografia", "lexicografia": "lexicografia",
    "lingüística": "linguistica", "linguistica": "linguistica",
    "sociolingüística": "sociolinguistica", "sociolinguistica": "sociolinguistica",
    "literatura": "literatura", "periodismo": "periodismo",
    "historia": "historia_castellano", "historia_castellano": "historia_castellano",
    "retórica": "retorica", "retorica": "retorica",
    "antropolingüística": "antropolinguistica", "antropolinguistica": "antropolinguistica",
    "etimología": "etimologia", "etimologia": "etimologia",
}

# ===== 1. Cargar pool de data/*.json =====
print("=" * 60)
print("CARGANDO data/*.json")
print("=" * 60)

pool = []
archivos_ok = []
archivos_err = []
for jf in sorted(data_dir.glob("*.json")):
    try:
        with open(jf, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        archivos_err.append((jf.name, str(e)[:80]))
        continue
    if not isinstance(data, list):
        continue
    for item in data:
        if not isinstance(item, dict):
            continue
        # Normalizar campos (13 archivos + etimologia)
        pregunta = item.get("ejercicio") or item.get("exercise")
        respuesta = item.get("suggestedAnswer")
        titulo = item.get("name") or item.get("element") or ""
        cat_raw = (item.get("category") or "").lower().strip()
        cat = CAT_MAP.get(cat_raw, "gramatica")
        teoria = item.get("teoria") or item.get("meaning") or ""
        ejemplo = item.get("ejemplo") or ""
        if not pregunta or not respuesta:
            continue
        pool.append({
            "pregunta": pregunta,
            "respuesta": respuesta,
            "titulo": titulo,
            "categoria": cat,
            "teoria": teoria,
            "ejemplo": ejemplo,
            "fuente": jf.name,
        })
    archivos_ok.append((jf.name, len(data)))

for name, n in archivos_ok:
    print(f"  OK   {name:40s} {n:3d}")
for name, err in archivos_err:
    print(f"  ERR  {name:40s} {err}")

print(f"\nPool total: {len(pool)} ejercicios reales")

# Agrupar por categoria
by_cat = defaultdict(list)
for item in pool:
    by_cat[item["categoria"]].append(item)

# ===== 2. Placeholders de EjercicioLinguistico =====
print("\n" + "=" * 60)
print("PLACEHOLDERS EjercicioLinguistico")
print("=" * 60)

ejs_placeholder = []
for ej in EjercicioLinguistico.objects.all():
    cont = ej.contenido or {}
    if isinstance(cont, dict):
        preg = cont.get("pregunta", "")
        if isinstance(preg, str) and RE_EJ_PLACEHOLDER.match(preg.strip()):
            ejs_placeholder.append(ej)

print(f"EjercicioLinguistico totales: {EjercicioLinguistico.objects.count()}")
print(f"Placeholders a reemplazar: {len(ejs_placeholder)}")

# Contadores por categoria
used = defaultdict(int)
updates_ej = []
for ej in ejs_placeholder:
    cat = (ej.categoria or "").lower().strip() or "gramatica"
    candidates = by_cat.get(cat) or pool  # fallback global
    if not candidates:
        continue
    idx = used[cat] % len(candidates)
    item = candidates[idx]
    used[cat] += 1
    updates_ej.append((ej, item))

# Samples
print(f"\n=== 3 samples (de {len(updates_ej)} a reemplazar) ===")
for ej, item in updates_ej[:3]:
    print(f"\n  ej.id={ej.id} cat={ej.categoria}")
    print(f"    OLD: {ej.contenido.get('pregunta', '')[:60]}")
    print(f"    NEW: {item['pregunta'][:60]}")
    print(f"         -> {item['respuesta'][:60]}")

# Aplicar
if APPLY and updates_ej:
    for ej, item in updates_ej:
        ej.titulo = item["titulo"] or ej.titulo  # keep titulo if empty
        ej.contenido = {
            "pregunta": item["pregunta"],
            "respuesta": item["respuesta"],
            "teoria": item["teoria"],
            "ejemplo": item["ejemplo"],
            "fuente": item["fuente"],
        }
        ej.save(update_fields=["titulo", "contenido"])
    print(f"\n[OK] {len(updates_ej)} EjercicioLinguistico actualizados")

# ===== 3. Placeholders de PreguntaEvaluacion =====
print("\n" + "=" * 60)
print("PLACEHOLDERS PreguntaEvaluacion")
print("=" * 60)

pes_placeholder = []
for pe in PreguntaEvaluacion.objects.all():
    enunciado = pe.enunciado or ""
    if RE_PE_PLACEHOLDER.match(enunciado):
        pes_placeholder.append(pe)

print(f"PreguntaEvaluacion totales: {PreguntaEvaluacion.objects.count()}")
print(f"Placeholders a reemplazar: {len(pes_placeholder)}")

used_pe = defaultdict(int)
updates_pe = []
for pe in pes_placeholder:
    # Preferir ejercicio vinculado (ya actualizado)
    if pe.ejercicio and isinstance(pe.ejercicio.contenido, dict):
        linked = pe.ejercicio.contenido
        if not RE_EJ_PLACEHOLDER.match(linked.get("pregunta", "")):
            updates_pe.append((pe, {
                "pregunta": linked.get("pregunta", ""),
                "respuesta": linked.get("respuesta", ""),
            }))
            continue
    # Fallback: pool por categoria del curso
    cat = "gramatica"
    try:
        curso = pe.evaluacion.curso
        # buscar en el pool por el nombre del curso
        if curso and curso.titulo:
            cat = next((k for k in by_cat if k in curso.titulo.lower()), "gramatica")
    except Exception:
        pass
    candidates = by_cat.get(cat) or pool
    if not candidates:
        continue
    idx = used_pe[cat] % len(candidates)
    item = candidates[idx]
    used_pe[cat] += 1
    updates_pe.append((pe, item))

print(f"\n=== 3 samples (de {len(updates_pe)} a reemplazar) ===")
for pe, item in updates_pe[:3]:
    print(f"\n  pe.id={pe.id} tipo={pe.tipo}")
    print(f"    OLD: {pe.enunciado[:60]}")
    print(f"    NEW: {item['pregunta'][:60]}")
    print(f"         -> {item['respuesta'][:60]}")

if APPLY and updates_pe:
    for pe, item in updates_pe:
        pe.enunciado = item["pregunta"]
        pe.respuesta_correcta = item["respuesta"]
        pe.save(update_fields=["enunciado", "respuesta_correcta"])
    print(f"\n[OK] {len(updates_pe)} PreguntaEvaluacion actualizadas")

# ===== Resumen final =====
print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"Pool ejercicios reales:       {len(pool)}")
print(f"Archivos JSON parseados:      {len(archivos_ok)}/{len(archivos_ok) + len(archivos_err)}")
print(f"Archivos JSON con error:      {len(archivos_err)}")
print(f"EjercicioLinguistico a act.:  {len(updates_ej)}")
print(f"EjercicioLinguistico quedan:  {len(ejs_placeholder) - len(updates_ej)} (placeholders)")
print(f"PreguntaEvaluacion a act.:    {len(updates_pe)}")

if not APPLY:
    print("\n[DRY_RUN] Sin cambios. Para aplicar:")
    print("  $env:POPULATE_APPLY='1'")
    print("  E:\\PythonPortable_Django5\\python.exe manage.py shell -c \"exec(open('scripts/populate_from_data.py', encoding='utf-8').read())\"")
    print("  $env:POPULATE_APPLY='0'")