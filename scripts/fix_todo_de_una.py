from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

print("=" * 60)
print("FIX 1/2 — views_recursos.py import")
print("=" * 60)

vp = BASE / "core" / "views_recursos.py"
c = vp.read_text(encoding="utf-8")

viejo = "from .models import Curso, Modulo, Leccion, EvaluacionCurso, EjercicioLinguistico"
nuevo = (
    "from .models import EjercicioLinguistico\n"
    "from .models_cursos import Curso, Modulo, Leccion, EvaluacionCurso"
)

if viejo in c:
    c = c.replace(viejo, nuevo)
    vp.write_text(c, encoding="utf-8")
    print("[OK] import corregido")
elif "from .models_cursos import Curso" in c:
    print("[SKIP] ya estaba corregido")
else:
    print("[!] No se encontró la línea esperada. Revisa manualmente")

# Quitar duplicados de 'from .models import Recurso'
lineas = c.split("\n")
vistos = set()
resultado = []
for l in lineas:
    stripped = l.strip()
    if stripped.startswith("from .models import") or stripped.startswith("from .models_cursos import"):
        if stripped in vistos:
            print(f"[FIX] línea duplicada eliminada: {stripped}")
            continue
        vistos.add(stripped)
    resultado.append(l)
c = "\n".join(resultado)
vp.write_text(c, encoding="utf-8")

print()
print("Imports finales en views_recursos.py:")
for l in c.split("\n"):
    if "import" in l and ("models" in l or "auth" in l):
        print("  " + l.strip())

print()
print("=" * 60)
print("FIX 2/2 — Leccion.ejercicios_relacionados related_name")
print("=" * 60)

mp = BASE / "core" / "models_cursos.py"
c2 = mp.read_text(encoding="utf-8")

if "related_name='lecciones_relacionadas'" in c2 or 'related_name="lecciones_relacionadas"' in c2:
    print("[SKIP] ya tiene related_name='lecciones_relacionadas'")
else:
    # El campo es: ejercicios_relacionados = models.ManyToManyField(EjercicioLinguistico, blank=True)
    patron = re.compile(
        r"(ejercicios_relacionados\s*=\s*models\.ManyToManyField\s*\(\s*EjercicioLinguistico\s*,\s*blank\s*=\s*True\s*)(\))"
    )
    if patron.search(c2):
        c2 = patron.sub(r"\1, related_name='lecciones_relacionadas'\2", c2, count=1)
        mp.write_text(c2, encoding="utf-8")
        print("[OK] related_name='lecciones_relacionadas' añadido")
    else:
        # Fallback: buscar cualquier forma del campo
        patron2 = re.compile(
            r"(ejercicios_relacionados\s*=\s*models\.ManyToManyField\s*\(\s*[^)]*?)(\))",
            re.DOTALL,
        )
        if patron2.search(c2):
            c2 = patron2.sub(r"\1, related_name='lecciones_relacionadas'\2", c2, count=1)
            mp.write_text(c2, encoding="utf-8")
            print("[OK] related_name añadido (fallback)")
        else:
            print("[!] No se encontró el campo. Búscalo manualmente")

# Mostrar el resultado
c2 = mp.read_text(encoding="utf-8")
m = re.search(r"ejercicios_relacionados[^\n]*", c2)
if m:
    print()
    print("Campo resultante:")
    print("  " + m.group(0).strip())

print()
print("=" * 60)
print("LISTO. Ahora ejecuta:")
print("=" * 60)
print("  1) E:\\PythonPortable_Django5\\python.exe manage.py makemigrations core")
print("  2) E:\\PythonPortable_Django5\\python.exe manage.py migrate")
print("  3) E:\\PythonPortable_Django5\\python.exe manage.py check")
