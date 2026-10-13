"""Diagnostico de los 3 comandos de management."""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")
cmds_dir = BASE / "core" / "management" / "commands"

for nombre in ["seed_content.py", "seed_and_test.py", "indexar_recursos.py"]:
    p = cmds_dir / nombre
    print()
    print("=" * 78)
    print(f"{nombre}")
    print("=" * 78)
    if not p.exists():
        print("  [!] No existe")
        continue

    c = p.read_text(encoding="utf-8", errors="replace")

    # Docstring / help
    m = re.search(r'help\s*=\s*["\']([^"\']+)["\']', c)
    if m:
        print(f"  help: {m.group(1)}")

    # class Command
    m = re.search(r"class\s+Command\s*\([^)]+\):", c)
    if m:
        print(f"  {m.group(0)}")

    # add_arguments
    if "def add_arguments" in c:
        print("  Tiene add_arguments (acepta opciones)")

    # handle
    m = re.search(r"def\s+handle\s*\([^)]*\):(.*?)(?=^    def |\Z)", c, re.MULTILINE | re.DOTALL)
    if m:
        lineas_handle = m.group(0).count("\n")
        print(f"  handle: ~{lineas_handle} lineas")

    # Imports
    print("  Imports clave:")
    for l in c.split("\n")[:40]:
        if re.match(r"^\s*(from|import)\s", l) and ("core" in l or "models" in l or "Command" in l):
            print(f"    {l.strip()}")

    # References a modelos en el cuerpo
    modelos = set()
    for m in re.finditer(r"\b(Curso|Modulo|Leccion|EvaluacionCurso|PreguntaEvaluacion|EjercicioLinguistico|TecnicaLinguistica|ContenidoJSON|Recurso|Logro|Certificacion)\b", c):
        modelos.add(m.group(1))
    print(f"  Modelos mencionados: {sorted(modelos)}")

    # Salidas (self.stdout.write)
    salidas = re.findall(r'self\.stdout\.write\([^)]+\)', c)
    print(f"  Salidas stdout: {len(salidas)}")