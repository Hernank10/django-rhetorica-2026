"""Vistas del explorador de corpus."""
from django.shortcuts import render

from core.services.corpus import (
    FUENTES,
    concordancias,
    corpus_completo,
    frecuencias,
    n_gramas,
)


def _stats_corpus(items):
    """Metricas basicas del corpus para mostrar en el indice."""
    por_fuente = {}
    for it in items:
        f = it["fuente"]
        por_fuente[f] = por_fuente.get(f, 0) + 1
    return {
        "total_items": len(items),
        "por_fuente": por_fuente,
        "fuentes_disponibles": sorted({it["fuente"] for it in items}),
    }


def indice(request):
    """Dashboard: stats + top 50 palabras del corpus."""
    items = corpus_completo()
    textos = [it["texto"] for it in items]

    frec = frecuencias(textos)
    top_palabras = sorted(frec.items(), key=lambda x: -x[1])[:50]

    return render(
        request,
        "core/corpus/indice.html",
        {
            "stats": _stats_corpus(items),
            "top_palabras": top_palabras,
        },
    )


def concordancia(request):
    """KWIC: buscar termino y mostrar todas sus apariciones con contexto."""
    q = request.GET.get("q", "").strip()
    fuente = request.GET.get("fuente", "").strip()

    items = corpus_completo()
    if fuente and fuente in FUENTES:
        items = [it for it in items if it["fuente"] == fuente]

    resultados = []
    if q:
        for it in items:
            for kwic in concordancias(it["texto"], q, contexto=5):
                kwic["fuente"] = it["fuente"]
                kwic["item_id"] = it["id"]
                resultados.append(kwic)

    return render(
        request,
        "core/corpus/concordancia.html",
        {
            "q": q,
            "fuente": fuente,
            "fuentes": sorted({it["fuente"] for it in items}),
            "resultados": resultados[:500],
            "total": len(resultados),
        },
    )


def frecuencias_view(request):
    """Tabla de frecuencias + top 20 bigramas."""
    items = corpus_completo()
    textos = [it["texto"] for it in items]

    frec = frecuencias(textos)
    tabla = sorted(frec.items(), key=lambda x: (-x[1], x[0]))[:200]

    bigramas = n_gramas(textos, n=2, top=20)
    trigramas = n_gramas(textos, n=3, top=10)

    return render(
        request,
        "core/corpus/frecuencias.html",
        {
            "tabla": tabla,
            "bigramas": bigramas,
            "trigramas": trigramas,
            "total_palabras_unicas": len(frec),
        },
    )