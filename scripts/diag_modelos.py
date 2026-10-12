from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# Buscar todos los modelos
modelos = []
for py_file in BASE.rglob("models*.py"):
    if "migrations" in str(py_file) or "__pycache__" in str(py_file):
        continue
    try:
        c = py_file.read_text(encoding="utf-8")
    except Exception:
        continue
    for m in re.finditer(r"^class\s+(\w+)\s*\(\s*models\.Model\s*\)", c, re.MULTILINE):
        modelos.append((py_file.name, m.group(1)))

print("=" * 60)
print("MODELOS ENCONTRADOS")
print("=" * 60)
for archivo, nombre in modelos:
    print(f"  {archivo:30} → {nombre}")

# Ver campos del modelo Recurso
print()
print("=" * 60)
print("CAMPOS DE Recurso")
print("=" * 60)
mp = BASE / "core" / "models.py"
if mp.exists():
    c = mp.read_text(encoding="utf-8")
    m = re.search(r"class\s+Recurso\(models\.Model\):(.*?)(?=^class |\Z)", c, re.MULTILINE | re.DOTALL)
    if m:
        bloque = m.group(1)
        for linea in bloque.split("\n"):
            s = linea.strip()
            if s and not s.startswith("#"):
                print(f"  {s}")