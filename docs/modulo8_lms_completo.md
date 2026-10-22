# Modulo 8 — LMS: Hub, Dashboards y Datos

**Commits**: 3 (`638930d` .. `8080bd3`)
**Tests del modulo**: 19 unitarios + 8 E2E heredados
**Cobertura global al cierre**: 97.38%

---

## 1. Resumen ejecutivo

Capa de **presentacion y datos** sobre el LMS ya existente (`Curso`, `Modulo`,
`Leccion`, `Certificacion`). Agrega:

- **Hub `/`** con 12 cards organizadas (accesos + 7 modulos + admin staff)
- **Dashboard profesor** con 3 graficas Chart.js (top cursos, progresos 30d, distribucion niveles)
- **Dashboard estudiante** con 4 graficas (2 preexistentes + 2 nuevas) y card de certificados recientes
- **Seed reproducible** de 108 users + 15 cursos + 45 certs + actividad
- **Scripts de mantenimiento** para reparar paths y populate desde `data/*.json`

No introduce modelos nuevos. Extiende vistas y templates existentes con KPIs
y visualizaciones.

## 2. Arquitectura

```
core/templates/core/index.html               Hub con 12 cards (nuevo)
core/templates/core/profesor/dashboard.html  Dashboard prof con 3 charts (extendido)
core/templates/core/estudiante/dashboard.html Dashboard est con 4 charts (extendido)

core/views_profesor.py:dashboard             +3 charts (chart_cursos, chart_actividad, chart_niveles)
core/views_estudiante.py:dashboard           (ya tenia aciertos_data, ultimos_certs - usados ahora)

static/js/chart.umd.min.js                   Chart.js local (sin CDN)
```

Chart.js servido local desde `static/js/` — sin CDN, sin dependencias externas,
sin llamadas de red. Funciona offline.

## 3. Hub `/` — 12 cards

Reescritura completa de `index.html` con 3 secciones visuales:

**Acceso rapido** (siempre visible para autenticados):
- Mi Dashboard (`/estudiante/`)
- Cursos (`/cursos/`)
- Ejercicios (`/biblioteca/`)

**Analisis linguistico**:
- POS morfosintaxis (`/pos/` + `/pos/corpus/`)
- Filologia (`/filologia/`)
- Lectura asistida (`/lectura/`)

**Sintaxis y redaccion**:
- Parafrasis activa-pasiva (`/sintaxis/parafrasis/`)
- Reordenamiento (`/sintaxis/parafrasis/`)
- Registro formal-coloquial (`/sintaxis/parafrasis/registro/`)

**Repaso y corpus**:
- SRS / SM-2 (`/estudiante/srs/repaso/`)
- Corpus (`/corpus/`)
- Redaccion (`/redaccion/`)

**Admin** (solo `user.is_staff`):
- Django Admin (`/admin/`)
- Panel Profesor (`/profesor/`) + Analytics (`/profesor/analytics/`)

Visitantes anonimos solo ven hero + botones login/registro.

## 4. Dashboard profesor — 3 graficas

`views_profesor.py:dashboard` extendido con 3 bloques de datos:

```python
# Top 10 cursos por estudiantes inscritos
chart_cursos = Curso.objects.order_by("-estudiantes_inscritos")[:10].values(
    "titulo", "estudiantes_inscritos"
)

# Progresos completados ultimos 30 dias (agrupados por dia)
chart_actividad = ProgresoUsuario.objects.filter(
    completado=True, completado_en__gte=hace_30
).annotate(dia=TruncDate("completado_en")).values("dia").annotate(count=Count("id"))

# Distribucion de cursos por nivel
chart_niveles = Curso.objects.values("nivel").annotate(count=Count("id"))
```

Renderizados con Chart.js en `profesor/dashboard.html`:

- **Bar chart**: top 10 cursos (`chartCursos`)
- **Line chart**: progresos diarios (`chartActividad`)
- **Doughnut chart**: distribucion niveles (`chartNiveles`)

Los KPIs existentes (estudiantes, cursos, lecciones, evaluaciones, certs,
progresos, tasa aciertos) se mantienen.

## 5. Dashboard estudiante — 4 graficas + card certs

`views_estudiante.py:dashboard` **ya calculaba** `aciertos_data` y
`ultimos_certs` pero el template no los renderizaba. Se agregaron:

