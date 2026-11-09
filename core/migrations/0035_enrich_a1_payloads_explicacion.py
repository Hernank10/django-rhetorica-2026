"""Data migration: enriquece payloads de ejercicios A1 con explicacion.

Generada manualmente (fix de 0026 con dependency rota).
Aplica la misma logica que _enrich_payloads.py, pero como data migration
para que corra automaticamente en `manage.py migrate` (deploy Render).

- Solo modifica ejercicios reales (no placeholders)
- Solo anade payload["explicacion"] desde TecnicaLectura.explicacion
- Idempotente: si el payload ya tiene explicacion, skip
- Reversible: reverse_code borra la clave "explicacion"
"""
from django.db import migrations

PLACEHOLDER_PATTERNS = [
    "(repaso)",
    "\u00bfA qu\u00e9 t\u00e9cnica corresponde",
    "corresponde esta descripci\u00f3n",
    "\u00bfQu\u00e9 haces para",
]

def _is_placeholder(enunciado):
    if not enunciado:
        return True
    return any(p in enunciado for p in PLACEHOLDER_PATTERNS)


def enrich_a1_payloads(apps, schema_editor):
    EjercicioLectura = apps.get_model("core", "EjercicioLectura")
    TecnicaLectura = apps.get_model("core", "TecnicaLectura")

    a1_ids = list(
        TecnicaLectura.objects.filter(nivel_mcer="A1").values_list("id", flat=True)
    )

    actualizados = 0
    saltados_placeholder = 0
    saltados_ya = 0

    for ej in EjercicioLectura.objects.filter(tecnica_id__in=a1_ids).select_related("tecnica"):
        if _is_placeholder(ej.enunciado):
            saltados_placeholder += 1
            continue
        payload = ej.payload if isinstance(ej.payload, dict) else {}
        if payload.get("explicacion"):
            saltados_ya += 1
            continue
        expl = (getattr(ej.tecnica, "explicacion", "") or "").strip()
        if not expl and ej.tecnica:
            expl = f"Aplica la tecnica: {ej.tecnica.titulo}."
        if not expl:
            continue
        payload = dict(payload)
        payload["explicacion"] = expl[:250]
        ej.payload = payload
        ej.save(update_fields=["payload"])
        actualizados += 1

    print(
        f"  [migration] enriquecidos {actualizados} ejercicios A1 "
        f"(placeholders: {saltados_placeholder}, ya-enriquecidos: {saltados_ya})"
    )


def reverse_enrich(apps, schema_editor):
    EjercicioLectura = apps.get_model("core", "EjercicioLectura")
    TecnicaLectura = apps.get_model("core", "TecnicaLectura")
    a1_ids = list(
        TecnicaLectura.objects.filter(nivel_mcer="A1").values_list("id", flat=True)
    )
    revertidos = 0
    for ej in EjercicioLectura.objects.filter(tecnica_id__in=a1_ids):
        payload = ej.payload if isinstance(ej.payload, dict) else {}
        if "explicacion" not in payload:
            continue
        payload = dict(payload)
        del payload["explicacion"]
        ej.payload = payload
        ej.save(update_fields=["payload"])
        revertidos += 1
    if revertidos:
        print(f"  [migration-reverse] borrada explicacion de {revertidos} ejercicios A1")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0034_alter_tecnicagramatical_nivel"),
    ]
    operations = [
        migrations.RunPython(enrich_a1_payloads, reverse_enrich),
    ]