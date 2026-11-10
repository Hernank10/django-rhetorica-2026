"""_export_c1_textos.py - Vuelca los 7 textos C1 con sus técnicas asignadas."""
import os, sys, re
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

def wc(text):
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

textos = list(TX.objects.filter(nivel_mcer="C1").order_by("id"))
print(f"=== {len(textos)} TEXTOS C1 ===\n")

tec_por_texto = defaultdict(list)
for ej in EJ.objects.filter(tecnica__nivel_mcer="C1").values("tecnica_id", "texto_id"):
    if ej["tecnica_id"] and ej["texto_id"]:
        tec_por_texto[ej["texto_id"]].append(ej["tecnica_id"])

for tx in textos:
    tec_ids = sorted(set(tec_por_texto.get(tx.id, [])))
    tec_nums = list(TL.objects.filter(id__in=tec_ids).order_by("numero").values_list("numero", flat=True))
    palabras = wc(tx.cuerpo)
    en_rango = "OK" if 450 <= palabras <= 700 else "FUERA"
    print("="*78)
    print(f"[id={tx.id}] {tx.titulo}")
    print(f"tipo={tx.tipo}  palabras={palabras}  [{en_rango}]  tecnicas={len(tec_nums)}")
    print(f"tecnicas: {tec_nums}")
    print("-"*78)
    print(tx.cuerpo)
    print()