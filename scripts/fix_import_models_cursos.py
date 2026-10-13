from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\models.py")
c = p.read_text(encoding="utf-8")

# 1) Verificar si ya importa models_cursos
if "import models_cursos" not in c and "from . import models_cursos" not in c:
    # Añadir al final del archivo
    c = c.rstrip() + "\n\n\n# Forzar a Django a cargar los modelos de cursos al iniciar\nfrom . import models_cursos  # noqa: F401,E402\n"
    p.write_text(c, encoding="utf-8")
    print("[OK] import models_cursos añadido al final de core/models.py")
else:
    print("[SKIP] import ya estaba")

# 2) Verificar
if "from . import models_cursos" in p.read_text(encoding="utf-8"):
    print("[OK] verificado")
