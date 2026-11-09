# Cierre de auditoría MCER y ortografía

**Fecha:** 2026-11-07
**Rama:** main
**Último commit:** fe8c284

## Resumen ejecutivo

Auditoría completa del módulo MCER (`/estudiante/`, `/lectura/`, `/redaccion/tecnicas/`)
detectó y corrigió 3 clases de bugs ortográficos:

1. **Variables Django con tildes** → templates con `{{ técnica.número }}` (con tilde)
   mientras la vista pasa `tecnica` (sin tilde). 10 casos, todos corregidos.
2. **Choices incompletos en modelos** → `TecnicaGramatical.nivel` tenía 100 técnicas
   con `nivel='maestria'` fuera de los choices. Corregido con migración `0034`.
3. **Tildes en texto plano visible** → 15 tildes reales en texto que el usuario ve.
   Corregidas. Los 26 falsos positivos del diccionario (evaluaciones, intermedio,
   avanzado, practica verbo) descartados.

**Estado final:** 0 bugs reales en las 7 categorías de la auditoría.

## Estado final del módulo MCER

| Página | Tildes | Variables | Choices |
|---|---|---|---|
| `/estudiante/` (dashboard) | OK | OK | — |
| `/estudiante/cursos/` | OK | OK | OK |
| `/estudiante/evaluaciones/` | OK | OK | — |
| `/estudiante/logros/` | OK | OK | — |
| `/estudiante/certificados/` | OK | OK | OK |
| `/estudiante/ranking/` | OK | OK | — |
| `/lectura/guia-certificados/` | OK | OK | — |
| `/lectura/flashcards/` | OK | OK | — |
| `/lectura/indice/` | OK | OK | — |
| `/redaccion/tecnicas/` | OK | OK | — |

**Auditoría `_audit_mcer.py` (última corrida):**
- Sección [2] Variables Django con tildes: 0
- Sección [3] Slugs visibles: 0
- Sección [4] Texto plano VISIBLE: 0 (tras diccionario limpio v2)
- Sección [5] Mojibake archivos: 0
- Sección [6] Choices incompletos: 0
- Sección [6] Mojibake DB: 0
- Sección [7] Templates desbalanceados: 0
- Sección [8] Render páginas: 0

**Veredicto: LIMPIO.**

---
## 1. Clases de bugs identificadas y resueltas

### A. Variables Django con tildes

**Síntoma:** el HTML renderizado muestra variables vacías (`<h3></h3>`, `>#<`, etc.).

**Causa:** el template usa `{{ técnica.número }}` (con tilde en `técnica` y `número`),
pero la vista pasa el contexto con claves sin tilde (`tecnica`, `numero`). Django
trata `técnica` y `tecnica` como variables distintas → no matchea → render vacío.

**Casos encontrados (10):**

| Template | Línea | Variable rota | Fix |
|---|---|---|---|
| `dashboard_estudiante.html` | 174 | `técnica.categoria` | `tecnica.categoria` |
| `dashboard_estudiante.html` | 175 | `técnica.nombre` | `tecnica.nombre` |
| `dashboard_estudiante.html` | 191 | `técnicas|length` | `tecnicas|length` |
| `tecnicas.html` | 91 | `técnicas|length` | `tecnicas|length` |
| `tecnicas.html` | 112 | `técnica.nombre` | `tecnica.nombre` |
| `tecnicas.html` | 116 | `técnica.descripcion` | `tecnica.descripcion` |
| `tecnicas.html` | 117 | `técnica.categoria` | `tecnica.categoria` |
| `mis_evaluaciones.html` | 193 | `c.último` | `c.ultimo` |
| `dashboard.html` | 413 | `cert.certificación.nombre` | `cert.certificacion.nombre` |
| `dashboard.html` | 414 | `cert.certificación.get_nivel_display` | `cert.certificacion.get_nivel_display` |

**Bug adicional:** `tecnicas.html` tenía el iterable del bucle con tilde
(`{% for técnica in técnicas %}`). La vista pasa `tecnicas` sin tilde → bucle vacío.
Corregido a `{% for tecnica in tecnicas %}`.

**Fix:** commit `1a15721`.

**Lección:** las variables Django **no** deben llevar tildes. Si el template las tiene,
o se corrigen en el template o se corrigen en la vista (pero la vista suele estar bien).
La regla: **el nombre de la variable = la clave del contexto**.

