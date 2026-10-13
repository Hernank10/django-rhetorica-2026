"""Quitar skip de test_genera_datos en test_certificados.py."""
from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\tests\test_certificados.py")
c = p.read_text(encoding="utf-8")

# Buscar el bloque de skip
patron = re.compile(
    r"        except KeyError as e:\n            pytest\.skip\(f\"Fuente no registrada[^\"]*\"\)\n",
)
if patron.search(c):
    # Reemplazar por fail (si el font falla ahora es un bug real)
    c = patron.sub(
        '        except KeyError as e:\n            pytest.fail(f"Fuente no registrada: {e}")\n',
        c, count=1,
    )
    p.write_text(c, encoding="utf-8")
    print("[OK] pytest.skip -> pytest.fail en test_certificados.py")
else:
    print("[SKIP] No se encontro el patron skip")