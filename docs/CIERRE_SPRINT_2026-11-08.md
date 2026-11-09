# Cierre de sprint — 2026-11-08

## Resumen ejecutivo

- **Local**: cerrado en verde.
- **Render**: bloqueado por quota de build minutes agotada (no es un bug de código).
- **Sprint de ingeniería**: cerrado. No hay trabajo pendiente en código.
- **Sprint de contenido A1** (ensayo de 5 fases, 10 semanas): **no iniciado**.

El código en `main` está estable. Lo único que diferencia local de producción es el
enriquecimiento de payloads A1 (`payload["explicacion"]`), que en local está aplicado
y en Render espera al próximo build exitoso.

---

## Qué está cerrado (local)

| Área | Estado |
|---|---|
| Pilot test (13 secciones) | ✅ 13/13 OK |
| `diag_all.py` | ✅ 0 FAILs |
| `_diag_preflight.py` | ✅ 0 FAILs |
| Dashboard onboarding (hero + metas) | ✅ |
| Timezone (naive datetimes) | ✅ 0 detectados |
| Ratio A1 | ✅ 2.00 ej/tec |
| M3 (Flashcard congelado) | ✅ documentado |
| Enrichment payloads A1 | ✅ 102 aplicados |
| Rúbrica automática | 3.45/5 |

## Qué está bloqueado (Render)

**Causa**: `build minutes` del plan Free agotados.

Esto no es un bug de código. El código en Render es `baf4109` (estable, funcional).
Los commits posteriores (`4ef5ebb` en adelante) añaden enrichment y limpieza de
`build.sh`, pero no se han podido desplegar porque Render cancela los builds en 0.4s
antes de ejecutar `bash build.sh`.

**No hay nada que arreglar en `build.sh`.** Los 5 commits de "fix" al `build.sh`
(4ef5ebb, ea1bc3c, e8d27e9, 96e7b14, más intentos) fueron parches a un problema que
no existía. La causa real era la quota.

### Desbloqueo

- **Opción A (gratis)**: esperar reset mensual de quota. Los commits pendientes se
  aplicarán automáticamente al próximo build exitoso.
- **Opción B (pago)**: upgrade a Starter ($7/mo). Elimina el límite y permite usar
  `Pre-Deploy Command` (adiós `build.sh` hack).
- **Opción C (migración)**: Fly.io / Railway. Más setup.

---

## Decisiones tomadas

### M3 — Congelar `Flashcard`

- **Decisión**: no se toca el modelo `Flashcard`. `_apply_opcion_m.py` permanece en
  repo pero no se ejecuta.
- **Motivo**: 0 usos en views reales. `views_flashcards_sesion.py`, `views_lectura.py`
  y `views_estudiante.py` usan `ProgresoTecnicaLectura` + `TecnicaLectura`. El
  `Flashcard` legacy está efectivamente muerto.
- **Documentado en**: `docs/CIERRE_AUDITORIA_MCER.md` (commit `5355e59`).

### Placeholders A1 — Deuda documentada

- **Decisión**: dejar los 98 ejercicios placeholder en DB.
- **Motivo**: crear 98 ejercicios pedagógicamente válidos requiere trabajo de contenido
  real (8-12h), no de ingeniería. La ratio 2.00 se cumple; la calidad pedagógica no.
- **Documentado en**: `docs/CIERRE_AUDITORIA_MCER.md`.
- **Reemplazo**: cuando se aborde Fase 3 del ensayo.

### Enrichment local vs Render

- **Local**: aplicado (`_enrich_payloads.py --apply`). Rúbrica 2.70 → 3.45.
- **Render**: pendiente por quota. Se aplicará solo en el próximo deploy exitoso.

---

## Estado de las fases del ensayo A1

El ensayo instructivo sobre producción de contenido real define 5 fases
(10 semanas estimadas). Estado actual:

| Fase | Descripción | Estado |
|---|---|---|
| 1 | Curaduría de textos (10-12 textos, 60-100 palabras) | ❌ 4 textos, todos >130 palabras |
| 2 | Mapeo texto↔técnica (sin sobrecarga >15/técnica) | ❌ 20-23 técnicas por texto |
| 3 | Reemplazar 98 placeholders con contenido real | ❌ 51% del contenido A1 es placeholder |
| 4 | Rúbrica automática ≥4.0/5 | ❌ 3.45/5 |
| 5 | Seed verificado en pilot | ❌ depende de Fase 3 |

**Ninguna fase está completa.** El ensayo es el plan para abrirlas, no un trabajo hecho.

---

## Scripts versionados

Estos scripts están en `main` y se ejecutan sin modificar la DB por defecto
(read-only o DRY-RUN):

| Script | Propósito | Modo |
|---|---|---|
| `scripts/pilot_test.py` | Test de aceptación (13 secciones) | read-only + temp users |
| `scripts/diag_all.py` | Auditoría integral del proyecto | read-only |
| `scripts/_diag_preflight.py` | Pre-flight antes de cambios | read-only |
| `scripts/_diag_contenido_a1.py` | Estado del contenido A1 (5 fases) | read-only |
| `scripts/_enrich_payloads.py` | Enriquece payloads con `explicacion` | DRY-RUN / --apply |
| `scripts/_apply_opcion_m.py` | Migración M1 (no ejecutar, M3 elegido) | DRY-RUN |
| `scripts/_seed_densificacion_a1.py` | Seed de 98 ejercicios A1 | DRY-RUN / --apply |

**Nota**: `_apply_opcion_m.py` y `_seed_densificacion_a1.py` tienen el modo
peligroso (--apply) documentado. No ejecutar sin decisión explícita.

---

## Migraciones

