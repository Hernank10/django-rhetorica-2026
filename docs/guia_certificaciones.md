# Guia del sistema de certificaciones — Rhetorica+

**Ultima actualizacion:** 2026-10-26
**Version:** v1.7.7
**Aplica a:** estudiantes, profesores y administradores

---

## 1. Vision general

Rhetorica+ emite **certificaciones** que acreditan que un estudiante completo un itinerario formativo. Cada certificado incluye:

- Folio unico (ej: RH-2026-000078)
- Codigo de verificacion (ej: CERT-0125-0007)
- Huella SHA256 (integridad del registro)
- URL publica de verificacion (para terceros)
- PDF y Word descargables
- Vista previa HTML tipo diploma

### 1.1 Los 5 niveles

| Nivel | Codigo | Requisitos tipicos |
|---|---|---|
| Bronce | bronce | 2-82 lecciones + 50-2050 puntos |
| Plata | plata | escala intermedia |
| Oro | oro | escala intermedia-alta |
| Platino | platino | escala alta |
| Diamante | diamante | 10-90 lecciones + 250-2250 puntos |

**Catalogo actual:** 49 certificaciones activas.

### 1.2 Otorgamiento automatico (nuevo v1.7.7)

A partir de v1.7.7, **las certificaciones se otorgan automaticamente** al cumplir los requisitos. Hay 3 caminos:

1. **Automatico (default):** al completar una leccion, el sistema verifica tu progreso contra TODAS las certificaciones activas y te otorga las que cumplas. No tienes que hacer nada extra.
2. **Manual por administrador:** via `/admin/core/certificacionobtenida/` para casos especiales.
3. **Backfill masivo:** un admin puede ejecutar `python manage.py otorgar_certificaciones` para otorgar certs pendientes a todos los usuarios.

**Estado actual:** 1,311 certificaciones emitidas a 45+ estudiantes.

---

## 2. Para estudiantes

### 2.1 Como obtengo un certificado?

**Camino principal (automatico):**

1. Completa lecciones en cualquier curso
2. Al completar CADA leccion, el sistema verifica tus estadisticas:
   - `lecciones`: cuantas has completado
   - `puntos`: suma de puntajes obtenidos
   - `tasa`: porcentaje de respuestas correctas
3. Si cumples los requisitos de alguna certificacion, se te otorga automaticamente
4. Recibes una notificacion

**Requisitos tipicos por certificacion:**

| Certificacion | Lecciones | Puntos | Tasa |
|---|---|---|---|
| Iniciacion a la Retorica | 5 | - | - |
| Certificacion 01 (Bronce) | 2 | 50 | - |
| Certificacion 05 (Diamante) | 10 | 250 | - |
| Maestria Retorica | 50 | - | 85% |
| Certificacion 45 (Diamante) | 90 | 2250 | - |

### 2.2 Donde veo mis certificados?

**URL:** `/estudiante/certificados/`

Muestra:
- Nombre de cada certificacion
- Nivel (Bronce/Plata/Oro/Platino/Diamante)
- Fecha de obtencion
- Codigo de verificacion
- Botones de descarga PDF y Word

### 2.3 Como descargo mi certificado?

En `/estudiante/certificados/`, cada certificado tiene:

- **PDF** -> abre el PDF en una pestaña nueva (diseno diploma, listo para imprimir)
- **Word** -> descarga un `.docx` editable

### 2.4 Como verifico mi certificado?

Cada certificado tiene una URL publica de verificacion:

```
https://tu-dominio.com/verificar/CERT-0125-0007/
```

Esta URL NO requiere login. Cualquier persona puede abrirla y ver:

- Nombre del estudiante
- Nombre de la certificacion
- Fecha de emision
- Folio unico
- Huella SHA256 (integridad)

**Comparte esta URL en tu CV o LinkedIn.** Es la prueba publica de tu certificado.

### 2.5 Puedo obtener certificados de niveles superiores?

Si. Los niveles escalan:

- **Bronce** -> requisitos minimos (2 lecciones + 50 puntos)
- **Plata** -> intermedios
- **Oro** -> intermedios-altos
- **Platino** -> altos
- **Diamante** -> maximos (90 lecciones + 2250 puntos)

**Solo completando lecciones escalas de nivel automaticamente.**

### 2.6 Que pasa si mi certificado no aparece?

Checklist:

1. Verifica que tu progreso este registrado en `/estudiante/cursos/`
2. El sistema verifica certs cada vez que completas una leccion. Si acabas de empezar, completa 1-2 lecciones
3. Contacta a tu profesor o admin si persiste (pueden ejecutar el backfill con `otorgar_certificaciones --user tu_username`)

---

## 3. Para profesores

### 3.1 Que puedo hacer con certificaciones?