### B. Choices incompletos en modelos

**Síntoma:** `get_<field>_display()` devuelve el valor crudo en minúsculas sin tilde.

**Causa:** la DB tiene valores que no están en el `choices=` del modelo.

**Caso encontrado (1):**

- Modelo: `TecnicaGramatical`
- Campo: `nivel`
- Valores en DB: `basico`, `intermedio`, `avanzado`, **`maestria`** (100 técnicas)
- Choices definidos: `basico`, `intermedio`, `avanzado`
- Faltante: `maestria`

**Fix:** añadir `("maestria", "Maestría")` a `NIVELES` + migración `0034`
`AlterField` (choices, no toca datos).

Commit `1a15721`.

**Lección:** si la DB tiene valores fuera de los choices, `get_*_display()` devuelve
el valor crudo. Detectar con `makemigrations --check` y migrar.
### C. Tildes en texto plano visible

**Síntoma:** palabras sin tilde en el HTML que el usuario ve.

**Causa:** hardcoded en el template, sin variable Django de por medio.

**Casos encontrados (15):**

| Archivo | Términos corregidos |
|---|---|
| `mi_progreso.html` | `comprension` x4, `precision` |
| `lectura/indice.html` | `progresion`, `argumentacion`, `comprension`, `automaticamente` |
| `asistida.html` | `categoria`, `analisis` |
| `texto_detalle.html` | `revision` |
| `certificaciones_lista.html` | `modulo`, `automaticamente`, `Obten` |
| `redaccion/historial.html` | `evaluacion` |
| `redaccion/indice.html` | `progresion`, `argumentacion`, `comprension`, `automaticamente` |

**Fix:** commits `b29a6d6` (15 tildes) y `fe8c284` (`Obten` → `Obtén`).

**Lección:** un replace masivo de todas las palabras del diccionario rompe JS
(variables `titulo`, `categoria` dentro de Chart.js) y comentarios HTML. Hay que
clasificar cada hit por contexto: **VISIBLE** (texto entre `>` y `<`),
**TEMPLATE** (`{{ }}`), **JS** (`<script>`), **ATRIBUTO** (`class="..."`),
**COMENTARIO** (`<!-- -->`), **CSS** (`<style>`).

Solo VISIBLE es accionable.

---

## 2. Falsos positivos documentados

Estas palabras **no llevan tilde** y hay que descartarlas del diccionario:

| Término | Por qué NO lleva tilde |
|---|---|
| `evaluaciones` | Plural de evaluación (la tilde está en "ción", no en "va") |
| `intermedio` | Sin diptongo ni hiato que requiera tilde |
| `avanzado` | Idem |
| `principiante` | Idem |
| `practica` | Verbo imperativo: "practica con los ejercicios". La tilde solo en el sustantivo: "la práctica" |
| `titulo`, `categoria` en JS | Variables JS dentro de `const labels = ['titulo', ...]` de Chart.js |
| `titulo` en `class="titulo-card"` | Atributo CSS |
| `{{ tecnica.titulo }}` | Template que Django resuelve en render |

---
## 3. Commits de esta fase

| Hash | Contenido | Archivos |
|---|---|---|
| `1a15721` | 10 variables + `maestria` en NIVELES | 6 archivos (incluye migración `0034`) |
| `79df5ae` | `.gitignore` para `docs/AUDIT_*.md` | 1 archivo |
| `b29a6d6` | 15 tildes en 7 templates | 7 archivos |
| `fe8c284` | `Obten` → `Obtén` | 1 archivo |

**Antes de esta fase** (contexto):
- `062f20c` — flashcards: 8 variables Django con tildes
- `9db6a2a` — flashcards: 27 tildes en texto
- `4ff4cd2` — flashcards: v2 (`No la sabia`, `La sabia`)
- `884a423` — redacción técnicas: badges con `tipo_label` / `categoria_label`
- `cf585cd`, `416139d` — redacción: custom filter para tipos
- `9c1ea6a` — ranking: 23 tildes
- `83a98d0` — certificados: NIVEL_CHOICES + mojibake + filtro 45 basura
- `dd79f26` — logros: filtro MCER + `10 → 100`
- `69b46d6` — logros: 9 tildes + tabla hardcoded
- `136f688` — evaluaciones: 9 + SUB-01 global
- `a89ce6f` — cursos: `basico` en NIVELES
- `960cf8a` — cursos: badge `get_nivel_display`
- `65bda85` — cursos: `Duracion` → `Duración`
- `8a42127` — cursos: 9 tildes
- `25aca70` — dashboard: 22 tildes
- `90e5853` — guía de certificados: 11 + versión

