# Estado actual — django-rhetorica-2026

Snapshot tras `v1.8.14` (2026-10-28). Verificar con `/debug/db/?token=...` (sin prefijo `/en/`).

## Modelos en producción

| Modelo | Filas |
|---|---|
| TecnicaGramatical | 400 |
| TecnicaSintactica | 100 |
| TecnicaLinguistica | 10 |
| EjercicioGramatical | 400 |
| EjercicioTecnica | 100 |
| EjercicioLinguistico | 1628 |
| Recurso | 564 |
| ContenidoJSON | 19 |
| Curso | 27 |
| Modulo | 93 |
| Leccion | 324 |
| EvaluacionCurso | 63 |
| PreguntaEvaluacion | 285 |
| Certificacion | 49 |
| CertificacionObtenida | 45 |
| Flashcard | 192 |
| Review | 194 |
| ProgresoTecnica | 3696 |
| ProgresoGramatical | 15046 |
| User | 110 |

## Tests (verificado 2026-10-28)

- **1279 passed, 1 skipped**
- **Cobertura: 94%**
- Líneas: 11637 total, 701 sin cubrir
- Tiempo: 358s (~6 min)

## Usuarios

| Grupo | Cantidad | Password |
|---|---|---|
| `testadmin1..3` | 3 | `Test1234!` |
| `testprofe01..09` | 9 | `Test1234!` |
| `testest001..096` | 96 | `Test1234!` |
| `admin` | 1 | (creado por `create_superuser`) |

## Rutas de debug

- `/debug/db/?token=...`
- `/debug/reload/?token=...`
- **Sin** prefijo `/en/`

## Pendiente

| Item | Prioridad |
|---|---|
| Bloque C de B1 (341-350) | media |
| Bug card Total: 0 en sintaxis | baja |
| Bug card Gramática con descripción de Sintaxis | baja |
| Cloudflare R2 para media | baja |

