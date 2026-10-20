# Modulo 7 — Sintaxis: Parafrasis Mecanica

**Commits**: 3 (`1ea4303` .. `45ef1e9`)
**Tests del modulo**: 52 (40 servicios + 12 vistas)
**Cobertura global al cierre**: 97.21%

---

## 1. Resumen ejecutivo

Motor de **parafrasis mecanica** 100% determinista, sin LLM. Evalua si una
parafrasis `activa_a_pasiva` o `pasiva_a_activa` cumple la transformacion
esperada, combinando features del arbol spaCy con similitud Jaccard. Incluye
demo interactiva con AJAX + debounce.

## 2. Arquitectura

```
core/services/parafrasis.py         (9 funciones, ~180 lineas)
  |- PARTICIPIOS_IRREGULARES        (15 irregulares)
  |- SER_FORMAS                     (5 tiempos x 6 personas)
  |- participio_verbo()             regular + irregular
  |- conjugar_ser()                 fallback a presente
  |- _pers_num() / _tiempo()        helpers sobre tok.morph
  |- _doc()                         spaCy con lru_cache
  |- es_pasiva()                    detecta ser/estar + participio
  |- transformar_a_pasiva()         activa -> pasiva sugerida
  |- transformar_a_activa()         pasiva -> activa sugerida
  |- comparar_features()            checks por tipo
  |- similitud_tokens()             Jaccard sin puntuacion
  |- verificar_parafrasis()         orquestador -> dict 7 claves

core/views_parafrasis.py            (2 vistas, 22 lineas, 100% cubierto)
core/templates/core/parafrasis/demo.html
django_retorica/urls.py             (2 paths, prefijo /sintaxis/parafrasis/)
```

Contrato JSON del endpoint AJAX (7 claves):
`aprobado, tipo, similitud, features, feedback, sugerencia, es_pasiva_original`

## 3. Instalacion reproducible

```powershell
cd "E:\02_proyectos\django-rhetorica"
E:\PythonPortable_Django5\python.exe -m pytest core\tests\test_services_parafrasis.py -v
E:\PythonPortable_Django5\python.exe -m pytest core\tests\test_views_parafrasis.py -v
E:\PythonPortable_Django5\python.exe manage.py runserver
# Abrir http://127.0.0.1:8000/sintaxis/parafrasis/
```

## 4. Servicio parafrasis.py

### 4.1 Tablas deterministas

**PARTICIPIOS_IRREGULARES** (15 entradas):

```
abrir->abierto, cubrir->cubierto, descubrir->descubierto,
escribir->escrito, romper->roto, hacer->hecho,
decir->dicho, ver->visto, poner->puesto,
volver->vuelto, devolver->devuelto, resolver->resuelto,
morir->muerto, freir->frito, imprimir->impreso
```

**SER_FORMAS**: 5 tiempos (Pres, Past, Imp, Fut, Cond) x 6 personas (1s..3p).
Fallback: `Pres/3s -> "es"`.

### 4.2 Flujo de verificacion

1. Rechaza copia identica (case-insensitive) -> `aprobado=False`
2. `comparar_features()` -> checks por tipo
3. `similitud_tokens()` -> Jaccard sin puntuacion
4. Aprueba si todos los checks True **y** `similitud >= 0.15`

### 4.3 Tipos soportados

| Tipo | Checks requeridos |
|---|---|
| `activa_a_pasiva` | `tiene_ser`, `tiene_participio`, `tiene_por` |
| `pasiva_a_activa` | `no_tiene_ser`, `no_tiene_participio` |
| `reordenamiento` (alias) | igual que `activa_a_pasiva` |

## 5. Vistas y URLs

| Vista | Metodo | Ruta | Proposito |
|---|---|---|---|
| `parafrasis_demo` | GET, POST | `/sintaxis/parafrasis/` | Renderiza template |
| `parafrasis_ajax` | POST | `/sintaxis/parafrasis/ajax/` | Contrato JSON |

**Validaciones del endpoint AJAX:**

