"""URLs del modulo de notificaciones."""
from django.urls import path

from . import views_notificaciones as notif

app_name = "notificaciones"

urlpatterns = [
    path("", notif.lista, name="lista"),
    path("ajax/contador/", notif.ajax_contador, name="ajax_contador"),
    path("ajax/ultimas/", notif.ajax_ultimas, name="ajax_ultimas"),
    path("ajax/marcar-todas/", notif.ajax_marcar_todas, name="ajax_marcar_todas"),
    path("ajax/marcar/<int:notif_id>/", notif.ajax_marcar_id, name="ajax_marcar_id"),
]