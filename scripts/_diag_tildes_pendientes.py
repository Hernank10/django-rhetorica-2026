"""_diag_tildes_pendientes.py - Lista ejercicios A2 sin tildes para revision manual."""
import os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps

EJ = apps.get_model("core", "EjercicioLectura")

def tiene_tildes(text):
    if not text:
        return False
    return any(c in text for c in "áéíóúñÁÉÍÓÚÑ¿¡")

ejs = list(EJ.objects.filter(tecnica__nivel_mcer="A2").select_related("tecnica"))

sin_tildes = [e for e in ejs if e.enunciado and not tiene_tildes(e.enunciado)]

print(f"=== EJERCICIOS A2 SIN TILDES: {len(sin_tildes)}/{len(ejs)} ===\n")
for e in sorted(sin_tildes, key=lambda x: x.tecnica.numero):
    print(f"  tec #{e.tecnica.numero:>3}  {e.enunciado[:80]}")
    # Ver si payload tambien falla
    if isinstance(e.payload, dict):
        ops = e.payload.get("opciones", [])
        ops_sin_tildes = [op for op in ops if isinstance(op, str) and not tiene_tildes(op)]
        if ops_sin_tildes:
            print(f"          opciones sin tildes: {len(ops_sin_tildes)}")