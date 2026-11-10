import pathlib
import os, sys, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps

TX = apps.get_model("core", "Texto")

def wc(text):
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

def recortar_por_parrafos(cuerpo, max_w):
    """Quita parrafos del final hasta bajar de max_w palabras."""
    parrafos = re.split(r"\n\s*\n", cuerpo.strip())
    while wc("\n\n".join(parrafos)) > max_w and len(parrafos) > 1:
        parrafos.pop()
    return "\n\n".join(parrafos), len(parrafos)

MIN_W, MAX_W = 700, 1200
plan = []

for tx_id in (33, 34, 35):
    tx = TX.objects.get(id=tx_id)
    cuerpo_orig = tx.cuerpo
    w_orig = wc(cuerpo_orig)
    if w_orig <= MAX_W:
        print(f"  [SKIP] id={tx_id} ya esta en rango ({w_orig}w)")
        continue
    cuerpo_new, n_parrafos = recortar_por_parrafos(cuerpo_orig, MAX_W)
    w_new = wc(cuerpo_new)
    ok = MIN_W <= w_new <= MAX_W
    plan.append((tx, cuerpo_new, w_orig, w_new, n_parrafos, ok))
    print(f"  id={tx_id}: {w_orig}w -> {w_new}w  ({w_new - w_orig:+d})  parrafos={n_parrafos}  [{'OK' if ok else 'FUERA'}]")

if "--apply" in sys.argv:
    print("\n[APLICAR]")
    for tx, cuerpo_new, w_orig, w_new, n_parrafos, ok in plan:
        if ok and cuerpo_new != tx.cuerpo:
            tx.cuerpo = cuerpo_new
            tx.save(update_fields=["cuerpo"])
            print(f"  [OK] id={tx.id}  {w_orig}w -> {w_new}w")

    print("\n[VERIFICAR]")
    textos = list(TX.objects.filter(nivel_mcer="C2").order_by("id"))
    en_rango = 0
    for t in textos:
        w = wc(t.cuerpo)
        ok = MIN_W <= w <= MAX_W
        en_rango += int(ok)
        print(f"  [{'OK ' if ok else 'FUERA'}] id={t.id:>3}  {w:>4}w  {t.titulo[:55]}")
    print(f"\n  En rango {MIN_W}-{MAX_W}: {en_rango}/{len(textos)}")
else:
    print("\nDRY-RUN. Nada modificado.")
    print("Ejecuta con --apply para escribir.")