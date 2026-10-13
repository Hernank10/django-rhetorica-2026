from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
c = p.read_text(encoding="utf-8")

if "Hosts permitidos" in c or 'ALLOWED_HOSTS = ["localhost"' in c:
    print("[SKIP] ya estaba")
else:
    c = c.rstrip() + '''


# -------------------------------------------------------------
# Hosts permitidos (incluye testserver para Django test Client)
# -------------------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
else:
    ALLOWED_HOSTS = ["rhetorica.com", "www.rhetorica.com"]
'''
    p.write_text(c, encoding="utf-8")
    print("[OK] ALLOWED_HOSTS añadido al final")
