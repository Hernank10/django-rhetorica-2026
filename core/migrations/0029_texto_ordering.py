"""
Migracion 0029: cambiar ordering de Texto a ["nivel_mcer", "orden"].

Motivo: los textos nuevos A1 (orden 13-16) deben aparecer antes que
los A2, B1, B2 y C1 en la UI. Con ordering=["orden"], los A1 aparecen
al final. Con ordering=["nivel_mcer", "orden"], van primero.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0028_lectura_por_nivel"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="texto",
            options={
                "ordering": ["nivel_mcer", "orden"],
                "verbose_name": "Texto de lectura",
                "verbose_name_plural": "Textos de lectura",
            },
        ),
    ]
