import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
TX = apps.get_model("core", "Texto")

nuevo = """Aquel martes por la tarde, Lucía empujó la puerta de la biblioteca del barrio y descubrió que estaba cerrada por obras. Un cartel anunciaba que reabriría en dos semanas. Lucía, que tenía doce años y una sed insaciable de historias, sintió que el corazón le daba un vuelco. No podía esperar dos semanas sin leer. Mientras volvía a casa, se fijó en una puerta pequeña y descuidada que nunca había visto antes, entre la panadería y la ferretería.

La puerta tenía un letrero dorado que decía: 'Biblioteca de libros olvidados'. Lucía dudó un momento, miró a ambos lados de la calle y empujó la puerta. Dentro, el aire olía a papel viejo y a madera. Las estanterías subían hasta el techo, repletas de libros con lomos gastados. Una mujer mayor, de pelo blanco y gafas redondas, levantó la vista de un libro y sonrió. -Bienvenida, Lucía -dijo la mujer-. Te estaba esperando.

Lucía se quedó muda. ¿Quién era aquella mujer? ¿Cómo sabía su nombre? La mujer se llamaba Rosa y le explicó que la biblioteca llevaba cerrada al público más de cincuenta años, pero que seguía abierta para quien de verdad necesitara un libro. -Los libros no se prestan -dijo Rosa-. Se regalan. Pero solo a quien los merece. Rosa le contó que la biblioteca había sido de su padre, un librero que creía que los libros debían circular libremente. Cuando murió, Rosa decidió mantenerla abierta en secreto, solo para lectores de verdad.

Lucía pasó toda la tarde allí. Al anochecer, Rosa le dio un libro pequeño, de tapas azules. -Este es para ti -dijo-. Cuando lo termines, vuelve y te daré otro. Lucía volvió a casa corriendo, con el libro apretado contra el pecho. Esa noche, leyó hasta que se le cerraron los ojos. Al día siguiente volvió a la biblioteca secreta. Rosa la esperaba con otro libro y una sonrisa."""

tx = TX.objects.get(id=7)
print(f"ANTES: {len((tx.cuerpo or '').split())} palabras, {len([p for p in tx.cuerpo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
print(f"NUEVO: {len(nuevo.split())} palabras, {len([p for p in nuevo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
if "--apply" in sys.argv:
    tx.cuerpo = nuevo
    tx.save(update_fields=["cuerpo"])
    print("[OK] Texto 7 actualizado")
else:
    print("[DRY-RUN] Para aplicar: --apply")