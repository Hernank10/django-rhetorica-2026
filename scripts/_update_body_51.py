import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
TX = apps.get_model("core", "Texto")

nuevo = """Me gusta mucho el verano. En verano no hay clases y puedo dormir hasta tarde. Por la mañana desayuno despacio y leo un poco en la terraza. Después, ayudo a mi madre a preparar la comida. Las tardes de verano son largas y tranquilas, y nunca tengo prisa.

Mi familia y yo vamos a la playa en julio. Nadamos en el mar y comemos helado. También me gusta leer libros en la arena, con el sonido de las olas. Mi hermana pequeña hace castillos de arena y mi padre nos hace fotos. Por la noche, volvemos al hotel cansados pero muy contentos.

No me gusta el invierno porque hace mucho frío y llueve. En invierno solo quiero quedarme en casa con una manta y ver películas. A veces mis amigos me llaman para salir, pero casi nunca quiero. Echo de menos el sol, la playa y los días sin horarios.

Por eso prefiero el verano: el sol, la playa y las vacaciones. Me gustan los días largos, el helado de limón y nadar en el mar. Cuando llega septiembre, ya estoy esperando el próximo verano. El verano es, sin duda, mi estación favorita."""

tx = TX.objects.get(id=51)
print(f"ANTES: {len((tx.cuerpo or '').split())} palabras, {len([p for p in tx.cuerpo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
print(f"NUEVO: {len(nuevo.split())} palabras, {len([p for p in nuevo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
if "--apply" in sys.argv:
    tx.cuerpo = nuevo
    tx.save(update_fields=["cuerpo"])
    print("[OK] Texto 51 actualizado")
else:
    print("[DRY-RUN] Para aplicar: --apply")