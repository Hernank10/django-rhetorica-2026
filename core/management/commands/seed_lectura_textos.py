"""Seed idempotente de textos + ejercicios de lectura desde JSON.

Claves de unicidad (robustas ante cambios de texto):
- Texto: (nivel_mcer, orden)       -> si cambia el titulo, actualiza sin duplicar
- EjercicioLectura: (texto, orden) -> si cambia el enunciado, actualiza sin duplicar
- Limpia ejercicios huerfanos (si desaparecen del JSON)
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from core.models_lectura import Texto, EjercicioLectura, TecnicaLectura


class Command(BaseCommand):
    help = "Carga textos y ejercicios de lectura desde JSON (idempotente por posicion)"

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
        huerfanos_borrados = 0

        for t in data:
            # Clave robusta: (nivel_mcer, orden)
            texto, created = Texto.objects.update_or_create(
                nivel_mcer=t["nivel_mcer"],
                orden=t.get("orden", 0),
                defaults={
                    "titulo": t["titulo"],
                    "tipo": t["tipo"],
                    "fuente": t.get("fuente", ""),
                    "cuerpo": t["cuerpo"],
                },
            )
            if created:
                textos_creados += 1
            else:
                textos_actualizados += 1

            ordenes_en_json = set()
            for e in t.get("ejercicios", []):
                try:
                    tecnica = TecnicaLectura.objects.get(
                        nivel_mcer=e["tecnica_nivel"],
                        numero=e["tecnica_numero"],
                    )
                except TecnicaLectura.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"  [SKIP] '{texto.titulo}': tecnica #{e['tecnica_numero']} ({e['tecnica_nivel']}) no existe"
                    ))
                    continue

                orden = e.get("orden", 0)
                ordenes_en_json.add(orden)

                # Clave robusta: (texto, orden)
                ej, created = EjercicioLectura.objects.update_or_create(
                    texto=texto,
                    orden=orden,
                    defaults={
                        "enunciado": e["enunciado"],
                        "tecnica": tecnica,
                        "tipo": e["tipo"],
                        "payload": e.get("payload", {}),
                    },
                )
                if created:
                    ejercicios_creados += 1
                else:
                    ejercicios_actualizados += 1

            # Limpiar huerfanos
            huerfanos = texto.ejercicios.exclude(orden__in=ordenes_en_json)
            n = huerfanos.count()
            if n > 0:
                huerfanos.delete()
                huerfanos_borrados += n
                self.stdout.write(self.style.WARNING(
                    f"  [CLEAN] {n} ejercicios huerfanos en '{texto.titulo}'"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"[OK] textos: {textos_creados} creados, {textos_actualizados} actualizados | "
            f"ejercicios: {ejercicios_creados} creados, {ejercicios_actualizados} actualizados | "
            f"huerfanos borrados: {huerfanos_borrados}"
        ))