# Motor de Adaptabilidad Lingüística — Diseño

## Objetivo

Transformar el historial de respuestas del estudiante en un disparador
algorítmico que inyecte micro-ejercicios correctivos en su dashboard cuando
detecte patrones de error recurrentes.

Sin ML. Sin API externa. Todo determinístico y testeable.

---

## 1. Taxonomía de errores

### 1.1 Estructura

Cada error se clasifica con una **tupla de 3**:

- `idioma`: `ES` | `EN` | `LA`
- `categoria_gramatical`: string libre (ver 1.2)
- `patron_error`: string libre opcional, más específico (ej: `militis->milite`)

### 1.2 Categorías latinas iniciales (5)

| Slug | Descripción | Tipo |
|---|---|---|
| `declinacion_3_consonantica` | Tema consonántico (`miles, militis`), desinencias -is/-i/-em/-e | Morfológico |
| `ablativo_instrumental` | Ablativo sin preposición como instrumento/medio | Sintáctico |
| `ablativo_locativo` | Lugar en donde: sin prep (`Roma`) vs con prep (`in Roma`) | Sintáctico |
| `genitivo_partitivo` | Dependiente de sustantivos/adjetivos de cantidad | Sintáctico |
| `cum_subjuntivo_imperfecto` | `cum` histórico + imperfecto de subjuntivo | Verbal |

**Extensible:** para agregar una categoría solo hay que añadirla a
`CATEGORIAS_LATIN` en `core/services/adaptive.py`. No requiere migración
porque el campo `categoria_gramatical` es `CharField` sin `choices`.

### 1.3 Categorías para otros idiomas (futuras, fuera del MVP)

- **ES:** `subjuntivo_presente`, `subjuntivo_preterito`, `ser_estar`,
  `por_para`, `concordancia_genero`
- **EN:** `present_perfect_vs_past_simple`, `modal_verbs`,
  `phrasal_verbs`, `articles`, `relative_clauses`

---

## 2. Umbrales y ventana temporal

Configurables vía `django_retorica/settings.py`:

```python
# Motor adaptativo
ADAPTIVE_ERROR_WINDOW_DAYS = 7
ADAPTIVE_ERROR_THRESHOLD = 3       # errores para disparar cápsula
ADAPTIVE_MASTERY_THRESHOLD = 3     # aciertos consecutivos para marcar resuelto


---

## 3.1 Validacion formal

El contrato esta codificado en:

- `core/schemas/microejercicio.schema.json` — JSON Schema Draft 7
- `core/schemas/validators.py` — validador con fallback sin dependencias

Uso:

```python
from core.schemas.validators import validar_microejercicio, es_valido

errores = validar_microejercicio(contenido)  # [] si valido
if errores:
    raise ValueError(errores)





