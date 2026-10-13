"""Ver como _resolver_archivo calcula las rutas."""
import sys, os
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.conf import settings


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


print("=" * 78)
print("SETTINGS DE MEDIA")
print("=" * 78)
safe(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
safe(f"  MEDIA_URL:  {settings.MEDIA_URL}")
safe(f"  BASE_DIR:   {settings.BASE_DIR}")


print()
print("=" * 78)
print("FUNCION _resolver_archivo (primeras 40 lineas de views_recursos.py)")
print("=" * 78)

vp = BASE / "core" / "views_recursos.py"
lineas = vp.read_text(encoding="utf-8", errors="replace").split("\n")
for i, l in enumerate(lineas[:50], 1):
    safe(f"  {i:3}: {l}")