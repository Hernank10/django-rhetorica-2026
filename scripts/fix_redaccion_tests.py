from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

SERVICIO = """\"\"\"Servicio de evaluacion morfosintactica. Funciones puras.\"\"\"

import re

from ._diccionarios_redaccion import COORDINANTES, MARCADORES_PARRAFO, SUBORDINANTES

MIN_PALABRAS = 3
MAX_PALABRAS = 500

# Lista blanca de verbos conjugados comunes (mas preciso que terminaciones)
VERBOS_LISTA_BLANCA = {
    "es", "son", "era", "eran", "fue", "fueron", "sera", "seran", "sido",
    "esta", "estan", "estaba", "estaban", "estuvo", "estuvieron",
    "tiene", "tienen", "tenia", "tenian", "tuvo", "tuvieron",
    "hay", "habia", "hubo",
    "hace", "hacen", "hacia", "hacian", "hizo", "hicieron",
    "puede", "pueden", "podia", "podian",
    "quiere", "quieren", "queria", "querian",
    "estudia", "estudian", "estudiaba", "estudiaban", "estudio", "estudie",
    "corre", "corren", "corria", "corrian", "corrio",
    "nada", "nadan", "nadaba", "nadaban", "nado",
    "juega", "juegan", "jugaba", "jugaban", "jugo",
    "vino", "vinieron", "viene", "vienen", "venia", "venian",
    "trabaja", "trabajan", "trabajaba", "trabajaban", "trabajo",
    "llega", "llegan", "llego", "llegaron", "llegaba",
    "debes", "debe", "deben", "debia",
    "fuimos", "vamos", "van", "iba", "iban",
    "cenamos", "ceno", "comio", "comemos",
    "dijo", "dijeron", "dice", "dicen",
    "cree", "creen", "creia",
    "pienso", "piensan", "penso", "pensaba",
    "opino", "opinan", "considero", "consideran",
    "sabe", "saben", "sabia", "sabemos",
    "afirmo", "afirman",
}

VERBOS_PENSAMIENTO = {
    "pienso", "pensaba", "penso", "creo", "creia", "cree",
    "digo", "dice", "dijo", "opino", "considero", "afirmo",
    "sabe", "sabemos", "sabia", "se",
}

PREPOSICIONES = {
    "a", "ante", "bajo", "con", "contra", "de", "desde",
    "en", "entre", "hacia", "hasta", "para", "por", "segun",
    "sin", "sobre", "tras", "el", "la", "los", "las", "un",
    "una", "unos", "unas", "mi", "tu", "su", "nuestro",
}


def _normalizar(texto):
    return " ".join(texto.lower().split()) if texto else ""


def _tokenizar_oraciones(texto):
    if not texto:
        return []
    return [s.strip() for s in re.split(r"[.!?]+", texto) if s.strip()]


def _contar_verbos(oracion):
    tokens = re.findall(r"\\b[a-záéíóúñ]+\\b", oracion.lower())
    verbos = 0
    for t in tokens:
        if t in VERBOS_LISTA_BLANCA:
            verbos += 1
            continue
        if len(t) < 3:
            continue
        if t.endswith(("ando", "iendo")):
            verbos += 1
        elif t.endswith(("amos", "aron", "ieron", "aba", "aban")):
            verbos += 1
        elif t.endswith(("aste", "iste")):
            verbos += 1
    return verbos


def _encontrar_conectores(texto):
    texto_lower = texto.lower()
    encontrados = []
    for nexo in sorted(COORDINANTES.keys(), key=len, reverse=True):
        patron = r"\\b" + re.escape(nexo) + r"\\b"
        for m in re.finditer(patron, texto_lower):
            encontrados.append({
                "texto": nexo, "tipo": COORDINANTES[nexo],
                "posicion": m.start(), "categoria": "coordinante",
            })
    for nexo in sorted(SUBORDINANTES.keys(), key=len, reverse=True):
        patron = r"\\b" + re.escape(nexo) + r"\\b"
        for m in re.finditer(patron, texto_lower):
            encontrados.append({
                "texto": nexo, "tipo": SUBORDINANTES[nexo],
                "posicion": m.start(), "categoria": "subordinante",
            })
    return encontrados


def _clasificar_subordinada_por_contexto(nexo, posicion, texto):
    \"\"\"Para 'que': sustantiva tras verbo de pensamiento, adjetiva tras sustantivo.\"\"\"
    tipo_default = SUBORDINANTES.get(nexo, "desconocida")

    if nexo != "que":
        if tipo_default.startswith("adjetiva"):
            return "adjetiva"
        if tipo_default.startswith("sustantiva"):
            return "sustantiva"
        if tipo_default.startswith("adverbial"):
            return "adverbial"
        return tipo_default

    antes = texto[:posicion].strip().split()
    if not antes:
        return "sustantiva"

    anterior = antes[-1].lower()
    if anterior in VERBOS_PENSAMIENTO:
        return "sustantiva"
    if anterior in VERBOS_LISTA_BLANCA:
        return "sustantiva"
    if anterior in PREPOSICIONES:
        return "sustantiva"

    # Si el anterior no es verbo ni preposicion → probablemente sustantivo → adjetiva
    return "adjetiva"


def analizar_oracion(texto):
    normalizado = _normalizar(texto)
    palabras = normalizado.split()
    if len(palabras) < MIN_PALABRAS:
        return {"tipo": "insuficiente", "n_oraciones": 0, "n_verbos": 0,
                "conectores": [], "subordinadas": [],
                "longitud_palabras": len(palabras),
                "error": "Texto demasiado corto"}
    if len(palabras) > MAX_PALABRAS:
        return {"tipo": "demasiado_largo", "n_oraciones": 0, "n_verbos": 0,
                "conectores": [], "subordinadas": [],
                "longitud_palabras": len(palabras),
                "error": "Maximo 500 palabras"}

    oraciones = _tokenizar_oraciones(normalizado)
    n_verbos = sum(_contar_verbos(o) for o in oraciones)
    conectores = _encontrar_conectores(normalizado)
    coordinantes = [c for c in conectores if c["categoria"] == "coordinante"]
    subordinantes = [c for c in conectores if c["categoria"] == "subordinante"]

    subordinadas = []
    for c in subordinantes:
        tipo = _clasificar_subordinada_por_contexto(c["texto"], c["posicion"], normalizado)
        subordinadas.append({"tipo": tipo, "nexo": c["texto"]})

    if n_verbos <= 1 and not coordinantes and not subordinantes:
        tipo = "simple"
    elif subordinantes:
        tipo = "compuesta_subordinada"
    elif coordinantes:
        tipo = "compuesta_coordinada"
    elif len(oraciones) >= 2 or n_verbos >= 2:
        tipo = "yuxtapuesta"
    else:
        tipo = "simple"

    return {
        "tipo": tipo, "n_oraciones": len(oraciones), "n_verbos": n_verbos,
        "conectores": conectores, "subordinadas": subordinadas,
        "longitud_palabras": len(palabras),
    }


def analizar_parrafo(texto):
    normalizado = _normalizar(texto)
    if not normalizado:
        return {"tipo_dominante": "vacio", "n_oraciones": 0,
                "marcadores_por_tipo": {}}
    marcadores = {k: 0 for k in MARCADORES_PARRAFO}
    for categoria, lista in MARCADORES_PARRAFO.items():
        for m in lista:
            marcadores[categoria] += len(
                re.findall(r"\\b" + re.escape(m) + r"\\b", normalizado)
            )
    maximo = max(marcadores.values())
    if maximo == 0:
        tipo = "neutro"
    else:
        tipo = next(k for k, v in marcadores.items() if v == maximo)
    return {
        "tipo_dominante": tipo,
        "n_oraciones": len(_tokenizar_oraciones(normalizado)),
        "marcadores_por_tipo": marcadores,
    }


_TIPO_MAP = {
    "oracion_simple": "simple",
    "oracion_coordinada": "compuesta_coordinada",
    "oracion_subordinada": "compuesta_subordinada",
    "oracion_yuxtapuesta": "yuxtapuesta",
    "parrafo_narrativo": "narrativos",
    "parrafo_descriptivo": "descriptivos",
    "parrafo_argumentativo": "argumentativos",
    "parrafo_expositivo": "expositivos",
}


def evaluar_ejercicio(texto, tipo_esperado):
    if tipo_esperado.startswith("parrafo_"):
        analisis = analizar_parrafo(texto)
        esperado = _TIPO_MAP.get(tipo_esperado, "")
        aprobado = analisis["tipo_dominante"] == esperado
        if aprobado:
            feedback = "Correcto. Parrafo " + analisis["tipo_dominante"] + "."
        else:
            feedback = "Pedimos parrafo " + esperado + ". Detectamos " + analisis["tipo_dominante"] + "."
    else:
        analisis = analizar_oracion(texto)
        esperado = _TIPO_MAP.get(tipo_esperado, "")
        aprobado = analisis["tipo"] == esperado
        if aprobado:
            feedback = "Correcto. Tipo detectado: " + analisis["tipo"] + "."
        else:
            feedback = "Pedimos " + esperado + ". Detectamos " + analisis["tipo"] + "."
    return {
        "aprobado": aprobado,
        "tipo_detectado": analisis.get("tipo") or analisis.get("tipo_dominante"),
        "analisis": analisis,
        "feedback": feedback,
    }


def clasificar_error(texto, tipo_esperado):
    r = evaluar_ejercicio(texto, tipo_esperado)
    if r["aprobado"]:
        return None
    return {
        "categoria_gramatical": tipo_esperado,
        "patron_error": r["tipo_detectado"] + "_en_lugar_de_" + tipo_esperado,
        "idioma": "ES",
    }
"""

