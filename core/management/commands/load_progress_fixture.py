from pathlib import Path

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Carga fixtures/core_progress.json (idempotente, con cleanup de huérfanos)"

    def add_arguments(self, parser):
        parser.add_argument("--fixture", default="fixtures/core_progress.json")
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Borrar progreso existente antes de cargar",
        )

    def _clean_orphans(self, PT, PG, TecnicaGramatical, TecnicaSintactica, label):
        """Borra Progreso* con tecnica_id huérfana (FK apunta a técnica inexistente)."""
        valid_gram = set(TecnicaGramatical.objects.values_list("id", flat=True))
        n_gram = PG.objects.exclude(tecnica_id__in=valid_gram).delete()[0]

        valid_sint = set(TecnicaSintactica.objects.values_list("id", flat=True))
        n_sint = PT.objects.exclude(tecnica_id__in=valid_sint).delete()[0]

        if n_gram or n_sint:
            self.stdout.write(
                f"[CLEANUP-{label}] ProgresoGramatical: {n_gram}, "
                f"ProgresoTecnica: {n_sint} huérfanos eliminados"
            )
        return n_gram + n_sint

    def handle(self, *args, **options):
        fixture_path = Path(options["fixture"])
        if not fixture_path.exists():
            self.stdout.write(self.style.WARNING(f"[SKIP] No existe {fixture_path}"))
            return

        PT = apps.get_model("core", "ProgresoTecnica")
        PG = apps.get_model("core", "ProgresoGramatical")
        TecnicaGramatical = apps.get_model("core", "TecnicaGramatical")
        TecnicaSintactica = apps.get_model("core", "TecnicaSintactica")

        antes_pt = PT.objects.count()
        antes_pg = PG.objects.count()

        if options["clear"]:
            PT.objects.all().delete()
            PG.objects.all().delete()
            self.stdout.write(
                f"[CLEAR] ProgresoTecnica: {antes_pt}, ProgresoGramatical: {antes_pg}"
            )

        # Cleanup PRE: elimina huérfanos existentes ANTES de meter nuevos
        self._clean_orphans(PT, PG, TecnicaGramatical, TecnicaSintactica, "PRE")

        self.stdout.write(f"[LOAD] {fixture_path}")
        try:
            call_command("loaddata", str(fixture_path), verbosity=1)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERROR] {e}"))
            return

        despues_pt = PT.objects.count()
        despues_pg = PG.objects.count()

        # Cleanup POST: elimina huérfanos que loaddata haya podido meter
        self._clean_orphans(PT, PG, TecnicaGramatical, TecnicaSintactica, "POST")

        self.stdout.write(
            self.style.SUCCESS(
                f"[OK] ProgresoTecnica: {antes_pt}->{despues_pt} | "
                f"ProgresoGramatical: {antes_pg}->{despues_pg}"
            )
        )
