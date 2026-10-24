"""Vistas del módulo 10: técnicas de sintaxis con flashcards."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
import json

from core.models_sintaxis import TecnicaSintactica, EjercicioTecnica, ProgresoTecnica
from core.services import sintaxis as engine


BLOQUES_INFO = {
    "A": "Oración simple",
    "B": "Concordancia y régimen",
    "C": "Coordinación",
    "D": "Subordinación sustantiva",
    "E": "Subordinación adjetiva",
    "F": "Subordinación adverbial",
    "G": "Yuxtaposición y puntuación",
}


@login_required
def indice(request):
    """Grid de 100 técnicas con progreso del usuario."""
    tecnicas = TecnicaSintactica.objects.all()
    progresos = {
        p.tecnica_id: p
        for p in ProgresoTecnica.objects.filter(usuario=request.user)
    }

    # Agrupar por bloque
    bloques = {}
    for letra, nombre in BLOQUES_INFO.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({
                "tecnica": t,
                "estado": p.estado if p else "no_iniciada",
                "intentos": p.intentos if p else 0,
            })
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {
                "nombre": nombre,
                "items": items,
                "dominadas": dominadas,
                "total": len(items),
            }

    resumen = engine.resumen_progreso(request.user)

    return render(request, "core/sintaxis/indice.html", {
        "bloques": bloques,
        "resumen": resumen,
    })


@login_required
def tecnica(request, numero):
    """Flashcard de una técnica + primer ejercicio disponible."""
    t = get_object_or_404(TecnicaSintactica, numero=numero)
    ejercicios = t.ejercicios.all()

    # Elegir ejercicio segun progreso: si no dominada, el primero; si dominada, todos
    progreso, _ = ProgresoTecnica.objects.get_or_create(
        usuario=request.user, tecnica=t,
    )

    # Navegacion: anterior y siguiente
    anterior = TecnicaSintactica.objects.filter(numero__lt=numero).order_by("-numero").first()
    siguiente = TecnicaSintactica.objects.filter(numero__gt=numero).order_by("numero").first()

    return render(request, "core/sintaxis/tecnica.html", {
        "tecnica": t,
        "ejercicios": ejercicios,
        "progreso": progreso,
        "anterior": anterior,
        "siguiente": siguiente,
        "bloque_nombre": BLOQUES_INFO.get(t.bloque, ""),
    })


@login_required
@require_POST
def evaluar_ajax(request):
    """POST JSON: {ejercicio_id, respuesta} -> evalua + actualiza progreso."""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "JSON invalido"}, status=400)

    ejercicio_id = data.get("ejercicio_id")
    respuesta = data.get("respuesta", {})

    if not ejercicio_id:
        return JsonResponse({"ok": False, "error": "Falta ejercicio_id"}, status=400)

    ej = get_object_or_404(EjercicioTecnica, pk=ejercicio_id)

    resultado = engine.evaluar_ejercicio(ej, respuesta, request.user)
    progreso = engine.actualizar_progreso(request.user, ej.tecnica, ej, resultado["ok"])

    return JsonResponse({
        "ok": resultado["ok"],
        "feedback": resultado["feedback"],
        "regla": resultado["regla"],
        "ejemplo_correcto": resultado["ejemplo_correcto"],
        "estado": progreso.estado,
        "aciertos_consecutivos": progreso.aciertos_consecutivos,
        "proxima_revision": progreso.proxima_revision.isoformat() if progreso.proxima_revision else None,
    })


@login_required
def progreso(request):
    """Detalle de progreso: heatmap + proximas revisiones + stats."""
    resumen = engine.resumen_progreso(request.user)
    proximas = list(engine.proximas_revisiones(request.user, n=10))

    dominadas = ProgresoTecnica.objects.filter(
        usuario=request.user, estado="dominada",
    ).select_related("tecnica").order_by("tecnica__numero")

    en_progreso = ProgresoTecnica.objects.filter(
        usuario=request.user, estado="en_progreso",
    ).select_related("tecnica").order_by("tecnica__numero")

    return render(request, "core/sintaxis/progreso.html", {
        "resumen": resumen,
        "proximas": proximas,
        "dominadas": dominadas,
        "en_progreso": en_progreso,
    })


@login_required
def contador_ajax(request):
    """Cuenta rápida para badge de navegación."""
    r = engine.resumen_progreso(request.user)
    return JsonResponse({
        "dominadas": r["dominadas"],
        "total": r["total"],
    })