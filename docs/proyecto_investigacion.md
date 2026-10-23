# Proyecto de Investigación

## Diseño, desarrollo y validación de un LMS para la enseñanza de lingüística computacional del español con soporte NLP determinista

---

## 1. Título del proyecto

**"Sistema de gestión de aprendizaje para la enseñanza de morfosintaxis y retórica del castellano basado en procesamiento de lenguaje natural determinista: diseño, implementación y validación de contenidos pedagógicos digitales"**

**Acrónimo:** Rhetorica+

**Línea de investigación:** Tecnologías educativas + Lingüística computacional + Ingeniería de software

---

## 2. Planteamiento del problema

### 2.1 Contexto

La enseñanza de la morfosintaxis y la retórica del castellano en entornos digitales enfrenta tres limitaciones estructurales:

1. **Plataformas LMS genéricas** (Moodle, Canvas, Blackboard) están optimizadas para gestionar contenido estático (PDFs, videos, quizzes de opción múltiple) pero **no pueden procesar la estructura lingüística** de los textos. Un ejercicio de sintaxis en Moodle es una pregunta sobre sintaxis, no un análisis sintáctico real.

2. **Soluciones basadas en LLM** (ChatGPT, Claude, Gemini) ofrecen flexibilidad pedagógica pero introducen tres problemas: (a) **no determinismo** — la misma entrada puede producir verificaciones distintas, lo que rompe la auditabilidad pedagógica; (b) **dependencia de API externa** — costo por uso y latencia variable; (c) **opacidad** — el estudiante no puede saber *por qué* su paráfrasis fue aceptada o rechazada.

3. **Herramientas de NLP aisladas** (spaCy, Stanford CoreNLP, FreeLing) permiten análisis lingüístico real pero **no ofrecen la capa pedagógica** de un LMS: progreso, evaluaciones, certificaciones, notificaciones.

### 2.2 Vacío identificado

No existe —hasta donde revisamos— un LMS orientado específicamente a la enseñanza del español que **integre procesamiento de lenguaje natural determinista** como parte del flujo pedagógico, con las siguientes características:

- Análisis morfosintáctico en tiempo real como input de ejercicios
- Verificación automática de transformaciones sintácticas (paráfrasis activa↔pasiva)
- Retroalimentación explicable (*por qué* se acepta/rechaza una respuesta)
- Repetición espaciada (SM-2) con contenido generado desde corpus lingüístico
- Contenido pedagógico derivado de fuentes primarias (1.628 ejercicios reales)

### 2.3 Pregunta problematizadora

¿Es factible diseñar un LMS que, apoyándose en NLP determinista y corpus pedagógicos reales, permita la enseñanza y evaluación de morfosintaxis del castellano con retroalimentación explicable, manteniendo estándares de calidad de software (cobertura > 97%, tests automatizados, reproducibilidad) y siendo desplegable en infraestructura estándar?

---

## 3. Preguntas de investigación

### 3.1 Pregunta general

¿Qué decisiones arquitectónicas, pedagógicas y de ingeniería se requieren para construir un LMS de lingüística del castellano con soporte NLP determinista que satisfaga estándares de calidad reproducibles y auditables?

### 3.2 Preguntas específicas

| # | Pregunta |
|---|---|
| PE1 | ¿Cómo modelar el dominio lingüístico (morfosintaxis, paráfrasis, registro) para que los servicios de análisis sean testeables de forma aislada sin requerir el modelo completo de spaCy? |
| PE2 | ¿Qué estrategias permiten extraer contenido pedagógico verificable desde corpus heterogéneos (16 JSONs, 505 HTMLs) y garantizar su integridad en base de datos? |
| PE3 | ¿Cómo verificar paráfrasis sintácticas de forma determinista y explicable, sin recurrir a LLMs? |
| PE4 | ¿Qué nivel de cobertura de tests es compatible con un desarrollo iterativo sostenible bajo restricciones de tiempo acotado? |
| PE5 | ¿Qué limitaciones emergen al integrar Playwright (E2E) con el stack Django + spaCy en un entorno Windows, y cómo mitigarlas? |
| PE6 | ¿Qué tan cerca del "production-ready" puede llegar un proyecto individual sin infraestructura dedicada (Postgres, Gunicorn, Nginx, S3)? |

