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


def verificar(request, review_id):
    """Verifica la respuesta del estudiante al ejercicio (sin afectar SM-2)."""
    from django.apps import apps
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404

    from core.services.parafrasis import similitud_tokens

    if not request.user.is_authenticated:
        return JsonResponse({"error": "No autenticado"}, status=401)

    Review = apps.get_model("core", "Review")
    rv = get_object_or_404(
        Review, id=review_id, flashcard__estudiante=request.user
    )
    fc = rv.flashcard

    respuesta = (request.POST.get("respuesta") or "").strip()
    esperada = (fc.respuesta_ejercicio or "").strip()

    if not esperada:
        return JsonResponse({
            "disponible": False,
            "razon": "Este ejercicio no tiene respuesta esperada.",
        })

    sim = similitud_tokens(respuesta, esperada) if respuesta else 0.0
    aprobado = sim >= 0.5

    return JsonResponse({
        "disponible": True,
        "aprobado": aprobado,
        "similitud": sim,
        "esperada": esperada,
        "tu_respuesta": respuesta,
    })


def estadisticas(request):
    """Dashboard de metricas del estudiante con 4 charts."""
    if not request.user.is_authenticated:
        return redirect(f"/login/?next={request.path}")

    from datetime import timedelta

    from django.apps import apps
    from django.utils import timezone

    Flashcard = apps.get_model("core", "Flashcard")
    Review = apps.get_model("core", "Review")

    stats = estadisticas_estudiante(request.user)

    mis_fc = Flashcard.objects.filter(estudiante=request.user)
    mis_rv = Review.objects.filter(flashcard__estudiante=request.user)

    madurez = {
        "Nueva (0 reps)": 0,
        "Aprendizaje (1-2)": 0,
        "Joven (<7d)": 0,
        "Madura (7-30d)": 0,
        "Dominada (30d+)": 0,
    }
    for rv in mis_rv:
        if rv.repeticiones == 0:
            madurez["Nueva (0 reps)"] += 1
        elif rv.repeticiones <= 2:
            madurez["Aprendizaje (1-2)"] += 1
        elif rv.intervalo_dias < 7:
            madurez["Joven (<7d)"] += 1
        elif rv.intervalo_dias < 30:
            madurez["Madura (7-30d)"] += 1
        else:
            madurez["Dominada (30d+)"] += 1

    facilidad = {"1.3-1.5": 0, "1.5-1.8": 0, "1.8-2.0": 0, "2.0-2.3": 0, "2.3+": 0}
    for rv in mis_rv:
        f = rv.facilidad or 2.5
        if f < 1.5:
            facilidad["1.3-1.5"] += 1
        elif f < 1.8:
            facilidad["1.5-1.8"] += 1
        elif f < 2.0:
            facilidad["1.8-2.0"] += 1
        elif f < 2.3:
            facilidad["2.0-2.3"] += 1
        else:
            facilidad["2.3+"] += 1

    intervalos = {"1d": 0, "2-3d": 0, "4-7d": 0, "8-30d": 0, "30d+": 0}
    for rv in mis_rv:
        i = rv.intervalo_dias or 0
        if i <= 1:
            intervalos["1d"] += 1
        elif i <= 3:
            intervalos["2-3d"] += 1
        elif i <= 7:
            intervalos["4-7d"] += 1
        elif i <= 30:
            intervalos["8-30d"] += 1
        else:
            intervalos["30d+"] += 1

    hoy = timezone.now().date()
    retencion = []
    for w in range(4, 0, -1):
        inicio = hoy - timedelta(days=w * 7)
        fin = inicio + timedelta(days=7)
        total_sem = mis_rv.filter(
            completada_en__date__gte=inicio, completada_en__date__lt=fin
        ).count()
        ok_sem = mis_rv.filter(
            completada_en__date__gte=inicio,
            completada_en__date__lt=fin,
            calidad_respuesta__gte=3,
        ).count()
        retencion.append({
            "label": f"Sem -{w}",
            "total": total_sem,
            "correctas": ok_sem,
        })

    charts = {
        "madurez": {"labels": list(madurez.keys()), "data": list(madurez.values())},
        "facilidad": {"labels": list(facilidad.keys()), "data": list(facilidad.values())},
        "intervalos": {"labels": list(intervalos.keys()), "data": list(intervalos.values())},
        "retencion": {
            "labels": [r["label"] for r in retencion],
            "total": [r["total"] for r in retencion],
            "correctas": [r["correctas"] for r in retencion],
        },
    }

    proxima_rv = (
        mis_rv.filter(completada_en__isnull=True)
        .order_by("programada_para")
        .first()
    )
    proxima_revision = proxima_rv.programada_para if proxima_rv else None

    context = {
        "stats": stats,
        "charts": charts,
        "flashcards": mis_fc.order_by("-creado_en")[:100],
        "total_flashcards": mis_fc.count(),
        "total_reviews": mis_rv.count(),
        "proxima_revision": proxima_revision,
    }
    return render(request, "estudiante/srs/estadisticas.html", context)