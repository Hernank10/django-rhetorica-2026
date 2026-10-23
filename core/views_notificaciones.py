"""Vistas y endpoints AJAX del sistema de notificaciones."""
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from core.services.notificaciones import (
    contar_no_leidas,
    marcar_todas_leidas,
    ultimas_notificaciones,
)


@login_required
def lista(request):
    """Lista paginada de notificaciones del usuario."""
    Notificacion = apps.get_model("core", "Notificacion")

    qs = Notificacion.objects.filter(user=request.user).order_by("-creada_en")

    # Filtros
    filtro = (request.GET.get("filtro") or "").strip()
    if filtro == "no_leidas":
        qs = qs.filter(leida=False)
    elif filtro in ("leccion_completada", "curso_completado", "certificacion", "logro", "sistema"):
        qs = qs.filter(tipo=filtro)

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    context = {
        "page_obj": page_obj,
        "notificaciones": page_obj.object_list,
        "filtro": filtro,
        "total_no_leidas": contar_no_leidas(request.user),
        "total": paginator.count,
    }
    return render(request, "core/notificaciones/lista.html", context)


@login_required
def ajax_contador(request):
    """Retorna count de no leidas (para el badge de la campana)."""
    return JsonResponse({"count": contar_no_leidas(request.user)})


@login_required
def ajax_ultimas(request):
    """Retorna las ultimas N notificaciones (para el dropdown)."""
    notifs = ultimas_notificaciones(request.user, n=8)
    data = [
        {
            "id": n.id,
            "tipo": n.tipo,
            "titulo": n.titulo,
            "mensaje": n.mensaje,
            "url_destino": n.url_destino,
            "icono": n.icono,
            "leida": n.leida,
            "creada_en": n.creada_en.isoformat(),
        }
        for n in notifs
    ]
    return JsonResponse({
        "count": contar_no_leidas(request.user),
        "notificaciones": data,
    })


@login_required
@require_POST
def ajax_marcar_todas(request):
    """Marca todas como leidas. Retorna count."""
    n = marcar_todas_leidas(request.user)
    return JsonResponse({"ok": True, "marcadas": n})


@login_required
@require_POST
def ajax_marcar_id(request, notif_id):
    """Marca una notificacion como leida."""
    Notificacion = apps.get_model("core", "Notificacion")
    n = get_object_or_404(Notificacion, id=notif_id, user=request.user)
    n.leida = True
    n.save(update_fields=["leida"])
    return JsonResponse({"ok": True, "count": contar_no_leidas(request.user)})