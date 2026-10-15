"""Importar models_preguntas en models.py + crear migracion."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
mp = BASE / "core" / "models.py"
c = mp.read_text(encoding="utf-8")

# Verificar si ya esta importado
if "models_preguntas" in c:
    print("[SKIP] models_preguntas ya esta importado en models.py")
else:
    # Anadir el import al final (igual que models_cursos)
    linea_import = "\nfrom . import models_preguntas  # noqa: F401,E402\n"
    c = c.rstrip() + linea_import
    mp.write_text(c, encoding="utf-8")
    print("[OK] Import anadido al final de core/models.py")
    print("     " + linea_import.strip())

# Mostrar las ultimas 5 lineas del archivo
print()
print("Ultimas lineas de core/models.py:")
lineas = mp.read_text(encoding="utf-8").split("\n")
for l in lineas[-8:]:
    print(f"  {l}")