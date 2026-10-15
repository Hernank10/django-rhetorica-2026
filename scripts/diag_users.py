"""Diagnostico del sistema de usuarios (solo lectura)."""
import re
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
OUT = BASE / "diag_users_report.txt"

# -------- 1. Settings --------
settings = BASE / "django_retorica" / "settings.py"
s = settings.read_text(encoding="utf-8") if settings.exists() else ""

def buscar_setting(nombre):
    for linea in s.split("\n"):
        if nombre in linea and "=" in linea:
            return linea.strip()
    return "(no encontrado)"

# -------- 2. Escanear .py --------
patrones = {
    "import_auth_user":     re.compile(r"from\s+django\.contrib\.auth\.models\s+import\s+.*\bUser\b"),
    "import_core_user":     re.compile(r"from\s+\.?\s*models\s+import\s+.*\bUser\b"),
    "import_core_user_abs": re.compile(r"from\s+core\.(models|models_cursos)\s+import\s+.*\bUser\b"),
    "fk_auth_user":         re.compile(r"ForeignKey\s*\(\s*User\b"),
    "fk_auth_user_model":   re.compile(r"ForeignKey\s*\(\s*settings\.AUTH_USER_MODEL"),
    "signal_post_save":     re.compile(r"@receiver\s*\(\s*post_save"),
    "signal_pre_save":      re.compile(r"@receiver\s*\(\s*pre_save"),
    "class_user":           re.compile(r"^class\s+User\s*\("),
    "get_user_model":       re.compile(r"get_user_model\s*\("),
}

skip_dirs = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules", "locale"}
archivos = []
for p in BASE.rglob("*.py"):
    if any(part in skip_dirs for part in p.parts):
        continue
    archivos.append(p)

hallazgos = {k: [] for k in patrones}

for p in archivos:
    try:
        texto = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    rel = str(p.relative_to(BASE))
    for i, linea in enumerate(texto.split("\n"), 1):
        for nombre, pat in patrones.items():
            if pat.search(linea):
                hallazgos[nombre].append((rel, i, linea.strip()[:120]))

# -------- 3. Tests que mencionan core.User / sincronizado --------
tests_sync = []
for p in archivos:
    if "tests" not in p.parts:
        continue
    try:
        texto = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for i, linea in enumerate(texto.split("\n"), 1):
        if "core.User" in linea or "sincronizado" in linea.lower():
            tests_sync.append((str(p.relative_to(BASE)), i, linea.strip()[:120]))

# -------- 4. Fixtures que crean User --------
fixtures_user = []
conftest = BASE / "conftest.py"
if conftest.exists():
    for i, linea in enumerate(conftest.read_text(encoding="utf-8").split("\n"), 1):
        if "User.objects" in linea or "create_user" in linea or "get_user_model" in linea:
            fixtures_user.append(("conftest.py", i, linea.strip()[:120]))

# -------- 5. Reporte --------
lineas = []
lineas.append("=" * 78)
lineas.append("DIAGNOSTICO DEL SISTEMA DE USUARIOS")
lineas.append("=" * 78)
lineas.append("")
lineas.append("--- 1. SETTINGS (django_retorica/settings.py) ---")
lineas.append(f"  AUTH_USER_MODEL:         {buscar_setting('AUTH_USER_MODEL')}")
lineas.append(f"  AUTHENTICATION_BACKENDS: {buscar_setting('AUTHENTICATION_BACKENDS')}")
lineas.append(f"  INSTALLED_APPS (django.contrib.auth): {'django.contrib.auth' in s}")
lineas.append("")

titulos = {
    "class_user":           "--- 2. CLASES 'class User(...)' ENCONTRADAS ---",
    "import_auth_user":     "--- 3. IMPORTS de auth.User ---",
    "import_core_user":     "--- 4. IMPORTS relativos de User (from .models ...) ---",
    "import_core_user_abs": "--- 5. IMPORTS absolutos (from core.models ...) ---",
    "get_user_model":       "--- 6. get_user_model() USADO EN ---",
    "fk_auth_user":         "--- 7. ForeignKey(User, ...) ---",
    "fk_auth_user_model":   "--- 8. ForeignKey(settings.AUTH_USER_MODEL, ...) ---",
    "signal_post_save":     "--- 9. @receiver(post_save, ...) ---",
    "signal_pre_save":      "--- 10. @receiver(pre_save, ...) ---",
}

for clave, titulo in titulos.items():
    lineas.append(titulo)
    entradas = hallazgos[clave]
    if not entradas:
        lineas.append("  (ninguno)")
    else:
        for rel, n, txt in entradas:
            lineas.append(f"  {rel}:{n}: {txt}")
    lineas.append("")

lineas.append("--- 11. TESTS que mencionan 'core.User' o 'sincronizado' ---")
if not tests_sync:
    lineas.append("  (ninguno)")
else:
    for rel, n, txt in tests_sync:
        lineas.append(f"  {rel}:{n}: {txt}")
lineas.append("")

lineas.append("--- 12. FIXTURES en conftest.py que crean User ---")
if not fixtures_user:
    lineas.append("  (ninguno)")
else:
    for rel, n, txt in fixtures_user:
        lineas.append(f"  {rel}:{n}: {txt}")
lineas.append("")

lineas.append("=" * 78)
lineas.append("FIN DEL REPORTE")
lineas.append("=" * 78)

OUT.write_text("\n".join(lineas), encoding="utf-8")
print(f"[OK] Reporte escrito en: {OUT}")
print(f"     {len(lineas)} lineas")
print()
# Tambien imprimirlo en consola
print("\n".join(lineas))