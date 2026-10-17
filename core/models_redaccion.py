"""Modelos para el taller de redaccion morfosintactica."""

from django.conf import settings
from django.db import models


class EvaluacionRedaccion(models.Model):
    """Registro de una entrega de redaccion evaluada."""
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evaluaciones_redaccion",
    )
    ejercicio = models.ForeignKey(
        "core.EjercicioLinguistico",
        on_delete=models.CASCADE,
        related_name="evaluaciones_redaccion",
    )
    texto_estudiante = models.TextField()
    analisis_json = models.JSONField(default=dict, blank=True)
    aprobado = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Evaluacion de redaccion"
        verbose_name_plural = "Evaluaciones de redaccion"
        indexes = [
            models.Index(fields=["estudiante", "-fecha"]),
        ]

    def __str__(self):
        return f"{self.estudiante.username} - ej {self.ejercicio_id}"
