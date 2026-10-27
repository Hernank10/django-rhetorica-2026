# Cómo construir un LMS educativo con Django y Python

## Un caso de estudio real: 400 técnicas, 1,311 certificaciones y 97% de cobertura

---

### Índice

1. El problema antes del código
2. Por qué Django y no otro framework
3. Los 4 modelos que sostienen todo
4. El patrón "data-driven": contenido en archivos Python
5. Los 5 tipos de ejercicio y su motor de evaluación
6. SM-2: repetición espaciada en 40 líneas
7. El sistema de certificaciones (manual + auto)
8. La arquitectura de roles: admin, profesor, estudiante
9. Tests que resisten 30 tags de evolución
10. Los 5 bugs recurrentes (y cómo prevenirlos)
11. Deploy: lo que nunca debes dejar para el final
12. Lecciones para tu propio proyecto

---

## 1. El problema antes del código

Antes de escribir una línea, hay que responder tres preguntas:

**¿Quién usa esto?** Tres roles con permisos radicalmente distintos:
- **Estudiante**: consume contenido, responde ejercicios, ve su progreso
- **Profesor**: ve estudiantes asignados, califica, genera reportes
- **Admin**: gestiona catálogo, emite certificaciones, audita

**¿Qué tipo de contenido?** Aquí decidí **técnicas pedagógicas autocontenidas**. Cada una tiene:
- Teoría formal (definición)
- Explicación (por qué funciona)
- Regla mnemotécnica (una frase)
- Ejemplo correcto + ejemplo incorrecto (contraste)
- Ejercicio evaluable

**¿Cómo se mide el progreso?** No con un simple "completado/no completado". Uso **SM-2**, el algoritmo de SuperMemo, que calcula cuándo revisar cada técnica para maximizar retención.

Estas tres decisiones definieron la arquitectura. Todo lo demás es consecuencia.

---

## 2. Por qué Django y no otro framework

Django no es "el mejor framework para LMS" (no existe tal cosa). Es el framework que **encaja con este proyecto específico** por cinco razones:

### 2.1 Modelos + migraciones automáticas

Un LMS tiene al menos 8-10 tablas relacionadas (users, courses, lessons, exercises, progress, certificates...). Django genera las migraciones SQL automáticamente:

```python
# Cambias esto:
class TecnicaGramatical(models.Model):
    nivel = models.CharField(max_length=20, choices=NIVELES)

# Django crea esto:
# migrations/0021_alter_nivel.py
operations = [
    migrations.AlterField(
        model_name='tecnicagramatical',
        name='nivel',
        field=models.CharField(choices=[...], max_length=20),
    ),
]
```

En el proyecto hay **22 migraciones** que se aplicaron sin escribir una línea de SQL.

### 2.2 Admin panel gratis

El módulo `django.contrib.admin` es un backoffice completo. Con 3 líneas registras un modelo:

```python
# core/admin.py
@admin.register(CertificacionObtenida)
class CertificacionObtenidaAdmin(admin.ModelAdmin):
    list_display = ("user", "certificacion", "fecha_obtenida", "codigo_verificacion")
    list_filter = ("certificacion", "fecha_obtenida")
    search_fields = ("user__username", "codigo_verificacion")
```

Y obtienes tabla, filtros, búsqueda y formulario. Eso son **días de desarrollo** ahorrados.

### 2.3 Autenticación incluida

Django trae `User`, `Group`, `Permission`, login, logout, password hashing. En este proyecto los roles son grupos:

```python
grupo_prof = Group.objects.get_or_create(name="Profesor")[0]
grupo_est = Group.objects.get_or_create(name="Estudiante")[0]
user.groups.add(grupo_prof)  # ahora es profesor
```

Y decoradores:

```python
@profesor_required  # custom, en core/decorators.py
def lista_certificaciones(request):
    ...
```

### 2.4 ORM expresivo

Las queries que necesitarías en SQL crudo se escriben así:

```python
# "Cuántos certificados tiene cada estudiante del profesor X"
from django.db.models import Count
profesor = User.objects.get(username="prof01")
estudiantes = User.objects.filter(
    groups__name="Estudiante"
).annotate(
    total_certs=Count("certificaciones_obtenidas")
).order_by("-total_certs")
```

