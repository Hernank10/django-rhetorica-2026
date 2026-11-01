# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).
Versionado: [SemVer](https://semver.org/lang/es/).

## [Unreleased]
### Pendiente (bloqueado por build minutes Render)
- Verificar en producción que `seed_mcer_demo` corre y las gráficas se llenan.

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
