# Modulo 15: Sistema de Certificaciones — 5 niveles + auto-otorgamiento

**Ultima actualizacion:** 2026-10-26
**Version:** v1.7.7
**Tests:** 13 (auto-cert)
**Certificaciones activas:** 49
**Certificaciones emitidas:** 1,311

---

## 1. Vision general

Sistema de emision y verificacion de certificados academicos. Cubre 5 niveles (Bronce → Diamante), 49 certificaciones activas, y otorgamiento automatico al cumplir requisitos.

Cada certificado tiene:

- **Folio unico** (ej: RH-2026-000078)
- **Codigo de verificacion** (ej: CERT-0125-0007)
- **Huella SHA256** de integridad
- **URL publica de verificacion** (sin login)
- **PDF + Word descargables**
- **Preview HTML** tipo diploma con QR

**Audiencia:** estudiantes (reciben), profesores (visualizan), administradores (gestionan), terceros (verifican).

---

## 2. Los 5 niveles

| Nivel | Codigo interno | Requisitos tipicos |
|---|---|---|
| Bronce | bronce | 2-82 lecciones + 50-2050 puntos |
| Plata | plata | escala intermedia |
| Oro | oro | escala intermedia-alta |
| Platino | platino | escala alta |
| Diamante | diamante | 10-90 lecciones + 250-2250 puntos |

**49 certificaciones activas:** 9 por nivel + 4 especiales (Iniciacion a la Retorica, Maestria Retorica, Comprension Lectora, Redaccion Profesional).

Los requisitos exactos estan en `Certificacion.requisitos` (JSONField):
- `lecciones`: minimo de ProgresoUsuario completadas
- `puntos`: suma de puntaje_obtenido
- `tasa`: porcentaje minimo de Respuesta.es_correcta

---

## 3. Modelos de datos

### 3.1 Certificacion (catalogo)

```python
class Certificacion(models.Model):
    nombre = CharField(200)
    descripcion = TextField()
    nivel = CharField(choices=[bronce, plata, oro, platino, diamante])
    requisitos = JSONField()  # {"lecciones": 30, "tasa": 75}
    imagen = CharField(blank=True, null=True)
    fecha_creacion = DateTimeField(auto_now_add=True)
    activa = BooleanField(default=True)
```

### 3.2 CertificacionObtenida (emitidas)

```python
class CertificacionObtenida(models.Model):
    user = FK(User)
    certificacion = FK(Certificacion)
    fecha_obtenida = DateTimeField()
    codigo_verificacion = CharField(unique=True)  # CERT-UUUU-CCCC
    url_verificacion = URLField(null=True, blank=True)
```

---

## 4. Motor de otorgamiento

**Archivo:** `core/services/certificaciones.py`

### 4.1 get_user_stats

```python
def get_user_stats(user):
    """Devuelve {lecciones, puntos, tasa} del usuario."""
    progresos = ProgresoUsuario.objects.filter(usuario=user, completado=True)
    lecciones = progresos.count()
    puntos = progresos.aggregate(total=Sum("puntaje_obtenido"))["total"] or 0
    total_resp = Respuesta.objects.filter(user=user).count()
    if total_resp > 0:
        correctas = Respuesta.objects.filter(user=user, es_correcta=True).count()
        tasa = round((correctas / total_resp) * 100, 1)
    else:
        tasa = 0.0
    return {"lecciones": lecciones, "puntos": puntos, "tasa": tasa}
```

### 4.2 cumple_requisitos

```python
def cumple_requisitos(stats, requisitos):
    """True si stats cumple TODOS los requisitos presentes."""
    if not isinstance(requisitos, dict):
        return False
    if "lecciones" in requisitos and stats["lecciones"] < requisitos["lecciones"]:
        return False
    if "puntos" in requisitos and stats["puntos"] < requisitos["puntos"]:
        return False
    if "tasa" in requisitos and stats["tasa"] < requisitos["tasa"]:
        return False
    return True
```

### 4.3 verificar_y_otorgar

