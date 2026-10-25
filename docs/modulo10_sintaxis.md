# Módulo 10: Sintaxis del castellano — 100 técnicas

**Última actualización:** 2026-10-24
**Versión:** v1.3.1
**Cobertura:** 97.19%
**Tests:** 57 (models + engine + views)

---

## 1. Visión general

Un curso autocontenido de **sintaxis oracional del castellano** que enseña a escribir correctamente oraciones simples y compuestas. Cada una de las **100 técnicas** es una unidad didáctica con:

- **Teoría** (1-2 párrafos con la regla)
- **Explicación** (por qué funciona, qué pasa si se viola)
- **Ejemplo correcto** e **incorrecto** contrastados
- **Ejercicio interactivo** de uno de 5 tipos
- **Retroalimentación inmediata**
- **Seguimiento SM-2 + mastery** hasta dominar las 100

**Principio pedagógico:** no se avanza a la siguiente técnica hasta 3 aciertos consecutivos en el ejercicio más difícil.

**No cubre:** morfología (módulo 1), redacción general (módulo 4), literatura/retórica (módulos 2 y 8).

---

## 2. Los 7 bloques de las 100 técnicas

| Bloque | Técnicas | Contenido | Cantidad |
|--------|----------|-----------|----------|
| **A** | 1-20 | Oración simple | 20 |
| **B** | 21-35 | Concordancia y régimen | 15 |
| **C** | 36-55 | Coordinación | 20 |
| **D** | 56-70 | Subordinación sustantiva | 15 |
| **E** | 71-80 | Subordinación adjetiva | 10 |
| **F** | 81-90 | Subordinación adverbial | 10 |
| **G** | 91-100 | Yuxtaposición y puntuación | 10 |
| **Total** | | | **100** |

### 2.1 Bloques A-B: fundamentos

- **A. Oración simple (1-20):** sujeto/predicado, concordancia, impersonales, pasiva refleja, CD/CI, CCs, atributo vs predicativo, voz pasiva.
- **B. Concordancia y régimen (21-35):** artículo-sustantivo, adjetivo-sustantivo, género ambiguo, régimen preposicional, dequeísmo/queísmo, sino/si no, porque/por qué, adonde, conque, también/tan bien, demás/de más, apenas, entorno, aparte.

### 2.2 Bloques C-G: oraciones compuestas

- **C. Coordinación (36-55):** y/e, ni, pero, sino, sin embargo, o/u, ya...ya, bien...bien, es decir, o sea, mas, comas antes de pero/sino/o, yuxtaposición con `;` y `:`.
- **D. Subordinación sustantiva (56-70):** sujeto, CD, CI, régimen, atributo, aposición, que conj/relativo, si cond/interr, estilo directo/indirecto, correlación temporal, infinitivo, "el hecho de que".
- **E. Subordinación adjetiva (71-80):** relativos que, quien, el cual, cuyo, donde, cuando, como; explicativa vs especificativa.
- **F. Subordinación adverbial (81-90):** temporal, causal, final, condicional, concesiva.
- **G. Yuxtaposición y puntuación (91-100):** coma, `;`, `:`, comillas, raya, paréntesis, puntos suspensivos, análisis completo.

---

## 3. Los 5 tipos de ejercicio

| Tipo | Nombre | Cantidad | Ejemplo |
|------|--------|----------|---------|
| 1 | Selección múltiple + justificación | 39 | "¿Cuál oración concuerda?" |
| 2 | Corrección inline | 40 | "Corrige la oración" |
| 3 | Clasificación | 10 | "Clasifica: CCL, CCT" |
| 4 | Construcción guiada | 3 | "Une A + conector + B" |
| 5 | Detección de error | 8 | "Señala el error y la regla" |

### 3.1 Tipo 1 — Selección con justificación

Payload: `enunciado` + `opciones` (id, texto, correcta, razon) + `justificacion_obligatoria` + `regla`.

**Evaluación:** elige opción **y** escribe razón. Compara con `razon` usando fuzzy ≥ 0.5.

### 3.2 Tipo 2 — Corrección inline

Payload: `oracion_incorrecta` + `respuesta_correcta` + `regla`.

**Evaluación:** exact match normalizado (sin acentos) o fuzzy ≥ 0.85 (variante válida).

