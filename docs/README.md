# django-rhetorica — Documentacion

**Estado**: produccion
**Commits en main**: 26
**Tests**: ~1040 (todos verdes)
**Cobertura**: 97.19% | **~1040 tests** verdes

Plataforma pedagogica para ensenanza de linguistica y retorica en castellano.
6 modulos en produccion. Dependencias externas: spaCy + gTTS.

---

## Modulos en produccion

| # | Modulo | Estado | Tests | Doc |
|---|---|---|---|---|
| 1 | Parser NLP con spaCy (POS + concordancia) | produccion | 47 | [modulo1_pos_completo.md](modulo1_pos_completo.md) |
| 2 | Filologia comparada (50 etimos) | produccion | 35 | [modulo2_filologia_completo.md](modulo2_filologia_completo.md) |
| 3 | Lectura asistida con TTS | produccion | 30 | [modulo3_lectura_completo.md](modulo3_lectura_completo.md) |
| 4 | Redaccion morfosintactica | produccion | 43 | [modulo4_redaccion_completo.md](modulo4_redaccion_completo.md) |
| 5 | SRS / SM-2 (repeticion espaciada) | produccion | 70 | [modulo5_srs_completo.md](modulo5_srs_completo.md) |
| 6 | Corpus y concordancia | produccion | 30 | [modulo6_corpus_completo.md](modulo6_corpus_completo.md) |
| 7 | Parafrasis mecanica (sintaxis) | produccion | 105 | [modulo7_sintaxis_completo.md](modulo7_sintaxis_completo.md) |
| 8 | LMS: hub + dashboards + populate | produccion | 936 + 8 E2E | [modulo8_lms_completo.md](modulo8_lms_completo.md) |

**Total**: ~1040 tests, cobertura 97.19%. **1.628 ejercicios** en DB (100% reales del pool, 0 placeholders). **564 recursos** (0 huérfanos).

---

## Requisitos

- Python 3.12.4 (portable en `E:\PythonPortable_Django5`)
- Django 5.2.11
- spaCy 3.8.16 + `es_core_news_sm` + `es_core_news_md`
- gTTS 2.5.4 (para lectura TTS)

---

## Instalacion

```bash
# Dependencias Python
pip install django spacy gtts

# Modelos spaCy ES
python -m spacy download es_core_news_sm
python -m spacy download es_core_news_md

# BD
python manage.py migrate

# Fixtures
python manage.py loaddata core/fixtures/redaccion_ejercicios.json
python manage.py loaddata core/fixtures/redaccion_100_tecnicas.json

# Servir
python manage.py runserver
```

---

## URLs principales

| URL | Modulo | Que hace |
|---|---|---|
| `/redaccion/` | 4 | Taller de redaccion |
| `/redaccion/<id>/` | 4 | Ejercicio especifico |
| `/redaccion/historial/` | 4 | Historial del estudiante |
| `/estudiante/srs/repaso/` | 5 | Sesion de repaso SM-2 |
| `/estudiante/srs/estadisticas/` | 5 | Metricas SRS |
| `/filologia/` | 2 | Explorador de etimos |
| `/filologia/<etimo>/` | 2 | Ficha de etimo |
| `/corpus/` | 6 | Dashboard del corpus |
| `/corpus/concordancia/` | 6 | KWIC (keyword in context) |
| `/corpus/frecuencias/` | 6 | Tabla de frecuencias + n-gramas |
| `/pos/` | 1 | Demo morfosintactico (AJAX) |
| `/pos/corpus/` | 1 | Analisis POS agregado |
| `/pos/ajax/analizar/` | 1 | Endpoint AJAX (POST JSON) |
| `/lectura/` | 3 | Selector de textos |
| `/lectura/<id>/` | 3 | Lector con click + audio |
| `/lectura/ajax/morfologia/` | 3 | Endpoint AJAX (POST JSON) |
| `/tts/?text=...&lang=es` | 3 | Audio MP3 (gTTS, cacheado) |

---

## Tests

```bash
# Suite completa
pytest -q

# Cobertura (umbral 97%)
pytest --cov=core --cov-fail-under=97 -q

# Un modulo especifico
pytest core/tests/test_services_pos.py -v
```

Tests que requieren spaCy estan marcados con `@pytest.mark.skipif(not modelo_disponible())`.
Si el modelo no esta, se skipean sin fallar. El resto de la suite sigue corriendo.

