"""Diagnostico de views.py para planear tests."""
import sys, os
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.urls import get_resolver

def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))

print("=" * 75)
print("VISTAS EN core/views.py")
print("=" * 75)

p = BASE / "core" / "views.py"
c = p.read_text(encoding="utf-8", errors="replace")

vistas = []
for m in re.finditer(r"^(def|class)\s+(\w+)", c, re.MULTILINE):
    vistas.append(m.group(2))
safe(f"  Total def/class: {len(vistas)}")
for v in vistas:
    safe(f"    - {v}")

print()
print("=" * 75)
print("URLS QUE APUNTAN A core.views (el archivo principal)")
print("=" * 75)

def walk(patterns, prefijo=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            walk(p.url_patterns, prefijo + str(p.pattern))
        else:
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            if mod == "core.views":
                pat = prefijo + str(p.pattern)
                nombre = p.name or "(sin nombre)"
                safe(f"  {pat:60} -> {nombre}")

walk(get_resolver().url_patterns)

print()
print("=" * 75)
print("MODELOS IMPORTADOS EN views.py")
print("=" * 75)
for m in re.finditer(r"from\s+\.(models\w*)\s+import\s+([^\n]+)", c):
    safe(f"  from .{m.group(1)} import {m.group(2)}")
