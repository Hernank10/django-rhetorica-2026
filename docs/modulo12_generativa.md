# Modulo 12: Gramatica generativa transformacional — 100 tecnicas

**Ultima actualizacion:** 2026-10-26
**Version:** v1.5.0
**Tests:** 8 (models + views)
**Tecnicas:** 100 (bloques A-G)
**Rango:** 101-200

---

## 1. Vision general

Un curso avanzado de **gramatica generativa transformacional (GGT)** segun el modelo de Noam Chomsky. Cubre desde los fundamentos (competencia, Gramatica Universal, principios y parametros, EP/ES) hasta el Programa Minimalista (Merge, Move, Agree, LF, PF) y aplicaciones al castellano.

**Audiencia:** estudiantes de linguistica, filologos, interesados en sintaxis formal. No es un curso para aprender a hablar castellano, sino para entender como funciona el lenguaje desde la teoria generativa.

Cada una de las **100 tecnicas** es una unidad didactica con teoria, explicacion, regla, ejemplos y ejercicio.

---

## 2. Los 7 bloques

| Bloque | Tecnicas | Contenido | Cantidad |
|--------|----------|-----------|----------|
| **A** | 101-115 | Fundamentos GGT (competencia, GU, principios, EP/ES) | 15 |
| **B** | 116-130 | Estructura X-barra (SN, SV, SP, SA, SAdv, SC, ST, SD) | 15 |
| **C** | 131-150 | Transformaciones (movimiento, huella, islas, ciclicidad) | 20 |
| **D** | 151-165 | Caso y papeles tematicos | 15 |
| **E** | 166-180 | Reccion y ligamiento (Principios A/B/C, PRO) | 15 |
| **F** | 181-190 | Programa minimalista (Merge, Move, Agree, LF, PF) | 10 |
| **G** | 191-200 | Aplicaciones al castellano (SVO, pro-drop, cliticos) | 10 |
| **Total** | | | **100** |

### 2.1 Bloque A — Fundamentos (101-115)

Competencia vs actuacion, Gramatica Universal, principios y parametros, estructura profunda vs superficial, reglas de reescritura, recursividad, ambiguedad estructural, gramaticalidad vs aceptabilidad, asterisco, categorias lexicas vs funcionales, nucleo/complemento/especificador, proyeccion maxima, principio de proyeccion.

### 2.2 Bloque B — X-barra (116-130)

