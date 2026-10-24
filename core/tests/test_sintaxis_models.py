"""Tests de los modelos de sintaxis + data del bloque A."""
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from core.models_sintaxis import TecnicaSintactica, EjercicioTecnica, ProgresoTecnica
from core.data.tecnicas_sintaxis import TECNICAS, EJERCICIOS


def crear_tecnica(numero=1, bloque="A"):
    return TecnicaSintactica.objects.create(
        numero=numero, bloque=bloque, titulo=f"T{numero}",
        teoria="t", explicacion="e", regla="r",
        ejemplo_correcto="ok", ejemplo_incorrecto="no",
    )


# ══════════════════════════════════════════════════════════════
# Modelo TecnicaSintactica
# ══════════════════════════════════════════════════════════════
class TestTecnicaSintactica(TestCase):
    def test_crear(self):
        t = crear_tecnica(1)
        self.assertEqual(t.numero, 1)
        self.assertEqual(t.nivel, "basico")
        self.assertEqual(str(t), "001. T1")

    def test_numero_unico(self):
        crear_tecnica(1)
        with self.assertRaises(IntegrityError):
            crear_tecnica(1)

    def test_ordering_por_numero(self):
        for i in [3, 1, 2]:
            crear_tecnica(i)
        nums = list(TecnicaSintactica.objects.values_list("numero", flat=True))
        self.assertEqual(nums, [1, 2, 3])


# ══════════════════════════════════════════════════════════════
# Modelo EjercicioTecnica
# ══════════════════════════════════════════════════════════════
class TestEjercicioTecnica(TestCase):
    def setUp(self):
        self.t = crear_tecnica(1)

    def test_crear(self):
        e = EjercicioTecnica.objects.create(
            tecnica=self.t, tipo=1, payload={"enunciado": "x"}, orden=1,
        )
        self.assertEqual(e.tipo, 1)
        self.assertIn("T001", str(e))

    def test_unique_tecnica_orden(self):
        EjercicioTecnica.objects.create(tecnica=self.t, tipo=1, payload={}, orden=1)
        with self.assertRaises(IntegrityError):
            EjercicioTecnica.objects.create(tecnica=self.t, tipo=2, payload={}, orden=1)


# ══════════════════════════════════════════════════════════════
# Modelo ProgresoTecnica
# ══════════════════════════════════════════════════════════════
class TestProgresoTecnica(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("sin_u", password="x")
        cls.t = crear_tecnica(1)

    def test_crear_defaults(self):
        p = ProgresoTecnica.objects.create(usuario=self.user, tecnica=self.t)
        self.assertEqual(p.estado, "no_iniciada")
        self.assertEqual(p.aciertos_consecutivos, 0)
        self.assertEqual(p.sm2_ef, 2.5)
        self.assertEqual(p.sm2_interval, 0)

    def test_unique_together(self):
        ProgresoTecnica.objects.create(usuario=self.user, tecnica=self.t)
        with self.assertRaises(IntegrityError):
            ProgresoTecnica.objects.create(usuario=self.user, tecnica=self.t)


# ══════════════════════════════════════════════════════════════
# Data bloque A (sin tocar DB)
# ══════════════════════════════════════════════════════════════
class TestDataSeed(TestCase):
    def test_bloque_A_tiene_20(self):
        bloque_a = [t for t in TECNICAS if t["bloque"] == "A"]
        self.assertEqual(len(bloque_a), 20)
        nums = sorted(t["numero"] for t in bloque_a)
        self.assertEqual(nums, list(range(1, 21)))

    def test_bloques_totales_acumulan(self):
        # Escalable: no hardcodea total, valida coherencia
        self.assertGreaterEqual(len(TECNICAS), 20)
        self.assertEqual(len(TECNICAS), len({t["numero"] for t in TECNICAS}))

    def test_campos_requeridos(self):
        campos = ["numero", "bloque", "titulo", "teoria", "explicacion",
                  "regla", "ejemplo_correcto", "ejemplo_incorrecto", "nivel"]
        for t in TECNICAS:
            for campo in campos:
                self.assertIn(campo, t, f"Técnica {t.get('numero')} sin '{campo}'")
                self.assertTrue(t[campo], f"Técnica {t['numero']} '{campo}' vacío")

    def test_numeros_unicos_consecutivos(self):
        nums = sorted(t["numero"] for t in TECNICAS)
        # Escalable: los números deben ser 1..N sin huecos ni duplicados
        self.assertEqual(nums, list(range(1, len(TECNICAS) + 1)))

    def test_ejercicios_por_tecnica(self):
        # Escalable: cada técnica debe tener al menos 1 ejercicio
        nums_tecnicas = {t["numero"] for t in TECNICAS}
        nums_ejercicios = set(EJERCICIOS.keys())
        faltantes = nums_tecnicas - nums_ejercicios
        self.assertEqual(faltantes, set(), f"Técnicas sin ejercicios: {faltantes}")
        for num, ejs in EJERCICIOS.items():
            self.assertGreaterEqual(len(ejs), 1, f"Técnica {num} sin ejercicios")

    def test_todos_los_tipos(self):
        tipos = {ej["tipo"] for ejs in EJERCICIOS.values() for ej in ejs}
        self.assertEqual(tipos, {1, 2, 3, 4, 5})


# ══════════════════════════════════════════════════════════════
# Seed idempotente
# ══════════════════════════════════════════════════════════════
class TestSeedIdempotente(TestCase):
    def test_seed_dos_veces_no_duplica(self):
        from scripts.seed_tecnicas_sintaxis import main as seed_main
        seed_main()
        n_t = TecnicaSintactica.objects.count()
        n_e = EjercicioTecnica.objects.count()
        # Escalable: compara contra la data, no contra un número fijo
        self.assertEqual(n_t, len(TECNICAS))
        self.assertEqual(n_e, sum(len(v) for v in EJERCICIOS.values()))
        # Segunda corrida: mismos totales
        seed_main()
        self.assertEqual(TecnicaSintactica.objects.count(), n_t)
        self.assertEqual(EjercicioTecnica.objects.count(), n_e)