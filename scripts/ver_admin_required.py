"""Ver donde se usa admin_required."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


safe("=" * 75)
safe("USOS DE admin_required")
safe("=" * 75)

found = 0
for py in BASE.rglob("*.py"):
    if "__pycache__" in str(py) or "scripts" in str(py) or "migrations" in str(py):
        continue
    try:
        c = py.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for i, l in enumerate(c.split("\n"), 1):
        if "admin_required" in l and "def admin_required" not in l:
            safe(f"  {py.relative_to(BASE)}:{i}")
            safe(f"      {l.strip()}")
            found += 1

if found == 0:
    safe("  [OK] admin_required NO se usa en ningun lado")


safe("")
safe("=" * 75)
safe("ATRIBUTOS DEL MODELO core.User")
safe("=" * 75)

# Ver el modelo User
um = BASE / "core" / "models.py"
c = um.read_text(encoding="utf-8", errors="replace")

# Buscar class User
import re
m = re.search(r"class\s+User\s*\([^)]*\):(.*?)(?=^class |\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    safe("  Metodos y propiedades de User:")
    for l in m.group(1).split("\n"):
        s = l.strip()
        if s.startswith("def ") or s.startswith("@property"):
            safe(f"    {s}")


safe("")
safe("=" * 75)
safe("URLS CON 'dashboard'")
safe("=" * 75)

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
            nombre = p.name or ""
            if "dashboard" in nombre.lower():
                pat = prefijo + str(p.pattern)
                clave = f"{namespace}:{nombre}" if namespace and nombre else nombre
                safe(f"  {pat:60} -> {clave}")

walk(get_resolver().url_patterns)