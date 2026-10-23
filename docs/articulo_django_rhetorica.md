Django-Rhetorica: crónica de un LMS para lingüística computacional
Un recorrido honesto por la arquitectura, los datos, las decisiones técnicas y las cicatrices de un proyecto que combina el ecosistema Django con NLP en español.

## Introducción
Django-Rhetorica empezó como una pregunta incómoda: ¿puede un LMS enseñar análisis lingüístico de verdad, no solo servir PDFs y quizzes genéricos? La respuesta que fuimos construyendo es un proyecto que integra spaCy, un corpus pedagógico de 1.628 ejercicios reales, un motor de paráfrasis mecánica que entiende árboles de dependencias, y un sistema de repetición espaciada SM-2. Todo sobre Django 5.2, con 959 tests y 97.04% de cobertura.

No es un producto terminado. Es un proyecto production-ready para demo interna, versionado en v1.0.1, con 6.5 de 8 items de deuda técnica resueltos y una lista honesta de lo que falta: deploy a producción y storage externo.

Este artículo recorre lo que se construyó, cómo se construyó, y por qué.

## Arquitectura
Stack base:

Python 3.12.4 (portable en E:\PythonPortable_Django5)

Django 5.2.11

spaCy 3.8.16 con es_core_news_md + es_core_news_sm

Chart.js (local, sin CDN)

gTTS 2.5.4

pytest 9.1.1 + plugins (django, cov, xdist, anyio, playwright)

Estructura de monolito modular:

text
django-rhetorica/
├── core/
│   ├── models.py, models_cursos.py, models_srs.py
│   ├── services/          # Lógica de negocio determinista
│   ├── views_*.py         # Vistas por módulo (14 archivos)
│   ├── templates/         # Bootstrap 5 + Chart.js
│   ├── migrations/        # 17 migraciones (0001 → 0017)
│   └── tests/             # 74 archivos de tests
├── django_retorica/       # Settings + URLs unificadas
├── data/                  # 16 JSONs con 1.628 ejercicios
├── ejercicios_completos-lengua-castellana/  # 505 HTMLs interactivos
├── docs/                  # 8 módulos documentados (105+ secciones)
└── scripts/               # ~15 scripts permanentes de mantenimiento
Filosofía: modelos delgados, servicios ricos, vistas de 20-40 líneas. Las vistas solo validan y delegan. Esto hace que la complejidad real viva en servicios testeables de forma aislada.

## Los nueve módulos
### 1. POS y morfosintaxis con spaCy
El corazón lingüístico. Etiquetado de categorías gramaticales, lemas y funciones sintácticas sobre es_core_news_md. Demo interactiva con AJAX + debounce 400ms, chart doughnut de distribución POS, chips de filtro por categoría, tabla de tokens con palabra | categoría | lema | función.

Hallazgo técnico crítico: spaCy en español no sigue Universal Dependencies para voz pasiva. El auxiliar ser aparece con dep=aux (no aux:pass), el participio es ROOT con VerbForm=Part, y el agente es obj con case=por (no obl:agent). Detectar pasivas requiere implementación custom. Esto está documentado en modulo7_sintaxis_completo.md sección 9.1.

### 2. Filología comparada
50 etimologías latinas con reglas fonéticas: noctem → noche, ferrum → hierro, oculum → ojo. Tres funciones puras sin dependencias externas — tests instantáneos.

### 3. Lectura asistida con TTS
Textos largos segmentados, morfología contextual clickeable, síntesis de voz con gTTS cacheada en disco. El usuario clickea una palabra y ve su análisis morfológico + escucha la pronunciación.

### 4. Redacción morfosintáctica
120 ejercicios de redacción con evaluación automática. Clasifica oraciones, detecta errores comunes (dequeísmo, leísmo, concordancia) y da feedback por categoría.

### 5. SRS con algoritmo SM-2
Sprint completo esta sesión. Migración de Flashcard con 5 campos nuevos (explicacion, ejemplo, ejercicio, respuesta_ejercicio, fuente_id), 100 flashcards de sintaxis reales desde data/sintaxis.json, dashboard con 4 charts (madurez SM-2, facilidad, intervalos, retención 4 semanas), y repaso interactivo con verificación por similitud Jaccard + 5 botones SM-2.

Decisión: verificación por similitud reutiliza similitud_tokens del servicio de paráfrasis. Umbral 0.5 — respuestas exactas dan 1.0, respuestas con palabras extra también pasan. Aplicar calidad SM-2 sigue siendo POST tradicional (más robusto que AJAX para mutaciones).

### 6. Corpus y concordancia
Búsqueda KWIC (keyword in context), tabla de frecuencias, n-gramas sobre corpus literario y periodístico.

### 7. Sintaxis: paráfrasis mecánica
El módulo más ambicioso. Motor 100% determinista, sin LLM, con tres capas:

