"""Data migration: certificación Recorrido MCER + 6 logros MCER para 45 estudiantes demo.

- Idempotente (get_or_create).
- Se aplica en local Y en producción (Render) vía `manage.py migrate`.
"""
import uuid
from django.db import migrations
from django.utils import timezone


def seed_mcer(apps, schema_editor):
    Certificacion         = apps.get_model("core", "Certificacion")
    CertificacionObtenida = apps.get_model("core", "CertificacionObtenida")
    Logro                 = apps.get_model("core", "Logro")
    LogroObtenido         = apps.get_model("core", "LogroObtenido")
    TecnicaGramatical     = apps.get_model("core", "TecnicaGramatical")
    ProgresoGramatical    = apps.get_model("core", "ProgresoGramatical")
    User                  = apps.get_model("auth", "User")

    # 1. Certificación MCER
    cert, _ = Certificacion.objects.get_or_create(
        nombre="Recorrido MCER A1-C2",
        defaults={
            "descripcion": "Completó el recorrido completo del MCER (A1-C2) con 610 técnicas dominadas.",
            "nivel": "avanzado",
            "requisitos": {"tecnicas_mcer": 610, "niveles": ["A1", "A2", "B1", "B2", "C1", "C2"]},
            "activa": True,
        },
    )

    # 2. Logros MCER (6 escalones)
    logros_spec = [
        {"nombre": "Primera técnica MCER", "descripcion": "Domina tu primera técnica del MCER.",
         "tipo": "insignia", "icono": "🌱", "color": "#10b981",
         "nivel_requerido": 1, "categoria_requerida": None,
         "puntos_requeridos": 0, "ejercicios_completados_requeridos": 0, "tasa_aciertos_requerida": 0.0},
        {"nombre": "Aprendiz MCER", "descripcion": "Domina 50 técnicas del MCER.",
         "tipo": "insignia", "icono": "📖", "color": "#3b82f6",
         "nivel_requerido": 1, "categoria_requerida": None,
         "puntos_requeridos": 0, "ejercicios_completados_requeridos": 0, "tasa_aciertos_requerida": 0.0},
        {"nombre": "B1 alcanzado", "descripcion": "Domina las 310 técnicas MCER hasta B1.",
         "tipo": "insignia", "icono": "🎯", "color": "#8b5cf6",
         "nivel_requerido": 1, "categoria_requerida": None,
         "puntos_requeridos": 0, "ejercicios_completados_requeridos": 0, "tasa_aciertos_requerida": 0.0},
        {"nombre": "B2 alcanzado", "descripcion": "Domina las 410 técnicas MCER hasta B2.",
         "tipo": "insignia", "icono": "🚀", "color": "#ec4899",
         "nivel_requerido": 1, "categoria_requerida": None,
         "puntos_requeridos": 0, "ejercicios_completados_requeridos": 0, "tasa_aciertos_requerida": 0.0},
        {"nombre": "C1 alcanzado", "descripcion": "Domina las 510 técnicas MCER hasta C1.",
         "tipo": "insignia", "icono": "⭐", "color": "#f59e0b",
         "nivel_requerido": 1, "categoria_requerida": None,
         "puntos_requeridos": 0, "ejercicios_completados_requeridos": 0, "tasa_aciertos_requerida": 0.0},
        {"nombre": "Recorrido MCER completado", "descripcion": "Has completado el recorrido MCER A1-C2 con 610 técnicas dominadas.",
         "tipo": "insignia", "icono": "🎓", "color": "#8b5cf6",
         "nivel_requerido": 1, "categoria_requerida": None,
         "puntos_requeridos": 0, "ejercicios_completados_requeridos": 0, "tasa_aciertos_requerida": 0.0},
    ]
    logros = []
    for spec in logros_spec:
        l, _ = Logro.objects.get_or_create(nombre=spec["nombre"], defaults=spec)
        logros.append(l)

    # 3. Técnicas MCER (guard)
    mcer_ids = list(
        TecnicaGramatical.objects
        .filter(modulo__in=["a1", "a2", "b1", "b2", "c1", "c2"])
        .values_list("id", flat=True)
    )
    if len(mcer_ids) != 610:
        return

    # 4. Usuarios demo
    estudiantes = list(
        User.objects.filter(username__startswith="testest").order_by("username")[:45]
    )
    if len(estudiantes) < 45:
        return

    # 5. Otorgar cert + los 6 logros a los 45
    now = timezone.now()
    for student in estudiantes:
        CertificacionObtenida.objects.get_or_create(
            user=student, certificacion=cert,
            defaults={
                "fecha_obtenida": now,
                "codigo_verificacion": f"MCER-{student.username.upper()}-{uuid.uuid4().hex[:12]}",
                "url_verificacion": f"/verificar/{student.username}/mcer/",
            },
        )
        for logro in logros:
            LogroObtenido.objects.get_or_create(
                user=student, logro=logro,
                defaults={"fecha_obtenida": now, "notificado": False},
            )

    # 6. Backfill ProgresoGramatical (no destructivo)
    for student in estudiantes:
        existing = set(
            ProgresoGramatical.objects
            .filter(usuario=student, tecnica_id__in=mcer_ids)
            .values_list("tecnica_id", flat=True)
        )
        to_create = [
            ProgresoGramatical(usuario=student, tecnica_id=tid, estado="dominada", intentos=1)
            for tid in mcer_ids if tid not in existing
        ]
        if to_create:
            ProgresoGramatical.objects.bulk_create(to_create, batch_size=500)
        ProgresoGramatical.objects.filter(
            usuario=student, tecnica_id__in=mcer_ids,
        ).exclude(estado="dominada").update(estado="dominada", intentos=1)


def reverse_mcer(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0022_a1_b1_modulo"),  # ← 4 CEROS, nombre exacto del archivo
    ]
    operations = [
        migrations.RunPython(seed_mcer, reverse_mcer),
    ]
