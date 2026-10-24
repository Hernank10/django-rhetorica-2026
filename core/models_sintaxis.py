from django.conf import settings
from django.db import models


class TecnicaSintactica(models.Model):
    BLOQUES = [
        ("A", "Oración simple"),
        ("B", "Concordancia y régimen"),
        ("C", "Coordinación"),
        ("D", "Subordinación sustantiva"),
        ("E", "Subordinación adjetiva"),
        ("F", "Subordinación adverbial"),
        ("G", "Yuxtaposición y puntuación"),
    ]
    NIVELES = [
        ("basico", "Básico"),
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

    class Meta:
        ordering = ["numero"]
        verbose_name = "Técnica sintáctica"
        verbose_name_plural = "Técnicas sintácticas"

    def __str__(self):
        return f"{self.numero:03d}. {self.titulo}"


class EjercicioTecnica(models.Model):
    TIPOS = [
        (1, "Selección múltiple con justificación"),
        (2, "Corrección inline"),
        (3, "Clasificación"),
        (4, "Construcción guiada"),
        (5, "Detección de error"),
    ]

    tecnica = models.ForeignKey(
        TecnicaSintactica, on_delete=models.CASCADE, related_name="ejercicios"
    )
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    payload = models.JSONField()
    orden = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["tecnica__numero", "orden"]
        unique_together = ("tecnica", "orden")
        verbose_name = "Ejercicio de técnica"
        verbose_name_plural = "Ejercicios de técnica"

    def __str__(self):
        return f"T{self.tecnica.numero:03d} - Ej{self.orden} (tipo {self.tipo})"


class ProgresoTecnica(models.Model):
    ESTADOS = [
        ("no_iniciada", "No iniciada"),
        ("en_progreso", "En progreso"),
        ("dominada", "Dominada"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progreso_tecnicas",
    )
    tecnica = models.ForeignKey(TecnicaSintactica, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default="no_iniciada", db_index=True
    )
    aciertos_consecutivos = models.PositiveSmallIntegerField(default=0)
    intentos = models.PositiveSmallIntegerField(default=0)
    ultima_revision = models.DateTimeField(null=True, blank=True)
    proxima_revision = models.DateTimeField(null=True, blank=True, db_index=True)
    # SM-2
    sm2_ef = models.FloatField(default=2.5)
    sm2_interval = models.PositiveIntegerField(default=0)
    sm2_repetitions = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("usuario", "tecnica")
        ordering = ["tecnica__numero"]
        verbose_name = "Progreso de técnica"
        verbose_name_plural = "Progresos de técnicas"

    def __str__(self):
        return f"{self.usuario.username} - T{self.tecnica.numero:03d} ({self.estado})"