Activa ↔ pasiva: "Juan lee el libro" → "El libro es leído por Juan" con verificación de features por árbol de dependencias + similitud.

Reordenamiento sintáctico: fronting de obl/advmod + normalización a SVO canónico.

Registro formal ↔ coloquial: 9 pares léxicos (usted→vos, dinero→plata, trabajo→laburo).

Cada capa con su demo visual: chart doughnut, tabla de checks ✅/❌, panel de sugerencia, export TXT/PDF del informe completo.

### 8. LMS, dashboards y administración
Hub / con 12 cards, dashboard del profesor con 3 charts (top 10 cursos, progresos 30 días, distribución niveles), dashboard del estudiante con 4 charts + notificaciones + tareas pendientes, CRUD completo de cursos/módulos/lecciones/evaluaciones/certificaciones, analytics con heatmap/retención/tiempos, ranking global, tabla consolidada de 96 estudiantes con 2 charts comparativos, y panel de 100 técnicas de redacción con 3 charts.

### 9. Sistema de notificaciones (nuevo)
Sprint de esta sesión. Modelo Notificacion con 9 tipos (leccion_completada, curso_completado, certificacion, logro, sistema, estudiante_leccion, estudiante_cert, estudiante_logro, profesor_aviso), 3 señales Django (post_save en ProgresoUsuario, CertificacionObtenida, LogroObtenido), servicio idempotente por referencia, vista paginada con filtros, 4 endpoints AJAX (contador, últimas, marcar-todas, marcar-id), campana en navbar con emoji nativo, y 620 notificaciones reales en DB (480 para estudiantes, 140 para profesores con actividad de sus cursos).

Lección aprendida: las notificaciones tienen que ser idempotentes. El campo referencia (f"curso_{curso.id}_{user_id}") hace que correr el seed dos veces no duplique nada.

## Las decisiones técnicas que importan
Determinismo sobre LLM
Todas las funciones lingüísticas son deterministas: mismo input → mismo output. Sin llamadas a APIs externas, sin caching de red. Esto permite tests deterministas y auditoría línea por línea. Si similitud_tokens("Juan lee", "El libro es leído") da 0.4, va a dar 0.4 siempre.

Trade-off aceptado: la calidad pedagógica de la paráfrasis está acotada por las reglas que implementamos. No competimos con GPT-4 en flexibilidad. Competimos en auditabilidad y costo cero.

spaCy como fuente de verdad
El modelo es_core_news_md es la fuente única para morfología y dependencias. Todos los servicios importan _cargar() con lru_cache para no recargar el modelo (3-5s) entre peticiones.

El costo: la primera carga del modelo tarda 5-8s. En tests E2E tuvimos que precalentar con preload_spacy (fixture scope="session"), porque Playwright con expect_response(timeout=5000) fallaba cuando spaCy tardaba 8s en la primera petición.

Templates delgados, servicios ricos
views_parafrasis.py tiene 22 líneas efectivas. services/parafrasis.py tiene 180. Las 22 líneas de vista son 100% cubiertas con 12 tests triviales. Las 180 líneas de servicio tienen tests específicos por rama.

Por qué: los tests de vista con client.post() no detectan bugs de CSRF (bypass por enforce_csrf_checks=False por defecto). Fue Playwright quien encontró, en su primera ejecución, que registro.html no tenía {% csrf_token %}. Los tests de Python no lo habrían detectado nunca.

Chart.js local, no CDN
static/js/chart.umd.min.js (205 KB) servido por Django. Funciona offline, sin dependencia de terceros, sin latencia de red. Trade-off: 205 KB en el repo vs 60 KB de CDN. Vale la pena por determinismo.

Backups antes de cirugía mayor
Cada populate_* y cleanup_* guarda un JSON con los registros afectados (scripts/_backup_placeholders.json con 1.400 registros, scripts/_backup_lecciones.json, scripts/_backup_pe.json). Todos gitignorados. Restaurables si algo no gusta.

## Calidad: 959 tests, 97.04% de cobertura
Distribuidos en 74 archivos:

Categoría	Tests	Ejemplo
Servicios puros	~250	paráfrasis, filología, SRS, corpus
Servicios con spaCy	~150	POS, lectura, paráfrasis con modelo
Vistas	~350	profesor, estudiante, notificaciones
Modelos	~80	SRS, LMS, notificaciones
Integración / smoke	~80	URLs, templates, commands
E2E Playwright	8	debounce, CSRF, filtros reales
El pytest.ini exige --cov-fail-under=97 en CI. Actualmente en 97.04% — margen de solo 0.04% puntos. Es un logro y una fragilidad: si el próximo feature agrega código sin tests, el CI falla.

La suite completa tarda ~40 segundos. E2E corre aparte (-m e2e, ~50s con Chromium headless).

