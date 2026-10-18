# Modulo 5 - Sistema de Repeticion Espaciada (SRS)

**Estado**: produccion
**Commits**: 4 (`2a36b39` .. `d74e477`)
**Tests del modulo**: 63 (todos verdes)
**Cobertura global al cierre**: 97.86%

---

## 1. Resumen ejecutivo

Sistema de repeticion espaciada basado en SM-2 (SuperMemo 2), el algoritmo
detras de Anki. Programa repasos automaticos de vocabulario y reglas segun
la tasa de olvido real de cada estudiante.

Componentes:
- **Flashcard**: tarjeta frente/reverso (vocabulario, declinacion, conjugacion, regla, redaccion)
- **Review**: instancia de repaso con estado SM-2 (intervalo, facilidad, repeticiones)
- **SM-2 puro**: algoritmo deterministico sin BD
- **Servicios con BD**: orquestan SM-2 + modelos
- **Vistas**: sesion de repaso + dashboard de estadisticas
- **Ciclo adaptativo**: errores de redaccion -> flashcards automaticas -> repaso

### Que NO hace

- No usa ML ni LLM. SM-2 es puro calculo deterministico
- No genera contenido de flashcards (lo hace el estudiante o el management command)
- No envia notificaciones por email/push (fuera de alcance)

---

## 2. Arquitectura

```
core/
  models_srs.py                 Flashcard, Review
  services/
    srs.py                      aplicar_sm2 (puro)
    srs_db.py                   programar_primera_revision, aplicar_sm2_y_guardar,
                                reviews_para_hoy, crear_flashcards_desde_errores,
                                estadisticas_estudiante
  views_srs.py                  repaso, estadisticas
  admin_srs.py                  FlashcardAdmin, ReviewAdmin
  management/commands/
    seed_srs.py                 35 flashcards de muestra
  templates/estudiante/srs/
    repaso.html                 sesion con botones Mal/Regular/Bien
    estadisticas.html           4 cards (total, pendientes, retencion, proxima)
  tests/
    test_services_srs.py        22 (SM-2 puro, sin BD)
    test_models_srs.py          7 (modelos, con BD)
    test_services_srs_db.py     20 (servicios con BD)
    test_views_srs.py           10 (vistas)
    test_seed_srs.py            4 (management command)

django_retorica/urls.py         /estudiante/srs/repaso/, /estudiante/srs/estadisticas/
```

---

## 3. Modelo de datos

### Flashcard

| Campo | Tipo | Notas |
|---|---|---|
| estudiante | FK AUTH_USER_MODEL CASCADE | related_name=flashcards |
| idioma | CharField(2) | ES, EN, LA |
| tipo | CharField(20) | vocabulario/declinacion/conjugacion/regla/redaccion |
| frente | TextField | "miles, militis" |
| reverso | TextField | "soldado (3a decl.)" |
| categoria_gramatical | CharField(100) | opcional |
| creado_en | DateTimeField auto_now_add | |

`unique_together = (estudiante, idioma, frente, tipo)`

### Review

| Campo | Tipo | Notas |
|---|---|---|
| flashcard | FK Flashcard CASCADE | related_name=reviews |
| programada_para | DateField db_index | fecha del proximo repaso |
| completada_en | DateTimeField null | null = pendiente |
| calidad_respuesta | IntegerField null | 0-5 |
| intervalo_dias | PositiveIntegerField | estado SM-2 |
| facilidad | FloatField default=2.5 | E-Factor SM-2 |
| repeticiones | PositiveIntegerField | estado SM-2 |

`ordering = [programada_para, id]` · property `pendiente = completada_en is None`

**Convencion clave**: cada Review es una sesion programada. Tras aplicar SM-2,
la Review actual se marca completada y se crea una NUEVA Review con el estado
actualizado. Esto da audit log gratis y el "current state" es el ultimo por
programada_para DESC.

---

## 4. Motor SM-2 puro (core/services/srs.py)

Funcion pura, sin BD. 100% testeable con SimpleNamespace.

`aplicar_sm2(review, calidad, hoy=None)`

Algoritmo:
- calidad 0-5 (0=fallo total, 5=perfecto)
- calidad < 3 -> reset: repeticiones=0, intervalo=1
- calidad >= 3:
  - repeticiones==0 -> intervalo=1
  - repeticiones==1 -> intervalo=6
  - repeticiones>=2 -> intervalo=round(intervalo * facilidad)
