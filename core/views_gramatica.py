"""Vistas del modulo 11: gramatica castellana."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
import json

from core.models_gramatica import TecnicaGramatical, EjercicioGramatical, ProgresoGramatical
from core.services import gramatica as engine


BLOQUES_INFO = {
    "A": "Historia de la gramática castellana",
    "B": "Clases de palabras",
    "C": "El sustantivo",
    "D": "El adjetivo",
    "E": "El verbo",
    "F": "Pronombres y determinantes",
    "G": "Reglas ortográficas (RAE 2010)",
}


@login_required
def indice(request):
    tecnicas = TecnicaGramatical.objects.filter(modulo="gramatica")
    progresos = {p.tecnica_id: p for p in ProgresoGramatical.objects.filter(usuario=request.user)}
    bloques = {}
    for letra, nombre in BLOQUES_INFO.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({"tecnica": t, "estado": p.estado if p else "no_iniciada", "intentos": p.intentos if p else 0})
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {"nombre": nombre, "items": items, "dominadas": dominadas, "total": len(items)}
    resumen = engine.resumen_progreso(request.user, modulo="gramatica")
    return render(request, "core/gramatica/indice.html", {"bloques": bloques, "resumen": resumen})




@login_required
def indice_generativa(request):
    """Indice de las 100 tecnicas de gramatica generativa."""
    tecnicas = TecnicaGramatical.objects.filter(modulo="generativa")
    progresos = {p.tecnica_id: p for p in ProgresoGramatical.objects.filter(usuario=request.user)}
    bloques = {}
    for letra, nombre in BLOQUES_INFO.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({"tecnica": t, "estado": p.estado if p else "no_iniciada", "intentos": p.intentos if p else 0})
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {"nombre": nombre, "items": items, "dominadas": dominadas, "total": len(items)}
    resumen = engine.resumen_progreso(request.user, modulo="generativa")
    return render(request, "core/gramatica/indice.html", {"bloques": bloques, "resumen": resumen, "es_generativa": True})


@login_required
def tecnica(request, numero):
    t = get_object_or_404(TecnicaGramatical, numero=numero)
    ejercicios = t.ejercicios.all()
    progreso, _ = ProgresoGramatical.objects.get_or_create(usuario=request.user, tecnica=t)
    anterior = TecnicaGramatical.objects.filter(numero__lt=numero).order_by("-numero").first()
    siguiente = TecnicaGramatical.objects.filter(numero__gt=numero).order_by("numero").first()
    return render(request, "core/gramatica/tecnica.html", {
        "tecnica": t, "ejercicios": ejercicios, "progreso": progreso,
        "anterior": anterior, "siguiente": siguiente,
        "bloque_nombre": BLOQUES_INFO.get(t.bloque, ""),
        "es_generativa": t.modulo == "generativa",
    })


@login_required
@require_POST
def evaluar_ajax(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "JSON invalido"}, status=400)
    ejercicio_id = data.get("ejercicio_id")
    respuesta = data.get("respuesta", {})
    if not ejercicio_id:
        return JsonResponse({"ok": False, "error": "Falta ejercicio_id"}, status=400)
    ej = get_object_or_404(EjercicioGramatical, pk=ejercicio_id)
    resultado = engine.evaluar_ejercicio(ej, respuesta, request.user)
    progreso = engine.actualizar_progreso(request.user, ej.tecnica, ej, resultado["ok"])
    return JsonResponse({
        "ok": resultado["ok"], "feedback": resultado["feedback"],
        "regla": resultado["regla"], "ejemplo_correcto": resultado["ejemplo_correcto"],
        "estado": progreso.estado, "aciertos_consecutivos": progreso.aciertos_consecutivos,
    })


@login_required
def progreso(request, modulo="gramatica"):
    resumen = engine.resumen_progreso(request.user, modulo=modulo)
    proximas = list(engine.proximas_revisiones(request.user, n=10, modulo=modulo))
    dominadas = ProgresoGramatical.objects.filter(
        usuario=request.user, estado="dominada", tecnica__modulo=modulo
    ).select_related("tecnica").order_by("tecnica__numero")
    en_progreso = ProgresoGramatical.objects.filter(
        usuario=request.user, estado="en_progreso", tecnica__modulo=modulo
    ).select_related("tecnica").order_by("tecnica__numero")
    return render(request, "core/gramatica/progreso.html", {
        "resumen": resumen, "proximas": proximas,
        "dominadas": dominadas, "en_progreso": en_progreso,
        "modulo": modulo,
    })


@login_required
def contador_ajax(request):
    modulo = request.GET.get("modulo") or None
    r = engine.resumen_progreso(request.user, modulo=modulo)
    return JsonResponse({"dominadas": r["dominadas"], "total": r["total"]})