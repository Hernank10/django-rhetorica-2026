"""Vistas del modulo de lectura asistida con TTS + morfologia."""
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from core.models import EjercicioLinguistico
from core.services.lectura import (
    estadisticas_texto,
    morfologia_contextual,
    segmentar_texto,
)


def _textos_disponibles():
    """Ejercicios con contenido.ejemplo de longitud suficiente."""
    qs = EjercicioLinguistico.objects.filter(es_redaccion=True)
    textos = []
    for ej in qs:
        ejemplo = (ej.contenido or {}).get("ejemplo", "").strip()
        if len(ejemplo) >= 80:  # textos cortos no valen la pena
            textos.append({
                "id": ej.id,
                "titulo": ej.titulo,
                "tipo": ej.tipo_redaccion or "",
                "texto": ejemplo,
                "longitud": len(ejemplo),
            })
    return textos


def selector(request):
    """Listado de textos disponibles para lectura asistida."""
    textos = _textos_disponibles()
    tipos = sorted({t["tipo"] for t in textos if t["tipo"]})
    return render(
        request,
        "core/lectura/selector.html",
        {
            "textos": textos,
            "total": len(textos),
            "tipos": tipos,
        },
    )


def lector(request, texto_id):
    """Lectura asistida de un texto especifico."""
    ej = get_object_or_404(EjercicioLinguistico, pk=texto_id, es_redaccion=True)
    texto = (ej.contenido or {}).get("ejemplo", "").strip()
    if not texto:
        texto = (ej.contenido or {}).get("enunciado", "").strip()

    segmentos = segmentar_texto(texto)
    stats = estadisticas_texto(texto)

    return render(
        request,
        "core/lectura/lector.html",
        {
            "ejercicio": ej,
            "texto": texto,
            "segmentos": segmentos,
            "stats": stats,
        },
    )


@require_POST
def morfologia_ajax(request):
    """POST /lectura/ajax/morfologia/ con JSON {texto, offset}.

    Retorna JSON con la morfologia de la palabra en `offset`.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON invalido"}, status=400)

    texto = (data.get("texto") or "").strip()
    offset = data.get("offset")

    if not texto:
        return JsonResponse({"error": "falta texto"}, status=400)
    if offset is None:
        return JsonResponse({"error": "falta offset"}, status=400)
    try:
        offset = int(offset)
    except (TypeError, ValueError):
        return JsonResponse({"error": "offset no numerico"}, status=400)

    if offset < 0 or offset >= len(texto):
        return JsonResponse({"error": "offset fuera de rango"}, status=400)

    return JsonResponse(morfologia_contextual(texto, offset))