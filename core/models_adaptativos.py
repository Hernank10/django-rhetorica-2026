"""Modelos para el motor de adaptabilidad linguistica.

Ver docs/adaptive_engine.md para el diseno completo.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Idioma(models.TextChoices):
    ESPANOL = "ES", _("Espanol")
    INGLES = "EN", _("Ingles")
    LATIN = "LA", _("Latin")


class HistorialErrorSintactico(models.Model):
    """Registro agregado de errores gramaticales por estudiante."""

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="historial_errores",
    )
    idioma = models.CharField(
        max_length=2,
        choices=Idioma.choices,
        default=Idioma.ESPANOL,
    )
    categoria_gramatical = models.CharField(max_length=100)
    patron_error = models.CharField(max_length=255, blank=True, default="")
    frecuencia = models.PositiveIntegerField(default=1)
    ultima_incidencia = models.DateTimeField(auto_now=True)
    resuelto = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Historial de error sintactico")
        verbose_name_plural = _("Historiales de errores sintacticos")
        ordering = ["-ultima_incidencia"]
        unique_together = [
            ("estudiante", "idioma", "categoria_gramatical", "patron_error"),
        ]
        indexes = [
            models.Index(
                fields=["estudiante", "idioma", "categoria_gramatical"],
                name="adapt_est_idioma_cat_idx",
            ),
            models.Index(
                fields=["estudiante", "resuelto"],
                name="adapt_est_resuelto_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.estudiante.username} - "
            f"{self.idioma}/{self.categoria_gramatical} "
            f"(x{self.frecuencia}{', resuelto' if self.resuelto else ''})"
        )

    def incrementar(self):
        self.frecuencia += 1
        if self.resuelto:
            self.resuelto = False
        self.save(update_fields=["frecuencia", "resuelto", "ultima_incidencia"])

    def marcar_resuelto(self):
        if not self.resuelto:
            self.resuelto = True
            self.save(update_fields=["resuelto", "ultima_incidencia"])