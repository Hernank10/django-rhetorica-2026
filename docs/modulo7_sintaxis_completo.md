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

*Ultima actualizacion: 2026-10-20 tras S5.2 (vistas parafrasis).*