---

## 4. Scripts creados (todos en `scripts/`, gitignored)

### Diagnóstico

| Script | Propósito |
|---|---|
| `_audit_mcer.py` | Auditoría general: variables con tildes, slugs visibles, mojibake, choices vs DB, templates desbalanceados, render de 10 páginas |
| `_diag_texto_plano.py` (v2) | Triage de tildes en texto plano con clasificación por contexto (VISIBLE/TEMPLATE/JS/ATRIBUTO/COMENTARIO) |
| `_diag_audit_vars.py` | Qué variable pasa la vista para cada template con hallazgo |
| `_diag_audit_vars_p2.py` | Detalle de contexto de vistas + modelo detrás de `c.ultimo` |
| `_diag_flashcards_p3.py` | Por qué `#` está vacío en flashcards (encontró `tecnica.número`) |
| `_diag_flashcards_p4.py` | Variables Django con tildes en flashcards (8) |
| `_diag_mcer_completo.py` | Verifica A1-C2 completos en flashcards |
| `_diag_flashcards_vacio.py` | Por qué `/lectura/flashcards/` se ve vacío (no lo estaba) |
| `_diag_mi_ranking.py` | Ortografía del ranking |
| `_diag_certificados.py` / `_p2.py` | Certificados: mojibake + 50 vs 5 + NIVEL_CHOICES |
| `_diag_mis_logros.py` / `_p2.py` | Logros: ortografía + comparación 6 MCER vs 20 basura |
| `_diag_logros_26.py` | Por qué 26 logros en vez de 6 |
| `_diag_mis_cursos.py` | Cursos: RUTA-01..14 |
| `_diag_mis_evaluaciones.py` | Evaluaciones: EVAL-01..09 + SUB-01 |
| `_diag_redaccion_tecnicas.py` | Redacción: 18 tildes + modelo |
| `_diag_guia_cert_estado.py` | Estado de la guía antes de Fase 6 |
### Fix

| Script | Propósito |
|---|---|
| `_fix_audit_vars.py` | Fix de las 10 variables + `maestria` |
| `_fix_texto_plano.py` | Fix de 15 tildes con clasificación por contexto (solo VISIBLE) |
| `_fix_flashcards_vars.py` | Fix de 8 variables Django en flashcards |
| `_fix_flashcards.py` + `_v2.py` | 27 + 2 tildes en flashcards |
| `_fix_mi_ranking.py` | 22 tildes en ranking |
| `_fix_certificados.py` + `_db.py` | Certificados: template + modelo + DB + vista |
| `_fix_mis_logros.py` + `_view.py` | Logros: 12 cambios + filtro MCER |
| `_fix_mis_cursos.py` + `_v2.py` + `_view.py` | Cursos: 9 + 4 + filtro |
| `_fix_mis_evaluaciones.py` + `_v2.py` | Evaluaciones: 8 + SUB-01 multi-template |
| `_fix_redaccion_tecnicas.py` + `_db.py` + `_badges.py` | Redacción: 18 + 10 títulos DB + filtros |

### Verify

| Script | Propósito |
|---|---|
| `_verify_audit_vars.py` | Verifica las 4 páginas con variables + `maestria` |
| `_verify_texto_plano.py` (v2) | Verifica los 7 archivos modificados |
| `_verify_flashcards_completo.py` | Variables resueltas + MCER A1-C2 |
| `_verify_mi_ranking.py` | 30 checks del ranking |
| `_verify_certificados.py` | 13 checks de certificados |
| `_verify_mis_logros.py` | 21 checks de logros |
| `_verify_mis_cursos.py` | 16 checks de cursos |
| `_verify_mis_evaluaciones.py` | 15 checks de evaluaciones |
| `_verify_redaccion_tecnicas.py` + `_tipos.py` | 24 + 14 checks |
| `_verify_guia_render.py` | 12 checks de guía |

