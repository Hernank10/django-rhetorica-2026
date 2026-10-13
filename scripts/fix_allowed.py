from pathlib import Path
import re
p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
c = p.read_text(encoding="utf-8")

bloque = '''

# -------------------------------------------------------------
# DEV: hosts permitidos (incluye 'testserver' para Django test Client)
# -------------------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
'''
if "testserver" not in c:
    c = c.rstrip() + bloque
    p.write_text(c, encoding="utf-8")
    print("[OK] ALLOWED_HOSTS con testserver en DEBUG")
else:
    print("[SKIP] ya estaba")
