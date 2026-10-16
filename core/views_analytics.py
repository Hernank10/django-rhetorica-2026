"""Endpoints JSON de analytics para profesores."""

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .decorators import solo_profesor
from .services import analytics


def _parse_int(request, key, default, minimo=1, maximo=None):
    """Parsea query param entero con validacion y clamps."""
    try:
        valor = int(request.GET.get(key, default))
    except (ValueError, TypeError):
        valor = default
    valor = max(minimo, valor)
    if maximo is not None:
        valor = min(maximo, valor)
    return valor


def _usuarios_para(request):
    """Devuelve el queryset de estudiantes que el profesor puede ver.

    Por ahora: todos los usuarios no-staff.
    """
    User = get_user_model()
    return User.objects.filter(is_staff=False)


@require_GET
@solo_profesor
def heatmap_alumnos(request):
    """GET /api/profesor/analytics/heatmap/?dias=30"""
    dias = _parse_int(request, "dias", 30, 1, 365)
    data = analytics.heatmap_categoria_por_alumno(_usuarios_para(request), dias)
    return JsonResponse(data)


@require_GET
@solo_profesor
def heatmap_grupo(request):
    """GET /api/profesor/analytics/heatmap-grupo/?dias=30"""
    dias = _parse_int(request, "dias", 30, 1, 365)
    data = analytics.heatmap_categoria_por_grupo(_usuarios_para(request), dias)
    return JsonResponse({"grupos": data})


@require_GET
@solo_profesor
def tiempos(request):
    """GET /api/profesor/analytics/tiempos/?dias=30"""
    dias = _parse_int(request, "dias", 30, 1, 365)
    data = analytics.tiempo_promedio_por_categoria(_usuarios_para(request), dias)
    return JsonResponse({"categorias": data})


@require_GET
@solo_profesor
def retencion(request):
    """GET /api/profesor/analytics/retencion/?semanas=8"""
    semanas = _parse_int(request, "semanas", 8, 1, 52)
    data = analytics.retencion_semanal(_usuarios_para(request), semanas)
    return JsonResponse({"semanas": data})


@require_GET
@solo_profesor
def errores(request):
    """GET /api/profesor/analytics/errores/?idioma=LA&dias=30"""
    idioma = request.GET.get("idioma", "LA").upper()
    if idioma not in {"ES", "EN", "LA"}:
        idioma = "LA"
    dias = _parse_int(request, "dias", 30, 1, 365)
    data = analytics.top_errores_por_idioma(idioma, dias)
    return JsonResponse({"idioma": idioma, "errores": data})


@require_GET
@solo_profesor
def resumen_alumno(request, estudiante_id):
    """GET /api/profesor/analytics/alumno/<id>/"""
    User = get_user_model()
    try:
        estudiante = User.objects.get(pk=estudiante_id, is_staff=False)
    except User.DoesNotExist:
        return JsonResponse({"error": "Alumno no encontrado"}, status=404)

    data = analytics.resumen_alumno(estudiante)
    data["username"] = estudiante.username
    data["id"] = estudiante.id
    return JsonResponse(data)



# ============================================================
# VISTA HTML (no JSON) — Dashboard de Analytics
# ============================================================
from django.shortcuts import render  # noqa: E402


@solo_profesor
def dashboard(request):
    """GET /profesor/analytics/ — UI con 4 widgets que consumen los endpoints JSON."""
    return render(request, "core/profesor/analytics.html")