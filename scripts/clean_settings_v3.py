from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
lines = p.read_text(encoding="utf-8").split("\n")

out = []
i = 0
quitados = 0
while i < len(lines):
    l = lines[i]
    s = l.strip()
    # saltar bloque if DEBUG: <linea con ALLOWED_HOSTS>
    if s == "if DEBUG:" and i + 1 < len(lines) and "ALLOWED_HOSTS" in lines[i+1]:
        quitados += 1
        i += 2
        # saltar la siguiente linea del bloque si tambien es ALLOWED_HOSTS
        if i < len(lines) and "ALLOWED_HOSTS" in lines[i]:
            i += 1
        # saltar lineas vacias
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        continue
    out.append(l)
    i += 1

c = "\n".join(out)

# limpiar lineas vacias multiples
import re
c = re.sub(r"\n{4,}", "\n\n\n", c)

# anadir UN bloque limpio si no existe
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
print(f"[OK] Bloques quitados: {quitados}")
print(f"[OK] Lineas totales: {len(c.splitlines())}")
print(f"[OK] ALLOWED_HOSTS restantes: {len(re.findall(r'(?m)^[ \\t]*ALLOWED_HOSTS', c))}")
print(f"[OK] if DEBUG restantes: {len(re.findall(r'(?m)^if DEBUG:', c))}")