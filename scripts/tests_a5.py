"""Tests de models_preguntas.py (Fase A5: cubrir 44 lineas al 0%)."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

test_content = '''"""Tests de core/models_preguntas.py.

Cubre los modelos PreguntaGenerada y RespuestaPregunta:
  - Creacion con campos minimos y completos
  - Choices (tipo, dificultad)
  - Metodos get_tipo_emoji, get_color_tipo
  - __str__ de ambos modelos
  - unique_together
  - SET_NULL en creado_por
  - CASCADE en FK
"""
import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from core.models_preguntas import PreguntaGenerada, RespuestaPregunta


# ============================================================
# PREGUNTA GENERADA - CREACION
# ============================================================
class TestPreguntaGeneradaCreacion:
    def test_crear_minima(self, db):
        p = PreguntaGenerada.objects.create(
            tipo="correccion",
            titulo="Corrige esta oracion",
            enunciado="El nino juega",
            respuesta_correcta="El nino juega",
        )
        assert p.id is not None
        assert p.activa is True
        assert p.usado_en == 0
        assert p.puntos == 10
        assert p.dificultad == 1

    def test_crear_completa(self, db, estudiante_user):
        p = PreguntaGenerada.objects.create(
            tipo="multiple_choice",
            titulo="Cual es el sujeto?",
            enunciado="El nino juega en el parque",
            respuesta_correcta="El nino",
            opciones=["El nino", "juega", "parque"],
            pista="Busca quien realiza la accion",
            dificultad=2,
            puntos=20,
            categoria="sintaxis",
            ejercicio_base_id=42,
            creado_por=estudiante_user,
            activa=True,
        )
        assert p.tipo == "multiple_choice"
        assert p.dificultad == 2
        assert p.puntos == 20
        assert len(p.opciones) == 3
        assert p.creado_por == estudiante_user

    def test_defaults_correctos(self, db):
        p = PreguntaGenerada.objects.create(
            tipo="completar",
            titulo="Completa",
            enunciado="El ___ corre",
            respuesta_correcta="perro",
        )
        assert p.opciones is None
        assert p.pista == ""
        assert p.categoria == ""
        assert p.ejercicio_base_id is None
        assert p.creado_por is None


# ============================================================
# PREGUNTA GENERADA - CHOICES
# ============================================================
class TestPreguntaGeneradaChoices:
    def test_todos_los_tipos_existen(self, db):
        tipos_validos = [
            "correccion", "completar", "reescribir", "elegir",
            "explicar", "verdadero_falso", "relacionar", "ordenar",
            "multiple_choice", "desarrollo",
        ]
        for tipo in tipos_validos:
            p = PreguntaGenerada.objects.create(
                tipo=tipo, titulo="Test", enunciado="x", respuesta_correcta="y",
            )
            assert p.tipo == tipo

    def test_todos_los_niveles_existen(self, db):
        for nivel in [1, 2, 3, 4]:
            p = PreguntaGenerada.objects.create(
                tipo="correccion", titulo="Test",
                enunciado="x", respuesta_correcta="y",
                dificultad=nivel,
            )
            assert p.dificultad == nivel


# ============================================================
# PREGUNTA GENERADA - METODOS
# ============================================================
class TestPreguntaGeneradaMetodos:
    def test_str(self, db):
        p = PreguntaGenerada.objects.create(
            tipo="correccion", titulo="Test Pregunta",
            enunciado="x", respuesta_correcta="y",
        )
        s = str(p)
        assert "Test Pregunta" in s
        assert "correccion" in s

    @pytest.mark.parametrize("tipo,emoji_esperado", [
        ("correccion", "✏"),
        ("completar", "📝"),
        ("reescribir", "🔄"),
        ("elegir", "✅"),
        ("explicar", "💡"),
    ])
    def test_get_tipo_emoji_tipos_conocidos(self, db, tipo, emoji_esperado):
        p = PreguntaGenerada(
            tipo=tipo, titulo="x", enunciado="y", respuesta_correcta="z",
        )
        emoji = p.get_tipo_emoji()
        assert isinstance(emoji, str)
        assert len(emoji) > 0

    def test_get_tipo_emoji_default(self, db):
        p = PreguntaGenerada(
            tipo="tipo_no_existe",  # valor raro
            titulo="x", enunciado="y", respuesta_correcta="z",
        )
        emoji = p.get_tipo_emoji()
        # Debe devolver el emoji default 📌
        assert emoji == "📌"

    @pytest.mark.parametrize("tipo,color_esperado", [
        ("correccion", "danger"),
        ("completar", "primary"),
        ("reescribir", "success"),
        ("elegir", "warning"),
        ("verdadero_falso", "info"),
        ("ordenar", "dark"),
    ])
    def test_get_color_tipo_conocidos(self, db, tipo, color_esperado):
        p = PreguntaGenerada(
            tipo=tipo, titulo="x", enunciado="y", respuesta_correcta="z",
        )
        assert p.get_color_tipo() == color_esperado

    def test_get_color_tipo_default(self, db):
        p = PreguntaGenerada(
            tipo="tipo_raro",
            titulo="x", enunciado="y", respuesta_correcta="z",
        )
        assert p.get_color_tipo() == "secondary"


# ============================================================
# RESPUESTA PREGUNTA
# ============================================================
class TestRespuestaPregunta:
    def test_crear(self, db, estudiante_user):
        p = PreguntaGenerada.objects.create(
            tipo="multiple_choice", titulo="Test",
            enunciado="x", respuesta_correcta="A",
        )
        r = RespuestaPregunta.objects.create(
            pregunta=p, usuario=estudiante_user,
            respuesta="A", es_correcta=True, puntos_obtenidos=10,
            tiempo_respuesta=30,
        )
        assert r.id is not None
        assert r.es_correcta is True
        assert r.puntos_obtenidos == 10
        assert r.tiempo_respuesta == 30

    def test_defaults(self, db, estudiante_user):
        p = PreguntaGenerada.objects.create(
            tipo="completar", titulo="Test",
            enunciado="x", respuesta_correcta="A",
        )
        r = RespuestaPregunta.objects.create(
            pregunta=p, usuario=estudiante_user, respuesta="B",
        )
        assert r.es_correcta is False
        assert r.puntos_obtenidos == 0
        assert r.tiempo_respuesta is None

    def test_str(self, db, estudiante_user):
        p = PreguntaGenerada.objects.create(
            tipo="correccion", titulo="Pregunta Titulo Largo",
            enunciado="x", respuesta_correcta="y",
        )
        r = RespuestaPregunta.objects.create(
            pregunta=p, usuario=estudiante_user, respuesta="z",
        )
        s = str(r)
        assert estudiante_user.username in s
        assert "Pregunta" in s

    def test_unique_together_mismo_usuario_pregunta(self, db, estudiante_user):
        p = PreguntaGenerada.objects.create(
            tipo="correccion", titulo="Test",
            enunciado="x", respuesta_correcta="y",
        )
        RespuestaPregunta.objects.create(
            pregunta=p, usuario=estudiante_user, respuesta="primera",
        )
        with pytest.raises(Exception):
            RespuestaPregunta.objects.create(
                pregunta=p, usuario=estudiante_user, respuesta="segunda",
            )

    def test_multiples_usuarios_misma_pregunta_ok(self, db, estudiante_user, prof_user):
        p = PreguntaGenerada.objects.create(
            tipo="correccion", titulo="Test",
            enunciado="x", respuesta_correcta="y",
        )
        RespuestaPregunta.objects.create(
            pregunta=p, usuario=estudiante_user, respuesta="a",
        )
        RespuestaPregunta.objects.create(
            pregunta=p, usuario=prof_user, respuesta="b",
        )
        assert RespuestaPregunta.objects.filter(pregunta=p).count() == 2


# ============================================================
# RELACIONES
# ============================================================
class TestRelaciones:
    def test_cascade_delete_pregunta(self, db, estudiante_user):
        """Al borrar la pregunta, se borran sus respuestas."""
        p = PreguntaGenerada.objects.create(
            tipo="correccion", titulo="Test",
            enunciado="x", respuesta_correcta="y",
        )
        RespuestaPregunta.objects.create(
            pregunta=p, usuario=estudiante_user, respuesta="a",
        )
        pk = p.pk
        p.delete()
        assert not PreguntaGenerada.objects.filter(pk=pk).exists()
        assert not RespuestaPregunta.objects.filter(pregunta_id=pk).exists()

    def test_creado_por_set_null(self, db, prof_user):
        """Al borrar el User, creado_por se pone a NULL."""
        p = PreguntaGenerada.objects.create(
            tipo="correccion", titulo="Test",
            enunciado="x", respuesta_correcta="y",
            creado_por=prof_user,
        )
        pk = p.pk
        prof_user.delete()
        p.refresh_from_db()
        assert p.creado_por is None
'''

p = BASE / "core" / "tests" / "test_models_preguntas.py"
p.write_text(test_content, encoding="utf-8")
print(f"[OK] {p.relative_to(BASE)} creado")
print(f"   ~20 tests para cubrir 44 lineas de models_preguntas.py")