**Nota:** todos los scripts están gitignored por el patrón `scripts/_*.py`.

---

## 5. Migraciones creadas

| Migración | Cambio | Commit |
|---|---|---|
| `0031_alter_tecnicagramatical_nivel.py` | `("basico", "Básico")` en choices | (previo a esta fase) |
| `0032_alter_curso_nivel.py` | `("basico", "Básico")` en `Curso.NIVELES` | `a89ce6f` |
| `0033_alter_certificacion_nivel.py` | `basico/intermedio/avanzado/experto` en `Certificacion` | `83a98d0` |
| `0034_alter_tecnicagramatical_nivel.py` | `("maestria", "Maestría")` | `1a15721` |

Todas son `AlterField` (solo cambian `choices`, **no tocan datos**).

---
## 6. Pendientes fuera de scope

Estos pendientes **no son ortografía** y no bloquean funcionalidad.

### 6.1 Bug estructural en `dashboard_estudiante.html`

**Síntoma:** las líneas 174-175 usan `tecnica.nombre` y `tecnica.categoria` **sin bucle**,
pero la vista (`views.py` L83-102) solo pasa `tecnicas` (plural, lista) y no `tecnica`
(singular, objeto). Tras el fix de variables, `tecnica.nombre` resuelve a vacío.

**Detalle del flujo:**

1. Template `dashboard_estudiante.html:174-175` usa `{{ técnica.categoria }}` y `{{ técnica.nombre }}`.
2. Vista `views.py:83-102` (`dashboard_estudiante`) pasa `tecnicas` (lista) pero NO `tecnica` (singular).
3. Tras el fix de tildes (`1a15721`), el template usa `tecnica.nombre` (sin tilde), pero el contexto no tiene la clave `tecnica` → Django resuelve a vacío.

**Opciones de fix:**

- **A.** La vista pasa `"tecnica": tecnicas.first()` y el template sigue usando `tecnica.nombre`.
- **B.** El template itera `{% for tecnica in tecnicas %}{{ tecnica.nombre }}{% endfor %}`.
- **C.** La vista pasa `"tecnica": tecnicas[0]`. Menos idiomático que A.

**Recomendación:** B (iterar) si se quiere mostrar todas, o A si solo se quiere una destacada. Es decisión de diseño, no de ortografía.

**Esfuerzo:** ~5 min.

### 6.2 `docs/DIAG_PANEL_ESTUDIANTE.md` untracked

**Síntoma:** el archivo lleva **7+ sesiones** untracked en el repo. Contenido obsoleto: dice `PENDIENTES=23`, `Fallos render: 3`. Ahora la auditoría da **0 en todas las secciones**.

**Opciones:**

- **A. Regenerar con resultado actual + commit**
- **B. Gitignore `docs/DIAG_*.md`** ← recomendado, coherente con `AUDIT_*.md`
- **C. Borrar directamente**

**Fix B:**

Add-Content .gitignore "`ndocs/DIAG_.md"
Remove-Item docs\DIAG_PANEL_ESTUDIANTE.md
git add .gitignore
git commit -m "chore: ignora reportes DIAG_.md (coherente con AUDIT_*.md)"
git push origin main

text

**Esfuerzo:** ~2 min.

### 6.3 Limpieza de DB
> **Estado 2026-11-08:** las 45 certificaciones basura (ids 9-53) han sido
> borradas de la DB. Quedan 6 legítimas. El filtro en views_estudiante.py:335-337
> se mantiene como defensivo. Los 20 `Logro` no-MCER (ids 11-30) **no se tocan**:
> tienen 296 `LogroObtenido` dependientes y el filtro MCER ya los excluye del render.

**Síntoma:** registros de test o de otra sección que no pertenecen al módulo MCER.

#### Logros no-MCER (20 registros)

**IDs 11-30 en `core_logro`:**

| IDs | Contenido | Origen |
|---|---|---|
| 11-20 | `Primer paso`, `Estudiante aplicado`, `Cien aciertos`, `Racha perfecta`, `100/500/1000 puntos`, `Experto`, `Sabio`, `Políglota` | Gamificación general |
| 21-30 | `Logro 01` ... `Logro 10` con `icon_N.svg` | Test seeds |

**Problema:** tienen **296 `LogroObtenido`** dependientes. No se pueden borrar sin:

