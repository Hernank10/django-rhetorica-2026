"""Tests de core/services/analytics.py."""

from datetime import timedelta

import pytest
from django.utils import timezone

from core.models import (
    Respuesta, ProgresoCategoria, Logro, LogroObtenido,
    Certificacion, CertificacionObtenida,
)
from core.models_adaptativos import HistorialErrorSintactico
from core.services import analytics


@pytest.fixture
def usuarios(db, estudiante_user, prof_user):
    return [estudiante_user, prof_user]


def _respuesta(user, cat="multiple_choice", correcta=True, seg=10, dias=0):
    return Respuesta.objects.create(
        user=user,
        tipo_ejercicio=cat,
        item_id=1,
        respuesta_usuario="x",
        es_correcta=correcta,
        puntuacion=10 if correcta else 0,
        tiempo_segundos=seg,
        fecha=timezone.now() - timedelta(days=dias),
        intento_numero=1,
    )


class TestHeatmapPorAlumno:
    def test_sin_datos(self, db, usuarios):
        r = analytics.heatmap_categoria_por_alumno(usuarios)
        assert r == {"usuarios": [], "categorias": [], "valores": []}

    def test_un_alumno_una_categoria(self, db, usuarios):
        _respuesta(usuarios[0], correcta=True)
        r = analytics.heatmap_categoria_por_alumno(usuarios)
        assert len(r["usuarios"]) == 1
        assert r["categorias"] == ["multiple_choice"]
        assert r["valores"][0][0] == 100.0

    def test_varias_categorias(self, db, usuarios):
        _respuesta(usuarios[0], cat="A")
        _respuesta(usuarios[0], cat="B")
        r = analytics.heatmap_categoria_por_alumno(usuarios)
        assert sorted(r["categorias"]) == ["A", "B"]

    def test_calcula_tasa(self, db, usuarios):
        _respuesta(usuarios[0], correcta=True)
        _respuesta(usuarios[0], correcta=False)
        _respuesta(usuarios[0], correcta=True)
        r = analytics.heatmap_categoria_por_alumno(usuarios)
        # 2/3 = 66.7%
        assert r["valores"][0][0] == 66.7

    def test_filtra_por_dias(self, db, usuarios):
        _respuesta(usuarios[0], dias=1)
        _respuesta(usuarios[0], dias=60)  # fuera de ventana
        r = analytics.heatmap_categoria_por_alumno(usuarios, dias=30)
        assert r["valores"][0][0] == 100.0

    def test_multiples_usuarios(self, db, usuarios):
        _respuesta(usuarios[0])
        _respuesta(usuarios[1])
        r = analytics.heatmap_categoria_por_alumno(usuarios)
        assert len(r["usuarios"]) == 2


class TestHeatmapPorGrupo:
    def test_sin_datos(self, db, usuarios):
        assert analytics.heatmap_categoria_por_grupo(usuarios) == []

    def test_agrega_por_categoria(self, db, usuarios):
        _respuesta(usuarios[0], cat="A", correcta=True)
        _respuesta(usuarios[1], cat="A", correcta=False)
        r = analytics.heatmap_categoria_por_grupo(usuarios)
        assert len(r) == 1
        assert r[0]["categoria"] == "A"
        assert r[0]["total"] == 2
        assert r[0]["aciertos"] == 1
        assert r[0]["tasa"] == 50.0

    def test_ordenado_desc(self, db, usuarios):
        _respuesta(usuarios[0], cat="A", correcta=True)
        _respuesta(usuarios[0], cat="B", correcta=False)
        r = analytics.heatmap_categoria_por_grupo(usuarios)
        assert r[0]["categoria"] == "A"


