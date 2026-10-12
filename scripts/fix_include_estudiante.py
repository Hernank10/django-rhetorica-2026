from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\urls.py")
c = p.read_text(encoding="utf-8")

# 1) Añadir include al import
if "include" not in c.split("urlpatterns")[0]:
    c = re.sub(r"from django\.urls import ([^\n]+)", r"from django.urls import \1, include", c, count=1)
    print("[OK] 'include' añadido al import")

# 2) Insertar el include del estudiante
if "core.urls_estudiante" not in c:
    patron = re.compile(r"(urlpatterns \+= i18n_patterns\(\r?\n)")
    reemplazo = r"\1    path('estudiante/', include('core.urls_estudiante')),\n"
    c2 = patron.sub(reemplazo, c, count=1)
    if c2 != c:
        c = c2
        print("[OK] path('estudiante/', include(...)) añadido")
    else:
        print("[!] No se encontró i18n_patterns(). Añádelo manualmente")

# 3) Verificar que core/urls_estudiante.py existe
up = Path(r"E:\02_proyectos\django-rhetorica\core\urls_estudiante.py")
if not up.exists():
    print("[!] core/urls_estudiante.py NO existe. Hay que ejecutar panel_estudiante.py primero")
else:
    print("[OK] core/urls_estudiante.py existe")

p.write_text(c, encoding="utf-8")

# 4) Mostrar primeras 30 lineas de i18n_patterns
idx = c.find("i18n_patterns(")
if idx > 0:
    print()
    print("=== Primeras 20 lineas de i18n_patterns ===")
    for l in c[idx:idx+900].split("\n")[:20]:
        print(l)