---

## Roadmap

### Completado (actualizado 2026-10-22)

- [x] Modulo 1 — POS + concordancia + funciones sintacticas (spaCy)
- [x] Modulo 2 — Filologia comparada (50 etimos con reglas foneticas)
- [x] Modulo 3 — Lectura asistida con TTS
- [x] Modulo 4 — Redaccion morfosintactica (120 ejercicios)
- [x] Modulo 5 — SRS / SM-2 (flashcards + repaso espaciado)
- [x] Modulo 6 — Corpus + concordancia (bonus no planeado)
- [x] R2b — Demo POS interactiva AJAX

### Pendiente (opcional)

- [ ] R4c redaccion — 200 tecnicas mas (bonus)
- [ ] Tests E2E con Playwright (frontend JS)
- [ ] Dashboard del profesor (agregacion multi-estudiante)
- [ ] Export PDF de redacciones evaluadas

### Fuera de scope

- [ ] Latin parsing (requiere CLTK)
- [ ] Evaluacion de calidad persuasiva (requiere LLM)
- [ ] Analisis de sentimiento
- [ ] Sincronizacion audio-palabra en tiempo real (requiere ASR)

---

## Estructura del proyecto

```
django-rhetorica/
  core/
    models.py                   Modelo principal + re-exports
    models_redaccion.py         EvaluacionRedaccion
    models_srs.py               Flashcard + Review
    services/
      redaccion.py              Clasificador morfosintactico
      _diccionarios_redaccion.py
      srs.py                    SM-2 puro (sin BD)
      srs_db.py                 SM-2 + BD (5 funciones)
      filologia.py              50 etimos (3 funciones)
      _etimos_filologia.py
      corpus.py                 Tokenizar + frecuencias + n-gramas
      pos.py                    spaCy (POS + lemma + dep)
      pos_integracion.py        Concordancia + funciones sintacticas
      lectura.py                Segmentar + morfologia contextual
      tts.py                    gTTS + cache
    views_*.py                  Vistas por modulo
    templates/core/             Templates por modulo
  django_retorica/
    settings.py
    urls.py                     URLs unificadas (namespaced por modulo)
  docs/
    README.md                   Este documento
    modulo1_pos_completo.md
    modulo2_filologia_completo.md
    modulo3_lectura_completo.md
    modulo4_redaccion_completo.md
    modulo5_srs_completo.md
    modulo6_corpus_completo.md
  scripts/                      Scripts de generacion (no produccion)
```

---

## Estado tecnico

- **Commits en main**: 26 (todos atomicos, mensajes claros)
- **Cobertura**: 97.19% (> 97% requerido)
- **Working tree**: clean
- **Dependencias fijadas**: spaCy 3.8.16, gTTS 2.5.4, Django 5.2.11
- **Fragilidad conocida**: `gtts 2.5.4` requiere `click<8.2` pero spaCy trae `click>=8.2.1`.
  Es un warning de `pip check`, no rompe funcionalidad. `gtts` funciona como libreria
  Python (solo el CLI falla).

---

## Changelog

### v1.3.1 — 2026-10-24 (dashboards por rol)
        
Extiende dashboards de profesor y admin con cards Notif + Tareas.
- `services/tareas.py`: `tareas_profesor()` + `tareas_admin()`
- `views_profesor.py`: dashboard con notif + tareas
- `profesor/dashboard.html`: 2 cards al inicio
- `views_admin.py` + `/admin-panel/`: dashboard superuser
- `base.html`: link "Panel" solo staff
- 6 tests

### v1.3.0 — 2026-10-24 (sintaxis integrado en LMS)

Módulo 10 navegable + notif al dominar.
- Link "Sintaxis 100" en navbar + badge
- Card en dashboard estudiante
- Notificación al dominar técnica (idempotente)
- 100 técnicas cargadas

### v1.2.1 — 2026-10-24 (vistas sintaxis)

5 vistas + 3 templates + JS AJAX.
- `/sintaxis/`, `/sintaxis/tecnica/<n>/`, `/sintaxis/evaluar/`,
  `/sintaxis/progreso/`, `/sintaxis/ajax/contador/`
- 12 tests de vistas
- Cobertura 97.21%

### v1.2.0 — 2026-10-24 (módulo 10 completo en datos)