### 3.3 Tipo 3 — Clasificación

Payload: `oraciones` (texto, categoria_correcta) + `categorias`.

**Evaluación:** compara cada oración individualmente. Feedback: `X/Y correctas`.

### 3.4 Tipo 4 — Construcción guiada

Payload: `oracion_a` + `oracion_b` + `conector` + `respuesta_correcta` + `regla`.

**Evaluación (3 pasos):**
1. Exact match normalizado.
2. Conector como palabra separada (`\bconector\b`).
3. Fuzzy ≥ 0.85 contra `respuesta_correcta`.

> **Nota:** no se valida `oracion_a`/`oracion_b` como substring porque el verbo cambia de número (viene → vienen).

### 3.5 Tipo 5 — Detección de error

Payload: `oracion` + `error_posicion` + `regla_violada` + `reglas_posibles`.

**Evaluación:** posición + regla deben coincidir exactamente.

---

# Módulo 10: Sintaxis del castellano — 100 técnicas

**Última actualización:** 2026-10-24
**Versión:** v1.3.1
**Cobertura:** 97.19%
**Tests:** 57 (models + engine + views)

---

## 1. Visión general

Un curso autocontenido de **sintaxis oracional del castellano** que enseña a escribir correctamente oraciones simples y compuestas. Cada una de las **100 técnicas** es una unidad didáctica con:

- **Teoría** (1-2 párrafos con la regla)
- **Explicación** (por qué funciona, qué pasa si se viola)
- **Ejemplo correcto** e **incorrecto** contrastados
- **Ejercicio interactivo** de uno de 5 tipos
- **Retroalimentación inmediata**
- **Seguimiento SM-2 + mastery** hasta dominar las 100

**Principio pedagógico:** no se avanza a la siguiente técnica hasta 3 aciertos consecutivos en el ejercicio más difícil.

**No cubre:** morfología (módulo 1), redacción general (módulo 4), literatura/retórica (módulos 2 y 8).

---

## 2. Los 7 bloques de las 100 técnicas

| Bloque | Técnicas | Contenido | Cantidad |
|--------|----------|-----------|----------|
| **A** | 1-20 | Oración simple | 20 |
| **B** | 21-35 | Concordancia y régimen | 15 |
| **C** | 36-55 | Coordinación | 20 |
| **D** | 56-70 | Subordinación sustantiva | 15 |
| **E** | 71-80 | Subordinación adjetiva | 10 |
| **F** | 81-90 | Subordinación adverbial | 10 |
| **G** | 91-100 | Yuxtaposición y puntuación | 10 |
| **Total** | | | **100** |

### 2.1 Bloques A-B: fundamentos

- **A. Oración simple (1-20):** sujeto/predicado, concordancia, impersonales, pasiva refleja, CD/CI, CCs, atributo vs predicativo, voz pasiva.
- **B. Concordancia y régimen (21-35):** artículo-sustantivo, adjetivo-sustantivo, género ambiguo, régimen preposicional, dequeísmo/queísmo, sino/si no, porque/por qué, adonde, conque, también/tan bien, demás/de más, apenas, entorno, aparte.

### 2.2 Bloques C-G: oraciones compuestas

- **C. Coordinación (36-55):** y/e, ni, pero, sino, sin embargo, o/u, ya...ya, bien...bien, es decir, o sea, mas, comas antes de pero/sino/o, yuxtaposición con `;` y `:`.
- **D. Subordinación sustantiva (56-70):** sujeto, CD, CI, régimen, atributo, aposición, que conj/relativo, si cond/interr, estilo directo/indirecto, correlación temporal, infinitivo, "el hecho de que".
- **E. Subordinación adjetiva (71-80):** relativos que, quien, el cual, cuyo, donde, cuando, como; explicativa vs especificativa.
- **F. Subordinación adverbial (81-90):** temporal, causal, final, condicional, concesiva.
- **G. Yuxtaposición y puntuación (91-100):** coma, `;`, `:`, comillas, raya, paréntesis, puntos suspensivos, análisis completo.

---

## 3. Los 5 tipos de ejercicio

