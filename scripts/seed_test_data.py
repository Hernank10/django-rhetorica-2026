"""Seed de datos de prueba: usuarios, currículo, certificaciones, actividad.

Idempotente (get_or_create). Correr con:
    python manage.py shell -c "exec(open('scripts/seed_test_data.py', encoding='utf-8').read())"

Si un modelo falla por FieldError, ajustar el bloque correspondiente.
"""
import uuid
from datetime import date, timedelta

from django.contrib.auth.models import Group, User

from django.apps import apps

def M(nombre):
    """Resuelve un modelo de la app core por nombre, sin importar archivo."""
    return apps.get_model("core", nombre)

Certificacion = M("Certificacion")
CertificacionObtenida = M("CertificacionObtenida")
ContenidoJSON = M("ContenidoJSON")
Curso = M("Curso")
EjercicioLinguistico = M("EjercicioLinguistico")
EvaluacionCurso = M("EvaluacionCurso")
EvaluacionRedaccion = M("EvaluacionRedaccion")
Flashcard = M("Flashcard")
HistorialErrorSintactico = M("HistorialErrorSintactico")
Leccion = M("Leccion")
Logro = M("Logro")
LogroObtenido = M("LogroObtenido")
Modulo = M("Modulo")
PreguntaEvaluacion = M("PreguntaEvaluacion")
ProgresoCategoria = M("ProgresoCategoria")
ProgresoUsuario = M("ProgresoUsuario")
Recurso = M("Recurso")
Respuesta = M("Respuesta")
ResultadoEvaluacionCurso = M("ResultadoEvaluacionCurso")
Review = M("Review")
TecnicaLinguistica = M("TecnicaLinguistica")

# === Configuración (ajustable) ===
N_ADMINS = 3
N_PROFESORES = 9
N_ESTUDIANTES = 96
N_CURSOS = 15
N_MODULOS_POR_CURSO = 3
N_LECCIONES_POR_MODULO = 4
N_TECNICAS = 10
N_EJERCICIOS = 20
N_CERTIFICACIONES_CATALOGO = 45
N_CERTIFICACIONES_OBTENIDAS = 45
N_LOGROS = 10
N_FLASHCARDS_POR_EST = 2
N_RESPUESTAS_POR_EST = 5
N_PROGRESOS_POR_EST = 5
PASSWORD = "Test1234!"
RESET_PASSWORDS = True

print("=" * 60)
print("SEED DE DATOS DE PRUEBA")
print("=" * 60)


# === 1. Grupos ===
print("\n[1/8] Grupos...")
grupos = {}
for nombre in ("Administrador", "Profesor", "Estudiante"):
    g, _ = Group.objects.get_or_create(name=nombre)
    grupos[nombre] = g
print(f"  {len(grupos)} grupos OK")


# === 2. Usuarios ===
print("\n[2/8] Usuarios...")
users_admin = []
users_prof = []
users_est = []

for i in range(1, N_ADMINS + 1):
    username = f"admin{i:02d}"
    u, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@test.local",
            "first_name": f"Admin{i}",
            "last_name": "Test",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    if created or RESET_PASSWORDS:
        u.set_password(PASSWORD)
        u.is_staff = True
        u.is_superuser = True
        u.save()
    u.groups.add(grupos["Administrador"])
    users_admin.append(u)

for i in range(1, N_PROFESORES + 1):
    username = f"prof{i:02d}"
    u, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@test.local",
            "first_name": f"Prof{i}",
            "last_name": "Test",
        },
    )
    if created or RESET_PASSWORDS:
        u.set_password(PASSWORD)
        u.save()
    u.groups.add(grupos["Profesor"])
    users_prof.append(u)

for i in range(1, N_ESTUDIANTES + 1):
    username = f"est{i:03d}"
    u, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@test.local",
            "first_name": f"Est{i}",
            "last_name": "Test",
        },
    )
    if created or RESET_PASSWORDS:
        u.set_password(PASSWORD)
        u.save()
    u.groups.add(grupos["Estudiante"])
    users_est.append(u)

print(f"  {len(users_admin)} admins, {len(users_prof)} profes, {len(users_est)} estudiantes")