---

## 4. Objetivos

### 4.1 Objetivo general

Diseñar, implementar y validar un LMS para la enseñanza de morfosintaxis y retórica del castellano que integre NLP determinista (spaCy + reglas custom), corpus pedagógicos reales y buenas prácticas de ingeniería de software, alcanzando cobertura de tests superior al 97% y estado "production-ready para demo interna".

### 4.2 Objetivos específicos

| # | Objetivo | Estado |
|---|---|---|
| OE1 | Modelar 9 módulos funcionales: POS, filología, lectura asistida, redacción, SRS, corpus, paráfrasis sintáctica, LMS administrativo, notificaciones | ✅ |
| OE2 | Construir un corpus pedagógico de al menos 1.500 ejercicios reales a partir de 16 fuentes JSON y 505 HTMLs | ✅ (1.628) |
| OE3 | Implementar un motor de paráfrasis 100% determinista (activa↔pasiva, reordenamiento, registro) verificable por tests | ✅ |
| OE4 | Alcanzar cobertura de tests automatizados ≥ 97% con suite < 60s | ✅ (97.04%, ~40s) |
| OE5 | Integrar tests E2E (Playwright) que detecten bugs de frontend (CSRF, debounce, fetch) no cubiertos por tests Django | ✅ (8 E2E) |
| OE6 | Documentar 8 módulos con al menos 100 secciones técnicas reutilizables | ✅ (105+) |
| OE7 | Publicar versiones semánticas (v1.0.0, v1.0.1) con tags anotados y releases GitHub | ✅ |
| OE8 | Desplegar en infraestructura de producción (Postgres + Gunicorn + Nginx + S3) | ⏳ pendiente |

**Cumplimiento:** 7/8 objetivos específicos alcanzados (87.5%). El OE8 queda como trabajo futuro.

---

## 5. Justificación

### 5.1 Justificación pedagógica

Los currículos de lengua castellana (Colombia: Estándares Básicos de Competencias del MEN; España: LOMLOE) requieren que el estudiante produzca textos cohesionados y analice estructuras sintácticas. Sin embargo, la evaluación formativa de morfosintaxis es difícil de escalar: requiere un docente por estudiante.

Un LMS con NLP determinista puede ofrecer retroalimentación inmediata y explicable sobre paráfrasis, concordancia y registro, liberando al docente para tareas de mayor valor.

### 5.2 Justificación técnica

El determinismo es una ventaja competitiva frente a LLMs en contextos educativos donde la auditabilidad importa: reproducibilidad, explicabilidad (cada decisión tiene un `razon` trazable), costo cero, offline.

### 5.3 Justificación de ingeniería

El proyecto aplica buenas prácticas demostrables en un contexto de recursos limitados: cobertura de tests > 97% sostenida, idempotencia en todos los seeds, DRY_RUN con previews, versionado semántico, documentación como artefacto de primer orden.

---

## 6. Marco teórico

### 6.1 Paradigma: Design Science Research (DSR)

El proyecto se enmarca en DSR (Hevner et al., 2004; Peffers et al., 2007), cuyo objetivo es diseñar artefactos que resuelvan problemas del mundo real, y evaluar su efectividad.

Ciclo aplicado: Problema → Diseño → Desarrollo → Demostración → Evaluación → Comunicación.

### 6.2 Marco pedagógico: TPACK + SAMR

TPACK (Mishra & Koehler, 2006): integra Technological Knowledge (Django, spaCy), Pedagogical Knowledge (SRS, gamificación, feedback formativo) y Content Knowledge (morfosintaxis, retórica).

SAMR (Puentedura, 2010): el proyecto se ubica en Modificación (M) y Redefinición (R).

### 6.3 Marco lingüístico: gramática estructural + dependencias

Morfosintaxis: categorías gramaticales (POS), lemas, funciones sintácticas según Universal Dependencies (Nivre et al., 2020). Particularidad hispánica: es_core_news_md no sigue UD para voz pasiva (documentado en modulo7_sintaxis_completo.md §9.1).

