"""URLs del módulo 10: sintaxis."""
from django.urls import path
from core import views_sintaxis as v

app_name = "sintaxis"

urlpatterns = [
    path("", v.indice, name="indice"),
    path("tecnica/<int:numero>/", v.tecnica, name="tecnica"),
    path("evaluar/", v.evaluar_ajax, name="evaluar"),
    path("progreso/", v.progreso, name="progreso"),
    path("ajax/contador/", v.contador_ajax, name="contador"),
]