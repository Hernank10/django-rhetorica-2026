from pathlib import Path

p = Path(r"core\views_recursos.py")
c = p.read_text(encoding="utf-8")

viejo = "from .models import Curso, Modulo, Leccion, EvaluacionCurso, EjercicioLinguistico"
nuevo = (
    "from .models import EjercicioLinguistico, Recurso\n"
    "from .models_cursos import Curso, Modulo, Leccion, EvaluacionCurso"
)

if viejo in c:
    c = c.replace(viejo, nuevo)
    p.write_text(c, encoding="utf-8")
    print("[OK] Import corregido en views_recursos.py")
else:
    # Por si acaso ya está corregido o con otra forma
    if "from .models_cursos import Curso" in c:
        print("[SKIP] Ya estaba corregido")
    else:
        print("[!] No se encontró la línea esperada. Revisa manualmente")
