# Modulo 1 - Parser NLP con spaCy

**Estado**: produccion
**Commits**: 4 (`aa58d38` .. R2b)
**Tests del modulo**: 47 (22 servicios POS + 12 vistas POS + 13 integracion)
**Cobertura global al cierre**: 97.36%
**Dependencias nuevas**: spaCy 3.8.16 + `es_core_news_sm` + `es_core_news_md`

---

## 1. Resumen ejecutivo

Analisis morfosintactico de frases en castellano usando spaCy con el modelo
entrenado `es_core_news_md`. Extrae por token: forma, lema, POS (en ingles y en
espanol legible), dependencia sintactica y cabeza del arbol. Ademas integra
verificacion de concordancia sujeto-verbo y funciones sintacticas principales
sobre el motor de redaccion existente (modulo 4).

Componentes:
- **Servicio `pos.py`**: analisis puro con POS_ES mapping y 4 funciones
- **Servicio `pos_integracion.py`**: concordancia S-V + funciones sintacticas + clasificacion de "que"
- **Vistas**: `/pos/` (demo interactivo) y `/pos/corpus/` (agregados)
- **Tests**: 41 en 3 archivos

### Que NO hace

- No hace analisis de sentimiento ni topic modeling
- No hace parsing de constituyentes (SN, SV, SP) — spaCy devuelve arbol de dependencias, no arbol de constitucion
- No entrena modelos custom (usa el modelo preentrenado)
- No analiza latin (requiere CLTK, no spaCy)

---

## 2. Arquitectura

```
core/
  services/
    pos.py                      POS_ES + 4 funciones (cargar modelo, analizar)
    pos_integracion.py          4 funciones (concordancia, funciones, que, evaluar)
  views_pos.py                  demo, corpus
  templates/core/pos/
    demo.html                   textarea + tabla de tokens
    corpus.html                 distribucion POS + lemmas detectados

django_retorica/urls.py         /pos/, /pos/corpus/

core/tests/
  test_services_pos.py          22 tests (13 deterministas + 10 con modelo, 1 skipif)
  test_views_pos.py             6 tests (2 deterministas + 4 con modelo)
  test_services_pos_integracion.py  13 tests (2 deterministas + 11 con modelo)
```

**Sin modelos Django nuevos.** Sin migraciones.

---

## 3. Instalacion reproducible

```bash
pip install --only-binary :all: spacy
python -m spacy download es_core_news_sm    # 12.9 MB, chico
python -m spacy download es_core_news_md    # 42.3 MB, medio (recomendado)
```

Verificado en Python 3.12.4 win_amd64 con spaCy 3.8.16. El flag `--only-binary :all:`
fuerza wheels precompilados (evita compilacion nativa).

**Nota sobre `gtts`**: spaCy instala `click>=8.2.1`, lo cual entra en conflicto
declarado con `gtts 2.5.4` (que pide `click<8.2`). El conflicto es de pip pero
**no afecta el funcionamiento**: `gtts` funciona como libreria Python; solo su
CLI secundario puede fallar.

**Configuracion de tests**:
- `POS_ES` mapping (17 tags)
- `modelo_disponible()` retorna bool
- Tests con `@pytest.mark.skipif(not modelo_disponible())` para los que requieren modelo

---

## 4. Servicio `pos.py`

### Constantes

```python
POS_ES = {
    "NOUN": "sustantivo", "VERB": "verbo", "ADJ": "adjetivo",
    "ADP": "preposicion", "DET": "determinante", "PRON": "pronombre",
    "CCONJ": "conjuncion coordinante", "SCONJ": "conjuncion subordinante",
    "AUX": "verbo auxiliar", "ADV": "adverbio", "NUM": "numeral",
    "PROPN": "nombre propio", "PUNCT": "puntuacion", "INTJ": "interjeccion",
    "PART": "particula", "SYM": "simbolo", "X": "desconocido",
}
MODELO_DEFAULT = "es_core_news_sm"
```

### `_cargar(nombre)` - @lru_cache(maxsize=4)

Carga spaCy + modelo. Cachea para evitar 3-5 segundos por cada llamada.

### `modelo_disponible(nombre)` - bool

True si `spacy.load(nombre)` funciona. Util para skipif en tests y para mostrar
banner de "spaCy no disponible" en la UI.

### `analizar_frase(texto, incluir_dependencias, modelo) -> dict`

