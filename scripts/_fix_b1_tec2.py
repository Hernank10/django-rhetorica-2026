"""_fix_b1_tec2.py - Cierra tec #2 B1: añade explicación + 2do ejercicio (respuesta abierta)."""
import os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

tec = TL.objects.get(nivel_mcer="B1", numero=2)
ejs_tec = list(EJ.objects.filter(tecnica=tec).order_by("orden"))
print(f"Tecnica #2: {tec.titulo}")
print(f"  Ejercicios actuales: {len(ejs_tec)}")

# 1. Añadir explicación al ej existente
if ejs_tec:
    ej = ejs_tec[0]
    payload = dict(ej.payload) if isinstance(ej.payload, dict) else {}
    if "explicacion" not in payload:
        payload["explicacion"] = (
            "Una buena respuesta debe captar la idea global del texto, "
            "no un detalle aislado ni una opinión personal."
        )
        ej.payload = payload
        ej.save(update_fields=["payload"])
        print(f"  [OK] Explicación añadida al ej existente (id={ej.id})")

# 2. Crear 2do ejercicio (mismo tipo: respuesta abierta, otro texto)
textos_usados = {e.texto_id for e in ejs_tec if e.texto_id}
textos_disponibles = list(
    TX.objects.filter(nivel_mcer="B1").exclude(id__in=textos_usados).order_by("id")
)

if len(ejs_tec) >= 2:
    print("  [SKIP] Ya hay 2+ ejercicios")
    sys.exit(0)

if not textos_disponibles:
    print("  [WARN] No hay otro texto disponible. Saltando 2do ej.")
    sys.exit(0)

tx = textos_disponibles[0]
print(f"  Texto elegido para 2do ej: id={tx.id} '{tx.titulo}'")

tipo_original = ejs_tec[0].tipo if ejs_tec and ejs_tec[0].tipo else "respuesta_abierta"

nuevo = EJ.objects.create(
    tecnica=tec,
    texto_id=tx.id,
    enunciado="¿Cuál de las siguientes afirmaciones resume mejor el texto?",
    tipo=tipo_original,
    payload={
        "respuesta_esperada": f"El estudiante debe formular una frase que capture el tema central de '{tx.titulo}'.",
        "criterios": ["Claridad", "Relevancia con el texto", "Síntesis (no copia literal)"],
        "explicacion": (
            f"Una buena respuesta sintetiza la idea principal de '{tx.titulo}', "
            "no repite una frase literal ni menciona un detalle secundario."
        ),
    },
    orden=1,
)
print(f"  [OK] 2do ejercicio creado (id={nuevo.id})")

# Verificar
print(f"\nEstado final tec #2:")
for e in EJ.objects.filter(tecnica=tec).order_by("orden"):
    keys = list(e.payload.keys()) if isinstance(e.payload, dict) else "?"
    print(f"  id={e.id} texto={e.texto_id} keys={keys}")