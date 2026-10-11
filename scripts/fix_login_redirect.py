from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\views.py")
c = p.read_text(encoding="utf-8")

if "profesor:dashboard" not in c:
    # Buscar la línea con redirect('dashboard_estudiante') dentro de login_view
    pat = re.compile(
        r"(def login_view\(request\):.*?)return redirect\(['\"]dashboard_estudiante['\"]\)",
        re.DOTALL
    )
    nuevo = r'''\1if request.user.is_staff:
            return redirect("profesor:dashboard")
        return redirect("dashboard_estudiante")'''
    c2, n = pat.subn(nuevo, c, count=1)
    if n:
        p.write_text(c2, encoding="utf-8")
        print("[OK] login_view ahora redirige a /profesor/ si es staff")
    else:
        print("[!] No se encontró login_view con redirect. Hazlo a mano.")
else:
    print("[SKIP] ya estaba")