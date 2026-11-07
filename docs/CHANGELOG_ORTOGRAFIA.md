# Changelog: Ortografía y redacción

**Proyecto:** django-rhetorica
**Última actualización:** 2026-11-06
**Tags:** v3.5.2-ortografia-tarjetas

---

## Resumen ejecutivo

| Fase | Descripción | Cambios | Commit |
|---|---|---|---|
| 1 | Eliminar `tarjeta-guia-certificados` duplicada | -5 tarjetas | `7215934` |
| 2 | Corregir títulos `Que/Como/Cual` sin tilde | 14 | `42250bb` |
| 3 | Tildes en texto visible de tarjetas | 276 | `41f7a51` |
| 4a | Residuales (`redaccion`, `retorica`, `linguisticas`) | 12 | `d88ab07` |
| 4b | SIGNOS (1 real + 5 citas) | 1 | `d88ab07` |
| 5 | Restaurar `tarjeta-guia-certificados` con tildes | 13 | `e4d1954` |

**Total tarjetas:** 30 (25 + 5 restauradas)
---

## Fase 1 — Eliminar tarjetas duplicadas (2026-11-06)

**Motivo:** `tarjeta-guia-certificados` repetida en 5 archivos de estudiante.

**Script:** `_fix_ortografia_v1_duplicados.py`

**Acción:** eliminación balanceada de `<div>` con `HTMLParser`.

**Resultado:**
- 5/5 archivos limpiados
- Backup automático en `docs/backups/<timestamp>/`

---

## Fase 2 — Corregir títulos (2026-11-06)

**Motivo:** títulos `<h1>`-`<h6>` dentro de tarjetas empezaban por `Que`, `Como`, `Cual`.

**Script:** `_fix_ortografia_v2_titulos.py`

**Resultado:**
- 14 títulos corregidos
- 0 falsos positivos

**Ejemplos:**
- `"Que es un corpus"` -> `"Qué es un corpus"`
- `"Como funciona SM-2"` -> `"Cómo funciona SM-2"`
---

## Fase 3 — Tildes en texto visible (2026-11-06)

**Motivo:** 245 palabras sin tilde en el cuerpo de las tarjetas.

**Script:** `_fix_ortografia_v3_tildes.py`

**Estrategia:** parser text-aware que distingue TAG / TEXT / RAW.

**Resultado:**
- 276 cambios en 23 archivos
- 0 roturas de HTML

**Top palabras:**
- `tecnicas` -> `técnicas` (43x)
- `tecnica` -> `técnica` (34x)
- `dia` -> `día` (18x)

---

## Fase 4a — Residuales (2026-11-06)

**Motivo:** palabras fuera del diccionario de Fase 3.

**Script:** `_fix_ortografia_v4_residuales.py`

**Palabras añadidas:** `redaccion`, `retorica`, `retoricas`, `linguisticas`.

**Resultado:** 12 cambios en 4 archivos.
---

## Fase 4b — SIGNOS (2026-11-06)

**Motivo:** preguntas sin `¿`.

**Decisión:** de 6 detecciones, solo 1 era error real (las otras 5 eran citas entre comillas).

**Corrección:**
- `No tienes evaluaciones pendientes?` -> `¿No tienes evaluaciones pendientes?`

---

## Fase 5 — Restaurar tarjeta guía (2026-11-06)

**Script:** `_restore_guia_certificados.py`

**Fuente:** `docs/backups/20261106_174842/`.

**Resultado:** 5/5 restauradas con tildes (`Guía`, `verificación`, `código`).

---

## Pendiente

- [ ] Fase 6 — `/lectura/guia-certificados/`: fix `Guia` -> `Guía` en template + vista.
- [ ] Fase 7 — `/redaccion/tecnicas/`: fix `{% for t in técnicas %}` -> `{% for t in tecnicas %}`.
- [ ] Blindar scripts de ortografía para NO tocar `{% ... %}` ni `{{ ... }}`.
---

# Lecciones aprendidas

---

## Bug #1 — f-string con `{% ... %}` en Python

**Síntoma:** `SyntaxError: f-string: expecting a valid expression after '{'`

**Causa:** `print(f"texto con {% include %}")`. Python interpreta `{%` como expresión.

**Fix:** quitar la `f` si no hay variables, o duplicar llaves.

**Regla:** en cualquier `f"..."` con `{%` o `{{`, duplicar llaves o quitar la `f`.

---

## Bug #2 — `except Exception: pass` como agujero negro

**Síntoma:** auditor reportó 0 templates, 0 tarjetas.

**Causa:** `try: ... except Exception: pass` silenciando errores.

**Fix:** loggear el error.

**Regla:** `except: pass` es siempre un bug latente.
---

## Bug #3 — `{# ... #}` dentro de f-string

**Síntoma:** `SyntaxError` en `_add_tarjeta_logros_ranking.py`.

