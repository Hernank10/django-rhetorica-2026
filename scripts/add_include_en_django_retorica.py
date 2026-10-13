from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\urls.py")
c = p.read_text(encoding="utf-8")

# 1) Asegurar import de include
if "include" not in c.split("urlpatterns")[0]:
    c = re.sub(r"from django\.urls import ([^\n]+)", r"from django.urls import \1, include", c, count=1)
    print("[OK] include añadido al import")

# 2) Insertar la ruta del panel del profesor dentro de i18n_patterns
if "core.urls_profesor" not in c:
    # Buscar el inicio de i18n_patterns y añadir la ruta justo después
    patron = re.compile(r"(urlpatterns \+= i18n_patterns\(\r?\n)")
    reemplazo = r"\1    path('profesor/', include('core.urls_profesor')),\n"
    c2 = patron.sub(reemplazo, c, count=1)
    if c2 == c:
        print("[!] No se encontró 'urlpatterns += i18n_patterns('. Revisa manualmente")
    else:
        c = c2
        p.write_text(c, encoding="utf-8")
        print("[OK] path('profesor/', include(...)) añadido")
else:
    print("[SKIP] ya estaba")
    p.write_text(c, encoding="utf-8")

# 3) Verificación
print()
print("=== Primeras 20 lineas de urlpatterns ===")
idx = c.find("urlpatterns += i18n_patterns")
if idx == -1:
    idx = c.find("urlpatterns")
for l in c[idx:idx+600].split("\n")[:20]:
    print(l)
