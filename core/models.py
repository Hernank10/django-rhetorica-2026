from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Respuesta(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='respuestas')
    tipo_ejercicio = models.CharField(max_length=50)
    item_id = models.IntegerField()
    respuesta_usuario = models.TextField()
    es_correcta = models.BooleanField(default=False)
    puntuacion = models.IntegerField(default=0)
    tiempo_segundos = models.IntegerField(default=0, help_text="Tiempo en segundos")
    fecha = models.DateTimeField(default=timezone.now)
    intento_numero = models.IntegerField(default=1)
    feedback = models.TextField(blank=True, null=True)

class ProgresoCategoria(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progreso')
    categoria = models.CharField(max_length=100)
    aciertos = models.IntegerField(default=0)
    intentos = models.IntegerField(default=0)
    nivel_dominio = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    estrellas_obtenidas = models.IntegerField(default=0)

    @property
    def porcentaje(self):
        if self.intentos == 0:
            return 0
        return round((self.aciertos / self.intentos) * 100)

class Evaluacion(models.Model):
    TIPO_CHOICES = [
        ('diagnostico', 'Diagnóstico'),
        ('formativa', 'Formativa'),
        ('sumativa', 'Sumativa'),
        ('final', 'Final'),
    ]

    titulo = models.CharField(max_length=300)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=100)
    nivel_requerido = models.IntegerField(default=1)
    puntos_base = models.IntegerField(default=10)
    duracion_minutos = models.IntegerField(default=30)
    preguntas = models.JSONField(default=list)
    creada_en = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"

class ResultadoEvaluacion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluaciones')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    puntaje = models.IntegerField(default=0)
    respuestas = models.JSONField(default=list)
    tiempo_utilizado = models.IntegerField(default=0)
    completada = models.BooleanField(default=False)
    fecha_completada = models.DateTimeField(null=True, blank=True)
    calificacion = models.CharField(max_length=20, blank=True, null=True)
    feedback_general = models.TextField(blank=True, null=True)

    def calcular_calificacion(self):
        if self.puntaje >= 90:
            return 'Excelente'
        elif self.puntaje >= 75:
            return 'Bueno'
        elif self.puntaje >= 60:
            return 'Regular'
        else:
            return 'Necesita Mejorar'

