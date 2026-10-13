from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\django_retorica\settings.py")
c = p.read_text(encoding="utf-8")

# 1) quitar TODOS los bloques previos de "if DEBUG: ALLOWED_HOSTS..."
pat_bloque = re.compile(
    r"\n*#\s*-+\n#\s*DEV: hosts permitidos.*?(?=\n[A-Z_]|\Z)",
    re.DOTALL
)
c = pat_bloque.sub("\n", c)

pat_bloque2 = re.compile(
    r"\n*if DEBUG:\s*\n\s*ALLOWED_HOSTS\s*=\s*\[[^\]]*\]\s*\nelse:\s*\n\s*ALLOWED_HOSTS\s*=\s*\[[^\]]*\]\n*",
    re.MULTILINE
)
c = pat_bloque2.sub("\n", c)

# 2) quitar DUPLICADOS de DEBUG = True (dejar solo el primero)
veces = len(re.findall(r"^DEBUG\s*=\s*True", c, flags=re.MULTILINE))
if veces > 1:
    # borrar todos y volver a poner 1
    c = re.sub(r"^DEBUG\s*=\s*True\s*$", "", c, flags=re.MULTILINE)
    # insertar uno al principio (después de los imports)
    idx = c.find("\n\n")
    c = c[:idx] + "\n\nDEBUG = True\n" + c[idx:]

# 3) quitar TODAS las líneas ALLOWED_HOSTS = [...] sueltas
c = re.sub(r"^\s*ALLOWED_HOSTS\s*=\s*\[[^\]]*\]\s*$", "", c, flags=re.MULTILINE)

# 4) añadir UNA sola vez el bloque limpio al final
bloque_final = """

# -------------------------------------------------------------
# Hosts permitidos
# -------------------------------------------------------------
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver", "[::1]"]
else:
    ALLOWED_HOSTS = ["rhetorica.com", "www.rhetorica.com"]
"""
if "Hosts permitidos" not in c:
    c = c.rstrip() + "\n" + bloque_final

# 5) limpiar lineas vacias múltiples
c = re.sub(r"\n{4,}", "\n\n\n", c)

p.write_text(c, encoding="utf-8")

# reporte
print(f"[OK] DEBUG = True: {len(re.findall(r'^DEBUG\s*=\s*True', c, flags=re.MULTILINE))} vez/veces")
print(f"[OK] ALLOWED_HOSTS: {len(re.findall(r'^ALLOWED_HOSTS', c, flags=re.MULTILINE))} linea(s)")
print(f"[OK] if DEBUG: {len(re.findall(r'^if DEBUG:', c, flags=re.MULTILINE))} bloque(s)")
