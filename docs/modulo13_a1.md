# Modulo 13: Lengua Castellana A1 — 100 tecnicas

**Ultima actualizacion:** 2026-10-26
**Version:** v1.6.0
**Tests:** 10 (data + views)
**Tecnicas:** 100 (bloques A-G)
**Rango:** 201-300

---

## 1. Vision general

Un curso completo de **Lengua Castellana A1** segun el Marco Comun Europeo de Referencia (MCER). Disenado para aprendices de espanol como lengua extranjera (ELE) sin conocimientos previos. Cubre desde el alfabeto hasta conversaciones cotidianas, pasando por articulos, genero, presente, vocabulario basico y situaciones comunicativas.

**Audiencia:** principiantes absolutos. Aprendices que quieren sobrevivir en espanol en contextos cotidianos (viajes, restaurantes, presentaciones, compras).

**Diferencia con modulos 11-12:** el modulo 11 es gramatica normativa para hispanohablantes; el modulo 12 es linguistica formal; el modulo 13 es pedagogia ELE para extranjeros.

Cada una de las **100 tecnicas** es una unidad didactica con teoria, explicacion, regla, ejemplos correcto/incorrecto y ejercicio.

---

## 2. Los 7 bloques

| Bloque | Tecnicas | Contenido | Cantidad |
|--------|----------|-----------|----------|
| **A** | 201-215 | Alfabeto, fonetica, saludos, presentaciones | 15 |
| **B** | 216-230 | Articulos, genero, numero, concordancia basica | 15 |
| **C** | 231-250 | Presente, ser/estar/tener, irregulares, construcciones | 20 |
| **D** | 251-265 | Vocabulario (familia, casa, comida, cuerpo, ropa, animales) | 15 |
| **E** | 266-280 | Preguntas, negacion, adverbios | 15 |
| **F** | 281-290 | Preposiciones y ubicacion | 10 |
| **G** | 291-300 | Frases utiles y situaciones cotidianas | 10 |
| **Total** | | | **100** |

### 2.1 Bloque A — Alfabeto y saludos (201-215)

Alfabeto espanol (27 letras con n con virgulilla), 5 vocales, n con virgulilla, digrafos (ch, ll, rr), h muda, acento prosodico, saludos (hola, buenos dias, buenas tardes, buenas noches), despedidas (adios, hasta luego, hasta manana), presentaciones (me llamo, soy), preguntar el nombre, preguntar como estas, respuestas (bien, mal, regular), cortesia (por favor, gracias, perdon), tu vs usted, numeros 1-10.

### 2.2 Bloque B — Articulos y concordancia (216-230)

Articulo definido (el, la, los, las), articulo indefinido (un, una, unos, unas), genero masculino/femenino, plural (-s, -es), concordancia articulo-sustantivo, demostrativos (este, ese, aquel), posesivos (mi, tu, su), cuantificadores (mucho, poco, todo), numerales cardinales 1-20, interrogativos (que, cual, cuanto), concordancia adjetivo-sustantivo, orden sustantivo+adjetivo, mayusculas, tildes, puntuacion basica.

### 2.3 Bloque C — Presente y ser/estar/tener (231-250)

Presente -ar (hablar), -er (comer), -ir (vivir), tres conjugaciones, persona/numero, ser (soy, eres, es...), estar (estoy, estas, esta...), ser vs estar, tener (tengo, tienes...), expresiones con tener (hambre, sed, frio), ir (voy, vas...), hacer (hago, haces...), venir (vengo, vienes...), poder (puedo, puedes...), querer (quiero, quieres...), presente continuo (estar + gerundio), gustar (me gusta...), reflexivos (me lavo...), hay vs esta/estan, muy vs mucho.

### 2.4 Bloque D — Vocabulario (251-265)

Familia basica (madre, padre, hermano), familia extendida (abuelo, tio, primo), casa (cocina, bano, dormitorio), muebles (mesa, silla, cama), colores, comida (pan, queso, carne), frutas (manzana, platano, naranja), bebidas (agua, cafe, te, jugo), numeros 11-100, dias de la semana, meses del ano, cuerpo (cabeza, mano, pie), ropa (camisa, pantalon, zapato), animales (perro, gato, pajaro).

