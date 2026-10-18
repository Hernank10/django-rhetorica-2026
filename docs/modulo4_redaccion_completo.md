# Modulo 4 - Taller de Redaccion Morfosintactica

**Estado**: produccion
**Commits**: 6 (`5983d60` .. `8284718`)
**Tests del modulo**: 43 (todos verdes)
**Ejercicios en DB**: 120 (20 manuales + 100 tecnicas)

> Documento generado desde el codigo fuente.

---

## 1. Resumen ejecutivo

El Taller de Redaccion evalua **produccion libre** de estudiantes en castellano
sin usar LLM ni NLP pesado. Todo deterministico, testeable, sin dependencias externas nuevas.

El estudiante escribe una oracion o un parrafo. El sistema detecta:

- **Tipo de oracion**: simple / compuesta coordinada / compuesta subordinada / yuxtapuesta
- **Tipo de subordinada**: sustantiva / adjetiva / adverbial
- **Conectores** usados y su categoria gramatical
- **Tipo de parrafo**: narrativo / descriptivo / argumentativo / expositivo

Devuelve feedback accionable, registra el error en `HistorialErrorSintactico` para el
motor adaptativo, y persiste cada intento en `EvaluacionRedaccion`.

### Que NO hace

- No evalua calidad literaria, originalidad, belleza
- No verifica concordancia sujeto-verbo con precision (requiere parser real)
- No analiza latin (requiere CLTK)
- No usa modelos de lenguaje

Es un **clasificador estructural** basado en reglas lexicas y heuristicas de contexto.

---

## 2. Arquitectura

```
core/
  models_redaccion.py           Modelo EvaluacionRedaccion
  models.py                     +3 campos en EjercicioLinguistico + re-export
  services/
    _diccionarios_redaccion.py  COORDINANTES, SUBORDINANTES, MARCADORES_PARRAFO
    redaccion.py                analizar_oracion, analizar_parrafo,
                                evaluar_ejercicio, clasificar_error
  views_redaccion.py            indice, detalle, historial
  admin_redaccion.py            EvaluacionRedaccionAdmin + inline
  templates/
    estudiante/base.html        Layout WCAG AA
    core/redaccion/             indice, ejercicio, historial
  fixtures/
    redaccion_ejercicios.json   20 manuales (R2)
    redaccion_100_tecnicas.json 100 tecnicas balanceadas (R4b)
  tests/                        21 + 9 + 6 + 7 = 43 tests
django_retorica/urls.py         /redaccion/*
```

---

## 3. Modelo de datos

### EvaluacionRedaccion

| Campo | Tipo | Notas |
|---|---|---|
| `estudiante` | FK AUTH_USER_MODEL CASCADE | related_name=evaluaciones_redaccion |
| `ejercicio` | FK EjercicioLinguistico CASCADE | related_name=evaluaciones_redaccion |
| `texto_estudiante` | TextField | Texto original |
| `analisis_json` | JSONField | Salida de analizar_* |
| `aprobado` | BooleanField | Resultado |
| `feedback` | TextField | Mensaje pedagogico |
| `fecha` | DateTimeField auto_now_add | Indexado con estudiante |

`ordering = ["-fecha"]` · indice compuesto `(estudiante, -fecha)`.

### Campos nuevos en EjercicioLinguistico

| Campo | Tipo | Notas |
|---|---|---|
| `es_redaccion` | BooleanField db_index | Flag rapido |
| `tipo_redaccion` | CharField(30) | Slug esperado por evaluar_ejercicio |
| `tecnica` | CharField(100) | Slug de la tecnica |

**Valores de `tipo_redaccion`**: oracion_simple, oracion_coordinada,
oracion_subordinada, oracion_yuxtapuesta, parrafo_narrativo,
parrafo_descriptivo, parrafo_argumentativo, parrafo_expositivo.

---

## 4. Servicio (core/services/redaccion.py)

Funciones puras. 100% testeable sin fixtures de Django.

### analizar_oracion(texto) -> dict

```python
{
    "tipo": "simple" | "compuesta_coordinada" | "compuesta_subordinada"
            | "yuxtapuesta" | "insuficiente" | "demasiado_largo",
    "n_oraciones": int,
    "n_verbos": int,
    "conectores": [{"texto", "tipo", "posicion", "categoria"}],
    "subordinadas": [{"tipo", "nexo"}],
    "longitud_palabras": int,
}
```

**Reglas de clasificacion:**

1. menos de 3 palabras -> insuficiente
2. mas de 500 palabras -> demasiado_largo
3. n_verbos <= 1 sin nexos -> simple
4. subordinantes -> compuesta_subordinada
5. coordinantes -> compuesta_coordinada
6. n_oraciones >= 2 o n_verbos >= 2 -> yuxtapuesta
7. fallback -> simple

**Desambiguacion de `que`**: verbo de pensamiento / verbo lista blanca /
preposicion previa -> sustantiva. Cualquier otro -> adjetiva.

### analizar_parrafo(texto) -> dict

