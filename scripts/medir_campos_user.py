"""Cuenta usos de campos de core.User en el codigo (solo lectura)."""
import re
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# Campos de core.User que no estan en auth.User
campos = [
    "points", "nivel", "is_admin", "estrellas", "medallas",
    "insignias", "certificaciones", "racha", "ultima_actividad",
    "total_ejercicios_completados", "tasa_aciertos", "nivel_experiencia",
]

# Directorios a escanear (solo codigo de produccion, NO scripts)
dirs = ["core", "django_retorica"]
skip = {"migrations", "__pycache__", "tests"}

# Patrones de uso: user.points, request.user.points, .points=, etc.
patrones = {}
for c in campos:
    patrones[c] = re.compile(rf"\.{c}\b")

hallazgos = {c: [] for c in campos}

for d in dirs:
    for p in (BASE / d).rglob("*.py"):
        if any(part in skip for part in p.parts):
            continue
        try:
            texto = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = str(p.relative_to(BASE))
        for i, linea in enumerate(texto.split("\n"), 1):
            for c, pat in patrones.items():
                if pat.search(linea):
                    hallazgos[c].append((rel, i, linea.strip()[:110]))

print("=" * 76)
print("USO DE CAMPOS DE core.User EN CODIGO DE PRODUCCION")
print("=" * 76)
total = 0
for c in campos:
    n = len(hallazgos[c])
    total += n
    print(f"\n--- {c}  ({n} usos) ---")
    for rel, i, txt in hallazgos[c][:20]:
        print(f"  {rel}:{i}: {txt}")
    if n > 20:
        print(f"  ... y {n - 20} mas")

print()
print("=" * 76)
print(f"TOTAL de usos: {total}")
print("=" * 76)