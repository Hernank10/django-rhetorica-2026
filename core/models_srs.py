"""Modelos del sistema de repeticion espaciada (SRS / SM-2)."""

from django.conf import settings
from django.db import models


class Flashcard(models.Model):
    """Tarjeta de repaso (vocabulario, declinacion, regla, etc.)."""

    TIPO_CHOICES = [
        ("vocabulario", "Vocabulario"),
        ("declinacion", "Declinacion"),
        ("conjugacion", "Conjugacion"),
        ("regla", "Regla gramatical"),
        ("redaccion", "Redaccion"),
    ]

    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="flashcards",
    )
    idioma = models.CharField(max_length=2, default="ES")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    frente = models.TextField()
    reverso = models.TextField()
    explicacion = models.TextField(blank=True, default="")
    ejemplo = models.TextField(blank=True, default="")
    ejercicio = models.TextField(blank=True, default="")
    respuesta_ejercicio = models.TextField(blank=True, default="")
    fuente_id = models.IntegerField(null=True, blank=True)
    categoria_gramatical = models.CharField(max_length=100, blank=True, default="")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("estudiante", "idioma", "frente", "tipo")
        ordering = ["-creado_en"]
        verbose_name = "Flashcard"
        verbose_name_plural = "Flashcards"

    def __str__(self):
        f = (self.frente or "")[:40]
        r = (self.reverso or "")[:40]
        return f"{f} -> {r}"


class Review(models.Model):
    """Instancia de repaso SM-2 de una flashcard.

    Cada Review es una sesion programada. El estado 'pendiente' es
    completada_en=None. Tras aplicar_sm2, la Review actual se marca
    completada y se crea una NUEVA Review con el estado actualizado.
    """

    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    programada_para = models.DateField(db_index=True)
    completada_en = models.DateTimeField(null=True, blank=True)
    calidad_respuesta = models.IntegerField(null=True, blank=True)

    # Estado SM-2
    intervalo_dias = models.PositiveIntegerField(default=0)
    facilidad = models.FloatField(default=2.5)
    repeticiones = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["programada_para", "id"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        f = (self.flashcard.frente or "")[:30]
        return f"{f} @ {self.programada_para}"

    @property
    def pendiente(self):
        return self.completada_en is None