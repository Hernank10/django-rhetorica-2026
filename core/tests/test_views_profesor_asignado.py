"""Tests de filtro profesor_asignado en lista_estudiantes_metricas."""
from datetime import date

from django.apps import apps
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class TestFiltroProfesorAsignado(TestCase):
    @classmethod
    def setUpTestData(cls):
        Curso = apps.get_model("core", "Curso")
        Modulo = apps.get_model("core", "Modulo")
        Leccion = apps.get_model("core", "Leccion")
        ProgresoUsuario = apps.get_model("core", "ProgresoUsuario")

        g_prof, _ = Group.objects.get_or_create(name="Profesor")
        g_est, _ = Group.objects.get_or_create(name="Estudiante")

        # 2 profesores
        cls.prof1 = User.objects.create_user(
            username="prof_test_1", password="Test1234!"
        )
        cls.prof1.groups.add(g_prof)
        cls.prof2 = User.objects.create_user(
            username="prof_test_2", password="Test1234!"
        )
        cls.prof2.groups.add(g_prof)

        # 1 admin
        cls.admin = User.objects.create_user(
            username="admin_test", password="Test1234!", is_superuser=True
        )
        cls.admin.groups.add(g_prof)

        # 2 cursos: uno de cada prof
        cls.curso1 = Curso.objects.create(
            titulo="Curso del Prof1",
            slug="curso-prof1-test",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="publicado",
            creado_por=cls.prof1,
            profesor_asignado=cls.prof1,
        )
        cls.curso2 = Curso.objects.create(
            titulo="Curso del Prof2",
            slug="curso-prof2-test",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="publicado",
            creado_por=cls.prof2,
            profesor_asignado=cls.prof2,
        )

        # modulos + lecciones
        cls.mod1 = Modulo.objects.create(curso=cls.curso1, titulo="M1", orden=1)
        cls.mod2 = Modulo.objects.create(curso=cls.curso2, titulo="M2", orden=1)
        cls.lec1 = Leccion.objects.create(
            modulo=cls.mod1, titulo="L1", contenido="c", tipo="teoria", orden=1
        )
        cls.lec2 = Leccion.objects.create(
            modulo=cls.mod2, titulo="L2", contenido="c", tipo="teoria", orden=1
        )

        # 2 estudiantes: uno en cada curso
        cls.est1 = User.objects.create_user(
            username="est_del_prof1", password="Test1234!"
        )
        cls.est1.groups.add(g_est)
        cls.est2 = User.objects.create_user(
            username="est_del_prof2", password="Test1234!"
        )
        cls.est2.groups.add(g_est)

        ProgresoUsuario.objects.create(
            usuario=cls.est1, leccion=cls.lec1, completado=True,
            puntaje_obtenido=80, ultima_actividad=date.today(),
        )
        ProgresoUsuario.objects.create(
            usuario=cls.est2, leccion=cls.lec2, completado=True,
            puntaje_obtenido=90, ultima_actividad=date.today(),
        )

    def setUp(self):
        self.client.force_login(self.prof1)

    def _get_estudiantes_usernames(self, response):
        return {e.username for e in response.context["estudiantes"]}

    def test_superuser_ve_todos(self):
        """Admin ve todos los estudiantes (con o sin curso asignado)."""
        self.client.force_login(self.admin)
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        assert r.status_code == 200
        assert r.context["es_superuser"] is True
        usernames = self._get_estudiantes_usernames(r)
        assert "est_del_prof1" in usernames
        assert "est_del_prof2" in usernames
        # Verifica que el dropdown muestra todos los cursos
        cursos_en_context = [c.id for c in r.context["cursos"]]
        assert self.curso1.id in cursos_en_context
        assert self.curso2.id in cursos_en_context

    def test_profesor_ve_solo_sus_cursos(self):
        """Prof1 solo ve estudiantes con progreso en sus cursos."""
        r = self.client.get(reverse("profesor:estudiantes_metricas"))
        assert r.status_code == 200
        assert r.context["es_superuser"] is False
        usernames = self._get_estudiantes_usernames(r)
        assert "est_del_prof1" in usernames
        assert "est_del_prof2" not in usernames
        # Dropdown solo muestra cursos del prof1
        cursos_en_context = [c.id for c in r.context["cursos"]]
        assert self.curso1.id in cursos_en_context
        assert self.curso2.id not in cursos_en_context