```python
def verificar_y_otorgar(user, dry_run=False):
    """Otorga certs pendientes. Idempotente. Retorna lista de nuevas."""
    stats = get_user_stats(user)
    ya_obtenidas = CertificacionObtenida.objects.filter(
        user=user
    ).values_list("certificacion_id", flat=True)
    pendientes = Certificacion.objects.filter(activa=True).exclude(id__in=ya_obtenidas)

    nuevas = []
    for cert in pendientes:
        if cumple_requisitos(stats, cert.requisitos):
            nuevas.append(cert)
            if not dry_run:
                codigo = f"CERT-{user.id:04d}-{cert.id:04d}"
                CertificacionObtenida.objects.create(
                    user=user, certificacion=cert,
                    fecha_obtenida=timezone.now(),
                    codigo_verificacion=codigo,
                    url_verificacion=f"/verificar/{codigo}/",
                )
    return nuevas
```

**Caracteristicas:**
- Idempotente: filtra por `certificacion_id` ya obtenidas
- Dry-run: auditable sin escribir
- Codigo deterministico: `CERT-UUUU-CCCC` (user_id, cert_id)

---

## 5. Signal + management command

### 5.1 Signal automatico

`core/signals_progreso.py` (linea ~148):

```python
@receiver(post_save, sender=ProgresoUsuario)
def auto_cert_al_completar(sender, instance, created, **kwargs):
    """Cuando un estudiante completa una leccion, verifica certs."""
    if not getattr(instance, "completado", False):
        return
    from core.services.certificaciones import verificar_y_otorgar
    try:
        verificar_y_otorgar(instance.usuario)
    except Exception:
        pass  # no rompe el flujo de progreso si hay error
```

**Flujo:** estudiante completa leccion → signal → verifica TODOS los certs pendientes → otorga los que cumplan.



### 5.2 Management command (backfill)

`core/management/commands/otorgar_certificaciones.py`:

```bash
# Otorgar a todos los usuarios no-staff
python manage.py otorgar_certificaciones

# Otorgar solo a un usuario
python manage.py otorgar_certificaciones --user est001

# Auditar sin escribir
python manage.py otorgar_certificaciones --dry-run
```

Uso tipico:
1. Ejecutar `--dry-run` para ver cuantos se otorgarian
2. Revisar que el output tenga sentido
3. Ejecutar sin `--dry-run` para aplicar

---

## 6. Vistas y endpoints

### 6.1 Estudiante

| URL | Vista | Proposito |
|---|---|---|
| `/estudiante/certificados/` | `est.mis_certificados` | Lista sus certs |
| `/estudiante/certificados/<id>/pdf/` | `est.descargar_certificado_pdf` | PDF |
| `/estudiante/certificados/<id>/docx/` | `est.descargar_certificado_docx` | Word |

### 6.2 Profesor

| URL | Vista | Proposito |
|---|---|---|
| `/profesor/certificaciones/` | `prof.lista_certificaciones` | Filtrado por profesor_asignado |
| `/profesor/certificaciones/<id>/pdf/` | `prof.certificado_pdf` | PDF |
| `/profesor/certificaciones/<id>/docx/` | `prof.certificado_docx` | Word |
| `/profesor/certificaciones/<id>/preview/` | `prof.certificado_preview` | Preview HTML |

### 6.3 Publico (sin login)

| URL | Vista | Proposito |
|---|---|---|
| `/verificar/<codigo>/` | `verificar_certificado_publico` | Verificacion por terceros |

---

## 7. Frontend

### 7.1 Preview HTML

`core/templates/core/profesor/certificados/preview.html` (6.9 KB):

- Diseño diploma (aspect-ratio 29.7/21, A4 horizontal)
- Borde azul + sello dorado
- Nombre del alumno, certificacion, nivel, fecha
- Firmas estaticas: Profesor, Sello Oficial, Direccion Academica
- QR code apuntando a `/verificar/<codigo>/`
- Panel de integridad: folio, codigo, huella SHA256 completa

### 7.2 PDF y Word

- **PDF:** `reportlab` (ya en requirements)
- **Word:** `python-docx`

Mismo diseño que preview, adaptado a cada formato.

---

## 8. Integracion con el LMS

### 8.1 Navbar profesor

Link "Certificaciones" visible en `/profesor/`.

### 8.2 Dashboard estudiante

Card "Certificados obtenidos: N" en `/estudiante/`.

### 8.3 Notificacion automatica

Signal `notif_certificacion` envia notificacion al estudiante cuando recibe un cert:

