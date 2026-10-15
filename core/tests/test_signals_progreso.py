"""Tests del signal que puebla ProgresoCategoria."""

import pytest

from core.models import Respuesta, ProgresoCategoria
from core.signals_progreso import _calcular_estrellas, _calcular_nivel_dominio


class TestCalcularNivelDominio:
    def test_sin_intentos(self):
        assert _calcular_nivel_dominio(0, 0) == 1

    @pytest.mark.parametrize("aciertos,intentos,esperado", [
        (0, 10, 1),    # 0%
        (2, 10, 1),    # 20% -> nivel 1
        (4, 10, 2),    # 40% -> nivel 2
        (6, 10, 3),    # 60% -> nivel 3
        (8, 10, 4),    # 80% -> nivel 4
        (9, 10, 5),    # 90% -> nivel 5
        (10, 10, 5),   # 100% -> nivel 5
        (3, 10, 1),    # 30% -> nivel 1
        (5, 10, 2),    # 50% -> nivel 2
        (7, 10, 3),    # 70% -> nivel 3
    ])
    def test_niveles(self, aciertos, intentos, esperado):
        assert _calcular_nivel_dominio(aciertos, intentos) == esperado


class TestCalcularEstrellas:
    def test_sin_intentos(self):
        assert _calcular_estrellas(0, 0) == 0

    @pytest.mark.parametrize("aciertos,intentos,esperado", [
        (0, 10, 0),    # 0%
        (1, 10, 0),    # 10%
        (2, 10, 1),    # 20% -> 1 estrella
        (4, 10, 2),    # 40% -> 2
        (6, 10, 3),    # 60% -> 3
        (8, 10, 4),    # 80% -> 4
        (9, 10, 5),    # 90% -> 5
        (10, 10, 5),   # 100% -> 5
    ])
    def test_estrellas(self, aciertos, intentos, esperado):
        assert _calcular_estrellas(aciertos, intentos) == esperado


class TestSignalProgresoCategoria:
    def test_crea_fila_si_no_existe(self, db, estudiante_user):
        """Al crear una Respuesta, se crea ProgresoCategoria."""
        assert ProgresoCategoria.objects.filter(user=estudiante_user).count() == 0

        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="A", es_correcta=True,
            puntuacion=10, tiempo_segundos=15, intento_numero=1,
        )

        prog = ProgresoCategoria.objects.get(
            user=estudiante_user, categoria="multiple_choice",
        )
        assert prog.intentos == 1
        assert prog.aciertos == 1

    def test_incrementa_si_ya_existe(self, db, estudiante_user):
        """Segunda respuesta actualiza la fila existente."""
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="A", es_correcta=True,
            puntuacion=10, tiempo_segundos=15, intento_numero=1,
        )
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=2, respuesta_usuario="B", es_correcta=False,
            puntuacion=0, tiempo_segundos=20, intento_numero=1,
        )

        prog = ProgresoCategoria.objects.get(
            user=estudiante_user, categoria="multiple_choice",
        )
        assert prog.intentos == 2
        assert prog.aciertos == 1

    def test_respuesta_incorrecta_solo_suma_intentos(self, db, estudiante_user):
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="completar",
            item_id=1, respuesta_usuario="X", es_correcta=False,
            puntuacion=0, tiempo_segundos=10, intento_numero=1,
        )
        prog = ProgresoCategoria.objects.get(
            user=estudiante_user, categoria="completar",
        )
        assert prog.intentos == 1
        assert prog.aciertos == 0
        assert prog.nivel_dominio == 1

    def test_categorias_separadas(self, db, estudiante_user):
        """Respuestas de tipos distintos van a filas distintas."""
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="A",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="B",
            item_id=1, respuesta_usuario="y", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        assert ProgresoCategoria.objects.filter(user=estudiante_user).count() == 2

    def test_no_actualiza_en_update(self, db, estudiante_user):
        """Modificar una Respuesta existente NO debe re-incrementar."""
        r = Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        prog_inicial = ProgresoCategoria.objects.get(
            user=estudiante_user, categoria="multiple_choice",
        )
        assert prog_inicial.intentos == 1

        # Modificar (no crear) — el signal solo actúa en created=True
        r.respuesta_usuario = "modificada"
        r.save()

        prog_final = ProgresoCategoria.objects.get(
            user=estudiante_user, categoria="multiple_choice",
        )
        assert prog_final.intentos == 1  # Sin cambio

    def test_multiples_usuarios(self, db, estudiante_user, prof_user):
        """Progreso independiente por usuario."""
        Respuesta.objects.create(
            user=estudiante_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        Respuesta.objects.create(
            user=prof_user, tipo_ejercicio="multiple_choice",
            item_id=1, respuesta_usuario="x", es_correcta=True,
            puntuacion=10, tiempo_segundos=10, intento_numero=1,
        )
        assert ProgresoCategoria.objects.filter(
            categoria="multiple_choice",
        ).count() == 2