"""
Migracion 0028: lectura por nivel.

- Cambia TecnicaLectura.numero de unique=True a unique_together=(nivel_mcer, numero).
- Renumera las 100 tecnicas actuales: cada nivel empieza en 1.

Orden de operaciones (importante):
  1. AlterField: quitar unique=True de numero (permite duplicados temporales)
  2. RunPython: renumerar por nivel (1, 2, 3, ... por cada nivel)
  3. AlterUniqueTogether: anadir unique_together (nivel_mcer, numero)
"""
from django.db import migrations, models


def renumerar_por_nivel(apps, schema_editor):
    """Renumera las tecnicas existentes por nivel.

    Actualmente: A1 tiene 14 (numeros 1, 4, 6, ...), A2 tiene 18, etc.
    Despues: A1 tiene 14 (numeros 1-14), A2 tiene 18 (numeros 1-18), etc.

    Idempotente: si se ejecuta varias veces, el resultado es el mismo
    (ordenar por numero y reasignar 1, 2, 3, ...).
    """
    TecnicaLectura = apps.get_model("core", "TecnicaLectura")
    for nivel in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        tecnicas = TecnicaLectura.objects.filter(
            nivel_mcer=nivel
        ).order_by("numero")
        for i, tec in enumerate(tecnicas, start=1):
            tec.numero = i
            tec.save(update_fields=["numero"])


def reverse_renumerar(apps, schema_editor):
    """No-op. La renumeracion no se puede revertir de forma segura."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0027_lectura_sm2"),
    ]

    operations = [
        # 1. Quitar unique=True de numero
        migrations.AlterField(
            model_name="tecnicalectura",
            name="numero",
            field=models.PositiveIntegerField(),
        ),
        # 2. Renumerar por nivel
        migrations.RunPython(renumerar_por_nivel, reverse_renumerar),
        # 3. Anadir unique_together (nivel_mcer, numero)
        migrations.AlterUniqueTogether(
            name="tecnicalectura",
            unique_together={("nivel_mcer", "numero")},
        ),
    ]
