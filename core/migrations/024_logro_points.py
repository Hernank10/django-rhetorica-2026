"""Migration 024: puntos bonus para los 6 logros MCER (10, 20, 30, 40, 50, 100)."""
from django.db import migrations


PUNTOS = {
    "Primera técnica MCER": 10,
    "Aprendiz MCER": 20,
    "B1 alcanzado": 30,
    "B2 alcanzado": 40,
    "C1 alcanzado": 50,
    "Recorrido MCER completado": 100,
}


def set_logro_points(apps, schema_editor):
    Logro = apps.get_model("core", "Logro")
    for nombre, pts in PUNTOS.items():
        Logro.objects.filter(nombre=nombre).update(puntos_requeridos=pts)


def reverse_points(apps, schema_editor):
    Logro = apps.get_model("core", "Logro")
    Logro.objects.filter(nombre__in=list(PUNTOS)).update(puntos_requeridos=0)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "023_seed_mcer_demo"),  # ← 3 ceros, coincide con el nombre real
    ]
    operations = [
        migrations.RunPython(set_logro_points, reverse_points),
    ]
