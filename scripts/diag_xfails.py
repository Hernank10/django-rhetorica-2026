"""Diagnostico de los 2 xfails."""
import sys, os, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# ============================================================
# 1) AUTH_USER_MODEL
# ============================================================
safe("=" * 78)
safe("1) AUTH_USER_MODEL y modelo de usuario")
safe("=" * 78)
safe(f"  AUTH_USER_MODEL:      {settings.AUTH_USER_MODEL}")
safe(f"  get_user_model():     {get_user_model()}")

# ============================================================
# 2) Campos de LogroObtenido (para ver el FK user)
# ============================================================
safe("")
safe("=" * 78)
safe("2) MODELO LogroObtenido - campos FK")
safe("=" * 78)

from core.models import LogroObtenido, Logro, CertificacionObtenida

for campo in LogroObtenido._meta.get_fields():
    if hasattr(campo, "name"):
        info = f"  - {campo.name}: {campo.__class__.__name__}"
        if hasattr(campo, "related_model") and campo.related_model:
            info += f"  -> {campo.related_model.__module__}.{campo.related_model.__name__}"
        safe(info)

safe("")
safe("CertificacionObtenida:")
for campo in CertificacionObtenida._meta.get_fields():
    if hasattr(campo, "name"):
        info = f"  - {campo.name}: {campo.__class__.__name__}"
        if hasattr(campo, "related_model") and campo.related_model:
            info += f"  -> {campo.related_model.__module__}.{campo.related_model.__name__}"
        safe(info)

# ============================================================
# 3) VISTA dashboard_gamificacion (actual, lineas 1576-1662)
# ============================================================
safe("")
safe("=" * 78)
safe("3) VISTA dashboard_gamificacion")
safe("=" * 78)

vp = BASE / "core" / "views.py"
c = vp.read_text(encoding="utf-8", errors="replace")
m = re.search(r"def\s+dashboard_gamificacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for l in m.group(0).split("\n")[:50]:
        safe(l)

# ============================================================
# 4) VISTA cambiar_contrasena (actual)
# ============================================================
safe("")
safe("=" * 78)
safe("4) VISTA cambiar_contrasena")
safe("=" * 78)

m = re.search(r"def\s+cambiar_contrasena\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for l in m.group(0).split("\n")[:40]:
        safe(l)

# ============================================================
# 5) Templates existentes que tengan que ver con perfil
# ============================================================
safe("")
safe("=" * 78)
safe("5) TEMPLATES DE PERFIL EXISTENTES")
safe("=" * 78)

for t in BASE.glob("core/templates/**/*.html"):
    nombre = t.name.lower()
    if "perfil" in nombre or "password" in nombre or "contra" in nombre:
        safe(f"  {t.relative_to(BASE)}")

# ============================================================
# 6) Signals que sincronizan User
# ============================================================
safe("")
safe("=" * 78)
safe("6) SIGNALS QUE SINCRONIZAN core.User")
safe("=" * 78)

sp = BASE / "core" / "signals.py"
if sp.exists():
    sc = sp.read_text(encoding="utf-8", errors="replace")
    for i, l in enumerate(sc.split("\n"), 1):
        if "user" in l.lower() or "sync" in l.lower() or "signal" in l.lower():
            safe(f"  {i:3}: {l}")