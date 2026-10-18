# Modulo 2 - Filologia Comparada

**Estado**: produccion
**Commits**: 2 (`9d1fe44` .. `959e1f0`)
**Tests del modulo**: 35 (todos verdes)
**Etimos**: 50 (5 categorias balanceadas)
**Cobertura global al cierre**: 97.89%

---

## 1. Resumen ejecutivo

Explorador de filologia comparada latin -> castellano. Muestra la evolucion
fonetica de 50 etimos con la doble via **patrimonial vs cultismo** (el eje
pedagogico central de la historia del espanol) y cognados ingleses cuando
aplican.

Dos paginas:
- **`/filologia/`**: explorador con buscador (por latin, castellano o ingles) + listado
- **`/filologia/<etimo>/`**: ficha completa con cadena evolutiva + regla + ejemplo

### Que NO hace

- No incluye ejercicios evaluables (solo explorador, por decision de scope)
- No entrena modelos ni usa NLP
- No incluye raiz proto-indoeuropea ni autores de referencia
- Latin -> ingles **NO** es derivacion directa: son cognados PIE. La distincion esta explicitada en el campo `regla`.

---

## 2. Arquitectura

```
core/
  services/
    _etimos_filologia.py      50 etimos (dict Python, versionable)
    filologia.py              3 funciones puras
  views_filologia.py          indice, detalle
  templates/core/filologia/
    indice.html               buscador + tabla de 50 etimos
    detalle.html              ficha completa (cadena + regla + ejemplo)

django_retorica/urls.py       /filologia/ + /filologia/<slug>/

core/tests/
  test_services_filologia.py  26 tests (motor puro, sin BD)
  test_views_filologia.py     9 tests (vistas)
```

---

## 3. Modelo de datos

**Sin modelos Django.** Los 50 etimos son dicts Python en `_etimos_filologia.py`.

**Estructura de cada etimo:**

| Campo | Tipo | Notas |
|---|---|---|
| `latin` | str | Forma latina de referencia |
| `es_patrimonial` | str | Evolucion popular |
| `es_cultismo` | str | Evolucion culta |
| `en_cognado` | str \| None | Cognado ingles (o None si no aplica) |
| `regla` | str | Cambio fonetico aplicado |
| `ejemplo` | str | Frase de uso |
| `categoria` | str | Una de las 5 categorias |

**Razon de la eleccion**: dicts > modelo Django porque son datos inmutables
de referencia. No hace falta CRUD, no hace falta migracion, no hace falta
admin. Si en el futuro se quiere permitir edicion, se migran a un modelo
con `loaddata` sin romper el servicio.

---

## 4. Servicio (core/services/filologia.py)

Funciones puras, sin BD, sin estado.

### `_normalizar(texto) -> str`

NFKD Unicode + lowercase + collapse whitespace. Quita acentos para busqueda
case-insensitive y acento-insensitive.

### `buscar_etimo(termino) -> list[dict]`

Busca el termino (substring) en `latin`, `es_patrimonial`, `es_cultismo`,
`en_cognado` y `categoria`. Retorna lista de dicts coincidentes.

- `buscar_etimo("noctem")` -> 1 resultado (latin exacto)
- `buscar_etimo("noche")` -> 1 (patrimonial)
- `buscar_etimo("night")` -> 1 (cognado)
- `buscar_etimo("noc")` -> 1+ (substring)
- `buscar_etimo("diptongacion")` -> 10 (categoria)
- `buscar_etimo("")` o `None` -> `[]`

### `cadena_evolutiva(etimo_latin) -> dict | None`

Lookup por latin exacto. Case-insensitive y sin acentos.
Retorna el dict completo del etimo o `None`.

### `categorias_disponibles() -> list[str]`

Lista ordenada (sorted) de categorias unicas presentes en ETIMOS.

---

## 5. Vista y URLs

```python
path('filologia/', views_filologia.indice, name='filologia_indice'),
path('filologia/<slug:etimo>/', views_filologia.detalle, name='filologia_detalle'),
```

### `indice(request)` - GET publico