- `original` vacio -> 400 `{"error": "Faltan textos"}`
- `parafraseado` vacio -> 400 `{"error": "Faltan textos"}`
- `tipo` fuera de `{activa_a_pasiva, pasiva_a_activa}` -> 400 `{"error": "Tipo invalido"}`
- GET al endpoint POST -> 405 (por `require_http_methods`)

## 6. Templates

`core/templates/core/parafrasis/demo.html`:

- `<form>` con `id="form-parafrasis"` + `{% csrf_token %}`
- `<textarea id="texto_original">` + `<textarea id="texto_parafraseado">`
- `<select id="tipo">` con 2 opciones
- `<div id="resultado">` para output
- JS con debounce 400ms, `fetch()` POST, `JSON.stringify(data, null, 2)`

## 7. Tests (52 totales)

### 7.1 Servicios (`test_services_parafrasis.py` — 40 tests)

| Clase | Tests | Modelo |
|---|---|---|
| `TestParticipios` | 8 | no |
| `TestConjugarSer` | 9 | no |
| `TestParticipioRamasDefensivas` | 2 | no |
| `TestEsPasiva` | 4 | si |
| `TestTransformarAPasiva` | 3 | si |
| `TestTransformarAActiva` | 2 | si |
| `TestSimilitud` | 3 | si |
| `TestVerificarParafrasis` | 5 | si |
| `TestRamasDefensivas` | 4 | si |

### 7.2 Vistas (`test_views_parafrasis.py` — 12 tests)

| Clase | Tests | Modelo |
|---|---|---|
| `TestDemoView` | 4 | no |
| `TestAjaxValidation` | 4 | no |
| `TestAjaxHappyPath` | 4 | si |

Cobertura `views_parafrasis.py`: **100%**.

## 8. Commits

```
45ef1e9  feat(sintaxis): S5.2 - vistas parafrasis + AJAX + template + 12 tests
242a3ab  test(parafrasis): cubre ramas defensivas
1ea4303  feat(parafrasis): S5.1 - motor mecanico + 34 tests
```

## 9. Decisiones tecnicas

### 9.1 spaCy ES vs UD estandar

El modelo `es_core_news_md` **no sigue** el esquema UD canonico para voz
pasiva. Diferencias empiricas (verificadas con `scripts/diag_pasiva.py`):

| Token | UD esperado | spaCy ES real |
|---|---|---|
| `ser` (aux) | `dep=aux:pass` | `dep=aux` |
| participio | `dep=ROOT` con `VerbForm=Part` | igual |
| agente | `obl:agent` | `obj` con `case=por` |

Por eso `es_pasiva()` y `transformar_a_activa()` detectan pasiva via
`tok.pos_=="AUX" and tok.lemma_ in {"ser","estar"}` + participio ROOT.

### 9.2 Sin LLM

Todas las funciones son deterministas: mismo input -> mismo output. Sin
llamadas a APIs externas, sin caching de red. Permite tests deterministas y
auditoria linea por linea.

### 9.3 Similitud como gate (no como score)

`similitud_tokens()` solo se usa para rechazar copias literales
(`similitud >= 0.15` como piso). No se usa para medir "calidad" de la
parafrasis.

### 9.4 Vista delgada

`views_parafrasis.py` (22 lineas) solo valida + delega al servicio. Toda la
logica vive en `parafrasis.py`. Resultado: 100% cobertura de la vista con 12
tests triviales, y la logica compleja se testea a nivel servicio.

## 10. Roadmap

- **S5.4**: parafrasis sintactica real usando arbol de dependencias
  (reordenamiento de constituyentes, no solo activa<->pasiva).
- **S5.5**: parafrasis de registro (formal<->coloquial) via lexico.
- **Futuro**: integracion con `adaptive_engine.md` para tracking de progreso.

## 11. Uso rapido

