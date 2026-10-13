from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# 1) Buscar el mensaje exacto
print("=== Archivos con 'Usuario no encontrado' ===")
for p in BASE.rglob("*.py"):
    if "venv" in str(p) or "site-packages" in str(p):
        continue
    try:
        c = p.read_text(encoding="utf-8", errors="ignore")
        if "Usuario no encontrado" in c:
            print(f"  {p.relative_to(BASE)}")
    except Exception:
        pass

for p in BASE.rglob("*.html"):
    if "venv" in str(p):
        continue
    try:
        c = p.read_text(encoding="utf-8", errors="ignore")
        if "Usuario no encontrado" in c:
            print(f"  {p.relative_to(BASE)}")
    except Exception:
        pass

# 2) Buscar context_processors en settings
print()
print("=== context_processors en settings.py ===")
s = (BASE / "django_retorica" / "settings.py").read_text(encoding="utf-8")
import re
idx = s.find("context_processors")
if idx > 0:
    print(s[idx-100:idx+600])

# 3) Ver si hay middleware que mencione "core"
print()
print("=== Middlewares ===")
idx = s.find("MIDDLEWARE")
if idx > 0:
    print(s[idx:idx+800])

# 4) Ver si hay un archivo context_processors.py
print()
print("=== context_processors.py ===")
for p in BASE.rglob("context_processors.py"):
    if "venv" in str(p) or "site-packages" in str(p):
        continue
    print(f"  {p.relative_to(BASE)}")
    print(p.read_text(encoding="utf-8")[:500])
