"""URLs de lectura."""
from django.urls import path
from . import views_lectura as v
from . import views_lectura_asistida as va
from . import views_flashcards_sesion as fs

app_name = "lectura"

urlpatterns = [
    path("", v.indice_lectura, name="indice"),
    path("evaluar/", v.evaluar_ejercicio_lectura, name="evaluar"),
    path("progreso/", v.mi_progreso_lectura, name="progreso"),
    path("<int:texto_id>/", v.texto_detalle, name="texto_detalle"),
    path('flashcards/', v.flashcards_lectura, name='flashcards_lectura'),
    path('flashcards/verificar/', v.flashcards_verificar, name='flashcards_verificar'),
    path("guia-certificados/", v.guia_certificados, name="guia_certificados"),
    # Sesion de flashcards (carta flip + 3 botones)
    path("flashcards/sesion/", fs.flashcards_sesion, name="flashcards_sesion"),
    path("flashcards/calificar/", fs.flashcards_calificar, name="flashcards_calificar"),    # Lectura asistida (TTS + morfologia contextual)
    path("asistida/", va.lectura_asistida, name="lectura_asistida"),
    path("asistida/<int:texto_id>/", va.lectura_asistida, name="lectura_asistida_detalle"),
    path("asistida/morfologia/", va.morfologia_palabra, name="lectura_asistida_morfologia"),]
