import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
TX = apps.get_model("core", "Texto")

nuevo = """Me llamo Carlos y tengo veinticinco años. Vivo en Madrid con mi familia. Mi padre se llama Juan y es médico. Mi madre se llama María y trabaja en una tienda del barrio. Tengo una hermana pequeña, Lucía. Ella tiene ocho años y va a la escuela. También tengo un perro que se llama Toby. Toby es pequeño, de color marrón, y siempre quiere jugar conmigo.

Los domingos comemos todos juntos en casa de mis abuelos. Mi abuela cocina muy bien: hace sopa, tortilla y un pastel de manzana. Después de comer, mi abuelo cuenta historias de cuando era joven. A Lucía le gustan mucho esas historias. Mi padre y mi madre hablan de trabajo, y yo juego con Toby en el jardín. Por la tarde volvemos a casa cansados pero muy contentos.

Me gusta mucho mi familia. Mi padre es serio pero muy bueno. Mi madre es alegre y siempre nos ayuda con los deberes. Lucía es pequeña, pero muy lista: ya sabe leer y escribir. Toby es el más juguetón de la casa. Los domingos son mi día favorito porque estamos todos juntos.

En verano vamos a la playa con mis abuelos. Nadamos en el mar, comemos helado y hacemos castillos de arena. Lucía se ríe mucho cuando Toby corre detrás de las olas. Por la noche, mi abuelo cuenta otra historia y mi abuela nos da un vaso de leche caliente. El verano con mi familia es lo mejor del año."""

tx = TX.objects.get(id=48)
print(f"ANTES: {len((tx.cuerpo or '').split())} palabras, {len([p for p in tx.cuerpo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
print(f"NUEVO: {len(nuevo.split())} palabras, {len([p for p in nuevo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
if "--apply" in sys.argv:
    tx.cuerpo = nuevo
    tx.save(update_fields=["cuerpo"])
    print("[OK] Texto 48 actualizado")
else:
    print("[DRY-RUN] Para aplicar: --apply")