- **Doughnut**: ejercicios por tipo (`chartAciertos`)
- **Bar**: correctas vs total por tipo (`chartTipos`)
- **Card HTML**: 3 certificados recientes con badge de nivel + link de verificacion

Las 2 graficas preexistentes (progreso por curso + actividad 30d) se mantienen.

Total: **4 charts + 1 card** + KPIs de cursos, lecciones, logros, certs, tasa.

## 6. E2E con Playwright

8 tests end-to-end (heredados del modulo 7). Cubren:

- `test_e2e_demo.py` (3 tests): carga demo, debounce AJAX, CSRF presente
- `test_e2e_reordenar.py` (3 tests): boton visible, click sin texto, click con texto
- `test_e2e_registro.py` (2 tests): link desde demo, transformacion formal-coloquial

Configuracion: `pytest.ini` con marker `e2e` excluido por defecto
(`addopts = -m "not e2e"`). Correr con `pytest -m e2e`.

Ver `modulo7_sintaxis_completo.md` seccion 14 para detalles del setup.

## 7. Seed reproducible (`scripts/seed_test_data.py`)

Idempotente. Crea:

| Entidad | Cantidad |
|---|---|
| Admins | 3 (`admin01-03` / `Test1234!`) |
| Profesores | 9 (`prof01-09` / `Test1234!`) |
| Estudiantes | 96 (`est001-096` / `Test1234!`) |
| Grupos | 3 (Administrador, Profesor, Estudiante) |
| Cursos | 15 (4 niveles x 4/4/4/3) |
| Modulos | 45 (3 por curso) |
| Lecciones | 180 (4 por modulo) |
| Tecnicas | 10 |
| Ejercicios | 20 (placeholder) |
| Certificaciones catalogo | 45 |
| Certificaciones obtenidas | 45 (distribuidas) |
| Logros catalogo | 10 |
| Actividad | ~5000 filas (progresos, respuestas, flashcards, reviews) |

`get_or_create` en todo. Correr dos veces no duplica.

## 8. Scripts de mantenimiento

| Script | Proposito | Dry-run |
|---|---|---|
| `fix_recurso_paths.py` | Prepende `ejercicios_completos-lengua-castellana/` a 564 paths rotos | por defecto |
| `populate_from_data.py` | Importa pool de `data/*.json` a placeholders del seed | por defecto |
| `verify_seed.py` | Verifica counts y login de cada rol | solo lectura |
| `verify_after_populate.py` | Verifica que populate dejo contenido real | solo lectura |
| `make_backup.py` | `dumpdata core` con encoding UTF-8 (evita error CP1252) | -- |

Aplicar: `$env:POPULATE_APPLY='1'; python manage.py shell -c "exec(open(...).read())"; $env:POPULATE_APPLY='0'`

## 9. Reparaciones de datos

- **564 recursos** con paths rotos: `Recurso.archivo` prepended con `ejercicios_completos-lengua-castellana/`
- **2 JSONs corruptos** (`psicolinguistica.json` y `semiotica.json`): reparados por `fix_corrupt_jsons.py`
  - `psicolinguistica.json`: `},\n},\n{` → `},\n{` (-5 bytes)
  - `semiotica.json`: `"texto" (aclaracion).` → `"texto (aclaracion).",` (-1 byte)
- **Pool ejercicios reales**: 1.393 → **1.593** (+200 tras reparar JSONs)
- **20 Ejercicios + 45 Preguntas** con contenido real (antropolinguistica, gramatica, etc.)
- **15 PDFs huerfanos** (`recursos/curso-01..05.pdf`): pendientes

## 10. Tests y cobertura

| Archivo | Tests | Cobertura |
|---|---|---|
| `test_views_hub.py` | 8 | — |
| `test_views_profesor_charts.py` | 6 | 100% |
| `test_views_estudiante_charts.py` | 5 | 100% |
| `tests/e2e/test_e2e_*.py` | 8 | — (E2E) |

Tests unitarios modulo 8: **19**. Global: 377 passed. Cobertura: **97.38%**.

## 11. Decisiones tecnicas

**Chart.js local, no CDN**: `static/js/chart.umd.min.js` (205 KB) servido por
Django. Funciona offline, sin dependencia de terceros, sin latencia de red.
Trade-off: 205 KB en el repo vs 60 KB de CDN. Vale la pena por determinismo.

