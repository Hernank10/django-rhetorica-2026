"""Tests de core/services/corpus.py - funciones puras."""
import pytest

from core.services.corpus import (
    concordancias,
    corpus_desde_etimos,
    frecuencias,
    n_gramas,
    tokenizar,
)


class TestTokenizar:
    def test_vacio(self):
        assert tokenizar("") == []

    def test_none(self):
        assert tokenizar(None) == []

    def test_puntuacion(self):
        assert tokenizar("Hola, mundo. Como estas?") == ["hola", "mundo", "como", "estas"]

    def test_acentos(self):
        assert tokenizar("cancion accion") == ["cancion", "accion"]

    def test_numeros_excluidos(self):
        assert tokenizar("Tengo 3 gatos y 2 perros") == ["tengo", "gatos", "y", "perros"]


class TestFrecuencias:
    def test_vacio(self):
        assert frecuencias([]) == {}

    def test_simple(self):
        assert frecuencias(["hola hola mundo"]) == {"hola": 2, "mundo": 1}

    def test_varios_textos(self):
        r = frecuencias(["uno dos", "dos tres"])
        assert r == {"uno": 1, "dos": 2, "tres": 1}


class TestConcordancias:
    def test_vacio(self):
        assert concordancias("", "gato") == []
        assert concordancias("texto", "") == []
        assert concordancias("", "") == []

    def test_sin_match(self):
        assert concordancias("el perro come", "gato") == []

    def test_un_match(self):
        r = concordancias("el gato come pescado", "gato", contexto=2)
        assert len(r) == 1
        assert r[0]["palabra"] == "gato"
        assert r[0]["izq"] == "el"
        assert r[0]["der"] == "come pescado"

    def test_varios_matches(self):
        r = concordancias("gato y gato y gato", "gato", contexto=1)
        assert len(r) == 3


class TestNGramas:
    def test_vacio(self):
        assert n_gramas([]) == []

    def test_bigramas(self):
        r = n_gramas(["el gato come el gato come"], n=2, top=3)
        assert r[0] == (("el", "gato"), 2)
        assert r[1] == (("gato", "come"), 2)

    def test_trigramas(self):
        r = n_gramas(["el gato come pescado"], n=3, top=5)
        assert (("el", "gato", "come"), 1) in r


class TestCorpusDesdeEtimos:
    def test_100_items(self):
        # 50 etimos x 2 campos (regla, ejemplo)
        items = corpus_desde_etimos()
        assert len(items) == 100

    def test_fuentes_correctas(self):
        items = corpus_desde_etimos()
        fuentes = {it["fuente"] for it in items}
        assert fuentes == {"etimologia_regla", "etimologia_ejemplo"}

@pytest.mark.django_db
class TestCorpusDesdeBD:
    def test_vacio_para_usuario_sin_datos(self):
        # En suite completa la BD tiene fixtures de otros modulos.
        # Verificamos que un usuario nuevo no aporta items de evaluacion/flashcard.
        from django.contrib.auth import get_user_model
        from core.services.corpus import corpus_desde_bd

        User = get_user_model()
        user = User.objects.create_user(username="corp_vacio", password="x")
        items = corpus_desde_bd()
        # Ningun item debe referenciar a este usuario
        de_usuario = [
            it for it in items
            if it["fuente"].startswith(("evaluacion_", "flashcard_"))
            and str(user.pk) in str(it["id"])
        ]
        assert de_usuario == []

    def test_un_ejercicio(self):
        from core.models import EjercicioLinguistico
        from core.services.corpus import corpus_desde_bd

        ej = EjercicioLinguistico.objects.create(
            titulo="Test",
            contenido={
                "enunciado": "Escribe una oracion simple",
                "teoria": "Sujeto + verbo",
            },
            categoria="gramatica",
            tipo="multiple_choice",
            nivel=1,
            puntos=5,
            idioma="ES",
        )
        items = corpus_desde_bd()
        de_mi_ejercicio = [
            it for it in items
            if it["fuente"].startswith("ejercicio_") and it["id"] == ej.pk
        ]
        fuentes = {it["fuente"] for it in de_mi_ejercicio}
        assert fuentes == {"ejercicio_enunciado", "ejercicio_teoria"}
        assert len(de_mi_ejercicio) == 2

    def test_una_evaluacion(self):
        from django.contrib.auth import get_user_model
        from core.models import EjercicioLinguistico, EvaluacionRedaccion
        from core.services.corpus import corpus_desde_bd

        User = get_user_model()
        user = User.objects.create_user(username="corp_u1", password="x")
        ej = EjercicioLinguistico.objects.create(
            titulo="Ej", contenido={}, categoria="redaccion",
            tipo="produccion_libre", nivel=2, puntos=10,
            es_redaccion=True, idioma="ES",
        )
        EvaluacionRedaccion.objects.create(
            estudiante=user, ejercicio=ej,
            texto_estudiante="Juan estudia", aprobado=True,
            feedback="Correcto",
        )
        items = corpus_desde_bd()
        fuentes = {it["fuente"] for it in items}
        assert "evaluacion_texto" in fuentes
        assert "evaluacion_feedback" in fuentes

    def test_una_flashcard(self):
        from django.contrib.auth import get_user_model
        from core.models import Flashcard
        from core.services.corpus import corpus_desde_bd

        User = get_user_model()
        user = User.objects.create_user(username="corp_u2", password="x")
        Flashcard.objects.create(
            estudiante=user, idioma="ES", tipo="vocabulario",
            frente="efimero", reverso="que dura muy poco",
        )
        items = corpus_desde_bd()
        fuentes = {it["fuente"] for it in items}
        assert "flashcard_frente" in fuentes
        assert "flashcard_reverso" in fuentes

    def test_fuentes_constant(self):
        from core.services.corpus import FUENTES
        assert len(FUENTES) == 10
        assert "ejercicio_enunciado" in FUENTES
        assert "etimologia_regla" in FUENTES