"""Indexa archivos de la carpeta de recursos en la BD."""
import os
import re
from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone

from core.models import Recurso


# Extensiones permitidas
EXTENSIONES_OK = {
    ".html", ".htm", ".json", ".md", ".txt", ".docx",
    ".py", ".js", ".css", ".sql", ".sh", ".csv", ".xml",
}
TAMAÑO_MAX = 10 * 1024 * 1024  # 10 MB


def clasificar(nombre):
    """Devuelve la categoría según el nombre del archivo."""
    n = nombre.lower()
    if "super cuaderno" in n or "súper cuaderno" in n:
        return "Súper Cuaderno"
    if "cuaderno" in n:
        return "Cuaderno"
    if "flota" in n:
        return "Flota"
    if "archivo de vector" in n:
        return "Vector"
    if "scriptorium" in n:
        return "Scriptorium"
    if "100 t" in n and ("técnica" in n or "tecnica" in n):
        return "Técnicas"
    if nombre.endswith(".json"):
        return "Datos JSON"
    return "Otros"


class Command(BaseCommand):
    help = "Indexa los archivos de recursos educativos en la BD"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Borra e indexa desde cero")
        parser.add_argument("--path", default=None, help="Ruta a la carpeta de recursos")

    def handle(self, *args, **opts):
        if opts["reset"]:
            n = Recurso.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"[RESET] {n[0]} recursos borrados"))

        carpeta = Path(opts["path"]) if opts["path"] else Path(settings.BASE_DIR) / "ejercicios_completos-lengua-castellana"
        if not carpeta.exists():
            self.stdout.write(self.style.ERROR(f"[!] No existe: {carpeta}"))
            return

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n=== Indexando: {carpeta} ===\n"))

        creados = 0
        actualizados = 0
        omitidos = 0
        errores = 0

        for f in sorted(carpeta.rglob("*")):
            if not f.is_file():
                continue

            ext = f.suffix.lower()
            if ext not in EXTENSIONES_OK:
                omitidos += 1
                continue

            try:
                size = f.stat().st_size
                if size > TAMAÑO_MAX:
                    omitidos += 1
                    continue

                rel = str(f.relative_to(carpeta)).replace("\\", "/")
                nombre = f.stem[:290]
                categoria = clasificar(f.name)

                # slug único
                base_slug = slugify(nombre)[:250] or "recurso"
                slug = base_slug
                i = 1
                while Recurso.objects.exclude(archivo=rel).filter(slug=slug).exists():
                    slug = f"{base_slug}-{i}"
                    i += 1
                    if i > 999:
                        break

                fecha_mod = timezone.make_aware(datetime.fromtimestamp(f.stat().st_mtime))

                obj, created = Recurso.objects.update_or_create(
                    archivo=rel,
                    defaults=dict(
                        nombre=nombre,
                        slug=slug,
                        categoria=categoria,
                        extension=ext.lstrip("."),
                        tamaño_bytes=size,
                        fecha_mod=fecha_mod,
                    ),
                )
                if created:
                    creados += 1
                else:
                    actualizados += 1
            except Exception as e:
                errores += 1
                self.stdout.write(self.style.ERROR(f"  [ERR] {f.name}: {e}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"[OK] Creados: {creados}"))
        self.stdout.write(self.style.SUCCESS(f"[OK] Actualizados: {actualizados}"))
        self.stdout.write(self.style.WARNING(f"[--] Omitidos: {omitidos}"))
        if errores:
            self.stdout.write(self.style.ERROR(f"[!!] Errores: {errores}"))

        # Resumen por categoría
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("=== Por categoría ==="))
        from django.db.models import Count
        for cat in Recurso.objects.values("categoria").annotate(n=Count("id")).order_by("-n"):
            self.stdout.write(f"  {cat['categoria']:20} {cat['n']:4} archivos")

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("=== Por extensión ==="))
        for ext in Recurso.objects.values("extension").annotate(n=Count("id")).order_by("-n"):
            self.stdout.write(f"  .{ext['extension']:10} {ext['n']:4} archivos")
