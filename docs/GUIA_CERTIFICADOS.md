# Guía para obtener certificados en django-rhetorica

**Cómo obtener, verificar y descargar tus certificados en la plataforma**

---

## 1. Qué es un certificado en django-rhetorica

Un **certificado** es un documento PDF verificable que acredita que has completado un módulo de aprendizaje en la plataforma. No es un título oficial del MCER ni una certificación de nivel lingüístico reconocida por instituciones externas: es un **reconocimiento interno** de la plataforma que acredita tu constancia y tu progreso.

Cada certificado incluye:

- **Nombre del módulo** completado (ej. "Lectura + Flashcards").
- **Código de verificación único** (ej. `PILOT-1447-A3F2B9C1`).
- **Fecha de obtención**.
- **URL de verificación**.
- **Tu nombre de usuario**.

**Importante:** el certificado no sustituye a una certificación oficial (DELE, SIELE, etc.). Es un reconocimiento de la plataforma que puede servirte como:

- Evidencia de constancia en tu portfolio personal.
- Motivación para seguir completando textos.
- Requisito interno en un curso impartido con la plataforma.

---

## 2. Qué certificados existen

En la versión actual (`v3.4.6`), el catálogo de certificaciones contiene:

| Certificación | Descripción | Requisito |
|---|---|---|
| **Lectura + Flashcards** | Módulo combinado de lectura progresiva y repaso con flashcards | Completar el número mínimo de textos + técnicas |

**Nota:** la plataforma está en fase de pilot. En futuras versiones se prevé añadir más certificaciones (por nivel MCER, por tipo de técnica, por módulo de gramática).

---

## 3. Requisitos para obtener un certificado

| # | Requisito | Dónde verificarlo |
|---|---|---|
| 1 | Estar registrado y con sesión iniciada | `/login/` |
| 2 | Haber completado un número mínimo de textos | `/lectura/progreso/` |
| 3 | Haber completado un número mínimo de técnicas | `/estudiante/estadisticas/` |
| 4 | Tener al menos un ejercicio con tasa de acierto ≥ 60% | `/lectura/progreso/` |
| 5 | Estar en el grupo `Estudiante` | (lo gestiona el administrador) |

**Nota:** en el pilot se han emitido certificados a estudiantes que completaron **al menos 3 textos** con una tasa de acierto razonable.

---

## 4. Guía paso a paso

### Paso 1 — Inicia sesión

1. Abre `https://django-rhetorica-2026-1.onrender.com/login/`
2. Introduce tu usuario y contraseña.
3. Si es tu primera vez, el administrador te habrá proporcionado credenciales.

**Resultado esperado:** te redirige a `/estudiante/` con tu dashboard personal.

### Paso 2 — Completa textos de lectura

1. Ve a `/lectura/`.
2. Elige un texto de tu nivel (A1, A2, B1, B2, C1 o C2).
3. Lee el texto con atención.
4. Responde los ejercicios.
5. Pulsa **"Enviar"** o **"Completar"**.

**Resultado esperado:** el texto se marca como completado en tu progreso.

### Paso 3 — Repite con más textos

Repite el paso 2 con al menos 3 textos diferentes. Se recomienda:

- Variar los niveles (empezar por A1/A2, subir a B1/B2).
- Leer textos de distintas temáticas.
- No dejar ejercicios en blanco.

### Paso 4 — Repasa con flashcards

1. Ve a `/lectura/flashcards/`.
2. Repasa las tarjetas de vocabulario o conceptos.
3. Marca las que ya dominas.

**Resultado esperado:** tu progreso en técnicas aumenta.

### Paso 5 — Verifica tu progreso

1. Ve a `/lectura/progreso/`.
2. Comprueba: textos completados, tasa de acierto media, técnicas dominadas.
3. Ve a `/estudiante/estadisticas/` para ver tu gráfico de progreso.

### Paso 6 — Accede a tus certificados

1. Ve a `/estudiante/certificados/`.
2. Verás una lista de certificados:
   - Si ya tienes uno: aparece con su código y fecha.
   - Si aún no lo tienes: aparece un mensaje indicando qué te falta.

### Paso 7 — Descarga el PDF

1. En la lista de certificados, pulsa **"Descargar PDF"**.
2. Se descarga un archivo PDF con: tu nombre de usuario, nombre del módulo, código de verificación, fecha de obtención y URL de verificación.

### Paso 8 — Verifica el certificado

1. Abre el PDF y localiza el **código de verificación**.
2. Abre en el navegador la URL de verificación.
3. Comprueba que el código del PDF coincide con el de la página.

---