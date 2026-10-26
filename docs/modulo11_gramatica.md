# Modulo 11: Gramatica castellana — 100 tecnicas

**Ultima actualizacion:** 2026-10-26
**Version:** v1.4.0
**Tests:** 18 (models + views)
**Tecnicas:** 100 (bloques A-G)
**Rango:** 1-100

---

## 1. Vision general

Un curso autocontenido de **gramatica normativa del castellano** para hablantes nativos que quieren consolidar las reglas de la RAE. Cubre desde la historia de la gramatica hasta la ortografia RAE 2010, pasando por morfologia, sustantivo, adjetivo, verbo, pronombres y determinantes.

Cada una de las **100 tecnicas** es una unidad didactica con teoria, explicacion, regla, ejemplos correcto/incorrecto, ejercicio interactivo y seguimiento SM-2 + mastery.

**Principio pedagogico:** no se avanza a la siguiente tecnica hasta dominar la actual con 3 aciertos consecutivos.

**Diferencia con modulo 10 (sintaxis):** modulo 10 enfoca construir oraciones correctas; modulo 11 enfoca las normas gramaticales y ortograficas del castellano (RAE 2010).

---

## 2. Los 7 bloques

| Bloque | Tecnicas | Contenido | Cantidad |
|--------|----------|-----------|----------|
| **A** | 1-15 | Historia de la gramatica castellana | 15 |
| **B** | 16-35 | Clases de palabras + morfologia | 20 |
| **C** | 36-50 | El sustantivo (genero, numero, clasificacion) | 15 |
| **D** | 51-60 | El adjetivo (grados, concordancia) | 10 |
| **E** | 61-80 | El verbo (fundamentos, tiempos, modos, tipos) | 20 |
| **F** | 81-90 | Pronombres y determinantes | 10 |
| **G** | 91-100 | Ortografia RAE 2010 | 10 |
| **Total** | | | **100** |

### 2.1 Bloque A — Historia (1-15)

Panorama historico: glosas emilianenses y silenses, Alfonso X el Sabio, Nebrija (1492, primera gramatica del castellano), la RAE (1713), Bello, Nueva gramatica (2009) y Ortografia (2010).

### 2.2 Bloque B — Clases de palabras (16-35)

Variables vs invariables, lexicas vs gramaticales, simples/derivadas/compuestas, patrimoniales vs cultismos, derivacion, composicion, parasintesis, prefijos, sufijos, morfemas, alomorfos.

### 2.3 Bloque C — El sustantivo (36-50)

Genero (masculino/femenino, casos especiales como el agua/la mano), numero (singular/plural, invariables), clasificacion (comun/propio, concreto/abstracto, contable/incontable, individual/colectivo), sustantivacion.

### 2.4 Bloque D — El adjetivo (51-60)

Concordancia, grados (positivo, comparativo, superlativo), una y dos terminaciones, posicion (antepuesto/pospuesto), sustantivacion, relacionales vs calificativos.

### 2.5 Bloque E — El verbo (61-80)

El bloque mas extenso: fundamentos (regulares/irregulares, 3 conjugaciones, persona/numero, presente, preterito simple), tiempos (imperfecto, perfecto compuesto, pluscuamperfecto, futuro, condicional), modos y aspecto (indicativo, subjuntivo, imperativo, perfectivo/imperfectivo, voz activa/pasiva), tipos (copulativos, transitivos/intransitivos, pronominales, perifrasis, irregulares frecuentes).

### 2.6 Bloque F — Pronombres y determinantes (81-90)

Tonicos vs atonos, leismo/laismo/loismo, demostrativos, posesivos, relativos (que, quien, cual, cuyo), interrogativos, determinantes demostrativos/posesivos/numerales.

### 2.7 Bloque G — Ortografia RAE 2010 (91-100)

Uso de b/v, c/z/s (seseo/ceceo), g/j, h, ll/y, m antes de p/b, acentuacion (agudas/llanas/esdrujulas), acento diacritico, diptongos/triptongos/hiatos, puntuacion RAE 2010.

