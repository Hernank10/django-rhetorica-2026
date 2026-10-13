"""Fix directo: reemplazar Helvetica-BoldItalic -> Helvetica-BoldOblique."""
from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\utils_certificados.py")
c = p.read_text(encoding="utf-8")

# Contar antes
n_antes = c.count("Helvetica-BoldItalic")

# Reemplazo global
c = c.replace("Helvetica-BoldItalic", "Helvetica-BoldOblique")

# Contar despues
n_despues = c.count("Helvetica-BoldItalic")

p.write_text(c, encoding="utf-8")
print(f"[OK] Reemplazos: {n_antes} -> {n_despues}")
print(f"[OK] Ahora hay {c.count('Helvetica-BoldOblique')} referencias a Helvetica-BoldOblique")


# Limpieza: quitar el bloque de alias que no funciono
if "def _registrar_alias_fuentes" in c:
    import re
    patron = re.compile(
        r"# -+\n# Alias de fuentes estandar.*?_registrar_alias_fuentes\(\)\n",
        re.DOTALL,
    )
    c2 = patron.sub("", c)
    if c2 != c:
        p.write_text(c2, encoding="utf-8")
        print("[OK] Bloque de alias fallido eliminado")