Teoria X-barra (X0, X', XP), sintagmas (SN, SV, SP, SA, SAdv, SC, ST, SD), nucleos funcionales T (Tiempo), C (Complementante), D (Determinante), concordancia, estructura de oracion simple (ST) y compuesta (SC), diagrama arboreo.

### 2.3 Bloque C — Transformaciones (131-150)

Transformacion, movimiento-alfa, huella y cadena, movimiento V->T y sujeto->ST, movimiento-qu (interrogativas y relativas), movimiento de nucleo y de constituyentes, restriccion de isla, principio de subyacencia, sujeto complejo, mov-A vs mov-A-barra, do-support, borrado, elipsis verbal, pro-drop, topicalizacion, focalizacion, dislocacion a la izquierda.

### 2.4 Bloque D — Caso y papeles tematicos (151-165)

Caso abstracto vs morfologico, nominativo (T), acusativo (V), dativo (V/P), genitivo (N), asignacion por T/V/P, filtro de caso, papeles tematicos (agente, tema/paciente, meta/origen/locativo), criterio tematico, estructura argumental, inacusativos vs inergativos.

### 2.5 Bloque E — Reccion y ligamiento (166-180)

Reccion, mando-c, principios A/B/C del ligamiento, se reflexivo, si mismo, pronombres y correferencia, PRO y control, sujeto tacito, restricciones castellano, reccion de nucleo/especificador, concordancia.

### 2.6 Bloque F — Minimalismo (181-190)

Del modelo PP al minimalismo, Merge, Move, Agree, rasgos formales (interpretables vs no interpretables), economia y ultima instancia, interfaz PF (fonetica) y LF (logica), derivacion minimalista.

### 2.7 Bloque G — Aplicaciones al castellano (191-200)

Orden SVO/VSO/VOS, pro-drop, movimiento del verbo (V->T), cliticos, doble negacion, ser vs estar, subordinadas sustantivas/relativas/interrogativas, analisis generativo completo.

---

## 3. Tipos de ejercicio

En el modulo 12 predominan:

| Tipo | Nombre | Cantidad | Ejemplo |
|------|--------|----------|---------|
| 1 | Opcion multiple con justificacion | 99 | "Cual es el nucleo del SN?" |
| 3 | Clasificacion | 1 | "Clasifica: categoria lexica vs funcional" |

Tipo 1 dominante. Tecnica 12 (categorias lexicas vs funcionales) usa tipo 3.

---

## 4. Modelos de datos

### 4.1 TecnicaGramatical (100 registros)

Modelo compartido con modulos 11, 13, 14 (mismo modelo, distinto campo modulo):

    class TecnicaGramatical(models.Model):
        numero = models.IntegerField(unique=True)   # 101-200
        bloque = models.CharField(max_length=1)     # A-G
        titulo = models.CharField(max_length=200)
        teoria = models.TextField()
        explicacion = models.TextField()
        regla = models.TextField()
        ejemplo_correcto = models.TextField()
        ejemplo_incorrecto = models.TextField()
        nivel = models.CharField(...)               # basico | intermedio | avanzado
        modulo = models.CharField(...)              # "generativa"

Migracion: 0020_add_modulo_tecnica.

### 4.2 EjercicioGramatical (100 registros)

    class EjercicioGramatical(models.Model):
        tecnica = models.ForeignKey(TecnicaGramatical, related_name="ejercicios")
        tipo = models.IntegerField(choices=...)     # 1-5
        orden = models.IntegerField(default=1)
        payload = models.JSONField()

### 4.3 ProgresoGramatical

Igual que otros modulos: usuario + tecnica (unique), intentos, aciertos_consecutivos, estado, SM-2.

---

## 5. Motor de evaluacion

**Archivo:** core/services/gramatica.py (wrapper sobre sintaxis.py)

Reutiliza el motor del modulo 10. Cero duplicacion. Cualquier mejora beneficia a los 5 modulos curriculares.

### 5.1 API publica

    def evaluar_ejercicio(ejercicio, respuesta, usuario=None)
    def actualizar_progreso(usuario, tecnica, ejercicio, ok)
    def proximas_revisiones(usuario, n=5, modulo=None)
    def resumen_progreso(usuario, modulo=None)

### 5.2 Mastery

Igual que en sintaxis: 3 aciertos consecutivos + ultimo en tipo 4/5 = dominada.

---

## 6. Vistas y endpoints

**Archivo:** core/views_gramatica.py + core/urls_gramatica.py

| URL | Metodo | Vista | Proposito |
|-----|--------|-------|-----------|
| /gramatica/generativa/ | GET | indice_generativa | Grid 100 tecnicas por bloque |
| /gramatica/tecnica/<n>/ | GET | tecnica | Detalle compartido con otros modulos |
| /gramatica/evaluar/ | POST | evaluar_ajax | Evaluacion + SM-2 |
| /gramatica/generativa/progreso/ | GET | progreso | Heatmap + proximas revisiones |
| /gramatica/ajax/contador/?modulo=generativa | GET | contador_ajax | Badge |

La vista tecnica es compartida. Para tecnicas del modulo 12 (101-200) el bloque_nombre viene de BLOQUES_GENERATIVA dict:

    BLOQUES_GENERATIVA = {
        "A": "Fundamentos de la GGT",
        "B": "Estructura X-barra",
        "C": "Transformaciones",
        "D": "Caso y papeles tematicos",
        "E": "Reccion y ligamiento",
        "F": "Programa minimalista",
        "G": "Aplicaciones al castellano",
    }

---

## 7. Frontend

### 7.1 Templates

- core/gramatica/indice.html — compartido con condicional es_generativa
- core/gramatica/tecnica.html — compartido con es_generativa flag
- core/gramatica/progreso.html — compartido con modulo=generativa

### 7.2 JavaScript

static/js/gramatica.js incluye badge para generativa (fetch a /gramatica/ajax/contador/?modulo=generativa).

---

## 8. Integracion con el LMS

### 8.1 Navbar

En core/templates/core/base.html, link "Generativa 100" con icono sitemap y badge amarillo.

### 8.2 Card en dashboard estudiante

Card azul con resumen + boton "Ver las 100 tecnicas" y "Empezar por la 101".

### 8.3 Notificaciones

Al dominar una tecnica -> notificacion tipo "logro", idempotente por referencia generativa_tecnica_{numero}_{user_id}.

---

## 9. Seed de las 100 tecnicas

**Archivo data:** core/data/tecnicas_generativa.py
**Archivo loader:** scripts/seed_generativa.py

Estructura:

    TECNICAS = [{"numero": 101, "bloque": "A", "modulo": "generativa", ...}, ...]
    EJERCICIOS = {101: [{"tipo": 1, "orden": 1, "payload": {...}}], ...}

**Idempotencia:** update_or_create por numero. **Aislamiento:** filtra por modulo="generativa". Correr N veces no duplica.

**Distribucion por tipo:** 99 tipo 1 + 1 tipo 3 (tecnica 12).

**Nota historica:** en v1.5.0 las tecnicas se renumeraron de 1-100 a 101-200 para evitar colision con gramatica (1-100). Bug corregido en commit `b134a2c`.

---

## 10. Tests

| Archivo | Tests | Cobertura |
|---------|-------|-----------|
| test_generativa_models.py | 4 | Modelos, data, seed idempotente, 15 tecnicas |
| test_generativa_views.py | 4 | Indice, filtro, progreso, contador por modulo |

Total: 8 tests. Los tests usan `len(TECNICAS)` dinamico, no hardcodean el total.

Ejecutar:

    python -m pytest core/tests/test_generativa_models.py core/tests/test_generativa_views.py -v

---

## 11. Decisiones tecnicas

### 11.1 Renumeracion 101-200

**Decision:** tecnicas generativas van de 101 a 200 (no de 1 a 100).

**Por que:** en v1.5.0 inicial se usaron numeros 1-100, lo que sobrescribio tecnicas de gramatica castellana. Fix en `b134a2c`: renumeradas a 101-200. Leccion aprendida: cada modulo tiene su rango fijo.

### 11.2 Modelo compartido

**Decision:** TecnicaGramatical compartido con gramatica, A1, B1.

**Por que:** misma estructura. Campo modulo distingue. Tabla separada = 4x mantenimiento.

### 11.3 Claves ASCII en data

**Decision:** claves en ASCII, valores con tildes.

**Por que:** bug en v1.5.2 (tildes en claves rompieron seed). Claves ASCII, valores libres.

---

## 12. Estado actual

| Aspecto | Estado |
|---------|--------|
| 100 tecnicas | OK |
| 100 ejercicios (99 tipo 1 + 1 tipo 3) | OK |
| Motor reutilizado | OK |
| SM-2 + mastery | OK |
| UI (indice + tecnica + progreso) | OK |
| AJAX evaluacion | OK |
| Notificaciones al dominar | OK |
| Navbar + dashboard | OK |
| Tests (8) | OK |
| Renumeracion 101-200 | OK (fix v1.5.0) |
| Deploy productivo | Pendiente |
| Mas ejercicios 4/5 | Pendiente |

**Tag:** v1.5.0 (2026-10-24)
**Repo:** github.com/Hernank10/django-rhetorica-2026

---

Documento del modulo 12: gramatica generativa transformacional. 100 tecnicas (101-200), bloques A-G, motor reutilizado. 8 tests.