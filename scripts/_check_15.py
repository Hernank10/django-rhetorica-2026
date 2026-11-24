import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

tx = TX.objects.get(id=15)
print(f"Texto 15: {tx.titulo}  [{tx.nivel_mcer}]  tipo={getattr(tx,'tipo',None)}")
print(f"Palabras: {len((tx.cuerpo or '').split())}")
print(f"Párrafos: {len([p for p in tx.cuerpo.split(chr(10)+chr(10)) if p.strip()])}")
print()
ejs = list(EJ.objects.filter(texto=tx).select_related("tecnica").order_by("orden","id"))
print(f"Total ejercicios: {len(ejs)}")
print()
for ej in ejs:
    p = ej.payload if isinstance(ej.payload, dict) else {}
    corr = p.get("correcta")
    n_ops = len(p.get("opciones", []) or [])
    print(f"ej.id={ej.id:>5}  tec=#{ej.tecnica.numero if ej.tecnica else '?':>3}  tipo={ej.tipo!r:>18}  orden={ej.orden!r:>4}  n_ops={n_ops}  correcta={corr}  Q: {(ej.enunciado or '')[:70]}")