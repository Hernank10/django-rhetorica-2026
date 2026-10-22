# django-rhetorica — Documentacion

**Estado**: produccion
**Commits en main**: 26
**Tests**: 248+ (todos verdes)
**Cobertura**: 97.08% | **936 tests** verdes

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

**Total**: 936 tests, cobertura 97.08%. **1.628 ejercicios** en DB (100% reales del pool, 0 placeholders). **564 recursos** (0 huérfanos).

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
- **Cobertura**: 97.36% (> 97% requerido)
- **Working tree**: clean
- **Dependencias fijadas**: spaCy 3.8.16, gTTS 2.5.4, Django 5.2.11
- **Fragilidad conocida**: `gtts 2.5.4` requiere `click<8.2` pero spaCy trae `click>=8.2.1`.
  Es un warning de `pip check`, no rompe funcionalidad. `gtts` funciona como libreria
  Python (solo el CLI falla).

---

## Changelog

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