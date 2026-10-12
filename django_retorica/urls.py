"""
URL Configuration for django_retorica project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from core.views import (
    verificar_certificado_publico,
    index, login_view, registro_view, logout_view,
    dashboard_estudiante, dashboard_gamificacion,
    perfil_usuario, editar_perfil, cambiar_contrasena,
    certificaciones_lista, ver_tecnicas, enviar_respuesta
)

from core.views_ejercicios import detalle_ejercicio, practicar_ejercicio
from core.views_biblioteca import ejercicios_biblioteca

from core.views_cursos_completo import (
    lista_cursos,
    detalle_curso,
    ver_leccion,
    ver_evaluacion,
    enviar_evaluacion,
    resultado_evaluacion,
    api_evaluacion_preguntas
)

# Rutas sin prefijo de idioma (admin + endpoint para cambiar idioma)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

# Rutas con prefijo de idioma (/, /en/, /ja/, /ar/, ...)
urlpatterns += i18n_patterns(
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

    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)