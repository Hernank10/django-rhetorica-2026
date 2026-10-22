"""populate_lecciones_v2: reemplaza placeholders de Leccion con contenido real del pool.

DRY_RUN por defecto. Aplicar: POPULATE_APPLY=1
"""
import json
import os
import re
from collections import defaultdict
from pathlib import Path

from django.apps import apps
from django.utils.html import escape

APPLY = os.environ.get("POPULATE_APPLY", "0") == "1"

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

PATRON_PLACEHOLDER = re.compile(
    r"^<h2>[^<]+</h2><p>Contenido de [A-Z]\w+\.</p>$|"
    r"^Contenido de [A-Z]\w+\.$|"
    r"^\s*$"
)


def es_placeholder(t):
    if not t or len(t.strip()) < 80:
        return bool(PATRON_PLACEHOLDER.match((t or "").strip()) or len(t.strip()) < 30)
    return False


def categoria_para_curso(titulo):
    tl = (titulo or "").lower()
    for key, cat in CATEGORIA_POR_CURSO.items():
        if key in tl:
            return cat
    return "gramatica"


def generar_html(item):
    """HTML semantico para una leccion desde item del JSON."""
    name = escape(item.get("name", "Tema"))
    categoria = escape(item.get("category", ""))
    teoria = escape(item.get("teoria", ""))
    ejemplo = escape(item.get("ejemplo", ""))

    partes = [f"<h2>{name}</h2>"]
    if categoria:
        partes.append(f'<p class="text-muted"><small>Categoria: {categoria}</small></p>')
    if teoria:
        partes.append("<h4>Teoria</h4>")
        partes.append(f"<p>{teoria}</p>")
    if ejemplo:
        partes.append("<h4>Ejemplo</h4>")
        partes.append(f'<blockquote class="blockquote"><p><em>{ejemplo}</em></p></blockquote>')
    return "\n".join(partes)


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
            if not (item.get("name") and item.get("teoria")):
                continue
            pool[cat].append(item)
        ok += 1
    except Exception as e:
        err += 1
        print(f"[ERR] {jf.name}: {e}")

print("=" * 60)
print("POOL CARGADO (items con name + teoria)")
print("=" * 60)
print(f"JSONs OK: {ok}  |  errores: {err}")
for cat, items in sorted(pool.items()):
    print(f"  {cat:22s} {len(items)}")
print(f"  TOTAL                {sum(len(v) for v in pool.values())}")

# === Detectar placeholders ===
Leccion = apps.get_model("core", "Leccion")
Ejercicio = apps.get_model("core", "EjercicioLinguistico")
Tecnica = apps.get_model("core", "TecnicaLinguistica")

todas = Leccion.objects.select_related("modulo__curso").all()
a_arreglar = [l for l in todas if es_placeholder(l.contenido)]

print("\n" + "=" * 60)
print("PLACEHOLDERS DETECTADOS")
print("=" * 60)
print(f"Total Lecciones: {todas.count()}")
print(f"Placeholders: {len(a_arreglar)}")

by_curso = defaultdict(int)
for l in a_arreglar:
    by_curso[l.modulo.curso.titulo] += 1
print(f"\nPor curso (primeros 10):")
for titulo, n in sorted(by_curso.items())[:10]:
    cat = categoria_para_curso(titulo)
    print(f"  {titulo[:45]:45s} n={n:3d}  cat={cat:18s} pool={len(pool.get(cat, []))}")

# === Generar updates ===
used = defaultdict(int)
updates = []
for lec in a_arreglar:
    titulo_curso = lec.modulo.curso.titulo
    cat = categoria_para_curso(titulo_curso)
    items = pool.get(cat) or pool.get("gramatica") or []
    if not items:
        continue
    idx = used[cat] % len(items)
    item = items[idx]
    used[cat] += 1

    nuevo_html = generar_html(item)

    # Ejercicios de la misma categoria (o primer fallback)
    ejs = list(Ejercicio.objects.filter(categoria=cat)[:3])
    if not ejs:
        ejs = list(Ejercicio.objects.all()[:3])

    # Tecnicas (opcional, si existen)
    tecs = list(Tecnica.objects.filter(categoria=cat)[:2])
    if not tecs:
        tecs = list(Tecnica.objects.all()[:2])

    updates.append({
        "lec": lec,
        "cat": cat,
        "curso": titulo_curso,
        "nuevo_html": nuevo_html,
        "item_name": item.get("name", ""),
        "ejercicios": ejs,
        "tecnicas": tecs,
    })

print("\n" + "=" * 60)
print(f"UPDATES GENERADOS: {len(updates)}")
print("=" * 60)
for u in updates[:5]:
    print(f"\n  LEC id={u['lec'].id} curso={u['curso'][:30]}")
    print(f"    titulo: {u['lec'].titulo[:60]}")
    print(f"    cat: {u['cat']} | item: {u['item_name'][:50]}")
    print(f"    ejercicios a relacionar: {len(u['ejercicios'])}")
    print(f"    tecnicas a relacionar: {len(u['tecnicas'])}")
    print(f"    HTML preview:")
    print(f"    {u['nuevo_html'][:200]}")

if APPLY:
    for u in updates:
        lec = u["lec"]
        lec.contenido = u["nuevo_html"]
        lec.save(update_fields=["contenido"])
        lec.ejercicios_relacionados.set(u["ejercicios"])
        if u["tecnicas"]:
            lec.tecnicas_relacionadas.set(u["tecnicas"])
    print(f"\n[OK] {len(updates)} Lecciones actualizadas")
else:
    print(f"\n[DRY_RUN] Sin cambios.")
    print(f"  Para aplicar: $env:POPULATE_APPLY='1' + rerun")