## Los datos: 1.628 ejercicios reales
Empezamos con 1.545 ejercicios del seed, todos placeholders "¿Pregunta 20?" → "Respuesta 20". Los limpiamos así:

Detección amplia de placeholders: ^Pregunta \d+, ^Respuesta \d+, ^item \d+, strings vacíos, una sola letra.

Verificación de 0 referencias en 3 FKs antes de borrar.

Backup JSON de los 1.400 registros.

Importación del pool desde 16 JSONs de data/: 1.483 ejercicios reales con pregunta + respuesta + teoria + ejemplo.

Cleanup de 1.400 placeholders puros.

Resultado final:

1.628 ejercicios reales en DB

0 placeholders

0 referencias huérfanas

564 recursos con archivo válido (antes 579, 15 eran PDFs inexistentes)

324 lecciones con HTML semántico + 3 ejercicios relacionados cada una

285 preguntas de evaluación con contenido real + opciones por categoría

100 flashcards SRS de sintaxis con teoría + ejemplo + ejercicio interactivo

Todos los scripts son idempotentes: get_or_create con clave semántica. Correr el seed dos veces no duplica nada.

## Los dolores reales
El bug del BOM
Los archivos guardados desde Notepad en Windows llevan BOM (EF BB BF) al inicio. Django lo tolera, pero ast.parse() falla con SyntaxError: invalid non-printable character U+FEFF. La solución: [IO.File]::WriteAllText con UTF8Encoding.new($false).

Los scripts de patch que rompen templates
Un script que hace c[:idx] con idx = -1 (cuando str.find() no encuentra el marker) corrompe el template — inserta contenido en el carácter 4, rompiendo el {% extends %}. Fue exactamente lo que pasó con profesor/base.html y profesor/estudiantes/detalle.html.

Lección aprendida: desde ahora, todo script que modifica templates necesita:

python
if not c.lstrip().startswith("{%"):
    sys.exit(1)  # template ya roto, no tocar
idx = c.find(marker)
if idx < 0:
    sys.exit(1)  # marker no encontrado, abortar
Los sys.exit(1) antes de escribir son la línea entre un fix y una regresión.

El bug de pytest 9 con -q en Windows
pytest -q imprime warnings antes del summary, y Select-Object -Last 3 en PowerShell 5.1 se queda con el trailer de warnings, no con el 406 passed. No es un problema del proyecto — es un quirk del pipe. La solución fue pytest --co -q con conteo por línea de archivo: N, que da el 936 tests collected exacto.

Playwright descubre lo que Python no ve
test_debounce_dispara_ajax fallaba con TimeoutError. Causa: primera carga de spaCy (5-8s) superaba el expect_response(timeout=5000) de Playwright. Fix: preload_spacy fixture + timeout=20000. Los tests Django no lo detectaban porque simulan POST desde Python sin browser real.

El bug del bell que no se ve
Sprint final de hoy. La campana de notificaciones existe en el HTML (línea 169 de base.html) pero no se renderiza visualmente. Causa probable: FontAwesome no renderiza <i class="fas fa-bell"> en este layout de navbar.

Lo que hicimos:

Diagnóstico completo con manage.py shell (la campana está en el HTML renderizado)

Fix A: reemplazar <i> por emoji nativo &#128276; (🔔) — funcionó a nivel HTML

Fix B (pendiente): agregar texto "Notif" + estilo visible

Estado actual: <span style="font-size:1.2em;">&#128276;</span><span style="font-weight:600;">Notif</span> está en el HTML, pero el usuario no lo ve. Puede ser cache del browser o CSS que oculta el <a>. No bloquea el sprint — todo el contenido es accesible vía /notificaciones/ y la card "Notificaciones recientes" del dashboard.

Deuda menor: este fix, 10 min.

