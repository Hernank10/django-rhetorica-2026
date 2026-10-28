# Deploy Log — django-rhetorica-2026

Cronología de los deploys desde `v1.7.9` hasta `v1.8.14`.

## v1.7.9 — Artículo LMS (2026-10-27)

- **Fix**: `docs/articulo_como_construir_lms_django.md`
- **Estado**: `live`

## v1.8.0 — Primer deploy Render (sin tag)

- **Fix**: build inicial con `build.sh`
- **Estado**: `failed` (bash mal, python no encontrado)

## v1.8.1 — Orden `--force || true`

- **Fix**: `load_content_fixture || true --force` → `load_content_fixture --force || true`
- **Files**: `build.sh`
- **Estado**: `live`

## v1.8.2 — Clear + reload idempotente

- **Fix**: `_clear_content()` antes de `loaddata`
- **Estado**: `failed` (sintaxis bash rota)

## v1.8.3 — Fix sintaxis bash

- **Fix**: reescribir `build.sh` sin duplicados
- **Files**: `build.sh`, `load_content_fixture.py`
- **Estado**: `live`

## v1.8.4 — Debug + i18n

- **Fix**: `/debug/db/`, `/debug/reload/`, `LANGUAGES` es/en/pt/fr
- **Files**: `urls.py`, `base.py`
- **Estado**: `failed` (`ModuleNotFoundError: core.views_debug`)

## v1.8.5 — views_debug + --force correcto

- **Fix**: crear `core/views_debug.py` + `--force || true`
- **Files**: `views_debug.py`, `build.sh`
- **Estado**: `live` (sin flashcards)

## v1.8.6 — Flashcards en fixture

- **Fix**: `Flashcard`, `Review`, `TecnicaLinguistica` al fixture (4052 → 4448)
- **Files**: `fixtures/core_content.json`, `load_content_fixture.py`, `views_debug.py`
- **Estado**: `live`

## v1.8.7 — Remap post-loaddata (scoping bug)

- **Fix**: bloque `REMAP_FLASHCARDS` (mal scoped)
- **Estado**: `failed` (mojibake UTF-8 de `e5ed991`)

## v1.8.8 — UTF-8 + remap Python

- **Fix**: regenerar fixture `est###` → `testest###` con Python
- **Files**: `fixtures/core_content.json`
- **Estado**: `failed` (`User matching query does not exist`)

## v1.8.9 — Fix scoping + `admin*`

- **Fix**: `get_user_model` a nivel de módulo + `admin01` → `admin`
- **Estado**: `failed` (`admin` no existe en local)

## v1.8.10 — `admin` → `testadmin1`

- **Fix**: remap al usuario `testadmin1` (existe en ambos)
- **Files**: `fixtures/core_content.json`, `load_content_fixture.py`
- **Estado**: `live`

## v1.8.11 — Progreso (vacío)

- **Fix**: `ProgresoTecnica` + `ProgresoGramatical` al fixture
- **Estado**: `failed` (extraído de `db.sqlite3.bak2` = vacío)

## v1.8.12 — Progreso real

- **Fix**: 18753 registros desde `db.sqlite3.bak` + remap
- **Files**: `fixtures/core_progress.json` (7.17 MB)
- **Estado**: `live`

## v1.8.13 — Eliminar huérfanos

- **Fix**: quitar 11 registros de `prof01`/`admin01`
- **Files**: `fixtures/core_progress.json` (18753 → 18742)
- **Estado**: `live`

## v1.8.14 — Recursos desde `static/recursos/`

- **Fix**: 568 archivos HTML/JSON a `static/recursos/` (32.81 MB)
- **Files**: `static/recursos/`, `views_recursos.py`, `.gitignore`
- **Estado**: `live`

## v1.8.15 — Documentación

- **Fix**: `docs/DEPLOY_LOG.md`, `docs/LECCIONES_DEPLOY.md`, `docs/ESTADO_ACTUAL.md`
- **Estado**: (este commit)