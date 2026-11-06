"""
Vistas de sesion de flashcards con carta flip + 3 botones.

Reutiliza:
  - ProgresoTecnicaLectura (SRS)
  - TecnicaLectura (contenido: teoria, regla, ejemplos)
  - _aplicar_sm2_a_progreso (existente en views_lectura.py)
  - Base de estudiante (template)
"""
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.models_lectura import ProgresoTecnicaLectura, TecnicaLectura

# Importar el motor SM-2 existente
try:
    from core.views_lectura import _aplicar_sm2_a_progreso
except ImportError:
    # Fallback: implementacion minima si no existe
    def _aplicar_sm2_a_progreso(progreso, calidad):
        from datetime import timedelta
        if calidad < 3:
            progreso.repeticiones = 0
            progreso.intervalo_dias = 1
        else:
            progreso.repeticiones += 1
            if progreso.repeticiones == 1:
                progreso.intervalo_dias = 1
            elif progreso.repeticiones == 2:
                progreso.intervalo_dias = 6
            else:
                progreso.intervalo_dias = int(progreso.intervalo_dias * progreso.facilidad)
        progreso.facilidad = max(1.3, progreso.facilidad + (0.1 - (5 - calidad) * 0.08))
        progreso.proxima_revision = date.today() + timedelta(days=progreso.intervalo_dias)
        progreso.ultima_revision = timezone.now()
        progreso.actualizado_en = timezone.now()
        progreso.save()


# ══════════════════════════════════════════════════════════════════
# GET /lectura/flashcards/sesion/
# ══════════════════════════════════════════════════════════════════
@login_required
def flashcards_sesion(request):
    """
    Muestra la siguiente carta vencida del usuario.

    Query params:
      - nivel (opcional): A1, A2, B1, B2, C1, C2
      - proceso (opcional): P1, P2, P3, P4

    Flujo:
      1. Busca cartas vencidas (proxima_revision <= hoy)
      2. Si no hay, muestra "sesion completada"
      3. Si hay, muestra la primera con su contenido
    """
    nivel = request.GET.get("nivel", "").strip() or None
    proceso = request.GET.get("proceso", "").strip() or None

    # Buscar cartas vencidas del usuario
    qs = ProgresoTecnicaLectura.objects.filter(
        usuario=request.user,
        proxima_revision__lte=date.today(),
    ).select_related("tecnica")

    if nivel:
        qs = qs.filter(tecnica__nivel_mcer=nivel)
    if proceso:
        qs = qs.filter(tecnica__proceso=proceso)

    # Ordenar por proxima_revision (las mas vencidas primero)
    qs = qs.order_by("proxima_revision", "id")

    total_vencidas = qs.count()
    pendientes_hoy = ProgresoTecnicaLectura.objects.filter(
        usuario=request.user,
        proxima_revision__lte=date.today(),
    ).count()

    if total_vencidas == 0:
        return render(request, "core/lectura/flashcards_sesion.html", {
            "completado": True,
            "total_vencidas": 0,
            "pendientes_hoy": pendientes_hoy,
            "nivel": nivel,
            "proceso": proceso,
        })

    progreso = qs.first()
    tecnica = progreso.tecnica

    return render(request, "core/lectura/flashcards_sesion.html", {
        "completado": False,
        "progreso": progreso,
        "tecnica": tecnica,
        "total_vencidas": total_vencidas,
        "pendientes_hoy": pendientes_hoy,
        "nivel": nivel,
        "proceso": proceso,
        # Badge de estado
        "estado_badge": {
            "no_iniciada": ("secondary", "Nueva"),
            "en_progreso": ("warning", "En repaso"),
            "dominada": ("success", "Dominada"),
        }.get(progreso.estado, ("secondary", progreso.estado)),
    })


# ══════════════════════════════════════════════════════════════════
# POST /lectura/flashcards/calificar/
# ══════════════════════════════════════════════════════════════════
@login_required
@require_POST
def flashcards_calificar(request):
    """
    Califica la carta actual y devuelve la siguiente.

    POST params:
      - tecnica_id (requerido)
      - calificacion (requerido): "no" | "casi" | "si"

    Devuelve JSON:
      {
        "ok": true,
        "siguiente": { ... } | null,
        "completado": bool,
        "total_restantes": int
      }
    """
    tecnica_id = request.POST.get("tecnica_id")
    calificacion = request.POST.get("calificacion", "").lower()

    if not tecnica_id:
        return JsonResponse({"ok": False, "error": "falta tecnica_id"}, status=400)

    if calificacion not in ("no", "casi", "si"):
        return JsonResponse({"ok": False, "error": "calificacion invalida"}, status=400)

    # Mapeo a calidad SM-2
    calidad_map = {"no": 1, "casi": 3, "si": 5}
    calidad = calidad_map[calificacion]

    tecnica = get_object_or_404(TecnicaLectura, id=tecnica_id)
    progreso, _ = ProgresoTecnicaLectura.objects.get_or_create(
        usuario=request.user,
        tecnica=tecnica,
        defaults={"estado": "no_iniciada"},
    )

    # Aplicar SM-2
    _aplicar_sm2_a_progreso(progreso, calidad)

    # Actualizar estado
    if progreso.repeticiones >= 5 and progreso.intervalo_dias >= 21:
        progreso.estado = "dominada"
    elif progreso.repeticiones >= 1:
        progreso.estado = "en_progreso"
    else:
        progreso.estado = "no_iniciada"
    progreso.save(update_fields=["estado"])

    # Buscar siguiente carta
    nivel = request.POST.get("nivel", "").strip() or None
    proceso = request.POST.get("proceso", "").strip() or None

    qs = ProgresoTecnicaLectura.objects.filter(
        usuario=request.user,
        proxima_revision__lte=date.today(),
    ).select_related("tecnica").order_by("proxima_revision", "id")

    if nivel:
        qs = qs.filter(tecnica__nivel_mcer=nivel)
    if proceso:
        qs = qs.filter(tecnica__proceso=proceso)

    total_restantes = qs.count()

    if total_restantes == 0:
        return JsonResponse({
            "ok": True,
            "completado": True,
            "siguiente": None,
            "total_restantes": 0,
            "progreso_actual": {
                "intervalo_dias": progreso.intervalo_dias,
                "repeticiones": progreso.repeticiones,
                "estado": progreso.estado,
            },
        })

    siguiente = qs.first()
    t = siguiente.tecnica
    return JsonResponse({
        "ok": True,
        "completado": False,
        "total_restantes": total_restantes,
        "siguiente": {
            "id": t.id,
            "numero": t.numero,
            "nivel_mcer": t.nivel_mcer,
            "proceso": t.proceso,
            "titulo": t.titulo,
            "teoria": t.teoria,
            "regla": t.regla,
            "ejemplo_correcto": t.ejemplo_correcto,
            "ejemplo_incorrecto": t.ejemplo_incorrecto,
            "explicacion": t.explicacion,
            "estado": siguiente.estado,
            "intervalo_dias": siguiente.intervalo_dias,
            "repeticiones": siguiente.repeticiones,
        },
        "progreso_actual": {
            "intervalo_dias": progreso.intervalo_dias,
            "repeticiones": progreso.repeticiones,
            "estado": progreso.estado,
        },
    })