"""Mide el estado actual de las tablas de usuario (solo lectura)."""
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.contrib.auth.models import User as AuthUser
from core.models import (
    User as CoreUser, ProgresoCategoria, ResultadoEvaluacion,
    Respuesta, LogroObtenido, CertificacionObtenida,
)
from core.models_cursos import Curso
from core.models_preguntas import PreguntaGenerada, RespuestaPregunta

print("=" * 72)
print("MEDICION DE TABLAS DE USUARIO")
print("=" * 72)

n_auth = AuthUser.objects.count()
n_core = CoreUser.objects.count()
print(f"auth.User (django.contrib.auth)     : {n_auth}")
print(f"core.User (paralelo)                : {n_core}")

auth_u = set(AuthUser.objects.values_list("username", flat=True))
core_u = set(CoreUser.objects.values_list("username", flat=True))
print(f"solo en auth.User                   : {len(auth_u - core_u)}")
print(f"solo en core.User                   : {len(core_u - auth_u)}")
print(f"en ambos (sincronizados)            : {len(auth_u & core_u)}")

faltan_en_core = sorted(auth_u - core_u)[:10]
faltan_en_auth = sorted(core_u - auth_u)[:10]
if faltan_en_core:
    print(f"  ejemplos solo en auth.User: {faltan_en_core}")
if faltan_en_auth:
    print(f"  ejemplos solo en core.User: {faltan_en_auth}")

print()
print("--- MODELOS CON FK A core.User ---")
print(f"ProgresoCategoria        : {ProgresoCategoria.objects.count()} filas")
print(f"ResultadoEvaluacion      : {ResultadoEvaluacion.objects.count()} filas")

print()
print("--- MODELOS CON FK A auth.User ---")
print(f"Respuesta                : {Respuesta.objects.count()} filas")
print(f"LogroObtenido            : {LogroObtenido.objects.count()} filas")
print(f"CertificacionObtenida    : {CertificacionObtenida.objects.count()} filas")
print(f"Curso (con creador)      : {Curso.objects.exclude(creado_por=None).count()} filas")
print(f"PreguntaGenerada         : {PreguntaGenerada.objects.count()} filas")
print(f"RespuestaPregunta        : {RespuestaPregunta.objects.count()} filas")

print()
print("--- MAPEO core.User.pk -> auth.User.pk (por username) ---")
pares_ok = 0
sin_match = 0
ejemplos = []
for cu in CoreUser.objects.all()[:2000]:
    au = AuthUser.objects.filter(username=cu.username).first()
    if au:
        pares_ok += 1
        if len(ejemplos) < 5:
            ejemplos.append(f"core.User(pk={cu.pk}, {cu.username!r}) -> auth.User(pk={au.pk})")
    else:
        sin_match += 1
print(f"con match: {pares_ok}  |  sin match: {sin_match}")
for e in ejemplos:
    print(f"  {e}")

print()
print("--- HUERFANOS en ProgresoCategoria / ResultadoEvaluacion ---")
core_pks = set(CoreUser.objects.values_list("pk", flat=True))
prog_pks = set(ProgresoCategoria.objects.values_list("user_id", flat=True))
reev_pks = set(ResultadoEvaluacion.objects.values_list("user_id", flat=True))
print(f"ProgresoCategoria.user_id fuera de core.User       : {len(prog_pks - core_pks)}")
print(f"ResultadoEvaluacion.user_id fuera de core.User     : {len(reev_pks - core_pks)}")

print()
print("=" * 72)
print("FIN")
print("=" * 72)