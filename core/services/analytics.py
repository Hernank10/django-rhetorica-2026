"""Servicio de analytics. Funciones puras, sin HTTP.

Todas reciben querysets o parametros y devuelven estructuras
JSON-serializables (listas, dicts, numeros).
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Min, Q
from django.db.models.functions import TruncWeek
from django.utils import timezone

from core.models import (
    ProgresoCategoria, Respuesta,
    LogroObtenido, CertificacionObtenida,
)
from core.models_adaptativos import HistorialErrorSintactico


def _cutoff(dias):
    """Datetime de hace 'dias' dias."""
    return timezone.now() - timedelta(days=dias)


def heatmap_categoria_por_alumno(usuarios, dias=30):
    """Matriz {usuarios:[], categorias:[], valores:[[tasa_% o None]]}."""
    qs = (
        Respuesta.objects
        .filter(user__in=usuarios, fecha__gte=_cutoff(dias))
        .values("user_id", "tipo_ejercicio")
        .annotate(
            total=Count("id"),
            aciertos=Count("id", filter=Q(es_correcta=True)),
        )
    )

    user_ids = sorted({r["user_id"] for r in qs})
    categorias = sorted({r["tipo_ejercicio"] for r in qs})

    if not user_ids:
        return {"usuarios": [], "categorias": [], "valores": []}

    idx = {(r["user_id"], r["tipo_ejercicio"]): r for r in qs}

    valores = []
    for uid in user_ids:
        fila = []
        for cat in categorias:
            r = idx.get((uid, cat))
            if r and r["total"]:
                fila.append(round(r["aciertos"] / r["total"] * 100, 1))
            else:
                fila.append(None)
        valores.append(fila)

    User = get_user_model()
    nombres = dict(
        User.objects.filter(id__in=user_ids).values_list("id", "username")
    )

    return {
        "usuarios": [
            {"id": uid, "username": nombres.get(uid, "?")}
            for uid in user_ids
        ],
        "categorias": categorias,
        "valores": valores,
    }


def heatmap_categoria_por_grupo(usuarios, dias=30):
    """Tasa agregada por categoria, ordenada desc."""
    qs = (
        Respuesta.objects
        .filter(user__in=usuarios, fecha__gte=_cutoff(dias))
        .values("tipo_ejercicio")
        .annotate(
            total=Count("id"),
            aciertos=Count("id", filter=Q(es_correcta=True)),
        )
    )

    resultado = []
    for r in qs:
        tasa = (r["aciertos"] / r["total"] * 100) if r["total"] else 0.0
        resultado.append({
            "categoria": r["tipo_ejercicio"],
            "total": r["total"],
            "aciertos": r["aciertos"],
            "tasa": round(tasa, 1),
        })
    resultado.sort(key=lambda x: -x["tasa"])
    return resultado


def tiempo_promedio_por_categoria(usuarios, dias=30):
    """Segundos promedio por categoria, ordenado desc."""
    qs = (
        Respuesta.objects
        .filter(user__in=usuarios, fecha__gte=_cutoff(dias))
        .values("tipo_ejercicio")
        .annotate(
            tiempo_promedio=Avg("tiempo_segundos"),
            n=Count("id"),
        )
        .order_by("-tiempo_promedio")
    )

    return [
        {
            "categoria": r["tipo_ejercicio"],
            "tiempo_promedio_seg": round(r["tiempo_promedio"] or 0, 1),
            "n_respuestas": r["n"],
        }
        for r in qs
    ]


def retencion_semanal(usuarios, semanas=8):
    """Activos y total de respuestas por semana ISO."""
    desde = timezone.now() - timedelta(weeks=semanas)

    qs = (
        Respuesta.objects
        .filter(user__in=usuarios, fecha__gte=desde)
        .annotate(semana=TruncWeek("fecha"))
        .values("semana")
        .annotate(
            activos=Count("user", distinct=True),
            total_respuestas=Count("id"),
        )
        .order_by("semana")
    )

    return [
        {
            "semana_iso": r["semana"].strftime("%Y-W%V") if r["semana"] else "?",
            "activos": r["activos"],
            "total_respuestas": r["total_respuestas"],
        }
        for r in qs
    ]


def top_errores_por_idioma(idioma="LA", dias=30):
    """Top categorias gramaticales con mas errores activos."""
    desde = _cutoff(dias)
    qs = (
        HistorialErrorSintactico.objects
        .filter(
            idioma=idioma,
            resuelto=False,
            ultima_incidencia__gte=desde,
        )
        .values("categoria_gramatical")
        .annotate(
            n_alumnos=Count("estudiante", distinct=True),
            frecuencia_total=Count("id"),
        )
        .order_by("-n_alumnos")
    )

    return [
        {
            "categoria_gramatical": e["categoria_gramatical"],
            "n_alumnos": e["n_alumnos"],
            "frecuencia_total": e["frecuencia_total"],
        }
        for e in qs
    ]


def resumen_alumno(estudiante):
    """Resumen individual: progreso, logros, certificaciones, errores."""
    progreso = list(ProgresoCategoria.objects.filter(user=estudiante).values(
        "categoria", "aciertos", "intentos",
        "nivel_dominio", "estrellas_obtenidas",
    ))

    logros = list(LogroObtenido.objects.filter(user=estudiante).values(
        "logro__nombre", "fecha_obtenida",
    ))

    certificaciones = list(
        CertificacionObtenida.objects.filter(user=estudiante).values(
            "certificacion__nombre", "fecha_obtenida",
            "codigo_verificacion",
        )
    )

    errores = list(
        HistorialErrorSintactico.objects
        .filter(estudiante=estudiante, resuelto=False)
        .values("idioma", "categoria_gramatical", "frecuencia")
    )

    return {
        "progreso": progreso,
        "logros": logros,
        "certificaciones": certificaciones,
        "historial_errores": errores,
    }