# === 3. Cursos ===
print("\n[3/8] Cursos...")
NIVELES = ["principiante", "intermedio", "avanzado", "experto"]
cursos = []
for i in range(1, N_CURSOS + 1):
    slug = f"curso-{i:02d}"
    nivel = NIVELES[(i - 1) % 4]
    curso, _ = Curso.objects.get_or_create(
        slug=slug,
        defaults={
            "titulo": f"Curso {i:02d} - {nivel.capitalize()}",
            "descripcion": f"Curso de prueba nivel {nivel}",
            "objetivo": "Dominar las técnicas del nivel",
            "nivel": nivel,
            "estado": "publicado",
            "duracion_estimada": 120,
            "puntos_totales": 1000,
            "creado_por": users_prof[i % len(users_prof)],
        },
    )
    cursos.append(curso)
print(f"  {len(cursos)} cursos")


# === 4. Módulos ===
print("\n[4/8] Módulos...")
modulos = []
for curso in cursos:
    for j in range(1, N_MODULOS_POR_CURSO + 1):
        mod, _ = Modulo.objects.get_or_create(
            curso=curso,
            orden=j,
            defaults={
                "titulo": f"Módulo {j} - {curso.titulo}",
                "descripcion": f"Módulo {j} del {curso.slug}",
            },
        )
        modulos.append(mod)
print(f"  {len(modulos)} módulos")


# === 5. Lecciones ===
print("\n[5/8] Lecciones...")
TIPOS_LECCION = ["teoria", "practica", "evaluacion", "mixto"]
lecciones = []
for mod in modulos:
    for k in range(1, N_LECCIONES_POR_MODULO + 1):
        lec, _ = Leccion.objects.get_or_create(
            modulo=mod,
            orden=k,
            defaults={
                "titulo": f"Lección {k} - {mod.titulo}",
                "contenido": f"Contenido de la lección {k}",
                "tipo": TIPOS_LECCION[(k - 1) % 4],
                "duracion_estimada": 30,
                "puntos": 100,
            },
        )
        lecciones.append(lec)
print(f"  {len(lecciones)} lecciones")


# === 6. Técnicas + Ejercicios ===
print("\n[6/8] Técnicas y ejercicios...")
CATEGORIAS = ["morfologia", "sintaxis", "lexico", "redaccion", "filologia"]
tecnicas = []
for i in range(1, N_TECNICAS + 1):
    tec, _ = TecnicaLinguistica.objects.get_or_create(
        nombre=f"Técnica {i:02d}",
        defaults={
            "descripcion": f"Técnica lingüística {i}",
            "categoria": CATEGORIAS[(i - 1) % 5],
            "nivel": (i - 1) % 4 + 1,
            "archivo_origen": "seed_test_data.py",
        },
    )
    tecnicas.append(tec)

ejercicios = []
for i in range(1, N_EJERCICIOS + 1):
    ej, _ = EjercicioLinguistico.objects.get_or_create(
        titulo=f"Ejercicio {i:02d}",
        defaults={
            "contenido": {"pregunta": f"¿Pregunta {i}?", "respuesta": f"Respuesta {i}"},
            "categoria": CATEGORIAS[(i - 1) % 5],
            "tipo": "multiple",
            "nivel": (i - 1) % 4 + 1,
            "puntos": 10,
            "es_adaptativo": False,
            "es_redaccion": False,
            "idioma": "ES",
        },
    )
    ejercicios.append(ej)

# Asociar técnicas y ejercicios a lecciones (round-robin)
for i, lec in enumerate(lecciones):
    lec.tecnicas_relacionadas.add(tecnicas[i % len(tecnicas)])
    lec.ejercicios_relacionados.add(ejercicios[i % len(ejercicios)])

# Asociar técnicas a cursos
for i, curso in enumerate(cursos):
    curso.tecnicas_relacionadas.add(tecnicas[i % len(tecnicas)])

print(f"  {len(tecnicas)} técnicas, {len(ejercicios)} ejercicios")
print("  Técnicas y ejercicios asociados a lecciones y cursos")

