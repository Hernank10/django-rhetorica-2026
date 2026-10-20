"""Vistas para el modulo de parafrasis (S5.2)."""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.services.parafrasis import (
    es_pasiva,
    transformar_a_activa,
    transformar_a_pasiva,
    verificar_parafrasis,
)

TIPOS_VALIDOS = {"activa_a_pasiva", "pasiva_a_activa"}


@require_http_methods(["GET", "POST"])
def parafrasis_demo(request):
    """GET/POST renderiza template con form + JS."""
    return render(request, "core/parafrasis/demo.html")


@require_http_methods(["POST"])
def parafrasis_ajax(request):
    """Endpoint AJAX: valida, delega al servicio, retorna JSON."""
    original = (request.POST.get("original") or "").strip()
    parafraseado = (request.POST.get("parafraseado") or "").strip()
    tipo = (request.POST.get("tipo") or "").strip()

    if not original or not parafraseado:
        return JsonResponse({"error": "Faltan textos"}, status=400)
    if tipo not in TIPOS_VALIDOS:
        return JsonResponse({"error": "Tipo invalido"}, status=400)

    resultado = verificar_parafrasis(original, parafraseado, tipo)
    sugerencia = (
        transformar_a_pasiva(original)
        if tipo == "activa_a_pasiva"
        else transformar_a_activa(original)
    )
    resultado["sugerencia"] = sugerencia
    resultado["es_pasiva_original"] = es_pasiva(original)
    return JsonResponse(resultado)