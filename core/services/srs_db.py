"""Servicio SRS con BD: orquesta SM-2 puro + modelos Flashcard/Review."""
from django.apps import apps
from django.utils import timezone

from core.models import Flashcard, Review
from core.services.srs import aplicar_sm2


def programar_primera_revision(flashcard, hoy=None):
    """Crea la primera Review pendiente de una Flashcard.

    Idempotente: si ya existe una Review pendiente, la retorna.
    """
    if hoy is None:
        hoy = timezone.localdate()

    existente = Review.objects.filter(
        flashcard=flashcard, completada_en__isnull=True
    ).first()
    if existente is not None:
        return existente

    return Review.objects.create(
        flashcard=flashcard,
        programada_para=hoy,
        intervalo_dias=0,
        facilidad=2.5,
        repeticiones=0,
    )


def aplicar_sm2_y_guardar(review, calidad, hoy=None):
    """Aplica SM-2 in-place, marca la Review actual como completada
    y crea una NUEVA Review con el estado post-SM-2.

    Retorna la nueva Review (pendiente).
    """
    if hoy is None:
        hoy = timezone.localdate()

    aplicar_sm2(review, calidad, hoy=hoy)

    review.completada_en = timezone.now()
    review.save()

    nueva = Review.objects.create(
        flashcard=review.flashcard,
        programada_para=review.programada_para,
        intervalo_dias=review.intervalo_dias,
        facilidad=review.facilidad,
        repeticiones=review.repeticiones,
    )
    return nueva


def reviews_para_hoy(estudiante, hoy=None):
    """QuerySet de Reviews pendientes del estudiante, ordenadas por fecha."""
    if hoy is None:
        hoy = timezone.localdate()
    return (
        Review.objects
        .filter(
            flashcard__estudiante=estudiante,
            completada_en__isnull=True,
            programada_para__lte=hoy,
        )
        .select_related("flashcard")
        .order_by("programada_para", "id")
    )


def crear_flashcards_desde_errores(estudiante):
    """Convierte HistorialErrorSintactico en Flashcards.

    Idempotente via unique_together de Flashcard.
    Programa la primera revision de las nuevas.
    Retorna lista de Flashcard (todas, nuevas o existentes).
    """
    Historial = apps.get_model("core", "HistorialErrorSintactico")
    errores = Historial.objects.filter(estudiante=estudiante, resuelto=False)

    resultado = []
    for err in errores:
        flashcard, creada = Flashcard.objects.get_or_create(
            estudiante=estudiante,
            idioma=err.idioma,
            tipo="redaccion",
            frente=err.patron_error,
            defaults={
                "reverso": err.categoria_gramatical,
                "categoria_gramatical": err.categoria_gramatical,
            },
        )
        if creada:
            programar_primera_revision(flashcard)
        resultado.append(flashcard)
    return resultado


def estadisticas_estudiante(estudiante, hoy=None):
    """Metricas del estudiante.

    Returns dict:
        total_flashcards: int
        reviews_pendientes: int
        retencion_pct: float | None  (None si no hay reviews completadas)
        proxima_revision: date | None
    """
    if hoy is None:
        hoy = timezone.localdate()

    total_fc = Flashcard.objects.filter(estudiante=estudiante).count()
    pendientes = reviews_para_hoy(estudiante, hoy).count()

    completadas = Review.objects.filter(
        flashcard__estudiante=estudiante,
        completada_en__isnull=False,
    )
    total_completadas = completadas.count()
    if total_completadas == 0:
        retencion = None
    else:
        correctas = completadas.filter(calidad_respuesta__gte=3).count()
        retencion = round(100.0 * correctas / total_completadas, 1)

    proxima = (
        Review.objects
        .filter(flashcard__estudiante=estudiante, completada_en__isnull=True)
        .order_by("programada_para")
        .values_list("programada_para", flat=True)
        .first()
    )

    return {
        "total_flashcards": total_fc,
        "reviews_pendientes": pendientes,
        "retencion_pct": retencion,
        "proxima_revision": proxima,
    }