"""Management command: otorgar_certificaciones.

Uso:
    python manage.py otorgar_certificaciones
    python manage.py otorgar_certificaciones --user est001
    python manage.py otorgar_certificaciones --dry-run
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.services.certificaciones import verificar_y_otorgar


class Command(BaseCommand):
    help = "Otorga certificaciones pendientes a todos los usuarios (o a uno especifico)"

    def add_arguments(self, parser):
        parser.add_argument("--user", type=str, help="Username especifico")
        parser.add_argument("--dry-run", action="store_true", help="No crea, solo muestra")

    def handle(self, *args, **options):
        if options["user"]:
            usuarios = User.objects.filter(username=options["user"])
        else:
            usuarios = User.objects.filter(is_staff=False, is_superuser=False)

        total_usuarios = usuarios.count()
        total_certs = 0
        prefix = "[DRY]" if options["dry_run"] else "[OK]"

        self.stdout.write(f"Procesando {total_usuarios} usuarios...\n")

        for user in usuarios:
            nuevas = verificar_y_otorgar(user, dry_run=options["dry_run"])
            if nuevas:
                total_certs += len(nuevas)
                nombres = ", ".join(c.nombre[:20] for c in nuevas[:3])
                extra = f"... (+{len(nuevas)-3})" if len(nuevas) > 3 else ""
                self.stdout.write(f"  {prefix} {user.username:15s} {len(nuevas):2d} certs: {nombres}{extra}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n[OK] {total_certs} certificaciones "
                f"{'se otorgarian' if options['dry_run'] else 'otorgadas'} "
                f"a {total_usuarios} usuarios"
            )
        )