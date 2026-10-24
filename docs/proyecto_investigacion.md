# Proyecto de Investigación

## Diseño, desarrollo y validación de un LMS para la enseñanza de lingüística computacional del español con soporte NLP determinista

---

## 1. Título del proyecto

**"Sistema de gestión de aprendizaje para la enseñanza de morfosintaxis y retórica del castellano basado en procesamiento de lenguaje natural determinista"**

**Acrónimo:** Rhetorica+

---

## 2. Planteamiento del problema

### 2.1 Contexto

Tres limitaciones estructurales en la enseñanza digital de morfosintaxis:

1. **LMS genéricos** (Moodle, Canvas) no procesan estructura lingüística.
2. **LLMs** (ChatGPT, Claude) son flexibles pero no deterministas, dependen de API externa y son opacos.
3. **NLP aislado** (spaCy, FreeLing) permite análisis real pero no ofrece capa pedagógica.

### 2.2 Vacío identificado

No existe un LMS del español que integre NLP determinista como parte del flujo pedagógico: análisis en tiempo real, verificación de transformaciones, retroalimentación explicable, SM-2 y corpus reales.

### 2.3 Pregunta problematizadora

¿Es factible un LMS con NLP determinista y corpus reales, con cobertura > 97%, tests automatizados y desplegable en infraestructura estándar?

---

## 3. Preguntas de investigación

| # | Pregunta |
|---|---|
| PE1 | ¿Cómo modelar el dominio lingüístico para que los servicios sean testeables sin spaCy? |
| PE2 | ¿Cómo extraer contenido pedagógico verificable desde corpus heterogéneos? |
| PE3 | ¿Cómo verificar paráfrasis sintácticas de forma determinista sin LLMs? |
| PE4 | ¿Qué cobertura de tests es sostenible bajo restricciones de tiempo? |
| PE5 | ¿Qué limitaciones emergen al integrar Playwright + Django + spaCy en Windows? |
| PE6 | ¿Qué tan cerca del "production-ready" puede llegar un proyecto individual? |

---

## 4. Objetivos

### 4.1 Objetivo general

Diseñar, implementar y validar un LMS para morfosintaxis y retórica del castellano con NLP determinista, corpus reales y buenas prácticas de ingeniería, con cobertura > 97% y estado "production-ready para demo interna".

### 4.2 Objetivos específicos

| # | Objetivo | Estado |
|---|---|---|
| OE1 | 9 módulos funcionales | ✅ |
| OE2 | Corpus ≥ 1.500 ejercicios | ✅ (1.628) |
| OE3 | Motor de paráfrasis determinista | ✅ |
| OE4 | Cobertura ≥ 97% con suite < 60s | ✅ (97.09%) |
| OE5 | E2E con Playwright | ✅ (8 E2E) |
| OE6 | Documentación ≥ 100 secciones | ✅ (105+) |
| OE7 | Releases semánticos | ✅ (v1.1.5) |
| OE8 | Deploy productivo | ⏳ pendiente |

**Cumplimiento:** 7/8 (87.5%).

---

## 5. Justificación

**Pedagógica:** currículos MEN Colombia y LOMLOE España requieren análisis sintáctico y producción textual. La evaluación formativa de morfosintaxis no escala sin NLP.

**Técnica:** el determinismo es ventaja competitiva auditable: reproducibilidad, explicabilidad, costo cero, offline.

**Ingeniería:** buenas prácticas con recursos limitados: cobertura > 97%, idempotencia, DRY_RUN, SemVer, doc como artefacto.

---

## 6. Marco teórico

**DSR (Design Science Research):** Hevner et al. (2004); Peffers et al. (2007). Ciclo: Problema → Diseño → Desarrollo → Demostración → Evaluación → Comunicación.

**TPACK + SAMR:** Mishra & Koehler (2006); Puentedura (2010). Modificación y Redefinición.

**Lingüística estructural:** Universal Dependencies (Nivre et al., 2020). Nota: es_core_news_md no sigue UD para voz pasiva (documentado en modulo7 §9.1).

**Ingeniería:** TDD (Beck, 2002), SemVer (Preston-Werner, 2013), reproducibilidad por seeds idempotentes.

---

## 7. Metodología

Investigación aplicada (I+D), paradigma DSR, enfoque mixto con dominancia técnica.

| Fase | Estado |
|---|---|
| F1 — Revisión literatura | ✅ |
| F2 — Diseño arquitectónico | ✅ |
| F3 — Desarrollo iterativo | ✅ |
| F4 — Población datos | ✅ |
| F5 — Validación E2E | ✅ |
| F6 — Versionado/release | ✅ |
| F7 — Deploy producción | ⏳ |