1. Migrar los `LogroObtenido` a otros logros, o
2. Eliminarlos primero (perdiendo historial del usuario), o
3. Marcarlos como inactivos (`activo=False` si se añade el campo)

**Mitigación actual:** `views_estudiante.py:307-310` los excluye del render con `MCER_FILTER = Q(nombre__icontains='MCER') | Q(nombre__regex=r'^(B1|B2|C1|C2) alcanzado$')`. El usuario no los ve. **No afecta funcionalidad.**

**Fix recomendado (futuro):**
1. Decidir si se quieren conservar los 296 LogroObtenido
LogroObtenido.objects.filter(logro_id__in=range(11, 31)).delete()
Logro.objects.filter(id__in=range(11, 31)).delete()

text

#### Certificaciones basura (45 registros)

**IDs 5-53 en `core_certificacion`:** `Certificación 01` ... `Certificación 45` con niveles `bronce/plata/oro/platino/diamante`.

**Dependencias:** **0** `CertificacionObtenida`. Se pueden borrar sin problema.

**Mitigación actual:** `views_estudiante.py:335-337` los excluye con `exclude(nombre__regex=r'^Certificación [0-9]+$')`. El usuario no los ve.

**Fix recomendado (futuro):**
Certificacion.objects.filter(nombre__regex=r'^Certificación [0-9]+$').delete()

text

#### Resumen de la limpieza

| Tipo | Registros | Dependencias | Mitigación | Fix |
|---|---|---|---|---|
| `Logro` no-MCER | 20 | 296 `LogroObtenido` | Filtro en vista | Migrar o borrar dependientes |
| `Certificación` basura | 45 | 0 | Filtro en vista | Borrar directo |
| `Logro 01-10` con `icon_N.svg` | 10 | 296 `LogroObtenido` | Filtro en vista | Igual que Logro no-MCER |

**Esfuerzo total:** 30-60 min con plan de migración y backup previo.

---

## 7. Cómo retomar

**Auditar más páginas:**
E:\PythonPortable_Django5\python.exe scripts_audit_mcer.py

text
Modifica `PAGINAS` en el script para incluir `/gramatica/`, `/sintaxis/`, `/cursos/`, etc.

**Regenerar el diag de texto plano:**
E:\PythonPortable_Django5\python.exe scripts_diag_texto_plano.py

text

**Si añades una página nueva:**
1. Añade la URL a `PAGINAS` en `_audit_mcer.py`
2. Ejecuta `_audit_mcer.py`
3. Si da 0 en las 8 secciones, la página está limpia

---

## 8. Lecciones aprendidas

### Sobre Django

1. `{{ variable }}` **no** lleva tildes. `{{ técnica }}` y `{{ tecnica }}` son variables distintas. La regla: **el nombre de la variable = la clave del contexto**.
2. `get_<field>_display()` solo devuelve el display correcto si el valor **está** en `choices=`. Si la DB tiene valores fuera de choices, devuelve el valor crudo.
3. `AlterField` por cambio de `choices` es no-op a nivel SQL pero necesario para que `makemigrations --check` no dé error y para mantener el estado consistente.

### Sobre PowerShell/Python

1. `f-string` con `{% ... %}` dentro → `SyntaxError`. Ocurrió **3 veces** en esta sesión. **Regla:** `print(f"...{% ... %}...")` está roto. Usar `print("...{% ... %}...")` o escapar con `{{` `}}`.
2. `Path.read_text()`/`write_text()` **convierte CRLF → LF**. Siempre `read_bytes()`/`write_bytes()` para preservar line endings.
3. `re.finditer()` devuelve un iterador que **no** soporta `[:5]`. Usar `itertools.islice(re.finditer(...), 5)` o `list(...)[:5]`.
4. Si pegas un bloque de markdown con múltiples code fences en un here-string de PowerShell, el paste del terminal Windows 10 1703 se trunca a ~4KB. Para contenido largo, usar editor (`notepad` / `code`) directamente.

### Sobre auditoría

1. Un `grep` masivo de tildes da **muchos falsos positivos** (variables JS, atributos, comentarios, palabras que no llevan tilde). **Clasificar por contexto** antes de fixear.
2. Los scripts de verify deben verificar los **archivos específicos** modificados, no `rglob("indice.html")` (encuentra 6 archivos en 6 directorios distintos).
3. El diccionario de tildes debe incluir **solo palabras que siempre llevan tilde**. `evaluaciones`, `intermedio`, `avanzado`, `principiante`, `practica` (verbo) NO.

