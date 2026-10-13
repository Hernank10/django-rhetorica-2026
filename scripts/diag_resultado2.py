"""Diagnostico sin emojis ni caracteres raros."""
import sys, os
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()


def safe_print(s):
    """Imprime sin romper si hay caracteres no-cp1252."""
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# 1) Resto de enviar_evaluacion
print("=" * 70)
print("RESTO DE enviar_evaluacion")
print("=" * 70)
p = BASE / "core" / "views_cursos_completo.py"
c = p.read_text(encoding="utf-8")
m = re.search(r"def\s+enviar_evaluacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for l in m.group(0).split("\n"):
        safe_print(l)

# 2) Campos de ResultadoEvaluacionCurso
print()
print("=" * 70)
print("CAMPOS DE ResultadoEvaluacionCurso")
print("=" * 70)
from core.models_cursos import ResultadoEvaluacionCurso, PreguntaEvaluacion
for f in ResultadoEvaluacionCurso._meta.get_fields():
    if hasattr(f, "name"):
        tipo = f.__class__.__name__
        safe_print(f"  - {f.name:35} {tipo}")

# 3) Campos de PreguntaEvaluacion
print()
print("=" * 70)
print("CAMPOS DE PreguntaEvaluacion")
print("=" * 70)
for f in PreguntaEvaluacion._meta.get_fields():
    if hasattr(f, "name"):
        tipo = f.__class__.__name__
        safe_print(f"  - {f.name:35} {tipo}")

# 4) Templates existentes en core/cursos/
print()
print("=" * 70)
print("TEMPLATES EN core/cursos/")
print("=" * 70)
tc = BASE / "core" / "templates" / "core" / "cursos"
for f in sorted(tc.rglob("*.html")):
    safe_print(f"  {f.name:45} {f.stat().st_size} bytes")

# 5) Primeras 40 lineas de evaluacion_detalle.html (para copiar estilo)
print()
print("=" * 70)
print("evaluacion_detalle.html - primeras 40 lineas")
print("=" * 70)
det = tc / "evaluacion_detalle.html"
if det.exists():
    for i, l in enumerate(det.read_text(encoding="utf-8", errors="replace").split("\n")[:40], 1):
        safe_print(f"  {i:3}: {l}")
