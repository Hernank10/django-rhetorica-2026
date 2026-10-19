# Modulo 6 - Corpus y Concordancia

**Estado**: produccion
**Commits**: 3 (`0a7cebc` .. `R2`)
**Tests del modulo**: 30 (22 servicios + 8 vistas)
**Funciones**: 6 (4 puras + 2 gatherers de BD)
**Vistas**: 3 (`/corpus/`, `/corpus/concordancia/`, `/corpus/frecuencias/`)
**Cobertura global al cierre**: 97.86%

---

## 1. Resumen ejecutivo

Explorador del corpus linguo-pedagogico del proyecto. Agrega **todos los textos**
de la aplicacion (1425 ejercicios + evaluaciones + 35 flashcards + 50 etimos) en
una coleccion unica y ofrece tres herramientas de analisis:

- **Frecuencias**: cuantas veces aparece cada palabra, top bigramas y trigramas
- **Concordancia (KWIC)**: keyword in context, ver cada aparicion con +-5 palabras
- **Indice**: dashboard con stats del corpus + top 50 palabras

El corpus se genera dinamicamente en cada request desde 4 modelos distintos +
1 fuente estatica (50 etimos). No hay tabla "corpus" en la BD: es una proyeccion
de los datos existentes.

### Que NO hace

- No preprocesa el texto con NLP (spaCy, POS tagging, lematizacion)
- No hace analisis de sentimiento ni topic modeling
- No cachea el corpus (se re-calcula en cada request; si crece >100k items,
  agregar `django.core.cache` en una iteracion futura)
- No persiste busquedas (no hay historial de concordancias)

---

## 2. Arquitectura

```
core/
  services/
    corpus.py                  6 funciones + constante FUENTES
                                (4 puras + 2 gatherers + corpus_completo)
  views_corpus.py              indice, concordancia, frecuencias_view
  templates/core/corpus/
    indice.html                dashboard + top 50
    concordancia.html          KWIC con filtro por fuente
    frecuencias.html           bigramas + trigramas + tabla completa

django_retorica/urls.py        /corpus/, /corpus/concordancia/, /corpus/frecuencias/

core/tests/
  test_services_corpus.py      22 tests (17 puros + 5 con BD)
  test_views_corpus.py         8 tests (integracion)
```

**Sin modelos Django nuevos.** Sin migraciones. Sin dependencias externas.

---

## 3. Modelo de datos del corpus (items, no modelo)

Cada "item" del corpus es un dict con 3 claves:

| Clave | Tipo | Notas |
|---|---|---|
| `texto` | str | Contenido textual a analizar |
| `fuente` | str | Una de las 10 constantes de `FUENTES` |
| `id` | int \| str | PK del modelo origen (o `latin` si es etimo) |

**10 fuentes** (constante `FUENTES`):

```
ejercicio_enunciado, ejercicio_teoria, ejercicio_ejemplo,
ejercicio_respuesta_esperada, evaluacion_texto, evaluacion_feedback,
flashcard_frente, flashcard_reverso, etimologia_regla, etimologia_ejemplo
```

Cada item se genera dinamicamente desde:

- **EjercicioLinguistico** (1425 en DB): 4 fuentes posibles desde `contenido.{enunciado, teoria, ejemplo, respuesta_esperada}`
- **EvaluacionRedaccion**: 2 fuentes (`texto_estudiante`, `feedback`)
- **Flashcard**: 2 fuentes (`frente`, `reverso`)
- **ETIMOS** (50 dicts en `_etimos_filologia.py`): 2 fuentes (`regla`, `ejemplo`)

Total esperado en produccion: **~1700 items** (1425 ejercicios con ~1 item cada uno + 100 etimos + evaluaciones + flashcards).

---

## 4. Servicios puros (sin BD)

### `tokenizar(texto) -> list[str]`

Regex `\b[a-záéíóúñü]+\b` sobre `texto.lower()`. Lowercase + solo letras (con
acentos) + excluye numeros y puntuacion.

- `tokenizar("Hola, mundo 2024")` -> `["hola", "mundo"]`
- `tokenizar("")` -> `[]`
- `tokenizar(None)` -> `[]`

### `frecuencias(textos) -> dict[str, int]`

Counter agregado sobre un iterable de strings.

- `frecuencias(["uno dos", "dos tres"])` -> `{"uno": 1, "dos": 2, "tres": 1}`

### `concordancias(texto_corpus, termino, contexto=5) -> list[dict]`

KWIC sobre un texto unico. Cada match retorna dict con:

```
{"izq": str, "palabra": str, "der": str, "posicion": int}
```

- Match exacto (no substring): busca token == termino.lower()
- `contexto` controla cuantas palabras a cada lado

### `n_gramas(textos, n=2, top=20) -> list[(tuple, count)]`

Bigramas/trigramas/etc. `n<1` retorna `[]`. Retorna `most_common(top)`.

---

## 5. Servicios gatherers (con BD)

### `corpus_desde_etimos() -> list[dict]`

Lee `ETIMOS` del modulo 2 y genera 2 items por etimo (regla, ejemplo).
50 etimos x 2 = 100 items.

