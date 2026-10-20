"""Vistas para parafrasis de registro (S5.5.2)."""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.services.parafrasis_registro import (
    detectar_registro,
    transformar_registro,
    verificar_registro,
)

TIPOS_VALIDOS = {"formal_a_coloquial", "coloquial_a_formal"}


@require_http_methods(["GET", "POST"])
def registro_demo(request):
    """GET/POST renderiza template con form + JS."""
    return render(request, "core/parafrasis/registro.html")


@require_http_methods(["POST"])
def registro_ajax(request):
    """Endpoint AJAX: detecta + transforma + verifica en un solo POST."""
    original = (request.POST.get("original") or "").strip()
    parafraseado = (request.POST.get("parafraseado") or "").strip()
    tipo = (request.POST.get("tipo") or "").strip()

    if not original:
        return JsonResponse({"error": "Falta original"}, status=400)
    if tipo not in TIPOS_VALIDOS:
        return JsonResponse({"error": "Tipo invalido"}, status=400)

    det = detectar_registro(original)
    hacia = "coloquial" if tipo == "formal_a_coloquial" else "formal"
    trans = transformar_registro(original, hacia)
    payload = {
        "deteccion_original": det,
        "transformacion_sugerida": trans,
    }
    if parafraseado:
        payload["verificacion"] = verificar_registro(original, parafraseado, tipo)
    return JsonResponse(payload)