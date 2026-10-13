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
from django.urls import reverse, resolve

User = get_user_model()

print("=" * 60)
print("1) QUE VISTA MANEJA core:detalle_curso")
print("=" * 60)

url = reverse("core:detalle_curso", kwargs={"curso_slug": "morfologia"})
print(f"  URL reverse: {url}")

match = resolve(url)
print(f"  Vista:       {match.func.__module__}.{match.func.__name__}")
print(f"  kwargs:      {match.kwargs}")

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
curso = Curso.objects.get(slug="morfologia")

print(f"  curso: {curso}")
print(f"  curso.recursos (related_name='recursos') → count = {curso.recursos.count()}")
print(f"  curso.recursos.exists() → {curso.recursos.exists()}")

# Ver TODOS los related_names que podrían existir
print()
print("  Recurso.objects.filter(curso=curso) → ", end="")
from core.models import Recurso
print(Recurso.objects.filter(curso=curso).count())

# Ver si el FK apunta al Curso correcto
print()
print("  FKs del recurso vinculado:")
r = Recurso.objects.filter(curso=curso).first()
if r:
    print(f"    nombre: {r.nombre}")
    print(f"    curso_id: {r.curso_id}")
    print(f"    curso: {r.curso}")
    print(f"    modulo_id: {r.modulo_id}")
    print(f"    leccion_id: {r.leccion_id}")
    print(f"    evaluacion_curso_id: {r.evaluacion_curso_id}")
    print(f"    ejercicio_id: {r.ejercicio_id}")

print()
print("=" * 60)
print("4) ¿Qué aparece en el HTML?")
print("=" * 60)

html = resp.content.decode("utf-8", errors="replace")
print(f"  Tamaño HTML: {len(html)} bytes")
print(f"  ¿'Recursos del curso'?    {'✓' if 'Recursos del curso' in html else '✗'}")
print(f"  ¿'recursos:para_objeto'?  {'✓' if 'recursos:para_objeto' in html else '✗'}")
print(f"  ¿'course.recursos'?       {'✓' if 'course.recursos' in html else '✗'}")
print(f"  ¿'Añadir recursos'?       {'✓' if 'Adir recursos' in html or 'Añadir recursos' in html else '✗'}")
print(f"  ¿'Anadir recursos'?       {'✓' if 'Anadir recursos' in html else '✗'}")

# Contar cuántos templates base se usaron
print()
print(f"  Total templates renderizados: {len(resp.templates)}")