### 6.4 Marco de ingeniería: TDD + CI/CD + Versionado semántico

TDD (Beck, 2002): tests antes de implementación. SemVer (Preston-Werner, 2013): v1.0.0 estable, v1.0.1 hot-fix. Reproducibilidad: seeds idempotentes, DRY_RUN, backups JSON.

---

## 7. Metodología

### 7.1 Diseño

Tipo de estudio: Investigación aplicada, diseño y desarrollo (I+D) con paradigma DSR. Enfoque mixto con dominancia técnica. La componente cuantitativa se expresa en métricas de calidad (cobertura, tests passing, líneas de código, número de ejercicios). La cualitativa en documentación técnica (105+ secciones).

### 7.2 Fases metodológicas

Fase 1 — Revisión de literatura y estado del arte ✅
Fase 2 — Diseño arquitectónico ✅
Fase 3 — Desarrollo iterativo ✅
Fase 4 — Población de datos pedagógicos ✅
Fase 5 — Validación E2E ✅
Fase 6 — Versionado y release ✅
Fase 7 — Despliegue a producción ⏳

### 7.3 Técnicas e instrumentos

Análisis de código (pytest --co, pytest --cov), análisis de corpus (diag_sources.py), validación E2E (Playwright + Chromium), documentación (Markdown por módulo), versionado (git tag -a, GitHub Releases), idempotencia (get_or_create).

### 7.4 Consideraciones éticas

No se usan datos personales reales; los 108 usuarios son ficticios generados por seed. Los 1.628 ejercicios provienen de corpus públicos. Código open source. Sin recolección de datos de usuarios reales en esta fase.

---

## 8. Contribuciones esperadas

### 8.1 Contribuciones teóricas

1. Caracterización del dominio lingüístico-pedagógico del español.
2. Justificación empírica del determinismo como ventaja competitiva.
3. Documentación de la divergencia UD vs es_core_news_md.

### 8.2 Contribuciones técnicas

1. Artefacto software: 9 módulos, ~975 tests, 97.04% cobertura.
2. Corpus pedagógico: 1.628 ejercicios, 324 lecciones, 285 preguntas.
3. Patrón arquitectónico: servicios ricos + vistas delgadas.
4. Estrategia de cobertura sostenible: DRY_RUN + seeds idempotentes + backups.

### 8.3 Contribuciones metodológicas

1. Ciclo DSR aplicado a proyecto individual.
2. E2E sobre Django + spaCy en Windows: mitigaciones documentadas.
3. Deuda técnica explícita como práctica.

---

## 9. Limitaciones y delimitaciones

### 9.1 Limitaciones

| Limitación | Impacto | Mitigación |
|---|---|---|
| Sin deploy a producción | No usable por usuarios reales aún | Documentar gap; fase 7 pendiente |
| Storage local | No escala más allá de demo | Migración a Postgres + S3 planificada |
| Sin validación con usuarios reales | Sin métricas de aprendizaje | Próxima fase: estudio con 20-30 estudiantes |
| Paráfrasis acotada a 3 tipos | Cobertura lingüística limitada | Roadmap: paráfrasis sintáctica real |
| Distractores por random.seed(42) | No siempre pedagógicamente plausibles | Mejora futura con similitud |
| Sin i18n completo (solo es-CO) | No usable en otros idiomas | Fuera del alcance actual |

### 9.2 Delimitaciones

Alcance: 9 módulos funcionales documentados; no incluye contenido audiovisual ni video.
Población de prueba: 108 usuarios ficticios.
Corpus: limitado a fuentes disponibles.
Idioma: español castellano.

---

## 10. Cronograma

### Fases completadas

| Fase | Duración | Estado |
|---|---|---|
| F1 — Revisión literatura | 1 sesión | ✅ |
| F2 — Diseño arquitectónico | 2 sesiones | ✅ |
| F3 — Desarrollo iterativo | 15+ sesiones | ✅ |
| F4 — Población datos | 3 sesiones | ✅ |
| F5 — Validación E2E | 2 sesiones | ✅ |
| F6 — Versionado/release | 1 sesión | ✅ |