class TestTiempoPromedio:
    def test_sin_datos(self, db, usuarios):
        assert analytics.tiempo_promedio_por_categoria(usuarios) == []

    def test_calcula_promedio(self, db, usuarios):
        _respuesta(usuarios[0], cat="A", seg=10)
        _respuesta(usuarios[0], cat="A", seg=20)
        r = analytics.tiempo_promedio_por_categoria(usuarios)
        assert r[0]["tiempo_promedio_seg"] == 15.0
        assert r[0]["n_respuestas"] == 2

    def test_ordenado_desc(self, db, usuarios):
        _respuesta(usuarios[0], cat="A", seg=5)
        _respuesta(usuarios[0], cat="B", seg=50)
        r = analytics.tiempo_promedio_por_categoria(usuarios)
        assert r[0]["categoria"] == "B"


class TestRetencion:
    def test_sin_datos(self, db, usuarios):
        assert analytics.retencion_semanal(usuarios) == []

    def test_una_semana(self, db, usuarios):
        _respuesta(usuarios[0], dias=1)
        r = analytics.retencion_semanal(usuarios, semanas=4)
        assert len(r) == 1
        assert r[0]["activos"] == 1
        assert r[0]["total_respuestas"] == 1

    def test_multiples_semanas(self, db, usuarios):
        _respuesta(usuarios[0], dias=1)
        _respuesta(usuarios[0], dias=10)
        r = analytics.retencion_semanal(usuarios, semanas=4)
        assert len(r) >= 2


class TestTopErrores:
    def test_sin_datos(self, db):
        assert analytics.top_errores_por_idioma() == []

    def test_agrupa(self, db, estudiante_user, prof_user):
        HistorialErrorSintactico.objects.create(
            estudiante=estudiante_user, idioma="LA",
            categoria_gramatical="ablativo_instrumental",
        )
        HistorialErrorSintactico.objects.create(
            estudiante=prof_user, idioma="LA",
            categoria_gramatical="ablativo_instrumental",
        )
        r = analytics.top_errores_por_idioma("LA")
        assert len(r) == 1
        assert r[0]["n_alumnos"] == 2

    def test_filtra_resueltos(self, db, estudiante_user):
        HistorialErrorSintactico.objects.create(
            estudiante=estudiante_user, idioma="LA",
            categoria_gramatical="X", resuelto=True,
        )
        assert analytics.top_errores_por_idioma("LA") == []

    def test_filtra_idioma(self, db, estudiante_user):
        HistorialErrorSintactico.objects.create(
            estudiante=estudiante_user, idioma="ES",
            categoria_gramatical="Y",
        )
        assert analytics.top_errores_por_idioma("LA") == []
        assert len(analytics.top_errores_por_idioma("ES")) == 1


class TestResumenAlumno:
    def test_sin_datos(self, db, estudiante_user):
        r = analytics.resumen_alumno(estudiante_user)
        assert r == {
            "progreso": [], "logros": [],
            "certificaciones": [], "historial_errores": [],
        }

    def test_con_progreso(self, db, estudiante_user):
        ProgresoCategoria.objects.create(
            user=estudiante_user, categoria="A",
            aciertos=5, intentos=10, nivel_dominio=3,
        )
        r = analytics.resumen_alumno(estudiante_user)
        assert len(r["progreso"]) == 1
        assert r["progreso"][0]["aciertos"] == 5

    def test_con_logro_y_cert(self, db, estudiante_user):
        logro = Logro.objects.create(
            nombre="L", descripcion="d", tipo="insignia", icono="fa-x",
        )
        LogroObtenido.objects.create(user=estudiante_user, logro=logro)
        cert = Certificacion.objects.create(
            nombre="C", descripcion="d", nivel="oro",
        )
        CertificacionObtenida.objects.create(
            user=estudiante_user, certificacion=cert,
            codigo_verificacion="V-1",
        )
        r = analytics.resumen_alumno(estudiante_user)
        assert len(r["logros"]) == 1
        assert len(r["certificaciones"]) == 1

    def test_con_historial(self, db, estudiante_user):
        HistorialErrorSintactico.objects.create(
            estudiante=estudiante_user, idioma="LA",
            categoria_gramatical="Z",
        )
        r = analytics.resumen_alumno(estudiante_user)
        assert len(r["historial_errores"]) == 1