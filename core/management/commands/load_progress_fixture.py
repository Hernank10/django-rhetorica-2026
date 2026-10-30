from pathlib import Path

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Carga fixtures/core_progress.json (append-only, idempotente)"

    def add_arguments(self, parser):
        parser.add_argument("--fixture", default="fixtures/core_progress.json")
        parser.add_argument("--clear", action="store_true",
                            help="Borrar progreso existente antes de cargar")

    def handle(self, *args, **options):
        fixture_path = Path(options["fixture"])
        if not fixture_path.exists():
            self.stdout.write(self.style.WARNING(f"[SKIP] No existe {fixture_path}"))
            return

        # Contar antes
        PT = apps.get_model("core", "ProgresoTecnica")
        PG = apps.get_model("core", "ProgresoGramatical")
        antes_pt = PT.objects.count()
        antes_pg = PG.objects.count()

        if options["clear"]:
            PT.objects.all().delete()
            PG.objects.all().delete()
            self.stdout.write(f"[CLEAR] ProgresoTecnica: {antes_pt}, ProgresoGramatical: {antes_pg}")

        self.stdout.write(f"[LOAD] {fixture_path}")
        try:
            call_command("loaddata", str(fixture_path), verbosity=1)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERROR] {e}"))
            return

        # Contar después
        despues_pt = PT.objects.count()
        despues_pg = PG.objects.count()
        

        # Limpiar ProgresoGramatical con tecnica_id huérfano
        from core.models_gramatica import TecnicaGramatical
        valid_ids = set(TecnicaGramatical.objects.values_list('id', flat=True))
        huerfanos = ProgresoGramatical.objects.exclude(tecnica_id__in=valid_ids)
        n = huerfanos.count()
        if n:
            huerfanos.delete()
            self.stdout.write(f'[CLEANUP] {n} ProgresoGramatical huérfanos eliminados')

self.stdout.write(self.style.SUCCESS(
            f"[OK] ProgresoTecnica: {antes_pt}->{despues_pt} | "
            f"ProgresoGramatical: {antes_pg}->{despues_pg}"
        ))