### 2.5 Bloque E — Preguntas y adverbios (266-280)

Preguntas con que, quien, donde, cuando, como, cuanto/cuantos, por que vs porque, cual/cuales, preguntas si/no, signos de interrogacion, negacion simple (no), negacion doble (no... nada), adverbios de tiempo (hoy, ayer, manana), frecuencia (siempre, a veces, nunca), cantidad (mucho, poco, muy).

### 2.6 Bloque F — Preposiciones y ubicacion (281-290)

Preposicion en (ubicacion), de (posesion/origen), a (direccion), con (compania), para (finalidad), por (causa), adverbios de lugar (aqui, ahi, alli), encima de/debajo de, delante de/detras de/entre, al lado de/cerca de/lejos de.

### 2.7 Bloque G — Situaciones cotidianas (291-300)

Restaurante (pedir, la cuenta), tienda (comprar, precio), medico (sintomas, me duele), transporte (horarios, billetes), presentaciones formales vs informales, hablar del tiempo (clima), describir la familia, describir la casa, hablar de gustos, conversacion A1 completa.

---

## 3. Tipos de ejercicio

En el modulo 13 predominan:

| Tipo | Nombre | Cantidad | Ejemplo |
|------|--------|----------|---------|
| 1 | Opcion multiple | 100 | "Cual es la forma correcta de 'hablar' en 1a persona?" |

100% tipo 1 (opcion multiple). Ejercicios cortos y directos, apropiados para principiantes. Sin produccion libre (tipo 4-5) porque A1 no requiere produccion compleja.

---

## 4. Modelos de datos

### 4.1 TecnicaGramatical (100 registros)

Modelo compartido con modulos 11, 12, 14 (mismo modelo, distinto campo modulo):

    class TecnicaGramatical(models.Model):
        numero = models.IntegerField(unique=True)   # 201-300
        bloque = models.CharField(max_length=1)     # A-G
        titulo = models.CharField(max_length=200)
        teoria = models.TextField()
        explicacion = models.TextField()
        regla = models.TextField()
        ejemplo_correcto = models.TextField()
        ejemplo_incorrecto = models.TextField()
        nivel = models.CharField(...)               # basico | intermedio | avanzado
        modulo = models.CharField(...)              # "a1"

### 4.2 EjercicioGramatical

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

Reutiliza el motor del modulo 10. Cero duplicacion. Cualquier mejora al motor beneficia a los 5 modulos curriculares.

### 5.1 API publica

    def evaluar_ejercicio(ejercicio, respuesta, usuario=None)
    def actualizar_progreso(usuario, tecnica, ejercicio, ok)
    def proximas_revisiones(usuario, n=5, modulo=None)
    def resumen_progreso(usuario, modulo=None)

### 5.2 Mastery

Para A1, el mastery es mas permisivo: se requieren 3 aciertos consecutivos en tipo 1 (no tipo 4-5). Como todos los ejercicios son tipo 1, el aprendiz "domina" al responder bien 3 veces seguidas la misma tecnica. Refuerza el aprendizaje por repeticion.

---

## 6. Vistas y endpoints

**Archivo:** core/views_gramatica.py + core/urls_gramatica.py

| URL | Metodo | Vista | Proposito |
|-----|--------|-------|-----------|
| /gramatica/a1/ | GET | indice_a1 | Grid 100 tecnicas por bloque |
| /gramatica/tecnica/<n>/ | GET | tecnica | Detalle compartido |
| /gramatica/evaluar/ | POST | evaluar_ajax | Evaluacion + SM-2 |
| /gramatica/progreso/?modulo=a1 | GET | progreso | Heatmap + proximas revisiones |
| /gramatica/ajax/contador/?modulo=a1 | GET | contador_ajax | Badge |

La vista tecnica es compartida. Para tecnicas A1 (201-300) el bloque_nombre viene de BLOQUES_A1 dict:

    BLOQUES_A1 = {
        "A": "Alfabeto, fonetica y saludos",
        "B": "Articulos, genero y numero",
        "C": "Presente, ser/estar/tener",
        "D": "Vocabulario basico",
        "E": "Preguntas, negacion, adverbios",
        "F": "Preposiciones y ubicacion",
        "G": "Frases utiles y situaciones",
    }

