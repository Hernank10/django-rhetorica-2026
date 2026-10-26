"""Asigna certificaciones a 45 estudiantes (est001-est045).

Idempotente: usa (user, certificacion) como lookup. Correr N veces no duplica.
Codigo de verificacion deterministico: CERT-{user_id}-{cert_id}.
"""
import os
import sys
import random
from pathlib import Path
from datetime import timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")

import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from core.models import CertificacionObtenida

# Import defensivo de Certificacion
try:
    from core.models import Certificacion
except ImportError:
    try:
        from core.models_cursos import Certificacion
    except ImportError:
        print("[!] Certificacion no encontrado. Pega el modulo donde vive.")
        sys.exit(1)

random.seed(42)


def main():
    print("=" * 65)
    print("SEED: 45 ESTUDIANTES CERTIFICADOS")
    print("=" * 65)

    # 1. Estudiantes objetivo
    estudiantes = list(
        User.objects.filter(
            username__startswith="est",
            is_staff=False,
            is_superuser=False,
        ).order_by("username")[:45]
    )
    print(f"\n[1/3] Estudiantes objetivo: {len(estudiantes)}")
    if estudiantes:
        print(f"  Primero: {estudiantes[0].username}")
        print(f"  Ultimo:  {estudiantes[-1].username}")

    if len(estudiantes) < 45:
        print(f"[!] Solo hay {len(estudiantes)} estudiantes. Corre seed_test_users.py primero.")
        return

    # 2. Certificaciones disponibles
    certs = list(Certificacion.objects.all())
    print(f"\n[2/3] Certificaciones disponibles: {len(certs)}")

    if not certs:
        print("[!] No hay Certificacion en DB.")
        print("    Pega los campos del modelo Certificacion para diagnosticar.")
        return

    for c in certs[:3]:
        nombre = getattr(c, "nombre", getattr(c, "titulo", str(c)))
        print(f"  - id={c.id} {nombre[:60]}")

    # 3. Asignar certificaciones
    print(f"\n[3/3] Asignando certificaciones...")
    creadas = 0
    existentes = 0

    for idx, student in enumerate(estudiantes, 1):
        k = random.randint(1, min(3, len(certs)))
        seleccion = random.sample(certs, k=k)

        for cert in seleccion:
            codigo = f"CERT-{student.id:04d}-{cert.id:04d}"
            fecha = timezone.now() - timedelta(days=random.randint(30, 365))
            url = f"/certificados/verificar/{codigo}/"

            existing = CertificacionObtenida.objects.filter(
                user=student, certificacion=cert
            ).first()

            if existing:
                existentes += 1
            else:
                CertificacionObtenida.objects.create(
                    user=student,
                    certificacion=cert,
                    fecha_obtenida=fecha,
                    codigo_verificacion=codigo,
                    url_verificacion=url,
                )
                creadas += 1

        if idx % 15 == 0 or idx == len(estudiantes):
            print(f"  [OK] {idx}/{len(estudiantes)} estudiantes procesados")

    # Resumen
    print("\n" + "=" * 65)
    print("RESUMEN")
    print("=" * 65)
    print(f"  Creadas:      {creadas}")
    print(f"  Ya existian:  {existentes}")
    print(f"  Total en DB:  {CertificacionObtenida.objects.count()}")

    # Verificacion
    print(f"\n=== VERIFICACION (muestra) ===")
    for student in estudiantes[:3]:
        qs = CertificacionObtenida.objects.filter(user=student)
        print(f"\n  {student.username}: {qs.count()} certificaciones")
        for c in qs[:3]:
            nombre = getattr(c.certificacion, "nombre",
                             getattr(c.certificacion, "titulo", "?"))
            print(f"    - {nombre[:45]:45s} {c.codigo_verificacion} {c.fecha_obtenida.date()}")


if __name__ == "__main__":
    main()