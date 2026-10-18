"""Vistas del explorador de filologia comparada."""
from django.http import Http404
from django.shortcuts import render

from core.services.filologia import (
    buscar_etimo,
    cadena_evolutiva,
    categorias_disponibles,
)


def indice(request):
    """Explorador: listado + buscador opcional via ?q=<termino>."""
    q = request.GET.get("q", "").strip()

    if q:
        etimos = buscar_etimo(q)
    else:
        from core.services._etimos_filologia import ETIMOS
        etimos = list(ETIMOS)

    return render(
        request,
        "core/filologia/indice.html",
        {
            "etimos": etimos,
            "q": q,
            "total": len(etimos),
            "categorias": categorias_disponibles(),
        },
    )


def detalle(request, etimo):
    """Ficha completa de un etimo por su forma latina."""
    data = cadena_evolutiva(etimo)
    if data is None:
        raise Http404(f"Etimo no encontrado: {etimo}")
    return render(
        request,
        "core/filologia/detalle.html",
        {"etimo": data},
    )