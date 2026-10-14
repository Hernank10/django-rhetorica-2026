from django.urls import path

from . import views_recursos as r

app_name = "recursos"

urlpatterns = [
    path("", r.lista_recursos, name="lista"),
    path("<slug:slug>/", r.visor_recurso, name="ver"),
    path("<slug:slug>/raw/", r.servir_recurso_raw, name="raw"),
    path("<slug:slug>/vincular/", r.vincular_recurso, name="vincular"),
    path("<slug:slug>/desvincular/<str:tipo>/", r.desvincular_recurso, name="desvincular"),
    path("objeto/<str:tipo>/<int:obj_id>/", r.recursos_para_objeto, name="para_objeto"),
    path("objeto/<str:tipo>/<int:obj_id>/asignar/", r.asignar_recursos, name="asignar"),
    path("objeto/<str:tipo>/<int:obj_id>/quitar/<int:recurso_id>/", r.quitar_recurso, name="quitar"),
]
