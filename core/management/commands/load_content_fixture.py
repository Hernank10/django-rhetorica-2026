from pathlib import Path

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Carga fixtures/core_content.json parcheando FKs a User (idempotente)"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true",
                            help="Recarga aunque ya haya datos")
        parser.add_argument("--fixture", default="fixtures/core_content.json")

    def handle(self, *args, **options):
        fixture_path = Path(options["fixture"])
        if not fixture_path.exists():
            self.stdout.write(self.style.WARNING(f"[SKIP] No existe {fixture_path}"))
            return

        # 1) Pre-parchear FKs a User (Curso.creado_por / profesor_asignado)
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
                self.stdout.write(self.style.WARNING(
                    "[WARN] No hay superusuario; se carga sin parchear"
                ))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"[WARN] Pre-parcheo fallo: {e}"))

        # 2) Heuristica de "ya hay datos"
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
                n = apps.get_model(app_label, model_name).objects.count()
                if n > 0:
                    self.stdout.write(f"[INFO] {model_name}: {n} filas")
                    todo_vacio = False
            except LookupError:
                continue

        if not todo_vacio and not options["force"]:
            self.stdout.write(self.style.SUCCESS(
                "[SKIP] Ya hay datos. Usa --force para recargar."
            ))
            return

        # 3) Cargar SIN atrapar errores -> set -o errexit cortara el build
        self.stdout.write(f"[LOAD] {fixture_path}")
        call_command("loaddata", str(fixture_path), verbosity=2)
        self.stdout.write(self.style.SUCCESS(f"[OK] Fixture cargado: {fixture_path}"))