Sin SQL. Y con `.filter()` anidable, joins automáticos, `select_related` para evitar N+1.

### 2.5 Tests con `TestCase` + `client`

No necesitas herramientas externas. El test es:

```python
from django.test import TestCase
from django.urls import reverse

class TestIndice(TestCase):
    def test_200(self):
        r = self.client.get(reverse("gramatica:indice"))
        self.assertEqual(r.status_code, 200)
```

`self.client` simula un navegador. `reverse` resuelve URL names. `self.assertEqual` es unittest. Todo incluido.

**Contras honestas de Django:** es monólito, no es "sexy" como Next.js, el ORM puede ocultar ineficiencias, y no escala horizontalmente sin pensarlo. Para un LMS pequeño-mediano, es la mejor elección. Para un LMS con 10M de usuarios, no.

---

## 3. Los 4 modelos que sostienen todo

Todo el sistema se construye sobre 4 modelos (más los auxiliares). Si los diseñas bien, el resto es trivial. Si los diseñas mal, todo duele.

### 3.1 `TecnicaGramatical` (el contenido)

```python
class TecnicaGramatical(models.Model):
    numero = models.IntegerField(unique=True)      # PK semántica (1-400)
    bloque = models.CharField(max_length=1)         # A-G
    titulo = models.CharField(max_length=200)
    teoria = models.TextField()
    explicacion = models.TextField()
    regla = models.TextField()
    ejemplo_correcto = models.TextField()
    ejemplo_incorrecto = models.TextField()
    nivel = models.CharField(...)                   # basico|intermedio|avanzado
    modulo = models.CharField(...)                  # gramatica|generativa|a1|b1
```

**Decisión clave:** `numero` es una PK semántica (`unique=True`) **además** del `id` auto. Esto permite:
- Reordenar técnicas sin romper URLs (`/tecnica/<numero>/`)
- Añadir técnicas en medio sin renumerar
- Referencias estables en seeds y tests

**Decisión arriesgada pero exitosa:** un solo modelo para 4 módulos, distinguidos por `modulo`. Al principio parecía mal (¿por qué A1 y B1 comparten modelo si son currículos distintos?). Pero todos tienen la misma estructura: teoría + regla + ejemplo + ejercicio. Cuatro tablas = 4x mantenimiento sin ganancia.

### 3.2 `EjercicioGramatical` (la evaluación)

```python
class EjercicioGramatical(models.Model):
    tecnica = models.ForeignKey(TecnicaGramatical, related_name="ejercicios")
    tipo = models.IntegerField(choices=TIPOS)       # 1-5
    orden = models.IntegerField(default=1)
    payload = models.JSONField()

    class Meta:
        unique_together = ("tecnica", "orden")
```

**Por qué `payload` es JSON y no columnas separadas:** cada tipo de ejercicio tiene estructura distinta.

```python
# Tipo 1 (opción múltiple)
{"enunciado": "...", "opciones": [{"id": "a", "correcta": True}], ...}

# Tipo 3 (clasificación)
{"enunciado": "...", "oraciones": [...], "categorias": ["..."]}
```

Si tuviera `opciones_json`, `oraciones_json`, `categorias_json`, sería un caos de columnas nulas. **JSONField es la respuesta cuando la estructura varía por tipo.**

### 3.3 `ProgresoGramatical` (el estado)

```python
class ProgresoGramatical(models.Model):
    usuario = models.ForeignKey(User)
    tecnica = models.ForeignKey(TecnicaGramatical)
    intentos = models.IntegerField(default=0)
    aciertos_consecutivos = models.IntegerField(default=0)
    estado = models.CharField(...)                  # no_iniciada|en_progreso|dominada
    sm2_ef = models.FloatField(default=2.5)
    sm2_interval = models.IntegerField(default=0)
    sm2_repetitions = models.IntegerField(default=0)
    proxima_revision = models.DateTimeField(null=True)
    ultima_revision = models.DateTimeField(null=True)

    class Meta:
        unique_together = ("usuario", "tecnica")
```

