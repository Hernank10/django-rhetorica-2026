"""
Seed extendido: 12 cursos, 48 módulos, 144 lecciones, 12 evaluaciones,
60 preguntas, 10 logros, 4 certificaciones, inscripciones y progreso.

Uso:  python manage.py seed_content
      python manage.py seed_content --reset
"""
import random
import time
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import (
    Certificacion,
    CertificacionObtenida,
    Logro,
    LogroObtenido,
    Respuesta,
)
from core.models_cursos import (
    Curso,
    EvaluacionCurso,
    Leccion,
    Modulo,
    PreguntaEvaluacion,
    ProgresoUsuario,
)

User = get_user_model()
SEED = 42

# ------------------------- DATOS BASE -------------------------
CURSOS = [
    ("Morfología", "basico",        "Estructura de las palabras: raíz, prefijos y sufijos."),
    ("Sintaxis",   "basico",        "Orden y función de las palabras en la oración."),
    ("Ortografía", "basico",        "Uso correcto de tildes, grafías y signos."),
    ("Redacción",  "intermedio",    "Cómo escribir textos claros, cohesionados y coherentes."),
    ("Retórica",   "intermedio",    "Arte de persuadir: figuras, tropos y estructura del discurso."),
    ("Etimología", "intermedio",    "Origen y evolución de las palabras del español."),
    ("Comprensión Lectora", "basico",  "Estrategias para entender y analizar textos."),
    ("Literatura",          "intermedio", "Panorama de géneros, autores y movimientos."),
    ("Poesía",              "intermedio", "Métrica, rima, verso libre y figuras poéticas."),
    ("Ensayo",              "avanzado",   "Argumentación, tesis, evidencia y estilo ensayístico."),
    ("Oratoria",            "avanzado",   "Hablar en público: voz, cuerpo y estructura."),
    ("Argumentación",       "avanzado",   "Construir y refutar argumentos con lógica."),
]

MODULOS_POR_CURSO = [
    ("Fundamentos",       "Conceptos básicos y vocabulario esencial."),
    ("Profundización",    "Detalles y casos avanzados."),
    ("Práctica",          "Ejercicios guiados y aplicados."),
    ("Evaluación",        "Prueba de dominio del curso."),
]

LECCIONES_POR_MODULO = [
    ("Introducción",  "lectura",  15, 10),
    ("Conceptos clave", "lectura", 20, 15),
    ("Ejercicios prácticos", "practica", 25, 20),
]

LOGROS = [
    ("Primer paso",         "Completa tu primera lección.",         "insignia",      "🌱", "#4ade80",  0,   1, "",  1,  0),
    ("Estudiante aplicado", "Completa 10 lecciones.",               "insignia",      "📚", "#60a5fa",  0,   1, "", 10,  0),
    ("Cien aciertos",       "Consigue 100 respuestas correctas.",   "medalla",       "💯", "#fbbf24",  0,   1, "",  0,  0),
    ("Racha perfecta",      "Alcanza 90% de aciertos.",             "medalla",       "🎯", "#f472b6",  0,   1, "",  0, 90),
    ("100 puntos",          "Acumula 100 puntos.",                  "estrella",      "⭐", "#facc15",100,   1, "",  0,  0),
    ("500 puntos",          "Acumula 500 puntos.",                  "estrella",      "🌟", "#f59e0b",500,   1, "",  0,  0),
    ("1000 puntos",         "Acumula 1000 puntos.",                 "estrella",      "✨", "#eab308",1000,  1, "",  0,  0),
    ("Experto",             "Alcanza el nivel 3.",                  "insignia",      "🎓", "#8b5cf6",  0,   3, "",  0,  0),
    ("Sabio",               "Alcanza el nivel 5.",                  "insignia",      "🧙", "#a855f7",  0,   5, "",  0,  0),
    ("Políglota",           "Usa la plataforma en 5 idiomas.",      "certificacion", "🌍", "#06b6d4",  0,   1, "",  0,  0),
]

CERTIFICACIONES = [
    ("Iniciación a la Retórica",   "basico",      {"lecciones": 5}),
    ("Comprensión Lectora",        "intermedio",  {"lecciones": 20, "tasa": 70}),
    ("Redacción Profesional",      "intermedio",  {"lecciones": 30, "tasa": 75}),
    ("Maestría Retórica",          "avanzado",    {"lecciones": 50, "tasa": 85}),
]


