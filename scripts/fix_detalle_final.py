"""Eliminar v1 de detalle_curso con verificacion exhaustiva."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
vp = BASE / "core" / "views_cursos_completo.py"
c = vp.read_text(encoding="utf-8", errors="replace")
lineas = c.split("\n")


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


# ============================================================
# 1) Localizar las 2 defs y la def de ver_leccion
# ============================================================
idx_detalle = []
idx_ver_leccion = None

for i, l in enumerate(lineas):
    if l.strip().startswith("def detalle_curso("):
        idx_detalle.append(i)
    if l.strip().startswith("def ver_leccion("):
        idx_ver_leccion = i

safe(f"detalle_curso en lineas: {[x+1 for x in idx_detalle]}")
safe(f"ver_leccion en linea:    {idx_ver_leccion+1 if idx_ver_leccion else 'NO ENCONTRADA'}")

if len(idx_detalle) != 2:
    safe(f"[ABORT] Se esperaban 2 defs de detalle_curso, hay {len(idx_detalle)}")
    exit(1)

if idx_ver_leccion is None:
    safe("[ABORT] ver_leccion no encontrada")
    exit(1)

if not (idx_detalle[0] < idx_ver_leccion < idx_detalle[1]):
    safe("[ABORT] ver_leccion no esta entre las 2 defs")
    exit(1)


# ============================================================
# 2) Determinar rango exacto a eliminar (v1)
# ============================================================
# Inicio: @login_required inmediatamente arriba de v1
inicio = idx_detalle[0]
if lineas[inicio - 1].strip() == "@login_required":
    inicio -= 1
else:
    safe("[ABORT] No hay @login_required arriba de la primera def")
    exit(1)

# Fin: @login_required de ver_leccion (no incluirlo)
fin = idx_ver_leccion
if lineas[fin - 1].strip() == "@login_required":
    fin -= 1  # apuntar al @login_required de ver_leccion
else:
    safe("[ABORT] No hay @login_required arriba de ver_leccion")
    exit(1)

safe("")
safe(f"Rango a eliminar: lineas {inicio+1} a {fin}  ({fin - inicio} lineas)")


# ============================================================
# 3) Verificar que SOLO contiene la v1 de detalle_curso
# ============================================================
bloque = lineas[inicio:fin]

# Contar defs en el bloque
defs_en_bloque = [l.strip() for l in bloque if l.strip().startswith("def ")]

safe(f"Funciones en el bloque: {defs_en_bloque}")

if len(defs_en_bloque) != 1 or "detalle_curso" not in defs_en_bloque[0]:
    safe(f"[ABORT] El bloque contiene otras funciones: {defs_en_bloque}")
    exit(1)

# Verificar que NO contiene import/class/etc
for i, l in enumerate(bloque):
    if l.strip().startswith("class ") or l.strip().startswith("import "):
        safe(f"[ABORT] El bloque contiene '{l.strip()}' en posicion {i+1}")
        exit(1)

safe("[OK] El bloque solo contiene detalle_curso v1")


# ============================================================
# 4) Guardar backup y aplicar
# ============================================================
backup_path = vp.with_suffix(".py.bak")
backup_path.write_text(c, encoding="utf-8")
safe(f"[OK] Backup guardado en {backup_path.name}")


# Eliminar del bloque
nuevas_lineas = lineas[:inicio] + lineas[fin:]
nuevo_c = "\n".join(nuevas_lineas)
vp.write_text(nuevo_c, encoding="utf-8")


# ============================================================
# 5) Verificacion posterior
# ============================================================
safe("")
safe("=" * 70)
safe("VERIFICACION POSTERIOR")
safe("=" * 70)
safe(f"  Lineas antes:  {len(lineas)}")
safe(f"  Lineas despues: {len(nuevas_lineas)}")
safe(f"  Eliminadas:    {len(lineas) - len(nuevas_lineas)}")

c2 = vp.read_text(encoding="utf-8", errors="replace")
checks = [
    ("def lista_cursos", 1),
    ("def detalle_curso", 1),
    ("def ver_leccion", 1),
    ("def ver_evaluacion", 1),
    ("def enviar_evaluacion", 1),
    ("def resultado_evaluacion", 1),
    ("def api_evaluacion_preguntas", 1),
]

all_ok = True
for patron, esperado in checks:
    n = c2.count(patron)
    marca = "[OK]" if n == esperado else "[!]"
    if n != esperado:
        all_ok = False
    safe(f"  {marca} {patron}: {n} (esperado {esperado})")

if not all_ok:
    safe("")
    safe("[!] Algo no cuadra. Restaurando backup...")
    vp.write_text(c, encoding="utf-8")
    safe("[OK] Archivo restaurado")
    exit(1)

safe("")
safe("[OK] Fix aplicado correctamente. Elimina el .bak cuando confirmes:")
safe(f"  del {backup_path}")