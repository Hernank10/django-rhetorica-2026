"""Reconstruye ProgresoCategoria desde el historico de Respuesta."""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Q

from core.models import ProgresoCategoria, Respuesta
from core.signals_progreso import _calcular_nivel_dominio, _calcular_estrellas


class Command(BaseCommand):
    help = "Reconstruye ProgresoCategoria agrupando Respuesta por (user, tipo)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Solo reportar, no escribir en BD",
        )

    def handle(self, *args, **options):
        dry = options["dry_run"]

        if not dry:
            with transaction.atomic():
                ProgresoCategoria.objects.all().delete()

        agregados = (
            Respuesta.objects
            .values("user_id", "tipo_ejercicio")
            .annotate(
                intentos=Count("id"),
                aciertos=Count("id", filter=Q(es_correcta=True)),
            )
        )

        creados = 0
        for a in agregados:
            nivel = _calcular_nivel_dominio(a["aciertos"], a["intentos"])
            estrellas = _calcular_estrellas(a["aciertos"], a["intentos"])
            if dry:
                self.stdout.write(
                    f"  [dry] user={a['user_id']} cat={a['tipo_ejercicio']} "
                    f"{a['aciertos']}/{a['intentos']} nivel={nivel} estrellas={estrellas}"
                )
            else:
                ProgresoCategoria.objects.create(
                    user_id=a["user_id"],
                    categoria=a["tipo_ejercicio"],
                    aciertos=a["aciertos"],
                    intentos=a["intentos"],
                    nivel_dominio=nivel,
                    estrellas_obtenidas=estrellas,
                )
                creados += 1

        self.stdout.write(self.style.SUCCESS(
            f"{'[dry] habria creado' if dry else 'Creados'}: {creados} ProgresoCategoria"
        ))