| Tipo | Nombre | Cantidad | Ejemplo |
|------|--------|----------|---------|
| 1 | Selección múltiple + justificación | 39 | "¿Cuál oración concuerda?" |
| 2 | Corrección inline | 40 | "Corrige la oración" |
| 3 | Clasificación | 10 | "Clasifica: CCL, CCT" |
| 4 | Construcción guiada | 3 | "Une A + conector + B" |
| 5 | Detección de error | 8 | "Señala el error y la regla" |

### 3.1 Tipo 1 — Selección con justificación

Payload: `enunciado` + `opciones` (id, texto, correcta, razon) + `justificacion_obligatoria` + `regla`.

**Evaluación:** elige opción **y** escribe razón. Compara con `razon` usando fuzzy ≥ 0.5.

### 3.2 Tipo 2 — Corrección inline

Payload: `oracion_incorrecta` + `respuesta_correcta` + `regla`.

**Evaluación:** exact match normalizado (sin acentos) o fuzzy ≥ 0.85.

### 3.3 Tipo 3 — Clasificación

Payload: `oraciones` + `categorias`.

**Evaluación:** compara cada oración individualmente. Feedback: `X/Y correctas`.

### 3.4 Tipo 4 — Construcción guiada

Payload: `oracion_a` + `oracion_b` + `conector` + `respuesta_correcta`.

**Evaluación:**
1. Exact match normalizado.
2. Conector como palabra separada (`\bconector\b`).
3. Fuzzy ≥ 0.85 contra `respuesta_correcta`.

> No se valida `oracion_a`/`oracion_b` como substring porque el verbo cambia de número (viene → vienen).

### 3.5 Tipo 5 — Detección de error

Payload: `oracion` + `error_posicion` + `regla_violada` + `reglas_posibles`.

**Evaluación:** posición + regla deben coincidir exactamente.

---

## 4. Modelos de datos

### 4.1 TecnicaSintactica (100 registros)

