"""Diagnostico de vistas sin tests: cursos_completo, ejercicios, biblioteca."""
import sys
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()


# ============================================================
# VISTAS DEFINIDAS EN CADA ARCHIVO
# ============================================================
ARCHIVOS = [
    "core/views_cursos_completo.py",
    "core/views_ejercicios.py",
    "core/views_biblioteca.py",
]

for archivo in ARCHIVOS:
    p = BASE / archivo
    print()
    print("=" * 75)
    print(f"VISTAS EN {archivo}")
    print("=" * 75)

    if not p.exists():
        print("  [!] No existe")
        continue

    c = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"^def\s+(\w+)\s*\(([^)]*)\):", c, re.MULTILINE):
        nombre = m.group(1)
        args = m.group(2).strip()
        # Ver decoradores (linea anterior)
        inicio = m.start()
        previo = c[max(0, inicio-300):inicio]
        decoradores = re.findall(r"@(\w+(?:\.\w+)*)", previo)
        deco_str = " ".join(decoradores[-3:]) if decoradores else ""
        print(f"  def {nombre}({args[:60]})")
        if deco_str:
            print(f"       decoradores: {deco_str}")


# ============================================================
# URLS QUE APUNTAN A ESAS VISTAS
# ============================================================
print()
print("=" * 75)
print("URLS RELACIONADAS")
print("=" * 75)

from django.urls import get_resolver

def walk(patterns, prefijo=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            walk(p.url_patterns, prefijo + str(p.pattern))
        else:
            pat = prefijo + str(p.pattern)
            nombre = p.name or "(sin nombre)"
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            if any(x in mod for x in ["cursos_completo", "ejercicios", "biblioteca"]):
                print(f"  {pat:65} -> {nombre}")
                print(f"       {mod}")

walk(get_resolver().url_patterns)


# ============================================================
# MODELOS USADOS
# ============================================================
print()
print("=" * 75)
print("MODELOS IMPORTADOS EN CADA ARCHIVO")
print("=" * 75)

for archivo in ARCHIVOS:
    p = BASE / archivo
    if not p.exists():
        continue
    print(f"\n{archivo}:")
    c = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"from\s+\.(models\w*)\s+import\s+([^\n]+)", c):
        print(f"  from .{m.group(1)} import {m.group(2)}")


# ============================================================
# MODELOS DISPONIBLES (EjercicioLinguistico, TecnicaLinguistica, etc.)
# ============================================================
print()
print("=" * 75)
print("CAMPOS DE MODELOS CLAVE")
print("=" * 75)

from core.models import EjercicioLinguistico, TecnicaLinguistica, ContenidoJSON
from core.models_cursos import Curso, Modulo, Leccion

for modelo in [EjercicioLinguistico, TecnicaLinguistica, ContenidoJSON]:
    print(f"\n{modelo.__name__}:")
    for f in modelo._meta.get_fields():
        if hasattr(f, "name"):
            tipo = f.__class__.__name__
            null = getattr(f, "null", "")
            blank = getattr(f, "blank", "")
            print(f"  - {f.name:35} {tipo:20} null={null} blank={blank}")