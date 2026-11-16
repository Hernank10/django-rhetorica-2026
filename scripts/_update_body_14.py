import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
TX = apps.get_model("core", "Texto")

nuevo = """Mi escuela se llama San Martín y está en el centro de la ciudad. Es un edificio grande, de color amarillo, con tres pisos y muchas aulas. Delante hay una puerta verde y un jardín pequeño con flores. Todos los días entro a las nueve de la mañana con mis compañeros.

En la planta baja están la biblioteca y la cafetería. La biblioteca tiene muchos libros y mesas para estudiar. En la cafetería vendemos zumos y bocadillos. En el patio hay árboles grandes y bancos de madera para sentarse. También hay una canasta de baloncesto y una portería de fútbol. En el recreo jugamos al fútbol y hablamos con los amigos.

Mi clase favorita es la de música, porque el profesor es muy divertido: toca la guitarra y nos enseña canciones. También me gusta la clase de dibujo. Mis compañeros son simpáticos y siempre me ayudan con los deberes. La profesora de matemáticas es seria pero muy buena.

Me gusta mucho mi escuela. Por la mañana aprendemos y por la tarde hacemos deportes y talleres. El viernes por la tarde hay cine en el salón de actos. Mi escuela es grande, amarilla y siempre está llena de gente. Para mí, es el mejor lugar del mundo después de casa."""

tx = TX.objects.get(id=14)
print(f"ANTES: {len((tx.cuerpo or '').split())} palabras, {len([p for p in tx.cuerpo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
print(f"NUEVO: {len(nuevo.split())} palabras, {len([p for p in nuevo.split(chr(10)+chr(10)) if p.strip()])} párrafos")
if "--apply" in sys.argv:
    tx.cuerpo = nuevo
    tx.save(update_fields=["cuerpo"])
    print("[OK] Texto 14 actualizado")
else:
    print("[DRY-RUN] Para aplicar: --apply")