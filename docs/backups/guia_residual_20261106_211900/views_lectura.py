"""Vistas de lectura (indice, detalle, evaluacion, progreso)."""
import json
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.services.srs import intervalo_estimado
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


# ═══════════════════════════════════════════════════════════════
# Fase 6B - Wrapper SM-2 para ProgresoTecnicaLectura
# ═══════════════════════════════════════════════════════════════
def _aplicar_sm2_a_progreso(progreso, calidad):
    """Adapta SM-2 (core.services.srs) a ProgresoTecnicaLectura.

    Calidad: 1 = no sabia, 5 = si sabia.

    Reglas:
      - Primer repaso (repeticiones == 0):
          * calidad < 3  -> proxima_revision = hoy (revisar hoy)
          * calidad >= 3 -> intervalo 1 dia, proxima_revision = hoy + 1
      - Repasos >= 2:
          * calidad < 3  -> reset (repeticiones=0, proxima_revision=hoy)
          * calidad >= 3 -> SM-2 estandar (intervalo x facilidad)
    """
    hoy = timezone.now().date()

    if progreso.repeticiones == 0:
        # Primer repaso: regla explicita (SM-2 estandar no distingue 1 vs 5 aqui)
        if calidad < 3:
            progreso.proxima_revision = hoy
            progreso.repeticiones = 0
        else:
            progreso.intervalo_dias = 1
            progreso.repeticiones = 1
            progreso.proxima_revision = hoy + timedelta(days=1)
    else:
        # SM-2 estandar para repasos posteriores
        if calidad < 3:
            progreso.repeticiones = 0
            progreso.intervalo_dias = 0
            progreso.proxima_revision = hoy
        else:
            nuevo_int = intervalo_estimado(
                progreso.intervalo_dias,
                progreso.facilidad,
                progreso.repeticiones,
                calidad,
            )
            progreso.intervalo_dias = nuevo_int
            progreso.repeticiones += 1
            progreso.facilidad = max(
                1.3,
                progreso.facilidad + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02))
            )
            progreso.proxima_revision = hoy + timedelta(days=nuevo_int)

    # Fase 6D: actualizar estado segun repeticiones y facilidad
    # - 2+ aciertos con facilidad >= 2.3 -> dominada
    # - 1+ acierto -> en_progreso
    # - 0 aciertos -> no_iniciada (no cambia)
    if progreso.repeticiones >= 2 and progreso.facilidad >= 2.3:
        progreso.estado = "dominada"
    elif progreso.repeticiones >= 1:
        if progreso.estado != "dominada":
            progreso.estado = "en_progreso"

    progreso.ultima_revision = timezone.now()
    progreso.save()
    return progreso


# ═══════════════════════════════════════════════════════════════
# Fase 6B - Vistas de flashcards (SM-2)
# ═══════════════════════════════════════════════════════════════
@login_required
def flashcards_lectura(request):
    """Sesion de estudio de flashcards de lectura (SM-2).

    GET /lectura/flashcards/?nivel=A1&proceso=P1&modo=estudio
    Muestra la primera tecnica pendiente (proxima_revision <= hoy o None).
    """
    nivel = request.GET.get("nivel", "A1").upper()
    proceso = request.GET.get("proceso", "").upper()
    modo = request.GET.get("modo", "estudio")
    hoy = timezone.now().date()

    qs = TecnicaLectura.objects.filter(nivel_mcer=nivel)
    if proceso in ("P1", "P2", "P3", "P4"):
        qs = qs.filter(proceso=proceso)
    qs = qs.order_by("numero")

    # Cargar progreso del usuario para estas tecnicas
    progresos = {
        p.tecnica_id: p
        for p in ProgresoTecnicaLectura.objects.filter(
            usuario=request.user, tecnica__in=qs
        )
    }

    # Pendientes: sin progreso, sin proxima_revision, o proxima_revision <= hoy
    pendientes = []
    for tec in qs:
        prog = progresos.get(tec.id)
        if prog is None or prog.proxima_revision is None or prog.proxima_revision <= hoy:
            pendientes.append((tec, prog))

    total = qs.count()
    completadas = total - len(pendientes)

    if not pendientes:
        return render(request, "core/lectura/flashcards_completado.html", {
            "nivel": nivel,
            "proceso": proceso or "todos",
            "total": total,
        })

    tec, prog = pendientes[0]
    # Textos que practican esta tecnica (ordenados por cercania de nivel)
    NIVEL_ORDER = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
    tec_nivel = NIVEL_ORDER.get(tec.nivel_mcer, 3)
    textos_practica = sorted(
        Texto.objects.filter(ejercicios__tecnica=tec).distinct(),
        key=lambda t: (abs(NIVEL_ORDER.get(t.nivel_mcer, 3) - tec_nivel), t.orden),
    )[:2]
    return render(request, "core/lectura/flashcards_lectura.html", {
        "tecnica": tec,
        "progreso": prog,
        "pendientes": len(pendientes),
        "total": total,
        "completadas": completadas,
        "nivel": nivel,
        "proceso": proceso or "todos",
        "modo": modo,
        "textos_practica": textos_practica,
    })


@login_required
@require_POST
def flashcards_verificar(request):
    """Registra la respuesta si/no y actualiza SM-2 del progreso."""
    tecnica_id = request.POST.get("tecnica_id")
    sabia = request.POST.get("sabia", "0") == "1"

    if not tecnica_id:
        return redirect("lectura:flashcards_lectura")

    tecnica = get_object_or_404(TecnicaLectura, id=tecnica_id)
    progreso, _ = ProgresoTecnicaLectura.objects.get_or_create(
        usuario=request.user,
        tecnica=tecnica,
        defaults={"estado": "no_iniciada"},
    )

    calidad = 5 if sabia else 1
    _aplicar_sm2_a_progreso(progreso, calidad)


    return redirect("lectura:flashcards_lectura")


# ══════════════════════════════════════════════════════════════════
# Vista de la guia de certificados
# ══════════════════════════════════════════════════════════════════
from pathlib import Path as _Path
from django.conf import settings as _settings
from django.shortcuts import render as _render


def guia_certificados(request):
    """Renderiza docs/GUIA_CERTIFICADOS.md como HTML."""
    guia_path = _Path(_settings.BASE_DIR) / "docs" / "GUIA_CERTIFICADOS.md"

    if not guia_path.exists():
        return _render(request, "core/lectura/guia_certificados.html", {
            "titulo": "Guia no disponible",
            "contenido_html": (
                "<p class='text-danger'>La guia aun no esta disponible. "
                "Contacta con el administrador.</p>"
            ),
        })

    try:
        import markdown
        md_content = guia_path.read_text(encoding="utf-8")
        contenido_html = markdown.markdown(
            md_content,
            extensions=["extra", "toc", "tables", "fenced_code", "sane_lists"],
        )
    except ImportError:
        contenido_html = "<pre>" + guia_path.read_text(encoding="utf-8") + "</pre>"

    return _render(request, "core/lectura/guia_certificados.html", {
        "titulo": "Guia para obtener certificados",
        "contenido_html": contenido_html,
    })

