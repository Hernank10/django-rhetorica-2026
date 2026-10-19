# Modulo 3 - Lectura Asistida con TTS

**Estado**: produccion
**Commits**: 2 (`R1` + `R2` — ver §9)
**Tests del modulo**: 30 (19 servicios + 11 vistas)
**Vistas**: 2 (`/lectura/`, `/lectura/<id>/`) + 1 AJAX
**Cobertura global al cierre**: 97.35%

---

## 1. Resumen ejecutivo

Lector interactivo de textos con click-por-palabra. Al hacer click en cualquier
palabra del texto se muestra su morfologia (lema, POS en espanol, dependencia
sintactica, oracion contenedora) y un boton para escuchar como se pronuncia.
Tambien hay un boton "Leer todo el texto" que sintetiza el texto completo.

Componentes:
- **Servicio `lectura.py`**: 3 funciones puras (segmentar, morfologia, estadisticas)
- **Vista `selector`**: lista de textos disponibles (ejercicios con `ejemplo` de 80+ chars)
- **Vista `lector`**: texto interactivo con palabras clickeables
- **Endpoint AJAX `morfologia_ajax`**: recibe `{texto, offset}`, retorna morfologia JSON
- **TTS**: reutiliza `/tts/?text=...&lang=es` ya existente

### Que NO hace

- No traduce el texto
- No hace resumen automatico
- No guarda progreso de lectura (podria ser R4)
- No marca palabras conocidas vs desconocidas (podria ser R4)

---

## 2. Arquitectura

```
core/
  services/
    lectura.py                  3 funciones puras
  views_lectura.py              selector, lector, morfologia_ajax
  templates/core/lectura/
    selector.html               lista de textos disponibles
    lector.html                 texto interactivo + panel lateral + JS

django_retorica/urls.py         /lectura/, /lectura/<id>/, /lectura/ajax/morfologia/

core/tests/
  test_services_lectura.py      19 tests (13 deterministas + 6 con modelo)
  test_views_lectura.py         11 tests
```

**Sin modelos Django nuevos.** **Sin dependencias nuevas.** Reutiliza spaCy + TTS.

---

## 3. Fuente de textos

Los textos vienen de `EjercicioLinguistico` filtrado por:
- `es_redaccion=True`
- `contenido.ejemplo` con `len >= 80` (textos cortos no valen la pena)
- Resultado esperado: ~100 textos de los 100 tecnicas de redaccion

Si el texto no tiene `ejemplo`, la vista `lector` cae al `enunciado`.

**Filtrado en `views_lectura._textos_disponibles()`**:
```python
qs = EjercicioLinguistico.objects.filter(es_redaccion=True)
for ej in qs:
    ejemplo = (ej.contenido or {}).get("ejemplo", "").strip()
    if len(ejemplo) >= 80:
        textos.append({...})
```

---

## 4. Servicio `lectura.py`

### `segmentar_texto(texto) -> list[dict]`

Divide el texto en segmentos tipados:

```python
[
    {"tipo": "palabra",    "texto": "Primero", "inicio": 0,  "fin": 7},
    {"tipo": "puntuacion", "texto": ",",       "inicio": 7,  "fin": 8},
    {"tipo": "espacio",    "texto": " ",       "inicio": 8,  "fin": 9},
    {"tipo": "palabra",    "texto": "me",      "inicio": 9,  "fin": 11},
    ...
]
```

**Reconstruccion**: `"".join(s["texto"] for s in segmentos) == texto` siempre.

Tipos: `palabra` | `espacio` | `puntuacion` | `otro`.

**Uso**: el template `lector.html` envuelve cada segmento `palabra` en un `<span class="palabra" data-offset="N">`. El JS del navegador lee `data-offset` y hace POST a `/lectura/ajax/morfologia/`.

### `morfologia_contextual(texto, offset) -> dict`

Dada una posicion (char index), devuelve morfologia del token que la contiene:

```python
{
    "disponible": True,
    "palabra": "Juan",
    "lemma": "Juan",
    "pos": "PROPN",
    "pos_es": "nombre propio",
    "dep": "nsubj",
    "head": "estudia",
    "oracion": "Juan estudia",
}
```

- Si no hay modelo: `disponible=False` + campos vacios
- Si offset cae en espacio/puntuacion: `disponible=False` (el JS no envia esos clicks)

### `estadisticas_texto(texto) -> dict`

```python
{
    "n_palabras": 156,
    "n_oraciones": 4,
    "longitud_media_palabra": 4.7,
    "distribucion_pos": {"verbo": 12, "sustantivo": 34, ...},
    "disponible": True,
}
```

Sin modelo: solo cuenta palabras/oraciones con regex. Con modelo: usa spaCy.

---

## 5. Vistas y URLs

```python
path('lectura/', views_lectura.selector, name='lectura_selector'),
path('lectura/ajax/morfologia/', views_lectura.morfologia_ajax, name='lectura_morfologia_ajax'),
path('lectura/<int:texto_id>/', views_lectura.lector, name='lectura_lector'),
```

