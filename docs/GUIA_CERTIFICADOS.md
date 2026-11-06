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
## 5. Como verificar y descargar tu certificado

### Descargar el PDF

| Donde | Como |
|---|---|
| Desde el dashboard | `/estudiante/certificados/` -> boton "Descargar PDF" |
| Desde URL directa | `/estudiante/certificados/<ID>/pdf/` |
| Desde el email | Si el administrador lo envio (opcional) |

**Ejemplo de URL directa:**

### Verificar el certificado

1. **Verificacion interna:** abrir la URL de verificacion y comprobar que los datos coinciden con el PDF.
2. **Verificacion por codigo:** comparar el codigo del PDF con el de la BD (solo administradores).
3. **Verificacion por email:** enviar el PDF a un tercero; el codigo permite comprobar su autenticidad.

---

## 6. Como funciona el codigo de verificacion

Cada certificado tiene un **codigo unico** con el formato:

**Ejemplo:** `PILOT-1447-A3F2B9C1`

| Parte | Significado |
|---|---|
| `PILOT-` | Prefijo que indica fase de pilot |
| `1447` | ID del usuario en la BD (4 digitos) |
| `A3F2B9C1` | Hash de 8 caracteres (aleatorio) |

**Propiedades:**

- **Unico:** no hay dos certificados con el mismo codigo.
- **Aleatorio:** el hash no se puede predecir.
- **Verificable:** el codigo esta en la BD y en el PDF.

---
## 7. Guia para docentes y administradores

### Docentes
1. Inicia sesion como profesor.
2. Ve a `/profesor/analytics/` para ver el progreso.
3. Certificados: `/admin/core/certificacionobtenida/` (staff).

### Administradores
1. Inicia sesion como admin.
2. Ve a `/admin/core/certificacionobtenida/add/`.
3. Rellena User, Certificacion, Codigo, Fecha, URL. Guarda.

### Emitir en bloque
Usa `_pilot_full_test.py` en modo `full` (45 certificados automaticos).

---

## 8. Guia para programadores

### Campos de CertificacionObtenida

| Campo | Tipo | Descripcion |
|---|---|---|
| user | FK a User | Usuario |
| certificacion | FK a Certificacion | Tipo |
| codigo_verificacion | CharField | Codigo unico |
| fecha_obtenida | DateField | Fecha |
| url_verificacion | URLField | URL |

### Codigo unico

codigo = f"PILOT-{user.id:04d}-{secrets.token_hex(4).upper()}"

### Extender certificados

1. Crear certificacion en catalogo.
2. Definir requisitos.
3. Implementar emision automatica.
4. Anadir vista de PDF.
5. Anadir vista de verificacion.

---

## 9. Preguntas frecuentes

- **Cuantos textos necesito?** Al menos 3, con acierto >= 60%.
- **Tiene validez oficial?** No. Reconocimiento interno, no MCER.
- **Puedo obtener de nivel especifico?** Solo "Lectura + Flashcards" en v3.4.6.
- **Como verifico autenticidad?** Comparar codigo del PDF con BD o abrir URL de verificacion.
- **Si pierdo el PDF?** Volver a descargarlo desde `/estudiante/certificados/`.
- **Si no estoy en grupo Estudiante?** No puedes obtenerlo.
- **Caduca?** No.
- **Varios certificados?** Si, si hay varios tipos.

---
## 10. Solucion de problemas

### No veo mi certificado
Causas: no cumples requisitos, no estas en grupo Estudiante, no se emitio, error en BD.
Solucion: verifica tu progreso y contacta con el administrador.

### El PDF no se descarga
Causas: URL incorrecta, permisos, error del servidor.
Solucion: prueba desde `/estudiante/certificados/`.

### El codigo no coincide
Causas: PDF antiguo, error en BD.
Solucion: contacta con el administrador con el PDF y el codigo.

### No tiene mi nombre real
Causas: no configuraste nombre, la plataforma usa username.
Solucion: contacta con el administrador.

---

## 11. Contacto y soporte

| Tipo de consulta | Canal |
|---|---|
| Problemas tecnicos | Contacta con el administrador |
| Solicitud de certificado | Contacta con el administrador |
| Verificacion | Contacta con el administrador |
| Bug | github.com/Hernank10/django-rhetorica-2026/issues |

---

## 12. Checklist de verificacion

- [ ] He iniciado sesion correctamente.
- [ ] He completado al menos 3 textos en `/lectura/`.
- [ ] Mi tasa de acierto media es >= 60%.
- [ ] He repasado al menos una vez las flashcards.
- [ ] Estoy en el grupo `Estudiante`.
- [ ] He revisado `/estudiante/certificados/`.
- [ ] He probado la URL directa `/estudiante/certificados/<id>/pdf/`.

Si todo es "si" y sigues sin certificado, contacta con el administrador.

---

*Guia derivada del proyecto django-rhetorica (tag v3.4.7-lectura-guia-integrada, noviembre 2026).*