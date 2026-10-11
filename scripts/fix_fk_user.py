from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\models.py")
c = p.read_text(encoding="utf-8")

# 1) Asegurar import de settings
if "from django.conf import settings" not in c:
    # insertar tras los primeros imports
    c = re.sub(r"(from django\.db import models\r?\n)", r"\1from django.conf import settings\n", c, count=1)
    print("[OK] import settings añadido")

# 2) Cambiar FK que apuntan a User -> settings.AUTH_USER_MODEL
# Solo para LogroObtenido, CertificacionObtenida, Respuesta y el propio User
patrones = [
    # LogroObtenido.user
    (r"user = models\.ForeignKey\(User, on_delete=models\.CASCADE, related_name='logros_obtenidos'\)",
     "user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logros_obtenidos')"),
    # CertificacionObtenida.user
    (r"user = models\.ForeignKey\(User, on_delete=models\.CASCADE, related_name='certificaciones_obtenidas'\)",
     "user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificaciones_obtenidas')"),
    # Respuesta.user
    (r"user = models\.ForeignKey\(User, on_delete=models\.CASCADE, related_name='respuestas'\)",
     "user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='respuestas')"),
]

total = 0
for pat, rep in patrones:
    c2, n = re.subn(pat, rep, c)
    if n:
        c = c2
        total += n

# 3) Reportar otros FK a User que queden
otros = re.findall(r"^\s*\w+\s*=\s*models\.ForeignKey\(User[,\)]", c, flags=re.MULTILINE)
if otros:
    print(f"[WARN] FKs que siguen apuntando a 'User': {len(otros)}")
    for o in otros:
        print("   ", o.strip())

p.write_text(c, encoding="utf-8")
print(f"[OK] {total} FK actualizadas a settings.AUTH_USER_MODEL")