- Sin `?q=`: renderiza los 50 etimos en tabla
- Con `?q=<termino>`: renderiza el resultado de `buscar_etimo(q)`
- Sin resultados: mensaje "Sin resultados"
- Muestra total + categorias disponibles

### `detalle(request, etimo)` - GET publico

`cadena_evolutiva(etimo)` -> render de ficha. Si es `None` -> `Http404`.

### Templates

- `estudiante/base.html` (heredado del modulo 4) como layout
- `indice.html`: tabla con latin / patrimonial / cultismo / cognado / categoria
- `detalle.html`: 4 cards (latin, patrimonial verde, cultismo azul, cognado rojo si aplica)
  + bloque regla + bloque ejemplo

---

## 6. Distribucion de los 50 etimos

| Categoria | Count | Ejemplos |
|---|---|---|
| `consonantico` | 15 | noctem, ferrum, aqua, oculum, plenum, clamare, flamma, causam, aurum, clavem, sigillum, speculum, vetulum, strictum, lactem |
| `diptongacion` | 10 | portam, terram, dentem, fortem, cornu, focus, novum, bonum, mortem, sortem |
| `doblete` | 10 | causam, clavem, sigillum, speculum, vetulum, directum, strictum, integrum, operam, rapidum |
| `cognado_ingles` | 10 | patrem, matrem, pedem, cornu, dentem, tres, duo, sex, septem, lac |
| `evolucion_curiosa` | 5 | calidum, auricula, multum, focum, civitatem |

**Nota**: algunos etimos aparecen en **dos categorias** (cornu, dentem, causam, clavem, sigillum, speculum, vetulum, strictum, lactem/lac, focus/focum). El test `test_pares_latin_categoria_unicos` verifica que cada par (latin, categoria) sea unico, no que cada latin sea unico.

---

## 7. Tests (35 totales)

| Archivo | Tests |
|---|---|
| `test_services_filologia.py` | 26 (motor puro) |
| `test_views_filologia.py` | 9 (vistas) |

### Cobertura por clase

**TestBuscarEtimo (11 tests):** vacio, none, sin match, latin exacto, patrimonial, cultismo, cognado, categoria, case-insensitive, sin acentos, substring

**TestCadenaEvolutiva (5 tests):** noctem completo, case-insensitive, inexistente, vacio, none

**TestCategoriasDisponibles (3 tests):** 5 categorias, ordenadas, categorias esperadas

**TestIntegridadEtimos (7 tests):** 50 etimos, todas las claves, categorias validas, reglas no vacias, ejemplos no vacios, pares unicos, distribucion correcta

**TestIndiceFilologia (5 tests):** GET 200, render HTML, 50 etimos sin filtro, filtro q, filtro sin match

**TestDetalleFilologia (4 tests):** noctem 200, cadena completa, case-insensitive URL, inexistente 404

---

## 8. Commits

| Hash | Ronda | Contenido | Tests |
|---|---|---|---|
| `9d1fe44` | R1 | 50 etimos + motor puro + 26 tests | +26 |
| `959e1f0` | R2 | vistas indice/detalle + 2 templates + 2 URLs + 9 tests | +9 |

---

## 9. Decisiones tecnicas

1. **Sin modelos Django**: los etimos son datos inmutables de referencia. Un dict es mas simple que un modelo con migracion + admin para datos que no cambian.

2. **Cognado ingles etiquetado como tal**: Latin -> ingles NO es derivacion, es cognado PIE (ambos vienen de proto-indoeuropeo). El campo `regla` lo explicita: "Latin p- / -t- -> germ. f- / th- (cognado PIE)".

3. **Doble via patrimonial/cultismo**: es el eje pedagogico central de la historia del espanol. Cada etimo muestra **ambas** formas (noche/nocturno, agua/acuatico, hierro/ferroso) + la regla fonetica que las diferencia.

4. **Categoria como mecanismo de filtro**: 5 categorias balanceadas (15+10+10+10+5) permiten busqueda tematica. `buscar_etimo("diptongacion")` retorna los 10 casos.

5. **Normalizacion Unicode NFKD**: quita acentos para busqueda robusta. `buscar_etimo("acuitico")` con o sin acento retornan lo mismo.

