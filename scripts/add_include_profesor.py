from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\urls.py")
c = p.read_text(encoding="utf-8")

# 1) Asegurar import de include
if "from django.urls import" in c and " include" not in c.split("\n")[0]:
    # ya hay from django.urls import ... probablemente
    pass
if "include" not in c.split("urlpatterns")[0]:
    c = c.replace(
        "from django.urls import path",
        "from django.urls import path, include",
        1
    )
    print("[OK] 'include' añadido al import")

# 2) Insertar el include del panel ANTES de todo en urlpatterns
nuevo_bloque = """urlpatterns = [
    # Panel del profesor (namespace 'profesor')
    path('profesor/', include('core.urls_profesor')),
"""

if "core.urls_profesor" not in c:
    c2 = re.sub(r"urlpatterns\s*=\s*\[\s*\n", nuevo_bloque, c, count=1)
    if c2 == c:
        # Fallback: buscar urlpatterns = [ sin \n
        c2 = re.sub(r"urlpatterns\s*=\s*\[", nuevo_bloque.rstrip(), c, count=1)
    if c2 == c:
        print("[!] No se pudo insertar el include. Revisa core/urls.py manualmente")
    else:
        c = c2
        p.write_text(c, encoding="utf-8")
        print("[OK] include de 'core.urls_profesor' añadido")
else:
    print("[SKIP] ya estaba el include")

# 3) Verificar
print()
print("=== Primeras 15 lineas de urlpatterns ===")
idx = c.find("urlpatterns")
for l in c[idx:idx+400].split("\n")[:15]:
    print(l)