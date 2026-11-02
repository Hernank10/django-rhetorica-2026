"""Modelos de competencia lectora (extension django-rhetorica)."""
from django.conf import settings
from django.db import models


class TecnicaLectura(models.Model):
    """Microhabilidad lectora (analogo a TecnicaGramatical)."""
    PROCESOS = [
        ("P1", "Localizacion y obtencion de informacion explicita"),
        ("P2", "Extraccion de conclusiones directas"),
        ("P3", "Interpretacion e integracion de ideas"),
        ("P4", "Analisis y evaluacion del contenido"),
    ]
    NIVELES = [
        ("A1", "A1"), ("A2", "A2"), ("B1", "B1"),
        ("B2", "B2"), ("C1", "C1"), ("C2", "C2"),
    ]
    numero = models.PositiveIntegerField()  # 1-100 por nivel
    proceso = models.CharField(max_length=2, choices=PROCESOS)
    nivel_mcer = models.CharField(max_length=2, choices=NIVELES)
    titulo = models.CharField(max_length=200)
    teoria = models.TextField()
    explicacion = models.TextField()
    regla = models.TextField()
    ejemplo_correcto = models.TextField()
    ejemplo_incorrecto = models.TextField()

    class Meta:
        ordering = ["numero"]
        unique_together = ("nivel_mcer", "numero")
        verbose_name = "Tecnica de lectura"
        verbose_name_plural = "Tecnicas de lectura"

    def __str__(self):
        return f"{self.numero} [{self.proceso}] {self.titulo}"


class Texto(models.Model):
    """Texto de lectura (literario o informativo)."""
    TIPOS = [
        ("literario", "Experiencia literaria"),
        ("informativo", "Adquisicion de informacion"),
    ]
    NIVELES = [
        ("A1", "A1"), ("A2", "A2"), ("B1", "B1"),
        ("B2", "B2"), ("C1", "C1"), ("C2", "C2"),
    ]
    titulo = models.CharField(max_length=300)
    cuerpo = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    nivel_mcer = models.CharField(max_length=2, choices=NIVELES)
    fuente = models.CharField(max_length=300, blank=True)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["nivel_mcer", "orden"]
        verbose_name = "Texto de lectura"
        verbose_name_plural = "Textos de lectura"

    def __str__(self):
        return f"[{self.nivel_mcer}] {self.titulo}"


class EjercicioLectura(models.Model):
    """Ejercicio asociado a un texto y a una tecnica lectora."""
    TIPOS = [
        ("multiple_choice", "Seleccion multiple"),
        ("verdadero_falso", "Verdadero/Falso"),
        ("ordenar", "Ordenar"),
        ("abierta", "Respuesta abierta"),
    ]
    texto = models.ForeignKey(Texto, on_delete=models.CASCADE, related_name="ejercicios")
    tecnica = models.ForeignKey(TecnicaLectura, on_delete=models.CASCADE, related_name="ejercicios")
    enunciado = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    payload = models.JSONField(default=dict)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["texto", "orden"]
        verbose_name = "Ejercicio de lectura"
        verbose_name_plural = "Ejercicios de lectura"

    def __str__(self):
        return f"{self.texto.titulo} - {self.get_tipo_display()}"


class RespuestaLectura(models.Model):
    """Respuesta de un usuario a un ejercicio de lectura."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="respuestas_lectura")
    ejercicio = models.ForeignKey(EjercicioLectura, on_delete=models.CASCADE, related_name="respuestas")
    texto = models.ForeignKey(Texto, on_delete=models.CASCADE, related_name="respuestas")
    respuesta = models.TextField(blank=True)
    es_correcta = models.BooleanField(null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    tiempo_segundos = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Respuesta de lectura"
        verbose_name_plural = "Respuestas de lectura"

    def __str__(self):
        return f"{self.user.username} - {self.ejercicio_id}"


class ProgresoTecnicaLectura(models.Model):
    """Estado de una tecnica lectora por usuario."""
    ESTADOS = [
        ("no_iniciada", "No iniciada"),
        ("en_progreso", "En progreso"),
        ("dominada", "Dominada"),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progreso_lectura")
    tecnica = models.ForeignKey(TecnicaLectura, on_delete=models.CASCADE, related_name="progresos")
    estado = models.CharField(max_length=15, choices=ESTADOS, default="no_iniciada")
    intentos = models.PositiveIntegerField(default=0)
    actualizado_en = models.DateTimeField(auto_now=True)

    # ─── Campos SM-2 (Fase 6A) ───
    # Algoritmo de repeticion espaciada (ver core/services/srs.py).
    # El wrapper de Fase 6B mapea calidad 1 (no sabia) -> hoy,
    # calidad 5 (si sabia) -> hoy + 1 dia (primer repaso).
    intervalo_dias = models.PositiveIntegerField(default=0)
    facilidad = models.FloatField(default=2.5)
    repeticiones = models.PositiveIntegerField(default=0)
    proxima_revision = models.DateField(null=True, blank=True)
    ultima_revision = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("usuario", "tecnica")
        verbose_name = "Progreso de tecnica lectora"
        verbose_name_plural = "Progresos de tecnicas lectoras"

    def __str__(self):
        return f"{self.usuario.username} - {self.tecnica_id} - {self.estado}"


class ProgresoTexto(models.Model):
    """Estado de un texto completo por usuario."""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progreso_textos")
    texto = models.ForeignKey(Texto, on_delete=models.CASCADE, related_name="progresos")
    completado = models.BooleanField(default=False)
    completado_en = models.DateTimeField(null=True, blank=True)
    ejercicios_correctos = models.PositiveIntegerField(default=0)
    ejercicios_totales = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("usuario", "texto")
        verbose_name = "Progreso de texto"
        verbose_name_plural = "Progresos de textos"

    def __str__(self):
        return f"{self.usuario.username} - {self.texto_id}"
