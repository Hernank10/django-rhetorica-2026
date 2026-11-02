"""Seed idempotente de textos + ejercicios de lectura desde JSON."""
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from core.models_lectura import Texto, EjercicioLectura, TecnicaLectura


class Command(BaseCommand):
    help = "Carga textos y ejercicios de lectura desde JSON (idempotente)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="scripts/_lectura_textos_demo.json",
            help="Ruta del JSON con los textos",
        )

    def handle(self, *args, **options):
        path = Path(options["file"])
        if not path.exists():
            self.stdout.write(self.style.ERROR(f"[ERROR] no existe: {path}"))
            return

        data = json.loads(path.read_text(encoding="utf-8"))
        textos_creados = 0
        textos_actualizados = 0
        ejercicios_creados = 0
        ejercicios_actualizados = 0

        for t in data:
            texto, created = Texto.objects.update_or_create(
                titulo=t["titulo"],
                defaults={
                    "tipo": t["tipo"],
                    "nivel_mcer": t["nivel_mcer"],
                    "fuente": t.get("fuente", ""),
                    "orden": t.get("orden", 0),
                    "cuerpo": t["cuerpo"],
                },
            )
            if created:
                textos_creados += 1
            else:
                textos_actualizados += 1

            for e in t.get("ejercicios", []):
                try:
                    # Fase 0: numero ya no es unico, buscar por nivel del texto + numero
                    tecnica = TecnicaLectura.objects.get(
                        nivel_mcer=e["tecnica_nivel"],
                        numero=e["tecnica_numero"],
                    )
                except TecnicaLectura.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"  [SKIP] ejercicio {e['orden']}: tecnica #{e['tecnica_numero']} no existe"
                    ))
                    continue

                ej, created = EjercicioLectura.objects.update_or_create(
                    texto=texto,
                    enunciado=e["enunciado"],
                    defaults={
                        "tecnica": tecnica,
                        "tipo": e["tipo"],
                        "payload": e.get("payload", {}),
                        "orden": e.get("orden", 0),
                    },
                )
                if created:
                    ejercicios_creados += 1
                else:
                    ejercicios_actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f"[OK] textos: {textos_creados} creados, {textos_actualizados} actualizados | "
            f"ejercicios: {ejercicios_creados} creados, {ejercicios_actualizados} actualizados"
        ))