import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")

import django
django.setup()

from django.urls import get_resolver

def walk(patterns, prefijo=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            walk(p.url_patterns, prefijo + str(p.pattern))
        else:
            pat = prefijo + str(p.pattern)
            nombre = p.name or "(sin nombre)"
            lower = pat.lower()
            if "estudiante" in lower or "profesor" in lower:
                print(f"  {pat:60} -> {nombre}")

print("=" * 90)
print("URLS DE ESTUDIANTE Y PROFESOR")
print("=" * 90)
walk(get_resolver().url_patterns)
