"""Vistas del taller de redaccion morfosintactica."""

from django.shortcuts import get_object_or_404, redirect, render

from core.models import EjercicioLinguistico, EvaluacionRedaccion
from core.services.redaccion import evaluar_ejercicio


def indice(request):
    """Lista publica de ejercicios de redaccion."""
    tecnicas = (
        EjercicioLinguistico.objects
        .filter(es_redaccion=True)
        .order_by("tipo_redaccion", "id")
    )
    return render(request, "core/redaccion/indice.html", {"tecnicas": tecnicas})


def detalle(request, ejercicio_id):
    """GET publico, POST requiere login. Param: ejercicio_id (viene de urls.py)."""
    ej = get_object_or_404(EjercicioLinguistico, pk=ejercicio_id, es_redaccion=True)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")

        texto = request.POST.get("texto", "").strip()
        tipo = ej.tipo_redaccion or ""

        if tipo:
            resultado = evaluar_ejercicio(texto, tipo)
        else:
            resultado = {
                "aprobado": False,
                "tipo_detectado": "n/a",
                "analisis": {},
                "feedback": "Ejercicio sin tipo_redaccion configurado.",
            }

        EvaluacionRedaccion.objects.create(
            estudiante=request.user,
            ejercicio=ej,
            texto_estudiante=texto,
            analisis_json=resultado.get("analisis", {}),
            aprobado=resultado.get("aprobado", False),
            feedback=resultado.get("feedback", ""),
        )

        return render(
            request,
            "core/redaccion/ejercicio.html",
            {"ejercicio": ej, "resultado": resultado, "texto_previo": texto},
        )

    return render(request, "core/redaccion/ejercicio.html", {"ejercicio": ej})


def historial(request):
    """Historial de evaluaciones del estudiante logueado."""
    if not request.user.is_authenticated:
        return redirect(f"/login/?next={request.path}")

    evaluaciones = (
        EvaluacionRedaccion.objects
        .filter(estudiante=request.user)
        .select_related("ejercicio")
        .order_by("-fecha", "-id")[:50]
    )
    return render(
        request,
        "core/redaccion/historial.html",
        {"evaluaciones": evaluaciones},
    )


def tecnicas_dashboard(request):
    """Dashboard de las 100 tecnicas de redaccion con charts + tabla."""
    from django.apps import apps
    from django.db.models import Count

    Ejercicio = apps.get_model("core", "EjercicioLinguistico")
    qs_base = Ejercicio.objects.filter(es_redaccion=True)

    tipo_sel = (request.GET.get("tipo") or "").strip()
    nivel_sel = (request.GET.get("nivel") or "").strip()

    qs = qs_base
    if tipo_sel:
        qs = qs.filter(tipo_redaccion=tipo_sel)
    if nivel_sel.isdigit():
        qs = qs.filter(nivel=int(nivel_sel))
    qs = qs.order_by("id")

    por_tipo = list(qs_base.values("tipo_redaccion").annotate(n=Count("id")).order_by("-n"))
    por_nivel = list(qs_base.values("nivel").annotate(n=Count("id")).order_by("nivel"))
    por_cat = list(qs_base.values("categoria").annotate(n=Count("id")).order_by("-n")[:10])

    context = {
        "tecnicas": qs,
        "total": qs.count(),
        "total_global": qs_base.count(),
        "filtros": {"tipo": tipo_sel, "nivel": nivel_sel},
        "tipos_disponibles": sorted({t for t in qs_base.values_list("tipo_redaccion", flat=True) if t}),
        "niveles_disponibles": sorted({n for n in qs_base.values_list("nivel", flat=True) if n}),
        "chart_tipos": {
            "labels": [x["tipo_redaccion"] or "Sin tipo" for x in por_tipo],
            "data": [x["n"] for x in por_tipo],
        },
        "chart_niveles": {
            "labels": [f"Nivel {x['nivel']}" for x in por_nivel],
            "data": [x["n"] for x in por_nivel],
        },
        "chart_categorias": {
            "labels": [x["categoria"] or "Sin categoria" for x in por_cat],
            "data": [x["n"] for x in por_cat],
        },
    }
    return render(request, "core/redaccion/tecnicas.html", context)