**`unique_together` es crítico.** Sin él, dos clicks rápidos crean dos filas y el progreso se corrompe.

### 3.4 `CertificacionObtenida` (la evidencia)

```python
class CertificacionObtenida(models.Model):
    user = models.ForeignKey(User)
    certificacion = models.ForeignKey(Certificacion)
    fecha_obtenida = models.DateTimeField()
    codigo_verificacion = models.CharField(unique=True)  # CERT-0125-0007
    url_verificacion = models.URLField(null=True, blank=True)
```

**`codigo_verificacion` es único**. Esto es auditable: dado un código, existe exactamente un certificado. No hay duplicados.

---

## 4. El patrón "data-driven": contenido en archivos Python

Uno de los problemas más difíciles en LMS es **versionar y revisar contenido**. Si el contenido vive en la DB, cualquier cambio requiere SQL o admin panel manual. Si vive en código, es git-friendly.

**Solución en este proyecto:** contenido en archivos Python.

```python
# core/data/tecnicas_a1.py
TECNICAS = [
    {
        "numero": 201, "bloque": "A", "modulo": "a1",
        "titulo": "El alfabeto español: 27 letras",
        "teoria": "El alfabeto español tiene 27 letras...",
        "explicacion": "...",
        "regla": "...",
        "ejemplo_correcto": "...",
        "ejemplo_incorrecto": "...",
    },
    # ... 99 más
]
```

Y un seed los carga idempotentemente:

```python
# scripts/seed_a1.py
for t in TECNICAS:
    TecnicaGramatical.objects.update_or_create(
        numero=t["numero"],
        defaults={k: v for k, v in t.items() if k != "numero"},
    )
```

**Ventajas:**
- Git diff sobre el contenido: ves exactamente qué técnica cambió
- Revisión de PR: cada técnica es un cambio auditable
- Rollback: `git checkout HEAD~1 -- core/data/tecnicas_a1.py`
- Sin migración de DB para añadir contenido (solo el seed)

**Desventajas:**
- Cambiar contenido requiere código (no UI)
- Un admin no técnico no puede añadir técnicas
- El archivo Python crece (100 técnicas ≈ 60 KB)

### 4.1 La regla de las claves ASCII (lección aprendida a golpes)

**Regla absoluta:** las claves del diccionario van en **ASCII**, los valores llevan tildes normales.

```python
# ✅ Correcto
{"numero": 301, "teoria": "El presente de indicativo..."}

# ❌ Incorrecto (rompe el seed)
{"número": 301, "teoría": "El presente de indicativo..."}
```

**Por qué:** un script que reemplazó masivamente tildes convirtió `"numero"` en `"número"`, y el seed falló con `KeyError: 'numero'`. La lección: **nunca metas tildes en claves de dict Python que vayas a acceder programáticamente**.



---

## 5. Los 5 tipos de ejercicio y su motor de evaluación

Un LMS serio necesita más que "opción múltiple". Pero tampoco necesita 20 tipos. Aquí hay 5:

| Tipo | Nombre | Evalúa | Complejidad |
|---|---|---|---|
| 1 | Opción múltiple + justificación | Reconocimiento | Baja |
| 2 | Corrección inline | Producción ortográfica | Media |
| 3 | Clasificación (emparejar) | Comprensión de categorías | Baja |
| 4 | Construcción guiada | Producción sintáctica | Alta |
| 5 | Detección de error | Análisis crítico | Alta |

### 5.1 El motor de evaluación (determinista)

Archivo: `core/services/sintaxis.py`

```python
def evaluar_ejercicio(ejercicio, respuesta, usuario=None):
    """Evalúa según tipo. Retorna {ok, feedback, regla, ejemplo_correcto}."""
    tipo = ejercicio.tipo
    if tipo == 1:
        return _evaluar_tipo1(ejercicio, respuesta)
    elif tipo == 2:
        return _evaluar_tipo2(ejercicio, respuesta)
    # ...
```