```python
{
    "tipo_dominante": "narrativos" | "descriptivos" | "argumentativos"
                    | "expositivos" | "neutro" | "vacio",
    "n_oraciones": int,
    "marcadores_por_tipo": {"narrativos": int, ...},
}
```

### evaluar_ejercicio(texto, tipo_esperado) -> dict

```python
{
    "aprobado": bool,
    "tipo_detectado": str,
    "analisis": dict,
    "feedback": str,
}
```

### clasificar_error(texto, tipo_esperado) -> dict | None

Devuelve dict compatible con `HistorialErrorSintactico`:
`{"categoria_gramatical", "patron_error", "idioma": "ES"}`.
Si el texto cumple el tipo esperado, retorna `None`.

### Diccionarios

**COORDINANTES**:

| Categoria | Nexos |
|---|---|
| copulativa | y, e, ni |
| disyuntiva | o, u, o bien |
| adversativa | pero, sino, mas, sin embargo, no obstante, aunque |
| explicativa | o sea, es decir, esto es |

**SUBORDINANTES**:

| Categoria | Nexos |
|---|---|
| sustantiva | que, si |
| adjetiva | que, quien, cual, cuyo |
| adverbial_tiempo | cuando, mientras, antes que, despues que, en cuanto |
| adverbial_lugar | donde |
| adverbial_modo | como, segun, conforme |
| adverbial_causa | porque, pues, ya que, puesto que, dado que |
| adverbial_condicion | si, siempre que, a menos que |
| adverbial_concesion | aunque, a pesar de que, por mas que |
| adverbial_finalidad | para que, a fin de que |

---

## 5. Vistas y URLs

```python
path('redaccion/', views_redaccion.indice, name='redaccion_indice'),
path('redaccion/historial/', views_redaccion.historial, name='redaccion_historial'),
path('redaccion/<int:ejercicio_id>/', views_redaccion.detalle, name='redaccion_ejercicio'),
```

**Importante**: `historial` va **antes** de `<int:ejercicio_id>`.
Si va despues, `"historial"` se castea a `int` -> 404.

### indice(request) — GET publico

`EjercicioLinguistico.filter(es_redaccion=True).order_by("tipo_redaccion", "id")`.

### detalle(request, ejercicio_id) — GET publico, POST requiere login

- GET: `get_object_or_404(..., es_redaccion=True)`
- POST: evalua, crea `EvaluacionRedaccion`, renderiza con feedback

### historial(request) — GET requiere login

`.filter(estudiante=request.user).order_by("-fecha", "-id")[:50]`.

**Desempate `-id`**: `auto_now_add` puede generar timestamps identicos en
escrituras consecutivas. Sin desempate, SQLite ordena por PK ascendente
-> incoherente con `-fecha`. Bug real detectado por `test_ordering_descendente`.

### Templates

- `estudiante/base.html` — layout WCAG AA (focus, contraste, tablas semanticas)
- `core/redaccion/indice.html`, `ejercicio.html`, `historial.html`

---

## 6. Admin (core/admin_redaccion.py)

`EvaluacionRedaccionAdmin`:

- `list_display`: estudiante, ejercicio, aprobado, fecha, tipo_ejercicio
- `list_filter`: aprobado, fecha, ejercicio__tipo_redaccion
- `search_fields`: estudiante__username, ejercicio__titulo, texto_estudiante
- `date_hierarchy`: fecha

`EvaluacionRedaccionInline` en `EjercicioLinguistico` (solo si es_redaccion=True).

**Anti-`AlreadyRegistered`**: `admin.site._registry.get(EjercicioLinguistico)` +
añadir inline. Sin `unregister/register` (rompe si se importa dos veces).

---

## 7. Fixtures

### Manuales (R2, PKs 20001-20012 y 20101-20108)

| Tipo | Cantidad |
|---|---|
| oracion_simple | 2 |
| oracion_coordinada | 3 |
| oracion_subordinada | 5 |
| oracion_yuxtapuesta | 2 |
| parrafo_narrativo | 2 |
| parrafo_descriptivo | 2 |
| parrafo_argumentativo | 2 |
| parrafo_expositivo | 2 |
| **Total** | **20** |

### Tecnicas R4b (PKs 30001-30100)

| Tipo | Cantidad |
|---|---|
| parrafo_narrativo | 25 |
| parrafo_descriptivo | 25 |
| parrafo_expositivo | 25 |
| parrafo_argumentativo | 25 |
| **Total** | **100** |

**Total en DB**: **120** ejercicios de redaccion.

### Redaccion 100 tecnicas (R4b)

Generadas por `scripts/crear_r4b_fixtures.py` desde el JSON fuente
`ejercicios_completos-lengua-castellana/JSON completo - 100 tecnicas de redaccion en ingles.json`.

Correcciones aplicadas por el script:

- Detector de idioma para deshacer **swap** `ejemplo_es` / `ejemplo_en` del JSON original
- Slug estable `tNNN_titulo_snake_case`
- Plantilla de `ejercicio` (el JSON no lo traia)
- `contenido` JSON: `tipo_redaccion`, `tipo_original`, `teoria`, `ejemplo`,
  `enunciado`, `respuesta_esperada`, `idioma`

