"""Migration 025: seed Respuesta + ProgresoUsuario para 45 estudiantes demo.

- Respuesta: 100 por estudiante (~80% correctas, últimos 30 días) → stats reales
- ProgresoUsuario: 15 lecciones por estudiante (últimos 30 días) → actividad + cursos
- Idempotente: skip si el estudiante ya tiene datos.
"""
import random
from datetime import timedelta

from django.db import migrations
from django.utils import timezone


def _has_field(model, name):
    try:
        model._meta.get_field(name)
        return True
    except Exception:
        return False


def seed_stats(apps, schema_editor):
    Respuesta = apps.get_model("core", "Respuesta")
    ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
    EjercicioGramatical = apps.get_model("core", "EjercicioGramatical")
    Leccion = apps.get_model("core", "Leccion")
    User = apps.get_model("auth", "User")

    students = list(
        User.objects.filter(username__startswith="testest").order_by("username")[:45]
    )
    if len(students) < 45:
        print(f"[SKIP] Solo hay {len(students)} testest users (necesito 45)")
        return

    ej_ids = list(EjercicioGramatical.objects.values_list("id", flat=True))
    if not ej_ids:
        print("[SKIP] Sin EjercicioGramatical")
        return

    tipos_pool = [
        "multiple_choice",
        "completar",
        "ordenar",
        "relacionar",
        "verificar",
        "correccion",
    ]

    lecciones = list(Leccion.objects.all()[:30])
    now = timezone.now()

    # ─── Respuesta: 100 por estudiante ───
    resp_batch = []
    students_with_resp = 0
    for student in students:
        if Respuesta.objects.filter(user=student).exists():
            students_with_resp += 1
            continue
        for _ in range(100):
            es_correcta = random.random() < 0.8
            fecha = now - timedelta(
                days=random.randint(0, 29),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )
            resp_batch.append(
                Respuesta(
                    user=student,
                    tipo_ejercicio=random.choice(tipos_pool),
                    item_id=random.choice(ej_ids),
                    respuesta_usuario="Opción A" if es_correcta else "Opción B",
                    es_correcta=es_correcta,
                    puntuacion=4 if es_correcta else 0,
                    tiempo_segundos=random.randint(15, 60),
                    fecha=fecha,
                    intento_numero=1,
                    feedback=None,
                )
            )

    if resp_batch:
        Respuesta.objects.bulk_create(resp_batch, batch_size=500)
        print(f"[OK] Respuesta: {len(resp_batch)} nuevas ({students_with_resp} students ya tenían)")
    else:
        print("[SKIP] Respuesta: todos los students ya tenían datos")

    # ─── ProgresoUsuario: 15 lecciones por estudiante ───
    if not lecciones:
        print("[SKIP] ProgresoUsuario: no hay Leccion en DB")
        return

    prog_batch = []
    students_with_prog = 0
    for student in students:
        if ProgresoUsuario.objects.filter(usuario=student).exists():
            students_with_prog += 1
            continue
        sample = random.sample(lecciones, min(15, len(lecciones)))
        for leccion in sample:
            fecha = now - timedelta(days=random.randint(0, 29))
            kwargs = {
                "usuario": student,
                "leccion": leccion,
                "completado": True,
            }
            if _has_field(ProgresoUsuario, "completado_en"):
                kwargs["completado_en"] = fecha
            if _has_field(ProgresoUsuario, "ultima_actividad"):
                kwargs["ultima_actividad"] = fecha
            if _has_field(ProgresoUsuario, "puntaje_obtenido"):
                kwargs["puntaje_obtenido"] = random.randint(60, 100)
            prog_batch.append(ProgresoUsuario(**kwargs))

    if prog_batch:
        ProgresoUsuario.objects.bulk_create(prog_batch, batch_size=500)
        print(f"[OK] ProgresoUsuario: {len(prog_batch)} nuevos ({students_with_prog} students ya tenían)")
    else:
        print("[SKIP] ProgresoUsuario: todos los students ya tenían datos")


def reverse_stats(apps, schema_editor):
    # No borrar datos en rollback (idempotente)
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "024_logro_points"),
    ]
    operations = [
        migrations.RunPython(seed_stats, reverse_stats),
    ]
