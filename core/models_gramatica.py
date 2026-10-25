"""Modelos del modulo 11: gramatica castellana (100 tecnicas)."""
from django.conf import settings
from django.db import models


class TecnicaGramatical(models.Model):
    BLOQUES = [
        ("A", "Historia de la gramatica castellana"),
        ("B", "Clases de palabras"),
        ("C", "El sustantivo"),
        ("D", "El adjetivo"),
        ("E", "El verbo"),
        ("F", "Pronombres y determinantes"),
        ("G", "Reglas ortograficas actuales (RAE 2010)"),
    ]
    NIVELES = [
        ("basico", "Basico"),
        ("intermedio", "Intermedio"),
        ("avanzado", "Avanzado"),
    ]

    numero = models.PositiveSmallIntegerField(unique=True)
    bloque = models.CharField(max_length=1, choices=BLOQUES, db_index=True)
    titulo = models.CharField(max_length=200)
    teoria = models.TextField()
    explicacion = models.TextField()
    regla = models.CharField(max_length=200)
    ejemplo_correcto = models.TextField()
    ejemplo_incorrecto = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVELES, default="basico")
    modulo = models.CharField(
        max_length=20,
        choices=[("gramatica", "Gramatica"), ("generativa", "Generativa")],
        default="gramatica",
        db_index=True,
    )

    class Meta:
        ordering = ["numero"]
        verbose_name = "Tecnica gramatical"
        verbose_name_plural = "Tecnicas gramaticales"

    def __str__(self):
        return f"{self.numero:03d}. {self.titulo}"


class EjercicioGramatical(models.Model):
    TIPOS = [
        (1, "Seleccion multiple con justificacion"),
        (2, "Correccion inline"),
        (3, "Clasificacion"),
        (4, "Construccion guiada"),
        (5, "Deteccion de error"),
    ]

    tecnica = models.ForeignKey(
        TecnicaGramatical, on_delete=models.CASCADE, related_name="ejercicios"
    )
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    payload = models.JSONField()
    orden = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["tecnica__numero", "orden"]
        unique_together = ("tecnica", "orden")

    def __str__(self):
        return f"T{self.tecnica.numero:03d} - Ej{self.orden} (tipo {self.tipo})"


class ProgresoGramatical(models.Model):
    ESTADOS = [
        ("no_iniciada", "No iniciada"),
        ("en_progreso", "En progreso"),
        ("dominada", "Dominada"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progreso_gramatica",
    )
    tecnica = models.ForeignKey(TecnicaGramatical, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default="no_iniciada", db_index=True
    )
    aciertos_consecutivos = models.PositiveSmallIntegerField(default=0)
    intentos = models.PositiveSmallIntegerField(default=0)
    ultima_revision = models.DateTimeField(null=True, blank=True)
    proxima_revision = models.DateTimeField(null=True, blank=True, db_index=True)
    sm2_ef = models.FloatField(default=2.5)
    sm2_interval = models.PositiveIntegerField(default=0)
    sm2_repetitions = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("usuario", "tecnica")
        ordering = ["tecnica__numero"]

    def __str__(self):
        return f"{self.usuario.username} - T{self.tecnica.numero:03d} ({self.estado})"