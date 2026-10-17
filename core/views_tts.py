"""Vista para servir MP3s de gTTS con cache en disco."""

from django.http import FileResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET

from .services import tts


@require_GET
def servir_audio(request):
    """GET /tts/?text=...&lang=... → MP3 cacheado o generado on-the-fly."""
    texto = request.GET.get("text", "").strip()
    lang = request.GET.get("lang", "es").lower()[:2]

    if not texto:
        return HttpResponseBadRequest("Falta el parametro 'text'")
    if len(texto) > tts.MAX_TEXTO:
        return HttpResponseBadRequest(
            f"Texto demasiado largo (max {tts.MAX_TEXTO} caracteres)"
        )

    if lang not in {"es", "en", "la"}:
        lang = "es"

    path = tts.generar_mp3(texto, lang)
    if not path or not path.exists():
        return JsonResponse(
            {
                "error": (
                    "No se pudo generar el audio. "
                    "Verifica que gTTS este instalado y que haya conexion."
                )
            },
            status=503,
        )

    response = FileResponse(open(path, "rb"), content_type="audio/mpeg")
    response["Cache-Control"] = "public, max-age=2592000"
    return response