- facilidad = max(1.3, facilidad + delta)
  - delta = 0.1 - (5-q) * (0.08 + (5-q) * 0.02)
- programada_para = hoy + intervalo_dias

Funcion auxiliar:

`intervalo_estimado(intervalo_dias, facilidad, repeticiones, calidad) -> int`

Calcula sin mutar. Util para previsualizar.

---

## 5. Servicios con BD (core/services/srs_db.py)

### programar_primera_revision(flashcard, hoy=None) -> Review

Crea la primera Review con `programada_para=hoy`, `intervalo=0`, `facilidad=2.5`,
`repeticiones=0`. Idempotente: si ya hay una pendiente, la retorna.

### aplicar_sm2_y_guardar(review, calidad, hoy=None) -> Review

Aplica SM-2 in-place, marca `review.completada_en=now`, guarda, crea nueva
Review con el estado post-SM-2. Retorna la nueva.

### reviews_para_hoy(estudiante, hoy=None) -> QuerySet[Review]

Reviews pendientes: `completada_en=null`, `programada_para<=hoy`,
`flashcard__estudiante=estudiante`. Ordenadas por fecha + id.

### crear_flashcards_desde_errores(estudiante) -> list[Flashcard]

Lee `HistorialErrorSintactico.objects.filter(estudiante, resuelto=False)`.
Por cada error: `get_or_create` Flashcard con `tipo="redaccion"`,
`frente=patron_error`, `reverso=categoria_gramatical`. Programa review inicial
de las nuevas. Retorna todas las flashcards (nuevas o existentes).

### estadisticas_estudiante(estudiante, hoy=None) -> dict

```python
{
    "total_flashcards": int,
    "reviews_pendientes": int,
    "retencion_pct": float | None,   # None si no hay reviews completadas
    "proxima_revision": date | None,
}
```

Retencion = % de reviews con `calidad_respuesta >= 3`.

---

## 6. Vistas y URLs

```python
path('estudiante/srs/repaso/', views_srs.repaso, name='srs_repaso'),
path('estudiante/srs/estadisticas/', views_srs.estadisticas, name='srs_estadisticas'),
```

Prefijo `srs/` obligatorio. `estudiante/repaso/` y `estudiante/estadisticas/`
ya estaban registrados por otro modulo. Django resuelve por primer match, asi que
URLs sin namespace devolvian templates del otro modulo.

### repaso(request) - GET/POST

- GET: renderiza la primera Review pendiente o "todo al dia"
- POST: aplica SM-2 con calidad, redirige a si mismo (evita doble-submit)
- Requiere login (redirect a /login/?next=...)

### estadisticas(request) - GET

Llama `estadisticas_estudiante(request.user)`, renderiza 4 cards.

### Templates

- `estudiante/srs/repaso.html` - frente + botones Mal/Regular/Bien + detalles reverso
- `estudiante/srs/estadisticas.html` - 4 cards + links

Ambos extienden `estudiante/base.html`. Nota: el campo `proxima_revision` se
formatea con `|date:"Y-m-d"` para mostrar ISO en lugar del formato locale.

---

## 7. Admin (core/admin_srs.py)

FlashcardAdmin:
- list_display: id, estudiante, idioma, tipo, frente_corto, creado_en
- list_filter: idioma, tipo
- search: frente, reverso, estudiante__username
- date_hierarchy: creado_en

ReviewAdmin:
- list_display: id, flashcard, programada_para, pendiente, repeticiones, intervalo, facilidad
- list_filter: completada_en, programada_para
- search: flashcard__frente, flashcard__estudiante__username
- date_hierarchy: programada_para

---

## 8. Management command: seed_srs

```bash
python manage.py seed_srs <username>
```

Crea 35 flashcards de muestra para el usuario:
- 15 castellano (efimero, uberrimo, sagaz, prolijo, soslayar...)
- 10 ingles (serendipity, ephemeral, ubiquitous, meticulous, candid...)
- 10 latin (miles/militis, tempus/temporis, amo/amas/amare...)

Idempotente via `get_or_create`. Programa review inicial de cada nueva.
Muestra resumen: `Creadas: N | Existentes: M | Total de <user>: T`.

