"""Ver que vistas renderizan admin_panel.html y examen.html."""
import re
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

objetivos = ["admin_panel.html", "examen.html", "practicar_pregunta.html", "preguntas/lista.html"]

print("=" * 75)
print("VISTAS QUE RENDERIZAN LOS TEMPLATES SOSPECHOSOS")
print("=" * 75)

for py in sorted(BASE.rglob("*.py")):
    if "__pycache__" in str(py) or "migrations" in str(py) or "scripts" in str(py):
        continue
    try:
        txt = py.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for i, l in enumerate(txt.split("\n"), 1):
        for obj in objetivos:
            # Buscar en la misma linea o en las 2 anteriores (render multi-linea)
            if obj in l:
                rel = py.relative_to(BASE)
                print(f"  {rel}:{i}")
                print(f"      {l.strip()[:120]}")

print()
print("=" * 75)
print("URLS ACTIVAS QUE USAN ESAS VISTAS")
print("=" * 75)

# Importar django para ver URLs
import sys, os
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()
from django.urls import get_resolver

def walk(patterns, prefijo="", namespace=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            ns = namespace
            if hasattr(p, "namespace") and p.namespace:
                ns = f"{namespace}:{p.namespace}" if namespace else p.namespace
            walk(p.url_patterns, prefijo + str(p.pattern), ns)
        else:
            pat = prefijo + str(p.pattern)
            nombre = p.name or "(sin nombre)"
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            func = p.callback.__name__ if hasattr(p.callback, "__name__") else "?"
            # Filtro: solo las que pueden renderizar esos templates
            if any(x in mod for x in ["admin", "views"]):
                print(f"  {pat:60} -> {mod}.{func}")

walk(get_resolver().url_patterns)
