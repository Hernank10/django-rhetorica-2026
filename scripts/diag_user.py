"""Diagnostica los modelos User y las FK que los apuntan."""
import os, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")

import django
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as AuthUser
from core.models import (
    User as CoreUser, LogroObtenido, CertificacionObtenida, Respuesta, Logro,
)
from core.models_cursos import ProgresoUsuario

print("AUTH_USER_MODEL:", settings.AUTH_USER_MODEL)
print("get_user_model():", get_user_model()._meta.label)
print()
print("core.User count:", CoreUser.objects.count())
print("auth.User count:", AuthUser.objects.count())
print()
print("=== FK targets (quién apunta a quién) ===")
for M, campo in [
    (LogroObtenido, "user"),
    (CertificacionObtenida, "user"),
    (Respuesta, "user"),
    (ProgresoUsuario, "usuario"),
]:
    fk = M._meta.get_field(campo)
    print(f"  {M.__name__}.{campo}  ->  {fk.related_model._meta.label}")

print()
print("=== Primeros 5 usuarios de cada modelo ===")
print("core.User:", list(CoreUser.objects.values_list("username", flat=True)[:5]))
print("auth.User:", list(AuthUser.objects.values_list("username", flat=True)[:5]))

print()
print("=== Test: query LogroObtenido con usuario ===")
for etiqueta, modelo, manager in [
    ("core.User", CoreUser, CoreUser.objects),
    ("auth.User", AuthUser, AuthUser.objects),
]:
    est = manager.filter(username="est001").first()
    if not est:
        print(f"  {etiqueta}: no existe est001")
        continue
    try:
        n = LogroObtenido.objects.filter(user=est).count()
        print(f"  {etiqueta}: OK -> {n} logros")
    except Exception as e:
        print(f"  {etiqueta}: ERROR -> {e}")
