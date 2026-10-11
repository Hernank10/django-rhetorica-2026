from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
lines = p.read_text(encoding="utf-8").split("\n")

# Buscar el último indice donde empieza el bloque corrupto
# Buscamos hacia atras desde el final: cualquier linea con
# "ALLOWED_HOSTS", "if DEBUG:", "else:", "Hosts permitidos", "# ----"
corte = len(lines)
for i in range(len(lines) - 1, -1, -1):
    s = lines[i].strip()
    if s in ("if DEBUG:", "else:", "") or \
       "ALLOWED_HOSTS" in s or \
       "Hosts permitidos" in s or \
       s.startswith("# ---") or \
       s == "#":
        continue
    # si es la linea que encontro una que NO pertenece al bloque
    corte = i + 1
    break

# Truncar hasta el corte
lines_limpias = lines[:corte]

# Asegurar que no queden lineas sueltas corruptas en las ultimas 5 lineas
while lines_limpias and lines_limpias[-1].strip() in ("else:", "if DEBUG:"):
    lines_limpias.pop()

c = "\n".join(lines_limpias).rstrip()

# Anadir bloque limpio
bloque = '''

# -------------------------------------------------------------
# Hosts permitidos (testserver para Django test Client)
# -------------------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
else:
    ALLOWED_HOSTS = ["rhetorica.com", "www.rhetorica.com"]
'''
c = c + bloque

p.write_text(c, encoding="utf-8")

import re
print("[OK] escrito")
print(f"DEBUG = True: {len(re.findall(r'(?m)^DEBUG = True', c))}")
print(f"if DEBUG:: {len(re.findall(r'(?m)^if DEBUG:', c))}")
print(f"ALLOWED_HOSTS: {len(re.findall(r'(?m)^[ \\t]*ALLOWED_HOSTS', c))}")
print(f"else:: {len(re.findall(r'(?m)^else:', c))}")
print()
print("=== Ultimas 12 lineas ===")
for l in c.splitlines()[-12:]:
    print(l)