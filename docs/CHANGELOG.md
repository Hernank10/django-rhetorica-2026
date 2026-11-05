# Changelog

Historial de versiones del proyecto `django-rhetorica`.
Formato: [Keep a Changelog](https://keepachangelog.com/), versionado semantico.

---

## [v3.4.2-lectura-v40c-completo] — 2026-11-05

### Added
- **Documentacion completa** del proyecto (este CHANGELOG, README, ESTADO)
- Reportes separados: `REPORTE_TILDES_v8_v40b.md/.txt` y `REPORTE_REDACCION_v8_v40b.md/.txt`
- Sprint de integracion v8-v40c: 317 tildes + 151 redacciones + 12 reescrituras

### Fixed
- **`observo Ramos` → `observó Ramos`** en 'El misterio del cuadro robado'
- **`energetica` → `energética`** en 'La promesa incumplida de la empresa energética'
- `continua dentro` → `continúa dentro` en 'La fiesta de cumpleaños'

### Commits
- `e27b0d6` v40c: 2 residuos + 4 reportes
- `0776471` reporte tildes y redaccion v8-v40b
- `e9076a4` v40b: continua dentro
- `26eeddd` v40 master: aplicar todos los fixes v8-v39

---

## [v3.4.1-lectura-v40-completo] — 2026-11-04

### Added
- **Master fix v40** que aplica TODOS los fixes v8-v39 en TODOS los textos
- 162 correcciones en 23 textos

### Fixed
- Residuos de tildes en textos C2, C1, B2, B1, A2, A1
- Coherencia redaccion: pronombres tonicos, concordancia, subjuntivo, signos `¿?`

### Commits
- `26eeddd` v40 master

---

## [v3.4.0-lectura-v8-v39-real] — 2026-11-04

### Added
- Correcciones individuales v8-v39 para los 27 textos revisados texto por texto
- Scripts `_upgrade_v8.py` ... `_fix_master_v40.py` para trazabilidad

### Fixed (muestra)
- v8-v10: `El archivo de los espejos` (214 correcciones)
- v11-v12: `El cuerpo como mercancia` (198 correcciones)
- v13: `El cuento que se escribia solo` (87)
- v14-v36: `Analisis critico del discurso institucional` (~200)
- v15: `Desinformacion` (221)
- v24: `Turismo masivo` (50 + 5 reescrituras)
- v25: `Semana laboral de 4 dias` (32)
- v26: `Viaje de Santiago` (33)
- v37: `IA en la educacion` (30)
- v38: `Manipulacion del lenguaje` (24)
- v39: `Sujeto atrapado` (30)

---

## [v3.4.4-b2-textos] — 2026-11-03

### Added
- Textos B2 completos con ejercicios
- Tags: `v3.4.0-b2-p1`, `v3.4.1-b2-p2`, `v3.4.2-b2-p3`, `v3.4.3-b2-completo`, `v3.4.4-b2-textos`

---

## [v3.3.5-lectura-b1-tecnicas-completas] — 2026-11-02

### Added
- **100 tecnicas B1** completas (P1-P4 = 25 c/u)
- Tags: `v3.3.0-lectura-b1-p1`, `v3.3.1-lectura-b1-p2`, `v3.3.2-lectura-b1-p3`, `v3.3.3-lectura-b1-completo`, `v3.3.4-lectura-b1-textos`, `v3.3.5-lectura-b1-tecnicas-completas`

---

## Notas

### Sobre la nomenclatura de tags

- `v3.3.x-lectura-b1-*` — sprint B1 tecnicas
- `v3.4.x-b2-*` — sprint B2 textos
- `v3.4.x-lectura-v*-*` — sprint de tildes y redaccion

### Sobre los reportes

Los reportes `.md` son para leer/renderizar. Los `.txt` son para email o logs.
Ambos se generan con `scripts/_reportes_unificados.py`.