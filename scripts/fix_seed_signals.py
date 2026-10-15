"""Quita import de core.signals en seed_and_test.py."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
p = BASE / "core" / "management" / "commands" / "seed_and_test.py"
c = p.read_text(encoding="utf-8")

antes = c

# Quitar el import roto (3 variantes)
c = c.replace("        from core import signals as _signals\n", "")
c = c.replace("    from core import signals as _signals\n", "")
c = c.replace("from core import signals as _signals\n", "")

# Quitar cualquier llamada a _signals
lineas = []
for linea in c.split("\n"):
    if "_signals" in linea and "import" not in linea:
        # Comentarla en vez de borrar (para ver que existia)
        lineas.append("        # (removido) " + linea.strip())
    else:
        lineas.append(linea)
c = "\n".join(lineas)

p.write_text(c, encoding="utf-8")

if c != antes:
    print("[OK] seed_and_test.py limpiado")
else:
    print("[!] No se encontro el import. Pegame el archivo para revisarlo manualmente.")