---

## 9. Tests (63 totales)

| Archivo | Tests |
|---|---|
| test_services_srs.py | 22 (SM-2 puro, sin BD) |
| test_models_srs.py | 7 (modelos) |
| test_services_srs_db.py | 20 (servicios con BD) |
| test_views_srs.py | 10 (vistas) |
| test_seed_srs.py | 4 (command) |
| **Total** | **63** |

Todos verdes. Cobertura del modulo SRS: ~99% (solo lineas de logging no cubiertas).

Casos cubiertos:
- SM-2: calidad 0-5, primera/segunda/tercera revision, reseteo, cadena
  monotonica, floor de facilidad 1.3, validacion 0-5, fecha default
- Modelos: str, unique_together, cascade, defaults
- Servicios: primera revision idempotente, aplicar y guardar cadena de 3,
  reviews filtran por estudiante y fecha, crear desde errores (vacio,
  3 errores, idempotente, ignora resueltos, programa review),
  estadisticas (vacio, con datos, retencion)
- Vistas: auth, todo al dia, con pendiente, POST calidad valida/invalida,
  estadisticas
- Command: 35 flashcards, idempotente, programa reviews, usuario inexistente

---

## 10. Commits

| Hash | Ronda | Contenido |
|---|---|---|
| 2a36b39 | R1 | Modelos Flashcard/Review + motor SM-2 puro + 29 tests |
| d500eea | R2 | Servicios con BD (5 funciones) + 20 tests |
| 1725925 | R3 | Vistas repaso/estadisticas + templates + 10 tests |
| d74e477 | R4 | Admin + management command seed_srs + 4 tests |

---

## 11. Decisiones tecnicas

1. **SM-2 puro separado de DB**: `srs.py` sin dependencias de BD, testea con
   SimpleNamespace. `srs_db.py` orquesta. Mismo patron que redaccion.

2. **Convencion de Review**: cada Review es una sesion programada. Tras aplicar
   SM-2, la actual queda completada y se crea una nueva. Audit log gratis.

3. **URLs namespaced**: `/estudiante/srs/...` en lugar de `/estudiante/...`
   para evitar colision con modulos existentes que ya registraban
   `estudiante/repaso/` y `estudiante/estadisticas/`.

4. **Ciclo adaptativo cerrado**: `crear_flashcards_desde_errores` conecta el
   modulo 4 (redaccion) con SRS. Errores -> flashcards -> repaso -> recalibracion.

5. **Management command en vez de fixture**: una fixture necesita user
   hardcodeado. Un command acepta username por argumento y es idempotente.

6. **Filtro `|date:"Y-m-d"`**: fuerza formato ISO en el template. Formato
   locale ("18 de octubre de 2026") hacia fallar los tests de proxima_revision.

7. **Facilidad floor 1.3**: SM-2 con facilidad menor implica intervalos
   demasiado cortos (ease hell). El floor evita ese patron.

---

## 12. Uso rapido

```bash
python manage.py migrate
python manage.py seed_srs <username>
python manage.py runserver
```

En el navegador:
- `/estudiante/srs/repaso/` -> sesion de repaso
- `/estudiante/srs/estadisticas/` -> metricas
- `/admin/core/flashcard/` -> gestion

En shell:

```python
from core.models import Flashcard, Review
from core.services.srs_db import (
    programar_primera_revision,
    aplicar_sm2_y_guardar,
    reviews_para_hoy,
    crear_flashcards_desde_errores,
    estadisticas_estudiante,
)

# Crear flashcard manualmente
fc = Flashcard.objects.create(
    estudiante=user, idioma="ES", tipo="vocabulario",
    frente="palabra", reverso="definicion",
)

# Programar repaso inicial
r = programar_primera_revision(fc)

# Aplicar SM-2 (bien)
nueva = aplicar_sm2_y_guardar(r, calidad=5)

# Pendientes hoy
for rev in reviews_para_hoy(user):
    print(rev.flashcard.frente)

# Convertir errores de redaccion a flashcards
crear_flashcards_desde_errores(user)

# Estadisticas
print(estadisticas_estudiante(user))
```

---

*Ultima actualizacion: 2026-10-18 tras R4 (d74e477).*