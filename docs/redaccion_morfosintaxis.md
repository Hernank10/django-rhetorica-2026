# Modulo 4 — Taller de Redaccion Morfosintactica

Evaluacion deterministica de produccion libre: tipos de oracion compuesta,
tipos de subordinada, conectores y tipos de parrafo. Sin LLM, sin NLP pesado.

## Objetivo

El estudiante escribe una oracion o parrafo libre. El sistema evalua:
tipo de oracion, tipo de subordinada, conectores, tipo de parrafo.
Devuelve feedback accionable y registra errores en HistorialErrorSintactico.

## Contrato

### analizar_oracion(texto) -> dict

    {
      "tipo": "compuesta_coordinada",
      "n_oraciones": 2,
      "n_verbos": 2,
      "conectores": [{"texto": "pero", "tipo": "adversativa"}],
      "subordinadas": [],
      "longitud_palabras": 8
    }

### analizar_parrafo(texto) -> dict

    {
      "tipo_dominante": "argumentativo",
      "n_oraciones": 5,
      "marcadores_por_tipo": {"argumentativos": 3}
    }

### evaluar_ejercicio(texto, tipo_esperado) -> dict

    {
      "aprobado": false,
      "tipo_detectado": "simple",
      "feedback": "Pedimos oracion compuesta. Detectamos simple."
    }

### clasificar_error(texto, tipo_esperado) -> dict | None

Devuelve dict compatible con HistorialErrorSintactico si falla.

## Tipos de oracion (4)

- simple: 1 verbo, sin nexos
- compuesta_coordinada: 2+ verbos + 1+ coordinante (y, pero, o)
- compuesta_subordinada: 2+ verbos + 1+ subordinante (que, porque, cuando)
- yuxtapuesta: 2+ oraciones sin nexos

## Tipos de subordinada (3)

- sustantiva: que, si (tras verbo de pensamiento)
- adjetiva: que, quien, cual, cuyo (tras sustantivo)
- adverbial: cuando, donde, como, porque, si, aunque, para que

## Tipos de parrafo (4)

- narrativo: primero, luego, despues, entonces
- descriptivo: es, esta, tiene, parece
- argumentativo: porque, por lo tanto, sin embargo, en consecuencia
- expositivo: consiste en, por ejemplo, es decir

## Fuera de alcance (Fase 4B)

- Concordancia sujeto-verbo precisa (spaCy)
- Funcion sintactica por palabra (parser)
- Latin (CLTK)