**Decisión crítica: cero LLM.** El motor es 100% determinista. Esto significa:
- **Reproducibilidad:** la misma respuesta produce el mismo feedback siempre
- **Explicabilidad:** cada decisión tiene un `razon` trazable
- **Costo cero:** sin API externa
- **Latencia predecible:** ~50ms por evaluación

**Trade-off:** si el estudiante da una respuesta válida no contemplada, el motor la rechaza. Mitigación: **fuzzy match con `SequenceMatcher`**.

```python
def _normalizar(texto):
    """Lowercase, sin acentos, sin puntuación."""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"[^\w\s]", "", texto).strip()

def _fuzzy_match(a, b):
    """Ratio de similitud entre dos strings normalizados."""
    return SequenceMatcher(None, _normalizar(a), _normalizar(b)).ratio()
```

Con umbrales distintos por tipo:
- Tipo 1 (justificación libre): 0.5 — variantes libres
- Tipo 2 (corrección): 0.85 — variantes ortográficas
- Tipo 4 (construcción): 0.85 + conector como palabra separada

### 5.2 El caso especial del tipo 4

El tipo 4 (construir oración) requiere 3 pasos:

```python
def _evaluar_tipo4(ejercicio, respuesta):
    # 1. Exact match normalizado
    if _normalizar(respuesta) == _normalizar(ejercicio.payload["respuesta_correcta"]):
        return {"ok": True, ...}

    # 2. Conector debe estar como palabra separada
    conector = ejercicio.payload["conector"]
    if not re.search(r"\b" + re.escape(conector) + r"\b", respuesta.lower()):
        return {"ok": False, "feedback": f"Falta el conector '{conector}'."}

    # 3. Fuzzy match contra respuesta canónica
    ratio = _fuzzy_match(respuesta, ejercicio.payload["respuesta_correcta"])
    if ratio >= 0.85:
        return {"ok": True, ...}

    return {"ok": False, ...}
```

**Sin el paso 2**, "Juan Pedro vienen" (sin "y") tenía fuzzy 0.79 y pasaba con umbral 0.75. El conector como palabra separada lo arregla.

---

## 6. SM-2: repetición espaciada en 40 líneas

El algoritmo SM-2 (SuperMemo 2, 1987) es el estándar de la industria. Implementación completa:

```python
def _actualizar_sm2(progreso, calidad):
    """
    calidad: 0-5.
    0 = negro total, 3 = correcto con esfuerzo, 5 = perfecto.
    """
    ef = progreso.sm2_ef
    ef = ef + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02))
    progreso.sm2_ef = max(1.3, ef)  # piso

    if calidad < 3:
        # Fallo: resetear
        progreso.sm2_repetitions = 0
        progreso.sm2_interval = 1
    else:
        # Acierto: incrementar
        progreso.sm2_repetitions += 1
        if progreso.sm2_repetitions == 1:
            progreso.sm2_interval = 1
        elif progreso.sm2_repetitions == 2:
            progreso.sm2_interval = 6
        else:
            progreso.sm2_interval = round(
                progreso.sm2_interval * progreso.sm2_ef
            )

    progreso.proxima_revision = timezone.now() + timedelta(
        days=progreso.sm2_interval
    )
```

### 6.1 Cómo se mapea calidad

```python
if not ok:
    calidad = 1      # fallo
elif ejercicio.tipo in (4, 5):
    calidad = 4      # acierto en producción (más meritorio)
else:
    calidad = 3      # acierto en reconocimiento
```

### 6.2 Cómo se marca "dominada"

```python
if (progreso.aciertos_consecutivos >= 3
        and ejercicio.tipo in (4, 5)
        and ok):
    progreso.estado = "dominada"
```

**3 aciertos consecutivos en ejercicios de producción** = dominada. Los tipos 1-3 son reconocimiento, no cuentan solos.

### 6.3 Por qué SM-2 y no SM-5, SM-8, FSRS

SM-2 tiene 5 parámetros y 40 líneas. FSRS (2022) tiene 17 parámetros y requiere entrenar con datos históricos. Para un LMS **sin usuarios aún**, SM-2 es lo correcto: funciona, es auditable, y si migras a FSRS después, la migración es trivial (mismo modelo de datos).

---