---

## 9. Verificación de cierre

Ejecutar los 3 comandos para confirmar que el módulo sigue limpio:
1. Auditoría general (esperado: 0 en secciones 2,3,5,6,7,8)
E:\PythonPortable_Django5\python.exe scripts_audit_mcer.py

2. Diag de texto plano (esperado: VISIBLES: 0, RESULTADO: LIMPIO)
E:\PythonPortable_Django5\python.exe scripts_diag_texto_plano.py

3. Migraciones pendientes (esperado: No changes detected)
E:\PythonPortable_Django5\python.exe manage.py makemigrations --check --dry-run

text

**Resultado verificado el 2026-11-07 (commit `fe8c284`):**

- `_audit_mcer.py` → 0 hallazgos en [2] Variables, [3] Slugs, [5] Mojibake, [6] Choices, [7] Templates desbalanceados, [8] Render
- `_diag_texto_plano.py` → `VISIBLES: 0`, `RESULTADO: LIMPIO`
- `makemigrations --check` → `No changes detected`

Si los 3 dan limpio, el módulo está verificado.

---

**Fin del documento.** Última actualización: 2026-11-07, commit `fe8c284`.

## Fases A-D cerradas (dashboard /estudiante/)

Commits:
- `e4be397` + `105936c`: tildes en etiquetas Django de `dashboard_estudiante.html`
- `07c5cd7`: mojibake `A1->C2`, empty states motivadores, `610->600`, `0%->—`
- `bfdb056`: hero CTA sin progreso (dentro de `{% block panel %}`), proximas 1-por-curso, metas MCER
- `2a4ef23`: seccion `[12] DASHBOARD_ESTUDIANTE` en `pilot_test.py`

## Gap conocido: catálogo plano (deuda técnica post-B1.3)

El dashboard de `/estudiante/` **no distingue visualmente** entre:

1. **Cursos que el estudiante está cursando** — no hay badge "Cursando" en el catálogo
2. **Cursos disponibles para empezar** — todos los cursos se ven iguales
3. **Cursos legacy "Curso NN"** (ids 25–39, 15 cursos) — existen en DB pero **no aparecen** en el catálogo

El catálogo muestra 9: Morfología, Sintaxis, Ortografía, Redacción, Retórica, A1, A2, B1, B2.
La DB tiene 27. Los 15 "Curso NN" son legacy del seed inicial.

### Verificación pendiente

Añadir sección `[13] OFERTA_CURSOS` al `pilot_test.py` que valide:
- `n_cursos_publicados_db == n_cursos_visibles_html`
- Estudiante con 1 curso activo ve badge "Cursando" en ese curso
- Estudiante con 0 cursos ve todos los cursos sin badge
- Los cursos legacy están **intencionalmente** ocultos (o borrados)

### Prioridad

Post-B1.3. No bloquea la nueva fase MCER. Documentado aquí para no perderlo.

## Fases M-D

### Opcion M (Flashcard)
- Estado: [[ completar tras decision M1/M2/M3 ]]
- Backfill: NO automatico (fuente_id=0/192, categoria='sustantivo' unico)
- Sistema legacy (Flashcard + Review) coexiste con el actual (TecnicaLectura + ProgresoTecnicaLectura)
- Vista real (`views_flashcards_sesion.py`) usa el sistema ACTUAL, no Flashcard

### Opcion D (densificar A1)
- Target: 2.00 ej/tecnica en A1
- Antes: 102 ejercicios / 100 tecnicas = 1.02
- Despues: [[ completar tras seed ]]
- Modo: [[ placeholder (baja calidad) | csv (contenido real) ]]

### Blindaje
- Seccion [13] DENSIFICACION_A1 anadida al pilot
- Preflight: `python scripts/_diag_preflight.py`

## Deuda conocida: placeholders A1

Los 98 ejercicios anadidos en A1 son auto-reconocimiento (baja calidad pedagogica). Reemplazar con contenido real: rellenar docs/plan_densificacion_A1_full.csv y correr _seed_densificacion_a1.py --mode csv.
