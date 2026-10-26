from django.contrib import admin

from .models import ContenidoJSON, EjercicioLinguistico, ProgresoCategoria, Respuesta, TecnicaLinguistica


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_ejercicio', 'item_id', 'es_correcta', 'puntuacion', 'fecha')
    list_filter = ('es_correcta', 'tipo_ejercicio', 'fecha')
    search_fields = ('user__username', 'respuesta_usuario')

@admin.register(ProgresoCategoria)
class ProgresoCategoriaAdmin(admin.ModelAdmin):
    list_display = ('user', 'categoria', 'aciertos', 'intentos', 'porcentaje')
    list_filter = ('categoria',)

@admin.register(EjercicioLinguistico)
class EjercicioLinguisticoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'tipo', 'creado_en')
    search_fields = ('titulo', 'categoria', 'tipo')
    list_filter = ('categoria', 'tipo', 'creado_en')

@admin.register(TecnicaLinguistica)
class TecnicaLinguisticaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'creado_en')
    search_fields = ('nombre', 'descripcion', 'categoria')
    list_filter = ('categoria', 'creado_en')

@admin.register(ContenidoJSON)
class ContenidoJSONAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'creado_en')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria', 'creado_en')
from core.admin_redaccion import *  # noqa: F401,E402
from core.admin_srs import *  # noqa: F401,E402

# ─── Certificaciones obtenidas (agregado v1.7.4) ───
try:
    from core.models import CertificacionObtenida

    @admin.register(CertificacionObtenida)
    class CertificacionObtenidaAdmin(admin.ModelAdmin):
        list_display = (
            "user", "certificacion", "fecha_obtenida",
            "codigo_verificacion", "url_verificacion",
        )
        list_filter = ("certificacion", "fecha_obtenida")
        search_fields = ("user__username", "codigo_verificacion")
        ordering = ("-fecha_obtenida",)
        autocomplete_fields = ("user",)
except ImportError:
    pass
