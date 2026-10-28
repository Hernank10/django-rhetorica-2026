from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.apps import apps


class Command(BaseCommand):
    help = "Carga fixtures/core_content.json en modelos vacíos (idempotente)"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")
        parser.add_argument("--fixture", default="fixtures/core_content.json")

    def handle(self, *args, **options):
        fixture_path = Path(options["fixture"])
        if not fixture_path.exists():
            self.stdout.write(self.style.WARNING(f"[SKIP] No existe {fixture_path}"))
            return

        # Chequear si ya hay contenido cargado
        targets = [
            ("core", "TecnicaGramatical"),
            ("core", "TecnicaSintactica"),
            ("core", "EjercicioLinguistico"),
            ("core", "Recurso"),
            ("core", "Curso"),
        ]

        todo_vacio = True
        for app_label, model_name in targets:
            try:
                Model = apps.get_model(app_label, model_name)
                n = Model.objects.count()
                if n > 0:
                    self.stdout.write(f"[INFO] {model_name} ya tiene {n} filas")
                    todo_vacio = False
            except LookupError:
                continue

        if not todo_vacio and not options["force"]:
            self.stdout.write(self.style.SUCCESS(
                "[SKIP] Ya hay datos en la DB. Usa --force para recargar."
            ))
            return

        self.stdout.write("[LOAD] Ejecutando loaddata...")
        try:
            call_command("loaddata", str(fixture_path), verbosity=2)
            self.stdout.write(self.style.SUCCESS(f"[OK] Fixture cargado: {fixture_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[ERROR] {e}"))