"""fix_pilot_cierre.py - Cierra los 3 frentes del pilot en un paso. Idempotente.
  A) Reset password testest001-009 -> 'Test1234!'
  B) ProgresoUsuario.completado_en: naive -> aware (corrige RuntimeWarning)
  C) Sanity-check de URLs del admin (tecnicalectura vs typo)
"""
import sys, os
sys.path.insert(0, ".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()

from django.contrib.auth import get_user_model
from django.apps import apps
from django.utils import timezone
from django.conf import settings
from django.urls import resolve, Resolver404

U = get_user_model()
OK, WARN, FAILS = [], [], []

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

# ── A. Passwords ────────────────────────────────────────────────────
header("A", "RESET password testest001-009")
bad = [f"testest{i:03d}" for i in range(1, 10)]
for u in U.objects.filter(username__in=bad):
    u.set_password("Test1234!")
    u.save(update_fields=["password"])
ok = sum(1 for u in U.objects.filter(username__in=bad) if u.check_password("Test1234!"))
print(f"  [{'OK' if ok == len(bad) else 'FAIL'}] {ok}/{len(bad)} con 'Test1234!'")
(OK if ok == len(bad) else FAILS).append(f"Passwords {ok}/{len(bad)}")

# ── B. ProgresoUsuario naive datetimes ──────────────────────────────
header("B", "ProgresoUsuario.completado_en -> make_aware")
try:
    PU = apps.get_model("core", "ProgresoUsuario")
except LookupError:
    print("  [SKIP] Modelo ProgresoUsuario no existe")
    WARN.append("ProgresoUsuario no existe (RuntimeWarning de otra fuente)")
else:
    print(f"  Modelo: {PU.__module__}.{PU.__name__}  USE_TZ={settings.USE_TZ}")
    to_fix, naive_seen = [], 0
    for obj in PU.objects.exclude(completado_en=None).iterator():
        if timezone.is_naive(obj.completado_en):
            naive_seen += 1
            obj.completado_en = timezone.make_aware(obj.completado_en)
            to_fix.append(obj)
    if to_fix:
        PU.objects.bulk_update(to_fix, ["completado_en"])
    remaining = sum(1 for obj in PU.objects.exclude(completado_en=None).iterator()
                    if timezone.is_naive(obj.completado_en))
    print(f"  Naive detectados:  {naive_seen}")
    print(f"  Corregidos:        {len(to_fix)}")
    print(f"  Naive remanentes:  {remaining}")
    if remaining == 0:
        OK.append(f"ProgresoUsuario: {naive_seen} naive -> aware")
    else:
        FAILS.append(f"ProgresoUsuario: {remaining} naive remanentes")

# ── C. URL resolve del admin ────────────────────────────────────────
header("C", "URL RESOLVE admin")
for url, debe_404 in [("/admin/core/tecnicalectura/", False),
                      ("/admin/core/tecnicatectura/", True)]:
    try:
        resolve(url)
        print(f"  [OK]  {url} resuelve")
        if debe_404:
            WARN.append(f"URL typo '{url}' resuelve (deberia 404)")
    except Resolver404:
        print(f"  [404] {url}")
        if not debe_404:
            FAILS.append(f"URL valida '{url}' NO resuelve")

# ── Resumen ─────────────────────────────────────────────────────────
print(); print("=" * 78); print("RESUMEN FIX"); print("=" * 78)
for o in OK:    print(f"  [OK] {o}")
for w in WARN:  print(f"  [??] {w}")
for f in FAILS: print(f"  [!!] {f}")
if FAILS: sys.exit(1)
print("\n  *** FIX OK ***")