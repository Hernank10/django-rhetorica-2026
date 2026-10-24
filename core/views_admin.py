"""Vista del panel de administración (dashboard del superuser)."""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from core.services.notificaciones import contar_no_leidas, ultimas_notificaciones
from core.services.tareas import tareas_admin


@staff_member_required
def panel(request):
    """Dashboard del admin con cards de notificaciones y tareas globales."""
    return render(request, "core/admin_panel.html", {
        "notif_recientes": list(ultimas_notificaciones(request.user, n=5)),
        "notif_count": contar_no_leidas(request.user),
        "tareas_admin": tareas_admin(),
    })