"""

URL Configuration for django_retorica project.

"""

from django.conf import settings

from django.conf.urls.i18n import i18n_patterns

from django.conf.urls.static import static

from django.contrib import admin

from django.urls import include, path



from core import views_corpus, views_filologia, views_lectura, views_pos, views_redaccion, views_srs, views_tts

from core.views import (

    cambiar_contrasena,

    certificaciones_lista,

    dashboard_estudiante,

    dashboard_gamificacion,

    editar_perfil,

    enviar_respuesta,

    index,

    login_view,

    logout_view,

    perfil_usuario,

    registro_view,

    ver_tecnicas,

    verificar_certificado_publico,

)

from core.views_biblioteca import ejercicios_biblioteca

from core.views_cursos_completo import (

    api_evaluacion_preguntas,

    detalle_curso,

    enviar_evaluacion,

    lista_cursos,

    resultado_evaluacion,

    ver_evaluacion,

    ver_leccion,

)

from core.views_ejercicios import detalle_ejercicio, practicar_ejercicio

from core import views_parafrasis
from core import views_parafrasis_reordenamiento
from core import views_parafrasis_registro


# Rutas sin prefijo de idioma (admin + i18n + TTS)

urlpatterns = [

    path('i18n/', include('django.conf.urls.i18n')),

    path('admin/', admin.site.urls),

    path('tts/', views_tts.servir_audio, name='tts_servir'),

]



# Rutas con prefijo de idioma (/, /en/, /ja/, /ar/, ...)

urlpatterns += i18n_patterns(

    path('recursos/', include('core.urls_recursos')),

    path('estudiante/', include('core.urls_estudiante')),

    path('verificar/<str:codigo>/', verificar_certificado_publico, name='verificar_certificado_publico'),

    path('profesor/', include('core.urls_profesor')),

    path('', index, name='index'),

    path('login/', login_view, name='login'),

    path('registro/', registro_view, name='registro'),

    path('logout/', logout_view, name='logout'),



    path('perfil/', perfil_usuario, name='perfil_usuario'),

    path('perfil/editar/', editar_perfil, name='editar_perfil'),

    path('perfil/cambiar-contrasena/', cambiar_contrasena, name='cambiar_contrasena'),



    path('dashboard/', dashboard_estudiante, name='dashboard_estudiante'),

    path('dashboard/gamificacion/', dashboard_gamificacion, name='dashboard_gamificacion'),



    path('biblioteca/', ejercicios_biblioteca, name='ejercicios_biblioteca'),

    path('ejercicio/<int:ejercicio_id>/', detalle_ejercicio, name='detalle_ejercicio'),

    path('practicar/<int:ejercicio_id>/', practicar_ejercicio, name='practicar_ejercicio'),

    path('enviar-respuesta/<int:ejercicio_id>/', enviar_respuesta, name='enviar_respuesta'),



    path('cursos/', lista_cursos, name='lista_cursos'),

    path('cursos/<slug:curso_slug>/', detalle_curso, name='detalle_curso'),

    path('cursos/<slug:curso_slug>/modulo/<int:modulo_id>/leccion/<int:leccion_id>/',

         ver_leccion, name='ver_leccion'),



    path('evaluacion/<int:evaluacion_id>/', ver_evaluacion, name='ver_evaluacion'),

    path('evaluacion/<int:evaluacion_id>/enviar/', enviar_evaluacion, name='enviar_evaluacion'),

    path('evaluacion/<int:evaluacion_id>/resultados/', resultado_evaluacion, name='resultado_evaluacion'),

    path('api/evaluacion/<int:evaluacion_id>/preguntas/', api_evaluacion_preguntas, name='api_evaluacion_preguntas'),



    path('tecnicas/', ver_tecnicas, name='ver_tecnicas'),

    path('certificaciones/', certificaciones_lista, name='certificaciones_lista'),



    # Taller de redaccion (Modulo 4)

    path('redaccion/', views_redaccion.indice, name='redaccion_indice'),
    path('redaccion/tecnicas/', views_redaccion.tecnicas_dashboard, name='redaccion_tecnicas'),

    path('redaccion/historial/', views_redaccion.historial, name='redaccion_historial'),

    path('redaccion/<int:ejercicio_id>/', views_redaccion.detalle, name='redaccion_ejercicio'),



    # SRS (Modulo 5)

    path('estudiante/srs/repaso/', views_srs.repaso, name='srs_repaso'),

    path('estudiante/srs/estadisticas/', views_srs.estadisticas, name='srs_estadisticas'),



    # Filologia comparada (Modulo 2)

    path('filologia/', views_filologia.indice, name='filologia_indice'),

    path('filologia/<slug:etimo>/', views_filologia.detalle, name='filologia_detalle'),



    # Corpus (Modulo 6)

    path('corpus/', views_corpus.indice, name='corpus_indice'),

    path('corpus/concordancia/', views_corpus.concordancia, name='corpus_concordancia'),

    path('corpus/frecuencias/', views_corpus.frecuencias_view, name='corpus_frecuencias'),



    # POS con spaCy (Modulo 1)

    path('pos/', views_pos.demo, name='pos_demo'),

    path('pos/corpus/', views_pos.corpus, name='pos_corpus'),

    path('pos/ajax/analizar/', views_pos.analizar_ajax, name='pos_analizar_ajax'),



    # Lectura asistida (Modulo 3)

    path('lectura/', views_lectura.selector, name='lectura_selector'),

    path('lectura/ajax/morfologia/', views_lectura.morfologia_ajax, name='lectura_morfologia_ajax'),

    path('lectura/<int:texto_id>/', views_lectura.lector, name='lectura_lector'),



    prefix_default_language=False,

)



if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



urlpatterns += [

    path("sintaxis/parafrasis/", views_parafrasis.parafrasis_demo, name="parafrasis_demo"),

    path("sintaxis/parafrasis/ajax/", views_parafrasis.parafrasis_ajax, name="parafrasis_ajax"),

]
urlpatterns += [
    path("sintaxis/parafrasis/reordenar/", views_parafrasis_reordenamiento.parafrasis_reordenar_ajax, name="parafrasis_reordenar"),
]
urlpatterns += [
    path("sintaxis/parafrasis/registro/", views_parafrasis_registro.registro_demo, name="registro_demo"),
    path("sintaxis/parafrasis/registro/ajax/", views_parafrasis_registro.registro_ajax, name="registro_ajax"),
]
