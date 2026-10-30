"""Vistas del modulo 11: gramatica castellana."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
import json

from core.models_gramatica import TecnicaGramatical, EjercicioGramatical, ProgresoGramatical
from core.services import gramatica as engine
from django.db import IntegrityError, transaction


BLOQUES_INFO = {
    "A": "Historia de la gramática castellana",
    "B": "Clases de palabras",
    "C": "El sustantivo",
    "D": "El adjetivo",
    "E": "El verbo",
    "F": "Pronombres y determinantes",
    "G": "Reglas ortográficas (RAE 2010)",
}

BLOQUES_GENERATIVA = {
    "A": "Fundamentos de la GGT",
    "B": "Estructura X-barra",
    "C": "Transformaciones",
    "D": "Caso y papeles temáticos",
    "E": "Rección y ligamiento",
    "F": "Programa minimalista",
    "G": "Aplicaciones al castellano",
}

BLOQUES_A1 = {
    "A": "Alfabeto, fonética y saludos",
    "B": "Artículos, género y número",
    "C": "Presente, ser/estar/tener",
    "D": "Vocabulario básico",
    "E": "Preguntas, negación, adverbios",
    "F": "Preposiciones y ubicación",
    "G": "Frases útiles y situaciones",
}


BLOQUES_A2 = {
    "A": "Pretérito indefinido regular",
    "B": "Pretérito indefinido irregular",
    "C": "Pretérito imperfecto",
    "D": "Contraste indefinido vs imperfecto",
    "E": "Pretérito perfecto",
    "F": "Futuro",
    "G": "Condicional simple",
    "H": "Imperativo",
    "I": "Pronombres personales",
    "J": "Comparativos y situaciones",
}




BLOQUES_B1 = {
    "A": "Consolidación y pasado",
    "B": "Futuro, condicional y subjuntivo",
    "C": "Subjuntivo ampliado y estilo indirecto",
    "D": "Oraciones compuestas y conectores",
    "E": "Verbos, preposiciones y construcciones",
    "F": "Vocabulario temático B1",
    "G": "Situaciones comunicativas B1",
    "H": "Subjuntivo imperfecto y condicionales 2/3",
}

BLOQUES_B2 = {
    "A": "Subjuntivo imperfecto avanzado",
    "B": "Condicionales 2/3 y mixtos",
    "C": "Secuencia de tiempos con subjuntivo",
    "D": "Voz pasiva",
    "E": "Estilo indirecto avanzado",
    "F": "Perífrasis verbales",
    "G": "Subordinadas complejas",
    "H": "Conectores avanzados",
    "I": "Verbos de cambio",
    "J": "Situaciones B2",
}

BLOQUES_C1 = {
    "A": "Discurso académico",
    "B": "Registro literario",
    "C": "Cohesión y coherencia avanzadas",
    "D": "Expresiones idiomáticas",
    "E": "Matices aspectuales y modales",
    "F": "Léxico especializado",
    "G": "Sintaxis compleja",
    "H": "Discurso oral formal",
    "I": "Análisis crítico del discurso",
    "J": "Síntesis y creación de textos",
}

BLOQUES_C2 = {
    "A": "Registro literario avanzado",
    "B": "Ironía fina y humor",
    "C": "Intertextualidad y metaficción",
    # D-J se añadirán en fases 3-6
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
def indice_a1(request):
    """Indice de las 100 tecnicas de Lengua Castellana A1."""
    tecnicas = TecnicaGramatical.objects.filter(modulo="a1")
    progresos = {p.tecnica_id: p for p in ProgresoGramatical.objects.filter(usuario=request.user)}
    bloques = {}
    for letra, nombre in BLOQUES_A1.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({"tecnica": t, "estado": p.estado if p else "no_iniciada", "intentos": p.intentos if p else 0})
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {"nombre": nombre, "items": items, "dominadas": dominadas, "total": len(items)}
    resumen = engine.resumen_progreso(request.user, modulo="a1")
    return render(request, "core/gramatica/indice.html", {"bloques": bloques, "resumen": resumen, "es_a1": True, "es_generativa": False})


@login_required
def indice_a2(request):
    """Indice de las 100 tecnicas de Lengua Castellana A2."""
    tecnicas = TecnicaGramatical.objects.filter(modulo="a2")
    progresos = {p.tecnica_id: p for p in ProgresoGramatical.objects.filter(usuario=request.user)}
    bloques = {}
    for letra, nombre in BLOQUES_A2.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({"tecnica": t, "estado": p.estado if p else "no_iniciada", "intentos": p.intentos if p else 0})
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {"nombre": nombre, "items": items, "dominadas": dominadas, "total": len(items)}
    resumen = engine.resumen_progreso(request.user, modulo="a2")
    return render(request, "core/gramatica/indice.html", {"bloques": bloques, "resumen": resumen, "es_a2": True})


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
def indice_b1(request):
    """Indice de las 100 tecnicas de Lengua Castellana B1."""
    tecnicas = TecnicaGramatical.objects.filter(modulo="b1")
    progresos = {p.tecnica_id: p for p in ProgresoGramatical.objects.filter(usuario=request.user)}
    bloques = {}
    for letra, nombre in BLOQUES_B1.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({"tecnica": t, "estado": p.estado if p else "no_iniciada", "intentos": p.intentos if p else 0})
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {"nombre": nombre, "items": items, "dominadas": dominadas, "total": len(items)}
    resumen = engine.resumen_progreso(request.user, modulo="b1")
    return render(request, "core/gramatica/indice.html", {"bloques": bloques, "resumen": resumen, "es_b1": True})


@login_required
def indice_b2(request):
    """Indice de las 100 tecnicas de Lengua Castellana B2."""
    tecnicas = TecnicaGramatical.objects.filter(modulo="b2")
    progresos = {p.tecnica_id: p for p in ProgresoGramatical.objects.filter(usuario=request.user)}
    bloques = {}
    for letra, nombre in BLOQUES_B2.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({"tecnica": t, "estado": p.estado if p else "no_iniciada", "intentos": p.intentos if p else 0})
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {"nombre": nombre, "items": items, "dominadas": dominadas, "total": len(items)}
    resumen = engine.resumen_progreso(request.user, modulo="b2")
    return render(request, "core/gramatica/indice.html", {"bloques": bloques, "resumen": resumen, "es_b2": True})


@login_required
def indice_c1(request):
    """Indice de las 100 tecnicas de Lengua Castellana C1."""
    tecnicas = TecnicaGramatical.objects.filter(modulo="c1")
    progresos = {p.tecnica_id: p for p in ProgresoGramatical.objects.filter(usuario=request.user)}
    bloques = {}
    for letra, nombre in BLOQUES_C1.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({"tecnica": t, "estado": p.estado if p else "no_iniciada", "intentos": p.intentos if p else 0})
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {"nombre": nombre, "items": items, "dominadas": dominadas, "total": len(items)}
    resumen = engine.resumen_progreso(request.user, modulo="c1")
    return render(request, "core/gramatica/indice.html", {"bloques": bloques, "resumen": resumen, "es_c1": True})


@login_required
def indice_c2(request):
    """Indice de las 100 tecnicas de Lengua Castellana C2."""
    tecnicas = TecnicaGramatical.objects.filter(modulo="c2")
    progresos = {p.tecnica_id: p for p in ProgresoGramatical.objects.filter(usuario=request.user)}
    bloques = {}
    for letra, nombre in BLOQUES_C2.items():
        items = []
        for t in tecnicas:
            if t.bloque != letra:
                continue
            p = progresos.get(t.id)
            items.append({"tecnica": t, "estado": p.estado if p else "no_iniciada", "intentos": p.intentos if p else 0})
        if items:
            dominadas = sum(1 for i in items if i["estado"] == "dominada")
            bloques[letra] = {"nombre": nombre, "items": items, "dominadas": dominadas, "total": len(items)}
    resumen = engine.resumen_progreso(request.user, modulo="c2")
    return render(request, "core/gramatica/indice.html", {"bloques": bloques, "resumen": resumen, "es_c2": True})


@login_required
def tecnica(request, numero):
    t = get_object_or_404(TecnicaGramatical, numero=numero)
    ejercicios = t.ejercicios.all()
    progreso = None
    try:
        with transaction.atomic():
            progreso, _ = ProgresoGramatical.objects.get_or_create(
                usuario=request.user, tecnica=t
            )
    except IntegrityError:
        # FK huérfana (progreso de fixture apunta a técnica borrada)
        try:
            ProgresoGramatical.objects.filter(usuario=request.user).exclude(
                tecnica__in=TecnicaGramatical.objects.all()
            ).delete()
            with transaction.atomic():
                progreso, _ = ProgresoGramatical.objects.get_or_create(
                    usuario=request.user, tecnica=t
                )
        except IntegrityError:
            # fallback final: no rompemos la vista
            progreso = ProgresoGramatical(usuario=request.user, tecnica=t, estado="no_iniciada")
    anterior = TecnicaGramatical.objects.filter(
        numero__lt=numero, modulo=t.modulo
    ).order_by("-numero").first()
    siguiente = TecnicaGramatical.objects.filter(
        numero__gt=numero, modulo=t.modulo
    ).order_by("numero").first()
    if t.modulo == "generativa":
        bname = BLOQUES_GENERATIVA.get(t.bloque, "")
    elif t.modulo == "a1":
        bname = BLOQUES_A1.get(t.bloque, "")
    elif t.modulo == "b1":
        bname = BLOQUES_B1.get(t.bloque, "")
    elif t.modulo == "b2":
        bname = BLOQUES_B2.get(t.bloque, "")
    elif t.modulo == "c1":
        bname = BLOQUES_C1.get(t.bloque, "")
    elif t.modulo == "c2":
        bname = BLOQUES_C2.get(t.bloque, "")
    else:
        bname = BLOQUES_INFO.get(t.bloque, "")

    return render(request, "core/gramatica/tecnica.html", {
        "tecnica": t, "ejercicios": ejercicios, "progreso": progreso,
        "anterior": anterior, "siguiente": siguiente,
        "bloque_nombre": bname,
        "es_generativa": t.modulo == "generativa",
        "es_a1": t.modulo == "a1",
        "es_b1": t.modulo == "b1",
        "es_b2": t.modulo == "b2",
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