# Estado actual — django-rhetorica-2026

Snapshot tras `v2.0.6` (2026-10-30). Verificar con `/debug/db/?token=...` (sin prefijo `/en/`).

## Modelos en producción

| Modelo | Filas |
|---|---|
| TecnicaGramatical | **610** |
| EjercicioGramatical | **610** |
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
| **A2** | **100** | **501-600** | **✅ completo** |
| B1 | 110 | 301-410 | ✅ completo (+10 bloque H) |
| **B2** | **100** | **601-700** | **✅ completo** |
| C1 | 0 | — | ❌ pendiente |
| C2 | 0 | — | ❌ pendiente |

## Distribución por módulo

| Módulo | Técnicas | Bloques |
|---|---|---|
| gramatica | 100 | A-G (base) |
| generativa | 100 | A-G |
| a1 | 100 | A-J |
| b1 | 110 | A-H (H = subjuntivo imperfecto + condicionales 2/3) |
| **a2** | **100** | **A-J** |
| **b2** | **100** | **A-J** |

## Tests (verificado 2026-10-30)

- **B2**: 5 tests, `5 passed` en ~7 s
- **A2**: 5 tests, `5 passed` en ~12 s
- Resto de la suite: verde (1279 passed en sesión v1.8.15)

## Tags pusheados (18)

`v1.8.15` · `v1.8.16` (B1-H) · `v1.9.0` a `v1.9.7` (A2 10 tags) · `v1.9.7-rollback` · `v2.0.0` a `v2.0.6` (B2 7 tags)

## Hitos de la sesión (2026-10-29 / 30)

- A2 completo: 10 tags, 100 técnicas, 100 ejercicios, UI, tests, dashboard
- B1 bloque H: subjuntivo imperfecto + condicionales 2/3 (401-410)
- B2 completo: 6 tags, 100 técnicas, 100 ejercicios, UI, tests, dashboard
- 7 fixes de build.sh (`RUN_SEEDS`, `RUN_SEED_A2`, `RUN_SEED_B2` después de `LOAD_FIXTURE`)
- Fix de navegación B2 (`anterior`/`siguiente` filtrados por módulo)
- Fix de URL A2 (`indice_a2` en vez de `gramatica_a2`)
- Cleanup de huérfanos en `load_progress_fixture.py`

## Usuarios

| Grupo | Cantidad | Password |
|---|---|---|
| `testadmin1..3` | 3 | `Test1234!` |
| `testprofe01..09` | 9 | `Test1234!` |
| `testest001..096` | 96 | `Test1234!` |
| `admin` | 1 | (creado por `create_superuser`) |

## Próximo paso: C1 (701-800)

Plan tentativo de 10 bloques:
- A (701-710): Discurso académico
- B (711-720): Registro literario
- C (721-730): Cohesión y coherencia
- D (731-740): Expresiones idiomáticas
- E (741-750): Matices aspectuales y modales
- F (751-760): Léxico especializado y culto
- G (761-770): Sintaxis compleja y variación estilística
- H (771-780): Discurso oral formal
- I (781-790): Análisis crítico del discurso
- J (791-800): Síntesis y creación

Fases: `v2.1.0` (A) · `v2.1.1` (B+C) · `v2.1.2` (D+E) · `v2.1.3` (F+G) · `v2.1.4` (H+I) · `v2.1.5` (J) = C1 100/100
