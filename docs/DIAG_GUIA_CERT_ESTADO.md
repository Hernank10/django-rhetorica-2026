# Diagnostico: estado de la guia de certificados

**Generado:** 2026-11-07 08:23
**Veredicto:** SOSPECHOSO
**Pendientes:** 0  ·  **Corregidos:** 9

---

## 1. Residuales por fuente

| ID | Fuente | Estado | Viejo | Nuevo | Descripcion |
|---|---|---|---|---|---|
| MD-01 | MD | CORREGIDO | `en fase de pilot` | `en fase piloto` | pilot -> piloto |
| MD-02 | MD | NO_ENCONTRADO | `En el pilot se han emitido` | `En el piloto se han emitido` | pilot -> piloto (mayuscula) |
| MD-03 | MD | CORREGIDO | `el código esta en la BD` | `el código está en la BD` | esta -> está (verbo) |
| MD-04 | MD | CORREGIDO | `no estas en grupo Estudiante` | `no estás en grupo Estudiante` | estas -> estás (verbo) |
| MD-05 | MD | CORREGIDO | `¿Si pierdo el PDF?` | `¿Y si pierdo el PDF?` | ¿Si -> ¿Y si |
| MD-06 | MD | CORREGIDO | `¿Si no estoy en grupo Estudiante?` | `¿Y si no estoy en grupo Estudiante?` | ¿Si -> ¿Y si |
| MD-07 | MD | NO_ENCONTRADO | `¿Varios certificados? Si, si hay varios ` | `¿Varios certificados? Sí, si hay varios ` | Si -> Sí (afirmativo) |
| MD-08 | MD | CORREGIDO | `Si todo es "si" y sigues sin certificado` | `Sí todo es "sí" y sigues sin certificado` | Si -> Sí (2x) |
| TPL-01 | TPL | CORREGIDO | `Guia de certificados` | `Guía de certificados` | Guia -> Guía (breadcrumb) |
| VIEW-01 | VIEW | CORREGIDO | `"Guia para obtener certificados"` | `"Guía para obtener certificados"` | Guia -> Guía (titulo) |
| VIEW-02 | VIEW | CORREGIDO | `"Guia no disponible"` | `"Guía no disponible"` | Guia -> Guía (fallback) |
| VER-01 | MD | NO_ENCONTRADO | `(v3.4.6)` | `(v3.4.7)` | coherencia con tag v3.4.7 |

---

## 2. Checks en HTML renderizado

- [x] Breadcrumb 'Guía' (con tilde)
- [x] Breadcrumb 'Guia' (sin tilde) NO
- [x] H1 'Guía para obtener'
- [x] H1 'Guia para obtener' NO
- [ ] 'piloto' (no 'pilot')
- [x] el código está en la BD
- [x] no estás en grupo Estudiante
- [x] ¿Y si pierdo el PDF?
- [x] ¿Y si no estoy en grupo?
- [ ] Sí, si hay varios tipos
- [x] Sí todo es "sí"
- [ ] v3.4.7 (no v3.4.6)

---

## 3. Veredicto

El MD ya no tiene residuales, pero el render falla. Revisar cache.