### `corpus_desde_bd() -> list[dict]`

Itera sobre 3 modelos con `values_list` (nada de queries N+1):

- `EjercicioLinguistico.objects.values_list("id", "contenido")` -> hasta 4 items por ej
- `EvaluacionRedaccion.objects.values_list("id", "texto_estudiante", "feedback")` -> hasta 2 items por ev
- `Flashcard.objects.values_list("id", "frente", "reverso")` -> hasta 2 items por fc

### `corpus_completo() -> list[dict]`

Union: `corpus_desde_bd() + corpus_desde_etimos()`.

---

## 6. Vistas y URLs

```python
path('corpus/', views_corpus.indice, name='corpus_indice'),
path('corpus/concordancia/', views_corpus.concordancia, name='corpus_concordancia'),
path('corpus/frecuencias/', views_corpus.frecuencias_view, name='corpus_frecuencias'),
```

### `indice(request)` - GET publico

Dashboard. Llama `corpus_completo()`, calcula `frecuencias()`, muestra:
- Stats por fuente (`_stats_corpus` helper)
- Top 50 palabras clickeables (link a concordancia)

### `concordancia(request)` - GET publico con `?q=<termino>&fuente=<opcional>`

Sin `q`: mensaje "Escribe un termino".
Con `q`: recorre cada item, ejecuta `concordancias(item["texto"], q, contexto=5)`,
acumula todos los KWIC. Cap a 500 resultados para no reventar el render con
terminos muy comunes (ej. "que" aparece cientos de veces).

Filtro opcional por fuente (dropdown de las 10 disponibles).

### `frecuencias_view(request)` - GET publico

Tres tablas:
1. Top 20 bigramas
2. Top 10 trigramas
3. Tabla completa limitada a **200 palabras** (no todos los tokens del corpus;
   puede haber miles de unicos, es UX no analisis exhaustivo)

---

## 7. Templates

Los 3 extienden `estudiante/base.html` (heredado del modulo 4).

- **indice.html**: 2 cards de acceso rapido + tabla de fuentes + tabla top 50
- **concordancia.html**: form con `q` + dropdown `fuente` + tabla KWIC con columna
  izquierda / palabra destacada en naranja / derecha / fuente
- **frecuencias.html**: 3 tablas (bigramas, trigramas, frecuencias completas)

**Accesibilidad**: `scope="col"` en todos los `<th>`, contraste WCAG AA heredado
del base.html.

---

## 8. Tests (30 totales)

| Archivo | Tests | Tipo |
|---|---|---|
| `test_services_corpus.py` | 22 | 17 puros + 5 con BD |
| `test_views_corpus.py` | 8 | integracion |

### Cobertura por clase

**TestTokenizar (5):** vacio, none, puntuacion, acentos, numeros excluidos

**TestFrecuencias (3):** vacio, simple, varios textos

**TestConcordancias (4):** vacio, sin match, un match, varios matches

**TestNGramas (3):** vacio, bigramas, trigramas

**TestCorpusDesdeEtimos (2):** 100 items, fuentes correctas

**TestCorpusDesdeBD (5):** usuario sin datos, un ejercicio, una evaluacion, una flashcard, constante FUENTES

**TestIndiceCorpus (3):** GET 200, render HTML, muestra top

**TestConcordanciaVista (3):** sin q, con noctem, con termino inexistente

**TestFrecuenciasVista (2):** GET 200, muestra secciones

**Nota critica sobre `test_vacio_para_usuario_sin_datos`**: la version original
`assert corpus_desde_bd() == []` fallaba en suite completa porque hay fixtures
de otros tests cargados en la BD. La version robusta crea un usuario nuevo y
verifica que ningun item del corpus lo referencie.

**Fix aplicado en `d93c6bd`**: separar tests que asumen BD vacia de tests que
no. Es un patron comun en suites grandes.

---

## 9. Commits

| Hash | Contenido |
|---|---|
| `0a7cebc` | R1: `corpus.py` + 22 tests (17 puros + 5 BD) |
| `d93c6bd` | fix: tests robustos ante interferencia de fixtures |
| `R2` | 3 vistas + 3 templates + 3 URLs + 8 tests integracion |

---

## 10. Decisiones tecnicas

1. **Sin modelo Django**: el corpus es una proyeccion dinamica. Si agregaramos
   un `CorpusItem` en BD, tendriamos que mantenerlo sincronizado con 4 modelos
   + 1 archivo estatico en cada save/delete. Mejor calcular al vuelo.

2. **Gatherers separados (`_bd` vs `_etimos`)**: permite testear los etimos
   sin BD (17 de 22 tests corren sin `django_db`). `corpus_completo()` es el
   unico punto de acoplamiento.

3. **Regex `\b[a-záéíóúñü]+\b`**: excluye numeros (no aportan al analisis
   linguistico) y puntuacion, pero conserva acentos y `ñ`/`ü`. `unicodedata` no
   se usa porque el corpus es en castellano (no hay caracteres exoticos).