class Logro(models.Model):
    TIPO_CHOICES = [
        ('insignia', 'Insignia'),
        ('medalla', 'Medalla'),
        ('estrella', 'Estrella'),
        ('certificacion', 'Certificación'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    icono = models.CharField(max_length=100, help_text="Clase de Font Awesome o emoji")
    color = models.CharField(max_length=50, default='gold')
    puntos_requeridos = models.IntegerField(default=0)
    nivel_requerido = models.IntegerField(default=1)
    categoria_requerida = models.CharField(max_length=100, blank=True, null=True)
    ejercicios_completados_requeridos = models.IntegerField(default=0)
    tasa_aciertos_requerida = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class LogroObtenido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logros_obtenidos')
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE)
    fecha_obtenida = models.DateTimeField(auto_now_add=True)
    notificado = models.BooleanField(default=False)

class Certificacion(models.Model):
    NIVEL_CHOICES = [
        ('bronce', 'Bronce'),
        ('plata', 'Plata'),
        ('oro', 'Oro'),
        ('platino', 'Platino'),
        ('diamante', 'Diamante'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    requisitos = models.JSONField(default=dict)
    imagen = models.CharField(max_length=200, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.nivel}"

class CertificacionObtenida(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificaciones_obtenidas')
    certificacion = models.ForeignKey(Certificacion, on_delete=models.CASCADE)
    fecha_obtenida = models.DateTimeField(auto_now_add=True)
    codigo_verificacion = models.CharField(max_length=100, unique=True)
    url_verificacion = models.URLField(blank=True, null=True)

class EjercicioLinguistico(models.Model):
    titulo = models.CharField(max_length=500, verbose_name="Título")
    contenido = models.JSONField(default=dict, verbose_name="Contenido completo")
    categoria = models.CharField(max_length=200, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    nivel = models.IntegerField(default=1, help_text="Nivel de dificultad")
    puntos = models.IntegerField(default=10)
    # Motor adaptativo (ver docs/adaptive_engine.md)
    es_adaptativo = models.BooleanField(default=False, db_index=True)
    es_redaccion = models.BooleanField(default=False, db_index=True)
    tipo_redaccion = models.CharField(max_length=30, blank=True, default="")
    tecnica = models.CharField(max_length=100, blank=True, default="")
    categoria_error = models.CharField(max_length=100, blank=True, default="")
    idioma = models.CharField(max_length=2, blank=True, default="ES")
    archivo_origen = models.CharField(max_length=300, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ejercicio Lingüístico"
        verbose_name_plural = "Ejercicios Lingüísticos"
        ordering = ['-creado_en']

    def __str__(self):
        return self.titulo[:100]

class TecnicaLinguistica(models.Model):
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=200, blank=True, null=True)
    nivel = models.IntegerField(default=1)
    archivo_origen = models.CharField(max_length=300, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Técnica Lingüística"
        verbose_name_plural = "Técnicas Lingüísticas"

    def __str__(self):
        return self.nombre[:100]

class ContenidoJSON(models.Model):
    nombre = models.CharField(max_length=300)
    archivo = models.CharField(max_length=300)
    datos = models.JSONField(default=dict)
    categoria = models.CharField(max_length=200, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contenido JSON"
        verbose_name_plural = "Contenidos JSON"

    def __str__(self):
        return self.nombre[:100]


# ============================================================
# RECURSO (archivos HTML/JSON interactivos)
# ============================================================
class Recurso(models.Model):
    """Archivo de recurso educativo (HTML interactivo, JSON, etc.)."""
    nombre = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    archivo = models.CharField(max_length=500, help_text="Ruta relativa a la carpeta de recursos")
    categoria = models.CharField(max_length=100, db_index=True)
    extension = models.CharField(max_length=10, db_index=True)
    tamaño_bytes = models.BigIntegerField(default=0)
    fecha_mod = models.DateTimeField(null=True, blank=True)
    curso = models.ForeignKey(
        'core.Curso', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )

    modulo = models.ForeignKey(
        'core.Modulo', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    leccion = models.ForeignKey(
        'core.Leccion', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    evaluacion_curso = models.ForeignKey(
        'core.EvaluacionCurso', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    ejercicio = models.ForeignKey(
        'core.EjercicioLinguistico', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='recursos',
    )
    orden = models.PositiveIntegerField(default=0)
    destacado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["categoria", "nombre"]
        indexes = [
            models.Index(fields=["categoria"]),
            models.Index(fields=["extension"]),
        ]

    def __str__(self):
        return self.nombre

    @property
    def tamaño_legible(self):
        b = self.tamaño_bytes
        for u in ["B", "KB", "MB", "GB"]:
            if b < 1024:
                return f"{b:.1f} {u}"
            b /= 1024
        return f"{b:.1f} TB"

    @property
    def icono(self):
        return {
            "html": "fa-file-code text-danger",
            "htm": "fa-file-code text-danger",
            "json": "fa-file-code text-warning",
            "md": "fa-file-alt text-info",
            "txt": "fa-file-alt text-secondary",
            "docx": "fa-file-word text-primary",
            "py": "fa-file-code text-success",
            "js": "fa-file-code text-warning",
            "css": "fa-file-code text-info",
            "sql": "fa-database text-secondary",
            "sh": "fa-terminal text-dark",
            "csv": "fa-file-csv text-success",
            "xml": "fa-file-code text-info",
            "pdf": "fa-file-pdf text-danger",
        }.get(self.extension, "fa-file text-muted")

    @property
    def color_badge(self):
        return {
            "Súper Cuaderno": "primary",
            "Cuaderno": "info",
            "Flota": "warning",
            "Vector": "success",
            "Técnicas": "danger",
            "Scriptorium": "dark",
            "Datos JSON": "secondary",
        }.get(self.categoria, "secondary")


# Forzar a Django a cargar los modelos de cursos al iniciar
from . import models_cursos  # noqa: F401,E402
from . import models_preguntas  # noqa: F401,E402
from . import models_adaptativos  # noqa: F401,E402
from . import models_redaccion  # noqa: F401,E402
from .models_redaccion import EvaluacionRedaccion  # noqa: F401,E402