| Accion | Donde | Notas |
|---|---|---|
| Ver certificados de mis estudiantes | `/profesor/certificaciones/` | Filtra por profesor_asignado |
| Ver todos los certificados | Admin panel (solo admin) | Los profesores NO ven todos |
| Descargar PDF de un estudiante | Boton en la lista | `/profesor/certificaciones/<id>/pdf/` |
| Descargar Word | Boton en la lista | `/profesor/certificaciones/<id>/docx/` |
| Vista previa HTML | Boton "preview" | `/profesor/certificaciones/<id>/preview/` |
| Otorgar certificado manualmente | NO disponible (solo admin) | Los certs se otorgan auto o via backfill |
| Editar certificacion | NO disponible (solo admin) | |

### 3.2 Filtros disponibles

`/profesor/certificaciones/` permite filtrar por:
- Estudiante (`?estudiante=<id>`)
- Curso (`?curso=<id>`)
- Nivel (Bronce/Plata/Oro/Platino/Diamante)

### 3.3 Firma del diploma

El diploma HTML (preview, PDF, Word) tiene 2 campos de firma estaticos:

- "Profesor" — firma autorizada
- "Direccion Academica" — firma autorizada
- "SELLO OFICIAL" — sello decorativo

**No hay personalizacion por profesor** actualmente (deuda tecnica).

### 3.4 Como veo cuantos certificados ha obtenido un estudiante?

En `/profesor/estudiantes/<id>/` (detalle del estudiante) -> seccion de certificados.

O en `/profesor/estudiantes/metricas/` (vista agregada) -> columna de certificados.



---

## 4. Para administradores

### 4.1 Panel de administracion

**URL:** `/admin/core/certificacionobtenida/`

Muestra TODOS los certificados emitidos:

| Columna | Descripcion |
|---|---|
| user | Estudiante que obtuvo el cert |
| certificacion | Nombre del certificado |
| fecha_obtenida | Fecha de emision |
| codigo_verificacion | Codigo unico |
| url_verificacion | URL publica |

**Filtros:** por certificacion, por fecha.
**Busqueda:** por usuario o codigo de verificacion.

### 4.2 Crear una certificacion (catalogo)

**URL:** `/admin/core/certificacion/add/`

Campos:

| Campo | Tipo | Ejemplo |
|---|---|---|
| nombre | CharField | "Redaccion Profesional" |
| descripcion | TextField | "Certificacion intermedio: Redaccion Profesional" |
| nivel | ChoiceField | Bronce / Plata / Oro / Platino / Diamante |
| requisitos | JSON | `{"lecciones": 30, "tasa": 75}` |
| activa | Boolean | True/False |

### 4.3 Otorgar manualmente (1 estudiante)

**Via admin panel:**

1. `/admin/core/certificacionobtenida/add/`
2. Seleccionar `user` (estudiante)
3. Seleccionar `certificacion` (del catalogo)
4. `fecha_obtenida` = ahora
5. `codigo_verificacion` = `CERT-{user_id:04d}-{cert_id:04d}` (ej: `CERT-0125-0007`)
6. `url_verificacion` = `/verificar/{codigo}/`
7. Save -> notificacion automatica al estudiante

### 4.4 Backfill masivo (auto-otorgamiento)

**Via management command:**

```bash
# Auditar primero (recomendado)
python manage.py otorgar_certificaciones --dry-run

# Otorgar a todos los estudiantes no-staff
python manage.py otorgar_certificaciones

# Solo a un usuario
python manage.py otorgar_certificaciones --user est001
```

**Cuando usar cada uno:**

| Situacion | Comando |
|---|---|
| Acabas de desplegar v1.7.7 | `otorgar_certificaciones` (una vez) |
| Un estudiante reporta que le falta un cert | `otorgar_certificaciones --user <username>` |
| Auditar cuantos certs se otorgarian | `otorgar_certificaciones --dry-run` |
| Despues de cambiar requisitos | `otorgar_certificaciones` |

### 4.5 Auditoria

El campo `codigo_verificacion` es unico e irrepetible.

La huella SHA256 (calculada en `utils_certificados.py`) garantiza integridad.

Para auditar un certificado:
1. Abrir `/verificar/<codigo>/`
2. Comparar la huella mostrada con la almacenada en la DB
3. Si coinciden -> certificado integro

### 4.6 Desactivar una certificacion

Si una certificacion ya no se emite:

1. `/admin/core/certificacion/<id>/change/`
2. Desmarcar `activa`
3. Save

**Efecto:** deja de ofrecerse en el catalogo pero los certificados ya emitidos siguen siendo validos.

---

## 5. Referencia tecnica (para devs)

### 5.1 Modelos

