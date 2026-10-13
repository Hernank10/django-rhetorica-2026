"""
Pobla la BD con 3 admin / 9 profesores / 96 estudiantes y prueba i18n + URLs.

Uso:
    python manage.py seed_and_test
    python manage.py seed_and_test --reset       (borra y recrea)
    python manage.py seed_and_test --skip-tests  (solo poblar)
"""
import time

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.test import Client
from django.utils import translation

User = get_user_model()

PASSWORD_ADMIN = "Admin123!"
PASSWORD_PROF  = "Prof123!"
PASSWORD_EST   = "Est123!"


class Command(BaseCommand):
    help = "Pobla con 3 admins / 9 profesores / 96 estudiantes y prueba todo"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Borra usuarios admin*/prof*/est* antes de crear")
        parser.add_argument("--skip-tests", action="store_true",
                            help="Solo pobla, no ejecuta pruebas")

    def handle(self, *args, **opts):
        t0 = time.time()
        # --- bypass temporal del signal sync_user_to_core ---
        from django.db.models.signals import post_save
        from django.contrib.auth import get_user_model as _gum
        from core import signals as _signals
        _User = _gum()
        try:
            post_save.disconnect(_signals.sync_user_to_core, sender=_User)
            self.stdout.write(self.style.WARNING("[WARN] signal sync_user_to_core desconectado"))
        except Exception:
            pass
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== SEED & TEST - django-rhetorica ===\n"))

        if opts["reset"]:
            n = User.objects.filter(username__regex=r"^(admin\d+|prof\d+|est\d+)$").delete()
            self.stdout.write(self.style.WARNING(f"[RESET] usuarios borrados: {n[0]}"))

        # --- Grupos ---
        g_admin, _ = Group.objects.get_or_create(name="Administrador")
        g_prof,  _ = Group.objects.get_or_create(name="Profesor")
        g_est,   _ = Group.objects.get_or_create(name="Estudiante")
        self.stdout.write(self.style.SUCCESS("[OK] Grupos: Administrador / Profesor / Estudiante"))

        # --- 3 admins ---
        admins = []
        for i in range(1, 4):
            u, created = User.objects.get_or_create(
                username=f"admin{i}",
                defaults=dict(
                    email=f"admin{i}@rhetorica.local",
                    first_name="Admin",
                    last_name=f"Numero {i}",
                    is_staff=True,
                    is_superuser=True,
                ),
            )
            if created:
                u.set_password(PASSWORD_ADMIN)
                u.save()
            u.groups.add(g_admin)
            admins.append(u)
        self.stdout.write(self.style.SUCCESS(
            f"[OK] {len(admins)} admins (admin1..admin3 / {PASSWORD_ADMIN})"))

        # --- 9 profesores ---
        profesores = []
        for i in range(1, 10):
            u, created = User.objects.get_or_create(
                username=f"prof{i:02d}",
                defaults=dict(
                    email=f"prof{i:02d}@rhetorica.local",
                    first_name="Profesor",
                    last_name=f"Apellido {i}",
                    is_staff=True,
                    is_superuser=False,
                ),
            )
            if created:
                u.set_password(PASSWORD_PROF)
                u.save()
            u.groups.add(g_prof)
            profesores.append(u)
        self.stdout.write(self.style.SUCCESS(
            f"[OK] {len(profesores)} profesores (prof01..prof09 / {PASSWORD_PROF})"))

        # --- 96 estudiantes ---
        estudiantes = []
        for i in range(1, 97):
            u, created = User.objects.get_or_create(
                username=f"est{i:03d}",
                defaults=dict(
                    email=f"est{i:03d}@rhetorica.local",
                    first_name="Estudiante",
                    last_name=f"Apellido {i}",
                    is_staff=False,
                ),
            )
            if created:
                u.set_password(PASSWORD_EST)
                u.save()
            u.groups.add(g_est)
            estudiantes.append(u)
        self.stdout.write(self.style.SUCCESS(
            f"[OK] {len(estudiantes)} estudiantes (est001..est096 / {PASSWORD_EST})"))

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n=== Total usuarios en BD: {User.objects.count()} ===\n"))

        # --- Listar modelos de core ---
        self.stdout.write(self.style.MIGRATE_HEADING("=== Modelos de la app 'core' ==="))
        try:
            core_cfg = apps.get_app_config("core")
            for m in core_cfg.get_models():
                fields = [f.name for f in m._meta.get_fields()
                          if not f.auto_created and not f.is_relation]
                self.stdout.write(f"  - {m.__name__}: {', '.join(fields[:12])}")
        except LookupError:
            self.stdout.write(self.style.ERROR("  [!] App 'core' no encontrada"))
        self.stdout.write("")

        # --- Pruebas ---
        if not opts["skip_tests"]:
            self._test_i18n()
            self._test_urls(admins[0], profesores[0], estudiantes[0])

        elapsed = time.time() - t0
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n=== FIN en {elapsed:.2f}s ===\n"))

    # ------------------------------------------------------------------
    def _test_i18n(self):
        self.stdout.write(self.style.MIGRATE_HEADING("=== TEST i18n (16 idiomas) ==="))
        c = Client()
        ok = 0
        langs = [code for code, _ in settings.LANGUAGES]
        for lang in langs:
            url = "/" if lang == "es" else f"/{lang}/"
            try:
                with translation.override(lang):
                    r = c.get(url)
                if r.status_code == 200:
                    ok += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  [OK] {url:12} -> 200 ({len(r.content)} bytes)"))
                else:
                    self.stdout.write(self.style.ERROR(
                        f"  [!!] {url:12} -> {r.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  [!!] {url:12} -> {e}"))
        self.stdout.write(self.style.SUCCESS(f"\n  >>> {ok}/{len(langs)} idiomas OK\n"))

    # ------------------------------------------------------------------
    def _test_urls(self, admin, prof, est):
        self.stdout.write(self.style.MIGRATE_HEADING("=== TEST URLs (roles) ==="))
        pruebas = [
            ("/",                     "anon"),
            ("/login/",               "anon"),
            ("/registro/",            "anon"),
            ("/dashboard/",           "est"),
            ("/dashboard/gamificacion/", "est"),
            ("/cursos/",              "est"),
            ("/biblioteca/",          "est"),
            ("/perfil/",              "est"),
            ("/tecnicas/",            "est"),
            ("/certificaciones/",     "est"),
            ("/admin/",               "admin"),
        ]
        for url, role in pruebas:
            c = Client()
            if role == "admin":
                c.force_login(admin)
            elif role == "est":
                c.force_login(est)
            elif role == "prof":
                c.force_login(prof)
            try:
                r = c.get(url, follow=False)
                color = self.style.SUCCESS if r.status_code in (200, 302) else self.style.WARNING
                self.stdout.write(color(f"  [{role:5}] {url:35} -> {r.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  [{role:5}] {url:35} -> {e}"))
        self.stdout.write("")
