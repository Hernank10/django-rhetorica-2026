"""Admin para modelos de lectura."""
from django.contrib import admin
from .models_lectura import (
    TecnicaLectura, Texto, EjercicioLectura,
    RespuestaLectura, ProgresoTecnicaLectura, ProgresoTexto,
)


@admin.register(TecnicaLectura)
class TecnicaLecturaAdmin(admin.ModelAdmin):
    list_display = ("numero", "proceso", "nivel_mcer", "titulo")
    list_filter = ("proceso", "nivel_mcer")
    search_fields = ("titulo", "teoria")


@admin.register(Texto)
class TextoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "nivel_mcer", "orden")
    list_filter = ("tipo", "nivel_mcer")
    search_fields = ("titulo",)


@admin.register(EjercicioLectura)
class EjercicioLecturaAdmin(admin.ModelAdmin):
    list_display = ("texto", "tecnica", "tipo", "orden")
    list_filter = ("tipo", "tecnica__proceso")
    search_fields = ("enunciado",)


@admin.register(RespuestaLectura)
class RespuestaLecturaAdmin(admin.ModelAdmin):
    list_display = ("user", "ejercicio", "es_correcta", "fecha")
    list_filter = ("es_correcta", "fecha")
    search_fields = ("user__username",)


@admin.register(ProgresoTecnicaLectura)
class ProgresoTecnicaLecturaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tecnica", "estado", "intentos")
    list_filter = ("estado",)
    search_fields = ("usuario__username",)


@admin.register(ProgresoTexto)
class ProgresoTextoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "texto", "completado", "ejercicios_correctos", "ejercicios_totales")
    list_filter = ("completado",)
    search_fields = ("usuario__username", "texto__titulo")