```python
class Certificacion(models.Model):
    nombre = CharField(200)
    descripcion = TextField()
    nivel = CharField(choices=[bronce, plata, oro, platino, diamante])
    requisitos = JSONField()
    imagen = CharField(blank=True, null=True)
    fecha_creacion = DateTimeField(auto_now_add=True)
    activa = BooleanField(default=True)

class CertificacionObtenida(models.Model):
    user = FK(User)
    certificacion = FK(Certificacion)
    fecha_obtenida = DateTimeField()
    codigo_verificacion = CharField(unique=True)
    url_verificacion = URLField(null=True, blank=True)
```

### 5.2 URLs

| URL | Vista | Rol |
|---|---|---|
| `/estudiante/certificados/` | est.mis_certificados | Estudiante |
| `/estudiante/certificados/<id>/pdf/` | est.descargar_certificado_pdf | Estudiante |
| `/estudiante/certificados/<id>/docx/` | est.descargar_certificado_docx | Estudiante |
| `/profesor/certificaciones/` | prof.lista_certificaciones | Profesor |
| `/profesor/certificaciones/<id>/pdf/` | prof.certificado_pdf | Profesor |
| `/profesor/certificaciones/<id>/docx/` | prof.certificado_docx | Profesor |
| `/profesor/certificaciones/<id>/preview/` | prof.certificado_preview | Profesor |
| `/verificar/<codigo>/` | verificar_certificado_publico | Publico |

### 5.3 Servicios

`core/services/certificaciones.py`:
- `get_user_stats(user)` -> `{lecciones, puntos, tasa}`
- `cumple_requisitos(stats, requisitos)` -> bool
- `verificar_y_otorgar(user, dry_run)` -> `list[Certificacion]`

### 5.4 Signals

- `notif_certificacion` (linea 121): notifica cuando se crea un cert
- `auto_cert_al_completar` (linea ~148): otorga certs al completar ProgresoUsuario

### 5.5 Utils

`core/utils_certificados.py`:
- `folio_unico(cert)` -> `RH-YYYY-NNNNNN`
- `huella_certificado(cert)` -> SHA256 completo
- `huella_corta(cert)` -> 16 chars en formato XXXX-XXXX-XXXX-XXXX

### 5.6 Management commands

- `seed_content.py` — crea las 49 certificaciones
- `otorgar_certificaciones.py` — backfill masivo con `--user` y `--dry-run`

### 5.7 Seed de prueba

`scripts/seed_test_certs.py`:
- Asigna 1-3 certs a `est001`-`est045`
- Idempotente (filter + create)

---

## 6. Preguntas frecuentes

**Por que no recibo mi certificado automaticamente?**

El sistema verifica automaticamente al completar CADA leccion. Si acabas de empezar, completa 1-2 lecciones mas. Si aun asi no aparece, un admin puede ejecutar `python manage.py otorgar_certificaciones --user tu_username` para forzar el backfill.

**Puedo falsificar un certificado?**

No. La huella SHA256 y el folio unico son verificables publicamente. Si alguien altera un PDF, la huella deja de coincidir.

**El certificado caduca?**

No. Una vez emitido, es valido indefinidamente. Solo puede "desactivarse" la certificacion del catalogo, pero los ya emitidos siguen siendo validos.

**Puedo tener el mismo certificado dos veces?**

No. `codigo_verificacion` es unico. El servicio `verificar_y_otorgar` es idempotente (filtra por certs ya obtenidas).

**Que pasa si cambio los requisitos de una certificacion?**

Los certs ya emitidos siguen siendo validos. Solo afecta a nuevos otorgamientos. Si bajas los requisitos, ejecuta `python manage.py otorgar_certificaciones` para otorgar los nuevos que cumplan.

**Como se que certificaciones puedo obtener?**

Depende de tu progreso actual. El sistema te las otorgara automaticamente al completar lecciones. Consulta con tu profesor.

**Puedo descargar todos mis certificados de una vez?**

No en la UI actual. Descarga uno a uno, o pide al admin un export batch (feature futura).

---

## 7. Roadmap / deuda tecnica conocida

**Completado (v1.7.7):**
- Otorgamiento automatico al cumplir requisitos (signal)
- Backfill masivo via management command
- Admin registrado con filtros y busqueda

**Pendiente:**
- Firma personalizada del profesor en el diploma
- Export masivo (ZIP con todos los certs de un estudiante)
- Notificacion al profesor cuando un estudiante obtiene un cert
- API REST para consultar certificados
- Verificacion de huella en el PDF (hoy solo en HTML)
- Personalizacion del diploma (logos, colores por nivel)

**Prioridad para el proximo sprint:**
1. Personalizacion del diploma (impacto alto, complejidad baja)
2. Notificacion al profesor (impacto medio, complejidad baja)
3. API REST (impacto bajo, complejidad baja)

---

Documento generado automaticamente desde el codigo en v1.7.7.
Para dudas: consultar `/admin/` o contactar al administrador.
