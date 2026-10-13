from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\core\views.py")
c = p.read_text(encoding="utf-8")
viejo = "messages.error(request, 'Usuario no encontrado.')"
nuevo = "pass  # silenciado (usar /estudiante/ en su lugar)"
if viejo in c:
    c = c.replace(viejo, nuevo)
    p.write_text(c, encoding="utf-8")
    print("[OK] último mensaje silenciado")
else:
    print("[SKIP] ya estaba silenciado o no existe")
