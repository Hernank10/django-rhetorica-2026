from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
c = p.read_text(encoding="utf-8")

# 1) Eliminar bloques completos if DEBUG: ALLOWED_HOSTS... (con o sin else)
c = re.sub(
    r"(?m)^[ \t]*if\s+DEBUG\s*:\s*\n[ \t]*ALLOWED_HOSTS\s*=\s*\[[^\]]*\]\s*\n"
    r"(?:[ \t]*else\s*:\s*\n[ \t]*ALLOWED_HOSTS\s*=\s*\[[^\]]*\]\s*\n)?",
    "", c)

# 2) Eliminar cualquier ALLOWED_HOSTS suelto
c = re.sub(r"(?m)^[ \t]*ALLOWED_HOSTS\s*=\s*\[[^\]]*\]\s*\n", "", c)

# 3) Eliminar if DEBUG huerfano (sin cuerpo indentado)
c = re.sub(r"(?m)^[ \t]*if\s+DEBUG\s*:\s*\n(?![ \t]+\S)", "", c)

# 4) Eliminar else huerfano en columna 0 (sin cuerpo indentado)
c = re.sub(r"(?m)^else\s*:\s*\n(?![ \t]+\S)", "", c)

# 5) Colapsar lineas vacias multiples
c = re.sub(r"\n{4,}", "\n\n\n", c)

# 6) Asegurar DEBUG = True una sola vez
lineas = c.split("\n")
encontrado = False
out = []
for l in lineas:
    if l.strip() == "DEBUG = True":
        if not encontrado:
            out.append(l)
            encontrado = True
        # si ya estaba, saltar
    else:
        out.append(l)
c = "\n".join(out)
if not encontrado:
    c = "DEBUG = True\n" + c

# 7) Anadir bloque limpio al final
bloque = """

# -------------------------------------------------------------
# Hosts permitidos
# -------------------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
else:
    ALLOWED_HOSTS = ["rhetorica.com", "www.rhetorica.com"]
"""
if "Hosts permitidos" not in c:
    c = c.rstrip() + "\n" + bloque

p.write_text(c, encoding="utf-8")

# Reporte
print(f"DEBUG = True: {len(re.findall(r'(?m)^DEBUG\\s*=\\s*True', c))}")
print(f"ALLOWED_HOSTS: {len(re.findall(r'(?m)^ALLOWED_HOSTS', c))}")
print(f"if DEBUG: {len(re.findall(r'(?m)^if DEBUG:', c))}")
print(f"else: {len(re.findall(r'(?m)^else:', c))}")
print()
print("[OK] settings.py limpio")