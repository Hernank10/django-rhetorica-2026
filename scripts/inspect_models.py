"""Inspecciona relaciones de los modelos de cursos."""
import os, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")

import django
django.setup()

from core.models_cursos import Curso, Modulo, Leccion, ProgresoUsuario, EvaluacionCurso, PreguntaEvaluacion
from core.models import Logro, LogroObtenido, Certificacion, CertificacionObtenida, Evaluacion, Respuesta

MODELOS = [Curso, Modulo, Leccion, ProgresoUsuario, EvaluacionCurso, PreguntaEvaluacion,
           Logro, LogroObtenido, Certificacion, CertificacionObtenida, Evaluacion, Respuesta]

for M in MODELOS:
    print(f"\n=== {M.__name__} ===")
    for f in M._meta.get_fields():
        if f.auto_created and not f.concrete:
            continue
        tipo = type(f).__name__
        info = ""
        if f.is_relation and hasattr(f, "related_model") and f.related_model:
            info = f" -> {f.related_model.__name__}"
        elif hasattr(f, "get_internal_type"):
            info = f" ({f.get_internal_type()})"
        print(f"  {f.name:30} {tipo}{info}")