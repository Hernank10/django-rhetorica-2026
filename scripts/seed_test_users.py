"""Seed de usuarios de prueba + progreso en los 5 modulos curriculares.

Crea:
- 3 admins (superuser + is_staff)
- 9 profesores (is_staff + grupo Profesor)
- 96 estudiantes (grupo Estudiante)
- Progreso aleatorio en los 5 modulos (sintaxis, gramatica, generativa, a1, b1)
- 1 notificacion de bienvenida por estudiante

Idempotente: update_or_create para users, bulk_create con ignore_conflicts
para progreso. Correr N veces no duplica ni rompe.

Uso:
    python scripts/seed_test_users.py

Password comun para todos: test1234
"""
import os
import sys
import random
from pathlib import Path
from datetime import timedelta

# ─── Setup Django ───
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")

import django
django.setup()

from django.contrib.auth.models import User, Group
from django.utils import timezone

from core.models_gramatica import TecnicaGramatical, ProgresoGramatical

# Sintaxis usa modelos separados
try:
    from core.models_sintaxis import TecnicaSintactica, ProgresoTecnica
    HAS_SINTAXIS = True
except ImportError:
    HAS_SINTAXIS = False
    print("[!] models_sintaxis no disponible; sintaxis no se pobla")

# ─── Configuracion ───
PASSWORD = "test1234"
ADMINS = 3
PROFESORES = 9
ESTUDIANTES = 96
MODULOS = ["gramatica", "generativa", "a1", "b1"]
BATCH_SIZE = 1000

# Seed para reproducibilidad (siempre genera el mismo progreso)
random.seed(42)


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

def get_or_create_grupo(nombre):
    """Devuelve el grupo; lo crea si no existe."""
    grupo, created = Group.objects.get_or_create(name=nombre)
    if created:
        print(f"  [NEW] Grupo '{nombre}' creado")
    return grupo


def upsert_user(username, email, first_name, last_name, password,
                is_superuser=False, is_staff=False, grupos=None):
    """Crea o actualiza un usuario. Siempre resetea password (entorno dev)."""
    user, created = User.objects.update_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_superuser": is_superuser,
            "is_staff": is_staff,
            "is_active": True,
        },
    )
    # Password siempre se resetea (dev/test)
    user.set_password(password)
    user.save(update_fields=["password"])

    if grupos:
        for g in grupos:
            user.groups.add(g)

    return user, created


# ═══════════════════════════════════════════════════════════
# 1. ADMINS
# ═══════════════════════════════════════════════════════════

def crear_admins():
    print(f"\n[1/5] Creando {ADMINS} administradores...")
    admins = []
    for i in range(1, ADMINS + 1):
        user, created = upsert_user(
            username=f"admin{i:02d}",
            email=f"admin{i:02d}@rhetorica.test",
            first_name=f"Admin {i}",
            last_name="Sistema",
            password=PASSWORD,
            is_superuser=True,
            is_staff=True,
        )
        tag = "NEW" if created else "UPD"
        print(f"  [{tag}] admin{i:02d} (superuser=True)")
        admins.append(user)
    return admins


# ═══════════════════════════════════════════════════════════
# 2. PROFESORES
# ═══════════════════════════════════════════════════════════

def crear_profesores():
    print(f"\n[2/5] Creando {PROFESORES} profesores...")
    grupo_prof = get_or_create_grupo("Profesor")
    profesores = []
    for i in range(1, PROFESORES + 1):
        user, created = upsert_user(
            username=f"prof{i:02d}",
            email=f"prof{i:02d}@rhetorica.test",
            first_name=f"Profesor {i}",
            last_name=f"Apellido {i}",
            password=PASSWORD,
            is_staff=True,   # profesores suelen tener acceso al admin
            is_superuser=False,
            grupos=[grupo_prof],
        )
        tag = "NEW" if created else "UPD"
        print(f"  [{tag}] prof{i:02d} (is_staff=True, grupo=Profesor)")
        profesores.append(user)
    return profesores


# ═══════════════════════════════════════════════════════════
# 3. ESTUDIANTES
# ═══════════════════════════════════════════════════════════

