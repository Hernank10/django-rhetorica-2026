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
