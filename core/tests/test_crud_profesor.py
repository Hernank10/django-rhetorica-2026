"""Tests del CRUD del profesor: permisos + vistas GET.

Los tests POST se añadirán en una segunda iteración tras inspeccionar
los campos exactos que espera cada *_form().
"""
from django.apps import apps
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


def crear_usuario_con_grupo(username, grupo_nombre):
    """Crea usuario y lo añade al grupo indicado (crea el grupo si no existe)."""
    u = User.objects.create_user(username=username, password="x")
    grupo, _ = Group.objects.get_or_create(name=grupo_nombre)
    u.groups.add(grupo)
    return u


class BaseProfesorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Curso = apps.get_model("core", "Curso")
        Modulo = apps.get_model("core", "Modulo")
        Leccion = apps.get_model("core", "Leccion")
        EvaluacionCurso = apps.get_model("core", "EvaluacionCurso")

        cls.prof = crear_usuario_con_grupo("prof_test_crud", "Profesor")
        cls.est = crear_usuario_con_grupo("est_test_crud", "Estudiante")

        curso_kwargs = dict(
            titulo="Curso Test CRUD", slug="curso-test-crud",
            descripcion="d", objetivo="o",
            nivel="principiante", estado="borrador",
        )
        if hasattr(Curso, "creado_por"):
            curso_kwargs["creado_por"] = cls.prof
        cls.curso = Curso.objects.create(**curso_kwargs)
        # Asignar profesor si el modelo lo tiene
        if hasattr(Curso, "profesor_asignado"):
            cls.curso.profesor_asignado = cls.prof
            cls.curso.save(update_fields=["profesor_asignado"])

        cls.mod = Modulo.objects.create(curso=cls.curso, titulo="M1", orden=1)
        cls.lec = Leccion.objects.create(
            modulo=cls.mod, titulo="L1", contenido="c",
            tipo="teoria", orden=1,
        )
        cls.eval = EvaluacionCurso.objects.create(
            curso=cls.curso, titulo="Eval Test", tipo="formativa",
        )


class TestPermisosEstudiante(BaseProfesorTest):
    """Estudiante autenticado (NO profesor) → 403 en todo el CRUD."""

    def setUp(self):
        self.client.force_login(self.est)

    def _assert_403(self, url_name, *args):
        url = reverse(url_name, args=args) if args else reverse(url_name)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 403, f"{url_name} debe ser 403")

    def test_dashboard_403(self):
        self._assert_403("profesor:dashboard")

    def test_cursos_lista_403(self):
        self._assert_403("profesor:cursos_lista")

    def test_curso_crear_403(self):
        self._assert_403("profesor:curso_crear")

    def test_curso_editar_403(self):
        self._assert_403("profesor:curso_editar", self.curso.id)

    def test_curso_eliminar_403(self):
        self._assert_403("profesor:curso_eliminar", self.curso.id)

    def test_modulo_crear_403(self):
        self._assert_403("profesor:modulo_crear")

    def test_leccion_crear_403(self):
        self._assert_403("profesor:leccion_crear")

    def test_evaluacion_crear_403(self):
        self._assert_403("profesor:evaluacion_crear")


