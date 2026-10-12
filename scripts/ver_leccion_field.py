from pathlib import Path
import re

p = Path(r"core\models_cursos.py")
c = p.read_text(encoding="utf-8")

# Encontrar la clase Leccion
m = re.search(r"class\s+Leccion\s*\([^)]*\):(.*?)(?=^class |\Z)", c, re.MULTILINE | re.DOTALL)
if not m:
    print("[!] No se encontró class Leccion")
    exit(1)

cuerpo = m.group(1)
# Encontrar el campo ejercicios_relacionados
mcampo = re.search(r"\n(\s*ejercicios_relacionados\s*=\s*models\.\w+\s*\(.*?\)\s*)", cuerpo, re.DOTALL)
if not mcampo:
    print("[!] No se encontró ejercicios_relacionados")
    exit(1)

print("=" * 60)
print("BLOQUE ACTUAL DE Leccion.ejercicios_relacionados")
print("=" * 60)
print(mcampo.group(1))
print("=" * 60)

if "related_name" in mcampo.group(1):
    print("[!] Ya tiene related_name. Nada que hacer.")
else:
    print("[OK] Necesita related_name. Ejecuta el Paso 2")