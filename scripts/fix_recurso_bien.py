from pathlib import Path
import re

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) FKs en Recurso — DENTRO DE LA CLASE Recurso, NO en otra
# ============================================================
print("=" * 60)
print("1) FKs en class Recurso")
print("=" * 60)

mp = BASE / "core" / "models.py"
c = mp.read_text(encoding="utf-8")

if "modulo = models.ForeignKey" in c and "evaluacion_curso" in c:
    print("[SKIP] FKs ya están en el archivo")
else:
    # Encontrar el bloque de class Recurso
    m = re.search(
        r"(class\s+Recurso\s*\(models\.Model\):)(.*?)(?=^class |\Z)",
        c,
        re.MULTILINE | re.DOTALL,
    )
    if not m:
        print("[!] No se encontró class Recurso")
        exit(1)

    cuerpo = m.group(2)

    # Insertar antes de 'creado_en = models.DateTimeField(auto_now_add=True)'
    # SOLO dentro del cuerpo de Recurso
    nuevos_campos = """
    modulo = models.ForeignKey(
        'core.Modulo', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    leccion = models.ForeignKey(
        'core.Leccion', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    evaluacion_curso = models.ForeignKey(
        'core.EvaluacionCurso', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    ejercicio = models.ForeignKey(
        'core.EjercicioLinguistico', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    orden = models.PositiveIntegerField(default=0)
    destacado = models.BooleanField(default=False)
"""

    if "creado_en = models.DateTimeField(auto_now_add=True)" in cuerpo:
        cuerpo_nuevo = cuerpo.replace(
            "    creado_en = models.DateTimeField(auto_now_add=True)",
            nuevos_campos + "    creado_en = models.DateTimeField(auto_now_add=True)",
            1,
        )
        c = c[:m.start(2)] + cuerpo_nuevo + c[m.end(2):]
        mp.write_text(c, encoding="utf-8")
        print("[OK] FKs insertadas DENTRO de class Recurso")
    else:
        print("[!] No se encontró 'creado_en' dentro de Recurso")

# Verificación: contar cuántas veces aparece cada campo
c = mp.read_text(encoding="utf-8")
print()
print("Verificación: apariciones en models.py")
for campo in ["modulo = models.ForeignKey", "leccion = models.ForeignKey",
              "evaluacion_curso = models.ForeignKey", "ejercicio = models.ForeignKey",
              "orden = models.PositiveIntegerField", "destacado = models.BooleanField"]:
    print(f"  {campo[:40]:42} → {c.count(campo)} vez/veces")

# ============================================================
# 2) related_name en Leccion.ejercicios_relacionados
# ============================================================
print()
print("=" * 60)
print("2) related_name en Leccion.ejercicios_relacionados")
print("=" * 60)

mpc = BASE / "core" / "models_cursos.py"
c2 = mpc.read_text(encoding="utf-8")

if "related_name='lecciones_relacionadas'" in c2:
    print("[SKIP] ya tenía related_name")
else:
    patron = re.compile(
        r"(ejercicios_relacionados\s*=\s*models\.ManyToManyField\s*\(\s*EjercicioLinguistico\s*,\s*blank\s*=\s*True\s*)(\))"
    )
    if patron.search(c2):
        c2 = patron.sub(r"\1, related_name='lecciones_relacionadas'\2", c2, count=1)
        mpc.write_text(c2, encoding="utf-8")
        print("[OK] related_name añadido")
    else:
        print("[!] No se encontró el campo. Aplica manual")

# ============================================================
# 3) Import en views_recursos.py
# ============================================================
print()
print("=" * 60)
print("3) Import en views_recursos.py")
print("=" * 60)

vp = BASE / "core" / "views_recursos.py"
if vp.exists():
    c3 = vp.read_text(encoding="utf-8")
    viejo = "from .models import Curso, Modulo, Leccion, EvaluacionCurso, EjercicioLinguistico"
    if viejo in c3:
        c3 = c3.replace(
            viejo,
            "from .models import EjercicioLinguistico\nfrom .models_cursos import Curso, Modulo, Leccion, EvaluacionCurso",
        )
        vp.write_text(c3, encoding="utf-8")
        print("[OK] import corregido")
    else:
        print("[SKIP] import ya estaba bien")

print()
print("=" * 60)
print("Ahora ejecuta:")
print("=" * 60)
print("  1) manage.py makemigrations core")
print("  2) manage.py migrate")
print("  3) manage.py check")