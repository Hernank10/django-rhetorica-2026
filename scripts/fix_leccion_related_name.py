from pathlib import Path
import re

p = Path(r"core\models_cursos.py")
c = p.read_text(encoding="utf-8")

# Encontrar la clase Leccion
m = re.search(r"(class\s+Leccion\s*\([^)]*\):)(.*?)(?=^class |\Z)", c, re.MULTILINE | re.DOTALL)
if not m:
    print("[!] No se encontró class Leccion")
    exit(1)

# Encontrar el campo ejercicios_relacionados (multi-línea hasta el cierre del paréntesis)
mcampo = re.search(
    r"(\n\s*ejercicios_relacionados\s*=\s*models\.\w+\s*\()(.*?)(\)\s*)",
    m.group(2),
    re.DOTALL,
)
if not mcampo:
    print("[!] No se encontró ejercicios_relacionados")
    exit(1)

argumentos = mcampo.group(2)

if "related_name" in argumentos:
    print("[SKIP] Ya tiene related_name. Nada que hacer.")
    exit(0)

# Insertar related_name antes del cierre del paréntesis
nuevos_args = argumentos.rstrip()
if not nuevos_args.endswith(","):
    nuevos_args += ","
nuevos_args += "\n        related_name='lecciones_relacionadas',\n    "

nuevo_campo = mcampo.group(1) + nuevos_args + mcampo.group(3)
c = c[:m.start(2) + mcampo.start()] + nuevo_campo + c[m.start(2) + mcampo.end():]

p.write_text(c, encoding="utf-8")
print("[OK] related_name='lecciones_relacionadas' añadido a Leccion.ejercicios_relacionados")

# Mostrar el bloque resultante
c2 = p.read_text(encoding="utf-8")
m2 = re.search(r"class\s+Leccion\s*\([^)]*\):(.*?)(?=^class |\Z)", c2, re.MULTILINE | re.DOTALL)
if m2:
    print()
    print("=" * 60)
    print("BLOQUE RESULTANTE")
    print("=" * 60)
    for linea in m2.group(1).split("\n"):
        if "ejercicios_relacionados" in linea or "related_name" in linea:
            print(linea)