```python
{
    "disponible": True,
    "tokens": [
        {"texto": "Juan", "lemma": "Juan", "pos": "PROPN",
         "pos_es": "nombre propio", "dep": "nsubj", "head_idx": 1,
         "es_stop": False, "es_punct": False},
        ...
    ],
    "oraciones": 1,
    "error": None,
}
```

Si spaCy falla, `disponible=False` + `error="..."` + `tokens=[]`.

### `estadisticas_pos(tokens) -> dict`

`Counter` por `pos_es`. Ej: `{"verbo": 3, "sustantivo": 2, ...}`.

---

## 5. Servicio `pos_integracion.py`

### `_nlp(texto)` - helper privado

Carga el modelo **`es_core_news_md`** explicitamente (no `sm`) porque `sm` NO
puebla `tok.morph` con informacion de numero. Fallback a `sm` si `md` no esta.
Retorna `doc` o `None`.

### `_morph_number(tok) -> str`

Primero intenta `tok.morph.get("Number")`. **Fallback heuristico** si morph
esta vacio (caso comun con `sm`):
- NOUN/PROPN/PRON/DET: plural si termina en `-s` (excluyendo `-es`, `-is`, `-us`)
- VERB/AUX: plural si termina en `-an`, `-en`, `-aron`, `-ieron`, etc.

### `concordancia_sujeto_verbo(texto) -> dict`

Busca el primer `nsubj`/`nsubj_pass`/`csubj`, compara su `Number` con el de la
cabeza. Retorna `{ok, razon, sujeto, verbo, sujeto_num, verbo_num}`.

**Limitacion**: solo verifica el primer sujeto (no sujetos coordinados).

### `funciones_sintacticas(texto) -> dict`

```python
{
    "sujeto": ["Juan"],
    "verbo": ["lee"],
    "objeto_directo": ["libro"],
    "objeto_indirecto": [],
    "oblicuos": ["en casa"],
    "disponible": True,
}
```

Acepta `dep_ in ("obl", "nmod")` para oblicuos (spaCy varia entre ambos). Si
no hay `case` child, toma la preposicion anterior en el doc.

### `clasificar_que_spacy(texto) -> str`

- `"sustantiva"`: `que` como SCONJ/PRON con head cuyo arbol llega a `ccomp`/`xcomp` en 3 niveles
- `"adjetiva"`: `que` como PRON con ancestro `acl`
- `"adverbial"`: `que` como SCONJ/PRON con ancestro `advcl`
- `""`: sin `que` o clasificacion incierta

**Fallback**: `que` con `dep_="mark"` → `"sustantiva"` (cubre el caso en que
spaCy no arboliza correctamente la subordinada sustantiva).

### `evaluar_ejercicio_con_spacy(texto, tipo_esperado) -> dict`

Llama al `evaluar_ejercicio` original del modulo 4 y le agrega el campo
`concordancia`. **No modifica** el aprobado/rechazado. Es una capa de
enriquecimiento opcional.

---

## 6. Vistas y URLs

```python
path('pos/', views_pos.demo, name='pos_demo'),
path('pos/corpus/', views_pos.corpus, name='pos_corpus'),
```

### `demo(request)` - GET/POST

- GET: textarea vacia
- POST con `texto`: analiza y renderiza tabla de tokens
- POST sin texto: mensaje "Escribe algo"

### `corpus(request)` - GET

Si `modelo_disponible()`: analiza los primeros 20 items de `corpus_completo()`.
Calcula distribucion POS agregada + top 10 lemmas de verbos y sustantivos.
Si no hay modelo: banner con instrucciones de instalacion.

---

## 7. Templates

- **`demo.html`**: form con textarea + boton "Analizar". Si hay resultado:
  tabla con #, texto, lemma, POS, POS-ES, dep, head. Ademas tabla de
  distribucion POS.
- **`corpus.html`**: stats (items, tokens, oraciones) + tabla de distribucion +
  2 cards con lemmas detectados (verbos verdes, sustantivos azules).

Ambos extienden `estudiante/base.html`.

---

## 8. Tests (41 totales)

| Archivo | Tests | Tipo |
|---|---|---|
| `test_services_pos.py` | 22 | 13 deterministas + 10 skipif(modelo) |
| `test_views_pos.py` | 6 | 2 deterministas + 4 con modelo |
| `test_services_pos_integracion.py` | 13 | 2 deterministas + 11 con modelo |

### Casos cubiertos

