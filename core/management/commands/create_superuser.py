import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Crea o actualiza un superusuario, leyendo variables de entorno"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.ERROR(
                "Faltan DJANGO_SUPERUSER_USERNAME o DJANGO_SUPERUSER_PASSWORD"
            ))
            return

        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(
                f"Superusuario {username} creado correctamente."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Contraseña del superusuario {username} actualizada correctamente."
            ))