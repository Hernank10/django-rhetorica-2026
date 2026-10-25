"""Tests del modulo 11: gramatica castellana."""
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from core.models_gramatica import (
    TecnicaGramatical, EjercicioGramatical, ProgresoGramatical,
)
from core.data.tecnicas_gramatica import TECNICAS, EJERCICIOS


class TestModelos(TestCase):
    def test_crear_tecnica(self):
        t = TecnicaGramatical.objects.create(
            numero=1, bloque="A", titulo="T1",
            teoria="t", explicacion="e", regla="r",
            ejemplo_correcto="ok", ejemplo_incorrecto="no",
        )
        self.assertEqual(str(t), "001. T1")
        self.assertEqual(t.nivel, "basico")

    def test_numero_unico(self):
        TecnicaGramatical.objects.create(
            numero=1, bloque="A", titulo="A", teoria="t", explicacion="e",
            regla="r", ejemplo_correcto="c", ejemplo_incorrecto="i",
        )
        with self.assertRaises(IntegrityError):
            TecnicaGramatical.objects.create(
                numero=1, bloque="A", titulo="B", teoria="t", explicacion="e",
                regla="r", ejemplo_correcto="c", ejemplo_incorrecto="i",
            )

    def test_progreso_defaults(self):
        u = User.objects.create_user("g_u", password="x")
        t = TecnicaGramatical.objects.create(
            numero=1, bloque="A", titulo="T1", teoria="t", explicacion="e",
            regla="r", ejemplo_correcto="c", ejemplo_incorrecto="i",
        )
        p = ProgresoGramatical.objects.create(usuario=u, tecnica=t)
        self.assertEqual(p.estado, "no_iniciada")
        self.assertEqual(p.sm2_ef, 2.5)


class TestData(TestCase):
    def test_bloque_A_tiene_15(self):
        bloque_a = [t for t in TECNICAS if t["bloque"] == "A"]
        self.assertEqual(len(bloque_a), 15)

    def test_numeros_consecutivos(self):
        nums = sorted(t["numero"] for t in TECNICAS)
        self.assertEqual(nums, list(range(1, len(TECNICAS) + 1)))

    def test_campos_requeridos(self):
        campos = ["numero", "bloque", "titulo", "teoria", "explicacion",
                  "regla", "ejemplo_correcto", "ejemplo_incorrecto", "nivel"]
        for t in TECNICAS:
            for c in campos:
                self.assertIn(c, t)
                self.assertTrue(t[c], f"Tecnica {t['numero']} campo {c} vacio")

    def test_ejercicios_por_tecnica(self):
        nums_tecnicas = {t["numero"] for t in TECNICAS}
        nums_ejercicios = set(EJERCICIOS.keys())
        faltantes = nums_tecnicas - nums_ejercicios
        self.assertEqual(faltantes, set(), f"Tecnicas sin ejercicios: {faltantes}")


class TestSeedIdempotente(TestCase):
    def test_seed_dos_veces_no_duplica(self):
        from scripts.seed_tecnicas_gramatica import main as seed
        seed()
        n1 = TecnicaGramatical.objects.count()
        e1 = EjercicioGramatical.objects.count()
        seed()
        self.assertEqual(TecnicaGramatical.objects.count(), n1)
        self.assertEqual(EjercicioGramatical.objects.count(), e1)
        self.assertEqual(n1, 15)