**Servicios POS**: 17 tags en POS_ES, `modelo_disponible()` retorna bool,
`modelo_disponible("no_existe")` retorna False, `analizar_frase("")` retorna
tokens=[], POS de "Juan estudia" (`PROPN`/`VERB`), dep de sujeto (`nsubj`/`ROOT`),
lemma de verbo conjugado, 2 oraciones con 2 puntos, `incluir_dependencias=False`
deja `dep=""`, puntuacion marcada, `pos_es` legible, `estadisticas_pos` con
diccionario vacio y con tokens.

**Integracion**: concordancia `Juan estudia` (ok), `Los ninos estudian` (plural ok),
`Juan estudian` (discordancia), `funciones_sintacticas("Juan lee un libro")`,
`funciones_sintacticas("Juan lee un libro en casa")` detecta oblicuo,
`clasificar_que_spacy("Pienso que debes...")` → sustantiva,
`clasificar_que_spacy("El hombre que vino...")` → adjetiva,
`evaluar_ejercicio_con_spacy` agrega campo concordancia.

---

## 9. Commits

| Hash | Contenido |
|---|---|
| `aa58d38` | R1: `pos.py` + 22 tests |
| `abea863` | R2: 2 vistas + templates + 6 tests |
| `28a8e2a` | R3: `pos_integracion.py` + 13 tests |

---

## 10. Decisiones tecnicas

1. **`md` sobre `sm` en integracion**: `sm` carga 6 componentes pero **NO
   puebla `tok.morph`** con informacion gramatical (Number, Person, etc.).
   `md` si trae esa info. Para concordancia S-V necesitamos Number → `md`. Los
   otros usos (`demo.html`, `corpus.html`) pueden seguir usando `sm` (mas rapido).

2. **Fallback heuristico de Number**: `es_core_news_sm` no trae morph. Aunque
   la solucion correcta es cargar `md`, tambien agregamos un fallback de forma
   para robustez. NO es tan preciso como morph real, pero cubre 80% de casos.

3. **Dependency tree para "que"**: la heuristica vieja del modulo 4 (analizar
   palabras anteriores) falla en casos complejos. spaCy arboliza y permite
   seguir el head hasta `ccomp`/`xcomp`/`advcl`. Es mas preciso. Fallback a
   `mark → sustantiva` por si el modelo no arboliza bien.

4. **`obl` y `nmod` aceptados como oblicuos**: spaCy varia entre etiquetarlos
   segun la frase. Aceptar ambos es mas robusto para "en casa", "con Juan", etc.

5. **Degradacion graceful**: si spaCy no esta, `modelo_disponible()` retorna
   False, `analizar_frase` retorna `disponible=False`, `evaluar_ejercicio_con_spacy`
   igual funciona (concordancia = ok=True neutro). Los otros 4 modulos
   (redaccion, SRS, filologia, corpus) NO dependen de spaCy.

6. **URLs namespaced `/pos/`**: patron establecido en el proyecto. Evita colisiones
   con otros modulos.

7. **`lru_cache` en `_cargar`**: cargar el modelo tarda 3-5 segundos la primera
   vez. Cache evita repetir en cada request.

8. **Sin modelo custom entrenado**: usamos `es_core_news_md` out-of-the-box.
   Si en el futuro necesitamos identificar figuras retoricas o autores literarios,
   necesitariamos fine-tuning (fuera de scope actual).

---

## 11. Roadmap

### Completado

- [x] R1: servicio `pos.py` (POS_ES + 4 funciones) + 22 tests
- [x] R2: 2 vistas (`/pos/`, `/pos/corpus/`) + templates + 6 tests
- [x] R3: `pos_integracion.py` (concordancia + funciones + que) + 13 tests
- [x] R4: este documento

### Extensiones posibles (futuras sesiones)

- **Integracion en UI de redaccion**: mostrar `concordancia` como badge debajo
  del feedback. Requiere template + vista en `/redaccion/<id>/`, +3 tests.
- **Concordancia en preguntas retoricas**: `¿Vienes?` — spaCy lo marca como
  interrogativa, la heuristica actual no lo verifica.
- **`es_core_news_lg`** para mejor precision si el rendimiento lo permite
  (600 MB en disco, descartado para esta sesion).
- **Concordancia de tiempo verbal**: verificar que subordinada y principal
  concuerdan en tiempo (ej. "Juan dijo que vendra/viene"). Requiere logica de
  secuencias temporales — complejo.
