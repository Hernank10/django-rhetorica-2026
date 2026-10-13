"""Fix definitivo: usar user_id en las 3 queries de dashboard_gamificacion."""
from pathlib import Path

p = Path(r"E:\02_proyectos\django-rhetorica\core\views.py")
c = p.read_text(encoding="utf-8")
lineas = c.split("\n")

# Encontrar la funcion dashboard_gamificacion
idx_def = None
for i, l in enumerate(lineas):
    if l.strip().startswith("def dashboard_gamificacion"):
        idx_def = i
        break

if idx_def is None:
    print("[!] No encontrada dashboard_gamificacion")
    exit(1)

print(f"  dashboard_gamificacion en linea {idx_def+1}")

# Buscar las 3 lineas de filtro
patrones = {
    "logros_obtenidos": "logros_obtenidos = LogroObtenido.objects.filter(user=usuario)",
    "certificaciones_obtenidas": "certificaciones_obtenidas = CertificacionObtenida.objects.filter(user=usuario)",
    "progreso": "progreso = ProgresoCategoria.objects.filter(user=usuario)",
}

reemplazos = {
    "logros_obtenidos": "logros_obtenidos = LogroObtenido.objects.filter(user_id=usuario_id)",
    "certificaciones_obtenidas": "certificaciones_obtenidas = CertificacionObtenida.objects.filter(user_id=usuario_id)",
    "progreso": "progreso = ProgresoCategoria.objects.filter(user_id=usuario_id)",
}

cambios = 0
for i in range(idx_def, min(idx_def + 100, len(lineas))):
    for nombre, viejo in patrones.items():
        if viejo in lineas[i]:
            lineas[i] = lineas[i].replace(viejo, reemplazos[nombre])
            print(f"  [OK] Reemplazado linea {i+1}: {nombre}")
            cambios += 1

# Anadir 'usuario_id = request.user.pk' justo antes de logros_obtenidos
for i in range(idx_def, min(idx_def + 100, len(lineas))):
    if "logros_obtenidos = LogroObtenido.objects.filter(user_id=usuario_id)" in lineas[i]:
        # Insertar una linea antes
        lineas.insert(i, "    usuario_id = request.user.pk")
        print(f"  [OK] 'usuario_id = request.user.pk' insertado antes de linea {i+1}")
        cambios += 1
        break

if cambios == 0:
    print("[SKIP] No se aplicaron cambios")
    exit(0)

c_nuevo = "\n".join(lineas)
p.write_text(c_nuevo, encoding="utf-8")
print(f"\n  [OK] {cambios} cambios aplicados")


# Verificacion
print()
print("=" * 60)
print("VERIFICACION")
print("=" * 60)
c = p.read_text(encoding="utf-8")
import re
m = re.search(r"def\s+dashboard_gamificacion\s*\([^)]*\):(.*?)(?=^def |^@|\Z)", c, re.MULTILINE | re.DOTALL)
if m:
    for i, l in enumerate(m.group(0).split("\n")[:30], 1):
        if "usuario_id" in l or "usuario = request" in l or "objects.filter" in l:
            print(f"  {i:3}: {l}")