# === 7. Certificaciones catálogo ===
print("\n[7/8] Certificaciones catálogo...")
NIVELES_CERT = ["bronce", "plata", "oro", "platino", "diamante"]
certificaciones = []
for i in range(1, N_CERTIFICACIONES_CATALOGO + 1):
    cert, _ = Certificacion.objects.get_or_create(
        nombre=f"Certificación {i:02d}",
        defaults={
            "descripcion": f"Certificación nivel {NIVELES_CERT[(i - 1) % 5]}",
            "nivel": NIVELES_CERT[(i - 1) % 5],
            "requisitos": {"lecciones": i * 2, "puntos": i * 50},
            "imagen": f"cert_{i:02d}.png",
            "activa": True,
        },
    )
    certificaciones.append(cert)
print(f"  {len(certificaciones)} certificaciones catálogo")


# === 8. Actividad ===
print("\n[8/8] Actividad por app...")

# 8a. Logros catálogo
TIPOS_LOGRO = ["insignia", "medalla", "estrella", "certificacion"]
logros = []
for i in range(1, N_LOGROS + 1):
    log, _ = Logro.objects.get_or_create(
        nombre=f"Logro {i:02d}",
        defaults={
            "descripcion": f"Logro {i}",
            "tipo": TIPOS_LOGRO[(i - 1) % 4],
            "icono": f"icon_{i}.svg",
            "color": "#3B82F6",
            "puntos_requeridos": i * 100,
            "nivel_requerido": (i - 1) % 4 + 1,
            "ejercicios_completados_requeridos": i * 5,
            "tasa_aciertos_requerida": 0.7,
        },
    )
    logros.append(log)

# 8b. ContenidoJSON (una por categoría)
for cat in CATEGORIAS:
    ContenidoJSON.objects.get_or_create(
        nombre=f"contenido_{cat}",
        defaults={
            "archivo": f"contenido_{cat}.json",
            "datos": {"categoria": cat, "items": [1, 2, 3]},
            "categoria": cat,
        },
    )

# 8c. Recurso (uno por curso)
for curso in cursos:
    Recurso.objects.get_or_create(
        slug=f"recurso-{curso.slug}",
        defaults={
            "nombre": f"Recurso de {curso.titulo}",
            "archivo": f"recursos/{curso.slug}.pdf",
            "categoria": "material",
            "extension": "pdf",
            "tamaño_bytes": 1024,
            "curso": curso,
            "orden": 1,
            "destacado": False,
        },
    )

# 8d. Evaluaciones + EvaluacionCurso + Preguntas
TIPOS_EVAL = ["diagnostico", "formativa", "sumativa", "final"]
evaluaciones_curso_list = []
for i, curso in enumerate(cursos):
    tipo = TIPOS_EVAL[i % 4]
    evc, _ = EvaluacionCurso.objects.get_or_create(
        curso=curso,
        titulo=f"Evaluación {tipo} - {curso.slug}",
        defaults={
            "descripcion": f"Evaluación {tipo}",
            "tipo": tipo.replace("diagnostico", "diagnostica").replace("final", "final"),
            "preguntas_por_evaluacion": 3,
            "tiempo_limite": 60,
            "puntaje_maximo": 100,
            "intentos_permitidos": 3,
        },
    )
    evaluaciones_curso_list.append(evc)

    # 3 preguntas por evaluación
    for j in range(1, 4):
        PreguntaEvaluacion.objects.get_or_create(
            evaluacion=evc,
            orden=j,
            defaults={
                "enunciado": f"Pregunta {j} de {evc.titulo}",
                "tipo": "multiple",
                "opciones": ["a", "b", "c", "d"],
                "respuesta_correcta": "a",
                "puntaje": 33,
            },
        )

