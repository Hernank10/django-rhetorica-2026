"""Vistas de lectura (indice, detalle, evaluacion, progreso)."""
import json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.models_lectura import (
    EjercicioLectura, ProgresoTecnicaLectura, ProgresoTexto,
    RespuestaLectura, TecnicaLectura, Texto,
)


@login_required
def indice_lectura(request):
    textos = Texto.objects.all().order_by("nivel_mcer", "orden")
    progreso_map = dict(
        ProgresoTexto.objects.filter(usuario=request.user).values_list("texto_id", "completado")
    )
    textos_con_progreso = [
        {"texto": t, "completado": progreso_map.get(t.id, False), "n_ejercicios": t.ejercicios.count()}
        for t in textos
    ]
    mcer = _calcular_mcer_lectura(request.user)
    return render(request, "core/lectura/indice.html", {
        "textos": textos_con_progreso,
        "mcer": mcer,
    })


@login_required
def texto_detalle(request, texto_id):
    texto = get_object_or_404(Texto, id=texto_id)
    ejercicios = texto.ejercicios.select_related("tecnica").order_by("orden")
    respuestas_previas = {
        r.ejercicio_id: r for r in RespuestaLectura.objects.filter(user=request.user, texto=texto)
    }
    ejercicios_data = [
        {"ejercicio": e, "respuesta": respuestas_previas.get(e.id)}
        for e in ejercicios
    ]
    progreso, _ = ProgresoTexto.objects.get_or_create(usuario=request.user, texto=texto)
    completados = sum(1 for e in ejercicios_data if e["respuesta"] and e["respuesta"].es_correcta)
    total = len(ejercicios_data)
    return render(request, "core/lectura/texto_detalle.html", {
        "texto": texto,
        "ejercicios": ejercicios_data,
        "progreso": progreso,
        "completados": completados,
        "total": total,
    })


@login_required
@require_POST
def evaluar_ejercicio_lectura(request):
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return JsonResponse({"error": "JSON invalido"}, status=400)
    else:
        data = request.POST.dict()

    ejercicio_id = data.get("ejercicio_id")
    respuesta_raw = (data.get("respuesta") or "").strip()
    if not ejercicio_id:
        return JsonResponse({"error": "falta ejercicio_id"}, status=400)

    try:
        ejercicio = EjercicioLectura.objects.select_related("tecnica", "texto").get(id=ejercicio_id)
    except EjercicioLectura.DoesNotExist:
        return JsonResponse({"error": "ejercicio no existe"}, status=404)

    es_correcta = None
    feedback = ""
    if ejercicio.tipo == "multiple_choice":
        correcta = str(ejercicio.payload.get("correcta", "")).upper()
        letra = respuesta_raw[:1].upper()
        es_correcta = (letra == correcta)
        feedback = f"{'Correcto' if es_correcta else 'Incorrecto'}. Correcta: {correcta}."
    elif ejercicio.tipo == "verdadero_falso":
        correcta = str(ejercicio.payload.get("correcta", "")).lower()
        es_correcta = respuesta_raw.lower() in (correcta, "v", "true")
        feedback = f"{'Correcto' if es_correcta else 'Incorrecto'}."
    elif ejercicio.tipo == "abierta":
        es_correcta = None
        feedback = "Respuesta guardada. Tu profesor la revisara."

    with transaction.atomic():
        RespuestaLectura.objects.create(
            user=request.user, ejercicio=ejercicio, texto=ejercicio.texto,
            respuesta=respuesta_raw, es_correcta=es_correcta,
        )
        prog_tec, _ = ProgresoTecnicaLectura.objects.get_or_create(
            usuario=request.user, tecnica=ejercicio.tecnica
        )
        prog_tec.intentos += 1
        if es_correcta is True:
            if prog_tec.estado == "no_iniciada":
                prog_tec.estado = "en_progreso"
            elif prog_tec.estado == "en_progreso":
                aciertos_prev = RespuestaLectura.objects.filter(
                    user=request.user, ejercicio__tecnica=ejercicio.tecnica, es_correcta=True
                ).count()
                if aciertos_prev >= 2:
                    prog_tec.estado = "dominada"
        elif es_correcta is False and prog_tec.estado == "no_iniciada":
            prog_tec.estado = "en_progreso"
        prog_tec.save()

        prog_texto, _ = ProgresoTexto.objects.get_or_create(
            usuario=request.user, texto=ejercicio.texto
        )
        total_ej = ejercicio.texto.ejercicios.count()
        correctos = RespuestaLectura.objects.filter(
            user=request.user, texto=ejercicio.texto, es_correcta=True
        ).values("ejercicio").distinct().count()
        prog_texto.ejercicios_correctos = correctos
        prog_texto.ejercicios_totales = total_ej
        if correctos >= total_ej and total_ej > 0:
            prog_texto.completado = True
            prog_texto.completado_en = timezone.now()
        prog_texto.save()

    return JsonResponse({
        "ok": True, "es_correcta": es_correcta, "feedback": feedback,
        "estado_tecnica": prog_tec.estado,
        "progreso_texto": {"correctos": correctos, "total": total_ej, "completado": prog_texto.completado},
    })


@login_required
def mi_progreso_lectura(request):
    mcer = _calcular_mcer_lectura(request.user)
    total_resp = RespuestaLectura.objects.filter(user=request.user).count()
    correctas = RespuestaLectura.objects.filter(user=request.user, es_correcta=True).count()
    tasa = round(correctas / total_resp * 100, 1) if total_resp else 0

    por_proceso = {}
    for p in ["P1", "P2", "P3", "P4"]:
        tecs_p = TecnicaLectura.objects.filter(proceso=p)
        dominadas = ProgresoTecnicaLectura.objects.filter(
            usuario=request.user, tecnica__in=tecs_p, estado="dominada"
        ).count()
        total_p = tecs_p.count()
        por_proceso[p] = {
            "dominadas": dominadas, "total": total_p,
            "pct": round(100 * dominadas / total_p) if total_p else 0,
        }

    textos_completados = ProgresoTexto.objects.filter(usuario=request.user, completado=True).count()
    textos_totales = Texto.objects.count()

    return render(request, "core/lectura/mi_progreso.html", {
        "mcer": mcer, "total_resp": total_resp, "correctas": correctas,
        "tasa": tasa, "por_proceso": por_proceso,
        "textos_completados": textos_completados, "textos_totales": textos_totales,
    })


def _calcular_mcer_lectura(user):
    out = {}
    for n in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        tecs_n = TecnicaLectura.objects.filter(nivel_mcer=n)
        total = tecs_n.count()
        dominadas = ProgresoTecnicaLectura.objects.filter(
            usuario=user, tecnica__in=tecs_n, estado="dominada"
        ).count()
        out[n] = {"total": total, "dominadas": dominadas,
                  "pct": round(100 * dominadas / total) if total else 0}
    return out