**Extender, no reescribir**: `profesor/dashboard.html` y `estudiante/dashboard.html`
ya existian. Se agregaron bloques `<div class="row g-3">` con `<canvas>` sin
tocar los KPIs ni las listas. Menor riesgo de regresion.

**app.get_model en tests**: `from core.models import Curso` falla porque el
modelo vive en `core/models_lms.py` (o similar). Los tests usan
`apps.get_model("core", "Curso")` para no acoplarse al archivo.

**Seed idempotente**: `get_or_create` + verificacion de count. Reset rapido:
`manage.py flush` + re-correr `seed_test_data.py` deja la DB limpia en ~30s.

**Backup con encoding UTF-8 explicito**: `dumpdata > file.json` en PowerShell
5.1 usa CP1252 y explota con emojis. `dumpdata --output=file.json` tambien
falla. Fix: `call_command("dumpdata", stdout=open(file, "w", encoding="utf-8"))`
en `make_backup.py`.

**Hub como `/`**: reescribir `index.html` en lugar de crear `/dashboard/` aparte.
Es lo primero que ve un user logueado. `/admin/` sigue en su URL estandar.

## 12. Roadmap

- **Vistas LMS propias**: `/cursos/crear/`, `/certificaciones/emitir/` fuera
  de `/admin/` (2-3 sesiones)
- **Eliminar 15 PDFs huerfanos** (`recursos/curso-01..05.pdf`): borrar `Recurso`
  o crear PDFs dummy (5 min)
- **`--create-new` en populate**: crear `EjercicioLinguistico` desde el pool
  excedente (1.593 - 1.545 = 48 nuevos posibles) (30 min)
- **Paginacion `/biblioteca/`**: actualmente 2.8 MB (45 min)
- **Analytics avanzados**: heatmap por estudiante, retencion por cohorte
  (ya existe `views_analytics.py` — extender UI)

## 13. Uso rapido

```powershell
# 1. Reset + seed (si necesitas datos limpios)
E:\PythonPortable_Django5\python.exe manage.py flush --no-input
E:\PythonPortable_Django5\python.exe manage.py shell -c "exec(open('scripts/seed_test_data.py', encoding='utf-8').read())"

# 2. Reparar paths (idempotente, solo primera vez post-seed)
$env:POPULATE_APPLY='1'
E:\PythonPortable_Django5\python.exe manage.py shell -c "exec(open('scripts/fix_recurso_paths.py', encoding='utf-8').read())"
$env:POPULATE_APPLY='0'

# 3. Populate desde data/*.json (reemplaza placeholders del seed)
$env:POPULATE_APPLY='1'
E:\PythonPortable_Django5\python.exe manage.py shell -c "exec(open('scripts/populate_from_data.py', encoding='utf-8').read())"
$env:POPULATE_APPLY='0'

# 4. Backup (UTF-8, restaurable con loaddata)
E:\PythonPortable_Django5\python.exe manage.py shell -c "exec(open('scripts/make_backup.py', encoding='utf-8').read())"

# 5. Servir
E:\PythonPortable_Django5\python.exe manage.py runserver 8000
# Abrir http://127.0.0.1:8000/ con admin01 / Test1234!
```

**Credenciales seed:**
- Admins: `admin01`, `admin02`, `admin03` / `Test1234!`
- Profesores: `prof01` ... `prof09` / `Test1234!`
- Estudiantes: `est001` ... `est096` / `Test1234!`

---

*Ultima actualizacion intermedia: 2026-10-21 tras modulo 8 (reemplazada por adenda seccion 14).*


## 14. Adenda — populate real + paginación + radios

**Agregado post-cierre.** Rellena los placeholders del seed con contenido real del pool `data/*.json`, pagina la biblioteca y renderiza `multiple_choice` con radios.

### 14.1 Lecciones con contenido real (312 reemplazos)

`scripts/populate_lecciones_v2.py` (~180 líneas):

- Detecta placeholders (`<h2>Introducción</h2><p>Contenido de X.</p>`)
- Mapea curso → categoría JSON (Sintaxis → sintaxis.json, etc.)
- Genera HTML semántico: `<h2>{name}</h2>` + `<h4>Teoría</h4><p>{teoria}</p>` + `<h4>Ejemplo</h4><blockquote>{ejemplo}</blockquote>`
- Relaciona **3 ejercicios + 2 técnicas** por lección
- Idempotente con `POPULATE_APPLY=1`