Técnicas: pytest --co, pytest --cov, Playwright + Chromium, Markdown por módulo, git tag -a, get_or_create.

Ética: 108 usuarios ficticios, corpus público, open source, sin recolección de datos reales.

---

## 8. Contribuciones

**Teóricas:** caracterización del dominio lingüístico-pedagógico español; justificación del determinismo; documentación de divergencia UD vs es_core_news_md.

**Técnicas:** artefacto software (9 módulos, ~975 tests, 97.09%); corpus (1.628 ejercicios, 324 lecciones, 285 preguntas); patrón servicios ricos + vistas delgadas; estrategia de cobertura sostenible.

**Metodológicas:** ciclo DSR individual; E2E Django + spaCy en Windows; deuda técnica explícita.

---

## 9. Limitaciones

| Limitación | Mitigación |
|---|---|
| Sin deploy productivo | Fase 7 pendiente |
| Storage local | Migración a S3 (v1.1.5 ya resuelto) |
| Sin usuarios reales | Próxima fase: 20-30 estudiantes |
| Paráfrasis acotada | Roadmap: paráfrasis completa |
| Distractores random.seed(42) | Mejora con similitud |
| Sin i18n completo | Fuera de alcance |

---

## 10. Cronograma

Completado: F1-F6 (~24 sesiones, ~35h). Pendiente: F7 deploy (2-3 sesiones), F8 estudio usuarios (4-6 semanas post-deploy).

---

## 11. Resultados esperados

| Indicador | Meta | Real | Estado |
|---|---|---|---|
| Módulos | 8 | 9 | ✅ |
| Tests | ≥ 500 | ~975 | ✅ |
| Cobertura | ≥ 97% | 97.09% | ✅ |
| Ejercicios | ≥ 1.500 | 1.628 | ✅ |
| Lecciones | ≥ 300 | 324 | ✅ |
| Docs | ≥ 100 sec | 105+ | ✅ |
| E2E | ≥ 5 | 8 | ✅ |
| Tags | ≥ 1 | 6 | ✅ |
| Deploy | Sí | No | ⏳ |
| Usuarios reales | Sí | No | ⏳ |

**Cumplimiento:** 8/10 (80%).

---

## 12. Productos

**Verificables:** software (GitHub), releases (v1.0.0, v1.0.1, v1.1.0-v1.1.5), docs (10 .md), artículo, corpus 1.628 ejercicios.

**Esperados:** artículo en revista indexada, dataset CC-BY-SA, ponencia, estudio empírico.

---

## 13. Referencias

- Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
- Hevner, A. R., et al. (2004). Design science in information systems research. *MIS Quarterly*, 28(1), 75-105.
- Honnibal, M., et al. (2020). spaCy: Industrial-strength NLP in Python.
- Mishra, P., & Koehler, M. J. (2006). TPACK. *Teachers College Record*, 108(6), 1017-1054.
- Nivre, J., et al. (2020). Universal Dependencies v2. LREC 2020.
- Peffers, K., et al. (2007). DSR methodology. *JMIS*, 24(3), 45-77.
- Preston-Werner, T. (2013). SemVer 2.0.0.
- Puentedura, R. R. (2010). SAMR and TPCK.
- Woźniak, P. A., & Gorzelanczyk, E. J. (1994). Optimization of repetition spacing. *Acta Neurobiologiae Experimentalis*, 54(1), 59-62.
- MEN Colombia (2006). Estándares Básicos de Competencias en Lenguaje.

---

## 14. Reflexión final

Este proyecto demuestra que un desarrollador individual, sin equipo ni infraestructura dedicada, puede llevar un proyecto al estado "production-ready para demo interna" aplicando: disciplina de tests, determinismo como decisión arquitectónica, deuda técnica explícita, SemVer y corpus pedagógico verificable.

Lo que no es: producto comercial escalable. Faltan deploy, storage externo (S3 resuelto en v1.1.5) y validación empírica.

Lo que sí es: caso de estudio replicable de DSR + TDD + buenas prácticas, con métricas auditables en cada fase.

El siguiente paso —deploy + estudio con estudiantes— requiere decisiones institucionales: hosting, financiamiento, ética, diseño experimental.

Ese es el límite honesto de este proyecto como investigación individual.

---

*Documento guía del artículo "Django-Rhetorica: crónica de un LMS para lingüística computacional". Última actualización: 2026-10-24. Repositorio: github.com/Hernank10/django-rhetorica-2026.*