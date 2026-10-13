"""Diagnostico del bug resultado_evaluacion.html."""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

print("=" * 75)
print("VISTA resultado_evaluacion COMPLETA")
print("=" * 75)
p = BASE / "core" / "views_cursos_completo.py"
c = p.read_text(encoding="utf-8")
m = re.search(r"def\s+resultado_evaluacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for l in m.group(0).split("\n")[:80]:
        print(l)
else:
    print("[!] No se encontro")

print()
print("=" * 75)
print("VISTA enviar_evaluacion COMPLETA (para entender el flujo)")
print("=" * 75)
m = re.search(r"def\s+enviar_evaluacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for l in m.group(0).split("\n")[:60]:
        print(l)

print()
print("=" * 75)
print("TEMPLATES EXISTENTES EN core/cursos/")
print("=" * 75)
tc = BASE / "core" / "templates" / "core" / "cursos"
for f in sorted(tc.rglob("*.html")):
    print(f"  {f.name:40} {f.stat().st_size:>8} bytes")

print()
print("=" * 75)
print("MODELO ResultadoEvaluacionCurso - campos")
print("=" * 75)
import sys
sys.path.insert(0, str(BASE))
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from core.models_cursos import ResultadoEvaluacionCurso, EvaluacionCurso, PreguntaEvaluacion
print("ResultadoEvaluacionCurso:")
for f in ResultadoEvaluacionCurso._meta.get_fields():
    if hasattr(f, "name"):
        print(f"  - {f.name:30} {f.__class__.__name__}")

print()
print("EvaluacionCurso campos clave:")
for f in EvaluacionCurso._meta.get_fields():
    if hasattr(f, "name") and f.name in ["id", "titulo", "curso", "modulo", "puntaje_maximo", "intentos_permitidos"]:
        print(f"  - {f.name}: {f.__class__.__name__}")

print()
print("PreguntaEvaluacion campos clave:")
for f in PreguntaEvaluacion._meta.get_fields():
    if hasattr(f, "name"):
        print(f"  - {f.name}: {f.__class__.__name__}")