---

## 3. Tipos de ejercicio

Cada tecnica tiene al menos 1 ejercicio. En el modulo 11 predominan:

| Tipo | Nombre | Cantidad | Ejemplo |
|------|--------|----------|---------|
| 1 | Opcion multiple con justificacion | 95 | "Cual es la forma correcta?" |
| 3 | Clasificacion | 5 | "Clasifica: aguda, llana, esdrujula" |

Payload tipico de tipo 1:

{
  "tipo": 1,
  "orden": 1,
  "payload": {
    "enunciado": "Cual es la forma correcta del verbo ir en 1a persona presente?",
    "opciones": [
      {"id": "a", "texto": "vo", "correcta": false, "razon": "Ir es irregular: voy."},
      {"id": "b", "texto": "voy", "correcta": true, "razon": "Irregular frecuente: voy."},
      {"id": "c", "texto": "ibo", "correcta": false, "razon": "No existe."}
    ],
    "justificacion_obligatoria": false,
    "regla": "Ir: voy"
  }
}

---

## 4. Modelos de datos

### 4.1 TecnicaGramatical (100 registros)

Modelo compartido con modulos 12-14 (mismo modelo, distinto campo modulo):

    class TecnicaGramatical(models.Model):
        numero = models.IntegerField(unique=True)   # 1-100
        bloque = models.CharField(max_length=1)     # A-G
        titulo = models.CharField(max_length=200)
        teoria = models.TextField()
        explicacion = models.TextField()
        regla = models.TextField()
        ejemplo_correcto = models.TextField()
        ejemplo_incorrecto = models.TextField()
        nivel = models.CharField(...)               # basico | intermedio | avanzado
        modulo = models.CharField(...)              # "gramatica"

Migracion: 0019_add_gramatica.

### 4.2 EjercicioGramatical (100 registros)

    class EjercicioGramatical(models.Model):
        tecnica = models.ForeignKey(TecnicaGramatical, related_name="ejercicios")
        tipo = models.IntegerField(choices=...)     # 1-5
        orden = models.IntegerField(default=1)
        payload = models.JSONField()

        class Meta:
            unique_together = ("tecnica", "orden")

### 4.3 ProgresoGramatical

Igual que en otros modulos: usuario + tecnica (unique), intentos, aciertos_consecutivos, estado, sm2_ef, sm2_interval, sm2_repetitions, proxima_revision.

---

## 5. Motor de evaluacion

**Archivo:** core/services/gramatica.py (wrapper sobre sintaxis.py)

El modulo 11 reutiliza el motor del modulo 10 (sintaxis). No hay motor propio. Esto es intencional: el motor de sintaxis soporta tipos 1-5, los ejercicios de gramatica usan tipo 1 y 3, cero duplicacion de codigo, cualquier mejora al motor beneficia a los 5 modulos.

### 5.1 API publica

    def evaluar_ejercicio(ejercicio, respuesta, usuario=None):
        """Delega a sintaxis_engine.evaluar_ejercicio."""

    def actualizar_progreso(usuario, tecnica, ejercicio, ok):
        """SM-2 + mastery + notif al dominar."""

    def proximas_revisiones(usuario, n=5, modulo=None):
        """Filtra por tecnica__modulo si se pasa modulo."""

    def resumen_progreso(usuario, modulo=None):
        """{total, iniciadas, dominadas} filtrado por modulo."""

### 5.2 Mastery

Igual que en sintaxis: 3 aciertos consecutivos + ultimo acierto en tipo 4 o 5 = dominada. En gramatica, como todos son tipo 1/3, se requiere tambien varios intentos en otras tecnicas del mismo bloque.

---

## 6. Vistas y endpoints

**Archivo:** core/views_gramatica.py + core/urls_gramatica.py (app_name="gramatica")

