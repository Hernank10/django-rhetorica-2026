"""Fix definitivo de ver_evaluacion: usa regex para tolerar whitespace variable."""
from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")
vp = BASE / "core" / "views_cursos_completo.py"
c = vp.read_text(encoding="utf-8")

if "leccion = modulo.lecciones.order_by" in c:
    print("[SKIP] Vista ya estaba corregida")
else:
    # Paso 1: insertar el calculo de 'leccion' justo despues de 'modulo = evaluacion.modulo'
    # Usamos regex con \s* para tolerar cualquier whitespace
    patron1 = re.compile(
        r"(    modulo = evaluacion\.modulo[ \t]*\n)",
        re.MULTILINE,
    )
    bloque_nuevo = (
        r"\1"
        r"\n"
        r"    # Primera leccion del modulo (para breadcrumb y boton Volver)\n"
        r"    leccion = None\n"
        r"    if modulo is not None:\n"
        r"        leccion = modulo.lecciones.order_by('orden').first()\n"
    )

    if patron1.search(c):
        c = patron1.sub(bloque_nuevo, c, count=1)
        print("[OK] Bloque 'leccion = ...' insertado despues de 'modulo = ...'")
    else:
        print("[!] No se encontro 'modulo = evaluacion.modulo'")

    # Paso 2: reemplazar 'leccion': None por 'leccion': leccion
    # Tambien con regex para tolerar indentacion variable
    patron2 = re.compile(r"(['\"]leccion['\"]\s*:\s*)None\b")
    if patron2.search(c):
        c = patron2.sub(r"\1leccion", c, count=1)
        print("[OK] 'leccion': None -> 'leccion': leccion")
    else:
        print("[!] No se encontro 'leccion': None")

    vp.write_text(c, encoding="utf-8")


# ============================================================
# Verificacion
# ============================================================
print()
print("=" * 60)
print("VERIFICACION")
print("=" * 60)

c = vp.read_text(encoding="utf-8")
m = re.search(r"def\s+ver_evaluacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    print("Bloque ver_evaluacion (con repr):")
    for i, l in enumerate(m.group(0).split("\n")):
        print(f"  {i:3}: {repr(l)}")

print()
print("Checks:")
print("  Tiene 'leccion = None':           ", "leccion = None" in c)
print("  Tiene 'if modulo is not None':    ", "if modulo is not None" in c)
print("  Tiene 'modulo.lecciones.order_by':", "modulo.lecciones.order_by" in c)
print("  'leccion': None sigue existiendo: ", bool(re.search(r"['\"]leccion['\"]\s*:\s*None\b", c)))