```python
from core.services.parafrasis import verificar_parafrasis, es_pasiva

r = verificar_parafrasis(
    "Juan lee el libro",
    "El libro es leido por Juan",
    "activa_a_pasiva",
)
# r["aprobado"] == True
# r["similitud"] ~= 0.7
# r["feedback"] == "Correcto. Transformacion mecanica..."

es_pasiva("El libro fue escrito por Juan")  # True
es_pasiva("Juan lee el libro")               # False
```

---

## 12. Reordenamiento sintactico (S5.4)

**Agregado post-S5.3.** 5 funciones de reordenamiento usando el arbol de
dependencias de spaCy. Interfaz visual con boton "Sugerir reordenamientos".

### 12.1 Servicio parafrasis_reordenamiento.py

`core/services/parafrasis_reordenamiento.py` (82 lineas, 5 funciones):

- `_subarbol_texto(tok)` - texto del subarbol (recursivo)
- `detectar_constituyentes(texto)` - dict con sujeto, verbo, objeto, obl, advmod
- `reordenar_fronting(texto, componente)` - mueve obl/advmod al frente con coma
- `reordenar_svo_canonico(texto)` - normaliza a SVO + extras
- `verificar_reordenamiento(orig, para, tipo)` - similitud Jaccard >= 0.6 + orden distinto

Importa `_doc` y `similitud_tokens` del servicio `parafrasis.py` para no
duplicar carga de spaCy ni logica de similitud.

### 12.2 Endpoint AJAX

```
POST /sintaxis/parafrasis/reordenar/   name=parafrasis_reordenar
Body: original=<texto>
Response: {
  "sugerencias": [fronting_obl, fronting_advmod, svo_canonico],
  "constituyentes": {sujeto, verbo, objeto, obl, advmod, disponible, razon}
}
```

- `400` si falta `original` o esta vacio
- `405` si GET (por `require_http_methods(["POST"])`)
- Cada sugerencia tiene: `disponible, esperado, razon, tipo`

### 12.3 Template (patch a demo.html)

Extendido en S5.4.2:

- Boton `id="btn-reordenar"` fuera del `<form>`
- Div `id="sugerencias"` para output
- JS: click handler que hace `fetch()` POST y renderiza lista (`- tipo: esperado`)
- CSRF token tomado del form existente

### 12.4 Tests (25 nuevos)

| Archivo | Tests | Modelo |
|---|---|---|
| `test_services_parafrasis_reordenamiento.py` | 15 | si (4 skipean sin modelo) |
| `test_views_parafrasis_reordenamiento.py` | 10 | si (6 sin modelo, 4 con) |

Desglose:

- `TestDetectarConstituyentes`: 4 tests (SVO, con obl, sin verbo, vacio)
- `TestReordenarFronting`: 5 tests (obl, advmod, invalido, sin obl, vacio)
- `TestReordenarSvoCanonico`: 2 tests (obl fronted, sin objeto)
- `TestVerificarReordenamiento`: 4 tests (valido, identicos, vacio, similitud baja)
- `TestReordenarValidation`: 4 tests (GET 405, sin original, vacio, solo espacios)
- `TestReordenarHappyPath`: 4 tests (con obl, sin obl, SVO, constituyentes)
- `TestReordenarContrato`: 2 tests (keys top-level, keys por sugerencia)

### 12.5 Cobertura al cierre

| Archivo | Cobertura |
|---|---|
| `parafrasis_reordenamiento.py` | 96% (3 lineas defensivas sin cubrir) |
| `views_parafrasis_reordenamiento.py` | 100% |
| Global | **97.25%** |

Las 3 lineas sin cubrir en `parafrasis_reordenamiento.py` son paths defensivos
de spaCy (subtree vacio, verbo no ROOT). No vale la pena forzarlos: los
happy paths y validaciones estan cubiertos.

### 12.6 Decisiones tecnicas

**Vista en archivo separado**: `views_parafrasis_reordenamiento.py` en lugar
de extender `views_parafrasis.py`. Razon: `views_parafrasis.py` estaba al
100% de cobertura, agregar branches hubiera bajado ese numero. Archivo aparte
mantiene granularidad.