| URL | Metodo | Vista | Proposito |
|-----|--------|-------|-----------|
| /gramatica/ | GET | indice | Grid 100 tecnicas por bloque |
| /gramatica/tecnica/<n>/ | GET | tecnica | Detalle + ejercicio + navegacion |
| /gramatica/evaluar/ | POST | evaluar_ajax | Evaluar + SM-2 |
| /gramatica/progreso/?modulo=gramatica | GET | progreso | Heatmap + proximas revisiones |
| /gramatica/ajax/contador/?modulo=gramatica | GET | contador_ajax | Badge de dominadas |

Todas con @login_required. evaluar_ajax con @require_POST.

La vista tecnica es compartida entre modulos 11-14. Decide bloque_nombre segun t.modulo:

    if t.modulo == "generativa":
        bname = BLOQUES_GENERATIVA.get(t.bloque, "")
    elif t.modulo == "a1":
        bname = BLOQUES_A1.get(t.bloque, "")
    elif t.modulo == "b1":
        bname = BLOQUES_B1.get(t.bloque, "")
    else:
        bname = BLOQUES_INFO.get(t.bloque, "")

---

## 7. Frontend

### 7.1 Templates

- core/gramatica/indice.html — listado de bloques con grid de tecnicas, color por estado (gris/azul/verde). Condicional por es_generativa / es_a1 / es_b1 en el titulo.
- core/gramatica/tecnica.html — flashcard + 1 ejercicio + navegacion anterior/siguiente. Links de "Volver al indice" condicionales segun tecnica.modulo.
- core/gramatica/progreso.html — stats + proximas revisiones + dominadas + en progreso. Filas condicionales segun modulo.

### 7.2 JavaScript

static/js/gramatica.js — AJAX + badges:
- Evaluacion AJAX (POST a /gramatica/evaluar/).
- Badge navbar para gramatica (fetch a /gramatica/ajax/contador/?modulo=gramatica).
- Badge navbar para generativa.
- Badge navbar para A1.
- Badge navbar para B1.

---

## 8. Integracion con el LMS

### 8.1 Navbar

En core/templates/core/base.html, despues del link "Sintaxis 100":

    <li class="nav-item">
      <a class="nav-link" href="{% url 'gramatica:indice' %}">
        <i class="fas fa-book"></i> Gramatica 100
        <span id="gramatica-badge" class="badge bg-info" style="display:none;">0</span>
      </a>
    </li>

### 8.2 Card en dashboard estudiante

En core/templates/core/estudiante/dashboard.html: card con resumen + boton "Ver las 100 tecnicas".

### 8.3 Notificaciones

Al dominar una tecnica -> notificacion tipo "logro", idempotente por referencia gramatica_tecnica_{numero}_{user_id}.

---

## 9. Seed de las 100 tecnicas

**Archivo data:** core/data/tecnicas_gramatica.py
**Archivo loader:** scripts/seed_tecnicas_gramatica.py

Estructura:

    TECNICAS = [{"numero": 1, "bloque": "A", ...}, ...]   # 100 items
    EJERCICIOS = {1: [{"tipo": 1, "orden": 1, "payload": {...}}], ...}

**Idempotencia:** update_or_create por numero (tecnicas) y (tecnica, orden) (ejercicios).

**Aislamiento:** el seed filtra por modulo="gramatica" para no sobrescribir tecnicas de modulos 12-14.

**Distribucion por tipo:** 95 tipo 1 + 5 tipo 3.

---

## 10. Tests

| Archivo | Tests | Cobertura |
|---------|-------|-----------|
| test_gramatica_models.py | 8 | Modelos, data, seed idempotente |
| test_gramatica_views.py | 10 | Vistas GET/POST/403/404/JSON invalido |

Total: 18 tests, 100% del modulo.

Ejecutar:

    python -m pytest core/tests/test_gramatica_models.py core/tests/test_gramatica_views.py -v

---

## 11. Decisiones tecnicas

### 11.1 Reutilizar motor de sintaxis

**Decision:** el modulo 11 no implementa motor propio; delega en sintaxis.py.

