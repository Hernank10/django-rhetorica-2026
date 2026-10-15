"""Script para corregir el import de User en core/views.py."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
views_path = BASE / "core" / "views.py"

content = views_path.read_text(encoding="utf-8")

# 1. Remover User de la tupla de importaciones de .models si está presente
content = content.replace("    User,\r\n", "").replace("    User,\n", "")

# 2. Agregar el import nativo de User arriba si no existe
auth_import = "from django.contrib.auth.models import User"
if auth_import not in content:
    content = auth_import + "\n" + content

views_path.write_text(content, encoding="utf-8")
print("[OK] core/views.py actualizado con el import nativo de auth.User")