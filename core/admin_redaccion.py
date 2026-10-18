"""Admin del taller de redaccion morfosintactica."""

from django.contrib import admin

from core.models import EjercicioLinguistico, EvaluacionRedaccion


class EvaluacionRedaccionInline(admin.TabularInline):
    model = EvaluacionRedaccion
    extra = 0
    fields = ("estudiante", "aprobado", "fecha")
    readonly_fields = ("fecha",)
    can_delete = False
    show_change_link = True


# El admin de EjercicioLinguistico ya esta registrado en core/admin.py.
# Le anadimos el inline SIN re-registrarlo (evita AlreadyRegistered).
_admin_existente = admin.site._registry.get(EjercicioLinguistico)
if _admin_existente is not None:
    _actuales = list(getattr(_admin_existente, "inlines", []))
    if EvaluacionRedaccionInline not in _actuales:
        _admin_existente.inlines = _actuales + [EvaluacionRedaccionInline]


@admin.register(EvaluacionRedaccion)
class EvaluacionRedaccionAdmin(admin.ModelAdmin):
    list_display = (
        "estudiante",
        "ejercicio",
        "aprobado",
        "fecha",
        "tipo_ejercicio",
    )
    list_filter = ("aprobado", "fecha", "ejercicio__tipo_redaccion")
    search_fields = ("estudiante__username", "ejercicio__titulo", "texto_estudiante")
    readonly_fields = ("fecha", "analisis_json")
    date_hierarchy = "fecha"
    ordering = ("-fecha",)

    def tipo_ejercicio(self, obj):
        return obj.ejercicio.tipo_redaccion or "-"
    tipo_ejercicio.short_description = "Tipo"