"""URLs del modulo 11: gramatica."""
from django.urls import path
from core import views_gramatica as v

app_name = "gramatica"

urlpatterns = [
    path("", v.indice, name="indice"),
    path("generativa/", v.indice_generativa, name="indice_generativa"),
    path("tecnica/<int:numero>/", v.tecnica, name="tecnica"),
    path("evaluar/", v.evaluar_ajax, name="evaluar"),
    path("progreso/", v.progreso, name="progreso"),
    path("ajax/contador/", v.contador_ajax, name="contador"),
]