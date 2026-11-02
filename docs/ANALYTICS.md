# Analytics — Arquitectura de gráficas y datos

## Modelos de datos

### `Respuesta` (`core.models`)
- `user` → auth.User
- `tipo_ejercicio` (multiple_choice, completar, ordenar...)
- `es_correcta` (bool), `fecha`, `puntuacion`

### `ProgresoUsuario` (`core.models_cursos`)
- `usuario` → auth.User
- `leccion` → Leccion (→ Modulo → Curso)
- `completado` (bool), `completado_en` (datetime)

### `ProgresoGramatical` (`core.models_gramatica`)
- `usuario` → auth.User
- `tecnica` → TecnicaGramatical (`modulo`: a1/a2/b1/b2/c1/c2)
- `estado` ("no_iniciada" | "en_progreso" | "dominada")

**IMPORTANTE:** todos los FKs apuntan a `auth.User`, no a un `CoreUser` custom.

## Endpoints

### `/estudiante/` — Dashboard
**Vista:** `views_estudiante.dashboard()`
**Contexto:** `kpis` (cursos_activos, lecciones, logros, certificados), `tasa`, `cursos_progreso`, `actividad` (30 días), `aciertos_por_tipo`, `mcer_progreso`.
**Post-procesado (v2.2.15):** MCER suma a `kpis.cursos_activos` y `kpis.lecciones`.

### `/estudiante/estadisticas/` — Estadísticas
**Vista:** `views_estudiante.mis_estadisticas()`
**Contexto (v2.2.18):** `comparativa` (user_tasa, class_tasa_avg, top10_tasa_avg, delta_tasa, mejor_tipo, peor_tipo, percentil, percentil_inv, cohorte_size), `comparativa_tipos`.
**Gráficas:** chartProm, chartAct, chartComparativaTasa, chartComparativaLecciones, chartPercentil, chartComparativaTipos.

### `/estudiante/ranking/` — Ranking
**Vista:** `views_estudiante.mi_ranking()`
**Contexto (v2.2.20):** `top10`, `mi_posicion`, `resumen_ranking` (mi_tasa, mi_percentil, mi_cuartil, prom_*, top10_*), `cuartiles` (q1-q4), `radar` (mi/clase/top10).
**Gráficas:** chartTop10, chartCuartiles, chartRadarRanking.

### `/estudiante/_diag/` — Diagnóstico JSON
Devuelve `respuesta_count`, `progreso_usuario_count`, `mcer_dominadas`, `cursos_activos`. Usado para verificar que el seed corrió.

## Cohortes
**Demo:** `username__startswith="testest"`. **Producción:** campo `cohorte_id` en User/Perfil.
**Filtros:** >=10 respuestas por usuario; >=5 por tipo. `exclude(user=u)` para no contar al usuario en su grupo.

## Encoding
- Scripts Python con acentos → `Set-Content -Encoding utf8`.
- Verificación HTML → buscar marcadores ASCII (`class="..."`, `data-*`).
- Si ves `ðŸ¥‡`, el archivo perdió bytes UTF-8.

## Chart.js
CDN: `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`
- `mis_estadisticas.html`: inline.
- `mi_ranking.html`: inline (v2.2.21+).
- `base.html`: NO lo carga global.


---

## Modulo de lectura (v2.7.0)

### Modelos (`core/models_lectura.py`)

| Modelo | Proposito |
|---|---|
| `TecnicaLectura` | Microhabilidad lectora. 100 tecnicas (1-100), por proceso PIRLS (P1-P4) y nivel MCER (A1-C2). |
| `Texto` | Texto de lectura (literario o informativo). 12 textos A2-C1. |
| `EjercicioLectura` | Ejercicio asociado a un texto y a una tecnica. 106 ejercicios. |
| `RespuestaLectura` | Respuesta de un usuario a un ejercicio. |
| `ProgresoTecnicaLectura` | Estado por usuario+tecnica: `no_iniciada`, `en_progreso`, `dominada`. |
| `ProgresoTexto` | Estado por usuario+texto: `completado`, `ejercicios_correctos/totales`. |

