from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# Buscar todos los templates de detalle de curso
for p in BASE.rglob("*.html"):
    if "cursos" in str(p).lower() and ("detalle" in p.name.lower() or "curso" in p.name.lower()):
        print(f"\n{p.relative_to(BASE)}")
        try:
            c = p.read_text(encoding="utf-8", errors="replace")
            tiene = "recursos" in c.lower() and ("curso.recursos" in c or "recursos:para_objeto" in c)
            print(f"  ¿Tiene 'curso.recursos' o 'recursos:para_objeto'? {tiene}")
            print(f"  Tamaño: {len(c)} bytes")
            print(f"  ¿Extiende? {re.search(r'{% extends.*?%}', c).group(0) if re.search(r'{% extends.*?%}', c) else 'no'}")
        except Exception as e:
            print(f"  [ERR] {e}")