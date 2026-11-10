"""_fix_b1_texto2.py"""
import os, sys, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
TX = apps.get_model("core", "Texto")

tx = TX.objects.get(id=2)
cuerpo = tx.cuerpo
# Añadir 2-3 palabras al final
nuevo = cuerpo.replace(
    "la educación ambiental es clave para mejorar estas cifras.",
    "la educación ambiental sigue siendo clave para mejorar estas cifras en el futuro."
)
if nuevo != cuerpo:
    tx.cuerpo = nuevo
    tx.save(update_fields=["cuerpo"])
    print(f"[OK] id=2 actualizado: {len(re.findall(r'\\b[\\wáéíóúñ]+\\b', nuevo))} palabras")
else:
    print("[WARN] No se encontró el fragmento")