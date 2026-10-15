"""Validador y esquema para micro-ejercicios adaptativos."""
import json
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "microejercicio.schema.json"
_SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8-sig"))


def validar_microejercicio(data: dict) -> list:
    """Valida un diccionario de micro-ejercicio contra reglas y esquema.

    Retorna una lista de cadenas con los errores encontrados (vacía si es
    válido).
    """
    errores = []

    if not isinstance(data, dict):
        return ["El micro-ejercicio debe ser un diccionario JSON."]

    # 1. Campos obligatorios
    campos_requeridos = [
        "tipo_adaptativo",
        "foco",
        "enunciado",
        "opciones",
        "respuesta_correcta",
        "retroalimentacion_adaptativa",
    ]
    for campo in campos_requeridos:
        if campo not in data:
            errores.append(f"Falta el campo obligatorio: '{campo}'.")

    if errores:
        return errores  # Si faltan campos base, detenemos validaciones avanzadas

    # 2. Validar tipo_adaptativo
    if data["tipo_adaptativo"] != "micro_ejercicio":
        errores.append(
            "El campo 'tipo_adaptativo' debe ser exactamente 'micro_ejercicio'."
        )

    # 3. Validar enunciado
    enunciado = data["enunciado"]
    if not isinstance(enunciado, str) or len(enunciado.strip()) < 10:
        errores.append(
            "El campo 'enunciado' debe ser una cadena de al menos 10 caracteres."
        )

    # 4. Validar opciones
    opciones = data["opciones"]
    if not isinstance(opciones, list) or len(opciones) < 2:
        errores.append(
            "El campo 'opciones' debe ser una lista con al menos 2 elementos."
        )
    else:
        if len(opciones) != len(set(opciones)):
            errores.append(
                "Las opciones del micro-ejercicio no deben contener valores duplicados."
            )

    # 5. Validar respuesta correcta
    respuesta = data["respuesta_correcta"]
    if isinstance(opciones, list) and respuesta not in opciones:
        errores.append(
            "La 'respuesta_correcta' debe coincidir con una de las opciones disponibles."
        )

    # 6. Validar retroalimentación
    retro = data["retroalimentacion_adaptativa"]
    if not isinstance(retro, str) or len(retro.strip()) < 10:
        errores.append(
            "El campo 'retroalimentacion_adaptativa' debe tener al menos 10 caracteres."
        )

    return errores


def es_valido(data: dict) -> bool:
    """Retorna True si el micro-ejercicio pasa todas las validaciones."""
    return len(validar_microejercicio(data)) == 0