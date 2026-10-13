from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
c = p.read_text(encoding="utf-8")

# 1) quitar TODO lo que huela a ALLOWED_HOSTS (linea por linea)
lines = c.split("\n")
out = []
saltar = 0
for i, l in enumerate(lines):
    s = l.strip()
    if "ALLOWED_HOSTS" in s:
        saltar = 1
        continue
    if s == "if DEBUG:" and i + 1 < len(lines) and "ALLOWED_HOSTS" in lines[i+1]:
        saltar = 1
        continue
    out.append(l)
c = "\n".join(out)

# 2) colapsar vacias
c = re.sub(r"\n{4,}", "\n\n\n", c)

# 3) bloquear la adicion si aun asi hay algo
if re.search(r"(?m)^[ \t]*ALLOWED_HOSTS", c):
    print("[WARN] Aun quedan ALLOWED_HOSTS, revisar manualmente")

# 4) anadir bloque
bloque = '''

# -------------------------------------------------------------
# Hosts permitidos (testserver para Django test Client)
# -------------------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
else:
    ALLOWED_HOSTS = ["rhetorica.com", "www.rhetorica.com"]
'''
c = c.rstrip() + bloque

p.write_text(c, encoding="utf-8")

# reporte
print("[OK] escrito")
print(f"DEBUG = True: {len(re.findall(r'(?m)^DEBUG = True', c))}")
print(f"ALLOWED_HOSTS: {len(re.findall(r'(?m)^[ \\t]*ALLOWED_HOSTS', c))}")
print(f"if DEBUG: {len(re.findall(r'(?m)^if DEBUG:', c))}")
