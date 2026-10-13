from pathlib import Path
import re
p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
c = p.read_text(encoding="utf-8")

# 1) Quitar el bloque previo si existe (con o sin testserver)
c = re.sub(r"\n# -+\n# DEV: hosts permitidos.*?ALLOWED_HOSTS\s*=\s*\[[^\]]*\]\n",
           "\n", c, flags=re.DOTALL)

# 2) Buscar línea ALLOWED_HOSTS actual y reemplazarla
patron = re.compile(r"^ALLOWED_HOSTS\s*=\s*\[[^\]]*\]", re.MULTILINE)
bloque = '''if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
else:
    ALLOWED_HOSTS = ["rhetorica.com", "www.rhetorica.com"]'''

if patron.search(c):
    c = patron.sub(bloque, c, count=1)
    print("[OK] ALLOWED_HOSTS reemplazado en linea existente")
else:
    c = c.rstrip() + "\n\n# Hosts\n" + bloque + "\n"
    print("[OK] ALLOWED_HOSTS agregado al final")

p.write_text(c, encoding="utf-8")