100 técnicas cargadas (A-G).
- 100 técnicas + 100 ejercicios (5 tipos)
- Seed idempotente
- 14 tests de modelos

### v1.1.7 — 2026-10-24 (docs cierre v1.1.x)

- modulo8: secciones 17-21 (notif, security, requirements, split, S3)
- README: counts + changelog v1.1.0-v1.1.5
- 12 H2 en artículo, 15 H2 en proyecto

### v1.1.5 — 2026-10-24 (S3 opcional)

`STORAGES` condicional via `USE_S3`. Compatible SeaweedFS/B2/AWS.
- `settings/base.py`: switch S3/FileSystem
- `conftest.py`: tests aislados de S3

### v1.1.4 — 2026-10-24 (settings split)

`settings.py` → paquete `base/dev/prod`.
- `check --deploy` en prod: 0 warnings
- `manage.py`/`wsgi.py`/`asgi.py`/`pytest.ini` actualizados

### v1.1.3 — 2026-10-24 (requirements reproducibles)

`requirements.txt` curado + `requirements-dev.txt`.
- Fix reportlab 5→4.0.9, spacy 3.8→3.7.5 + click==8.1.7
- Modelos spacy via `spacy download`

### v1.1.2 — 2026-10-24 (SECRET_KEY rotada)

SECRET_KEY fuera del código → `.env` + `.env.example`.
- python-dotenv + BOM eliminado

### v1.1.1 — 2026-10-23 (CRUD profesor tests)

37 tests + decorador `@profesor_required` devuelve 403.
- 8 permisos + 14 GET + 10 POST + 1 toggle + 4 botones

### v1.1.0 — 2026-10-23 (notificaciones + tareas)

**Feature completo**: sistema de notificaciones con backend + frontend + seeds.

**Backend:**
- Modelo Notificacion (9 tipos, idempotencia por referencia)
- 3 señales Django (leccion/curso/cert/logro) con try/except defensivo
- Servicio idempotente (4 funciones)

**Frontend:**
- Vista /notificaciones/ paginada con filtros
- 4 endpoints AJAX (contador, últimas, marcar-todas, marcar-id)
- Campana en navbar con emoji nativo (FontAwesome no renderiza)
- 3 cards en /estudiante/: notificaciones recientes + tareas pendientes + evaluaciones programadas

**Seeds:**
- 476 notifs para 96 estudiantes
- 140 notifs para 9 profesores
- Total: 620 notificaciones en DB

**Tests:** +16 (8 modelo/señales + 9 vistas/AJAX + 7 tareas).

**Deuda resuelta:** 6.5/8 items.
**Deuda pendiente:** #7 deploy, #8 storage S3, bell visible, Parte B (CRUD profesor).

### v1.0.0 — 2026-10-22 (demo-ready)

**Hito**: production-ready para demo interna. 8/8 modulos funcionales, 1628 ejercicios 100% reales, 6/8 items de deuda tecnica resueltos.

**Features grandes:**
- 3 demos interactivas reescritas con charts (POS, parafrasis, registro)
- Registro con export TXT/PDF
- Dashboard 100 tecnicas redaccion (3 charts + tabla filtrable)
- SRS completo: 100 flashcards sintaxis + dashboard 4 charts + repaso interactivo
- Tabla consolidada 96 estudiantes + 2 charts comparativos

**Data:**
- 312 lecciones con HTML semantico + 3 ejercicios cada una
- 240 preguntas evaluacion con contenido real + opciones por categoria
- 1628 ejercicios 100% reales del pool (0 placeholders)
- 564 recursos (0 huerfanos)
- 0 lecciones con ejercicios duplicados

**Infra:**
- Biblioteca paginada (2.75 MB -> 240 KB, 68 paginas)
- Login redirect por rol (staff/profesor/estudiante)
- `profesor_asignado` FK en Curso (multi-profesor real)
- `_resolver_archivo` root-aware (visor recursos)

**Migraciones:** 0014 (Flashcard SRS), 0015 (profesor_asignado).

**Deuda tecnica pendiente (2/8):**
- #7 Deploy produccion (Postgres + Gunicorn + Nginx)
- #8 Storage externo S3 para PDFs y certificados

**Estado**: `runserver` en Windows, SQLite. No production deploy aun.

*Ultima actualizacion: 2026-10-22 tras sprint SRS completo (100 flashcards + 4 charts + repaso interactivo).*