La vista tecnica pasa `es_a1=True` al template cuando `t.modulo == "a1"`.

---

## 7. Frontend

### 7.1 Templates

- core/gramatica/indice.html — compartido, condicional es_a1 para titulo "Gramatica A1"
- core/gramatica/tecnica.html — compartido, boton "Volver al indice A1"
- core/gramatica/progreso.html — compartido con modulo=a1

### 7.2 JavaScript

static/js/gramatica.js incluye badge verde (bg-success) para A1 (fetch a /gramatica/ajax/contador/?modulo=a1).

---

## 8. Integracion con el LMS

### 8.1 Navbar

En core/templates/core/base.html, link "A1 100" con icono seedling y badge verde.

### 8.2 Card en dashboard estudiante

Card verde con resumen + boton "Ver las 100 tecnicas" y "Empezar por la 201".

### 8.3 Notificaciones

Al dominar una tecnica -> notificacion tipo "logro", idempotente por referencia a1_tecnica_{numero}_{user_id}.

---

## 9. Seed de las 100 tecnicas

**Archivo data:** core/data/tecnicas_a1.py
**Archivo loader:** scripts/seed_a1.py

Estructura:

    TECNICAS = [{"numero": 201, "bloque": "A", "modulo": "a1", ...}, ...]
    EJERCICIOS = {201: [{"tipo": 1, "orden": 1, "payload": {...}}], ...}

**Idempotencia:** update_or_create por numero. **Aislamiento:** filtra por modulo="a1".

**Distribucion por tipo:** 100% tipo 1.

**Crecimiento progresivo:** los tags v1.6.0-alpha/beta/beta.2...beta.5 documentan la carga progresiva (A, A+B, A+B+C, etc.) hasta v1.6.0 con las 100 tecnicas completas.

---

## 10. Tests

| Archivo | Tests | Cobertura |
|---------|-------|-----------|
| test_a1_data.py | 5 | Data, seed idempotente, campos, ejercicios |
| test_a1_views.py | 5 | Indice, tecnica, filtro, es_a1 flag, anonimo |

Total: 10 tests.

**Tests dinamicos:** `test_a1_data.py` usa `len(TECNICAS)` entre 50 y 100 y verifica rango consecutivo desde 201. No hardcodea el total. Aguanta crecimiento hasta 100 tecnicas sin tocar el test.

Ejecutar:

    python -m pytest core/tests/test_a1_data.py core/tests/test_a1_views.py -v

---

## 11. Decisiones tecnicas

### 11.1 100% tipo 1

**Decision:** todos los ejercicios son opcion multiple.

**Por que:** A1 requiere reconocimiento, no produccion. El aprendiz aun no tiene vocabulario ni estructuras para producir oraciones libres. Los tipos 4-5 se reservan para B1+.

### 11.2 Modelo compartido

**Decision:** TecnicaGramatical compartido con gramatica, generativa, B1.

**Por que:** misma estructura. Campo modulo distingue.

### 11.3 Tests dinamicos

**Decision:** los tests no hardcodean `len(TECNICAS)`.

**Por que:** bug historico (v1.6.0-alpha con tests hardcodeados a 50). Los tests ahora verifican `min <= len <= max` (50-100), rango consecutivo, bloques A-G. Sobreviven a crecimiento.

---

## 12. Estado actual

| Aspecto | Estado |
|---------|--------|
| 100 tecnicas | OK |
| 100 ejercicios (100% tipo 1) | OK |
| Motor reutilizado | OK |
| SM-2 + mastery | OK |
| UI (indice + tecnica + progreso) | OK |
| AJAX evaluacion | OK |
| Notificaciones al dominar | OK |
| Navbar + dashboard | OK |
| Tests (10) | OK |
| Tests dinamicos | OK |
| Deploy productivo | Pendiente |

**Tag:** v1.6.0 (2026-10-24)
**Repo:** github.com/Hernank10/django-rhetorica-2026

---

Documento del modulo 13: Lengua Castellana A1. 100 tecnicas (201-300), bloques A-G, MCER nivel principiante. 10 tests.