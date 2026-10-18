"""Admin de Flashcard y Review (SRS)."""
from django.contrib import admin

from core.models import Flashcard, Review


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ("id", "estudiante", "idioma", "tipo", "frente_corto", "creado_en")
    list_filter = ("idioma", "tipo")
    search_fields = ("frente", "reverso", "estudiante__username")
    date_hierarchy = "creado_en"
    list_per_page = 50

    def frente_corto(self, obj):
        return (obj.frente or "")[:60]
    frente_corto.short_description = "Frente"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id", "flashcard", "programada_para", "pendiente",
        "repeticiones", "intervalo_dias", "facilidad",
    )
    list_filter = ("completada_en", "programada_para")
    search_fields = ("flashcard__frente", "flashcard__estudiante__username")
    date_hierarchy = "programada_para"
    readonly_fields = ("completada_en",)
    list_per_page = 50

    def pendiente(self, obj):
        return obj.completada_en is None
    pendiente.boolean = True
    pendiente.short_description = "Pendiente"