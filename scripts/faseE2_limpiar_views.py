"""Fase E2: limpiar views.py preservando SOLO las 13 defs activas.

Estrategia:
  1. Backup views.py -> views.py.bak
  2. Generar nuevo views.py con solo defs activas (ultima ocurrencia)
  3. Verificar con manage.py check + pytest
  4. Si OK -> borrar backup
  5. Si falla -> restaurar backup
"""
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
VIEWS = BASE / "core" / "views.py"
BACKUP = BASE / "core" / "views.py.bak"


def safe(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))


def run(cmd):
    r = subprocess.run(cmd, shell=True, cwd=str(BASE), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


# ============================================================
# 1) Determinar vistas activas via Django
# ============================================================
import os
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.urls import get_resolver

vistas_activas = set()
def walk(patterns):
    for p in patterns:
        if hasattr(p, "url_patterns"):
            walk(p.url_patterns)
        else:
            mod = p.callback.__module__ if hasattr(p.callback, "__module__") else "?"
            func = p.callback.__name__ if hasattr(p.callback, "__name__") else "?"
            if mod == "core.views":
                vistas_activas.add(func)

walk(get_resolver().url_patterns)

safe("=" * 70)
safe("VISTAS ACTIVAS EN core.views")
safe("=" * 70)
for v in sorted(vistas_activas):
    safe(f"  {v}")
safe("")


# ============================================================
# 2) Backup
# ============================================================
if BACKUP.exists():
    safe(f"[SKIP] Backup ya existe: {BACKUP}")
else:
    BACKUP.write_text(VIEWS.read_text(encoding="utf-8"), encoding="utf-8")
    safe(f"[OK] Backup creado: {BACKUP} ({BACKUP.stat().st_size} bytes)")


# ============================================================
# 3) Parsear views.py
# ============================================================
c = VIEWS.read_text(encoding="utf-8")
lineas = c.split("\n")
safe(f"[INFO] views.py: {len(lineas)} lineas")

# Encontrar todas las defs
patron_def = re.compile(r"^(def|class)\s+(\w+)")
defs = []

for i, l in enumerate(lineas):
    m = patron_def.match(l)
    if m:
        # Buscar decoradores arriba (mientras sean @ o lineas vacias que no cierren el bloque)
        inicio = i
        j = i - 1
        while j >= 0:
            s = lineas[j].strip()
            if s.startswith("@"):
                inicio = j
                j -= 1
            elif s == "":
                # linea vacia antes de decorador: puede ser separador
                # solo saltamos si la linea anterior es decorador
                if j > 0 and lineas[j-1].strip().startswith("@"):
                    inicio = j
                    j -= 1
                else:
                    break
            else:
                break

        defs.append({
            "nombre": m.group(2),
            "tipo": m.group(1),
            "linea_def": i,
            "linea_inicio": inicio,
        })

# Calcular fin de cada def
for idx, d in enumerate(defs):
    if idx + 1 < len(defs):
        d["linea_fin"] = defs[idx + 1]["linea_inicio"] - 1
    else:
        d["linea_fin"] = len(lineas) - 1

safe(f"[INFO] Total defs encontradas: {len(defs)}")


# ============================================================
# 4) Determinar que lineas borrar
# ============================================================
por_nombre = defaultdict(list)
for d in defs:
    por_nombre[d["nombre"]].append(d)

consumidas = set()
preservadas = []

for nombre, lista in por_nombre.items():
    if nombre in vistas_activas:
        # Preservar solo la ULTIMA
        for d in lista[:-1]:
            for i in range(d["linea_inicio"], d["linea_fin"] + 1):
                consumidas.add(i)
        preservadas.append(lista[-1])
    else:
        # Borrar todas
        for d in lista:
            for i in range(d["linea_inicio"], d["linea_fin"] + 1):
                consumidas.add(i)

safe(f"[INFO] Defs preservadas: {len(preservadas)}")
safe(f"[INFO] Lineas a borrar:  {len(consumidas)}")

# Verificar lineas NO consumidas que NO sean parte de una def
# (para no borrar codigo global: imports, constantes, etc)
def cubierta(x):
    for d in defs:
        if d["linea_inicio"] <= x <= d["linea_fin"]:
            return True
    return False

lineas_globales_no_cubiertas = []
for i, l in enumerate(lineas):
    if i in consumidas:
        continue
    if cubierta(i):
        continue
    # Linea no esta en ninguna def
    lineas_globales_no_cubiertas.append((i, l))

safe(f"[INFO] Lineas fuera de defs (imports, constantes): {len(lineas_globales_no_cubiertas)}")


# ============================================================
# 5) Generar nuevo archivo
# ============================================================
lineas_nuevas = []
for i, l in enumerate(lineas):
    if i not in consumidas:
        lineas_nuevas.append(l)

# Limpiar lineas vacias excesivas (3+ seguidas -> 2)
limpias = []
vacias = 0
for l in lineas_nuevas:
    if l.strip() == "":
        vacias += 1
        if vacias <= 2:
            limpias.append(l)
    else:
        vacias = 0
        limpias.append(l)

nuevo_contenido = "\n".join(limpias)

safe("")
safe("=" * 70)
safe("RESULTADO (dry run)")
safe("=" * 70)
safe(f"  Lineas originales:  {len(lineas)}")
safe(f"  Lineas nuevas:      {len(limpias)}")
safe(f"  Reduccion:          {len(lineas) - len(limpias)} lineas")

# Verificar que las 13 activas están presentes
faltantes = []
for nombre in vistas_activas:
    if not any(d["nombre"] == nombre for d in preservadas):
        faltantes.append(nombre)

if faltantes:
    safe("")
    safe("[!] FALTAN VISTAS ACTIVAS:")
    for f in faltantes:
        safe(f"    - {f}")
    safe("")
    safe("[ABORT] No se aplicaron cambios")
    sys.exit(1)
else:
    safe("")
    safe("[OK] Todas las vistas activas estan presentes")


# ============================================================
# 6) Escribir y verificar
# ============================================================
VIEWS.write_text(nuevo_contenido, encoding="utf-8")
safe("")
safe("[OK] views.py sobreescrito")


# Verificacion Django
safe("")
safe("=" * 70)
safe("VERIFICACION")
safe("=" * 70)

code, out, err = run(r"E:\PythonPortable_Django5\python.exe manage.py check")
safe(f"  manage.py check -> exit={code}")
if out.strip():
    safe(f"  {out.strip()[:200]}")

# Verificacion pytest
code2, out2, err2 = run(
    r"E:\PythonPortable_Django5\python.exe -m pytest -q --tb=line --no-header -p no:cacheprovider"
)
safe(f"  pytest -> exit={code2}")
for l in (out2 + err2).strip().split("\n")[-3:]:
    safe(f"  {l}")


# ============================================================
# 7) Decidir: mantener o restaurar
# ============================================================
if code == 0 and code2 == 0:
    safe("")
    safe("[OK] Todo funciona. Borrando backup.")
    BACKUP.unlink()
    safe(f"[OK] Backup eliminado: {BACKUP}")
    safe("")
    safe("Siguiente:")
    safe("  git add core/views.py scripts/diag_views_e2.py scripts/faseE2_limpiar_views.py")
    safe("  git commit -m \"refactor(views): eliminar 34 defs huerfanas + 10 duplicadas (~1309 lineas)\"")
    safe("  git push")
else:
    safe("")
    safe("[!] Algo fallo. Restaurando backup.")
    VIEWS.write_text(BACKUP.read_text(encoding="utf-8"), encoding="utf-8")
    BACKUP.unlink()
    safe("[OK] views.py restaurado al estado original")
    sys.exit(1)