**Resultado**: 324/324 lecciones con contenido real (antes 12). Cada una con teoría + ejemplo + ejercicios navegables.

### 14.2 Evaluaciones con contenido real (240 reemplazos)

`scripts/populate_evaluaciones_v2.py` (~180 líneas):

- Detección amplia de placeholders:
  - `Pregunta N de/del/en/para/sobre ...`
  - `Pregunta N` / `¿Pregunta N?`
  - `Respuesta N` / `a,b,c,d` / vacíos
- Reemplaza `enunciado` + `respuesta_correcta` desde el pool
- Para `multiple_choice`: genera **4 opciones** (1 correcta + 3 distractores random con seed=42)
- Aplica a 240 preguntas (el resto ya tenían contenido custom)

**Resultado**: 285/285 `PreguntaEvaluacion` con contenido real.

### 14.3 Template eval con radios (240 preguntas funcionales)

Fix de 2 líneas en `core/templates/core/cursos/evaluacion_detalle.html`:

```django
{% if pregunta.tipo == 'multiple' or pregunta.tipo == 'multiple_choice' %}
```

El template ya tenía el código de `<input type="radio">` para `multiple`. Faltaba matchear el `tipo='multiple_choice'` que usan los 240 del pool. Ahora:
- **45 preguntas** `tipo=multiple` → radios (ya funcionaba)
- **240 preguntas** `tipo=multiple_choice` → **radios** (antes textarea)
- **~45 preguntas** `verdadero_falso` → 2 radios V/F
- Otras (`desarrollo`, `completar`) → textarea

### 14.4 Biblioteca paginada (2.75 MB → 80 KB)

`core/views_biblioteca.py:ejercicios_biblioteca` con `Paginator(qs, 24)`:

- Antes: los 1545 ejercicios en una sola página = **2.75 MB**
- Después: 24 por página = **~80 KB** × 65 páginas
- Contador muestra `total_ejercicios` (1545) no solo los de la página
- Paginación UI: `« 1 2 3 ... 65 »` (rango de 5 números alrededor de la actual)

Impacto: **tiempo de carga 30x menor**. Backend `Paginator` hace `LIMIT 24 OFFSET N` en cada request.

### 14.5 Tests agregados

| Archivo | Tests |
|---|---|
| `test_views_biblioteca_paginada.py` | 4 (primera página, diferencia entre páginas, overflow, HTML de paginación) |
| `test_evaluacion_render.py` | 3 (radios para multiple_choice, textarea para desarrollo, mezcla) |
| `test_views_profesor_metricas.py` | 9 (6 de tabla + 3 de charts) |

Total: **16 tests nuevos** entre populate y rendering.

### 14.6 Cobertura al cierre de la adenda

| Archivo | Cobertura |
|---|---|
| `views_biblioteca.py` | 100% |
| `templates/core/cursos/evaluacion_detalle.html` | — (template) |
| `views_profesor.py` | 100% |
| Global | **97.27%** (8726 líneas, 238 sin cubrir) |

Subió de 97.26% (con los tests de charts) a **97.27%** (con los tests de paginación).

### 14.7 Decisiones técnicas

**Populate idempotente con DRY_RUN**: `os.environ.get("POPULATE_APPLY")` gatea la escritura. Antes de aplicar muestra 5 samples `OLD: ... / NEW: ...` para revisar.

**Backups JSON locales**: `scripts/_backup_lecciones.json` y `scripts/_backup_pe.json` guardan estado pre-populate. Gitignorados (`.gitignore` agregó `scripts/_backup_*.json`). Restaurables si algo no gusta.

**Paginación con `Paginator` estándar**: sin AJAX, sin infinite scroll. Simple, robusto, cacheable. Suficiente para 65 páginas. Si crece a 1000+ páginas se puede migrar a cursor-based.

**Template radios sin tocar vista**: el `ver_evaluacion` ya itera `evaluacion.preguntas.order_by('orden')` y el POST lee `request.POST.get('pregunta_X')` genéricamente. Solo cambia el input HTML. Cero cambios en lógica.

**Distractores random**: `random.seed(42)` para reproducibilidad. Los distractores son aleatorios del mismo JSON (no del pool global). Mejora futura: filtrar por `category` del ítem original.

---

*Ultima actualizacion: 2026-10-22 tras populate_v2 + paginacion + template radios.*

## 15. Quick wins de deuda tecnica (2026-10-22)

