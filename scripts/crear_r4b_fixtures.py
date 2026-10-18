"""Genera core/fixtures/redaccion_100_tecnicas.json desde el JSON fuente.

Corrige:
  - swap de ejemplo_es <-> ejemplo_en del JSON original
  - mapeo tipo -> tipo_redaccion esperado por core.services.redaccion
  - slug estable para `tecnica`
  - plantilla de `ejercicio` (el JSON no trae uno)
"""
import json
import re
import unicodedata
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
SRC = BASE / "ejercicios_completos-lengua-castellana" / "JSON completo - 100 técnicas de redacción en inglés.json"
OUT = BASE / "core" / "fixtures" / "redaccion_100_tecnicas.json"

# Mapeo tipo del JSON -> tipo_redaccion del servicio
TIPO_MAP = {
    "narrativo": "parrafo_narrativo",
    "descriptivo": "parrafo_descriptivo",
    "expositivo": "parrafo_expositivo",
    "argumentativo": "parrafo_argumentativo",
}

# Detector de ingles (muy simple, suficiente para el swap)
EN_STOPWORDS = {"the", "and", "i", "you", "is", "was", "of", "to", "in", "that", "with"}
ES_STOPWORDS = {"el", "la", "los", "las", "y", "es", "era", "de", "con", "que", "para", "en"}


def _score_en(texto):
    tokens = re.findall(r"\b[a-záéíóúñ]+\b", texto.lower())
    return sum(1 for t in tokens if t in EN_STOPWORDS)


def _score_es(texto):
    tokens = re.findall(r"\b[a-záéíóúñ]+\b", texto.lower())
    return sum(1 for t in tokens if t in ES_STOPWORDS)


def _es_texto_ingles(texto):
    """True si el texto parece estar en ingles."""
    return _score_en(texto) > _score_es(texto)


def _slug(texto):
    """'Tecnica 1: Estructura narrativa basica' -> 'estructura_narrativa_basica'."""
    # Quitar prefijo 'Tecnica N:'
    texto = re.sub(r"^T[eé]cnica\s+\d+\s*:\s*", "", texto, flags=re.IGNORECASE)
    # Quitar acentos
    nfkd = unicodedata.normalize("NFKD", texto)
    sin_acentos = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Solo alfanumerico y _
    s = re.sub(r"[^a-zA-Z0-9]+", "_", sin_acentos).strip("_").lower()
    return s[:80] or "tecnica"


def _limpiar_titulo(titulo):
    return re.sub(r"^T[eé]cnica\s+\d+\s*:\s*", "", titulo, flags=re.IGNORECASE).strip()


def main():
    data = json.loads(SRC.read_text(encoding="utf-8", errors="replace"))
    tecnicas = data["tecnicas"]
    print(f"[INPUT] {len(tecnicas)} tecnicas")

    fixtures = []
    swap_count = 0

    for idx, t in enumerate(tecnicas, start=1):
        pk = 30000 + idx
        tipo_json = t.get("tipo", "").strip().lower()
        tipo_redaccion = TIPO_MAP.get(tipo_json)
        if not tipo_redaccion:
            print(f"[SKIP] id={t.get('id')} tipo='{tipo_json}' sin mapeo")
            continue

        # Corregir swap de ejemplo
        ejemplo_es = (t.get("ejemplo_es") or "").strip()
        ejemplo_en = (t.get("ejemplo_en") or "").strip()
        if _es_texto_ingles(ejemplo_es) and not _es_texto_ingles(ejemplo_en):
            ejemplo_es, ejemplo_en = ejemplo_en, ejemplo_es
            swap_count += 1

        teoria = (t.get("explicacion_es") or "").strip()
        titulo = _limpiar_titulo(t.get("titulo_es") or f"Tecnica {idx}")
        keywords = (t.get("ejercicio_correcto") or "").strip()

        tecnica_slug = f"t{idx:03d}_{_slug(t.get('titulo_es') or '')}"

        # Plantilla de ejercicio (el JSON no trae uno)
        enunciado = (
            f"Escribe un parrafo {tipo_json} aplicando la tecnica: {titulo}. "
            f"Guia: {teoria} "
            f"Modelo: {ejemplo_es[:200]}... "
            f"Palabras clave esperadas: {keywords}."
        )

        contenido = {
            "tipo_redaccion": tipo_redaccion,
            "tipo_original": tipo_json,
            "teoria": teoria,
            "ejemplo": ejemplo_es,
            "enunciado": enunciado,
            "respuesta_esperada": keywords,
            "idioma": "ES",
        }

        fixtures.append({
            "model": "core.ejerciciolinguistico",
            "pk": pk,
            "fields": {
                "titulo": f"T{idx:03d} - {titulo}",
                "contenido": contenido,
                "categoria": "redaccion",
                "tipo": "produccion_libre",
                "nivel": 3,
                "puntos": 10,
                "es_redaccion": True,
                "tipo_redaccion": tipo_redaccion,
                "tecnica": tecnica_slug,
                "idioma": "ES",
                "creado_en": "2026-10-18T00:00:00Z",
            },
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(fixtures, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OUT] {OUT} ({OUT.stat().st_size} bytes, {len(fixtures)} fixtures)")
    print(f"[FIX] ejemplos corregidos (swap ES/EN): {swap_count}")

    # Distribucion final
    from collections import Counter
    dist = Counter(f["fields"]["tipo_redaccion"] for f in fixtures)
    print(f"[DIST] {dict(dist)}")


if __name__ == "__main__":
    main()