**Total invertido:** ~24 sesiones equivalentes a ~30-40 horas efectivas.

### Fase pendiente

| Fase | Duración estimada |
|---|---|
| F7 — Deploy producción | 2-3 sesiones |
| F8 — Estudio con usuarios reales | 4-6 semanas post-deploy |

---

## 11. Resultados esperados

| Indicador | Meta | Real | Estado |
|---|---|---|---|
| Módulos funcionales | 8 | 9 | ✅ 112% |
| Tests automatizados | ≥ 500 | ~975 | ✅ 195% |
| Cobertura | ≥ 97% | 97.04% | ✅ |
| Ejercicios reales | ≥ 1.500 | 1.628 | ✅ 109% |
| Lecciones con contenido | ≥ 300 | 324 | ✅ |
| Documentación | ≥ 100 secciones | 105+ | ✅ |
| E2E tests | ≥ 5 | 8 | ✅ |
| Tags/releases | ≥ 1 | 3 | ✅ |
| Deploy producción | Sí | No | ⏳ |
| Estudio con usuarios | Sí | No | ⏳ |

**Cumplimiento global:** 8/10 indicadores (80%).

---

## 12. Productos de la investigación

### 12.1 Productos verificables

1. Software: github.com/Hernank10/django-rhetorica-2026
2. Releases: v1.0.0, v1.0.1, v1.1.0
3. Documentación: 10 archivos .md en docs/
4. Artículo de divulgación: articulo_django_rhetorica.md
5. Corpus pedagógico: 1.628 ejercicios

### 12.2 Productos esperados (fase 7+)

1. Artículo académico en revista indexada
2. Dataset público con licencia CC-BY-SA
3. Ponencia en congreso
4. Estudio empírico con estudiantes reales

---

## 13. Referencias

- Beck, K. (2002). Test-Driven Development: By Example. Addison-Wesley.
- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75-105.
- Honnibal, M., Montani, I., Van Landeghem, S., & Boyd, A. (2020). spaCy: Industrial-strength NLP in Python.
- Mishra, P., & Koehler, M. J. (2006). Technological pedagogical content knowledge. Teachers College Record, 108(6), 1017-1054.
- Nivre, J., et al. (2020). Universal Dependencies v2. LREC 2020.
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology. Journal of Management Information Systems, 24(3), 45-77.
- Preston-Werner, T. (2013). Semantic Versioning 2.0.0.
- Puentedura, R. R. (2010). SAMR and TPCK.
- Woźniak, P. A., & Gorzelanczyk, E. J. (1994). Optimization of repetition spacing. Acta Neurobiologiae Experimentalis, 54(1), 59-62.
- Ministerio de Educación Nacional de Colombia (2006). Estándares Básicos de Competencias en Lenguaje.

---

## 14. Reflexión final

Este proyecto demuestra que un desarrollador individual, sin equipo, sin infraestructura dedicada y con tiempo fragmentado entre sesiones cortas, puede llevar un proyecto software al estado "production-ready para demo interna" aplicando: disciplina de tests, determinismo como decisión arquitectónica, documentación explícita de deuda técnica, versionado semántico y corpus pedagógico verificable.

Lo que el proyecto no es: un producto comercial listo para escalar. Le faltan deploy, storage externo, y validación empírica con usuarios reales.

Lo que el proyecto sí es: un caso de estudio replicable de cómo aplicar DSR, TDD y buenas prácticas de ingeniería a un problema pedagógico concreto, con métricas auditables en cada fase.

El siguiente paso —deploy + estudio con estudiantes— requiere decisiones que ya no son técnicas sino institucionales: hosting, financiamiento, ética de investigación, diseño experimental con grupo control.

Ese es el límite honesto de este proyecto como proyecto de investigación individual.

---

*Documento guía del artículo "Django-Rhetorica: crónica de un LMS para lingüística computacional". Última actualización: 2026-10-23. Repositorio: github.com/Hernank10/django-rhetorica-2026.*