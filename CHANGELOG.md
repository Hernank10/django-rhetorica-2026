# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).
Versionado: [SemVer](https://semver.org/lang/es/).

## [Unreleased]
### Pendiente
- Verificar manualmente (Ctrl+Shift+R) que los botones "Leer" de `/lectura/` funcionan. Diagnostico ya confirmo hrefs validos y rutas 200; probablemente era cache del navegador.

## [v2.7.0] - 2026-11-02
### Added
- Fase 5: 100 tecnicas lectoras (22 nuevas: 79-100) + 2 textos (11, 12).
- Texto 11 "La receta de la abuela" (A2, literario, 9 ejercicios).
- Texto 12 "El turismo masivo en las ciudades" (B2, argumentativo, 13 ejercicios).
- Cobertura completa 100/100 tecnicas.
### Changed
- Distribucion final: P1=25, P2=24, P3=24, P4=27.
- Niveles MCER: A1=14, A2=18, B1=21, B2=20, C1=16, C2=11.
- 12 textos, 106 ejercicios totales.
- Tag: `v2.7.0-lectura-100tecnicas`. Commit: `834a571`.

## [v2.6.0] - 2026-11-02
### Added
- Fase 4: 78 tecnicas lectoras (20 nuevas: 59-78) + 2 textos (9, 10).
- Texto 9 "El gato que hablaba" (A2, literario, 10 ejercicios).
- Texto 10 "La moda rapida y el costo humano" (B2, argumentativo, 13 ejercicios).
- Cobertura completa 78/78 tecnicas.
### Changed
- Distribucion: P1=19, P2=19, P3=19, P4=21.
- 10 textos, 84 ejercicios totales.
- Tag: `v2.6.0-lectura-78tecnicas`. Commit: `bd2b39a`.

## [v2.5.2] - 2026-11-02
### Fixed
- **Bug critico de deploy**: `build.sh` no ejecutaba `seed_lectura_tecnicas` ni `seed_lectura_textos` en Render.
  - Causa: los seeds se crearon en Fase 2/3 pero nunca se anadieron a `build.sh`.
  - Sintoma: `/lectura/7/` y `/lectura/8/` daban 404 en produccion, aunque en local funcionaban.
  - Fix: bloque con `if [ "$RUN_SEEDS" = "True" ]` al final de `build.sh`.
  - Leccion: cualquier `seed_*` nuevo DEBE anadirse a `build.sh`.
### Changed
- `.gitignore` con `scripts/_*.py`, `scripts/_*.ps1`, `*.bak`, `pytest_*.log`.
- Tags: `v2.5.2-deploy-fix`. Commits: `2cbdf5b` + `b98de33`.

## [v2.5.1] - 2026-11-01
### Added
- Fase 3: 58 tecnicas lectoras (20 nuevas: 39-58) + 2 textos (7, 8).
- Texto 7 "La biblioteca secreta" (B1, literario, 11 ejercicios). Cubre la tecnica 19 (huerfana de Fase 2).
- Texto 8 "El ruido de las redes sociales" (C1, argumentativo, 10 ejercicios).
- Cobertura completa 58/58 tecnicas.
### Fixed
- `services/certificaciones.py::verificar_y_otorgar`: `create` → `get_or_create` (idempotencia).
- Tests de lectura v2 con fixtures (`test_views_lectura_v2.py`).
- Templates huerfanos eliminados (`selector.html`, `lector.html`).
- Skips justificados en `test_views_hub.py` y `test_certificaciones_auto.py`.
- Tag: `v2.5.1-lectura-58tecnicas`.

## [v2.5.0] - 2026-11-01
### Added
- Fase 2 ampliada: 38 tecnicas lectoras (18 nuevas) + 2 textos (5, 6) + 17 ejercicios.
- Cobertura 37/38 tecnicas (tecnica 19 huerfana).
- Tag: `v2.5.0-lectura-38tecnicas`. Commit: `b927be0`.

## [v2.4.9] - 2026-11-01
### Added
- Fase 3C: 2 textos mas (B1 debate redes sociales en institutos + C1 manipulacion politica).
- 17 ejercicios adicionales.
- Cobertura 28/28 tecnicas.

## [v2.4.8] - 2026-11-01
### Added
- 20 tecnicas nuevas (total 28): P1/P2/P3/P4 distribuidas A1-C2.

## [v2.4.7] - 2026-11-01
### Fixed
- Fix 500 en `/` por `NoReverseMatch: lectura_selector` en `index.html`.
- El template `index.html` usaba `{% url 'lectura_selector' %}` (URL eliminada en Fase 3B). Reemplazado por `{% url 'lectura:indice' %}`.

## [v2.4.6] - 2026-11-01
### Fixed
- Eliminar referencias a `lectura_selector` en templates (`index.html`, `lector.html`).
- Actualizar `reverse('lectura_selector')` → `reverse('lectura:indice')` en tests.
- Tags: `v2.4.6-lectura-fase3b-fix`, `v2.4.6-tests-fix`.

## [v2.4.5] - 2026-11-01
### Added
- Fase 3B: pipeline `/lectura/` completo.
  - 4 vistas: `indice_lectura`, `texto_detalle`, `evaluar_ejercicio_lectura`, `mi_progreso_lectura`.
  - 4 URLs: `/lectura/`, `/lectura/progreso/`, `/lectura/evaluar/`, `/lectura/<id>/`.
  - 3 templates: `indice.html`, `texto_detalle.html`, `mi_progreso.html`.
  - Enlace "Lectura" en sidebar del estudiante (`base.html`).
  - JS AJAX para evaluacion de ejercicios.

## [v2.4.4] - 2026-11-01
### Added
- Fase 3A: 3 textos + 11 ejercicios.
- Texto 1 "El faro y la tormenta" (A2, literario, 3 ejercicios).
- Texto 2 "El reciclaje de vidrio en Espana" (B1, informativo, 4 ejercicios).
- Texto 3 "La promesa incumplida de la empresa energetica" (C1, informativo, 4 ejercicios).

## [v2.4.3] - 2026-11-01
### Added
- Fase 2: `seed_lectura_tecnicas` con 8 tecnicas PIRLS de muestra.
- JSON en `scripts/_lectura_tecnicas_demo.json`.
- Management command idempotente (`update_or_create`).

## [v2.4.1] - 2026-11-01
### Fixed
- `core/admin.py` no importaba `admin_lectura`, por lo que los 6 modelos no aparecian en `/admin/`.
- Anadido `from . import admin_lectura` al final de `core/admin.py`.

## [v2.4.0] - 2026-11-01
### Added
- Fase 1: 6 modelos de lectura + migracion `0026_add_lectura`.
  - `TecnicaLectura`, `Texto`, `EjercicioLectura`, `RespuestaLectura`, `ProgresoTecnicaLectura`, `ProgresoTexto`.
  - Admin registrado para los 6 modelos.

## [v2.3.0] - 2026-10-31
### Added
- Ranking de estudiantes con 3 graficas (Top 10, cuartiles, radar).
- Guia de lectura + footers interpretativos.

## [v2.2.22] - 2026-10-31
### Fixed
- Template `mi_ranking.html`: eliminado `{% else %}` huérfano antes de `{% elif %}` (causaba `TemplateSyntaxError`).
- Footer radar: `>` en vez de `>=` (evita falso positivo "▲ estás por encima" con 0/0).

## [v2.2.21] - 2026-10-31
### Fixed
- Chart.js no cargaba en `mi_ranking.html` → gráficas vacías. Añadido CDN `cdn.jsdelivr.net/npm/chart.js`.
- Ranking vacío: filtro `groups__name="Estudiante"` no incluye `testest*`. Ampliado a `Q(groups__name="Estudiante") | Q(username__startswith="testest")`.

## [v2.2.20] - 2026-10-31
### Added
- Ranking con 3 tarjetas (posición, percentil, tasa) + 3 gráficas (Top 10, cuartiles, radar).
- Guía de lectura + footers interpretativos.
### Fixed
- Emojis corruptos en `mi_ranking.html`: `ðŸ¥‡` → 🥇, `TÃº` → Tú, `posiciÃ³n` → posición.

## [v2.2.19] - 2026-10-31
### Added
- `build.sh` ejecuta `seed_mcer_demo` si `RUN_SEED_MCER=True`.
### Fixed
- Migrations 023/025 one-shot fallaban en prod por guard. `seed_mcer_demo` idempotente corre después de seeds.

## [v2.2.18] - 2026-10-31
### Added
- Gráficas interpretativas: guía + footers (delta, percentil, mejor/peor tipo).
### Fixed
- Encoding ASCII corrompía acentos. Scripts usan `-Encoding utf8`.

## [v2.2.17] - 2026-10-31
### Added
- 4 gráficas comparativas vs cohorte (tasa, lecciones, percentil, radar por tipo).
- Endpoint `/estudiante/_diag/` para diagnóstico JSON.

## [v2.2.15] - 2026-10-31
### Added
- MCER suma a KPIs: `cursos_activos += 1`, `lecciones_completadas += mcer_dominadas`.

## [v2.2.13] - 2026-10-31
### Added
- Migration 025: 100 `Respuesta` + 15 `ProgresoUsuario` por estudiante.

## [v2.2.12] - 2026-10-31
### Added
- Migration 024: puntos bonus logros MCER (10/20/30/40/50/100).

## [v2.2.11] - 2026-10-31
### Added
- Migration 023: cert + 6 logros MCER + backfill `ProgresoGramatical`.
### Known issues
- Guard `if len(mcer_ids) != 610: return` → no-op en prod. Resuelto en v2.2.19.

## [v2.2.9] - 2026-10-31
### Added
- Panel Recorrido MCER A1-C2 en dashboard (6 barras de progreso).

## [v2.2.8] - 2026-10-31
### Fixed
- Botón "Volver al índice" mapea módulo → nivel (`/gramatica/c2/` para C2).

## [v2.2.7] - 2026-10-31
### Fixed
- Test B1 obsoleto (110 técnicas, no 100). `.coveragerc` excluye one-shots.

## [v2.2.6] - 2026-10-31
### Added
- Cierre MCER A1-C2: 810 técnicas totales.