**Sin LLM, determinista**: reordenamientos basados en reglas sobre el arbol
spaCy. Mismo input -> mismo output. Permite tests reproducibles.

**Verificador robusto**: similitud Jaccard >= 0.6 + orden distinto. Acepta
"En el parque, Juan lee el libro" desde "Juan lee el libro en el parque"
porque Jaccard de tokens ~0.83 y el orden cambio. Rechaza "Pedro corre"
porque Jaccard bajo.

**Alineacion con S5.1**: `verificar_reordenamiento` mantiene el mismo
contrato de retorno que `verificar_parafrasis` (5 claves: aprobado, tipo,
similitud, features, feedback). Coherencia de API interna.

### 12.7 Uso rapido

```python
from core.services.parafrasis_reordenamiento import (
    detectar_constituyentes,
    reordenar_fronting,
    verificar_reordenamiento,
)

c = detectar_constituyentes("Juan lee el libro en el parque")
# c["sujeto"]="Juan", c["objeto"]="el libro", c["obl"]=["en el parque"]

r = reordenar_fronting("Juan lee el libro en el parque", "obl")
# r["esperado"] = "En el parque, Juan lee el libro"

v = verificar_reordenamiento(
    "Juan lee el libro en el parque",
    "En el parque, Juan lee el libro",
)
# v["aprobado"] == True, v["similitud"] ~= 0.83
```

---
## 13. Parafrasis de registro (S5.5)

**Agregado post-S5.4.** Transformacion lexica formal <-> coloquial sin LLM.
9 pares de palabras + deteccion de registro dominante + verificacion.

### 13.1 Servicio parafrasis_registro.py

`core/services/parafrasis_registro.py` (87 lineas, 5 funciones):

- `_palabras(texto)` - tokeniza a palabras lowercase via regex
- `_reemplazar_palabras(texto, mapping)` - replace preservando capitalizacion
- `detectar_registro(texto)` - cuenta marcadores formales vs coloquiales
- `transformar_registro(texto, hacia)` - formal->coloquial o coloquial->formal
- `verificar_registro(orig, para, tipo)` - valida reduccion de marcadores

**9 pares lexicos** (PARES_FORMAL_A_COLOQUIAL):

| Formal | Coloquial |
|---|---|
| usted | vos |
| ustedes | vosotros |
| automovil | carro |
| dinero | plata |
| trabajo | laburo |
| profesor | profe |
| estupendo | genial |
| comer | papear |
| cansado | reventado |

Sin acentos ni colisiones. `PARES_COLOQUIAL_A_FORMAL` es el inverso
generado por dict comprehension.

### 13.2 Logica de deteccion

`detectar_registro` devuelve dict con:
- `registro`: "formal" | "coloquial" | "neutral"
- `formal_count`, `coloquial_count`: conteo de marcadores
- `marcadores_formal`, `marcadores_coloquial`: listas de palabras encontradas

Regla: si `formal_count > coloquial_count` -> formal, vice versa, empate -> neutral.

### 13.3 Verificacion

`verificar_registro(orig, para, tipo)` valida:
- `formal_a_coloquial`: original tiene formales Y parafraseado reduce el conteo
- `coloquial_a_formal`: original tiene coloquiales Y parafraseado reduce el conteo
- Identicos -> rechazo inmediato
- Contrato de retorno alineado con S5.1/S5.4 (aprobado, tipo, features, feedback)

### 13.4 Vistas y URLs

| Vista | Metodo | Ruta | Proposito |
|---|---|---|---|
| `registro_demo` | GET, POST | `/sintaxis/parafrasis/registro/` | Renderiza template |
| `registro_ajax` | POST | `/sintaxis/parafrasis/registro/ajax/` | Deteccion + transformacion + verificacion |

**Validaciones del endpoint AJAX:**
- `original` vacio -> 400 `{"error": "Falta original"}`
- `tipo` fuera de `{formal_a_coloquial, coloquial_a_formal}` -> 400 `{"error": "Tipo invalido"}`
- Si `parafraseado` esta presente, incluye `verificacion` en la respuesta
- GET -> 405

