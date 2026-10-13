"""Diagnóstico completo para FASE 3: certificados, i18n, utils."""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

print("=" * 70)
print("1) ARCHIVOS DE UTILS / CERTIFICADOS")
print("=" * 70)
for p in sorted(BASE.rglob("utils*.py")):
    if "__pycache__" in str(p) or "migrations" in str(p):
        continue
    print(f"  {p.relative_to(BASE)}")

print()
print("=" * 70)
print("2) CONTENIDO DE core/utils_certificados.py (si existe)")
print("=" * 70)
for nombre in ["utils_certificados.py", "utils.py", "certificados.py"]:
    p = BASE / "core" / nombre
    if p.exists():
        print(f"--- {p.name} ---")
        c = p.read_text(encoding="utf-8", errors="replace")
        for i, l in enumerate(c.split("\n"), 1):
            if l.strip().startswith(("def ", "class ", "from ", "import ")) or "def " in l[:10]:
                print(f"  {i:3}: {l}")
        print()

print("=" * 70)
print("3) MODELOS DE CERTIFICACION (campos)")
print("=" * 70)
try:
    from core.models import Certificacion, CertificacionObtenida
    print("Certificacion:")
    for f in Certificacion._meta.get_fields():
        if hasattr(f, "name"):
            print(f"  - {f.name}: {f.__class__.__name__}")
    print()
    print("CertificacionObtenida:")
    for f in CertificacionObtenida._meta.get_fields():
        if hasattr(f, "name"):
            print(f"  - {f.name}: {f.__class__.__name__}")
except Exception as e:
    print(f"[!] {e}")

print()
print("=" * 70)
print("4) URLS RELACIONADAS CON CERTIFICADOS / VERIFICAR")
print("=" * 70)
from django.urls import get_resolver

def walk(patterns, prefijo=""):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            walk(p.url_patterns, prefijo + str(p.pattern))
        else:
            pat = prefijo + str(p.pattern)
            nombre = p.name or "(sin nombre)"
            lower = pat.lower()
            if "cert" in lower or "verific" in lower or "diploma" in lower:
                print(f"  {pat:70} -> {nombre}")

walk(get_resolver().url_patterns)

print()
print("=" * 70)
print("5) SETTINGS DE IDIOMA")
print("=" * 70)
from django.conf import settings
print(f"  USE_I18N:    {getattr(settings, 'USE_I18N', None)}")
print(f"  USE_L10N:    {getattr(settings, 'USE_L10N', None)}")
print(f"  LANGUAGE_CODE: {getattr(settings, 'LANGUAGE_CODE', None)}")
print(f"  LANGUAGES:")
langs = getattr(settings, "LANGUAGES", [])
print(f"    Total: {len(langs)}")
for code, name in langs:
    print(f"      - {code:6} → {name}")

print()
print("=" * 70)
print("6) FUNCIONES EXPORTADAS EN core/utils_certificados.py")
print("=" * 70)
try:
    from core import utils_certificados as uc
    for nombre in dir(uc):
        if not nombre.startswith("_"):
            obj = getattr(uc, nombre)
            if callable(obj):
                print(f"  def {nombre}(...)")
            else:
                print(f"  {nombre} = {type(obj).__name__}")
except ImportError as e:
    print(f"[!] No se pudo importar: {e}")

print()
print("=" * 70)
print("7) LOCALE DIRECTORIES")
print("=" * 70)
locale_dir = BASE / "locale"
if locale_dir.exists():
    for d in sorted(locale_dir.iterdir()):
        if d.is_dir():
            print(f"  {d.name}")
else:
    print("  (no existe carpeta locale/)")