def crear_estudiantes():
    print(f"\n[3/5] Creando {ESTUDIANTES} estudiantes...")
    grupo_est = get_or_create_grupo("Estudiante")
    estudiantes = []
    for i in range(1, ESTUDIANTES + 1):
        user, created = upsert_user(
            username=f"est{i:03d}",
            email=f"est{i:03d}@rhetorica.test",
            first_name=f"Estudiante {i}",
            last_name=f"Apellido {i}",
            password=PASSWORD,
            is_staff=False,
            is_superuser=False,
            grupos=[grupo_est],
        )
        estudiantes.append(user)
        # Log cada 12 estudiantes para no inundar
        if i % 12 == 0 or i == ESTUDIANTES:
            print(f"  [OK] {i}/{ESTUDIANTES} estudiantes creados/actualizados")
    return estudiantes


# ═══════════════════════════════════════════════════════════
# 4. PROGRESO EN LOS 5 MODULOS
# ═══════════════════════════════════════════════════════════

def _generar_estado():
    """Devuelve 'en_progreso' o 'dominada' (nunca 'no_iniciada')."""
    return random.choices(
        ["en_progreso", "dominada"],
        weights=[60, 40],
    )[0]


def _generar_progreso_dict():
    """Diccionario con los campos SM-2 aleatorios."""
    return {
        "intentos": random.randint(1, 15),
        "aciertos_consecutivos": random.randint(0, 5),
        "estado": _generar_estado(),
        "sm2_ef": 2.5,
        "sm2_interval": random.randint(1, 30),
        "sm2_repetitions": random.randint(0, 4),
        "proxima_revision": timezone.now() + timedelta(days=random.randint(1, 30)),
        "ultima_revision": timezone.now() - timedelta(days=random.randint(0, 15)),
    }


def sembrar_progreso_gramatica(estudiantes):
    """Pobla ProgresoGramatical para gramatica, generativa, a1, b1."""
    print(f"\n[4/5] Progreso en modulos de gramatica...")
    total_global = 0

    for modulo in MODULOS:
        tecnicas = list(TecnicaGramatical.objects.filter(modulo=modulo))
        if not tecnicas:
            print(f"  [!] {modulo}: 0 tecnicas en DB, saltando")
            continue

        print(f"  [INFO] {modulo}: {len(tecnicas)} tecnicas x {len(estudiantes)} estudiantes")

        progresos = []
        for estudiante in estudiantes:
            k_min = max(1, int(len(tecnicas) * 0.2))
            k_max = max(k_min, int(len(tecnicas) * 0.6))
            k = random.randint(k_min, k_max)
            muestra = random.sample(tecnicas, k=k)

            for tecnica in muestra:
                progresos.append(ProgresoGramatical(
                    usuario=estudiante,
                    tecnica=tecnica,
                    **_generar_progreso_dict(),
                ))

        # Bulk insert en batches (evita limites SQLite/Postgres)
        for i in range(0, len(progresos), BATCH_SIZE):
            ProgresoGramatical.objects.bulk_create(
                progresos[i:i + BATCH_SIZE],
                ignore_conflicts=True,   # idempotente: no duplica si ya existe
            )

        print(f"  [OK] {modulo}: {len(progresos)} progresos insertados")
        total_global += len(progresos)

    return total_global


def sembrar_progreso_sintaxis(estudiantes):
    """Pobla ProgresoTecnica para el modulo 10."""
    if not HAS_SINTAXIS:
        print(f"\n[4/5] Sintaxis: saltado (modelo no disponible)")
        return 0

    print(f"\n[4/5b] Progreso en sintaxis (modulo 10)...")
    tecnicas = list(TecnicaSintactica.objects.all())
    if not tecnicas:
        print(f"  [!] sintaxis: 0 tecnicas en DB, saltando")
        return 0

    print(f"  [INFO] sintaxis: {len(tecnicas)} tecnicas x {len(estudiantes)} estudiantes")

    progresos = []
    for estudiante in estudiantes:
        k_min = max(1, int(len(tecnicas) * 0.2))
        k_max = max(k_min, int(len(tecnicas) * 0.6))
        k = random.randint(k_min, k_max)
        muestra = random.sample(tecnicas, k=k)

        for tecnica in muestra:
            progresos.append(ProgresoTecnica(
                usuario=estudiante,
                tecnica=tecnica,
                **_generar_progreso_dict(),
            ))

    for i in range(0, len(progresos), BATCH_SIZE):
        ProgresoTecnica.objects.bulk_create(
            progresos[i:i + BATCH_SIZE],
            ignore_conflicts=True,
        )

    print(f"  [OK] sintaxis: {len(progresos)} progresos insertados")
    return len(progresos)


