"""Script para corregir el import de User en core/tests/test_models_extended.py."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
test_path = BASE / "core" / "tests" / "test_models_extended.py"

content = test_path.read_text(encoding="utf-8")

# Reemplazar la importación de User desde core.models si está integrada en la terna local
content = content.replace("    User,\r\n", "").replace("    User,\n", "")

# Asegurar que se importe User nativo de Django
auth_import = "from django.contrib.auth.models import User"
if auth_import not in content:
    content = auth_import + "\n" + content

test_path.write_text(content, encoding="utf-8")
print("[OK] core/tests/test_models_extended.py actualizado con el import nativo de auth.User")