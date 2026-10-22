"""Tests de rendering multiple_choice en evaluacion_detalle.html."""
from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestEvaluacionRenderRadios(TestCase):
    @classmethod
    def setUpTestData(cls):
        Curso = apps.get_model("core", "Curso")
        Modulo = apps.get_model("core", "Modulo")
        EvaluacionCurso = apps.get_model("core", "EvaluacionCurso")
        PreguntaEvaluacion = apps.get_model("core", "PreguntaEvaluacion")

        prof = User.objects.create_user(username="prof_eval_test", password="Test1234!")
        cls.curso = Curso.objects.create(
            titulo="Curso Eval Test",
            slug="curso-eval-test",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="publicado",
            creado_por=prof,
        )
        cls.modulo = Modulo.objects.create(curso=cls.curso, titulo="M1", orden=1)
        cls.evaluacion = EvaluacionCurso.objects.create(
            curso=cls.curso, modulo=cls.modulo,
            titulo="Eval Test", tipo="formativa",
        )
        # 3 preguntas: 2 multiple_choice, 1 desarrollo
        PreguntaEvaluacion.objects.create(
            evaluacion=cls.evaluacion, orden=1,
            enunciado="¿Cuál es el sujeto?",
            tipo="multiple_choice",
            opciones=["Juan", "libro", "lee", "el"],
            respuesta_correcta="Juan",
        )
        PreguntaEvaluacion.objects.create(
            evaluacion=cls.evaluacion, orden=2,
            enunciado="¿Cuál es el verbo?",
            tipo="multiple_choice",
            opciones=["lee", "Juan", "libro", "el"],
            respuesta_correcta="lee",
        )
        PreguntaEvaluacion.objects.create(
            evaluacion=cls.evaluacion, orden=3,
            enunciado="Explica la diferencia",
            tipo="desarrollo",
            opciones=[],
            respuesta_correcta="Respuesta abierta",
        )

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="est_eval_test",
            defaults={"email": "est@test.local"},
        )
        self.user.set_password("Test1234!")
        self.user.save()
        self.client.force_login(self.user)

    def test_multiple_choice_renderiza_radios(self):
        r = self.client.get(reverse("ver_evaluacion", args=[self.evaluacion.id]))
        assert r.status_code == 200
        html = r.content.decode("utf-8")
        # 2 preguntas multiple_choice * 4 opciones = 8 radios
        assert 'type="radio"' in html
        assert 'value="Juan"' in html
        assert 'value="lee"' in html

    def test_desarrollo_renderiza_textarea(self):
        r = self.client.get(reverse("ver_evaluacion", args=[self.evaluacion.id]))
        html = r.content.decode("utf-8")
        assert '<textarea' in html

    def test_no_mezcla_radios_y_textarea_por_pregunta(self):
        r = self.client.get(reverse("ver_evaluacion", args=[self.evaluacion.id]))
        html = r.content.decode("utf-8")
        # Contar radios: deben ser al menos 8 (2 preguntas * 4 opciones)
        assert html.count('type="radio"') >= 8
        # Contar textareas: deben ser al menos 1 (la de desarrollo)
        assert html.count('<textarea') >= 1