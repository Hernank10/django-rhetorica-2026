"""URLs de lectura."""
from django.urls import path
from . import views_lectura as v

app_name = "lectura"

urlpatterns = [
    path("", v.indice_lectura, name="indice"),
    path("evaluar/", v.evaluar_ejercicio_lectura, name="evaluar"),
    path("progreso/", v.mi_progreso_lectura, name="progreso"),
    path("<int:texto_id>/", v.texto_detalle, name="texto_detalle"),
    path('flashcards/', v.flashcards_lectura, name='flashcards_lectura'),
    path('flashcards/verificar/', v.flashcards_verificar, name='flashcards_verificar'),
    path("guia-certificados/", v.guia_certificados, name="guia_certificados"),
]
