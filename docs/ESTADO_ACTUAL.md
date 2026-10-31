# Estado actual — django-rhetorica-2026

Snapshot tras `v2.2.6` / `MCER-COMPLETO` (2026-10-30).

## 🎉 MCER A1–C2 COMPLETO

**810 técnicas** en producción. **6 niveles MCER cerrados**. **32 tags** pusheados.

## Modelos en producción

| Modelo | Filas |
|---|---|
| **TecnicaGramatical** | **810** |
| **EjercicioGramatical** | **810** |
| TecnicaSintactica | 100 |
| TecnicaLinguistica | 10 |
| EjercicioTecnica | 100 |
| EjercicioLinguistico | 1628 |
| Recurso | 564 |
| ContenidoJSON | 19 |
| Curso | 27 |
| Modulo | 93 |
| Leccion | 324 |
| EvaluacionCurso | 63 |
| PreguntaEvaluacion | 285 |
| Certificacion | 49 |
| CertificacionObtenida | 45 |
| Flashcard | 192 |
| Review | 194 |
| ProgresoTecnica | 3696 |
| ProgresoGramatical | 15046 |
| User | 110 |

## Cobertura MCER

| Nivel | Técnicas | Rango | Estado |
|---|---|---|---|
| A1 | 100 | 201-300 | ✅ completo |
| A2 | 100 | 501-600 | ✅ completo |
| B1 | 110 | 301-410 | ✅ completo (+10 bloque H) |
| B2 | 100 | 601-700 | ✅ completo |
| C1 | 100 | 701-800 | ✅ completo |
| **C2** | **100** | **801-900** | **✅ completo** |

**Total MCER (A1–C2): 610 técnicas** + 200 técnicas base (gramática + generativa) = **810 técnicas**.

## Distribución por módulo

| Módulo | Técnicas | Bloques |
|---|---|---|
| gramatica | 100 | A-G (base) |
| generativa | 100 | A-G |
| a1 | 100 | A-J |
| a2 | 100 | A-J |
| b1 | 110 | A-H |
| b2 | 100 | A-J |
| c1 | 100 | A-J |
| c2 | 100 | A-J |

## Tests (verificado 2026-10-30)

- **C2**: 3 tests, `3 passed` en ~7.65 s
- **C1**: 7 tests, `7 passed`
- **B2**: 5 tests, `5 passed`
- **A2**: 5 tests, `5 passed`
- Suite completa: verde

## Tags pusheados (32)

`v1.8.15` · `v1.8.16` (B1-H) · `v1.9.0` a `v1.9.7` (A2 10 tags) · `v1.9.7-rollback` · `v2.0.0` a `v2.0.6` (B2 7 tags) · `v2.1.0` a `v2.1.7` (C1 8 tags) · `v2.2.0` a `v2.2.6` (C2 7 tags) · **`MCER-COMPLETO`**

## Hitos del proyecto

- **A1 completo**: 100 técnicas
- **A2 completo**: 10 tags, 100 técnicas
- **B1 completo**: 110 técnicas (+10 bloque H: subjuntivo imperfecto + condicionales 2/3)
- **B2 completo**: 6 tags, 100 técnicas, UI, tests, dashboard
- **C1 completo**: 6 tags, 100 técnicas, UI, tests, dashboard
- **C2 completo**: 6 tags, 100 técnicas, UI, tests, dashboard
- **MCER A1–C2 cerrado**: 810 técnicas, 6 niveles, producción estable
- 7 fixes de build.sh (`RUN_SEEDS`, `RUN_SEED_A2/B2/C1/C2` después de `LOAD_FIXTURE`)
- Fix de navegación B2/C1/C2 (`anterior`/`siguiente` filtrados por módulo)
- Fix de URL A2 (`indice_a2` en vez de `gramatica_a2`)
- Cleanup de huérfanos en `load_progress_fixture.py`
- Resiliencia `tecnica()` contra FK huérfanas
- Card B2/C1/C2 con "Ver las 100 técnicas"

## Usuarios

| Grupo | Cantidad | Password |
|---|---|---|
| `testadmin1..3` | 3 | `Test1234!` |
| `testprofe01..09` | 9 | `Test1234!` |
| `testest001..096` | 96 | `Test1234!` |
| `admin` | 1 | (creado por `create_superuser`) |

## URL de producción

https://django-rhetorica-2026-1.onrender.com

## Estado: PROYECTO CERRADO

MCER A1–C2 completo. 810 técnicas. 32 tags. Producción estable.
