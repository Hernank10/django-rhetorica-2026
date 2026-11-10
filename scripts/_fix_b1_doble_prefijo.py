"""_fix_b1_doble_prefijo.py - Limpia "Según el texto, ¿según el texto, ..." en variantes."""
import os, sys, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")

ejs = EJ.objects.filter(tecnica__nivel_mcer="B1")
cambios = 0
for e in ejs:
    orig = e.enunciado or ""
    # Quitar "Según el texto, ¿según el texto, " (doble prefijo)
    nuevo = re.sub(
        r"^Según el texto,\s*¿?\s*según el texto,\s*¿?\s*",
        "Según el texto, ¿",
        orig, flags=re.IGNORECASE
    )
    # Si aún hay "según el texto" al final sobrante en preguntas meta, quitar
    # (ej: "¿qué relación..., según el texto?" → "¿qué relación...?")
    # Solo si el segundo "según el texto" está al final tras coma
    nuevo = re.sub(
        r",\s*según el texto\?\s*$",
        "?", nuevo, flags=re.IGNORECASE
    )
    if nuevo != orig:
        e.enunciado = nuevo
        e.save(update_fields=["enunciado"])
        cambios += 1
        if cambios <= 10:
            print(f"  tec #{e.tecnica.numero}")
            print(f"    ANTES:   {orig[:90]}")
            print(f"    DESPUES: {nuevo[:90]}")
print(f"\n[OK] {cambios} ejercicios limpiados")