from pathlib import Path

from django.apps import apps
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
        # ─── REMAP_FLASHCARDS: reasignar flashcards/reviews a usuarios válidos ───
        # El fixture tiene PKs de est### de local (121..216) que no existen en Render.
        # Este bloque los remapea a testest### (o est###) si existen.
        try:
            User = get_user_model()

            Flashcard = apps.get_model("core", "Flashcard")
            Review = apps.get_model("core", "Review")

            valid_pks = set(User.objects.values_list("pk", flat=True))
            users_by_name = {u.username: u for u in User.objects.all()}

            remapped_fc = 0
            remapped_rv = 0
            skipped_fc = 0

            for fc in Flashcard.objects.all():
                if fc.estudiante_id in valid_pks:
                    continue
                # Intentar remapear por offset: PK original = 120 + n
                n = fc.estudiante_id - 120
                if 1 <= n <= 96:
                    for candidate in (f"testest{n:03d}", f"est{n:03d}"):
                        target = users_by_name.get(candidate)
                        if target:
                            fc.estudiante = target
                            fc.save(update_fields=["estudiante"])
                            remapped_fc += 1
                            break
                    else:
                        skipped_fc += 1
                else:
                    skipped_fc += 1

            for rv in Review.objects.all():
                if rv.flashcard.estudiante_id in valid_pks:
                    continue
                # La Review apunta a Flashcard; ya debería haberse remapeado
                # Pero por si acaso, remapear la Flashcard también
                fc = rv.flashcard
                if fc.estudiante_id not in valid_pks:
                    n = fc.estudiante_id - 120
                    if 1 <= n <= 96:
                        for candidate in (f"testest{n:03d}", f"est{n:03d}"):
                            target = users_by_name.get(candidate)
                            if target:
                                fc.estudiante = target
                                fc.save(update_fields=["estudiante"])
                                remapped_fc += 1
                                break
                remapped_rv += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"[REMAP] flashcards={remapped_fc} reviews={remapped_rv} skipped={skipped_fc}"
                )
            )
            if skipped_fc:
                self.stdout.write(
                    self.style.WARNING(
                        f"[REMAP] {skipped_fc} flashcards sin usuario válido (PK rango 121-216 esperado)"
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"[REMAP] fallo: {e}"))
        # ─── FIN REMAP_FLASHCARDS ───
        self.stdout.write(
            self.style.SUCCESS(f"[OK] Fixture cargado: {fixture_path}")
        )