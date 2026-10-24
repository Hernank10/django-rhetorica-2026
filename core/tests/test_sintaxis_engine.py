"""Tests del motor de evaluacion de sintaxis."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from core.models_sintaxis import TecnicaSintactica, EjercicioTecnica, ProgresoTecnica
from core.services import sintaxis as engine


def crear_tecnica(numero=1, bloque="A"):
    return TecnicaSintactica.objects.create(
        numero=numero, bloque=bloque, titulo=f"T{numero}",
        teoria="t", explicacion="e", regla="r",
        ejemplo_correcto="ok", ejemplo_incorrecto="no",
    )


def crear_ejercicio(tecnica, tipo=1, orden=1, payload=None):
    if payload is None:
        payload = {"opciones": [{"id": "a", "texto": "ok", "correcta": True, "razon": "r"}]}
    return EjercicioTecnica.objects.create(tecnica=tecnica, tipo=tipo, orden=orden, payload=payload)


class TestEvaluarTipo1(TestCase):
    def setUp(self):
        self.t = crear_tecnica()
        self.ej = crear_ejercicio(self.t, tipo=1, payload={
            "opciones": [
                {"id": "a", "texto": "A", "correcta": False, "razon": "no"},
                {"id": "b", "texto": "B", "correcta": True, "razon": "si"},
            ],
            "justificacion_obligatoria": False,
            "regla": "regla X",
        })

    def test_opcion_correcta(self):
        r = engine.evaluar_ejercicio(self.ej, {"opcion_id": "b"})
        self.assertTrue(r["ok"])
        self.assertIn("Correcto", r["feedback"])
        self.assertEqual(r["regla"], "regla X")

    def test_opcion_incorrecta(self):
        r = engine.evaluar_ejercicio(self.ej, {"opcion_id": "a"})
        self.assertFalse(r["ok"])

    def test_justificacion_obligatoria(self):
        self.ej.payload["justificacion_obligatoria"] = True
        self.ej.save()
        r = engine.evaluar_ejercicio(self.ej, {"opcion_id": "b", "justificacion": "no coincide"})
        self.assertFalse(r["ok"])


class TestEvaluarTipo2(TestCase):
    def setUp(self):
        self.t = crear_tecnica()
        self.ej = crear_ejercicio(self.t, tipo=2, payload={
            "respuesta_correcta": "Los alumnos estudian mucho.",
            "regla": "sujeto plural -> verbo plural",
        })

    def test_exacto(self):
        r = engine.evaluar_ejercicio(self.ej, {"texto": "Los alumnos estudian mucho."})
        self.assertTrue(r["ok"])

    def test_con_espacios_extra(self):
        r = engine.evaluar_ejercicio(self.ej, {"texto": "  Los alumnos estudian mucho.  "})
        self.assertTrue(r["ok"])

    def test_con_acentos_extra(self):
        r = engine.evaluar_ejercicio(self.ej, {"texto": "Los alumnos estudian muchó."})
        # Normalizado coincide (acento eliminado)
        self.assertTrue(r["ok"])

    def test_variante_cercana(self):
        r = engine.evaluar_ejercicio(self.ej, {"texto": "Los alumnos estudian muchos."})
        # Fuzzy >= 0.85, acepta como variante
        self.assertTrue(r["ok"])

    def test_incorrecta(self):
        r = engine.evaluar_ejercicio(self.ej, {"texto": "Los alumno estudia."})
        self.assertFalse(r["ok"])
        self.assertIn("regla", r)


class TestEvaluarTipo3(TestCase):
    def setUp(self):
        self.t = crear_tecnica()
        self.ej = crear_ejercicio(self.t, tipo=3, payload={
            "oraciones": [
                {"texto": "A", "categoria_correcta": "CCL"},
                {"texto": "B", "categoria_correcta": "CCT"},
            ],
            "categorias": ["CCL", "CCT", "CCC"],
        })

    def test_todo_correcto(self):
        r = engine.evaluar_ejercicio(self.ej, {"clasificacion": ["CCL", "CCT"]})
        self.assertTrue(r["ok"])

    def test_uno_incorrecto(self):
        r = engine.evaluar_ejercicio(self.ej, {"clasificacion": ["CCL", "CCC"]})
        self.assertFalse(r["ok"])
        self.assertIn("1/2", r["feedback"])

    def test_lista_incompleta(self):
        r = engine.evaluar_ejercicio(self.ej, {"clasificacion": ["CCL"]})
        self.assertFalse(r["ok"])
        self.assertIn("Se esperaban 2", r["feedback"])


class TestEvaluarTipo4(TestCase):
    def setUp(self):
        self.t = crear_tecnica()
        self.ej = crear_ejercicio(self.t, tipo=4, payload={
            "oracion_a": "Juan viene.",
            "oracion_b": "Pedro viene.",
            "conector": "y",
            "respuesta_correcta": "Juan y Pedro vienen.",
            "regla": "sujeto multiple -> verbo plural",
        })

    def test_correcta(self):
        r = engine.evaluar_ejercicio(self.ej, {"texto": "Juan y Pedro vienen."})
        self.assertTrue(r["ok"])

    def test_falta_conector(self):
        r = engine.evaluar_ejercicio(self.ej, {"texto": "Juan Pedro vienen."})
        self.assertFalse(r["ok"])

    def test_falta_b(self):
        r = engine.evaluar_ejercicio(self.ej, {"texto": "Juan y vienen."})
        self.assertFalse(r["ok"])


class TestEvaluarTipo5(TestCase):
    def setUp(self):
        self.t = crear_tecnica()
        self.ej = crear_ejercicio(self.t, tipo=5, payload={
            "oracion": "Hubieron muchos problemas.",
            "error_texto": "Hubieron",
            "error_posicion": [0, 8],
            "regla_violada": "haber_impersonal_singular",
            "reglas_posibles": ["haber_impersonal_singular", "concordancia"],
        })

    def test_correcta(self):
        r = engine.evaluar_ejercicio(self.ej, {
            "posicion": [0, 8],
            "regla": "haber_impersonal_singular",
        })
        self.assertTrue(r["ok"])

    def test_posicion_incorrecta(self):
        r = engine.evaluar_ejercicio(self.ej, {
            "posicion": [9, 15],
            "regla": "haber_impersonal_singular",
        })
        self.assertFalse(r["ok"])

    def test_regla_incorrecta(self):
        r = engine.evaluar_ejercicio(self.ej, {
            "posicion": [0, 8],
            "regla": "concordancia",
        })
        self.assertFalse(r["ok"])


class TestSM2(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("sm2_u", password="x")
        cls.t = crear_tecnica(1)
        cls.ej = crear_ejercicio(cls.t, tipo=1)

    def test_primer_acierto_intervalo_1(self):
        p = engine.actualizar_progreso(self.user, self.t, self.ej, ok=True)
        self.assertEqual(p.sm2_interval, 1)
        self.assertEqual(p.sm2_repetitions, 1)
        self.assertEqual(p.aciertos_consecutivos, 1)

    def test_segundo_acierto_intervalo_6(self):
        engine.actualizar_progreso(self.user, self.t, self.ej, ok=True)
        p = engine.actualizar_progreso(self.user, self.t, self.ej, ok=True)
        self.assertEqual(p.sm2_interval, 6)
        self.assertEqual(p.sm2_repetitions, 2)

    def test_fallo_resetea(self):
        engine.actualizar_progreso(self.user, self.t, self.ej, ok=True)
        engine.actualizar_progreso(self.user, self.t, self.ej, ok=True)
        p = engine.actualizar_progreso(self.user, self.t, self.ej, ok=False)
        self.assertEqual(p.sm2_repetitions, 0)
        self.assertEqual(p.sm2_interval, 1)
        self.assertEqual(p.aciertos_consecutivos, 0)

    def test_ef_actualizado(self):
        p = engine.actualizar_progreso(self.user, self.t, self.ej, ok=True)
        # calidad=3 para tipo 1: ef = 2.5 + (0.1 - 2*(0.08+2*0.02)) = 2.5 - 0.14 = 2.36
        self.assertAlmostEqual(p.sm2_ef, 2.36, places=2)


class TestMastery(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("mastery_u", password="x")
        cls.t = crear_tecnica(1)
        cls.ej1 = crear_ejercicio(cls.t, tipo=1, orden=1)
        cls.ej4 = crear_ejercicio(cls.t, tipo=4, orden=2, payload={
            "oracion_a": "A", "oracion_b": "B", "conector": "y",
            "respuesta_correcta": "AB", "regla": "r",
        })
        cls.ej5 = crear_ejercicio(cls.t, tipo=5, orden=3, payload={
            "oracion": "X", "error_posicion": [0, 1],
            "regla_violada": "r", "reglas_posibles": ["r"],
        })

    def test_3_aciertos_tipo1_no_domina(self):
        for _ in range(3):
            p = engine.actualizar_progreso(self.user, self.t, self.ej1, ok=True)
        self.assertEqual(p.estado, "en_progreso")
        self.assertEqual(p.aciertos_consecutivos, 3)

    def test_3_aciertos_tipo4_domina(self):
        for _ in range(3):
            p = engine.actualizar_progreso(self.user, self.t, self.ej4, ok=True)
        self.assertEqual(p.estado, "dominada")

    def test_3_aciertos_tipo5_domina(self):
        for _ in range(3):
            p = engine.actualizar_progreso(self.user, self.t, self.ej5, ok=True)
        self.assertEqual(p.estado, "dominada")


class TestProximasRevisiones(TestCase):
    def test_vacio(self):
        user = User.objects.create_user("pr_u", password="x")
        self.assertEqual(engine.proximas_revisiones(user).count(), 0)

    def test_pendiente(self):
        user = User.objects.create_user("pr_u2", password="x")
        t = crear_tecnica(1)
        p = ProgresoTecnica.objects.create(
            usuario=user, tecnica=t,
            proxima_revision=timezone.now() - timedelta(hours=1),
        )
        self.assertEqual(engine.proximas_revisiones(user).count(), 1)


class TestHelpers(TestCase):
    def test_normalizar_acentos(self):
        self.assertEqual(engine._normalizar("Los ALUMNOS están aquí."), "los alumnos estan aqui")

    def test_normalizar_vacio(self):
        self.assertEqual(engine._normalizar(""), "")
        self.assertEqual(engine._normalizar(None), "")

    def test_fuzzy_match_identicos(self):
        self.assertAlmostEqual(engine._fuzzy_match("abc def", "abc def"), 1.0, places=2)

    def test_fuzzy_match_vacios(self):
        self.assertEqual(engine._fuzzy_match("", "abc"), 0.0)


class TestResumenProgreso(TestCase):
    def test_vacio(self):
        user = User.objects.create_user("res_u", password="x")
        r = engine.resumen_progreso(user)
        self.assertEqual(r["dominadas"], 0)
        self.assertEqual(r["iniciadas"], 0)
        self.assertGreaterEqual(r["total"], 0)