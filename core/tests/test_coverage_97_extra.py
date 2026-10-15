"""Cobertura al 97%.

Sin try/except, sin loops, sin helpers dinamicos.
"""
from unittest.mock import MagicMock, patch

from django.test import RequestFactory

from core.models import EjercicioLinguistico
from core.views_ejercicios import (
    detalle_ejercicio,
    practicar_ejercicio,
    api_ejercicio_detalle,
)
from core.templatetags.custom_filters import total_lecciones, total_modulos


def _ejercicio(contenido):
    return EjercicioLinguistico.objects.create(
        titulo="Test", categoria="sintaxis", tipo="multiple_choice",
        nivel=1, puntos=10, contenido=contenido,
    )


class TestViewsEjercicios97:
    """Cubre views_ejercicios.py."""

    def test_detalle_contenido_no_dict(self, db, estudiante_user):
        ej = _ejercicio("texto plano")
        request = RequestFactory().get("/")
        request.user = estudiante_user
        with patch("core.views_ejercicios.render", return_value="ok"):
            assert detalle_ejercicio.__wrapped__(request, ej.id) == "ok"

    def test_practicar_contenido_no_dict(self, db, estudiante_user):
        ej = _ejercicio("otro texto")
        request = RequestFactory().get("/")
        request.user = estudiante_user
        with patch("core.views_ejercicios.render", return_value="ok"):
            assert practicar_ejercicio.__wrapped__(request, ej.id) == "ok"

    def test_api_detalle_json(self, db, estudiante_user):
        ej = _ejercicio({"clave": "valor"})
        request = RequestFactory().get("/")
        request.user = estudiante_user
        r = api_ejercicio_detalle.__wrapped__(request, ej.id)
        assert r.status_code == 200


class TestCustomFilters97:
    """Cubre custom_filters.py usando MagicMock (no fakes a mano)."""

    def test_total_lecciones(self, db):
        modulo = MagicMock()
        modulo.lecciones.count.return_value = 4
        curso = MagicMock()
        curso.modulos.all.return_value = [modulo, modulo, modulo]
        assert total_lecciones(curso) == 12

    def test_total_modulos(self, db):
        curso = MagicMock()
        curso.modulos.count.return_value = 5
        assert total_modulos(curso) == 5