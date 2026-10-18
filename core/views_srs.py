"""Vistas del sistema de repeticion espaciada (SRS)."""
from django.shortcuts import redirect, render

from core.services.srs_db import (
    aplicar_sm2_y_guardar,
    estadisticas_estudiante,
    reviews_para_hoy,
)


def repaso(request):
    """Sesion de repaso: muestra la proxima flashcard pendiente.

    GET  -> renderiza la primera pendiente o "todo al dia"
    POST -> aplica SM-2 con la calidad enviada y redirige
    """
    if not request.user.is_authenticated:
        return redirect(f"/login/?next={request.path}")

    pendientes = reviews_para_hoy(request.user)
    siguiente = pendientes.first()

    if request.method == "POST":
        if siguiente is not None:
            try:
                calidad = int(request.POST.get("calidad", 3))
            except (TypeError, ValueError):
                calidad = 3
            calidad = max(0, min(5, calidad))
            aplicar_sm2_y_guardar(siguiente, calidad)
        return redirect("srs_repaso")

    return render(
        request,
        "estudiante/srs/repaso.html",
        {"review": siguiente, "pendientes_count": pendientes.count()},
    )


def estadisticas(request):
    """Dashboard de metricas del estudiante."""
    if not request.user.is_authenticated:
        return redirect(f"/login/?next={request.path}")

    stats = estadisticas_estudiante(request.user)
    return render(request, "estudiante/srs/estadisticas.html", {"stats": stats})