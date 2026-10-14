# -*- coding: utf-8 -*-
"""URLs del panel del estudiante."""
from django.urls import path

from . import views_estudiante as est

app_name = "estudiante"

urlpatterns = [
    path('', est.dashboard, name='dashboard'),
    path('cursos/', est.mis_cursos, name='cursos'),
    path('evaluaciones/', est.mis_evaluaciones, name='evaluaciones'),
    path('logros/', est.mis_logros, name='logros'),
    path('certificados/', est.mis_certificados, name='certificados'),
    path('estadisticas/', est.mis_estadisticas, name='estadisticas'),
    path('ranking/', est.mi_ranking, name='ranking'),
    path('certificados/<int:certificado_id>/pdf/', est.descargar_certificado_pdf, name='certificado_pdf'),
    path('certificados/<int:certificado_id>/docx/', est.descargar_certificado_docx, name='certificado_docx'),
]