```python
@receiver(post_save, sender=CertificacionObtenida)
def notif_certificacion(sender, instance, created, **kwargs):
    if not created:
        return
    crear_notificacion(
        user=instance.user,
        tipo="certificacion",
        titulo=f"Certificacion: {instance.certificacion.nombre}",
        mensaje=f"Obtuviste la certificacion '{instance.certificacion.nombre}'",
        url_destino="/estudiante/certificados/",
    )
```

---

## 9. Seed y datos actuales

### 9.1 Catalogo (seed inicial)

`core/management/commands/seed_content.py` crea las 49 certificaciones.

### 9.2 Emitidas (estado actual v1.7.7)

- **1,311 certificaciones emitidas**
- 147 preexistentes (seed v1.7.5)
- 1,164 auto-otorgadas (v1.7.7 con `otorgar_certificaciones`)
- 45 estudiantes con 2-20 certs cada uno
- Promedio: ~9 certs por estudiante

### 9.3 Testing (seed_test_certs.py)

`scripts/seed_test_certs.py` — asigna certs manualmente a `est001`-`est045`. Idempotente (filter + create).

---

## 10. Tests

| Archivo | Tests | Cobertura |
|---|---|---|
| `test_certificaciones_auto.py` | 13 | get_user_stats, cumple_requisitos, verificar_y_otorgar |

Ejecutar:

```bash
python -m pytest core/tests/test_certificaciones_auto.py -v
```

**Cobertura detallada:**
- `get_user_stats`: 4 tests (lecciones, puntos, tasa, sin actividad)
- `cumple_requisitos`: 4 tests (vacio, todos, falta uno, no dict)
- `verificar_y_otorgar`: 5 tests (otorga, no otorga, idempotente, dry_run, signal)

**Helper de tests:** `_crear_leccion()` crea Curso → Modulo → Leccion con `orden` incremental (evita UNIQUE constraint `modulo_id + orden`).

---

## 11. Decisiones tecnicas

### 11.1 Signal con try/except

**Decision:** signal `auto_cert_al_completar` envuelve en `try/except Exception: pass`.

**Por que:** el otorgamiento de certs nunca debe bloquear el guardado de progreso. Si hay un bug en el servicio, el usuario sigue progresando; solo no recibe el cert hasta el proximo intento o el backfill.

### 11.2 Idempotencia por certificacion_id

**Decision:** `verificar_y_otorgar` filtra por certs ya obtenidas via `values_list("certificacion_id")`.

**Por que:** un usuario no puede tener el mismo cert dos veces. El `codigo_verificacion` es unico.

### 11.3 Dry-run obligatorio antes de masivo

**Decision:** `otorgar_certificaciones` soporta `--dry-run`.

**Por que:** 1,164 certs otorgados de golpe en v1.7.7. Si hay bug, es dificil de revertir. Dry-run permite auditar el output antes de ejecutar.

### 11.4 Helper _crear_leccion en tests

**Decision:** los tests usan `_crear_leccion()` que crea la jerarquia completa.

**Por que:** `Leccion` tiene `UNIQUE constraint modulo_id + orden`. Crear varias sin `orden` rompe el test con `IntegrityError`. El helper calcula `orden` como `Leccion.objects.filter(modulo=modulo).count() + 1`.

### 11.5 Codigo deterministico

**Decision:** el codigo de verificacion es `CERT-{user.id:04d}-{cert.id:04d}` (ej: `CERT-0125-0007`).

**Por que:** deterministico = auditable. Dado un user_id y cert_id, siempre genera el mismo codigo. No hay colisiones porque `user_id + cert_id` es unico.

---

## 12. Estado actual

| Aspecto | Estado |
|---|---|
| 49 certificaciones activas | OK |
| 1,311 certificaciones emitidas | OK |
| Auto-otorgamiento (signal) | OK |
| Management command + dry-run | OK |
| PDF + Word + preview | OK |
| Verificacion publica | OK |
| Admin registrado (list, filter, search) | OK |
| Notificacion al recibir | OK |
| 13 tests verdes | OK |
| Deploy productivo | Pendiente |

**Tag:** v1.7.7 (2026-10-26)
**Repo:** github.com/Hernank10/django-rhetorica-2026

---

Documento del modulo 15: sistema de certificaciones. 5 niveles, 49 certs activas, 1,311 emitidas, auto-otorgamiento, 13 tests.