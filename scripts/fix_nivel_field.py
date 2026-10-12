from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\views_profesor.py")
c = p.read_text(encoding="utf-8")

# Bloque viejo (usa .values("nivel"))
viejo = '''    # --- Distribución de niveles ---
    niveles = (
        User.objects.filter(groups__name="Estudiante")
        .values("nivel")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    niveles_data = [{"nivel": n["nivel"] or "Sin nivel", "count": n["count"]} for n in niveles]
'''

# Bloque nuevo: distribución por rango de progreso
nuevo = '''    # --- Distribución por nivel de actividad (rangos de progreso) ---
    estudiantes_qs = User.objects.filter(groups__name="Estudiante").annotate(
        num_progresos=Count("progreso_lecciones", filter=Q(progreso_lecciones__completado=True))
    )
    rangos = [
        ("Sin actividad", 0, 0),
        ("Principiante (1-5)", 1, 5),
        ("Intermedio (6-20)", 6, 20),
        ("Avanzado (21-50)", 21, 50),
        ("Experto (51+)", 51, 10**9),
    ]
    niveles_data = []
    for nombre, min_, max_ in rangos:
        n = estudiantes_qs.filter(num_progresos__gte=min_, num_progresos__lte=max_).count()
        niveles_data.append({"nivel": nombre, "count": n})
'''

if viejo in c:
    c = c.replace(viejo, nuevo)
    p.write_text(c, encoding="utf-8")
    print("[OK] distribución por niveles reemplazada por rangos de progreso")
else:
    # Fallback: buscar por patrón
    pat = re.compile(
        r'# --- Distribución de niveles ---.*?niveles_data = \[.*?\]\n',
        re.DOTALL
    )
    c2, n = pat.subn(nuevo, c)
    if n:
        p.write_text(c2, encoding="utf-8")
        print(f"[OK] reemplazado con regex ({n} bloque/s)")
    else:
        print("[!] No se encontró. Pégame estas líneas:")
        idx = c.find("values(\"nivel\")")
        if idx > 0:
            print(c[idx-200:idx+400])

# Verificar compilación
import py_compile
try:
    py_compile.compile(str(p), doraise=True)
    print("[OK] compila sin errores")
except Exception as e:
    print(f"[!] Error: {e}")