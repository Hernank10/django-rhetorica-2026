"""Genera datos sinteticos realistas para analytics."""
import os
import random
import sys
from datetime import timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings")
import django
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import (
    Respuesta, Logro, LogroObtenido,
    Certificacion, CertificacionObtenida,
)
from core.models_adaptativos import HistorialErrorSintactico

User = get_user_model()

CATEGORIAS = [
    "multiple_choice", "completar", "correccion",
    "verificar", "ordenar", "relacionar", "explicar",
]

CATEGORIAS_ERROR_LATIN = [
    "declinacion_3_consonantica",
    "ablativo_instrumental",
    "ablativo_locativo",
    "genitivo_partitivo",
    "cum_subjuntivo_imperfecto",
]

random.seed(42)


def crear_usuarios():
    print("[1/4] Creando usuarios...")
    for i in range(1, 6):
        username = f"prof_analytics_{i:02d}"
        User.objects.get_or_create(
            username=username,
            defaults={"email": f"{username}@test.com", "is_staff": True},
        )
    for i in range(1, 51):
        username = f"est_analytics_{i:03d}"
        User.objects.get_or_create(
            username=username,
            defaults={"email": f"{username}@test.com"},
        )
    print(f"      Profesores: {User.objects.filter(username__startswith='prof_analytics').count()}")
    print(f"      Estudiantes: {User.objects.filter(username__startswith='est_analytics').count()}")


def crear_respuestas():
    print("[2/4] Creando Respuesta (ultimas 8 semanas)...")
    estudiantes = list(User.objects.filter(username__startswith="est_analytics"))
    if not estudiantes:
        print("      [!] No hay estudiantes, saltando")
        return

    ahora = timezone.now()
    total = 0
    for est in estudiantes:
        n = random.randint(20, 60)
        for _ in range(n):
            dias_atras = random.randint(0, 55)
            horas = random.randint(0, 23)
            fecha = ahora - timedelta(days=dias_atras, hours=horas)
            es_correcta = random.random() < 0.65
            Respuesta.objects.create(
                user=est,
                tipo_ejercicio=random.choice(CATEGORIAS),
                item_id=random.randint(1, 200),
                respuesta_usuario="x",
                es_correcta=es_correcta,
                puntuacion=10 if es_correcta else 0,
                tiempo_segundos=random.randint(5, 120),
                fecha=fecha,
                intento_numero=1,
            )
            total += 1
    print(f"      Creadas: {total} Respuesta")


def crear_logros_y_certs():
    print("[3/4] Creando LogroObtenido / CertificacionObtenida...")
    estudiantes = list(User.objects.filter(username__startswith="est_analytics"))
    logros = list(Logro.objects.all()[:5])
    certs = list(Certificacion.objects.all()[:3])

    if not logros and not certs:
        print("      [!] No hay Logro/Certificacion en BD, saltando")
        return

    n_logros = 0
    n_certs = 0
    for est in random.sample(estudiantes, min(20, len(estudiantes))):
        for logro in random.sample(logros, min(2, len(logros))):
            LogroObtenido.objects.get_or_create(user=est, logro=logro)
            n_logros += 1
        if certs and random.random() < 0.3:
            cert = random.choice(certs)
            CertificacionObtenida.objects.get_or_create(
                user=est, certificacion=cert,
                defaults={"codigo_verificacion": f"VER-{est.id}-{cert.id}-{random.randint(1000,9999)}"},
            )
            n_certs += 1
    print(f"      LogroObtenido: {n_logros}  CertificacionObtenida: {n_certs}")


def crear_historial_errores():
    print("[4/4] Creando HistorialErrorSintactico...")
    estudiantes = list(User.objects.filter(username__startswith="est_analytics"))
    total = 0
    for est in random.sample(estudiantes, min(15, len(estudiantes))):
        n = random.randint(1, 4)
        for _ in range(n):
            cat = random.choice(CATEGORIAS_ERROR_LATIN)
            HistorialErrorSintactico.objects.get_or_create(
                estudiante=est,
                idioma="LA",
                categoria_gramatical=cat,
                patron_error="",
                defaults={"frecuencia": random.randint(2, 8)},
            )
            total += 1
    print(f"      Creados: {total} HistorialErrorSintactico")


def main():
    print("=" * 60)
    print("SUPER-GENERADOR DE DATOS PARA ANALYTICS")
    print("=" * 60)
    crear_usuarios()
    crear_respuestas()
    crear_logros_y_certs()
    crear_historial_errores()
    print()
    print("=" * 60)
    print("LISTO. Proximos pasos:")
    print("  1. manage.py backfill_progreso")
    print("  2. pytest -q  (verificar que nada rompio)")
    print("=" * 60)


if __name__ == "__main__":
    main()