6. **URL namespaced `/filologia/...`**: mismo patron que SRS (`/estudiante/srs/...`). Evita colisiones con otros modulos. El proyecto ya tenia `/estudiante/repaso/` y `/estudiante/estadisticas/` registrados, asi que agregamos prefijo propio.

7. **Deduplicacion post-hoc**: los 50 etimos originales se generaron en 4 bloques por limite de paste de PowerShell. Algunos bloques se re-ejecutaron accidentalmente y duplicaron etimos (87 en total). El script `dedupe_filologia.py` limpio duplicados exactos por firma JSON. Los pares (latin, categoria) duplicados con contenido distinto (ej. cornu como diptongacion + cognado_ingles) se conservaron ambos.

---

## 10. Roadmap

### Completado

- [x] R1: 50 etimos + motor puro (26 tests)
- [x] R2: vistas + templates + 9 tests
- [x] R3: este documento

### Pendiente opcional (Ruta B del plan original)

- [ ] **R4 filologia**: ejercicios evaluables
  - Nuevos campos en `EjercicioLinguistico`: `es_filologico`, `etimo_latin`
  - Migracion 0014
  - 30-40 fixtures con enunciado + respuesta esperada
  - Servicio `evaluar_respuesta_filologica(texto, respuesta_esperada)` con scoring
  - Vista `/filologia/ejercicio/<pk>/` con textarea + feedback
  - ~15 tests
  - ~2-3h

### Fuera de alcance

- Raiz proto-indoeuropea (requiere investigacion linguistica, no programacion)
- Autores de referencia (datos bibliograficos, no funcionalidad)
- Filologia de otras lenguas (frances, italiano, portugues): la estructura del dict lo permitiria, agregar mas filas)

---

## 11. Uso rapido

```bash
python manage.py check
python manage.py runserver

# En el navegador:
#   /filologia/                    -> explorador
#   /filologia/?q=noctem           -> busqueda
#   /filologia/noctem/             -> ficha completa
```

### Uso en shell

```python
from core.services.filologia import (
    buscar_etimo,
    cadena_evolutiva,
    categorias_disponibles,
)

# Explorar
categorias_disponibles()
# ['cognado_ingles', 'consonantico', 'diptongacion', 'doblete', 'evolucion_curiosa']

# Busqueda
buscar_etimo("noche")
# [{'latin': 'noctem', 'es_patrimonial': 'noche', 'es_cultismo': 'nocturno', ...}]

# Ficha completa
cadena_evolutiva("noctem")
# {'latin': 'noctem', 'es_patrimonial': 'noche', 'es_cultismo': 'nocturno',
#  'en_cognado': 'night', 'regla': 'Latin -ct- -> ES -ch- ...',
#  'ejemplo': 'La noche es tiempo de noctambulos.', 'categoria': 'consonantico'}

# Busqueda por categoria
buscar_etimo("diptongacion")
# [10 dicts con categoria='diptongacion']
```

### Agregar un etimo nuevo

Editar `core/services/_etimos_filologia.py` y agregar un dict con las 7 claves.
El test `test_50_etimos` va a fallar hasta que actualices el numero esperado
a 51. Los tests de integridad (`test_todos_tienen_7_claves`,
`test_distribucion_por_categoria`) tambien pueden requerir ajuste segun el
nuevo etimo.

---

## 12. Cierre de modulos completados esta sesion

Modulos cerrados con docs:

- **Modulo 4 (Redaccion morfosintactica)**: 6 commits, 43 tests, 120 ejercicios, `docs/modulo4_redaccion_completo.md`
- **Modulo 5 (SRS / SM-2)**: 4 commits, 63 tests, 35 flashcards seed, `docs/modulo5_srs_completo.md`
- **Modulo 2 (Filologia comparada)**: 2 commits, 35 tests, 50 etimos, este documento

**Total**: 12 commits, 141 tests, 97.89% cobertura, 3 docs de 12 secciones.

---

*Ultima actualizacion: 2026-10-18 tras R2 (959e1f0).*