# ═══════════════════════════════════════════════════════════
# 5. NOTIFICACIONES DE BIENVENIDA
# ═══════════════════════════════════════════════════════════

def crear_notificaciones_bienvenida(estudiantes):
    """1 notificacion de bienvenida por estudiante (idempotente)."""
    print(f"\n[5/5] Notificaciones de bienvenida...")

    try:
        from core.services.notificaciones import crear_notificacion
    except ImportError:
        print("  [!] crear_notificacion no disponible, saltando")
        return 0

    count = 0
    errores = 0
    for estudiante in estudiantes:
        try:
            crear_notificacion(
                user=estudiante,
                tipo="logro",
                titulo="Bienvenido/a a Rhetorica",
                mensaje="Empieza por el modulo A1: 100 tecnicas para principiantes.",
                url_destino="/gramatica/a1/",
                icono="star",
                referencia=f"bienvenida_{estudiante.id}",
            )
            count += 1
        except Exception as e:
            errores += 1
            if errores <= 3:
                print(f"  [!] {estudiante.username}: {e}")

    print(f"  [OK] {count} notificaciones creadas ({errores} errores)")
    return count


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("SEED USUARIOS DE PRUEBA + PROGRESO EN 5 MODULOS")
    print("=" * 65)

    # Detectar estado previo
    print(f"\n[INFO] Estado previo:")
    print(f"  Users existentes: {User.objects.count()}")
    print(f"  TecnicasGramatical: {TecnicaGramatical.objects.count()}")
    if HAS_SINTAXIS:
        print(f"  TecnicasSintactica: {TecnicaSintactica.objects.count()}")

    # 1. Admins
    admins = crear_admins()

    # 2. Profesores
    profesores = crear_profesores()

    # 3. Estudiantes
    estudiantes = crear_estudiantes()

    # 4. Progreso
    total_gram = sembrar_progreso_gramatica(estudiantes)
    total_sint = sembrar_progreso_sintaxis(estudiantes)

    # 5. Notificaciones
    total_notif = crear_notificaciones_bienvenida(estudiantes)

    # Resumen final
    print("\n" + "=" * 65)
    print("RESUMEN")
    print("=" * 65)
    print(f"Admins:        {len(admins)}  (admin01 - admin{ADMINS:02d})")
    print(f"Profesores:    {len(profesores)}  (prof01 - prof{PROFESORES:02d})")
    print(f"Estudiantes:   {len(estudiantes)}  (est001 - est{ESTUDIANTES:03d})")
    print(f"")
    print(f"Progreso:")
    print(f"  Gram+Gen+A1+B1: {total_gram} filas")
    print(f"  Sintaxis:       {total_sint} filas")
    print(f"  Notificaciones: {total_notif}")
    print(f"")
    print(f"Password comun: {PASSWORD}")
    print(f"")
    print(f"URLs para probar:")
    print(f"  /admin/                          admin01 / {PASSWORD}")
    print(f"  /admin-panel/                    admin01 / {PASSWORD}")
    print(f"  /profesor/                       prof01 / {PASSWORD}")
    print(f"  /estudiante/                     est001 / {PASSWORD}")
    print(f"  /sintaxis/                       (cualquier user)")
    print(f"  /gramatica/                      (cualquier user)")
    print(f"  /gramatica/generativa/           (cualquier user)")
    print(f"  /gramatica/a1/                   (cualquier user)")
    print(f"  /gramatica/b1/                   (cualquier user)")
    print("=" * 65)


if __name__ == "__main__":
    main()