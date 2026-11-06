# Reporte final: Ortografia y redaccion de tarjetas contextuales

## Estado final

| Fase | Descripcion | Cambios |
|---|---|---|
| 1 | Eliminar duplicados (`tarjeta-guia-certificados` x5) | -5 tarjetas |
| 2 | Corregir titulos `Que`/`Como`/`Cual` | 14 |
| 3 | Tildes en texto visible | 276 |
| 4a | Residuales (`redaccion`, `retorica`, `linguisticas`) | 12 |
| 4b | SIGNOS (1 real + 5 citas) | 1 |
| **TOTAL** | | **303** |

## Tarjetas: antes vs despues

- Antes: 30 tarjetas, 5 IDs duplicados, 340 hallazgos
- Despues: 25 tarjetas, 0 duplicados, 1 hallazgo (cita)

## Hallazgos no corregidos (por diseno)

- 5 SIGNOS: citas de ejemplo entre comillas (`Ej: "Cuando sucedio X?"`) — decision editorial
- 75 BAJA: artefactos del extractor (espacios entre `</em>` y `,`), enumeraciones abiertas con `...`, transiciones de bloque (`</h5><p>`)

## Commits

- 7215934: Fase 1 (duplicados)
- 42250bb: Fase 2 (titulos)
- 41f7a51: Fase 3 (tildes)
- [PENDIENTE]: Fase 4a + 4b

## Tag

v3.5.2-ortografia-tarjetas