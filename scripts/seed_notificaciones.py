"""Poblar notificaciones para todos los estudiantes de prueba.

Estrategia:
- Ultimas 2 lecciones completadas por estudiante
- Todas sus certificaciones obtenidas
- Todos sus logros obtenidos
- 1 notif de sistema "bienvenida" (solo si no tiene actividad)

Idempotente via `referencia`. DRY_RUN por defecto.
"""
import os

from django.apps import apps

APPLY = os.environ.get("NOTIF_APPLY", "0") == "1"

Notificacion = apps.get_model("core", "Notificacion")
ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")
CertificacionObtenida = apps.get_model("core", "CertificacionObtenida")
LogroObtenido = apps.get_model("core", "LogroObtenido")
User = apps.get_model("auth", "User")

from core.services.notificaciones import crear_notificacion

estudiantes = User.objects.filter(groups__name="Estudiante").order_by("username")
print(f"Estudiantes a procesar: {estudiantes.count()}")

creadas = 0
existentes = 0
sin_actividad = 0

for est in estudiantes:
    # 1. Ultimas 2 lecciones completadas
    progresos = list(
        ProgresoUsuario.objects.filter(usuario=est, completado=True)
        .select_related("leccion__modulo__curso")
        .order_by("-completado_en")[:2]
    )
    for p in progresos:
        ref = f"seed_leccion_{p.leccion_id}_{est.id}"
        if APPLY:
            _, created = crear_notificacion(
                user=est,
                tipo="leccion_completada",
                titulo=f"Leccion completada: {p.leccion.titulo[:60]}",
                mensaje=f"Terminaste '{p.leccion.titulo[:80]}' del curso '{p.leccion.modulo.curso.titulo}'",
                url_destino=f"/cursos/{p.leccion.modulo.curso.slug}/",
                icono="check-circle",
                referencia=ref,
            )
            if created:
                creadas += 1
            else:
                existentes += 1
        else:
            if Notificacion.objects.filter(user=est, referencia=ref).exists():
                existentes += 1
            else:
                creadas += 1

    # 2. Certificaciones
    for cert in CertificacionObtenida.objects.filter(user=est).select_related("certificacion"):
        ref = f"seed_cert_{cert.certificacion_id}_{est.id}"
        if APPLY:
            _, created = crear_notificacion(
                user=est,
                tipo="certificacion",
                titulo=f"Certificacion obtenida: {cert.certificacion.nombre[:60]}",
                mensaje=f"Obtuviste la certificacion '{cert.certificacion.nombre}' nivel {cert.certificacion.get_nivel_display()}",
                url_destino="/estudiante/certificados/",
                icono="award",
                referencia=ref,
            )
            if created:
                creadas += 1
            else:
                existentes += 1
        else:
            if Notificacion.objects.filter(user=est, referencia=ref).exists():
                existentes += 1
            else:
                creadas += 1

    # 3. Logros (max 3 por estudiante)
    for logro in LogroObtenido.objects.filter(user=est).select_related("logro")[:3]:
        ref = f"seed_logro_{logro.logro_id}_{est.id}"
        if APPLY:
            _, created = crear_notificacion(
                user=est,
                tipo="logro",
                titulo=f"Logro: {logro.logro.nombre[:60]}",
                mensaje=f"Desbloqueaste el logro '{logro.logro.nombre}'",
                url_destino="/estudiante/logros/",
                icono="star",
                referencia=ref,
            )
            if created:
                creadas += 1
            else:
                existentes += 1
        else:
            if Notificacion.objects.filter(user=est, referencia=ref).exists():
                existentes += 1
            else:
                creadas += 1

    # 4. Fallback: si no tiene ninguna notif, crear bienvenida
    tiene_algo = (
        progresos or
        CertificacionObtenida.objects.filter(user=est).exists() or
        LogroObtenido.objects.filter(user=est).exists()
    )
    if not tiene_algo:
        sin_actividad += 1
        ref = f"seed_bienvenida_{est.id}"
        if APPLY:
            _, created = crear_notificacion(
                user=est,
                tipo="sistema",
                titulo="Bienvenido a Rhetorica+",
                mensaje=f"Hola {est.first_name or est.username}, explora los cursos disponibles y comienza tu aprendizaje.",
                url_destino="/cursos/",
                icono="bell",
                referencia=ref,
            )
            if created:
                creadas += 1
            else:
                existentes += 1
        else:
            if Notificacion.objects.filter(user=est, referencia=ref).exists():
                existentes += 1
            else:
                creadas += 1

# Resumen
print(f"\n=== RESUMEN ===")
print(f"Notificaciones {'creadas' if APPLY else 'que se crearian'}: {creadas}")
print(f"Ya existentes (skip): {existentes}")
print(f"Estudiantes sin actividad (bienvenida): {sin_actividad}")

if APPLY:
    total_db = Notificacion.objects.count()
    print(f"\nTotal notifs en DB: {total_db}")

    print("\n=== 3 muestras reales ===")
    for n in Notificacion.objects.filter(tipo="certificacion").order_by("-id")[:1]:
        print(f"  [cert] {n.user.username}: {n.titulo[:60]}")
    for n in Notificacion.objects.filter(tipo="leccion_completada").order_by("-id")[:1]:
        print(f"  [lec] {n.user.username}: {n.titulo[:60]}")
    for n in Notificacion.objects.filter(tipo="logro").order_by("-id")[:1]:
        print(f"  [logro] {n.user.username}: {n.titulo[:60]}")

    print("\n=== Distribucion por tipo ===")
    from django.db.models import Count
    for d in Notificacion.objects.values("tipo").annotate(n=Count("id")).order_by("-n"):
        print(f"  {d['tipo']:25s} {d['n']:5d}")

    print("\n=== Top 5 usuarios con mas notifs ===")
    for d in Notificacion.objects.values("user__username").annotate(n=Count("id")).order_by("-n")[:5]:
        print(f"  {d['user__username']:15s} {d['n']:3d} notifs")
else:
    print("\n[DRY_RUN] Aplicar: $env:NOTIF_APPLY='1'")