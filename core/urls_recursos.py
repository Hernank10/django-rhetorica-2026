from django.urls import path
from . import views_recursos as r

app_name = "recursos"

urlpatterns = [
    path("", r.lista_recursos, name="lista"),
    path("<slug:slug>/", r.visor_recurso, name="ver"),
    path("<slug:slug>/raw/", r.servir_recurso_raw, name="raw"),
]
