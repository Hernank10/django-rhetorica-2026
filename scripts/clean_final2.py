from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
lines = p.read_text(encoding="utf-8").split("\n")

out = []
i = 0
bloques_quitados = 0
while i < len(lines):
    l = lines[i]
    # detectar inicio de bloque if DEBUG: ALLOWED_HOSTS
    if l.strip() == "if DEBUG:" and i + 1 < len(lines) and "ALLOWED_HOSTS" in lines[i+1]:
        # saltar este bloque completo (if + 1 linea indentada)
        bloques_quitados += 1
        i += 2
        # saltar linea vacia siguiente si hay
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        continue
    out.append(l)
    i += 1

c = "\n".join(out)

# limpiar lineas vacias multiples
import re
c = re.sub(r"\n{4,}", "\n\n\n", c)

# anadir bloque limpio al final
if "Hosts permitidos" not in c:
    c = c.rstrip() + '''

# -------------------------------------------------------------
# Hosts permitidos
# -------------------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
else:
    ALLOWED_HOSTS = ["rhetorica.com", "www.rhetorica.com"]
'''

p.write_text(c, encoding="utf-8")
print(f"[OK] Bloques if DEBUG: ALLOWED_HOSTS quitados: {bloques_quitados}")
print(f"[OK] lineas totales: {len(c.splitlines())}")
