"""
Vistas para 'Lectura asistida':
  - GET /lectura/asistida/             -> lista de textos disponibles
  - GET /lectura/asistida/<texto_id>/  -> texto con tokens + audio
  - POST /lectura/asistida/morfologia/ -> devuelve morfologia de una palabra

Reutiliza:
  - core.services.lectura.segmentar_texto
  - core.services.lectura.morfologia_contextual
  - core.services.lectura.estadisticas_texto
  - core.views_tts.servir_audio (GET /tts/?text=...&lang=es)
"""
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from core.models_lectura import Texto

# Import defensivo del servicio
try:
    from core.services.lectura import (
        segmentar_texto,
        morfologia_contextual,
        estadisticas_texto,
    )
    SERVICIO_OK = True
except Exception as e:
    SERVICIO_OK = False
    SERVICIO_ERROR = str(e)


def _normalizar_tokens(tokens):
    """Normaliza las claves de los tokens por si el servicio cambia."""
    out = []
    for t in tokens or []:
        if not isinstance(t, dict):
            continue
        out.append({
            "texto":  t.get("texto") or t.get("text") or t.get("token") or "",
            "inicio": t.get("inicio") or t.get("start") or t.get("offset") or 0,
            "fin":    t.get("fin") or t.get("end") or 0,
            "pos":    t.get("pos") or t.get("tipo") or t.get("etiqueta") or "",
            "lema":   t.get("lema") or t.get("lemma") or "",
        })
    return out


@login_required
def lectura_asistida(request, texto_id=None):
    """
    GET /lectura/asistida/             -> lista de textos
    GET /lectura/asistida/<texto_id>/  -> detalle con tokens
    """
    textos = Texto.objects.all().order_by("nivel_mcer", "orden")

    if texto_id is None:
        # Modo lista
        return render(request, "core/lectura/asistida.html", {
            "modo": "lista",
            "textos": textos,
            "servicio_ok": SERVICIO_OK,
        })

    # Modo detalle
    texto = get_object_or_404(Texto, id=texto_id)

    tokens = []
    stats = {}
    error = None

    if SERVICIO_OK:
        try:
            raw_tokens = segmentar_texto(texto.cuerpo or "")
            tokens = _normalizar_tokens(raw_tokens)
        except Exception as e:
            error = f"Error segmentando: {e}"

        try:
            stats = estadisticas_texto(texto.cuerpo or "") or {}
        except Exception as e:
            stats = {"error": str(e)}
    else:
        error = f"Servicio no disponible: {SERVICIO_ERROR}"

    return render(request, "core/lectura/asistida.html", {
        "modo": "detalle",
        "texto": texto,
        "tokens": tokens,
        "tokens_json": json.dumps(tokens, ensure_ascii=False),
        "stats": stats,
        "error": error,
        "textos": textos,
    })


@login_required
@require_POST
def morfologia_palabra(request):
    """
    POST /lectura/asistida/morfologia/
    Body: texto_id, offset
    Devuelve JSON con la morfologia de la palabra en esa posicion.
    """
    if not SERVICIO_OK:
        return JsonResponse(
            {"ok": False, "error": "Servicio no disponible"},
            status=503,
        )

    texto_id = request.POST.get("texto_id")
    offset = request.POST.get("offset")

    if not texto_id or offset is None:
        return JsonResponse(
            {"ok": False, "error": "Faltan texto_id u offset"},
            status=400,
        )

    try:
        offset = int(offset)
    except (TypeError, ValueError):
        return JsonResponse(
            {"ok": False, "error": "offset invalido"},
            status=400,
        )

    texto = get_object_or_404(Texto, id=texto_id)

    try:
        info = morfologia_contextual(texto.cuerpo or "", offset)
        return JsonResponse({"ok": True, "info": info or {}})
    except Exception as e:
        return JsonResponse(
            {"ok": False, "error": str(e)},
            status=500,
        )