"""Diccionarios de conectores para el modulo de redaccion."""

COORDINANTES = {
    "y": "copulativa", "e": "copulativa", "ni": "copulativa",
    "o": "disyuntiva", "u": "disyuntiva",
    "pero": "adversativa", "sino": "adversativa", "mas": "adversativa",
    "sin embargo": "adversativa", "no obstante": "adversativa",
    "aunque": "adversativa",
    "o sea": "explicativa", "es decir": "explicativa", "esto es": "explicativa",
}

SUBORDINANTES = {
    "que": "sustantiva",
    "si": "sustantiva_condicional",
    "quien": "adjetiva", "quienes": "adjetiva",
    "cual": "adjetiva", "cuales": "adjetiva",
    "cuyo": "adjetiva", "cuya": "adjetiva",
    "cuando": "adverbial_tiempo", "mientras": "adverbial_tiempo",
    "antes que": "adverbial_tiempo", "despues que": "adverbial_tiempo",
    "donde": "adverbial_lugar",
    "como": "adverbial_modo", "segun": "adverbial_modo",
    "porque": "adverbial_causa", "pues": "adverbial_causa",
    "ya que": "adverbial_causa", "puesto que": "adverbial_causa",
    "siempre que": "adverbial_condicion", "a menos que": "adverbial_condicion",
    "a pesar de que": "adverbial_concesion", "por mas que": "adverbial_concesion",
    "para que": "adverbial_finalidad", "a fin de que": "adverbial_finalidad",
}

MARCADORES_PARRAFO = {
    "narrativos": [
        "primero", "luego", "despues", "entonces", "al final",
        "mientras", "de repente", "mas tarde", "finalmente",
    ],
    "argumentativos": [
        "porque", "por lo tanto", "por consiguiente", "en consecuencia",
        "sin embargo", "no obstante", "en primer lugar", "finalmente",
        "por un lado", "por otro lado", "en resumen", "en conclusion",
    ],
    "expositivos": [
        "consiste en", "se define como", "por ejemplo", "es decir",
        "esto significa", "en otras palabras",
    ],
    "descriptivos": [
        "es", "esta", "son", "estan", "tiene", "tienen",
        "hay", "se ve", "parece", "presenta",
    ],
}