**Agregado post-cierre.** Cuatro limpiezas de bajo esfuerzo que dejaron la DB con solo contenido real.

### 15.1 PDFs huerfanos eliminados (15 recursos)

`scripts/clean_recurso_huerfanos.py`: detecta `Recurso.archivo` que no existe en disco y borra el registro.

- Antes: 579 recursos (15 apuntaban a `recursos/curso-01..15.pdf` inexistentes)
- Despues: **564 recursos, 0 huerfanos**

### 15.2 Offset rotativo de ejercicios por leccion

`scripts/fix_ejercicios_offset.py`: reasigna `Leccion.ejercicios_relacionados` con rotacion `offset += 3` por categoria.

- Antes: todas las lecciones de un curso compartian los mismos 3 ejercicios (`(30117, 30112, 30107)` x4)
- Despues: **12 lecciones con triples distintos** (L1: 30102, L2: 30117, L3: 30112, L4: 30107...)

### 15.3 Distractores por categoria del JSON

`scripts/improve_distractores.py`: para `multiple_choice`, agrupa distractores por `item.category` del JSON original.

- Antes: 240 preguntas con distractores aleatorios (`"Ven aca ahora."`, `"llueva"`)
- Despues: **240 preguntas con distractores tematicamente coherentes** (`"Vi la pelicula y luego la comente."` vs `"Mas de uno lo sabe."`)

### 15.4 Importacion completa del pool (1483 ejercicios)

`scripts/populate_exercises_new.py`: crea `EjercicioLinguistico` faltantes desde `data/*.json`.

- Antes: 1545 ejercicios en DB (todos placeholders `item N`)
- Despues: **3028 ejercicios** (1545 + 1483 reales)

### 15.5 Cleanup de placeholders (1400 eliminados)

`scripts/cleanup_placeholders_items.py`: elimina ejercicios con `titulo` matching `^item [0-9]+$` **despues de verificar 0 referencias** (PreguntaEvaluacion, EvaluacionRedaccion, Leccion M2M, Recurso).

- Antes: 3028 ejercicios, **1400 placeholders puros** (`"Item 99"` x14 = 1545 duplicados)
- Despues: **1628 ejercicios, 0 placeholders**

Backup local en `scripts/_backup_placeholders.json` (1400 registros, gitignored).

### 15.6 Estado final de la DB

| Entidad | Count |
|---|---|
| Ejercicios reales | **1628** |
| Placeholders | **0** |
| Recursos validos | 564 |
| Lecciones con ejercicios | 324 |
| Lecciones con triples unicos | 324 |

Distribucion de los 1628 por categoria:

### 15.7 Decisiones tecnicas

**Borrado con verificacion previa**: antes de eliminar los 1400 placeholders se corrio `_diag_impacto_cleanup.py` que confirmo 0 referencias en 3 FKs (`PreguntaEvaluacion`, `EvaluacionRedaccion`, `Recurso`) y 0 filas M2M. Sin verificacion, el `delete()` habria dejado `PreguntaEvaluacion` huerfanas o cascadeado sin saber.

**Backup JSON antes de delete**: los 1400 registros se exportaron a `_backup_placeholders.json` (gitignored) antes de borrar. Restaurables si fuese necesario (aunque son basura, no hace falta).

**Idempotencia con `titulo` como clave**: en `populate_exercises_new.py` la deteccion de faltantes usa el `titulo` del JSON (`"Parentesco y terminologia"`). Es imperfecto si dos ejercicios legitimos comparten titulo, pero en la practica los 100 titulos por JSON son unicos.

**Offset rotativo con wraparound**: `used[cat] = (offset + 3) % len(pool)` garantiza que despues de `len(pool)/3` lecciones se vuelva al inicio. Con 100 ejercicios por categoria, hay 33 lecciones antes de repetir.

### 15.8 Deuda tecnica restante

Los 4 items que **no** se resolvieron (todos requieren sesion propia):

| # | Item | Esfuerzo |
|---|---|---|
| 5 | `profesor_asignado` FK en Curso | 45 min |
| 6 | Notificaciones (completar curso, cert) | 2 sesiones |
| 7 | Deploy (Postgres + Gunicorn + Nginx) | 2-3 sesiones |
| 8 | Storage externo S3 para PDFs | 1-2 sesiones |

---

*Ultima actualizacion: 2026-10-22 tras quick wins de deuda tecnica.*