### `selector(request)` - GET publico

Lista los textos disponibles (100+ ejercicios). Cada fila: `#`, titulo, tipo, longitud, boton "Leer".

### `lector(request, texto_id)` - GET publico

- 404 si el ejercicio no existe o no es de redaccion
- Segmenta el texto en `segmentar_texto()`
- Calcula `estadisticas_texto()` para mostrar `n_palabras`, `n_oraciones`, `longitud_media`
- Renderiza tabla interactiva

### `morfologia_ajax(request)` - POST AJAX

Recibe JSON `{texto: str, offset: int}`:
- Valida JSON, `texto`, `offset`, `offset < len(texto)`
- Llama `morfologia_contextual(texto, offset)`
- Retorna JSON con la morfologia

Errores 400 si:
- JSON invalido
- Falta `texto`
- Falta `offset`
- `offset` no numerico
- `offset` fuera de rango

Metodo GET rechazado por `@require_POST` → 405.

---

## 6. Template `lector.html` — el JS

### Estructura HTML

```html
<div class="lectura-texto" data-texto="{{ texto }}">
    <span class="palabra" data-offset="0">Primero</span>, me desperté...
</div>
<div class="panel-morfologia" id="panel">...</div>
```

### JS — click por palabra

```javascript
textoDiv.addEventListener("click", (e) => {
    const span = e.target.closest(".palabra");
    if (!span) return;
    // highlight visual
    if (palabraActiva) palabraActiva.classList.remove("activa");
    span.classList.add("activa");
    palabraActiva = span;
    // fetch morfologia
    const offset = parseInt(span.dataset.offset, 10);
    pedirMorfologia(offset);
});
```

`pedirMorfologia` hace `fetch("/lectura/ajax/morfologia/", {method: "POST", body: JSON.stringify({texto, offset})})`.
Respuesta se renderiza en el panel con boton "🔊 Escuchar palabra".

### JS — audio

```javascript
function reproducir(txt) {
    const url = `/tts/?text=${encodeURIComponent(txt)}&lang=es`;
    const audio = new Audio(url);
    audio.play();
}
```

No hay proxy: el navegador hace `GET /tts/` directamente al servidor Django. Aprovecha el cache de 30 dias del servidor.

### JS — boton "Leer todo"

```javascript
btnTodo.addEventListener("click", () => {
    btnTodo.disabled = true;
    const url = `/tts/?text=${encodeURIComponent(textoCompleto)}&lang=es`;
    const audio = new Audio(url);
    audio.addEventListener("ended", () => { btnTodo.disabled = false; });
    audio.play();
});
```

Disabled durante la reproduccion para evitar doble click.

---

## 7. TTS — API reutilizada

El TTS es **pre-existente**. `core/views_tts.py` expone:

```
GET /tts/?text=<texto>&lang=es|en|la
```

- Devuelve `audio/mpeg` (FileResponse)
- Cache en disco de 30 dias
- Max texto: `tts.MAX_TEXTO` chars
- 400 si falta `text` o excede maximo
- 503 si `gtts` fallo (sin conexion, no instalado)

**El modulo de lectura NO toca `views_tts.py`.** Solo el JS del navegador llama a esa URL.

---

## 8. Tests (30 totales)

| Archivo | Tests | Tipo |
|---|---|---|
| `test_services_lectura.py` | 19 | 13 deterministas + 6 con modelo |
| `test_views_lectura.py` | 11 | integracion (BD + AJAX) |

### Casos cubiertos

**Servicios**:
- `segmentar_texto`: vacio, none, una palabra, dos palabras, puntuacion, reconstruccion byte-a-byte, offsets, acentos
- `morfologia_contextual`: vacio, none, offset negativo, juan en 0, estudia en 5, offset en espacio
- `estadisticas_texto`: vacio, none, simple, dos oraciones, texto real de ejercicio (155 chars)

**Vistas**:
- Selector: GET 200, muestra texto creado con `ejemplo` >= 80 chars
- Lector: GET 200, 404 si no existe, 404 si no es redaccion, contiene `<span data-offset>`
- AJAX: GET rechazado (405), JSON invalido (400), falta texto (400), falta offset (400), offset fuera de rango (400), OK con morfologia

---

## 9. Commits

| Hash | Contenido |
|---|---|
| `R1` | `lectura.py` (3 funciones) + 19 tests |
| `R2` | `views_lectura.py` + 2 templates + 1 AJAX + 11 tests |

---

## 10. Decisiones tecnicas

1. **Click por palabra sin proxy AJAX para audio**: el navegador llama directo a `/tts/?text=...` en vez de pasar por un endpoint propio. Ahorra ~50 lineas de codigo y aprovecha el cache de 30 dias. Desventaja: el texto va en URL query string (visible en network tab). Aceptable pedagogicamente.

2. **Sin modelo `Texto` dedicado**: uso `EjercicioLinguistico` filtrado. Si en el futuro se quiere subir textos custom (no atados a ejercicios), se crea `TextoLectura` con campo `contenido`.

