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