### Distribucion final de las 100 tecnicas
Por proceso PIRLS: P1=25, P2=24, P3=24, P4=27.
Por nivel MCER: A1=14, A2=18, B1=21, B2=20, C1=16, C2=11.

### Los 12 textos

| # | Nivel | Titulo | Ejercicios |
|---|---|---|---|
| 1 | A2 | El faro y la tormenta | 3 |
| 2 | B1 | El reciclaje de vidrio en Espana | 4 |
| 3 | C1 | La promesa incumplida de la empresa energetica | 4 |
| 4 | B1 | El debate sobre las redes sociales en los institutos | 8 |
| 5 | C1 | La manipulacion del lenguaje en el discurso politico | 9 |
| 6 | B2 | La inteligencia artificial en la educacion | 12 |
| 7 | B1 | La biblioteca secreta | 11 |
| 8 | C1 | El ruido de las redes sociales | 10 |
| 9 | A2 | El gato que hablaba | 10 |
| 10 | B2 | La moda rapida y el costo humano | 13 |
| 11 | A2 | La receta de la abuela | 9 |
| 12 | B2 | El turismo masivo en las ciudades | 13 |

### Endpoints

| URL | Vista | Proposito |
|---|---|---|
| `/lectura/` | `indice_lectura` | Lista los 12 textos + panel MCER. |
| `/lectura/<id>/` | `texto_detalle` | Muestra el texto y sus ejercicios. |
| `/lectura/evaluar/` | `evaluar_ejercicio_lectura` | POST AJAX: evalua, actualiza progreso, devuelve JSON. |
| `/lectura/progreso/` | `mi_progreso_lectura` | Panel: MCER, procesos PIRLS, tasa de acierto. |

### Flujo de evaluacion (AJAX)
1. Usuario hace clic en "Enviar respuesta" en `texto_detalle.html`.
2. JS envia `POST /lectura/evaluar/` con `{"ejercicio_id": N, "respuesta": "B"}`.
3. La vista valida el tipo, crea `RespuestaLectura`, actualiza `ProgresoTecnicaLectura` (dominada a los 2 aciertos) y `ProgresoTexto`.
4. Devuelve JSON: `es_correcta`, `feedback`, `estado_tecnica`, `progreso_texto`.

### Seeds

| Comando | Fuente | Idempotencia |
|---|---|---|
| `seed_lectura_tecnicas` | `scripts/_lectura_tecnicas_demo.json` (100 items) | `update_or_create(numero=...)` |
| `seed_lectura_textos` | `scripts/_lectura_textos_demo.json` (12 items) | `update_or_create` |

**IMPORTANTE:** ambos seeds se ejecutan en `build.sh` en cada deploy (v2.5.2+). Ver `docs/DEPLOY.md`.

### Tests
- `core/tests/test_views_lectura_v2.py`: 6 tests (indice, detalle, progreso, evaluar, sin login).
- pytest completo en verde (Exit code 0).

### Tags / commits clave

| Version | Commit | Hito |
|---|---|---|
| v2.4.0 | `5b9cbd9` | Fase 1: modelos + migracion 0026 |
| v2.4.5 | `3d5f8b6` | Fase 3B: pipeline `/lectura/` |
| v2.5.0 | `b927be0` | Fase 2: 38 tecnicas, 6 textos |
| v2.5.1 | `8e8ecf2` | Fase 3: 58 tecnicas, 8 textos |
| v2.5.2 | `2cbdf5b` | Fix `build.sh` (seeds de lectura) |
| v2.6.0 | `bd2b39a` | Fase 4: 78 tecnicas, 10 textos |
| **v2.7.0** | **`834a571`** | **Fase 5: 100 tecnicas, 12 textos, cobertura 100/100** |
