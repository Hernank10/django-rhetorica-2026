"""Seed idempotente de tecnicas lectoras desde JSON."""
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from core.models_lectura import TecnicaLectura


class Command(BaseCommand):
    help = "Carga tecnicas lectoras desde un JSON (idempotente)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="scripts/_lectura_tecnicas_demo.json",
            help="Ruta del JSON con las tecnicas",
        )

    def handle(self, *args, **options):
        path = Path(options["file"])
        if not path.exists():
            self.stdout.write(self.style.ERROR(f"[ERROR] no existe: {path}"))
            return

        data = json.loads(path.read_text(encoding="utf-8"))
        creadas = 0
        actualizadas = 0

        for t in data:
            obj, created = TecnicaLectura.objects.update_or_create(
                nivel_mcer=t["nivel_mcer"],
                numero=t["numero"],
                defaults={
                    "proceso": t["proceso"],
                    "nivel_mcer": t["nivel_mcer"],
                    "titulo": t["titulo"],
                    "teoria": t["teoria"],
                    "explicacion": t["explicacion"],
                    "regla": t["regla"],
                    "ejemplo_correcto": t["ejemplo_correcto"],
                    "ejemplo_incorrecto": t["ejemplo_incorrecto"],
                },
            )
            if created:
                creadas += 1
            else:
                actualizadas += 1

        self.stdout.write(self.style.SUCCESS(
            f"[OK] tecnicas: {creadas} creadas, {actualizadas} actualizadas (total: {len(data)})"
        ))