## 7. El sistema de certificaciones (manual + auto)

Este fue el sistema más complejo del proyecto. Dos capas:

### 7.1 Capa manual (v1.7.5)

Admin panel o seed crea `CertificacionObtenida` manualmente:

```python
CertificacionObtenida.objects.create(
    user=user,
    certificacion=cert,
    fecha_obtenida=timezone.now(),
    codigo_verificacion=f"CERT-{user.id:04d}-{cert.id:04d}",
    url_verificacion=f"/verificar/CERT-{user.id:04d}-{cert.id:04d}/",
)
```

El `signal notif_certificacion` dispara una notificación al estudiante.

### 7.2 Capa automática (v1.7.7)

El servicio `verificar_y_otorgar` es el cerebro:

```python
def verificar_y_otorgar(user, dry_run=False):
    """Otorga certs pendientes. Idempotente."""
    stats = get_user_stats(user)  # {lecciones, puntos, tasa}

    ya_obtenidas = CertificacionObtenida.objects.filter(
        user=user
    ).values_list("certificacion_id", flat=True)

    pendientes = Certificacion.objects.filter(activa=True).exclude(
        id__in=ya_obtenidas
    )

    nuevas = []
    for cert in pendientes:
        if cumple_requisitos(stats, cert.requisitos):
            nuevas.append(cert)
            if not dry_run:
                CertificacionObtenida.objects.create(
                    user=user, certificacion=cert, ...
                )
    return nuevas
```

### 7.3 El signal que dispara automáticamente

```python
@receiver(post_save, sender=ProgresoUsuario)
def auto_cert_al_completar(sender, instance, created, **kwargs):
    """Cuando el estudiante completa una lección, verifica certs."""
    if not getattr(instance, "completado", False):
        return
    from core.services.certificaciones import verificar_y_otorgar
    try:
        verificar_y_otorgar(instance.usuario)
    except Exception:
        pass  # NUNCA rompe el flujo de progreso
```

**`try/except Exception: pass`** es deliberado. Un bug en el servicio de certificaciones no debe romper el guardado de progreso del estudiante. Los certs se otorgan en el siguiente intento o con un backfill manual.

### 7.4 El management command (backfill)

```bash
python manage.py otorgar_certificaciones           # todos los usuarios
python manage.py otorgar_certificaciones --user est001  # uno
python manage.py otorgar_certificaciones --dry-run     # auditar
```

**En este proyecto, el dry-run predijo 1,164 certs, la ejecución real creó exactamente 1,164.** Auditable.

### 7.5 Los requisitos como JSON

Cada certificación define sus requisitos:

```python
{"lecciones": 30, "puntos": 750, "tasa": 75}
```

El servicio evalúa **todos los presentes**:

```python
def cumple_requisitos(stats, requisitos):
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

---

## 8. La arquitectura de roles: admin, profesor, estudiante

### 8.1 Los tres roles

No son tablas separadas. Son `Group` de Django:

```python
grupo_admin = Group.objects.get_or_create(name="Admin")[0]
grupo_prof = Group.objects.get_or_create(name="Profesor")[0]
grupo_est = Group.objects.get_or_create(name="Estudiante")[0]
```

Y los decoradores controlan acceso:

```python
def profesor_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"/login/?next={request.path}")
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped
```

### 8.2 El patrón de la vista compartida

Uno de los patrones más valiosos del proyecto: **una sola vista renderiza 4 módulos**.

```python
def tecnica(request, numero):
    t = get_object_or_404(TecnicaGramatical, numero=numero)

    if t.modulo == "generativa":
        bname = BLOQUES_GENERATIVA.get(t.bloque, "")
    elif t.modulo == "a1":
        bname = BLOQUES_A1.get(t.bloque, "")
    elif t.modulo == "b1":
        bname = BLOQUES_B1.get(t.bloque, "")
    else:
        bname = BLOQUES_INFO.get(t.bloque, "")

    return render(request, "core/gramatica/tecnica.html", {
        "tecnica": t, "bloque_nombre": bname,
        "es_a1": t.modulo == "a1",
        "es_b1": t.modulo == "b1",
        "es_generativa": t.modulo == "generativa",
    })
