"""Seed notificaciones para los 9 profesores: actividad de sus estudiantes.

Idempotente via `referencia`. DRY_RUN por defecto.

Estrategia por profesor:
- 5 últimos progresos (lecciones completadas) de sus cursos
- 5 últimas certs de estudiantes en sus cursos
- 5 últimos logros de estudiantes en sus cursos
- 1 bienvenida
Total: ~16 notifs por profesor * 9 = ~144 notifs
"""
import os
from django.apps import apps
from django.db.models import Count

APPLY = os.environ.get("PROF_NOTIF_APPLY", "0") == "1"

Notificacion = apps.get_model("core", "Notificacion")
Curso = apps.get_model("core", "Curso")
ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
CertificacionObtenida = apps.get_model("core", "CertificacionObtenida")
LogroObtenido = apps.get_model("core", "LogroObtenido")
User = apps.get_model("auth", "User")

from core.services.notificaciones import crear_notificacion

LIMIT = 5
profesores = User.objects.filter(groups__name="Profesor").order_by("username")
print(f"Profesores: {profesores.count()}")

creadas = 0
existentes = 0
sin_curso = 0

def _check_or_create(prof, ref, kwargs):
    """Crea o verifica existencia. Retorna (ok, created)."""
    global creadas, existentes
    if APPLY:
        _, created = crear_notificacion(user=prof, referencia=ref, **kwargs)
        if created:
            creadas += 1
            return True, True
        existentes += 1
        return True, False
    else:
        if Notificacion.objects.filter(user=prof, referencia=ref).exists():
            existentes += 1
            return True, False
        creadas += 1
        return True, True

for prof in profesores:
    mis_cursos = Curso.objects.filter(profesor_asignado=prof)
    if not mis_cursos.exists():
        sin_curso += 1
        continue

    mis_estudiantes = User.objects.filter(
        progreso_lecciones__leccion__modulo__curso__in=mis_cursos
    ).distinct()

    # 1. Últimos progresos
    for prog in (
        ProgresoUsuario.objects.filter(
            leccion__modulo__curso__in=mis_cursos, completado=True
        )
        .select_related("usuario", "leccion__modulo__curso")
        .order_by("-completado_en")[:LIMIT]
    ):
        _check_or_create(
            prof,
            f"seed_prof_prog_{prog.id}",
            dict(
                tipo="estudiante_leccion",
                titulo=f"{prog.usuario.username} completó: {prog.leccion.titulo[:50]}",
                mensaje=f"Curso: {prog.leccion.modulo.curso.titulo}",
                url_destino=f"/profesor/estudiantes/{prog.usuario_id}/",
                icono="user-check",
            ),
        )

    # 2. Certs
    for cert in (
        CertificacionObtenida.objects.filter(user__in=mis_estudiantes)
        .select_related("user", "certificacion")
        .order_by("-fecha_obtenida")[:LIMIT]
    ):
        _check_or_create(
            prof,
            f"seed_prof_cert_{cert.id}",
            dict(
                tipo="estudiante_cert",
                titulo=f"{cert.user.username} obtuvo: {cert.certificacion.nombre[:50]}",
                mensaje=f"Nivel {cert.certificacion.get_nivel_display()}",
                url_destino=f"/profesor/estudiantes/{cert.user_id}/",
                icono="award",
            ),
        )

    # 3. Logros
    for logro in (
        LogroObtenido.objects.filter(user__in=mis_estudiantes)
        .select_related("user", "logro")
        .order_by("-fecha_obtenida")[:LIMIT]
    ):
        _check_or_create(
            prof,
            f"seed_prof_logro_{logro.id}",
            dict(
                tipo="estudiante_logro",
                titulo=f"{logro.user.username} desbloqueó: {logro.logro.nombre[:50]}",
                mensaje=f"Tipo: {logro.logro.get_tipo_display()}",
                url_destino=f"/profesor/estudiantes/{logro.user_id}/",
                icono="star",
            ),
        )

    # 4. Bienvenida
    _check_or_create(
        prof,
        f"seed_prof_bienvenida_{prof.id}",
        dict(
            tipo="sistema",
            titulo=f"Bienvenido profesor {prof.get_full_name() or prof.username}",
            mensaje="Revisa las últimas actividades de tus estudiantes",
            url_destino="/profesor/estudiantes/metricas/",
            icono="chalkboard-teacher",
        ),
    )

print(f"\n=== RESUMEN ===")
print(f"Notifs {'creadas' if APPLY else 'que se crearian'}: {creadas}")
print(f"Ya existentes (skip): {existentes}")
print(f"Profesores sin curso asignado: {sin_curso}")

if APPLY:
    total = Notificacion.objects.count()
    print(f"\nTotal notifs en DB: {total}")

    print("\n=== Nuevas por tipo (de profesores) ===")
    for d in (
        Notificacion.objects.filter(
            tipo__in=["estudiante_leccion", "estudiante_cert", "estudiante_logro"]
        ).values("tipo").annotate(n=Count("id")).order_by("-n")
    ):
        print(f"  {d['tipo']:25s} {d['n']}")

    print("\n=== Notifs por profesor ===")
    for p in profesores:
        n = Notificacion.objects.filter(user=p).count()
        print(f"  {p.username:10s} {n:3d} notifs")

    print("\n=== 3 muestras ===")
    for n in Notificacion.objects.filter(tipo="estudiante_leccion").order_by("-id")[:2]:
        print(f"  [{n.tipo}] {n.user.username}: {n.titulo[:60]}")
    for n in Notificacion.objects.filter(tipo="estudiante_cert").order_by("-id")[:1]:
        print(f"  [{n.tipo}] {n.user.username}: {n.titulo[:60]}")
else:
    print("\n[DRY_RUN] Aplicar: $env:PROF_NOTIF_APPLY='1'")