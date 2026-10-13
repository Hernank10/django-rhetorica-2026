"""
Test 1: Vincular un recurso a un curso via HTTP POST.
"""
import sys
from pathlib import Path

# Añadir la raíz del proyecto al sys.path
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")

import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Recurso, EjercicioLinguistico
from core.models_cursos import Curso, Modulo, Leccion, EvaluacionCurso

User = get_user_model()

print("=" * 60)
print("TEST 1 — VINCULAR RECURSO A CURSO")
print("=" * 60)

print()
print("[0] Estado actual de la BD")
print(f"    Cursos:                {Curso.objects.count()}")
print(f"    Módulos:               {Modulo.objects.count()}")
print(f"    Lecciones:             {Leccion.objects.count()}")
print(f"    Evaluaciones de curso: {EvaluacionCurso.objects.count()}")
print(f"    Ejercicios:            {EjercicioLinguistico.objects.count()}")
print(f"    Recursos:              {Recurso.objects.count()}")
print(f"    Usuarios:              {User.objects.count()}")

print()
print("[1] Usuario para el test")
user = User.objects.filter(is_superuser=True).first() or User.objects.first()
if not user:
    print("    [!] No hay usuarios.")
    exit(1)
print(f"    Usando: {user.username}  (superuser={user.is_superuser})")

print()
print("[2] Login con test client")
client = Client()
client.force_login(user)
print(f"    [OK] Login forzado")

print()
print("[3] Buscar recurso 'Ars Grammatica'")
recurso = Recurso.objects.filter(nombre__icontains="Ars Grammatica").first() \
          or Recurso.objects.filter(nombre__icontains="Flota Adjectivum").first() \
          or Recurso.objects.first()
if not recurso:
    print("    [!] No hay recursos.")
    exit(1)
print(f"    Recurso:  {recurso.nombre}")
print(f"    Slug:     {recurso.slug}")
print(f"    Curso actual: {recurso.curso}")

print()
print("[4] GET al visor del recurso")
url_ver = reverse("recursos:ver", kwargs={"slug": recurso.slug})
resp = client.get(url_ver)
print(f"    GET {url_ver} → {resp.status_code}")
if resp.status_code == 200:
    html = resp.content.decode("utf-8", errors="replace")
    tiene_vincular = "vincular" in html.lower()
    print(f"    ¿Botón Vincular? {'SÍ' if tiene_vincular else 'NO'}")

print()
print("[5] GET al formulario de vinculación")
url_vincular = reverse("recursos:vincular", kwargs={"slug": recurso.slug})
resp = client.get(url_vincular)
print(f"    GET {url_vincular} → {resp.status_code}")
if resp.status_code != 200:
    print(f"    [!] Status {resp.status_code}")
    print(resp.content.decode("utf-8", errors="replace")[:800])
    exit(1)

html = resp.content.decode("utf-8", errors="replace")
for campo in ["name=\"curso\"", "name=\"modulo\"", "name=\"leccion\"",
              "name=\"evaluacion_curso\"", "name=\"ejercicio\"",
              "name=\"orden\"", "name=\"destacado\""]:
    presente = "✓" if campo in html else "✗"
    print(f"    {presente}  {campo}")

print()
print("[6] Elegir curso objetivo")
curso = Curso.objects.filter(titulo__icontains="Morfolog").first() or Curso.objects.first()
if not curso:
    print("    [!] No hay cursos.")
    exit(1)
print(f"    Curso:  {curso.titulo}  (ID: {curso.id})")

print()
print("[7] POST para vincular recurso")
datos = {
    "curso": str(curso.id),
    "modulo": "",
    "leccion": "",
    "evaluacion_curso": "",
    "ejercicio": "",
    "orden": "1",
}
resp = client.post(url_vincular, data=datos)
print(f"    POST → {resp.status_code}")
if resp.status_code == 302:
    print(f"    [OK] Redirect: {resp.headers.get('Location')}")
elif resp.status_code == 200:
    print("    [!] Formulario devuelto (error de validación)")
    exit(1)
else:
    print(f"    [!] Status {resp.status_code}")
    print(resp.content.decode("utf-8", errors="replace")[:500])
    exit(1)

print()
print("[8] Verificar vinculación en BD")
recurso.refresh_from_db()
print(f"    recurso.curso_id  → {recurso.curso_id}")
print(f"    recurso.curso     → {recurso.curso}")
print(f"    recurso.orden     → {recurso.orden}")
print(f"    recurso.destacado → {recurso.destacado}")
if recurso.curso_id == curso.id:
    print("    [✓] VINCULACIÓN EXITOSA")
else:
    print("    [✗] FALLÓ")
    exit(1)

print()
print("[9] Recursos vinculados al curso")
vinculados = Recurso.objects.filter(curso=curso)
print(f"    Total: {vinculados.count()}")
for r in vinculados[:5]:
    print(f"      - {r.nombre[:60]}")

print()
print("[10] GET a recursos:para_objeto")
url_para = reverse("recursos:para_objeto", kwargs={"tipo": "curso", "obj_id": curso.id})
resp = client.get(url_para)
print(f"    GET {url_para} → {resp.status_code}")
if resp.status_code == 200:
    html = resp.content.decode("utf-8", errors="replace")
    print(f"    ¿Sección 'Vinculados'?   {'✓' if 'Vinculados' in html else '✗'}")
    print(f"    ¿Sección 'Disponibles'?  {'✓' if 'Disponibles' in html else '✗'}")

print()
print("[11] GET al detalle del curso")
try:
    url_curso = reverse("core:detalle_curso", kwargs={"curso_slug": curso.slug})
except Exception:
    url_curso = f"/cursos/{curso.slug}/"
resp = client.get(url_curso)
print(f"    GET {url_curso} → {resp.status_code}")
if resp.status_code == 200:
    html = resp.content.decode("utf-8", errors="replace")
    tiene = "Recursos del curso" in html or "recursos del curso" in html.lower()
    print(f"    ¿Sección 'Recursos del curso'? {'✓' if tiene else '✗'}")

print()
print("=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"  Recurso probado: {recurso.nombre}")
print(f"  Curso vinculado: {curso.titulo}")
print(f"  Estado:          [✓] TODO OK")
print("=" * 60)
