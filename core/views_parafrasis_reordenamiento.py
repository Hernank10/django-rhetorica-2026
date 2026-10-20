"""Vistas para el modulo de reordenamiento sintactico (S5.4.2)."""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from core.services.parafrasis_reordenamiento import (
    detectar_constituyentes,
    reordenar_fronting,
    reordenar_svo_canonico,
)


@require_http_methods(["POST"])
def parafrasis_reordenar_ajax(request):
    """Endpoint AJAX: devuelve 3 sugerencias + constituyentes detectados."""
    original = (request.POST.get("original") or "").strip()
    if not original:
        return JsonResponse({"error": "Falta original"}, status=400)

    sugerencias = [
        reordenar_fronting(original, "obl"),
        reordenar_fronting(original, "advmod"),
        reordenar_svo_canonico(original),
    ]
    constituyentes = detectar_constituyentes(original)
    return JsonResponse({
        "sugerencias": sugerencias,
        "constituyentes": constituyentes,
    })