```

**Por qué funciona:** los 4 currículos tienen la **misma estructura** (teoría + ejercicio + navegación). Cuatro vistas separadas serían 4x mantenimiento por cero ganancia.

### 8.3 El dashboard del profesor y su bug de `groups`

Un bug clásico que ejemplifica el diseño:

```python
# ❌ Mi código original (roto)
estudiantes = User.objects.filter(
    grupos__name="Estudiante"  # 'grupos' no existe
)

# ✅ Fix
estudiantes = User.objects.filter(
    groups__name="Estudiante"  # Django hardcodea 'groups' en inglés
)
```

**Django usa nombres en inglés para sus campos internos**: `groups`, `permissions`, `user_permissions`. No los tradujo ni siquiera cuando el resto del proyecto está en español. Lección: **siempre verifica los nombres de campos reverse de Django** con `_meta.get_fields()`.


---

## 9. Tests que resisten 30 tags de evolución

**~1,320 tests, 97%+ coverage.** Pero lo importante no es el número: es que **los tests sobrevivieron 30 tags sin reescribirse**.

### 9.1 El patrón "dinámico"

**Regla:** los tests de data verifican **rangos**, no números hardcodeados.

```python
# ❌ Mal (se rompe al añadir técnicas)
def test_total(self):
    self.assertEqual(len(TECNICAS), 15)

# ✅ Bien (aguanta hasta 100)
def test_total(self):
    self.assertGreaterEqual(len(TECNICAS), 15)
    self.assertLessEqual(len(TECNICAS), 100)

# ✅ Mejor (rango consecutivo dinámico)
def test_numeros_consecutivos(self):
    nums = sorted(t["numero"] for t in TECNICAS)
    inicio = min(nums)
    self.assertEqual(inicio, 201)
    self.assertEqual(nums, list(range(inicio, inicio + len(nums))))
```

**Por qué importa:** durante v1.6.0 se añadieron 15 técnicas en bloque A, después 15 en B, después 20 en C... Si el test hardcodea `== 15`, se rompe 6 veces. El dinámico no se rompe nunca.

### 9.2 El helper que arma jerarquías

Un test que crea una `Leccion` requiere `Curso → Modulo → Leccion` por el `UNIQUE constraint modulo_id + orden`. Helper:

```python
def _crear_leccion(titulo="Leccion test", puntos=10, contenido="x"):
    """Crea la jerarquía completa y devuelve la Leccion."""
    curso, _ = Curso.objects.get_or_create(titulo="Curso test")
    modulo, _ = Modulo.objects.get_or_create(curso=curso, titulo="Modulo test")
    orden = Leccion.objects.filter(modulo=modulo).count() + 1
    return Leccion.objects.create(
        modulo=modulo, titulo=titulo, contenido=contenido,
        puntos=puntos, orden=orden,  # ← crítico: orden incremental
    )
```

Sin el `orden` incremental, 3 lecciones en el mismo módulo = `IntegrityError`.

### 9.3 El patrón de cobertura quirúrgica

Cuando el coverage baja a 96.8%, no se resuelve con tests genéricos. Se resuelve con **tests que apuntan a branches específicos**:

```python
class TestCoverageBranches(TestCase):
    def test_cumple_requisitos_falla_puntos(self):
        """Cubre línea 46: falla por puntos insuficientes."""
        stats = {"lecciones": 10, "puntos": 100, "tasa": 80}
        self.assertFalse(cumple_requisitos(stats, {"puntos": 200}))
