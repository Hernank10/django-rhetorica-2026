"""Tests del comando backfill_progreso."""

from io import StringIO

import pytest
from django.core.management import call_command

from core.models import Respuesta, ProgresoCategoria


class TestBackfillProgreso:
    def test_sin_respuestas(self, db):
        """Sin Respuesta, no crea nada."""
        call_command("backfill_progreso", stdout=StringIO())
        assert ProgresoCategoria.objects.count() == 0

    def test_crea_desde_respuestas(self, db, estudiante_user):
        """Crea ProgresoCategoria a partir de las Respuesta existentes."""
        for i in range(3):
            Respuesta.objects.create(
                user=estudiante_user, tipo_ejercicio="multiple_choice",
                item_id=i, respuesta_usuario="x", es_correcta=True,
                puntuacion=10, tiempo_segundos=10, intento_numero=1,
            )
        for i in range(2):
            Respuesta.objects.create(
                user=estudiante_user, tipo_ejercicio="multiple_choice",
                item_id=100 + i, respuesta_usuario="y", es_correcta=False,
                puntuacion=0, tiempo_segundos=10, intento_numero=1,
            )

        # Borrar lo que el signal haya creado, para probar el backfill puro
        ProgresoCategoria.objects.all().delete()

        call_command("backfill_progreso", stdout=StringIO())

        prog = ProgresoCategoria.objects.get(
            user=estudiante_user, categoria="multiple_choice",
        )
        assert prog.intentos == 5
        assert prog.aciertos == 3

    def test_limpia_antes_de_reconstruir(self, db, estudiante_user):
        """El backfill borra las filas existentes antes de recrear."""
        # Crear una fila "corrupta" manualmente
        ProgresoCategoria.objects.create(
            user=estudiante_user, categoria="fake",
            aciertos=999, intentos=999,
        )
        assert ProgresoCategoria.objects.count() == 1

        call_command("backfill_progreso", stdout=StringIO())

        # La fila 'fake' ya no existe (fue borrada)
        assert not ProgresoCategoria.objects.filter(categoria="fake").exists()

    def test_dry_run_no_escribe(self, db, estudiante_user):
        """Con --dry-run no debe modificar la BD."""
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        ProgresoCategoria.objects.all().delete()

        out = StringIO()
        call_command("backfill_progreso", "--dry-run", stdout=out)

        assert ProgresoCategoria.objects.count() == 0
        assert "[dry]" in out.getvalue()

    def test_dry_run_reporta(self, db, estudiante_user):
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="completar",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        ProgresoCategoria.objects.all().delete()

        out = StringIO()
        call_command("backfill_progreso", "--dry-run", stdout=out)
        salida = out.getvalue()
        assert "estudiante" in salida or f"user={estudiante_user.id}" in salida

    def test_mensaje_final(self, db, estudiante_user):
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        ProgresoCategoria.objects.all().delete()

        out = StringIO()
        call_command("backfill_progreso", stdout=out)
        assert "Creados:" in out.getvalue() or "Creados" in out.getvalue()