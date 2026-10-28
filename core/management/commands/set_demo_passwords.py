from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Resetea contrasenas de los usuarios est* a Test1234! (demo)"

    def add_arguments(self, parser):
        parser.add_argument("--password", default="Test1234!")
        parser.add_argument("--prefix", default="est")

    def handle(self, *args, **options):
        User = get_user_model()
        password = options["password"]
        prefix = options["prefix"].lower()

        qs = User.objects.filter(username__istartswith=prefix)
        total = qs.count()
        updated = 0

        for u in qs.iterator():
            u.set_password(password)
            u.is_active = True
            u.save(update_fields=["password", "is_active"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"[OK] {updated}/{total} usuarios '{prefix}*' con password '{password}'"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Prueba con: est035, est045, est011, est061... / {password}"
        ))