3. **Umbral 80 chars en selector**: `contenido.ejemplo` de los 100 tecnicas tiene 100-250 chars. Textos cortos (<80) no dan buena experiencia de lectura. Si hay pocos textos, bajar a 40-50.

4. **Sin guardar progreso**: el modulo no persiste "que palabras ya viste". Podria agregarse con un modelo `LecturaRealizada(estudiante, ejercicio, palabras_clickeadas)` pero es scope R4.

5. **JS vanilla, sin frameworks**: el lector usa `addEventListener`, `fetch`, `Audio` nativos. Cero dependencias JS. ~80 lineas.

6. **Modelo `md` sobre `sm`**: igual que en modulo POS. `sm` no trae morph, y `morfologia_contextual` no necesita morph (solo POS + lemma + dep). Pero `md` da mejor `dep_`, mas util pedagogicamente. **Fallback a `sm`** si `md` no esta.

7. **Modulo no depende de gTTS**: si `gtts` falla (sin internet, no instalado), el boton "🔊" muestra alert pero el resto del lector funciona. Degradacion graceful.

8. **`data-texto` con `|escapejs`**: el texto completo se pasa al JS embebido en `data-texto` con escape de JS para caracteres especiales. El JS lo lee de `textoDiv.dataset.texto` sin re-fetch. Evita 2 requests a `/lectura/ajax/morfologia/` cuando el usuario hace click rapido en varias palabras.

---

## 11. Roadmap

### Completado

- [x] R1: servicio `lectura.py` (3 funciones) + 19 tests
- [x] R2: 2 vistas + 2 templates + 1 AJAX + 11 tests
- [x] R3: este documento

### Extensiones posibles (futuras sesiones)

- **Guardar progreso**: modelo `LecturaRealizada` con palabras clickeadas
- **Marcar palabras conocidas**: integracion con SRS (`Flashcard` generico)
- **Traduccion al click**: pasar por DeepL/Google Translate (requiere API externa)
- **Velocidad de lectura TTS**: el endpoint `/tts/` no acepta `rate`. Podria extenderse
- **Modo "solo escuchar"**: sin click, sin panel — el texto se lee completo con highlight de palabra actual (requiere `SpeechSynthesis` con `onboundary` en vez de audio servidor)

### Fuera de scope

- Analisis de entonacion
- Comparacion con audio de hablante nativo
- Sincronizacion audio-palabra en tiempo real (requiere modelo ASR)

---

## 12. Uso rapido

```bash
python manage.py runserver

# En el navegador:
#   /lectura/                    -> selector de textos
#   /lectura/30001/              -> lector del texto 30001
```

### Flujo de uso

1. Ir a `/lectura/`
2. Elegir un texto ("Leer" en la fila)
3. En el lector:
   - Click en cualquier palabra → panel con POS, lemma, dependencia, oracion contenedora
   - Boton "🔊 Escuchar" → reproduce la palabra
   - Boton "🔊 Leer todo" → reproduce el texto completo

### Uso en shell

```python
from core.services.lectura import (
    segmentar_texto,
    morfologia_contextual,
    estadisticas_texto,
)

# Segmentacion
segmentos = segmentar_texto("Hola, mundo!")
# [{"tipo": "palabra", "texto": "Hola", "inicio": 0, "fin": 4}, ...]

# Morfologia
r = morfologia_contextual("Juan estudia", 0)
# {"palabra": "Juan", "pos_es": "nombre propio", ...}

# Estadisticas
r = estadisticas_texto("Primero me desperté. Luego tomé el tren.")
# {"n_palabras": 8, "n_oraciones": 2, ...}
```

### Verificar manualmente

Abrir navegador en `http://localhost:8000/lectura/`:
- Selector debe listar ~100 textos
- Click en "Leer" → lector con texto segmentado
- Click en palabra → panel lateral con morfologia
- Boton audio → suena (requiere conexion a internet para gTTS)
- Boton "Leer todo" → suena el texto completo

Si el panel no aparece: revisar console del navegador (F12) → puede ser que `/lectura/ajax/morfologia/` devuelva error.

---

## Cierre del plan original

| Modulo | Estado | Commits | Tests | Doc |
|---|---|---|---|---|
| 1 - POS / spaCy | ✅ | 4 | 41 | ✅ |
| 2 - Filologia | ✅ | 3 | 35 | ✅ |
| 3 - Lectura TTS | ✅ | 2 | 30 | este |
| 4 - Redaccion | ✅ | 6 | 43 | ✅ |
| 5 - SRS / SM-2 | ✅ | 5 | 63 | ✅ |
| 6 - Corpus (bonus) | ✅ | 4 | 30 | ✅ |

**Total proyecto**: 24 commits, ~242 tests, cobertura 97.35%, 6 docs de 12 secciones.

**Plan original**: 5 modulos. **Completado**: 6 (incluye corpus como bonus).

---

*Ultima actualizacion: 2026-10-19 tras R2 lectura.*