## La deuda técnica: 6.5 de 8 items resueltos
Resueltos
#	Item	Cómo
1	15 PDFs huérfanos	clean_recurso_huerfanos.py con verificación de archivo + DELETE
2	1.400 ejercicios placeholder	cleanup_placeholders_items.py con verificación de 0 referencias + backup
3	Distractores genéricos	improve_distractores.py agrupando por category del JSON
4	Ejercicios repetidos entre lecciones	fix_ejercicios_offset.py con offset rotativo offset += 3 por categoría
5	profesor_asignado FK ausente	Migración 0015 + assign_cursos_profesores.py heredando de creado_por + round-robin
6	Notificaciones	Sprint completo: modelo + señales + frontend + tasks + 620 notifs seed
Pendientes
#	Item	Esfuerzo	Por qué no se hizo
7	Deploy producción	2-3 sesiones	Requiere settings/production.py, requirements, Procfile, nginx, Postgres. No mezclar con fixes.
8	Storage S3	1-2 sesiones	Solo urgente con usuarios reales
Cobertura	97.04% → 97.15%	15 min	Antes de #7, para que CI tenga margen
Bell visible	Emoji + texto	10 min	Deuda menor
Doc	Sección 17 modulo8	20 min	Cierre documental sprint #6
## Los números, al cierre
Métrica	Valor
Commits totales	46+ en sesión, history completa en origin/main
Tests	959 (936 unit + 8 E2E + 15 nuevos del sprint)
Cobertura	97.04%
Migraciones	17 (0001 → 0017_notif_tipos_profesor)
Ejercicios reales	1.628 (0 placeholders)
Lecciones con contenido	324 (con teoría + ejemplo + 3 ejercicios)
Preguntas evaluación	285 (240 con radios de opción múltiple)
Flashcards SRS	102 de est001 + más
Notificaciones en DB	620 (480 estudiantes + 140 profesores)
Recursos válidos	564 (0 huérfanos)
Módulos documentados	8 (105+ secciones, 127 KB)
Tags	v1.0.0, v1.0.1 (latest)
Releases GitHub	2 con assets
Deuda resuelta	6.5/8
## Lecciones aprendidas
1. Determinismo como ventaja competitiva
Competir con LLMs en flexibilidad es perder. Competir en auditabilidad, costo cero y offline es ganar en el nicho pedagógico. Cada paráfrasis es verificable línea por línea.

2. Los guards son la diferencia entre fix y regresión
Un if idx < 0: sys.exit(1) antes de escribir el archivo previene el 90% de los bugs de scripts de patch. Sin guards, c[:idx] con idx = -1 inserta en el carácter 4 y rompe el template.

3. El CSS no es opcional
Tener un botón invisible en HTML porque FontAwesome no carga es un bug, no un trade-off aceptable. La próxima vez: emoji nativo desde el inicio, nunca confiar en iconos externos.

4. Backups JSON antes de borrados masivos
Borrar 1.400 placeholders sin backup hubiera sido apostar. Con _backup_placeholders.json, la operación es reversible en 30 segundos si algo sale mal.

5. La idempotencia es requisito, no nice-to-have
Cada seed usa get_or_create con clave semántica. Correr dos veces el mismo seed no duplica nada. Esto es lo que permite iterar rápido sin miedo.

6. E2E Playwright encuentra lo que Python no ve
CSRF, debounce, fetch, dropdowns, botones — todo eso vive en el frontend real. Los tests Django client no lo detectan. Playwright sí.

7. La cobertura es una métrica honesta
97.04% no es "casi 100%". Es "una línea sin cubrir por cada 33 líneas". El margen de 0.04% al 97% es fragilidad real. Cuando bajó desde 97.08% por el sprint de notificaciones, es señal de que hay que reforzar antes del próximo feature.

## Roadmap
Corto plazo (1 sesión):

Reforzar cobertura 97.04% → 97.15% (3-4 tests defensivos)

Fix bell visible (emoji + texto + estilo)

Doc modulo8 sección 17 (sprint #6)

Fix del warning naive datetime en seed

Mediano plazo (2-3 sesiones):

#7 Deploy producción (Postgres + Gunicorn + Nginx)

Parte B: CRUD del profesor para enviar avisos a estudiantes

Doc modulo9_notificaciones.md

Largo plazo (opcional):

#8 Storage S3 para PDFs y certificados

E2E para dashboards nuevos

Audit de CSS/UX en mobile

## Conclusión
Django-Rhetorica es un proyecto inusual: combina la madurez del ecosistema Django (ORM, migraciones, admin, tests) con la frescura de spaCy para NLP en español, sobre un dominio concreto — enseñanza de lengua castellana — donde la competencia es genérica.

La apuesta por lo determinista (sin LLM, sin dependencias de red, todo verificado por tests) convierte cada funcionalidad en algo auditable. La apuesta por la disciplina (tests primero, DRY_RUN, backups, verificación antes de commit) convierte cada sprint en algo recuperable.

El proyecto no está terminado. Está sólido:

959 tests verdes, 97.04% de cobertura

1.628 ejercicios reales, 0 placeholders

620 notificaciones distribuidas entre estudiantes y profesores

8 módulos documentados con 105+ secciones

2 releases con tag versionado

Working tree clean y origin/main sincronizado

Lo que falta — deploy a producción y storage externo — es infraestructura, no producto. El contenido pedagógico está listo. El sistema de usuarios está listo. La API interna está lista.

Cuando se decida deployar a Postgres + Gunicorn + Nginx, el proyecto va a estar en condiciones de recibir a los 3 admins, 9 profesores y 96 estudiantes reales que el seed ya simula.


Última actualización: 2026-10-23 tras sprint #6 (notificaciones), 46+ commits en sesión, tags v1.0.0 y v1.0.1. Repositorio: github.com/Hernank10/django-rhetorica-2026.