---

## 8. Tests (43 totales)

| Archivo | Tests |
|---|---|
| `test_services_redaccion.py` | 21 (servicio puro, sin BD) |
| `test_views_redaccion.py` | 9 (vistas) |
| `test_views_redaccion_historial.py` | 6 (historial) |
| `test_r4b_tecnicas.py` | 7 (fixtures) |
| **Total** | **43** |

### Patron loaddata en tests

```python
@pytest.fixture(scope="module")
def fixtures_cargadas(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "core/fixtures/redaccion_100_tecnicas.json", verbosity=0)

class TestAlgo:
    def test_x(self, fixtures_cargadas, db, client):  # db obligatorio
        ...
```

Sin `db`, cualquier `client.get()` que toque la BD lanza
`RuntimeError: Database access not allowed`.

---

## 9. Historial de commits

| Hash | Ronda | Contenido | Tests |
|---|---|---|---|
| `5983d60` | R2 | Modelo + 3 campos + 20 fixtures + migracion 0012 | — |
| `601c1c9` | R1 | Diccionarios + servicio + doc contrato | +21 |
| `ff5085b` | R3 | Vistas + templates + URLs | +9 |
| `12af84d` | R4a | Admin + inline | — |
| `87d17f8` | R5 | Historial + ordering determinista | +6 |
| `8284718` | R4b | 100 tecnicas balanceadas | +7 |

**Orden cronologico real**: R2 -> R1 -> R3 -> R4a -> R5 -> R4b.
R1 (servicio) y R2 (modelo) son independientes entre si.

---

## 10. Decisiones tecnicas

1. **Sin deps nuevas**: no spaCy, no CLTK, no LLM. Determinismo total, coste cero.
2. **Funciones puras en el servicio**: 21 tests sin BD.
3. **`que` por contexto**: 3 heuristicas -> 80-85% precision.
4. **Re-export de `EvaluacionRedaccion`**: `from core.models import X` sigue funcionando.
5. **Anti-`AlreadyRegistered`**: `_registry.get()` en vez de `unregister/register`.
6. **URL `historial` antes que `<int:id>`**: order matters.
7. **Ordering con `-id` desempate**: timestamps empatados son inevitables.

---

## 11. Roadmap

### Completado

- [x] R1: diccionarios + servicio + doc
- [x] R2: modelo + campos + migracion + fixtures manuales
- [x] R3: vistas + templates + URLs
- [x] R4a: admin + inline
- [x] R5: historial + ordering determinista
- [x] R4b: 100 tecnicas balanceadas

### Pendiente opcional

- [ ] **R4c**: 100 tecnicas periodisticas (JSON parsea OK, sin `tipo` -> reclasificar)
- [ ] **R4c-bis**: 100 tecnicas cientificas (JSON roto L652, comillas anidadas)
- [ ] **R4c-tris**: 100 tecnicas retoricas (JSON parsea OK, lista pura)

### Fuera de alcance (fase futura)

- Concordancia S-V precisa -> spaCy
- Funcion sintactica por palabra -> parser
- Analisis de latin -> CLTK
- Evaluacion de calidad persuasiva -> LLM
- Deteccion de figuras retoricas -> modulo 4.5 separado

### Modulos siguientes

- **Modulo 5 (SRS)**: SM-2 reusando Respuesta + ProgresoCategoria + HistorialErrorSintactico
- Modulo 2 (Filologia), Modulo 3 (TTS lectura), Modulo 1 (Parser NLP)

---

## 12. Uso rapido

```bash
python manage.py migrate
python manage.py loaddata core/fixtures/redaccion_ejercicios.json
python manage.py loaddata core/fixtures/redaccion_100_tecnicas.json

python -m pytest core/tests/test_services_redaccion.py -v
python -m pytest core/tests/test_views_redaccion.py -v
python -m pytest core/tests/test_views_redaccion_historial.py -v
python -m pytest core/tests/test_r4b_tecnicas.py -v
```

### Evaluar en shell

```python
from core.services.redaccion import evaluar_ejercicio

evaluar_ejercicio("Juan estudia, pero su hermano juega", "oracion_coordinada")
# {'aprobado': True, 'tipo_detectado': 'compuesta_coordinada', ...}
```

### Crear un ejercicio nuevo

```python
from core.models import EjercicioLinguistico

EjercicioLinguistico.objects.create(
    titulo="Mi tecnica nueva",
    contenido={"enunciado": "...", "teoria": "...", "ejemplo": "..."},
    categoria="redaccion",
    tipo="produccion_libre",
    nivel=2,
    puntos=10,
    es_redaccion=True,
    tipo_redaccion="parrafo_argumentativo",
    tecnica="mi_tecnica_nueva",
    idioma="ES",
)
```

---

*Ultima actualizacion: 2026-10-18 tras cierre de R4b (8284718).*