```

Seis tests así subieron de 96.78% a **97.04%**. Cada uno cubre 1-3 líneas específicas.

### 9.4 Los tests como red de seguridad

Los tests que más valen son los que detectaron bugs reales:

- `test_profesor_ve_certificaciones`: detectó el bug `grupos` vs `groups`
- `test_gramatica_views.py::TestIndice`: detectó que `'Gramatica'` vs `'Gramática'` rompía el template post-fix
- `test_signal_dispara_otorgamiento`: garantiza que el signal de certificaciones funciona

Sin estos tests, los 3 bugs hubieran llegado a producción.

---

## 10. Los 5 bugs recurrentes (y cómo prevenirlos)

**Regla del proyecto:** cada bug se convierte en una regla documentada que no se repite.

### 10.1 Bug: colisión de numeración

**Caso:** v1.5.0, técnicas generativas con número 1-100 sobreescribieron técnicas de gramática.

**Fix:** renumerar a 101-200. Regla: **cada módulo tiene su rango fijo**.

### 10.2 Bug: tildes en claves de dict

**Caso:** v1.5.2, un script de "fix de tildes" masivo convirtió `"numero"` en `"número"`. El seed falló con `KeyError: 'numero'`.

**Fix:** revertir con patrón exacto `"clave":` + manual. Regla: **claves ASCII, valores con tildes**.

### 10.3 Bug: `groups` vs `grupos`

**Caso:** v1.7.5, filtro de certificaciones por profesor usó `grupos__name` (español). Django usa `groups` (inglés).

**Fix:** `groups__name`. Regla: **siempre verificar campos reverse con `_meta.get_fields()` antes de asumir**.

### 10.4 Bug: tests hardcodeados

**Caso:** v1.6.0-alpha, tests de A1 hardcodeados a `== 15`. Se rompieron en cada bloque nuevo.

**Fix:** tests dinámicos con `assertGreaterEqual` + rango. Regla: **los tests de data no hardcodean totales**.

### 10.5 Bug: comillas dobles dentro de string Python

**Caso:** v1.7.0 (bloque C2), un string `"Dijo: "Vengo""` rompió Python con `SyntaxError`.

**Fix:** usar `«...»` (guillemets) o `'...'` (comillas simples) dentro del string. Regla: **`"` dentro de `"..."` siempre escapa como `\"` o usa `«...»`**.

### 10.6 Bug del proyecto: `AppendAllText` sin `\n`

**Caso:** escribir docs en chunks fusionaba headers (`---## 3.` en una línea).

**Fix:** cada `AppendAllText` empieza con `` "`n`n" + $content ``. Regla: **los appends siempre añaden separador**.

---

## 11. Deploy: lo que nunca debes dejar para el final

**El error más grande del proyecto:** tener 400 técnicas en `localhost` después de 30 tags sin deployar.

### 11.1 El stack de producción

- **Cloudflare R2** para estáticos (bucket + token + URL pública)
- **Render** para web service (Gunicorn) + PostgreSQL
- **dj-database-url** para parsear `DATABASE_URL`
- **django-storages + boto3** para R2

### 11.2 El fix específico de R2

Cloudflare R2 no soporta el checksum SHA256 que boto3 usa por defecto. Sin este fix, las subidas fallan con `SignatureDoesNotMatch`:

```python
# django_retorica/settings/prod.py
AWS_S3_CLIENT_CONFIG = {
    "request_checksum_calculation": "when_required",
    "response_checksum_validation": "when_required",
}
```

### 11.3 Los 14 env vars de Render

```
PYTHON_VERSION=3.12.4
DJANGO_SETTINGS_MODULE=django_retorica.settings.prod
DEBUG=False
SECRET_KEY=<generar con secrets.token_urlsafe(50)>
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://rhetorica-plus.onrender.com
DATABASE_URL=<internal de Render>
USE_S3=True
AWS_ACCESS_KEY_ID=<R2>
AWS_SECRET_ACCESS_KEY=<R2>
AWS_STORAGE_BUCKET_NAME=rhetorica-media
AWS_S3_ENDPOINT_URL=https://<ACCOUNT_ID>.r2.cloudflarestorage.com
AWS_S3_REGION_NAME=auto
AWS_S3_CUSTOM_DOMAIN=https://pub-xxxx.r2.dev
```

### 11.4 El seed de producción

```bash
python manage.py createsuperuser
python manage.py migrate
python scripts/seed_tecnicas_sintaxis.py
python scripts/seed_tecnicas_gramatica.py
python scripts/seed_generativa.py
python scripts/seed_a1.py
python scripts/seed_b1.py
```

**Los mismos seeds de desarrollo, sin cambios.** Ese es el poder de los seeds idempotentes.

