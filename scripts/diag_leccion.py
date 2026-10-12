from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

print("=" * 60)
print("FKS QUE APUNTAN A Leccion")
print("=" * 60)

for py_file in BASE.rglob("models*.py"):
    if "migrations" in str(py_file) or "__pycache__" in str(py_file):
        continue
    c = py_file.read_text(encoding="utf-8", errors="replace")
    # Buscar clases
    for m in re.finditer(r"class\s+(\w+)\s*\([^)]*\):(.*?)(?=^class |\Z)", c, re.MULTILINE | re.DOTALL):
        clase = m.group(1)
        cuerpo = m.group(2)
        # Buscar campos que apunten a Leccion
        for fm in re.finditer(r"(\w+)\s*=\s*models\.(ForeignKey|OneToOneField|ManyToManyField)\s*\(\s*['\"]core\.Leccion['\"]|(\w+)\s*=\s*models\.(ForeignKey|OneToOneField|ManyToManyField)\s*\(\s*['\"]Leccion['\"]|(\w+)\s*=\s*models\.(ForeignKey|OneToOneField|ManyToManyField)\s*\(\s*Leccion", cuerpo):
            campo = fm.group(1) or fm.group(3) or fm.group(5)
            linea = fm.group(0)
            # Extraer related_name si existe
            rn = re.search(r"related_name\s*=\s*['\"]([^'\"]+)['\"]", cuerpo[fm.end():fm.end()+300])
            related = rn.group(1) if rn else "(default)"
            print(f"  {py_file.name:20} → class {clase}.{campo}  related_name={related}")

print()
print("=" * 60)
print("FKS QUE APUNTAN A EjercicioLinguistico")
print("=" * 60)
for py_file in BASE.rglob("models*.py"):
    if "migrations" in str(py_file) or "__pycache__" in str(py_file):
        continue
    c = py_file.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"class\s+(\w+)\s*\([^)]*\):(.*?)(?=^class |\Z)", c, re.MULTILINE | re.DOTALL):
        clase = m.group(1)
        cuerpo = m.group(2)
        for fm in re.finditer(r"(\w+)\s*=\s*models\.(ForeignKey|OneToOneField|ManyToManyField)\s*\(\s*['\"]core\.EjercicioLinguistico['\"]|(\w+)\s*=\s*models\.(ForeignKey|OneToOneField|ManyToManyField)\s*\(\s*['\"]EjercicioLinguistico['\"]|(\w+)\s*=\s*models\.(ForeignKey|OneToOneField|ManyToManyField)\s*\(\s*EjercicioLinguistico", cuerpo):
            campo = fm.group(1) or fm.group(3) or fm.group(5)
            rn = re.search(r"related_name\s*=\s*['\"]([^'\"]+)['\"]", cuerpo[fm.end():fm.end()+300])
            related = rn.group(1) if rn else "(default)"
            print(f"  {py_file.name:20} → class {clase}.{campo}  related_name={related}")

print()
print("=" * 60)
print("CAMPO 'leccion' EN EjercicioLinguistico")
print("=" * 60)
mp = BASE / "core" / "models.py"
c = mp.read_text(encoding="utf-8")
m = re.search(r"class\s+EjercicioLinguistico\s*\([^)]*\):(.*?)(?=^class |\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for linea in m.group(1).split("\n"):
        s = linea.strip()
        if "leccion" in s.lower() or "related_name" in s:
            print(f"  {s}")