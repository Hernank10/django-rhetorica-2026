from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\core\management\commands\seed_and_test.py")
c = p.read_text(encoding="utf-8")

# insertar al inicio de handle()
bloque = '''        # --- bypass temporal del signal sync_user_to_core ---
        from django.db.models.signals import post_save
        from django.contrib.auth import get_user_model as _gum
        from core import signals as _signals
        _User = _gum()
        try:
            post_save.disconnect(_signals.sync_user_to_core, sender=_User)
            self.stdout.write(self.style.WARNING("[WARN] signal sync_user_to_core desconectado"))
        except Exception:
            pass
'''

# insertar después de "t0 = time.time()"
marker = '        t0 = time.time()\n'
if marker in c and "signal sync_user_to_core desconectado" not in c:
    c = c.replace(marker, marker + bloque, 1)
    p.write_text(c, encoding="utf-8")
    print("[OK] seed_and_test.py ahora desconecta el signal al inicio")
else:
    print("[!] No se pudo insertar (¿ya estaba?)")