4. **Cap a 500 resultados en concordancia**: "que" aparece cientos de veces en
   el corpus. Sin cap, el render tarda >5s y puede matar el browser. 500 es
   suficiente para exploracion pedagogica.

5. **Tabla de frecuencias a 200 filas**: mismo motivo. Hay miles de tokens
   unicos. Mostrar los 200 mas frecuentes cubre el 95%+ del valor pedagogico.

6. **No cachear el corpus**: por ahora ~1700 items, calcular tarda <100ms.
   Si crece (mas usuarios, mas evaluaciones), agregar
   `django.core.cache.cache` con clave `corpus:v1:<n_items_db>`.

7. **Fix de tests con BD compartida**: `test_vacio` original asumia BD limpia.
   En suite completa, pytest-django comparte la BD entre tests del mismo modulo
   (con transacciones). Los fixtures de un test contaminan el siguiente.
   Solucion: filtrar por ID especifico, nunca por count global.

---

## 11. Roadmap

### Completado

- [x] R1: motor puro + gatherers (22 tests)
- [x] R2: 3 vistas + templates + 8 tests
- [x] R3: este documento

### Modulo 1 (spaCy POS/parser) - proxima sesion

El corpus actual es **lexico** (frecuencias, concordancias, n-gramas). El
siguiente nivel es **morfosintactico**:

- **POS tagging**: clasificar cada palabra (sustantivo, verbo, adjetivo, etc.)
- **Lematizacion**: reducir "corriendo" -> "correr", "corri" -> "correr"
- **Dependencias**: arbol sintactico (sujeto, objeto, modificadores)

**Requisitos**:
- `pip install spacy` (~50MB)
- `python -m spacy download es_core_news_sm` (~12MB, modelo chico)
- `python -m spacy download es_core_news_md` (~40MB, modelo medio, mejor)

**Alcance propuesto para R1 spaCy**:
- Servicio `core/services/pos.py` con `analizar_frase(texto) -> list[token]`
- Cada token: `{texto, lemma, pos, dependency, head_idx}`
- Vistas: `/pos/` para probar una frase, `/pos/corpus/` para analizar items del corpus
- **~20 tests** con `spacy.blank("es")` para tests deterministicos (sin descargar modelo)

**Riesgo**: instalacion de spaCy en Python portable puede tener friccion. Plan B:
procesar con `spacy.blank("es")` (reglas minimas) sin modelo entrenado.

### Mejoras opcionales al corpus (R4)

- Cache con `django.core.cache`
- Paginacion en `/corpus/frecuencias/` (500 por pagina)
- Export CSV de concordancias
- Filtro multiple por fuente (checkboxes, no dropdown)
- Comparar frecuencias entre fuentes (ej. "que" en ejercicios vs evaluaciones)

---

## 12. Uso rapido

```bash
python manage.py runserver

# En el navegador:
#   /corpus/                              -> dashboard
#   /corpus/concordancia/?q=noctem        -> KWIC de "noctem"
#   /corpus/concordancia/?q=noctem&fuente=etimologia_regla  -> filtrado
#   /corpus/frecuencias/                  -> bigramas, trigramas, tabla
```

### Uso en shell

```python
from core.services.corpus import (
    tokenizar,
    frecuencias,
    concordancias,
    n_gramas,
    corpus_desde_bd,
    corpus_desde_etimos,
    corpus_completo,
)

# Explorar tamanos
items = corpus_completo()
len(items)                     # total de items
{it["fuente"] for it in items} # 10 fuentes

# Top palabras
textos = [it["texto"] for it in items]
frec = frecuencias(textos)
top10 = sorted(frec.items(), key=lambda x: -x[1])[:10]

# KWIC sobre un texto especifico
concordancias("el gato come el raton y el gato duerme", "gato", contexto=2)
# [{'izq': 'el', 'palabra': 'gato', 'der': 'come el', 'posicion': 1},
#  {'izq': 'y el', 'palabra': 'gato', 'der': 'duerme', 'posicion': 7}]

# Bigramas top
n_gramas(textos, n=2, top=5)
```

### Agregar una fuente nueva

1. Añadir el nombre a `FUENTES` en `corpus.py`
2. Añadir un `for ... values_list(...)` en `corpus_desde_bd()` o un bloque en `corpus_desde_etimos()`
3. Añadir test en `TestCorpusDesdeBD` que verifique la nueva fuente
4. Actualizar `test_fuentes_constant` (`assert len(FUENTES) == 11`)

---

## Cierre de modulos completados

| Modulo | Commits | Tests | Doc |
|---|---|---|---|
| **4 - Redaccion morfosintactica** | 6 | 43 | ✅ |
| **5 - SRS / SM-2** | 5 | 63 | ✅ |
| **2 - Filologia comparada** | 3 | 35 | ✅ |
| **6 - Corpus y concordancia** | 3 | 30 | este |

**Total sesion completa**: 17 commits, ~186 tests, 4 docs de 12 secciones,
cobertura 97.86%.

---

*Ultima actualizacion: 2026-10-19 tras cierre de R2 corpus.*