class TestAnonimoRedirige(BaseProfesorTest):
    """Anónimo → 302 a login (no 403)."""

    def test_cursos_lista_redirige_a_login(self):
        r = self.client.get(reverse("profesor:cursos_lista"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("login", r.url)


class TestVistasProfesor(BaseProfesorTest):
    """Profesor autenticado → 200 en vistas GET."""

    def setUp(self):
        self.client.force_login(self.prof)

    def test_dashboard_200(self):
        r = self.client.get(reverse("profesor:dashboard"))
        self.assertEqual(r.status_code, 200)

    def test_cursos_lista_200(self):
        r = self.client.get(reverse("profesor:cursos_lista"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Curso Test CRUD")

    def test_curso_crear_get_200(self):
        r = self.client.get(reverse("profesor:curso_crear"))
        self.assertEqual(r.status_code, 200)

    def test_curso_editar_get_200(self):
        r = self.client.get(reverse("profesor:curso_editar", args=[self.curso.id]))
        self.assertEqual(r.status_code, 200)

    def test_modulos_lista_200(self):
        r = self.client.get(reverse("profesor:modulos_lista"))
        self.assertEqual(r.status_code, 200)

    def test_modulo_crear_get_200(self):
        r = self.client.get(reverse("profesor:modulo_crear"))
        self.assertEqual(r.status_code, 200)

    def test_modulo_editar_get_200(self):
        r = self.client.get(reverse("profesor:modulo_editar", args=[self.mod.id]))
        self.assertEqual(r.status_code, 200)

    def test_lecciones_lista_200(self):
        r = self.client.get(reverse("profesor:lecciones_lista"))
        self.assertEqual(r.status_code, 200)

    def test_leccion_crear_get_200(self):
        r = self.client.get(reverse("profesor:leccion_crear"))
        self.assertEqual(r.status_code, 200)

    def test_leccion_editar_get_200(self):
        r = self.client.get(reverse("profesor:leccion_editar", args=[self.lec.id]))
        self.assertEqual(r.status_code, 200)

    def test_evaluaciones_lista_200(self):
        r = self.client.get(reverse("profesor:evaluaciones"))
        self.assertEqual(r.status_code, 200)

    def test_evaluacion_crear_get_200(self):
        r = self.client.get(reverse("profesor:evaluacion_crear"))
        self.assertEqual(r.status_code, 200)

    def test_evaluacion_editar_get_200(self):
        r = self.client.get(reverse("profesor:evaluacion_editar", args=[self.eval.id]))
        self.assertEqual(r.status_code, 200)

    def test_evaluacion_detalle_200(self):
        r = self.client.get(reverse("profesor:evaluacion_detalle", args=[self.eval.id]))
        self.assertEqual(r.status_code, 200)

# ============================================================
# POST tests — basados en la inspección de *_form() (2026-10-23)
# Los 4 forms usan request.POST.get() manual, no ModelForm.
# ============================================================


class TestCRUDCursoPOST(BaseProfesorTest):
    def setUp(self):
        self.client.force_login(self.prof)

    def test_crear_post_crea_curso(self):
        Curso = apps.get_model("core", "Curso")
        r = self.client.post(reverse("profesor:curso_crear"), {
            "titulo": "Curso Nuevo POST",
            "descripcion": "desc",
            "objetivo": "obj",
            "nivel": "basico",
            "estado": "borrador",
            "duracion_estimada": 90,
            "puntos_totales": 150,
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Curso.objects.filter(titulo="Curso Nuevo POST").exists())

    def test_crear_post_sin_titulo_no_crea(self):
        Curso = apps.get_model("core", "Curso")
        n_before = Curso.objects.count()
        r = self.client.post(reverse("profesor:curso_crear"), {
            "titulo": "",
            "descripcion": "d", "objetivo": "o",
            "nivel": "basico", "estado": "borrador",
        })
        self.assertEqual(r.status_code, 200)  # renderiza form con error
        self.assertEqual(Curso.objects.count(), n_before)

    def test_editar_post_actualiza(self):
        r = self.client.post(
            reverse("profesor:curso_editar", args=[self.curso.id]),
            {
                "titulo": "Curso Editado POST",
                "descripcion": "nueva",
                "objetivo": "nuevo",
                "nivel": "basico",
                "estado": "borrador",
                "duracion_estimada": 45,
                "puntos_totales": 80,
            },
        )
        self.assertEqual(r.status_code, 302)
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.titulo, "Curso Editado POST")
        self.assertEqual(self.curso.duracion_estimada, 45)


class TestCRUDModuloPOST(BaseProfesorTest):
    def setUp(self):
        self.client.force_login(self.prof)

    def test_crear_post(self):
        Modulo = apps.get_model("core", "Modulo")
        r = self.client.post(reverse("profesor:modulo_crear"), {
            "curso": self.curso.id,
            "titulo": "M2 Nuevo POST",
            "descripcion": "desc",
            "orden": 2,
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Modulo.objects.filter(titulo="M2 Nuevo POST").exists())

    def test_editar_post(self):
        r = self.client.post(
            reverse("profesor:modulo_editar", args=[self.mod.id]),
            {
                "curso": self.curso.id,
                "titulo": "M1 Editado",
                "descripcion": "nueva",
                "orden": 5,
            },
        )
        self.assertEqual(r.status_code, 302)
        self.mod.refresh_from_db()
        self.assertEqual(self.mod.titulo, "M1 Editado")
        self.assertEqual(self.mod.orden, 5)


class TestCRUDLeccionPOST(BaseProfesorTest):
    def setUp(self):
        self.client.force_login(self.prof)

    def test_crear_post(self):
        Leccion = apps.get_model("core", "Leccion")
        r = self.client.post(reverse("profesor:leccion_crear"), {
            "modulo": self.mod.id,
            "titulo": "L2 Nueva POST",
            "contenido": "<p>contenido</p>",
            "tipo": "teoria",
            "orden": 2,
            "duracion_estimada": 20,
            "puntos": 15,
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Leccion.objects.filter(titulo="L2 Nueva POST").exists())

    def test_editar_post(self):
        r = self.client.post(
            reverse("profesor:leccion_editar", args=[self.lec.id]),
            {
                "modulo": self.mod.id,
                "titulo": "L1 Editada",
                "contenido": "<p>nuevo</p>",
                "tipo": "lectura",
                "orden": 3,
                "duracion_estimada": 25,
                "puntos": 20,
            },
        )
        self.assertEqual(r.status_code, 302)
        self.lec.refresh_from_db()
        self.assertEqual(self.lec.titulo, "L1 Editada")
        self.assertEqual(self.lec.orden, 3)


class TestCRUDEvaluacionPOST(BaseProfesorTest):
    def setUp(self):
        self.client.force_login(self.prof)

    def test_crear_post(self):
        EvaluacionCurso = apps.get_model("core", "EvaluacionCurso")
        r = self.client.post(reverse("profesor:evaluacion_crear"), {
            "curso": self.curso.id,
            "modulo": self.mod.id,
            "titulo": "Eval Nueva POST",
            "descripcion": "desc",
            "tipo": "modulo",
            "preguntas_por_evaluacion": 5,
            "tiempo_limite": 30,
            "puntaje_maximo": 100,
            "intentos_permitidos": 3,
        })
        self.assertEqual(r.status_code, 302)
        self.assertTrue(EvaluacionCurso.objects.filter(titulo="Eval Nueva POST").exists())

    def test_editar_post(self):
        r = self.client.post(
            reverse("profesor:evaluacion_editar", args=[self.eval.id]),
            {
                "curso": self.curso.id,
                "modulo": "",
                "titulo": "Eval Editada",
                "descripcion": "nueva",
                "tipo": "modulo",
                "preguntas_por_evaluacion": 8,
                "tiempo_limite": 45,
                "puntaje_maximo": 120,
                "intentos_permitidos": 2,
            },
        )
        self.assertEqual(r.status_code, 302)
        self.eval.refresh_from_db()
        self.assertEqual(self.eval.titulo, "Eval Editada")
        self.assertEqual(self.eval.tiempo_limite, 45)


class TestCursoToggle(BaseProfesorTest):
    def setUp(self):
        self.client.force_login(self.prof)

    def test_toggle_publica(self):
        self.assertEqual(self.curso.estado, "borrador")
        r = self.client.post(reverse("profesor:curso_toggle", args=[self.curso.id]))
        if r.status_code == 405:  # el toggle puede ser GET en esta implementación
            r = self.client.get(reverse("profesor:curso_toggle", args=[self.curso.id]))
        self.assertIn(r.status_code, (200, 302))
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.estado, "publicado")