```python
class TecnicaSintactica(models.Model):
    numero = models.PositiveSmallIntegerField(unique=True)
    bloque = models.CharField(max_length=1, choices=BLOQUES, db_index=True)
    titulo = models.CharField(max_length=200)
    teoria = models.TextField()
    explicacion = models.TextField()
    regla = models.CharField(max_length=200)
    ejemplo_correcto = models.TextField()
    ejemplo_incorrecto = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVELES, default="basico")




## Migración: 0018_add_sintaxis.

## 4.2 EjercicioTecnica (100 registros)
python
class EjercicioTecnica(models.Model):
    tecnica = models.ForeignKey(TecnicaSintactica, on_delete=models.CASCADE,
                                related_name="ejercicios")
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)  # 1-5
    payload = models.JSONField()
    orden = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ("tecnica", "orden")
## 4.3 ProgresoTecnica (1 por usuario × técnica)
python
class ProgresoTecnica(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tecnica = models.ForeignKey(TecnicaSintactica, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default="no_iniciada")
    aciertos_consecutivos = models.PositiveSmallIntegerField(default=0)
    intentos = models.PositiveSmallIntegerField(default=0)
    ultima_revision = models.DateTimeField(null=True)
    proxima_revision = models.DateTimeField(null=True, db_index=True)
    sm2_ef = models.FloatField(default=2.5)
    sm2_interval = models.PositiveIntegerField(default=0)
    sm2_repetitions = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ("usuario", "tecnica")
## 5. Motor de evaluación
Archivo: core/services/sintaxis.py

## 5.1 API pública
python
def evaluar_ejercicio(ejercicio, respuesta, usuario=None) -> dict:
    """Retorna {"ok", "feedback", "regla", "ejemplo_correcto"}."""

def actualizar_progreso(usuario, tecnica, ejercicio, ok) -> ProgresoTecnica:
    """Actualiza SM-2 + mastery + notificación al dominar."""

def proximas_revisiones(usuario, n=5) -> QuerySet:
    """Técnicas con proxima_revision <= now."""

def resumen_progreso(usuario) -> dict:
    """{total, iniciadas, dominadas}."""
## 5.2 Helpers
python
def _normalizar(texto) -> str:
    """Lowercase + trim + sin acentos + sin puntuación."""

def _fuzzy_match(a, b) -> float:
    """SequenceMatcher ratio 0.0-1.0."""
## 5.3 SM-2 simplificado
python
def _actualizar_sm2(progreso, calidad):
    """calidad: 0-5."""
    ef = progreso.sm2_ef
    ef = ef + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02))
    progreso.sm2_ef = max(1.3, ef)

    if calidad < 3:
        progreso.sm2_repetitions = 0
        progreso.sm2_interval = 1
    else:
        progreso.sm2_repetitions += 1
        if progreso.sm2_repetitions == 1:
            progreso.sm2_interval = 1
        elif progreso.sm2_repetitions == 2:
            progreso.sm2_interval = 6
        else:
            progreso.sm2_interval = round(progreso.sm2_interval * progreso.sm2_ef)

    progreso.proxima_revision = timezone.now() + timedelta(days=progreso.sm2_interval)
Calidad: fallo → 1; acierto tipo 1/2/3 → 3; acierto tipo 4/5 → 4.

## 5.4 Mastery
python
if progreso.aciertos_consecutivos >= 3 and ejercicio.tipo in (4, 5) and ok:
    progreso.estado = "dominada"
Justificación: tipos 1-3 son reconocimiento; 4-5 son producción.

## 5.5 Notificación al dominar
python
if progreso.estado == "dominada" and estado_anterior != "dominada":
    try:
        crear_notificacion(
            user=usuario, tipo="logro",
            titulo=f"Tecnica {tecnica.numero} dominada",
            mensaje=f"'{tecnica.titulo}' superada",
            url_destino=f"/sintaxis/tecnica/{tecnica.numero}/",
            icono="star",
            referencia=f"sintaxis_tecnica_{tecnica.numero}_{usuario.id}",
        )
    except Exception:
        pass
Idempotente por referencia. Envuelto en try/except.

## 6. Vistas y endpoints
Archivo: core/views_sintaxis.py + core/urls_sintaxis.py

URL	Método	Vista	Propósito
/sintaxis/	GET	indice	Grid 100 técnicas
/sintaxis/tecnica/<n>/	GET	tecnica	Flashcard + ejercicio
/sintaxis/evaluar/	POST	evaluar_ajax	Evaluar + SM-2
/sintaxis/progreso/	GET	progreso	Heatmap + próximas
/sintaxis/ajax/contador/	GET	contador_ajax	Badge
Todas con @login_required. evaluar_ajax con @require_POST.

## 7. Frontend
## 7.1 Templates
core/sintaxis/indice.html: header stats + 7 cards (uno por bloque). Color: gris (no iniciada), azul (en progreso), verde (dominada).

core/sintaxis/tecnica.html: flashcard + ejercicio + navegación.

core/sintaxis/progreso.html: stats + próximas (SM-2) + dominadas.

## 7.2 JavaScript
static/js/sintaxis.js (4 KB):

Evaluación AJAX: lee respuesta, POST a /sintaxis/evaluar/.

Badge navbar: fetch /sintaxis/ajax/contador/ cada 60s.

## 8. Integración con el LMS
8.1 Navbar
html
<li class="nav-item">
  <a class="nav-link" href="{% url 'sintaxis:indice' %}">
    <i class="fas fa-pen-fancy"></i> Sintaxis 100
    <span id="sintaxis-badge" class="badge bg-success" style="display:none;">0</span>
  </a>
</li>
8.2 Card en dashboard estudiante
Card verde al final con resumen + botón "Ver las 100 técnicas".

8.3 Notificaciones
Notif tipo logro al dominar, idempotente. Aparece en campana, /notificaciones/, y dashboard.

## 9. Seed de las 100 técnicas
Archivo: core/data/tecnicas_sintaxis.py + scripts/seed_tecnicas_sintaxis.py

## Estructura:

python
TECNICAS = [{"numero": 1, "bloque": "A", ...}, ...]  # 100 items
EJERCICIOS = {1: [{"tipo": 1, "orden": 1, "payload": {...}}], ...}
Idempotencia: update_or_create por numero y (tecnica, orden).

Distribución: 39 tipo 1, 40 tipo 2, 10 tipo 3, 3 tipo 4, 8 tipo 5.

Falta: más ejercicios tipo 3 y 4.

## 10. Tests (57 totales)
Archivo	Tests	Cobertura
test_sintaxis_models.py	14	Modelos, data, seed
test_sintaxis_engine.py	31	5 evaluadores + SM-2 + mastery
test_sintaxis_views.py	12	Vistas GET/POST/403/404
Ejecutar:

## powershell
pytest core/tests/test_sintaxis_*.py -v
Cobertura motor: ~95%. Global: 97.19%.

## 11. Decisiones técnicas
11.1 Determinismo vs LLM
Decisión: motor determinista (reglas + fuzzy), no LLM.

Por qué: reproducibilidad, explicabilidad, costo cero, latencia predecible.
Trade-off: respuesta válida no contemplada → rechazada. Mitigación: fuzzy ≥ 0.85.

11.2 Fuzzy match contra respuesta canónica
Por qué: múltiples formas válidas de expresar lo mismo.
Umbrales: tipo 1 → 0.5; tipo 2 → 0.85; tipo 4 → 0.85 + conector como palabra.

11.3 Conector como palabra separada
Problema: "Juan Pedro vienen" sin "y" tenía fuzzy 0.79.
Solución: validar \bconector\b antes del fuzzy.

11.4 Mastery solo con tipos 4-5
Por qué: tipos 1-3 = reconocimiento; 4-5 = producción.

11.5 Emoji no FontAwesome
Por qué: el navbar oculta iconos FontAwesome en ciertos contextos.

## 12. Roadmap / Deuda técnica
Completado (v1.3.1)
100 técnicas A-G

100 ejercicios (5 tipos)

Motor determinista

SM-2 + mastery

5 vistas + templates + JS

Integración navbar + dashboard

Notificaciones al dominar

57 tests, cobertura 97.19%

## Pendiente
Más ejercicios tipo 3 y 4

Re-incluir sintaxis en seed de notificaciones

Modo repaso puro

Exportar progreso (PDF/CSV)

Ranking de técnicas difíciles

## Deuda
Tipos 3 y 4 infrarrepresentados

Fuzzy match puede dar falsos positivos

Sin revisión humana

Sin tests E2E

13. Métricas de uso (post-deploy)
% técnicas dominadas por usuario

Tiempo medio por técnica

Tasa de acierto por tipo

Tasa de abandono en técnica N

Correlación mastery ↔ nota

Sin tracking implementado. Próxima iteración con django-prometheus.

## 14. Referencias
Beck, K. (2002). Test-Driven Development: By Example. Addison-Wesley.

Nivre, J., et al. (2020). Universal Dependencies v2. LREC 2020.

Woźniak, P. A., & Gorzelanczyk, E. J. (1994). Optimization of repetition spacing. Acta Neurobiologiae Experimentalis, 54(1), 59-62.

RAE & ASALE (2009). Nueva gramática de la lengua española. Espasa.

RAE (2010). Ortografía de la lengua española. Espasa.

## 15. Reproducir el módulo
powershell
# 1. Migración
E:\PythonPortable_Django5\python.exe manage.py migrate

# 2. Seed
E:\PythonPortable_Django5\python.exe scripts\seed_tecnicas_sintaxis.py

# 3. Verificar (→ 100)
E:\PythonPortable_Django5\python.exe manage.py shell -c "from core.models_sintaxis import TecnicaSintactica; print(TecnicaSintactica.objects.count())"

# 4. Tests (→ 57 passed)
E:\PythonPortable_Django5\python.exe -m pytest core/tests/test_sintaxis_*.py -v

# 5. Navegar
E:\PythonPortable_Django5\python.exe manage.py runserver 8000
# → http://127.0.0.1:8000/sintaxis/
## 16. Estado actual
Aspecto	Estado
100 técnicas	Completo
5 tipos de ejercicio	Completo (distribución a mejorar)
Motor determinista	Completo
SM-2 + mastery	Completo
UI (indice + tecnica + progreso)	Completo
AJAX evaluación	Completo
Notificaciones al dominar	Completo
Navbar + dashboard	Completo
Tests (57)	Completo
Cobertura 97.19%	Completo
Deploy productivo	Pendiente
Seed notif integrado	Pendiente
Más ejercicios 3/4	Pendiente
Tag: v1.3.1 (2026-10-24)
Repo: github.com/Hernank10/django-rhetorica-2026