TESTS = """\"\"\"Tests de core/services/redaccion.py (sin BD).\"\"\"

from core.services.redaccion import (
    analizar_oracion,
    analizar_parrafo,
    clasificar_error,
    evaluar_ejercicio,
)


class TestAnalizarOracion:
    def test_vacia(self):
        assert analizar_oracion("")["tipo"] == "insuficiente"

    def test_corta(self):
        assert analizar_oracion("hola que")["tipo"] == "insuficiente"

    def test_simple(self):
        r = analizar_oracion("Juan estudia matematicas en su casa")
        assert r["tipo"] == "simple"
        assert r["conectores"] == []

    def test_coordinada_pero(self):
        r = analizar_oracion("Juan estudia, pero su hermano juega")
        assert r["tipo"] == "compuesta_coordinada"
        assert any(c["texto"] == "pero" for c in r["conectores"])

    def test_coordinada_y(self):
        r = analizar_oracion("Juan corre y Maria nada todos los dias")
        assert r["tipo"] == "compuesta_coordinada"

    def test_subordinada_porque(self):
        r = analizar_oracion("Juan se fue porque estaba cansado")
        assert r["tipo"] == "compuesta_subordinada"

    def test_subordinada_adjetiva(self):
        r = analizar_oracion("El hombre que vino ayer era mi tio")
        assert r["tipo"] == "compuesta_subordinada"
        tipos = [s["tipo"] for s in r["subordinadas"]]
        assert "adjetiva" in tipos

    def test_subordinada_sustantiva(self):
        r = analizar_oracion("Pienso que debes estudiar mas")
        tipos = [s["tipo"] for s in r["subordinadas"]]
        assert "sustantiva" in tipos

    def test_muy_larga(self):
        r = analizar_oracion("palabra " * 600)
        assert r["tipo"] == "demasiado_largo"


class TestAnalizarParrafo:
    def test_vacio(self):
        assert analizar_parrafo("")["tipo_dominante"] == "vacio"

    def test_narrativo(self):
        r = analizar_parrafo(
            "Primero fuimos al parque. Luego regresamos. Despues cenamos."
        )
        assert r["tipo_dominante"] == "narrativos"

    def test_argumentativo(self):
        r = analizar_parrafo(
            "Es malo porque perjudica. Por lo tanto, debe revisarse. En consecuencia, la rechazo."
        )
        assert r["tipo_dominante"] == "argumentativos"

    def test_expositivo(self):
        r = analizar_parrafo(
            "La gravedad consiste en una fuerza. Por ejemplo atrae. Esto significa que la masa importa."
        )
        assert r["tipo_dominante"] == "expositivos"

    def test_neutro(self):
        r = analizar_parrafo("Un texto cualquiera sin marcadores claros")
        assert r["tipo_dominante"] == "neutro"


class TestEvaluarEjercicio:
    def test_aprobado_coordinada(self):
        r = evaluar_ejercicio(
            "Juan estudia, pero su hermano juega", "oracion_coordinada"
        )
        assert r["aprobado"] is True

    def test_no_aprobado_simple(self):
        r = evaluar_ejercicio("Juan estudia", "oracion_coordinada")
        assert r["aprobado"] is False

    def test_aprobado_subordinada(self):
        r = evaluar_ejercicio(
            "Juan se fue porque estaba cansado", "oracion_subordinada"
        )
        assert r["aprobado"] is True

    def test_aprobado_parrafo_argumentativo(self):
        r = evaluar_ejercicio(
            "Porque es importante, por lo tanto actuamos. Sin embargo, cuidado.",
            "parrafo_argumentativo",
        )
        assert r["aprobado"] is True

    def test_no_aprobado_parrafo(self):
        r = evaluar_ejercicio("Hola mundo cruel", "parrafo_argumentativo")
        assert r["aprobado"] is False


class TestClasificarError:
    def test_aprobado_none(self):
        r = clasificar_error(
            "Juan estudia, pero Maria trabaja", "oracion_coordinada"
        )
        assert r is None

    def test_fallido_dict(self):
        r = clasificar_error("Hola mundo cruel", "oracion_coordinada")
        assert r is not None
        assert r["categoria_gramatical"] == "oracion_coordinada"
        assert r["idioma"] == "ES"
        assert "en_lugar_de_oracion_coordinada" in r["patron_error"]
"""

p1 = BASE / "core" / "services" / "redaccion.py"
p1.write_text(SERVICIO, encoding="utf-8")
print(f"[OK] {p1.relative_to(BASE)} ({len(SERVICIO)} bytes)")

p2 = BASE / "core" / "tests" / "test_services_redaccion.py"
p2.write_text(TESTS, encoding="utf-8")
print(f"[OK] {p2.relative_to(BASE)} ({len(TESTS)} bytes)")