### 11.5 La lección de deploy

**Deploya v0.1, no v1.0.** El primer deploy debe ir cuando el MVP funciona, no cuando está "completo". Porque:
- Detecta problemas reales (CORS, SMTP, sesión, latencia)
- Te da feedback de usuarios reales
- Convierte "código" en "producto"

**En este proyecto, fue un error.** 400 técnicas + 1,311 certificados + 97% coverage sin URL pública es trabajo sin validación.

---

## 12. Lecciones para tu propio proyecto LMS

### 12.1 Empieza con los 4 modelos

No con vistas, no con templates, no con features. Con:

1. **Content** (técnica, lección, curso)
2. **Exercise** (evaluación)
3. **Progress** (estado del usuario)
4. **Evidence** (certificado, logro)

Si estos 4 están bien diseñados, todo lo demás fluye.

### 12.2 Contenido en archivos, no en DB

Al menos para el MVP. Cambiar de data-driven a editor visual es fácil. Lo contrario es un infierno de migraciones.

### 12.3 Motor determinista, no LLM

Un LLM es tentador para evaluación semántica. Pero: costo variable, latencia impredecible, falsos positivos difíciles de auditar, imposible de versionar. Para LMS básico, motor determinista + fuzzy match resuelve el 90% de casos.

### 12.4 SM-2 desde el día 1

Es 40 líneas de código y cambia radicalmente la UX. Estudiantes con SM-2 vuelven; sin SM-2, olvidan y no vuelven.

### 12.5 Tests dinámicos, no hardcodeados

Si vas a añadir contenido progresivamente (y siempre se añade), los tests deben crecer con el contenido. `assertGreaterEqual` + rango, no `assertEqual == N`.

### 12.6 Deploya antes de la tercera feature

Los primeros dos módulos son para validar el diseño. Si el tercero llega sin deploy, es señal de sobre-ingeniería.

### 12.7 Un solo módulo de evaluación

Todos los tipos de ejercicio (1-5) viven en **un archivo** (`services/sintaxis.py`) y lo usan **todos los módulos**. Cero duplicación. Cualquier mejora beneficia a todos.

### 12.8 Documenta cada bug como regla

Cada bug que resolví se convirtió en una regla del proyecto. Sin documentación, el bug vuelve en 3 meses.

### 12.9 Sobre el tamaño del proyecto

400 técnicas es "mucho". Pero **no fue difícil**, porque:
- 15 técnicas = 1 archivo Python de ~5 KB
- 100 técnicas = 4 archivos de ~60 KB
- 400 técnicas = 15 archivos de ~60 KB

La dificultad no creció linealmente con el contenido. Creció con la **complejidad estructural** (roles, certificaciones, SM-2).

### 12.10 Sobre el tiempo

30+ tags, ~5 meses de trabajo intermitente, ~1,300 tests, 97% coverage.

**El 80% del valor se entregó en las primeras 4 semanas** (v1.0 a v1.2: sintaxis funcionando). El otro 20% (currículos A1, B1, certificaciones, docs) tomó el 80% del tiempo.

**Lección:** no esperes a tener 400 técnicas para deployar. Deploya con 100, con 50, con 10. **El primer deploy es el que más cuesta. Los siguientes son rutinarios.**

---

## Cierre

`django-rhetorica-2026` es un LMS completo en 15 tablas, 15 archivos de datos, 4 servicios, 5 tipos de ejercicio, 2 sistemas de certificación, 3 roles y **cero deuda técnica conocida**. Los bugs recurrentes están documentados. El contenido vive en git. Los tests resisten 30 tags de evolución.

Pero no es un producto exitoso todavía. **Es un código excelente en `localhost`.** El éxito empieza con el primer usuario real que lo usa y dice "no entiendo" — y tú puedes responder arreglando lo que falta.

**La distancia entre "proyecto técnico bien hecho" y "producto educativo real" es de 1 URL pública.** Todo lo demás ya está.

---

*Artículo escrito el 27 de octubre de 2026. Repo: `github.com/Hernank10/django-rhetorica-2026`. Próximo tag: `v1.8.0` (post-deploy).*

