from pathlib import Path
import re

p = Path(r"E:\02_proyectos\django-rhetorica\core\urls.py")
c = p.read_text(encoding="utf-8")

# 1) Asegurar import de views_profesor
if "import views_profesor as prof" not in c:
    c = c.replace(
        "from . import views",
        "from . import views\nfrom . import views_profesor as prof"
    )
    print("[OK] import views_profesor añadido")

# 2) Bloque de URLs del profesor
bloque_urls = '''
    # ============================================================
    # PANEL DEL PROFESOR (nuevo)
    # ============================================================
    path('profesor/', prof.dashboard, name='profesor_dashboard'),
    path('profesor/estudiantes/', prof.lista_estudiantes, name='profesor_estudiantes'),
    path('profesor/estudiantes/<int:estudiante_id>/', prof.detalle_estudiante, name='profesor_estudiante_detalle'),
    path('profesor/evaluaciones/', prof.lista_evaluaciones, name='profesor_evaluaciones'),
    path('profesor/certificaciones/', prof.lista_certificaciones, name='profesor_certificaciones'),
    path('profesor/cursos/', prof.cursos_lista, name='profesor_cursos_lista'),
    path('profesor/cursos/crear/', prof.curso_form, name='profesor_curso_crear'),
    path('profesor/cursos/<int:curso_id>/editar/', prof.curso_form, name='profesor_curso_editar'),
    path('profesor/cursos/<int:curso_id>/eliminar/', prof.curso_eliminar, name='profesor_curso_eliminar'),
    path('profesor/lecciones/', prof.lecciones_lista, name='profesor_lecciones_lista'),
    path('profesor/lecciones/crear/', prof.leccion_form, name='profesor_leccion_crear'),
    path('profesor/lecciones/<int:leccion_id>/editar/', prof.leccion_form, name='profesor_leccion_editar'),
    path('profesor/lecciones/<int:leccion_id>/eliminar/', prof.leccion_eliminar, name='profesor_leccion_eliminar'),
'''

# Insertar justo después del inicio de i18n_patterns(
patron = re.compile(r"(urlpatterns \+= i18n_patterns\(\r?\n)")
if patron.search(c) and "profesor/estudiantes/" not in c:
    c = patron.sub(r"\1" + bloque_urls, c, count=1)
    p.write_text(c, encoding="utf-8")
    print("[OK] URLs del profesor añadidas")
else:
    print("[SKIP] ya estaba o no encontrado i18n_patterns")
