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

---

## Flashcards SM-2 (v2.8.2)

### Concepto

Sistema de repaso espaciado sobre las 100 tecnicas lectoras, basado en el algoritmo SM-2
(SuperMemo 2). Complementa la practica con textos (ejercicios) con un modo de "estudio de
conceptos" (flashcards).

**Diferencia con el SRS de gramatica:**
- El SRS de gramatica usa `Flashcard` (por estudiante) + `Review` (SM-2 estandar).
- Las flashcards de lectura usan `ProgresoTecnicaLectura` (por usuario + tecnica) extendido con 5 campos SM-2.
- **Razon**: las 100 tecnicas son globales (no por estudiante). Duplicar 100 tarjetas por cada estudiante no escala.

### Modelo extendido (`ProgresoTecnicaLectura`)

Campos originales (v2.4.0):
- `usuario`, `tecnica`, `estado` (no_iniciada / en_progreso / dominada), `intentos`, `actualizado_en`

Campos SM-2 anadidos (v2.8.0, migracion `0027_lectura_sm2`):
- `intervalo_dias` (PositiveIntegerField, default 0)
- `facilidad` (FloatField, default 2.5)
- `repeticiones` (PositiveIntegerField, default 0)
- `proxima_revision` (DateField, null=True)
- `ultima_revision` (DateTimeField, null=True)

### Wrapper `_aplicar_sm2_a_progreso(progreso, calidad)`

Adapta el servicio `core.services.srs` a `ProgresoTecnicaLectura`.

Parametros:
- `progreso`: instancia de `ProgresoTecnicaLectura`
- `calidad`: 1 (no sabia) o 5 (si sabia)

Reglas:
| Caso | Accion |
|---|---|
| Primer repaso (`repeticiones == 0`), calidad < 3 | `proxima_revision = hoy` (revisar hoy) |
| Primer repaso, calidad >= 3 | `intervalo_dias = 1`, `proxima_revision = hoy + 1` |
| Repasos >= 2, calidad < 3 | Reset: `repeticiones = 0`, `proxima_revision = hoy` |
| Repasos >= 2, calidad >= 3 | SM-2 estandar: `intervalo = intervalo_anterior * facilidad`, `proxima_revision = hoy + intervalo` |

Actualizacion de `estado` (v2.8.2):
- `repeticiones >= 2` y `facilidad >= 2.3` -> `dominada`
- `repeticiones >= 1` -> `en_progreso` (si no estaba dominada)

**IMPORTANTE**: si la calidad es 1 en el primer repaso, la proxima revision es HOY. Esto evita
que SM-2 estandar (que siempre devuelve 1 dia en el primer repaso) obligue al usuario a esperar
24h para volver a ver una tarjeta que no sabia.

### Vistas

| URL | Vista | Proposito |
|---|---|---|
| `/lectura/flashcards/` | `flashcards_lectura` | GET. Muestra la primera pendiente del nivel/proceso. |
| `/lectura/flashcards/verificar/` | `flashcards_verificar` | POST. Registra `sabia=0/1`, aplica SM-2, redirige. |

Parametros GET de `flashcards_lectura`:
- `nivel`: A1 (default), A2, B1, B2, C1, C2
- `proceso`: P1, P2, P3, P4, o vacio (todos)
- `modo`: estudio (default, todas las pendientes)

### Flujo de usuario

1. Usuario entra a `/lectura/flashcards/` (desde sidebar o boton en `/lectura/`).
2. Ve la primera tecnica pendiente (sin progreso, o proxima_revision <= hoy).
3. Lee el titulo + teoria + regla + ejemplos.
4. Responde "No la sabia" (calidad 1) o "Si la sabia" (calidad 5).
5. `flashcards_verificar` aplica SM-2 y redirige a `flashcards_lectura`.
6. Al dia siguiente (o hoy si fallo), vuelve a ver las pendientes.

### Integracion con el panel de progreso

Antes de v2.8.2: `flashcards_verificar` marcaba `en_progreso` la primera vez, pero no `dominada`.
Por eso el panel `/lectura/progreso/` se quedaba en `0/14` aunque estudiaras todas las flashcards.

Despues de v2.8.2: el wrapper actualiza `estado`:
- 1 acierto -> `en_progreso` (no cuenta en el panel, pero es visible en admin)
- 2 aciertos con facilidad >= 2.3 -> `dominada` (SI cuenta en el panel `X/14`)

### Templates

- `core/templates/core/lectura/flashcards_lectura.html`: tarjeta con `<details>` para el reverso, 2 botones (sabia / no sabia), atajos de teclado (Space = ver, 1 = no, 2 = si), selector de nivel/proceso.
- `core/templates/core/lectura/flashcards_completado.html`: pantalla "sesion completada" con enlaces a los textos y al progreso.

### Tests

- `pytest core/tests/` verde (Exit 0, ~327s).
- El wrapper se verifica funcionalmente en `_fase6cd_p2d.py` (Fase 6D): sabia=1 x2 -> dominada.

### Tags / commits

| Version | Commit | Hito |
|---|---|---|
| v2.8.0 | `1c8348d` | 5 campos SM-2 + migracion 0027 |
| v2.8.1 | `9ab6f52` | Wrapper + 2 vistas + 2 templates + 2 URLs |
| **v2.8.2** | **`c404ec7`** | **MVP completo (enlace + boton + selector + estado dominada)** |
