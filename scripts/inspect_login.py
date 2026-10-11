from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\core\views.py")
c = p.read_text(encoding="utf-8")

if "profesor:dashboard" not in c:
    # Buscar la línea exacta donde se redirige después del login
    # Patrón probable: 'return redirect("dashboard_estudiante")' o similar
    import re
    # Buscar cualquier return redirect en login_view
    i = c.find("def login_view(")
    j = c.find("def ", i+10)
    bloque = c[i:j]
    print("=== Vista login_view actual ===")
    print(bloque[:1500])
    print()
    print("Pégame este bloque y te doy el fix exacto.")
else:
    print("[SKIP] ya estaba")