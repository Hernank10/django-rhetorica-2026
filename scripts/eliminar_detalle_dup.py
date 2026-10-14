"""Eliminar SOLO la primera version de detalle_curso (lineas 22-52).

Verifica antes y despues que lista_cursos y ver_leccion siguen intactas.
"""
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


# Verificar el estado ANTES
safe("=" * 75)
safe("ANTES")
safe("=" * 75)
safe(f"Total lineas: {len(lineas)}")

# Verificar que las lineas clave existen
def find_line(texto):
    for i, l in enumerate(lineas):
        if l.strip() == texto or l.startswith(texto):
            return i
    return -1


idx_lista = find_line("def lista_cursos(request):")
idx_ver_leccion = find_line("def ver_leccion(request, curso_slug, modulo_id, leccion_id):")
idx_detalle_2 = find_line("def detalle_curso(request, curso_slug):")

safe(f"  lista_cursos en linea: {idx_lista+1}")
safe(f"  primera detalle_curso en linea: {idx_detalle_2+1}")
safe(f"  ver_leccion en linea: {idx_ver_leccion+1}")


# Encontrar la SEGUNDA detalle_curso
detalle_lineas = []
for i, l in enumerate(lineas):
    if l.strip() == "def detalle_curso(request, curso_slug):":
        detalle_lineas.append(i)

safe(f"  Total detalle_curso: {len(detalle_lineas)} en lineas {[x+1 for x in detalle_lineas]}")

if len(detalle_lineas) != 2:
    safe("[ABORT] No hay exactamente 2 defs")
    exit(1)

# La primera esta en detalle_lineas[0]. Quitar desde el decorador arriba.
primera = detalle_lineas[0]
inicio = primera
if lineas[primera - 1].strip() == "@login_required":
    inicio = primera - 1

# Fin: linea vacia antes de la siguiente funcion
fin = detalle_lineas[1]
# Retroceder hasta encontrar "@login_required" de la segunda def
while fin > 0 and lineas[fin - 1].strip() != "@login_required":
    fin -= 1
# fin apunta al inicio de la segunda def (que queremos conservar)
# Quitamos desde 'inicio' hasta 'fin' (exclusivo)

safe("")
safe(f"  Rango a ELIMINAR: lineas {inicio+1} a {fin}  ({(fin - inicio)} lineas)")

# Verificar que entre esas lineas solo este la primera detalle_curso
bloque = "\n".join(lineas[inicio:fin])
if "def lista_cursos" in bloque or "def ver_leccion" in bloque:
    safe("[ABORT] El bloque contiene funciones importantes")
    exit(1)

safe("  [OK] El bloque solo contiene la primera detalle_curso")

# Aplicar
nuevas_lineas = lineas[:inicio] + lineas[fin:]
nuevo_c = "\n".join(nuevas_lineas)
vp.write_text(nuevo_c, encoding="utf-8")

safe("")
safe("=" * 75)
safe("DESPUES")
safe("=" * 75)
safe(f"Total lineas: {len(nuevas_lineas)} (antes {len(lineas)})")

# Verificar que todo sigue
c2 = vp.read_text(encoding="utf-8", errors="replace")
checks = [
    ("def lista_cursos", "lista_cursos"),
    ("def detalle_curso", "detalle_curso (debe haber 1)"),
    ("def ver_leccion", "ver_leccion"),
    ("def ver_evaluacion", "ver_evaluacion"),
    ("def enviar_evaluacion", "enviar_evaluacion"),
    ("def resultado_evaluacion", "resultado_evaluacion"),
    ("def api_evaluacion_preguntas", "api_evaluacion_preguntas"),
]
for patron, nombre in checks:
    count = c2.count(patron)
    marca = "[OK]" if count >= 1 else "[!]"
    safe(f"  {marca} {nombre}: {count} aparicion(es)")