**Por que:** el motor ya soporta tipo 1-5 con fuzzy match y SM-2. Duplicarlo introduciria bugs y deuda. Todos los modulos curriculares (11-14) comparten este motor.

### 11.2 Modelo compartido TecnicaGramatical

**Decision:** un solo modelo para gramatica, generativa, A1, B1 (campo modulo distingue).

**Por que:** misma estructura (teoria, regla, ejemplos, ejercicio). Tablas separadas serian 4x mantenimiento por cero beneficio.

### 11.3 Claves ASCII en data

**Decision:** claves en ASCII (numero, teoria, categoria_correcta), valores con tildes.

**Por que:** aprendido de bug en generativa (v1.5.2), donde tildes en claves rompieron el seed con KeyError. Los valores libres llevan tildes normales.

### 11.4 Tipo 1 dominante

**Decision:** 95 tecnicas con tipo 1, 5 con tipo 3.

**Por que:** la gramatica normativa se presta a "elegir la forma correcta". Los tipos 4-5 (produccion libre) se reservan para B1, donde el aprendiz ya produce.

---

## 12. Roadmap / Deuda tecnica

### 12.1 Completado (v1.4.0)

- 100 tecnicas A-G
- 100 ejercicios (95 tipo 1 + 5 tipo 3)
- Seed idempotente + aislamiento por modulo
- 5 vistas + 3 templates + JS
- Integracion navbar + dashboard
- Notificaciones al dominar
- 18 tests, 100% del modulo

### 12.2 Pendiente

- Mas ejercicios tipo 4 y 5 (produccion libre)
- Modo repaso puro (pagina dedicada)
- Exportar progreso (PDF/CSV)
- Ranking de tecnicas mas dificiles (telemetria)

### 12.3 Deuda

- Tipo 1 dominante: 95/100. Limitacion pedagogica.
- Sin revision humana: el docente no puede "override".
- Sin tests E2E (Playwright no cubre gramatica aun).

---

## 13. Metricas de uso (post-deploy)

Sin datos reales aun. Objetivo post-deploy: % de tecnicas dominadas por usuario, tiempo medio por tecnica, tasa de acierto por tipo, tasa de abandono en tecnica N, correlacion mastery vs nota.

---

## 14. Referencias

- RAE & ASALE (2009). Nueva gramatica de la lengua espanola. Espasa.
- RAE (2010). Ortografia de la lengua espanola. Espasa.
- Real Academia Espanola. Diccionario panhispanico de dudas.
- Bosque, I. & Demonte, V. (1999). Gramatica descriptiva de la lengua espanola. Espasa.

---

## 15. Reproducir el modulo

    python manage.py migrate
    python scripts/seed_tecnicas_gramatica.py
    python manage.py shell -c "from core.models_gramatica import TecnicaGramatical; print(TecnicaGramatical.objects.filter(modulo='gramatica').count())"
    python -m pytest core/tests/test_gramatica_models.py core/tests/test_gramatica_views.py -v
    python manage.py runserver
    # -> http://127.0.0.1:8000/gramatica/

---

## 16. Estado actual

| Aspecto | Estado |
|---------|--------|
| 100 tecnicas | OK |
| 100 ejercicios (tipo 1 y 3) | OK |
| Motor reutilizado | OK |
| SM-2 + mastery | OK |
| UI (indice + tecnica + progreso) | OK |
| AJAX evaluacion | OK |
| Notificaciones al dominar | OK |
| Navbar + dashboard | OK |
| Tests (18) | OK |
| Cobertura 100% del modulo | OK |
| Deploy productivo | Pendiente |
| Mas ejercicios 4/5 | Pendiente |

**Tag:** v1.4.0 (2026-10-22)
**Repo:** github.com/Hernank10/django-rhetorica-2026

---

Documento del modulo 11: gramatica castellana. 100 tecnicas, bloques A-G, motor reutilizado, SM-2. 18 tests, 100% del modulo.