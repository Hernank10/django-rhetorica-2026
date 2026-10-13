from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
c = p.read_text(encoding="utf-8")

if "LOGIN_URL" not in c:
    bloque = '''

# -------------------------------------------------------------
# Login/Logout
# -------------------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
'''
    c = c.rstrip() + bloque
    p.write_text(c, encoding="utf-8")
    print("[OK] LOGIN_URL añadido a settings.py")
else:
    print("[SKIP] LOGIN_URL ya estaba")
