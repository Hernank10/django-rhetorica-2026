from pathlib import Path

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction


DELETE_ORDER = [
    # Hijos primero, padres al final
    ("core", "PreguntaEvaluacion"),
    ("core", "EvaluacionCurso"),
    ("core", "Leccion"),
    ("core", "Modulo"),
    ("core", "Curso"),
    ("core", "Review"),              # FK a Flashcard
    ("core", "Flashcard"),           # FK a User
    ("core", "EjercicioGramatical"),
    ("core", "EjercicioTecnica"),
    ("core", "EjercicioLinguistico"),
    ("core", "TecnicaGramatical"),
    ("core", "TecnicaSintactica"),
    ("core", "TecnicaLinguistica"),  # M2M desde Curso/Leccion
    ("core", "Recurso"),
    ("core", "ContenidoJSON"),
    ("core", "Certificacion"),       # cascada a CertificacionObtenida
]


class Command(BaseCommand):
    help = "Carga fixtures/core_content.json parcheando FKs a User (idempotente)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Borra contenido existente y recarga",
        )
        parser.add_argument(
            "--no-clear",
            action="store_true",
            help="Con --force, no borrar; solo intentar loaddata",
        )
        parser.add_argument(
            "--fixture",
            default="fixtures/core_content.json",
        )

    def _clear_content(self):
        total = 0
        with transaction.atomic():
            for app_label, model_name in DELETE_ORDER:
                try:
                    Model = apps.get_model(app_label, model_name)
                except LookupError:
                    continue
                deleted, _ = Model.objects.all().delete()
                if deleted:
                    self.stdout.write(f"[CLEAR] {model_name}: {deleted} borrados")
                    total += deleted
        self.stdout.write(f"[CLEAR] Total borrados: {total}")

    def handle(self, *args, **options):
        fixture_path = Path(options["fixture"])
        if not fixture_path.exists():
            self.stdout.write(self.style.WARNING(f"[SKIP] No existe {fixture_path}"))
            return

        force = options["force"]
        no_clear = options["no_clear"]

        if not force:
            targets = [
                ("core", "TecnicaGramatical"),
                ("core", "Recurso"),
                ("core", "Curso"),
            ]
            todo_vacio = True
            for app_label, model_name in targets:
                try:
                    n = apps.get_model(app_label, model_name).objects.count()
                    if n > 0:
                        self.stdout.write(f"[INFO] {model_name}: {n} filas")
                        todo_vacio = False
                except LookupError:
                    continue
            if not todo_vacio:
                self.stdout.write(
                    self.style.SUCCESS(
                        "[SKIP] Ya hay datos. Usa --force para recargar."
                    )
                )
                return

        if force and not no_clear:
            self._clear_content()

        try:
            import json

            User = get_user_model()
            admin = User.objects.filter(is_superuser=True).order_by("pk").first()
            if admin:
                data = json.loads(fixture_path.read_text(encoding="utf-8"))
                patched = 0
                for obj in data:
                    if obj.get("model") == "core.curso":
                        fields = obj.get("fields", {})
                        if "creado_por" in fields:
                            fields["creado_por"] = admin.pk
                            patched += 1
                        if "profesor_asignado" in fields:
                            fields["profesor_asignado"] = admin.pk
                            patched += 1
                if patched:
                    patched_path = fixture_path.with_name("_patched.json")
                    patched_path.write_text(
                        json.dumps(data, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    fixture_path = patched_path
                    self.stdout.write(
                        f"[PATCH] {patched} FKs a User -> pk={admin.pk}"
                    )
                else:
                    self.stdout.write("[PATCH] Sin FKs de Curso que parchear")
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "[WARN] No hay superusuario; se carga sin parchear"
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"[WARN] Pre-parcheo fallo: {e}"))

        self.stdout.write(f"[LOAD] {fixture_path}")
        call_command("loaddata", str(fixture_path), verbosity=2)
        self.stdout.write(
            self.style.SUCCESS(f"[OK] Fixture cargado: {fixture_path}")
        )