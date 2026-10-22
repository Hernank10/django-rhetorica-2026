"""Crea EjercicioLinguistico faltantes desde el pool JSON."""
import json
import os
from pathlib import Path

from django.apps import apps

APPLY = os.environ.get("CREATE_APPLY", "0") == "1"

Ejercicio = apps.get_model("core", "EjercicioLinguistico")
data_dir = Path(r"E:\02_proyectos\django-rhetorica\data")

# Titulos ya en DB
titulos_db = set(Ejercicio.objects.values_list("titulo", flat=True))

# Cargar pool y encontrar faltantes
faltantes = []
for jf in sorted(data_dir.glob("*.json")):
    try:
        d = json.loads(jf.read_text(encoding="utf-8"))
        if not isinstance(d, list):
            continue
        cat = jf.stem
        for item in d:
            titulo = (item.get("name") or "").strip()
            if not titulo or titulo in titulos_db:
                continue
            pregunta = (item.get("ejercicio") or "").strip()
            respuesta = (item.get("suggestedAnswer") or "").strip()
            if not pregunta or not respuesta:
                continue
            faltantes.append({
                "titulo": titulo,
                "contenido": {
                    "pregunta": pregunta,
                    "respuesta": respuesta,
                    "teoria": (item.get("teoria") or "").strip(),
                    "ejemplo": (item.get("ejemplo") or "").strip(),
                    "fuente": jf.name,
                },
                "categoria": cat,
                "tipo": "multiple",
                "nivel": 1,
                "puntos": 10,
                "es_adaptativo": False,
                "es_redaccion": False,
                "idioma": "ES",
            })
    except Exception as e:
        print(f"[ERR] {jf.name}: {e}")

print(f"Ejercicios en DB: {Ejercicio.objects.count()}")
print(f"Faltantes del pool: {len(faltantes)}")

if faltantes:
    print("\n=== 3 muestras ===")
    for f in faltantes[:3]:
        print(f"\n  titulo: {f['titulo'][:60]}")
        print(f"  categoria: {f['categoria']}")
        print(f"  pregunta: {f['contenido']['pregunta'][:80]}")

if APPLY and faltantes:
    for f in faltantes:
        Ejercicio.objects.create(**f)
    print(f"\n[OK] {len(faltantes)} ejercicios creados")
    print(f"Total en DB: {Ejercicio.objects.count()}")
else:
    print("\n[DRY_RUN] Aplicar: $env:CREATE_APPLY='1'")