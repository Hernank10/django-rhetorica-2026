"""Genera modelos + fixtures de Redaccion (R2)."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")

# ============================================================
# 1) core/models_redaccion.py
# ============================================================
MODELS_REDACCION = """\"\"\"Modelos para el taller de redaccion morfosintactica.\"\"\"

from django.conf import settings
from django.db import models


class EvaluacionRedaccion(models.Model):
    \"\"\"Registro de una entrega de redaccion evaluada.\"\"\"
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evaluaciones_redaccion",
    )
    ejercicio = models.ForeignKey(
        "core.EjercicioLinguistico",
        on_delete=models.CASCADE,
        related_name="evaluaciones_redaccion",
    )
    texto_estudiante = models.TextField()
    analisis_json = models.JSONField(default=dict, blank=True)
    aprobado = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Evaluacion de redaccion"
        verbose_name_plural = "Evaluaciones de redaccion"
        indexes = [
            models.Index(fields=["estudiante", "-fecha"]),
        ]

    def __str__(self):
        return f"{self.estudiante.username} - ej {self.ejercicio_id}"
"""

# ============================================================
# 2) core/fixtures/redaccion_ejercicios.json
# ============================================================
FIXTURES = [
    # ORACIONES
    {"pk": 20001, "titulo": "Oracion simple: sujeto + verbo + objeto",
     "tipo": "oracion_simple", "enunciado": "Escribe una oracion simple con sujeto, verbo y objeto directo. Ej: 'Juan lee un libro.'"},
    {"pk": 20002, "titulo": "Oracion simple: atributiva",
     "tipo": "oracion_simple", "enunciado": "Escribe una oracion simple con verbo copulativo y atributo. Ej: 'Maria es inteligente.'"},
    {"pk": 20003, "titulo": "Coordinada copulativa",
     "tipo": "oracion_coordinada", "enunciado": "Une dos ideas con un coordinante copulativo (y, e, ni). Ej: 'Juan corre y Maria nada.'"},
    {"pk": 20004, "titulo": "Coordinada adversativa",
     "tipo": "oracion_coordinada", "enunciado": "Une dos ideas opuestas con 'pero', 'sino' o 'sin embargo'."},
    {"pk": 20005, "titulo": "Coordinada disyuntiva",
     "tipo": "oracion_coordinada", "enunciado": "Presenta dos alternativas con 'o' o 'u'."},
    {"pk": 20006, "titulo": "Subordinada causal",
     "tipo": "oracion_subordinada", "enunciado": "Explica una causa con 'porque', 'ya que' o 'puesto que'."},
    {"pk": 20007, "titulo": "Subordinada temporal",
     "tipo": "oracion_subordinada", "enunciado": "Indica tiempo con 'cuando', 'mientras' o 'antes que'."},
    {"pk": 20008, "titulo": "Subordinada condicional",
     "tipo": "oracion_subordinada", "enunciado": "Expresa una condicion con 'si', 'siempre que' o 'a menos que'."},
    {"pk": 20009, "titulo": "Subordinada concesiva",
     "tipo": "oracion_subordinada", "enunciado": "Expresa una objecion con 'aunque', 'a pesar de que' o 'por mas que'."},
    {"pk": 20010, "titulo": "Subordinada final",
     "tipo": "oracion_subordinada", "enunciado": "Expresa proposito con 'para que' o 'a fin de que'."},
    {"pk": 20011, "titulo": "Yuxtapuesta con punto y coma",
     "tipo": "oracion_yuxtapuesta", "enunciado": "Une tres acciones con punto y coma, sin conectores."},
    {"pk": 20012, "titulo": "Yuxtapuesta con comas",
     "tipo": "oracion_yuxtapuesta", "enunciado": "Enlaza varias acciones con comas sin usar conjunciones."},
    # PARRAFOS
    {"pk": 20101, "titulo": "Parrafo narrativo breve",
     "tipo": "parrafo_narrativo", "enunciado": "Narra en 3-4 oraciones algo que ocurrio ayer. Usa 'primero', 'luego', 'despues'."},
    {"pk": 20102, "titulo": "Parrafo narrativo con punto de giro",
     "tipo": "parrafo_narrativo", "enunciado": "Narra un suceso con un giro inesperado ('de repente')."},
    {"pk": 20103, "titulo": "Parrafo descriptivo de un lugar",
     "tipo": "parrafo_descriptivo", "enunciado": "Describe un lugar fisico con 3-4 oraciones usando 'es', 'esta', 'tiene', 'hay'."},
    {"pk": 20104, "titulo": "Parrafo descriptivo de una persona",
     "tipo": "parrafo_descriptivo", "enunciado": "Describe el aspecto fisico y caracter de una persona."},
    {"pk": 20105, "titulo": "Parrafo argumentativo con tesis",
     "tipo": "parrafo_argumentativo", "enunciado": "Defiende una opinion en 4 oraciones usando 'porque', 'por lo tanto', 'en consecuencia'."},
    {"pk": 20106, "titulo": "Parrafo argumentativo con objecion",
     "tipo": "parrafo_argumentativo", "enunciado": "Defiende una tesis y refuta una objecion con 'sin embargo' o 'no obstante'."},
    {"pk": 20107, "titulo": "Parrafo expositivo con definicion",
     "tipo": "parrafo_expositivo", "enunciado": "Explica un concepto con 'consiste en', 'se define como' y un 'por ejemplo'."},
    {"pk": 20108, "titulo": "Parrafo expositivo de proceso",
     "tipo": "parrafo_expositivo", "enunciado": "Explica como ocurre un proceso natural usando 'es decir', 'esto significa'."},
]

# Construye JSON
import json
fixture_json = []
for f in FIXTURES:
    tipo_esperado = f["tipo"]
    fixture_json.append({
        "model": "core.ejerciciolinguistico",
        "pk": f["pk"],
        "fields": {
            "titulo": f["titulo"],
            "contenido": {
                "tipo_redaccion": tipo_esperado,
                "enunciado": f["enunciado"],
            },
            "categoria": "redaccion",
            "tipo": "produccion_libre",
            "nivel": 2,
            "puntos": 10,
            "es_redaccion": True,
            "tipo_redaccion": tipo_esperado,
            "tecnica": tipo_esperado,
            "idioma": "ES",
            "creado_en": "2026-10-17T00:00:00Z",
        },
    })

FIXTURES_JSON = json.dumps(fixture_json, ensure_ascii=False, indent=2)

# ============================================================
# 3) Escritura de archivos
# ============================================================
p1 = BASE / "core" / "models_redaccion.py"
p1.write_text(MODELS_REDACCION, encoding="utf-8")
print(f"[OK] {p1.relative_to(BASE)} ({len(MODELS_REDACCION)} bytes)")

FIXTURES_DIR = BASE / "core" / "fixtures"
FIXTURES_DIR.mkdir(exist_ok=True)
p2 = FIXTURES_DIR / "redaccion_ejercicios.json"
p2.write_text(FIXTURES_JSON, encoding="utf-8")
print(f"[OK] {p2.relative_to(BASE)} ({len(FIXTURES_JSON)} bytes, {len(fixture_json)} ejercicios)")

# ============================================================
# 4) Extender core/models.py con 3 campos + import
# ============================================================
p3 = BASE / "core" / "models.py"
content = p3.read_text(encoding="utf-8")

CAMPO_VIEJO = """    es_adaptativo = models.BooleanField(default=False, db_index=True)"""
CAMPO_NUEVO = """    es_adaptativo = models.BooleanField(default=False, db_index=True)
    es_redaccion = models.BooleanField(default=False, db_index=True)
    tipo_redaccion = models.CharField(max_length=30, blank=True, default="")
    tecnica = models.CharField(max_length=100, blank=True, default="")"""

if "es_redaccion" in content:
    print("[SKIP] core/models.py ya tiene los campos de redaccion")
elif CAMPO_VIEJO in content:
    content = content.replace(CAMPO_VIEJO, CAMPO_NUEVO, 1)
    print("[OK] core/models.py: 3 campos agregados a EjercicioLinguistico")
else:
    print("[!] No se encontro el patron es_adaptativo en models.py")

# Agregar import
IMPORT_VIEJO = "from . import models_adaptativos  # noqa: F401,E402"
IMPORT_NUEVO = """from . import models_adaptativos  # noqa: F401,E402
from . import models_redaccion  # noqa: F401,E402"""

if "models_redaccion" in content:
    print("[SKIP] core/models.py ya importa models_redaccion")
elif IMPORT_VIEJO in content:
    content = content.replace(IMPORT_VIEJO, IMPORT_NUEVO, 1)
    print("[OK] core/models.py: import models_redaccion agregado")
else:
    # Fallback: agregar al final
    content = content.rstrip() + "\nfrom . import models_redaccion  # noqa: F401,E402\n"
    print("[OK] core/models.py: import models_redaccion agregado al final")

p3.write_text(content, encoding="utf-8")
print(f"[OK] {p3.relative_to(BASE)} actualizado ({len(content)} bytes)")