# 8e. Progreso + actividad por estudiante
for i, est in enumerate(users_est):
    # ProgresoUsuario (5 lecciones por estudiante)
    for k in range(N_PROGRESOS_POR_EST):
        lec = lecciones[(i * 5 + k) % len(lecciones)]
        ProgresoUsuario.objects.get_or_create(
            usuario=est,
            leccion=lec,
            defaults={
                "completado": True,
                "puntaje_obtenido": 80 + (k * 5),
                "intentos": 1,
                "tiempo_dedicado": 30,
            },
        )

    # ProgresoCategoria (3 categorías por estudiante)
    for cat in CATEGORIAS[:3]:
        ProgresoCategoria.objects.get_or_create(
            user=est,
            categoria=cat,
            defaults={
                "aciertos": 10 + i % 5,
                "intentos": 15,
                "nivel_dominio": (i % 4) + 1,
                "estrellas_obtenidas": i % 3,
            },
        )

    # Respuesta (5 por estudiante, con tipos variados)
    TIPOS_EJ = ["pos", "parafrasis", "reordenamiento", "registro", "redaccion"]
    for k in range(N_RESPUESTAS_POR_EST):
        Respuesta.objects.get_or_create(
            user=est,
            tipo_ejercicio=TIPOS_EJ[k % 5],
            item_id=1000 + i * 10 + k,
            defaults={
                "respuesta_usuario": f"respuesta_{k}",
                "es_correcta": (k % 2 == 0),
                "puntuacion": 10 if k % 2 == 0 else 0,
                "tiempo_segundos": 30 + k * 5,
                "intento_numero": 1,
                "feedback": "ok" if k % 2 == 0 else "revisar",
            },
        )

    # HistorialErrorSintactico (1 por estudiante)
    HistorialErrorSintactico.objects.get_or_create(
        estudiante=est,
        patron_error=f"patrón_{i % 5}",
        defaults={
            "idioma": "ES",
            "categoria_gramatical": "sintaxis",
            "frecuencia": 3,
            "resuelto": False,
        },
    )

    # EvaluacionRedaccion (1 por estudiante)
    EvaluacionRedaccion.objects.get_or_create(
        estudiante=est,
        ejercicio=ejercicios[i % len(ejercicios)],
        defaults={
            "texto_estudiante": f"Texto de prueba del estudiante {est.username}",
            "analisis_json": {"longitud": 50, "errores": 2},
            "aprobado": (i % 2 == 0),
            "feedback": "Buen trabajo" if i % 2 == 0 else "Mejorar",
        },
    )

    # Flashcard (N por estudiante) + Review
    for k in range(N_FLASHCARDS_POR_EST):
        fc, _ = Flashcard.objects.get_or_create(
            estudiante=est,
            frente=f"Frente {k} de {est.username}",
            defaults={
                "idioma": "ES",
                "tipo": "vocabulario",
                "reverso": f"Reverso {k}",
                "categoria_gramatical": "sustantivo",
            },
        )
        Review.objects.get_or_create(
            flashcard=fc,
            programada_para=date.today() + timedelta(days=k + 1),
            defaults={
                "calidad_respuesta": 4,
                "intervalo_dias": k + 1,
                "facilidad": 2.5,
                "repeticiones": 1,
            },
        )

    # LogroObtenido (2 por estudiante)
    for k in range(2):
        LogroObtenido.objects.get_or_create(
            user=est,
            logro=logros[(i + k) % len(logros)],
            defaults={"notificado": False},
        )

# 8f. Certificaciones obtenidas (45 distribuidas)
print("  Distribuyendo certificaciones obtenidas...")
for i in range(N_CERTIFICACIONES_OBTENIDAS):
    est = users_est[i % len(users_est)]
    cert = certificaciones[i % len(certificaciones)]
    codigo = f"CERT-{i + 1:04d}-{uuid.uuid4().hex[:8].upper()}"
    CertificacionObtenida.objects.get_or_create(
        user=est,
        certificacion=cert,
        defaults={
            "codigo_verificacion": codigo,
            "url_verificacion": f"https://example.com/verify/{codigo}",
        },
    )

print(f"  {len(logros)} logros catálogo")
print(f"  {N_CERTIFICACIONES_OBTENIDAS} certificaciones obtenidas")


# === RESUMEN ===
print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
modelos_a_contar = [
    User, Group, Curso, Modulo, Leccion, TecnicaLinguistica,
    EjercicioLinguistico, Certificacion, CertificacionObtenida,
    Logro, LogroObtenido, ContenidoJSON, Recurso, EvaluacionCurso,
    PreguntaEvaluacion, ProgresoUsuario, ProgresoCategoria, Respuesta,
    HistorialErrorSintactico, EvaluacionRedaccion, Flashcard, Review,
]
for m in modelos_a_contar:
    print(f"  {m.__name__:30s} {m.objects.count():>6d}")
print("=" * 60)
print("[OK] Seed completado")