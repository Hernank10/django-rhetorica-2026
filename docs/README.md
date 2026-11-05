# django-rhetorica — Documentacion

*Actualizado: 2026-11-05 12:38*

Plataforma de aprendizaje de retorica y lectura en espanol, 
organizada por niveles MCER (A1, A2, B1, B2, C1, C2).

---

## Estado del proyecto

| Metrica | Valor |
|---|---|
| Textos | 36 |
| Ejercicios | 606 |
| A1 | 4 textos |
| A2 | 7 textos |
| B1 | 7 textos |
| B2 | 7 textos |
| C1 | 7 textos |
| C2 | 4 textos |
| Correcciones tildes | 317 |
| Correcciones redaccion | 151 |
| Ejercicios reescritos | 12 |
| Residuos reales | 0 |
| Ultimo commit | `9f78469 docs(lectura): listado completo de 36 textos con correcciones (317 tildes + 157 redacciones + 12 contenido)` |
| Ultimo tag | `v3.4.2-lectura-v40c-completo` |

---

## Reportes disponibles

| Documento | Descripcion |
|---|---|
| [REPORTE_TILDES_v8_v40b.md](REPORTE_TILDES_v8_v40b.md) | Detalle de 317 tildes por texto |
| [REPORTE_TILDES_v8_v40b.txt](REPORTE_TILDES_v8_v40b.txt) | Version texto plano |
| [REPORTE_REDACCION_v8_v40b.md](REPORTE_REDACCION_v8_v40b.md) | 151 correcciones contextuales + 12 reescrituras |
| [REPORTE_REDACCION_v8_v40b.txt](REPORTE_REDACCION_v8_v40b.txt) | Version texto plano |
| [CHANGELOG.md](CHANGELOG.md) | Historia de versiones v8 -> v40c |
| [ESTADO_PROYECTO.md](ESTADO_PROYECTO.md) | Snapshot tecnico actual |

---

## Sprints cerrados

### Sprint v8 - v40c (tildes y redaccion)

- **Alcance:** 36 textos, 606 ejercicios
- **Correcciones:** 317 tildes + 151 redacciones + 12 reescrituras de contenido
- **Commits clave:**
  - `e27b0d6` v40c - observo Ramos + energetica + reportes
  - `0776471` reporte tildes y redaccion v8-v40b
  - `e9076a4` v40b - continua dentro
  - `26eeddd` v40 master - todos los fixes v8-v39
  - `58876b4` v26 - B1 viaje de Santiago (ultimo fix individual)
- **Tag:** `v3.4.2-lectura-v40c-completo`

### Sprint B2 (previo)

Tags: `v3.4.0-b2-p1`, `v3.4.1-b2-p2`, `v3.4.2-b2-p3`, `v3.4.3-b2-completo`, `v3.4.4-b2-textos`

### Sprint B1 (previo)

Tags: `v3.3.0-lectura-b1-p1`, `v3.3.1-lectura-b1-p2`, `v3.3.2-lectura-b1-p3`, `v3.3.3-lectura-b1-completo`, `v3.3.4-lectura-b1-textos`, `v3.3.5-lectura-b1-tecnicas-completas`

---

## Como regenerar los reportes

```powershell
# 1. Aplicar fixes pendientes (si hay)
E:\PythonPortable_Django5\python.exe scripts\fix_tildes.py
E:\PythonPortable_Django5\python.exe manage.py seed_lectura_textos

# 2. Regenerar los 4 reportes (md + txt)
E:\PythonPortable_Django5\python.exe scripts\_reportes_unificados.py

# 3. Regenerar esta documentacion
E:\PythonPortable_Django5\python.exe scripts\_generar_documentacion.py

# 4. Commit
git add docs/
git commit -m "docs: regenerar reportes y documentacion"
git push origin main
```

---

## Pendientes estructurales

1. **Cobertura B1** — cada tecnica tiene 1 ejercicio; faltan 2-4 mas por tecnica (Sprint B1.5)
2. **Integracion `fix_tildes.py`** — consolidar WORDS_V8...V40c en dict global + regex con tests de regresion
3. **Cobertura de textos no revisados individualmente** — verificar 'La promesa incumplida' y otros que solo pasaron por v40 master
4. **Regresion completa en pytest** — antes del proximo tag de cierre
