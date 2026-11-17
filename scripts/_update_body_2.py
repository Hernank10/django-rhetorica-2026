import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
TX = apps.get_model("core", "Texto")

nuevo = """El reciclaje de vidrio es una práctica consolidada en España. Cada año, los ciudadanos depositan millones de envases en los contenedores verdes que se encuentran en las calles. Según datos de Ecovidrio, en 2023 se reciclaron más de 900.000 toneladas de vidrio, lo que supone un aumento del 5% respecto al año anterior. El vidrio es uno de los materiales más reciclables y su proceso es relativamente sencillo.

Primero, los ciudadanos separan los envases de vidrio en sus hogares y los llevan al contenedor correspondiente. Después, camiones especiales recogen el material y lo transportan a plantas de tratamiento. Allí, el vidrio se limpia, se tritura y se funde a altas temperaturas. El vidrio reciclado puede utilizarse para fabricar nuevos envases sin perder calidad.

El vidrio puede reciclarse infinitas veces sin degradarse. Además, reciclar vidrio ahorra energía y reduce las emisiones de CO2. Por eso, el reciclaje de vidrio tiene una consecuencia muy positiva para el medio ambiente: menos residuos en vertederos y menos contaminación. Muchas familias ya han incorporado este hábito a su rutina diaria.

Sin embargo, aún queda trabajo por hacer. Muchos envases todavía acaban en vertederos, y algunas regiones tienen tasas de reciclaje muy bajas. Los expertos coinciden en que la educación ambiental sigue siendo clave para mejorar estas cifras en el futuro. El texto cita la fábula de 'La cigarra y la hormiga' para recordar que el esfuerzo constante tiene recompensa."""

tx = TX.objects.get(id=2)
print(f"ANTES: {len((tx.cuerpo or '').split())} palabras, {len([p for p in tx.cuerpo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
print(f"NUEVO: {len(nuevo.split())} palabras, {len([p for p in nuevo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
if "--apply" in sys.argv:
    tx.cuerpo = nuevo
    tx.save(update_fields=["cuerpo"])
    print("[OK] Texto 2 actualizado")
else:
    print("[DRY-RUN] Para aplicar: --apply")