| Migración | Contenido | Estado local | Estado Render |
|---|---|---|---|
| `0035_enrich_a1_payloads_explicacion.py` | Enriquece payloads A1 | ✅ aplicada | ⏳ pendiente deploy |

La migración `0026_enrich_a1_payloads_explicacion.py` (rota, dependency en leaf node
incorrecto) fue eliminada en `d26fe96`.

**Nota**: la migración `0035` corre en `manage.py migrate`, que `build.sh` ejecuta
**antes** de los seeds. Eso significa que en una DB vacía, `0035` enriquece 0 filas
y no se vuelve a ejecutar. El enrichment real en producción debe venir del
`_enrich_payloads.py --apply` al final de `build.sh` (post-seeds), no de la migración.

---

## Lecciones aprendidas

### Patrón a evitar: fixes sin causa raíz

5 commits consecutivos (`4ef5ebb`, `ea1bc3c`, `e8d27e9`, `96e7b14`, más intentos)
intentaron arreglar `build.sh` como si el problema fueran CRLF, BOM o shebang.
Ninguno verificó el **log real de Render**. La causa era quota agotada.

**Regla para futuros sprints**: cuando un deploy falla en <1s o de forma repetida,
pedir el log completo de Render **antes** de tocar código. Si el log no se puede
obtener en el momento, no commitear fixes profilácticos.

### Patrón positivo: scripts read-only + verificación

`diag_all.py`, `_diag_preflight.py` y `_diag_contenido_a1.py` son read-only y
permiten diagnosticar sin riesgo. Son el modelo a seguir.

### Patrón positivo: migraciones reversibles

`0035` incluye `reverse_enrich` (borra `explicacion` del payload). Se puede revertir
con `manage.py migrate core 0034`. Sin esto, un error en producción sería difícil
de deshacer.

### Patrón negativo: PowerShell como lenguaje de scripting

Los `Replace` con overload de 3 argumentos (que no existe en PS 5.1), los `f\"...\"`
que rompen el parser, los `Add-Content` con CRLF implícito, los here-strings con
`$` sin escapar... PowerShell ha costado más tiempo que el código Python que genera.
Para scripts de este tamaño, un `.py` con `subprocess` a `git` sería más robusto.

---

## Próximos pasos

### Cuando se desbloquee Render (reset o upgrade)

1. Verificar que el deploy aplica `0035` y `_enrich_payloads.py`:
   - Render Logs: buscar `Enriching A1 payloads...` y `[OK] Actualizados: 102`
2. Verificar funcional: `/lectura/` → texto A1 → click ejercicio → ¿aparece `explicacion`?
3. Si no aparece: revisar orden en `build.sh` (¿`migrate` antes o después de seeds?)

### Cuando se aborde el contenido (Fase 1 del ensayo)

1. Escribir 6 textos A1 de 60-100 palabras (temas: presentación, rutina, lugar,
   narración, instrucción, opinión).
2. Reescribir los 4 textos actuales (`El perro perdido`, `Mi escuela`,
   `La fiesta de cumpleaños`, `Los animales de la granja`) a 60-100 palabras.
3. Reasignar técnicas a textos para que ningún texto soporte >15.
4. `python scripts/_diag_contenido_a1.py` → Fase 1 debe pasar a ✅.

### Cuando se aborde el contenido (Fase 3)

1. Generar CSV: `python scripts/_plan_densificacion.py --nivel A1 --csv docs/plan_densificacion_A1_full.csv`
2. Añadir columnas `enunciado`, `opcion_a`, `opcion_b`, `opcion_c`, `correcta`.
3. Rellenar 98 filas con preguntas reales (no placeholders).
4. Borrar placeholders: `E.objects.filter(enunciado__contains="(repaso)").delete()`
5. `python scripts/_seed_densificacion_a1.py --mode csv --apply`.

---

## Commits relevantes del sprint
96e7b14 build(v3): build.sh limpio (40 líneas, sin duplicados, shebang OK) + .gitattributes sin BOM
e8d27e9 build(v2): enrich A1 sin condicional + normaliza build.sh
ea1bc3c fix(build): simplifica enrichment (sin if RUN_SEEDS) + .gitattributes LF
4ef5ebb build: corre enrich payloads A1 despues de seeds (migrate corre antes, ve DB vacia)
baf4109 fix(diag): reconfigure UTF-8 + Fase 2 detecta sobrecarga (no solo textos faltantes)
d26fe96 fix(migration): 0035 reemplaza 0026 rota (dependency en 0034, leaf real de core)
e3f4944 feat(migration): enriquece payloads A1 con explicacion (data migration para Render)
f1a4698 chore: versiona diag contenido A1 + enrich payloads
5355e59 docs: cierra sprint con decision M3 (congelar Flashcard) y placeholders A1 como deuda
2d0e588 docs: placeholders A1 documentados como deuda (ratio 2.00 con relleno)
aa0ff84 feat: densifica A1 a 2.00 ej/tec + blindaje pilot [13]

Los commits `4ef5ebb` a `96e7b14` son técnicamente correctos (build.sh limpio es
mejor que build.sh duplicado) pero no resolvieron el problema real (quota agotada).
Se mantienen por higiene, no como fix.

---

## Nota final

El sprint de ingeniería está cerrado. El proyecto está funcional en local y en
producción (Render `baf4109`). La única diferencia visible al usuario es que en
producción los ejercicios A1 no muestran la explicación después de responder,
porque el enrichment no se ha aplicado por quota.

**No hay trabajo pendiente en código.** Lo que queda es:

1. Contenido (Fase 1-4 del ensayo, 10 semanas).
2. Desbloqueo de Render (quota o upgrade, no código).

Cualquier nueva "mejora" al código ahora será deuda cosmética o ruido. El siguiente
sprint debe ser de contenido o de infraestructura, no de ingeniería.