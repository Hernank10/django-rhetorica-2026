import sys
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import resolve

User = get_user_model()

# Usar PATH LITERAL en vez de reverse()
url = "/cursos/morfologia/"

print("=" * 60)
print(f"1) QUE VISTA MANEJA {url}")
print("=" * 60)

try:
    match = resolve(url)
    print(f"  Vista:       {match.func.__module__}.{match.func.__name__}")
    print(f"  kwargs:      {match.kwargs}")
    print(f"  url_name:    {match.url_name}")
    print(f"  namespace:   {match.namespace}")
    print(f"  app_name:    {match.app_name}")
except Exception as e:
    print(f"  [!] No se pudo resolver: {e}")

print()
print("=" * 60)
print("2) QUE TEMPLATES SE USAN AL RENDERIZAR")
print("=" * 60)

user = User.objects.filter(is_superuser=True).first()
client = Client()
client.force_login(user)

resp = client.get(url)
print(f"  Status: {resp.status_code}")
print(f"  Templates usados (en orden):")
for t in resp.templates:
    print(f"    - {t.name}")

print()
print("=" * 60)
print("3) ¿curso.recursos existe?")
print("=" * 60)

from core.models_cursos import Curso
try:
    curso = Curso.objects.get(slug="morfologia")
    print(f"  curso: {curso}")
    print(f"  curso.recursos.count() → {curso.recursos.count()}")
    print(f"  curso.recursos.exists() → {curso.recursos.exists()}")
except Exception as e:
    print(f"  [!] {e}")

from core.models import Recurso
print(f"  Recurso.objects.filter(curso__slug='morfologia').count() → {Recurso.objects.filter(curso__slug='morfologia').count()}")

r = Recurso.objects.filter(curso__slug='morfologia').first()
if r:
    print(f"  Primer recurso vinculado: {r.nombre}")
    print(f"    curso_id: {r.curso_id}")

print()
print("=" * 60)
print("4) ¿Qué aparece en el HTML?")
print("=" * 60)

html = resp.content.decode("utf-8", errors="replace")
print(f"  Tamaño HTML: {len(html)} bytes")
for buscar in ["Recursos del curso", "recursos:para_objeto", "Añadir recursos", "Anadir recursos", "folder-open"]:
    print(f"  ¿'{buscar}'?  {'✓' if buscar in html else '✗'}")

print()
print("=" * 60)
print("5) URLS QUE MATCHEAN /cursos/")
print("=" * 60)

from django.urls import get_resolver
def walk(patterns, prefijo=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            walk(p.url_patterns, prefijo + str(p.pattern))
        else:
            pat = prefijo + str(p.pattern)
            if "curso" in pat.lower():
                print(f"  {pat}  →  {p.callback.__module__}.{p.callback.__name__}")

walk(get_resolver().url_patterns)
