# Índice de scripts (ortografía y redacción)

Catálogo de todos los scripts de esta sesión.

---

## Diagnóstico (SOLO LECTURA)

| Script | Propósito | Salida |
|---|---|---|
| `_diag_tarjetas_inventario.py` | Inventario de `<div id="tarjeta-*">` | `INVENTARIO_TARJETAS.md` |
| `_audit_ortografia.py` | Auditoría de tarjetas (ALTA/MEDIA/SIGNOS/BAJA) | `AUDIT_ORTOGRAFIA_v1.md` |
| `_audit_detallado_signos_baja.py` | Detalle de SIGNOS y BAJA con contexto | consola |
| `_audit_global.py` | Auditoría de TODOS los templates | `AUDIT_GLOBAL.md` + dumps |
| `_diag_template.py` | Template reutilizable de diagnóstico | `AUDIT_<SLUG>.md` |
| `_diag_guia_py_only.py` | Busca strings de guía en `.py` | `DIAG_GUIA_PY_ONLY.md` |
| `_diag_guia_view_source.py` | Lee source de vista con AST | `DIAG_GUIA_VIEW_SOURCE.md` |
| `_diag_tecnicas_redaccion.py` | Diag de `/redaccion/tecnicas/` | consola |
| `_diag_tecnicas_redaccion_v2.py` | Diag de modelos + DB | consola |
| `_diag_tecnicas_redaccion_v3.py` | Diag de template + for-loop | consola |
| `_diag_guia_cert_extendido.py` | Busca palabras en py/json/templates/BD | `DIAG_GUIA_CERT_EXTENDIDO.md` |
---

## Fix (ESCRITURA)

| Script | Propósito | Backup | Idempotente |
|---|---|---|---|
| `_fix_ortografia_v1_duplicados.py` | Elimina tarjetas duplicadas | Sí | Sí |
| `_fix_ortografia_v2_titulos.py` | Corrige títulos `<h[1-6]>` | Sí | Sí |
| `_fix_ortografia_v3_tildes.py` | Tildes en texto visible (parser text-aware) | Sí | Sí |
| `_fix_ortografia_v4_residuales.py` | Palabras fuera de Fase 3 | Sí | Sí |
| `_restore_guia_certificados.py` | Restaura tarjetas desde backup | Sí | Sí |
| `_fix_guia_cert_md.py` | Tildes en `GUIA_CERTIFICADOS.md` | Sí | Sí |
| `_fix_guia_cert_residual.py` | Residuales MD + template + vista | Sí | Sí |

---

## Patches (corrigen otros scripts)

| Script | Qué arregla |
|---|---|
| `_fix_import_asistida.py` | Añade `from . import views_lectura_asistida as va` |
| `_fix_syntax_logros.py` | Reemplaza `{# #}` por `<!-- -->` en f-string |
| `_patch_guia_md.py` | Extiende DICC y arregla `¿` dentro del bold |
---

## Scripts de instalación de tarjetas

| Script | Tarjeta instalada |
|---|---|
| `_add_tarjeta_parafrasis.py` | `/sintaxis/parafrasis/` |
| `_add_tarjeta_parafrasis_registro.py` | `/sintaxis/parafrasis/registro/` |
| `_add_tarjeta_redaccion.py` | `/redaccion/` |
| `_add_tarjeta_corpus.py` | `/corpus/` |
| `_add_tarjeta_srs_estadisticas.py` | `/estudiante/srs/estadisticas/` |
| `_add_tarjeta_srs_v2.py` | `/estudiante/srs/repaso/` |
| `_add_tarjeta_lectura_progreso.py` | `/lectura/progreso/` |
| `_add_tarjeta_redaccion_tecnicas.py` | `/redaccion/tecnicas/` |
| `_add_tarjeta_ranking.py` | `/estudiante/ranking/` |
| `_add_tarjeta_flashcards_detallada.py` | `/lectura/flashcards/` |
| `_add_tarjeta_logros_ranking.py` | `/estudiante/logros/` |
| `_add_tarjeta_evaluaciones.py` | `/estudiante/evaluaciones/` |
| `_add_tarjeta_mis_cursos.py` | `/estudiante/cursos/` |
| `_add_tarjeta_dashboard_completa.py` | `/estudiante/` |
| `_add_boton_index_asistida.py` | Botón en `core/index.html` |

Todos idempotentes (SKIP si ya existe).

---

## Convenciones de estilo

- Todo script tiene fase `[0]`/`[1]` de entorno y validación.
- Los de escritura soportan `--apply` (sin flag = DRY-RUN).
- Backup automático en `docs/backups/<timestamp>/`.
- Verificación con `manage.py check` al final.
- Test clients usan `get_or_create` + `user.delete()` en `finally`.
---

## Cómo crear un nuevo script

### 1. Diagnóstico primero (solo lectura)

- Resolver la URL con `resolve()`.
- Leer el template con `inspect.getsource()`.
- Contar registros en modelos.
- Verificar con `Client().get()`.
- Trazar dónde vive el texto.

### 2. Fix después (con `--apply`)

- Backup antes de escribir.
- Parser `HTMLParser` o `ast`, nunca regex de estructura.
- Preservar `{% ... %}` y `{{ ... }}` (nunca tocarlos).
- Escribir solo el texto entre tags HTML.
- Re-renderizar y verificar.

### 3. Documentar

- Añadir al `CHANGELOG_ORTOGRAFIA.md`.
- Si toca template nuevo, actualizar este índice.
---

## Stack

| Componente | Valor |
|---|---|
| Python | `E:\PythonPortable_Django5\python.exe` |
| Django | 5.2.11 |
| Proyecto | `E:\02_proyectos\django-rhetorica` |
| Settings | `django_retorica.settings.dev` |

## Comandos frecuentes

Compilar un script:

    E:\PythonPortable_Django5\python.exe -m py_compile scripts\<nombre>.py

Ejecutar un script:

    E:\PythonPortable_Django5\python.exe scripts\<nombre>.py

Aplicar un fix:

    E:\PythonPortable_Django5\python.exe scripts\<nombre>.py --apply

Check global de Django:

    E:\PythonPortable_Django5\python.exe manage.py check