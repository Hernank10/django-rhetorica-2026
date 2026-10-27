import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Crea 3 superusuarios, 9 profesores y 96 estudiantes de prueba (idempotente)"

    def add_arguments(self, parser):
        parser.add_argument("--password", default=os.getenv("TEST_USERS_PASSWORD", "Test1234!"))
        parser.add_argument("--prefix", default="Test")

    def handle(self, *args, **options):
        User = get_user_model()
        password = options["password"]
        prefix = options["prefix"].lower()

        field_names = [f.name for f in User._meta.get_fields()]

        def set_role(user, role):
            for field in ("role", "tipo", "rol"):
                if field in field_names:
                    try:
                        setattr(user, field, role)
                        user.save()
                        return True
                    except Exception:
                        continue
            return False

        profe_group, _ = Group.objects.get_or_create(name="profesores")
        estudiante_group, _ = Group.objects.get_or_create(name="estudiantes")

        created_super = 0
        created_prof = 0
        created_est = 0
        errors = []

        for i in range(1, 4):
            username = f"{prefix}admin{i}"
            if User.objects.filter(username=username).exists():
                continue
            try:
                u = User.objects.create_superuser(username=username, email=f"{username}@test.local", password=password)
                set_role(u, "admin")
                created_super += 1
            except Exception as e:
                errors.append(f"{username}: {e}")

        for i in range(1, 10):
            username = f"{prefix}profe{i:02d}"
            if User.objects.filter(username=username).exists():
                continue
            try:
                u = User.objects.create_user(username=username, email=f"{username}@test.local", password=password)
                u.is_staff = True
                u.save()
                set_role(u, "profesor")
                profe_group.user_set.add(u)
                created_prof += 1
            except Exception as e:
                errors.append(f"{username}: {e}")

        for i in range(1, 97):
            username = f"{prefix}est{i:03d}"
            if User.objects.filter(username=username).exists():
                continue
            try:
                u = User.objects.create_user(username=username, email=f"{username}@test.local", password=password)
                set_role(u, "estudiante")
                estudiante_group.user_set.add(u)
                created_est += 1
            except Exception as e:
                errors.append(f"{username}: {e}")

        self.stdout.write(self.style.SUCCESS(f"[OK] Creados: {created_super} superusuarios, {created_prof} profesores, {created_est} estudiantes"))
        self.stdout.write(self.style.SUCCESS(f"[OK] Password para todos: {password}"))
        if errors:
            self.stdout.write(self.style.ERROR(f"[!] {len(errors)} errores:"))
            for err in errors[:10]:
                self.stdout.write(self.style.ERROR(f"  - {err}"))