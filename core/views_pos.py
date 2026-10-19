"""Vistas del analizador morfosintactico con spaCy."""
from django.shortcuts import render

from core.services.corpus import corpus_completo
from core.services.pos import (
    analizar_frase,
    estadisticas_pos,
    modelo_disponible,
)


def demo(request):
    """Demo: analiza una frase libre del usuario."""
    texto = ""
    resultado = None

    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        if texto:
            resultado = analizar_frase(texto)
        else:
            resultado = {
                "disponible": True,
                "tokens": [],
                "oraciones": 0,
                "error": "escribe_algo",
            }

    return render(
        request,
        "core/pos/demo.html",
        {
            "texto": texto,
            "resultado": resultado,
            "stats": estadisticas_pos(resultado["tokens"]) if resultado else {},
            "modelo_ok": modelo_disponible(),
        },
    )


def corpus(request):
    """Analiza los primeros N items del corpus y muestra agregados."""
    if not modelo_disponible():
        return render(
            request,
            "core/pos/corpus.html",
            {
                "disponible": False,
                "items_analizados": 0,
                "total_tokens": 0,
                "stats": {},
                "ejemplos_verbos": [],
                "ejemplos_sustantivos": [],
            },
        )

    items = corpus_completo()[:20]
    todos_tokens = []
    ejemplos_verbos = []
    ejemplos_sustantivos = []
    oraciones_total = 0

    for it in items:
        r = analizar_frase(it["texto"], incluir_dependencias=False)
        if not r.get("disponible"):
            continue
        oraciones_total += r["oraciones"]
        for t in r["tokens"]:
            todos_tokens.append(t)
            if t["pos"] == "VERB" and len(ejemplos_verbos) < 10:
                ejemplos_verbos.append(t["lemma"] or t["texto"])
            elif t["pos"] == "NOUN" and len(ejemplos_sustantivos) < 10:
                ejemplos_sustantivos.append(t["lemma"] or t["texto"])

    return render(
        request,
        "core/pos/corpus.html",
        {
            "disponible": True,
            "items_analizados": len(items),
            "total_tokens": len(todos_tokens),
            "oraciones": oraciones_total,
            "stats": estadisticas_pos(todos_tokens),
            "ejemplos_verbos": ejemplos_verbos,
            "ejemplos_sustantivos": ejemplos_sustantivos,
        },
    )