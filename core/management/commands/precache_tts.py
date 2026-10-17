"""Precachea MP3s de TTS para todos los ejercicios existentes."""

from django.core.management.base import BaseCommand

from core.models import EjercicioLinguistico
from core.services import tts


class Command(BaseCommand):
    help = "Genera MP3s cacheados de TTS para todos los ejercicios."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--limpiar", action="store_true", help="Borra cache y sale")

    def handle(self, *args, **options):
        if options["limpiar"]:
            n = tts.limpiar_cache()
            self.stdout.write(self.style.SUCCESS(f"Borrados {n} MP3s"))
            return

        dry = options["dry_run"]
        ejercicios = EjercicioLinguistico.objects.all()
        total = ejercicios.count()
        self.stdout.write(f"Procesando {total} ejercicios...")

        generados = 0
        cacheados = 0
        fallidos = 0
        omitidos = 0

        for ej in ejercicios:
            texto = self._texto_para_tts(ej)
            if not texto:
                omitidos += 1
                continue

            if tts.esta_cacheado(texto, "es"):
                cacheados += 1
                continue

            if dry:
                self.stdout.write(f"  [dry] ej={ej.id}: {texto[:60]!r}")
                generados += 1
                continue

            if tts.generar_mp3(texto, "es"):
                generados += 1
            else:
                fallidos += 1

        prefijo = "[dry] habria generado" if dry else "Generados"
        self.stdout.write(self.style.SUCCESS(
            f"{prefijo}: {generados} | Ya cacheados: {cacheados} | "
            f"Fallidos: {fallidos} | Omitidos (sin texto): {omitidos}"
        ))

    def _texto_para_tts(self, ej):
        contenido = ej.contenido or {}
        if isinstance(contenido, dict):
            texto = contenido.get("ejercicio") or contenido.get("enunciado")
            if texto:
                return texto
        return ej.titulo or ""