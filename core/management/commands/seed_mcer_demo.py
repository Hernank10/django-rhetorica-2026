"""Seed idempotente del recorrido MCER demo.

Reemplaza migrations 023/024/025 para producción, donde las migrations
corren ANTES de los seeds de técnicas/usuarios y fallan por guard.
Puede ejecutarse en cualquier momento; no rompe si ya está aplicado.
"""
import random
import uuid
from datetime import timedelta

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    help = "Seed idempotente: cert MCER + 6 logros + 610 técnicas + 100 respuestas x 45 students"

    def handle(self, *args, **options):
        Certificacion         = apps.get_model("core", "Certificacion")
        CertificacionObtenida = apps.get_model("core", "CertificacionObtenida")
        Logro                 = apps.get_model("core", "Logro")
        LogroObtenido         = apps.get_model("core", "LogroObtenido")
        TecnicaGramatical     = apps.get_model("core", "TecnicaGramatical")
        ProgresoGramatical    = apps.get_model("core", "ProgresoGramatical")
        Respuesta             = apps.get_model("core", "Respuesta")
        ProgresoUsuario       = apps.get_model("core", "ProgresoUsuario")
        EjercicioGramatical   = apps.get_model("core", "EjercicioGramatical")
        Leccion               = apps.get_model("core", "Leccion")
        User                  = apps.get_model("auth", "User")

        # ─── 0. Pre-flight ───
        mcer_ids = list(
            TecnicaGramatical.objects
            .filter(modulo__in=["a1", "a2", "b1", "b2", "c1", "c2"])
            .values_list("id", flat=True)
        )
        estudiantes = list(
            User.objects.filter(username__startswith="testest").order_by("username")[:45]
        )
        self.stdout.write(f"MCER técnicas: {len(mcer_ids)}/610")
        self.stdout.write(f"testest users: {len(estudiantes)}/45")
        if len(mcer_ids) < 610:
            self.stdout.write(self.style.WARNING(
                f"[WARN] Faltan técnicas MCER. Corre RUN_SEEDS primero. "
                f"Continuo con cert+logros (no dependen de técnicas)."
            ))

        # ─── 1. Certificación MCER ───
        cert, created = Certificacion.objects.get_or_create(
            nombre="Recorrido MCER A1-C2",
            defaults={
                "descripcion": "Completó el recorrido MCER (A1-C2) con 610 técnicas dominadas.",
                "nivel": "avanzado",
                "requisitos": {"tecnicas_mcer": 610, "niveles": ["A1","A2","B1","B2","C1","C2"]},
                "activa": True,
            },
        )
        self.stdout.write(f"  cert: {'creado' if created else 'existia'} (id={cert.id})")

        # ─── 2. Logros MCER (con puntos 10/20/30/40/50/100) ───
        logros_spec = [
            ("Primera técnica MCER", 10,  "🌱"),
            ("Aprendiz MCER",        20,  "📖"),
            ("B1 alcanzado",         30,  "🎯"),
            ("B2 alcanzado",         40,  "🚀"),
            ("C1 alcanzado",         50,  "⭐"),
            ("Recorrido MCER completado", 100, "🎓"),
        ]
        logros = []
        for nombre, puntos, icono in logros_spec:
            l, created = Logro.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": f"Logro MCER: {nombre}",
                    "tipo": "insignia", "icono": icono, "color": "#8b5cf6",
                    "puntos_requeridos": puntos, "nivel_requerido": 1,
                    "categoria_requerida": None,
                    "ejercicios_completados_requeridos": 0,
                    "tasa_aciertos_requerida": 0.0,
                },
            )
            # Corregir puntos si existía con valor viejo (migration 024 pudo no aplicar)
            if not created and l.puntos_requeridos != puntos:
                l.puntos_requeridos = puntos
                l.save(update_fields=["puntos_requeridos"])
            logros.append(l)
        self.stdout.write(f"  logros: {len(logros)} asegurados (puntos corregidos)")

        # ─── 3. Otorgar cert + logros a estudiantes ───
        if estudiantes:
            now = timezone.now()
            nuevos_certs = nuevos_logros = 0
            with transaction.atomic():
                for student in estudiantes:
                    _, created = CertificacionObtenida.objects.get_or_create(
                        user=student, certificacion=cert,
                        defaults={
                            "fecha_obtenida": now,
                            "codigo_verificacion": f"MCER-{student.username.upper()}-{uuid.uuid4().hex[:12]}",
                            "url_verificacion": f"/verificar/{student.username}/mcer/",
                        },
                    )
                    if created: nuevos_certs += 1
                    for logro in logros:
                        _, created = LogroObtenido.objects.get_or_create(
                            user=student, logro=logro,
                            defaults={"fecha_obtenida": now, "notificado": False},
                        )
                        if created: nuevos_logros += 1
            self.stdout.write(f"  certs: {nuevos_certs} nuevos / {len(estudiantes)} total")
            self.stdout.write(f"  logros: {nuevos_logros} nuevos")

        # ─── 4. Backfill ProgresoGramatical (solo si hay 610 técnicas) ───
        if len(mcer_ids) == 610 and estudiantes:
            prog_creados = 0
            with transaction.atomic():
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
                        prog_creados += len(to_create)
                    ProgresoGramatical.objects.filter(
                        usuario=student, tecnica_id__in=mcer_ids,
                    ).exclude(estado="dominada").update(estado="dominada", intentos=1)
            self.stdout.write(f"  ProgresoGramatical: {prog_creados} nuevos")
        elif estudiantes:
            self.stdout.write(self.style.WARNING(
                f"  [SKIP] backfill MCER: faltan tecnicas ({len(mcer_ids)}/610)"
            ))

        # ─── 5. Seed Respuesta (100/estudiante) + ProgresoUsuario (15/estudiante) ───
        ej_ids = list(EjercicioGramatical.objects.values_list("id", flat=True))
        lecciones = list(Leccion.objects.all()[:30])

        if estudiantes and ej_ids:
            resp_batch = []
            for student in estudiantes:
                if Respuesta.objects.filter(user=student).exists():
                    continue
                for _ in range(100):
                    es_correcta = random.random() < 0.8
                    resp_batch.append(Respuesta(
                        user=student,
                        tipo_ejercicio=random.choice(
                            ["multiple_choice","completar","ordenar","relacionar","verificar","correccion"]
                        ),
                        item_id=random.choice(ej_ids),
                        respuesta_usuario="Opción A" if es_correcta else "Opción B",
                        es_correcta=es_correcta,
                        puntuacion=4 if es_correcta else 0,
                        tiempo_segundos=random.randint(15, 60),
                        fecha=timezone.now() - timedelta(
                            days=random.randint(0, 29), hours=random.randint(0, 23)
                        ),
                        intento_numero=1,
                        feedback=None,
                    ))
            if resp_batch:
                Respuesta.objects.bulk_create(resp_batch, batch_size=500)
                self.stdout.write(f"  Respuesta: {len(resp_batch)} nuevas")

        if estudiantes and lecciones:
            prog_batch = []
            for student in estudiantes:
                if ProgresoUsuario.objects.filter(usuario=student).exists():
                    continue
                for leccion in random.sample(lecciones, min(15, len(lecciones))):
                    fecha = timezone.now() - timedelta(days=random.randint(0, 29))
                    prog_batch.append(ProgresoUsuario(
                        usuario=student, leccion=leccion, completado=True,
                        completado_en=fecha, puntaje_obtenido=random.randint(60, 100),
                    ))
            if prog_batch:
                ProgresoUsuario.objects.bulk_create(prog_batch, batch_size=500)
                self.stdout.write(f"  ProgresoUsuario: {len(prog_batch)} nuevos")

        self.stdout.write(self.style.SUCCESS("[OK] seed_mcer_demo completado"))