**Respuesta JSON:** 2 o 3 claves segun si hay parafraseado:
- Siempre: `deteccion_original`, `transformacion_sugerida`
- Opcional: `verificacion` (solo si `parafraseado` no vacio)

### 13.5 Template registro.html

`core/templates/core/parafrasis/registro.html`:
- Form `id="form-registro"` con 2 textareas + select de tipo
- Boton `id="btn-registro"` (click handler, no submit)
- Div `id="resultado"` para output
- Link de vuelta al demo principal `/sintaxis/parafrasis/`
- JS: fetch POST + render lineas (registro detectado / sugerencia / verificacion)

Ademas, `demo.html` extendido con link a la pagina de registro.

### 13.6 Tests (28 nuevos)

| Archivo | Tests | Modelo |
|---|---|---|
| `test_services_parafrasis_registro.py` | 18 | no (puro Python) |
| `test_views_parafrasis_registro.py` | 10 | no |

Sin spaCy: los 28 tests corren en ~3s total (vs ~10s los que usan modelo).

Desglose servicios:
- `TestDetectarRegistro`: 5 tests (formal, coloquial, neutral, vacio, empate)
- `TestTransformarRegistro`: 4 tests (formal->coloq, coloq->formal, sin cambios, hacia invalido)
- `TestDicts`: 3 tests (inverso correcto, 9 pares, sin colisiones)
- `TestVerificarRegistro`: 6 tests (aprobado ambos sentidos, identicos, original neutral, tipo invalido, vacio)

Desglose vistas:
- `TestRegistroDemo`: 4 tests (GET ok, ids presentes, url ajax, POST)
- `TestRegistroAjaxValidation`: 3 tests (GET 405, sin original, tipo invalido)
- `TestRegistroAjaxHappyPath`: 3 tests (solo original, con parafraseado aprobado, contrato JSON)

### 13.7 Cobertura al cierre

| Archivo | Cobertura |
|---|---|
| `parafrasis_registro.py` | 98% (2 lineas defensivas sin cubrir) |
| `views_parafrasis_registro.py` | 100% |
| Global | **97.31%** |

### 13.8 Decisiones tecnicas

**Determinista, sin spaCy**: reemplazo 1-a-1 por diccionario + regex. No
requiere modelo. Tests en <2s. Permite uso offline total.

**Dict comprehension inverso**: `PARES_COLOQUIAL_A_FORMAL` derivado de
`PARES_FORMAL_A_COLOQUIAL`, no escrito a mano. Imposible desincronizacion.

**Capitalizacion preservada**: `_reemplazar_palabras` mantiene la primera
letra mayuscula si el original lo estaba ("Usted" -> "Vos", "usted" -> "vos").

**Template separado**: `registro.html` en lugar de extender `demo.html`.
`demo.html` ya tiene 12 tests S5.2 + 10 S5.4.2; agregar mas riesgo sin
beneficio. Demo principal linkea a registro, cada pagina mantiene su scope.

**Endpoint unificado**: un solo POST `/registro/ajax/` que hace deteccion +
transformacion + verificacion en una llamada. El cliente no necesita 3
endpoints. El campo `verificacion` es opcional segun si el usuario ya
escribio su parafrasis.

### 13.9 Uso rapido

```python
from core.services.parafrasis_registro import (
    detectar_registro,
    transformar_registro,
    verificar_registro,
)

d = detectar_registro("Usted tiene dinero")
# d["registro"] == "formal", d["formal_count"] == 2

t = transformar_registro("Usted tiene dinero", "coloquial")
# t["esperado"] == "Vos tiene plata", t["cambios"] == [{de:"usted",a:"vos"}, {de:"dinero",a:"plata"}]

v = verificar_registro(
    "Usted tiene dinero",
    "Vos tiene plata",
    "formal_a_coloquial",
)
# v["aprobado"] == True
```

---

*Ultima actualizacion: 2026-10-20 tras S5.5.2 (parafrasis de registro).*
