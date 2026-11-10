"""_diag_tecnicas_a2.py - Lista las 100 tecnicas A2 con titulo, proceso, texto y 1er ej."""
import os, sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

tecnicas = list(TL.objects.filter(nivel_mcer="A2").order_by("numero"))
print(f"=== 100 TECNICAS A2 ===\n")

por_proc = {"P1": [], "P2": [], "P3": [], "P4": []}
for t in tecnicas:
    ejs = list(EJ.objects.filter(tecnica=t).order_by("orden"))
    if not ejs:
        continue
    ej1 = ejs[0]
    tx = TX.objects.filter(id=ej1.texto_id).first() if ej1.texto_id else None
    tx_nombre = tx.titulo[:30] if tx else "(sin texto)"
    por_proc[t.proceso].append({
        "num": t.numero,
        "titulo": t.titulo,
        "n_ejs": len(ejs),
        "texto": tx_nombre,
        "enunciado": ej1.enunciado[:70],
    })

for proc in ("P1", "P2", "P3", "P4"):
    print(f"\n{'='*78}")
    print(f"--- {proc} ({len(por_proc[proc])} tecnicas) ---")
    print(f"{'='*78}\n")
    for t in por_proc[proc]:
        marca = "  " if t["n_ejs"] >= 2 else "→ "
        print(f"  {marca}#{t['num']:>3} [{t['n_ejs']}ej] {t['titulo'][:55]}")
        print(f"          texto: {t['texto']}")
        print(f"          1er ej: {t['enunciado']}")
        print()

# Resumen
con_1ej = sum(1 for p in por_proc.values() for t in p if t["n_ejs"] == 1)
con_2ej = sum(1 for p in por_proc.values() for t in p if t["n_ejs"] >= 2)
print(f"\n=== RESUMEN ===")
print(f"  Tecnicas con 1 ej (necesitan segundo): {con_1ej}")
print(f"  Tecnicas con 2+ ej (ya completas):     {con_2ej}")