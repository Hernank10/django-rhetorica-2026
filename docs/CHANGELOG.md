# Changelog

## v1.7.8 — Documentacion de certificaciones (modulo15 + guia)

- `docs/modulo15_certificaciones.md` (nuevo, 12 secciones, ~11.6 KB)
- `docs/guia_certificaciones.md` (nuevo, 7 secciones, ~12.5 KB)
- Actualiza `docs/README.md` con links a modulo15 + guia

## v1.7.7 — Otorgamiento automatico de certificaciones (1,311 certs)

- `core/services/certificaciones.py`: motor (get_user_stats, cumple_requisitos, verificar_y_otorgar)
- `core/signals_progreso.py`: signal auto_cert_al_completar
- `core/management/commands/otorgar_certificaciones.py`: backfill con --user y --dry-run
- `core/tests/test_certificaciones_auto.py`: 13 tests verdes
- **1,311 certificaciones emitidas** (147 previas + 1,164 auto-otorgadas)
- Cierra deuda tecnica: no mas emision manual obligatoria

## v1.7.6 — Guia del sistema de certificaciones

- `docs/guia_certificaciones.md`: 7 secciones (estudiantes, profesores, admins)
- 49 certificaciones activas documentadas
- 5 niveles (Bronce -> Diamante)

## v1.7.5 — Seed de 45 estudiantes certificados

- `scripts/seed_test_certs.py`: 85 certs para est001-est045
- `core/admin.py`: CertificacionObtenida registrado
- `core/views_profesor.py`: lista_certificaciones filtra por profesor_asignado

## v1.7.2 — Fix tildes en presentacion de modulos

- 14 reemplazos en dashboard/base/indice (Gramatica -> Gramática, tecnicas -> técnicas)

## v1.7.1 — Documentacion completa modulos 11-14

- `docs/modulo11_gramatica.md` (16 secciones)
- `docs/modulo12_generativa.md` (12 secciones)
- `docs/modulo13_a1.md` (12 secciones)
- `docs/modulo14_b1.md` (12 secciones)
- README actualizado

## v1.7.0 — Lengua Castellana B1 completa (400 tecnicas totales)

- 100 tecnicas B1 (301-400), bloques A-G
- 100 ejercicios tipo 1
- 400 totales (100 gram + 100 gen + 100 A1 + 100 B1)

## v1.6.0 — Lengua Castellana A1 completa (300 tecnicas)

- 100 tecnicas A1 (201-300), bloques A-G
- 300 tecnicas totales

## v1.5.0 — Gramatica generativa completa (200 tecnicas)

- 100 tecnicas GGT (101-200)
- Migracion 0020 (campo modulo)
- 200 tecnicas totales

## v1.4.0 — Gramatica castellana completa (100 tecnicas)

- 100 tecnicas gramatica (1-100)
- 100 tecnicas totales

## v1.3.x — Modulo 10: Sintaxis del castellano (100 tecnicas)

- v1.3.1: dashboards por rol
- v1.3.0: sintaxis integrada en LMS
- v1.2.1: 5 vistas + 3 templates + JS AJAX
- v1.2.0: 100 tecnicas + 100 ejercicios

## v1.1.x — Base del proyecto

- v1.1.7: docs cierre v1.1.x
- v1.1.5: STORAGES condicional via USE_S3
- v1.1.4: settings split (base/dev/prod)
- v1.1.3: requirements.txt curado
- v1.1.2: SECRET_KEY fuera del codigo (.env)
- v1.1.1: CRUD profesor tests + @profesor_required

## v1.0.0 — Base inicial

- Modelos base: Curso, Leccion, ProgresoUsuario
- SRS, POS, redaccion, corpus, parafrasis, TTS
- Tests iniciales

---

## Proximos hitos

- **Deploy R2 + Render** (pendiente desde v1.1.5)
- Posible fase 2: A2, B2, C1, C2
- Posible fase 2: audio con TTS
- Posible fase 2: mas tipos de ejercicios (4 y 5)