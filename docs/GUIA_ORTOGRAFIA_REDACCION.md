# Guía de corrección ortográfica, redacción y desarrollo — Rhetorica

> Para tres audiencias: desarrolladores, profesores y estudiantes.
> Basada en el sprint de tildes del 2026-11-09 (174 correcciones en 99 registros).

## 1. Metodología común

Patrón que funcionó:

1. DIAGNOSTICAR — script read-only que reporta el estado real
2. DRY-RUN — muestra qué haría sin hacerlo
3. BACKUP — copiar la DB antes de tocar
4. APLICAR — script con --apply dentro de transacción atómica
5. VERIFICAR — re-correr el diagnóstico, debe dar 0
6. VERSIONAR — commit descriptivo

Regla de oro: si no puedes verificar que un fix funcionó, no lo apliques.

## 2. Guía para desarrolladores

### Diagnosticar

    E:\PythonPortable_Django5\python.exe scripts\_diag_tildes.py

Busca 23 palabras con tilde obligatoria (gramatica, ortografia, retorica, espanol, musica, numero, lexico, silaba, morfologia, semantica, pragmatica, fonetica) y mojibake en 6 modelos: TecnicaGramatical, Modulo, Curso, TecnicaLectura, Texto, Flashcard.

No busca tildes contextuales (aun/aún, solo/sólo). Esas requieren juicio semántico y no se automatizan con regex.

### Aplicar el fix

    E:\PythonPortable_Django5\python.exe scripts\_fix_tildes.py            # DRY-RUN
    E:\PythonPortable_Django5\python.exe scripts\_fix_tildes.py --apply    # Aplicar

Resultado del sprint: 174 sustituciones en 99 registros. Post-fix: 0 errores.

### Reglas de un fix

- Idempotente (ejecutar 2 veces deja el mismo estado)
- Solo actúa sobre lo que el diagnóstico reportó
- DRY-RUN por defecto, --apply opt-in
- transaction.atomic() (rollback si falla a mitad)
- Backup antes de aplicar
- Preserva capitalización (Gramatica → Gramática, no gramática)
- Versiona el script con excepción en .gitignore

### Cuándo NO automatizar

- Tildes contextuales (aun/aún, solo/sólo)
- Contenido pedagógico (los 98 placeholders de A1)
- Reescritura de textos (>130 palabras)

Para estos: manual, en CSV, con validación por pares.

### Aplicar en producción

Los fixes de contenido se ejecutan en build.sh, no en migraciones, porque migrate corre antes de los seeds:

    python scripts/_fix_tildes.py --apply || true

Cuando Render haga el próximo deploy exitoso (reset de quota o upgrade), se aplica solo.

## 3. Guía para profesores

### Qué revisar

- /gramatica/ — títulos, teorías y reglas con tildes correctas
- /lectura/ — textos coherentes y ejercicios del nivel
- /lectura/flashcards/ — preguntas claras
- /cursos/ — títulos descriptivos

### Cómo reportar

1. Captura o copia del texto incorrecto
2. Ruta exacta (ej. /gramatica/ → Gramática castellana → Nebrija)
3. Modelo afectado (técnica, texto, flashcard)

No abras GitHub issues. Envía al desarrollador con esos 3 datos.

### Estado actual

Corregido (2026-11-09):
- 174 tildes en 99 registros de TecnicaGramatical
- 810 registros con 0 errores

Pendiente (deuda documentada):
- 98 placeholders en A1 (no enseñan)
- 4 textos A1 densos (>130 palabras, objetivo 60-100)
- Enriquecimiento en Render (pendiente próximo deploy)
- Fix tildes en Render (pendiente próximo deploy)

## 4. Guía para estudiantes

### Cómo empezar

1. Regístrate en /registro/
2. Lee un texto A1 en /lectura/ (El perro perdido, Mi escuela, La fiesta de cumpleaños, Los animales de la granja)
3. Haz los ejercicios debajo del texto
4. Repasa 10 min en /lectura/flashcards/
5. Mira tu progreso en /estudiante/

### Qué está pulido

- 704 ejercicios funcionales
- Tildes corregidas en gramática
- SRS de flashcards funciona
- Dashboard real (no decorativo)

### Qué está menos pulido

- 98 ejercicios A1 de relleno (¿A qué técnica corresponde X?). Pasa al siguiente.
- 4 textos A1 densos. Léelos despacio.
- En Render no hay explicación después de responder. Pendiente próximo deploy.

### Cómo reportar

Copia el texto, apunta la ruta, envía al profesor. No es útil reportar "hay errores" sin decir dónde.

### Cómo aprovechar

- 25 min al día es mejor que 3 horas un domingo
- No saltes los textos
- Usa el SRS (10 min diarios)
- Mira el ranking sin obsesión
- Los certificados son reales y descargables en PDF

## 5. Scripts del repo

Todos read-only por defecto. Solo _fix_* y _enrich_* requieren --apply.

| Script | Para quién | Qué hace |
|--------|-----------|----------|
| pilot_test.py | Devs | Test 13 secciones |
| diag_all.py | Devs | Auditoría integral |
| _diag_preflight.py | Devs | Pre-flight |
| _diag_tildes.py | Devs, profes | Diagnóstico de tildes |
| _fix_tildes.py | Devs | Corrige tildes (DRY-RUN/--apply) |
| _diag_contenido_a1.py | Devs, profes | Estado del contenido A1 |
| _enrich_payloads.py | Devs | Añade explicación (DRY-RUN/--apply) |

## 6. Estado actual del proyecto

Cerrado:
- Pilot test 13/13
- Tildes en TecnicaGramatical: 0 errores
- Enrichment A1: local aplicado, Render pendiente
- M3 (Flashcard congelado): decidido y documentado
- Dashboard onboarding: hero + metas OK

Pendiente (deuda documentada):
- 98 placeholders A1 (prioridad alta, Fase 3 del ensayo)
- 4 textos A1 densos (prioridad media, Fase 1 del ensayo)
- Render sin enrichment (infra, no código)
- Render sin fix tildes (se aplica en próximo deploy)

## Apéndice: ensayo de 5 fases para contenido A1

1. Curaduría de textos (10-12 textos de 60-100 palabras)
2. Mapeo texto ↔ técnica (sin sobrecarga >15 por texto)
3. Reemplazar 98 placeholders con contenido real
4. Validación por pares + piloto con estudiantes
5. Seed y verificación (pilot_test.py [13])

Siguiente sprint: contenido, no ingeniería.