**Causa:** f-string contenía `{# Dos columnas #}` (comentario Django). Python lo interpreta como inicio inválido.

**Fix:** sustituir `{# ... #}` por `<!-- ... -->`.

**Regla:** nunca uses `{# #}` dentro de `f"""..."""`.

---

## Bug #4 — import faltante en URLs dinámicas

**Síntoma:** `NameError: name 'va' is not defined`.

**Causa:** script insertó `path(..., va.lectura_asistida, ...)` pero olvidó `from . import views_lectura_asistida as va`.

**Fix:** añadir el import.

---

## Bug #5 — Variable Django con tilde (CRÍTICO)

**Síntoma:** `/redaccion/tecnicas/` muestra "No hay técnicas" aunque hay 120 en DB.

**Causa:** template usa `{% for t in técnicas %}` (con tilde) pero view pasa `context["tecnicas"]` (sin tilde). El for-loop itera sobre variable inexistente = vacío.

**Fix:** cambiar `técnicas` -> `tecnicas` en el template.

**Regla crítica:** las variables de Django NO llevan tildes. Solo el texto visible entre tags lleva tildes.

**Lección principal:** los scripts de ortografía nunca deben procesar el interior de `{% ... %}` ni `{{ ... }}`.
---

## Bug #6 — `core_root` duplicado en resolver

**Síntoma:** `_diag_guia_py_only.py` resolvió 0 de 23 imports.

**Causa:** `core_root = cwd / "core"` y luego `core_root / Path("core", "services")` generaba `core/core/services/` (duplicado).

**Fix:** `core_root.parent / Path(*sub)` o quitar el prefijo `core.`.

---

## Bug #7 — Script de ortografía procesando sintaxis Django

**Síntoma:** variable `técnicas` con tilde en `{% for %}` (Bug #5).

**Causa:** script anterior aplicó diccionario al HTML completo sin proteger `{% %}` ni `{{ }}`.

**Fix:** los scripts deben saltarse `<script>`, `<style>`, `<code>`, `<pre>`, `{% ... %}` y `{{ ... }}`. Solo procesar texto entre tags HTML.

**Pseudocódigo:**

- Si encuentra `{%` -> saltar hasta `%}`
- Si encuentra `{{` -> saltar hasta `}}`
- Si encuentra `<`  -> saltar hasta `>`
- Si no -> aplicar diccionario al texto
---

## Bug #8 — No se pudo cerrar el div

**Síntoma:** scripts de "remover tarjeta" no borraban nada.

**Causa:** conteo manual de `<div>` fallaba con strings JS dentro de `<script>`.

**Fix:** usar `HTMLParser` que distingue tags reales de strings.

**Regla:** para manipular HTML, siempre `HTMLParser`, nunca regex ni conteo manual.
---

## Bug #9 — La guía vive en .md, no en el template

**Síntoma:** `_diag_fix_guia_cert.py` no encontraba las 40 palabras perdidas.

**Causa:** el template `guia_certificados.html` solo tiene 36 palabras. El texto real está en `docs/GUIA_CERTIFICADOS.md` (8428 bytes, 1313 palabras) y se renderiza con `markdown.markdown()` en la vista.

**Fix:** auditar el `.md`, no el template.

**Regla:** si un template tiene mucho menos texto que el HTML renderizado, el contenido viene de otro lado. Buscar en includes recursivos, `.md`, strings en la vista (con AST), modelos con TextField, o fixtures JSON.

---

## Bug #10 — Técnicas de redacción en otro modelo

**Síntoma:** `/redaccion/tecnicas/` vacío aunque DB tiene 120 técnicas.

**Causa:** template usaba `{% for t in técnicas %}` con tilde (Bug #5). El view usaba el modelo correcto (`EjercicioLinguistico`), pero el template no encontraba la variable.

**Dato adicional:** `TecnicaSintactica` tiene 100 registros pero NO son las técnicas de redacción (son sintácticas). Las 120 reales están en `EjercicioLinguistico` con `es_redaccion=True`.

**Regla:** cuando hay múltiples modelos similares, verificar cuál es el correcto antes de cambiar el view.

---

## Checklist para futuras sesiones

**Antes de aplicar scripts de ortografía:**

- [ ] Distingue TAG / TEXT / RAW / `{% %}` / `{{ }}`?
- [ ] Verifica `manage.py check` al final?
- [ ] DRY-RUN antes de `--apply`?
- [ ] Backup con timestamp?
- [ ] Idempotente?
- [ ] Log de cada cambio?
- [ ] Re-renderiza para verificar?

**Antes de crear un script de fix:**

- [ ] Identificaste el archivo fuente real (no el render)?
- [ ] Path resuelto con `resolve()` + `inspect`?
- [ ] Includes recursivos contemplados?
- [ ] `.md` / `.json` externos contemplados?
- [ ] Modelos con `TextField` contemplados?