class Command(BaseCommand):
    help = "Seed extendido: cursos, módulos, lecciones, evaluaciones, logros, certificaciones"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true")

    def handle(self, *args, **opts):
        random.seed(SEED)
        t0 = time.time()
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== SEED CONTENT EXTENDIDO ===\n"))

        if opts["reset"]:
            self._reset()

        admins = list(User.objects.filter(username__startswith="admin"))
        if not admins:
            self.stdout.write(self.style.ERROR("[!] No hay admins. Corre primero seed_and_test"))
            return
        admin = admins[0]

        estudiantes = list(User.objects.filter(username__regex=r"^est\d+$"))
        if not estudiantes:
            self.stdout.write(self.style.ERROR("[!] No hay estudiantes. Corre primero seed_and_test"))
            return

        cursos = self._crear_cursos(admin)
        self._crear_logros()
        self._crear_certificaciones()
        self._inscribir_y_progresar(estudiantes, cursos)
        self._dar_logros(estudiantes)
        self._dar_certificados(estudiantes)
        self._crear_respuestas(estudiantes)

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("=== RESUMEN ==="))
        self.stdout.write(f"  Cursos:                {Curso.objects.count()}")
        self.stdout.write(f"  Módulos:               {Modulo.objects.count()}")
        self.stdout.write(f"  Lecciones:             {Leccion.objects.count()}")
        self.stdout.write(f"  Evaluaciones:          {EvaluacionCurso.objects.count()}")
        self.stdout.write(f"  Preguntas:             {PreguntaEvaluacion.objects.count()}")
        self.stdout.write(f"  Progresos:             {ProgresoUsuario.objects.count()}")
        self.stdout.write(f"  Logros:                {Logro.objects.count()}")
        self.stdout.write(f"  Logros obtenidos:      {LogroObtenido.objects.count()}")
        self.stdout.write(f"  Certificaciones:       {Certificacion.objects.count()}")
        self.stdout.write(f"  Certificados obtenidos:{CertificacionObtenida.objects.count()}")
        self.stdout.write(f"  Respuestas:            {Respuesta.objects.count()}")
        self.stdout.write(self.style.SUCCESS(f"\n[OK] FIN en {time.time()-t0:.2f}s\n"))

    # ------------------------------------------------
    def _reset(self):
        self.stdout.write(self.style.WARNING("[RESET] borrando datos de cursos..."))
        PreguntaEvaluacion.objects.all().delete()
        EvaluacionCurso.objects.all().delete()
        ProgresoUsuario.objects.all().delete()
        Leccion.objects.all().delete()
        Modulo.objects.all().delete()
        Curso.objects.all().delete()
        LogroObtenido.objects.all().delete()
        Logro.objects.all().delete()
        CertificacionObtenida.objects.all().delete()
        Certificacion.objects.all().delete()
        Respuesta.objects.all().delete()

    # ------------------------------------------------
    def _crear_cursos(self, admin):
        self.stdout.write(self.style.MIGRATE_HEADING("--- Cursos ---"))
        cursos = []
        for titulo, nivel, descripcion in CURSOS:
            slug = titulo.lower().replace(" ", "-").replace("ó","o").replace("í","i").replace("é","e").replace("á","a")
            curso, created = Curso.objects.get_or_create(
                slug=slug,
                defaults=dict(
                    titulo=titulo,
                    descripcion=descripcion,
                    objetivo=f"Dominar {titulo.lower()} con teoría y práctica.",
                    nivel=nivel,
                    estado="publicado",
                    duracion_estimada=180,
                    puntos_totales=500,
                    creado_por=admin,
                    publicado_en=timezone.now(),
                    estudiantes_inscritos=0,
                ),
            )
            cursos.append(curso)
            if not created:
                continue

            # 4 módulos
            for m_orden, (m_titulo, m_desc) in enumerate(MODULOS_POR_CURSO, start=1):
                modulo = Modulo.objects.create(
                    curso=curso, titulo=f"{m_titulo} de {titulo}",
                    descripcion=m_desc, orden=m_orden,
                )
                # 3 lecciones
                for l_orden, (l_titulo, l_tipo, l_dur, l_puntos) in enumerate(LECCIONES_POR_MODULO, start=1):
                    Leccion.objects.create(
                        modulo=modulo,
                        titulo=f"{l_titulo} - {modulo.titulo}",
                        contenido=f"<h2>{l_titulo}</h2><p>Contenido de {titulo}.</p>",
                        tipo=l_tipo, orden=l_orden,
                        duracion_estimada=l_dur, puntos=l_puntos,
                    )
                # 1 evaluación por módulo
                ev = EvaluacionCurso.objects.create(
                    curso=curso, modulo=modulo,
                    titulo=f"Evaluación: {modulo.titulo}",
                    descripcion=f"Prueba del módulo {m_titulo}.",
                    tipo="modulo",
                    preguntas_por_evaluacion=5,
                    tiempo_limite=30,
                    puntaje_maximo=100,
                    intentos_permitidos=3,
                )
                # 5 preguntas
                for i in range(1, 6):
                    PreguntaEvaluacion.objects.create(
                        evaluacion=ev,
                        enunciado=f"Pregunta {i} del módulo {m_titulo} ({titulo})",
                        tipo="multiple_choice",
                        opciones=[
                            {"texto": "Opción A", "correcta": True},
                            {"texto": "Opción B", "correcta": False},
                            {"texto": "Opción C", "correcta": False},
                            {"texto": "Opción D", "correcta": False},
                        ],
                        respuesta_correcta="Opción A",
                        puntaje=20,
                        orden=i,
                    )
            self.stdout.write(f"  [OK] {titulo}")
        return cursos

    # ------------------------------------------------
    def _crear_logros(self):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Logros ---"))
        for (nombre, desc, tipo, icono, color, pts, nivel, cat, ej, tasa) in LOGROS:
            _, created = Logro.objects.get_or_create(
                nombre=nombre,
                defaults=dict(
                    descripcion=desc, tipo=tipo, icono=icono, color=color,
                    puntos_requeridos=pts, nivel_requerido=nivel,
                    categoria_requerida=cat,
                    ejercicios_completados_requeridos=ej,
                    tasa_aciertos_requerida=tasa,
                ),
            )
            if created:
                self.stdout.write(f"  [OK] {nombre}")

    # ------------------------------------------------
    def _crear_certificaciones(self):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Certificaciones ---"))
        for nombre, nivel, req in CERTIFICACIONES:
            _, created = Certificacion.objects.get_or_create(
                nombre=nombre,
                defaults=dict(
                    descripcion=f"Certificación {nivel}: {nombre}",
                    nivel=nivel, requisitos=req, activa=True,
                ),
            )
            if created:
                self.stdout.write(f"  [OK] {nombre}")

    # ------------------------------------------------
    def _inscribir_y_progresar(self, estudiantes, cursos):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Inscripciones + progreso ---"))
        total_lecciones = 0
        for est in estudiantes:
            # cada estudiante toma 3 cursos random
            mis_cursos = random.sample(cursos, 3)
            for curso in mis_cursos:
                curso.estudiantes_inscritos = (curso.estudiantes_inscritos or 0) + 1
                curso.save(update_fields=["estudiantes_inscritos"])

                lecciones = list(Leccion.objects.filter(modulo__curso=curso))
                if not lecciones:
                    continue
                # completar 0-100% de las lecciones
                n = random.randint(0, len(lecciones))
                for lec in random.sample(lecciones, n):
                    ProgresoUsuario.objects.get_or_create(
                        usuario=est, leccion=lec,
                        defaults=dict(
                            completado=True,
                            puntaje_obtenido=random.randint(50, 100),
                            intentos=random.randint(1, 3),
                            tiempo_dedicado=random.randint(5, 40),
                            completado_en=timezone.now() - timedelta(days=random.randint(1, 60)),
                        ),
                    )
                    total_lecciones += 1
        self.stdout.write(f"  [OK] Progresos creados: {total_lecciones}")

    # ------------------------------------------------
    def _dar_logros(self, estudiantes):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Otorgar logros ---"))
        logros = list(Logro.objects.all())
        n = 0
        for est in estudiantes:
            # 30% de estudiantes tiene logros
            if random.random() > 0.3:
                continue
            for logro in random.sample(logros, random.randint(1, 3)):
                _, created = LogroObtenido.objects.get_or_create(
                    user=est, logro=logro,
                    defaults=dict(fecha_obtenida=timezone.now() - timedelta(days=random.randint(1, 30))),
                )
                if created:
                    n += 1
        self.stdout.write(f"  [OK] {n} logros otorgados")

    # ------------------------------------------------
    def _dar_certificados(self, estudiantes):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Otorgar certificaciones ---"))
        certs = list(Certificacion.objects.all())
        n = 0
        for est in estudiantes:
            if random.random() > 0.1:
                continue
            cert = random.choice(certs)
            _, created = CertificacionObtenida.objects.get_or_create(
                user=est, certificacion=cert,
                defaults=dict(
                    codigo_verificacion=f"CERT-{est.id:04d}-{cert.id:02d}",
                    url_verificacion=f"https://rhetorica.com/verificar/CERT-{est.id:04d}-{cert.id:02d}",
                ),
            )
            if created:
                n += 1
        self.stdout.write(f"  [OK] {n} certificados otorgados")

    # ------------------------------------------------
    def _crear_respuestas(self, estudiantes):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Respuestas simuladas ---"))
        n = 0
        for est in estudiantes:
            if random.random() > 0.6:
                continue
            for _ in range(random.randint(5, 20)):
                Respuesta.objects.create(
                    user=est,
                    tipo_ejercicio=random.choice(["multiple_choice", "completar", "ordenar"]),
                    item_id=random.randint(1, 100),
                    respuesta_usuario="Opción A",
                    es_correcta=random.random() > 0.3,
                    puntuacion=random.randint(0, 20),
                    tiempo_segundos=random.randint(5, 60),
                    intento_numero=random.randint(1, 3),
                )
                n += 1
        self.stdout.write(f"  [OK] {n} respuestas creadas")