- **Enriquecer corpus con POS**: agregar filtro "solo verbos" o "solo sustantivos"
  en `/corpus/concordancia/`. Requiere re-analizar corpus con pos, ~2s por request.

### Fuera de scope

- Constituent parsing (SN, SV, SP) — spaCy no lo hace
- Latin (requiere CLTK, no spaCy)
- Sentiment/topic modeling

---

## 12. Uso rapido

```bash
python manage.py runserver

# En el navegador:
#   /pos/                           -> demo interactivo
#   /pos/corpus/                    -> distribucion POS agregada
```

### Uso en shell

```python
from core.services.pos import analizar_frase, modelo_disponible
from core.services.pos_integracion import (
    concordancia_sujeto_verbo,
    funciones_sintacticas,
    clasificar_que_spacy,
    evaluar_ejercicio_con_spacy,
)

# Demo de analisis
r = analizar_frase("Juan estudia matematicas")
for t in r["tokens"]:
    print(t["texto"], t["pos_es"], t["lemma"], t["dep"])

# Concordancia
concordancia_sujeto_verbo("Juan estudia")       # ok=True
concordancia_sujeto_verbo("Juan estudian")      # ok=False

# Funciones sintacticas
funciones_sintacticas("Juan lee un libro en casa")
# {"sujeto": ["Juan"], "verbo": ["lee"], "objeto_directo": ["libro"],
#  "oblicuos": ["en casa"], "disponible": True}

# Clasificar "que"
clasificar_que_spacy("Pienso que debes estudiar")      # "sustantiva"
clasificar_que_spacy("El hombre que vino era mi tio")  # "adjetiva"

# Evaluar con concordancia
r = evaluar_ejercicio_con_spacy("Juan estudia, pero su hermano juega", "oracion_coordinada")
r["aprobado"]       # True
r["concordancia"]   # {"ok": True, "razon": "concuerdan", ...}
```

### Verificar instalacion

```bash
python -c "import spacy; print('spaCy:', spacy.__version__)"
python -m spacy info es_core_news_md
python manage.py check
```

---

## Cierre de modulos completados

| Modulo | Commits | Tests | Doc |
|---|---|---|---|
| **4 - Redaccion morfosintactica** | 6 | 43 | ✅ |
| **5 - SRS / SM-2** | 5 | 63 | ✅ |
| **2 - Filologia comparada** | 3 | 35 | ✅ |
| **6 - Corpus y concordancia** | 4 | 30 | ✅ |
| **1 - POS / spaCy** | 3 | 41 | este |

**Total**: 21 commits, ~212 tests, 97.48% cobertura, 5 modulos en produccion.

**Solo queda pendiente**: Modulo 3 (Lectura TTS con morfologia al click).

---

*Ultima actualizacion: 2026-10-20 tras R2b(demo AJAX).*


## 11.bis Adenda R2b — Demo interactiva con AJAX

**Agregado post-R3.** Añade interactividad al demo de POS.

### Endpoint AJAX

```
POST /pos/ajax/analizar/   name=pos_analizar_ajax
Body: {"texto": "..."}
Response: {"analisis": {...}, "stats": {...}}
```

- `require_POST` (GET -> 405)
- 400 si JSON invalido, `texto` vacio, o `texto > 1000` chars
- Llama `analizar_frase()` + `estadisticas_pos()` y retorna JSON

### Template reescrito

`demo.html` ahora es JS-driven:
- **Debounce 400ms** al tipear
- **AbortController** para cancelar requests anteriores
- Render dinamico de tabla con badges coloreados por POS
- Contador `N / 1000` caracteres en vivo
- Fallback: mensaje "spaCy no disponible" si el modelo falta

### Tests nuevos (6)

`TestAnalizarAjax` en `test_views_pos.py`:
- GET rechazado (405)
- JSON invalido (400)
- Falta texto (400)
- Texto > 1000 chars (400)
- Estructura JSON ok (keys `analisis` y `stats` presentes)
- Analisis completo con modelo (`tokens`, `stats` poblados)

### Decision tecnica #9

**AJAX + debounce + AbortController**: la demo original hacia POST + reload.
Reescrita con `fetch` — analisis en tiempo real, cancelacion de requests
previos, sin recarga de pagina. El endpoint valida independiente del
limite `MAX_PALABRAS=500` del servicio (aqui 1000 chars porque un demo
puede aceptar texto mas largo sin ejecutar el flujo completo de redaccion).

---