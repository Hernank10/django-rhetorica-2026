# -*- coding: utf-8 -*-
"""URLs del panel del profesor con namespace 'profesor'."""
from django.urls import path
from . import views_profesor as prof

app_name = "profesor"

urlpatterns = [
    path('', prof.dashboard, name='dashboard'),
    path('estudiantes/', prof.lista_estudiantes, name='estudiantes'),
    path('estudiantes/<int:estudiante_id>/', prof.detalle_estudiante, name='estudiante_detalle'),
    path('evaluaciones/', prof.lista_evaluaciones, name='evaluaciones'),
    path('certificaciones/', prof.lista_certificaciones, name='certificaciones'),
    path('cursos/', prof.cursos_lista, name='cursos_lista'),
    path('cursos/crear/', prof.curso_form, name='curso_crear'),
    path('cursos/<int:curso_id>/editar/', prof.curso_form, name='curso_editar'),
    path('cursos/<int:curso_id>/eliminar/', prof.curso_eliminar, name='curso_eliminar'),
    path('lecciones/', prof.lecciones_lista, name='lecciones_lista'),
    path('lecciones/crear/', prof.leccion_form, name='leccion_crear'),
    path('lecciones/<int:leccion_id>/editar/', prof.leccion_form, name='leccion_editar'),
    path('lecciones/<int:leccion_id>/eliminar/', prof.leccion_eliminar, name='leccion_eliminar'),
    # Módulos
    path('modulos/', prof.modulos_lista, name='modulos_lista'),
    path('modulos/crear/', prof.modulo_form, name='modulo_crear'),
    path('modulos/<int:modulo_id>/editar/', prof.modulo_form, name='modulo_editar'),
    path('modulos/<int:modulo_id>/eliminar/', prof.modulo_eliminar, name='modulo_eliminar'),

    # Evaluaciones + Preguntas
    path('evaluaciones/crear/', prof.evaluacion_form, name='evaluacion_crear'),
    path('evaluaciones/<int:evaluacion_id>/', prof.evaluacion_detalle, name='evaluacion_detalle'),
    path('evaluaciones/<int:evaluacion_id>/editar/', prof.evaluacion_form, name='evaluacion_editar'),
    path('evaluaciones/<int:evaluacion_id>/eliminar/', prof.evaluacion_eliminar, name='evaluacion_eliminar'),
    path('evaluaciones/<int:evaluacion_id>/preguntas/crear/', prof.pregunta_form, name='pregunta_crear'),
    path('evaluaciones/<int:evaluacion_id>/preguntas/<int:pregunta_id>/editar/', prof.pregunta_form, name='pregunta_editar'),
    path('evaluaciones/<int:evaluacion_id>/preguntas/<int:pregunta_id>/eliminar/', prof.pregunta_eliminar, name='pregunta_eliminar'),
    path('cursos/<int:curso_id>/toggle/', prof.curso_toggle_publicar, name='curso_toggle'),
    path('estadisticas/', prof.estadisticas_dashboard, name='estadisticas'),
    path('ranking/', prof.ranking_estudiantes, name='ranking'),
    path('certificaciones/<int:certificado_id>/pdf/', prof.certificado_pdf, name='certificado_pdf'),
    path('certificaciones/<int:certificado_id>/docx/', prof.certificado_docx, name='certificado_docx'),
    path('certificaciones/<int:certificado_id>/preview/', prof.certificado_preview, name='certificado_preview'),
    path('recursos/', prof.recursos_lista, name='recursos_lista'),
    path('recursos/autovincular/', prof.recursos_autovincular, name='recursos_autovincular'),
    path('recursos/<int:recurso_id>/asignar/', prof.recurso_asignar, name='recurso_asignar'),
]
