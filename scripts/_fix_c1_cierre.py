"""_fix_c1_cierre.py - Cierra C1: ajusta 5 textos al rango 450-700 palabras.

  id=3   436w -> 450w  (+14w)  añadir frase final
  id=8   447w -> 450w  (+3w)   2 micro-ajustes
  id=31  712w -> 700w  (-12w)  4 recortes quirúrgicos
  id=32  828w -> 700w  (-128w) eliminar puntos 13/15/17 + renumerar + trim
  id=63  404w -> 450w  (+46w)  3 intercambios extra en el diálogo

DRY-RUN por defecto. --apply para escribir.
"""
import os, sys, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_retorica.settings.dev")
import django; django.setup()
from django.apps import apps
from django.db import transaction

TX = apps.get_model("core", "Texto")
MIN_W, MAX_W = 450, 700

def wc(text):
    text = re.sub(r"<[^>]+>", " ", str(text or ""))
    return len(re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑü]+\b", text))

REPLACEMENTS = {
    3: {
        "label": "La promesa incumplida",
        "pairs": [
            (
                'El futuro, por ahora, no llega.',
                'El futuro, por ahora, no llega. Mientras tanto, los ciudadanos y las organizaciones ecologistas siguen esperando respuestas que nunca llegan.'
            ),
        ],
    },
    8: {
        "label": "El ruido de las redes",
        "pairs": [
            (
                'El cuarto problema es la erosión de la confianza.',
                'El cuarto problema es la lenta erosión de la confianza.'
            ),
            (
                'El resultado es una sociedad más polarizada',
                'El resultado es una sociedad cada vez más polarizada'
            ),
        ],
    },
    31: {
        "label": "El cuento que se escribía solo",
        "pairs": [
            (
                'Al día siguiente, Aurelio fue a ver a su amigo Bernardo, profesor de literatura.',
                'Al día siguiente, Aurelio fue a ver a su amigo Bernardo.'
            ),
            (
                'Y en él, Aurelio se veía a sí mismo escribiendo el cuento que estaba leyendo.',
                'Y en él, Aurelio se veía escribiendo el cuento que estaba leyendo.'
            ),
            (
                'Y luego, en algún otro lugar, alguien los retoma".',
                'Y luego alguien los retoma".'
            ),
            (
                'Aurelio sintió un vértigo. Miró sus manos. Miró la mesa. Miró a Bernardo. Todo parecía real.',
                'Aurelio sintió un vértigo. Miró sus manos, la mesa, a Bernardo. Todo parecía real.'
            ),
        ],
    },
    32: {
        "label": "Desinformación",
        "pairs": [
            (
                '13. Analogía compleja: diferencias relevantes\n\n"Como el cuerpo necesita ejercicio, la mente necesita estimulación" es una analogía relevante. "Como los barcos necesitan capitán, los países necesitan rey" tiene diferencias relevantes (un país no es un barco). Evaluar una analogía requiere identificar esas diferencias.\n\n',
                ''
            ),
            (
                '15. Calidad ética de un argumento\n\nUn argumento puede ser lógicamente válido pero éticamente rechazable. Defender la esclavitud con lógica es éticamente rechazable. La calidad ética depende del respeto a la dignidad, la justicia y las personas.\n\n',
                ''
            ),
            (
                '17. Coherencia entre medios, fines y valores\n\nUn argumento político es sólido si los medios propuestos son coherentes con los fines y con los valores declarados. Defender la libertad usando censura es incoherente. Evaluar esta coherencia permite analizar críticamente las propuestas políticas.\n\n',
                ''
            ),
            ('14. Falsa premisa', '13. Falsa premisa'),
            ('16. Falsa causa compleja: multicausalidad', '14. Falsa causa compleja: multicausalidad'),
            ('18. Manipulación emocional en publicidad', '15. Manipulación emocional en publicidad'),
            (
                'Las 18 herramientas de este texto son un kit básico para detectar la manipulación y evaluar críticamente la información. Aplicarlas no garantiza la verdad, pero al menos nos protege de la mentira.',
                'Las 15 herramientas de este texto son un kit básico para detectar la manipulación y evaluar críticamente la información.'
            ),
        ],
    },
    63: {
        "label": "La entrevista",
        "pairs": [
            (
                '—Mi capacidad de adaptación. He cambiado de sector, de ciudad, de equipo, y siempre he sabido encontrar mi lugar. Creo que eso es útil en una organización como esta, donde los proyectos cambian constantemente.\n\n—De acuerdo. ¿Tienes alguna pregunta para mí?',
                '—Mi capacidad de adaptación. He cambiado de sector, de ciudad, de equipo, y siempre he sabido encontrar mi lugar. Creo que eso es útil en una organización como esta, donde los proyectos cambian constantemente.\n\n—¿Cómo manejarías un conflicto con un compañero?\n\n—Escucharía su punto de vista sin interrumpir, identificaría el origen del desacuerdo y buscaría una solución para ambos. Si no lo consiguiéramos, pediría mediación.\n\n—Buena respuesta. La convivencia en equipo es clave aquí.\n\n—Muchas gracias. Lo tendré en cuenta.\n\n—De acuerdo. ¿Tienes alguna pregunta para mí?'
            ),
        ],
    },
}

def apply_replacements(tx_id, pairs, label):
    tx = TX.objects.get(id=tx_id)
    cuerpo = tx.cuerpo
    cambios = 0
    for old, new in pairs:
        if old in cuerpo:
            cuerpo = cuerpo.replace(old, new, 1)
            cambios += 1
        else:
            print(f"  [WARN] id={tx_id} ({label}): no encontrado: {old[:70]!r}")
    return tx, cuerpo, cambios

print()
print("=" * 78)
print("  FIX CIERRE C1 - DRY-RUN")
print("=" * 78)

plan = []
for tx_id, cfg in REPLACEMENTS.items():
    tx, cuerpo_new, cambios = apply_replacements(tx_id, cfg["pairs"], cfg["label"])
    w_old = wc(tx.cuerpo)
    w_new = wc(cuerpo_new)
    ok = MIN_W <= w_new <= MAX_W
    found_all = (cambios == len(cfg["pairs"]))
    plan.append((tx, cuerpo_new, cambios, w_old, w_new, ok, found_all))
    estado = "OK" if ok and found_all else ("FUERA" if not ok else "PARCIAL")
    print(f"\n  id={tx_id:>3} [{cfg['label']}]")
    print(f"    {w_old}w -> {w_new}w  ({w_new - w_old:+d})  "
          f"reemplazos={cambios}/{len(cfg['pairs'])}  [{estado}]")

todo_ok = all(p[5] and p[6] for p in plan)
print()
if todo_ok:
    print("  [OK] Los 5 textos quedan en rango y todos los reemplazos se encontraron")
else:
    print("  [WARN] Revisar avisos arriba antes de aplicar")

if "--apply" not in sys.argv:
    print("\n  DRY-RUN. Nada modificado.")
    print("  Ejecuta con --apply para escribir.")
    if not todo_ok:
        sys.exit(1)
    sys.exit(0)

if not todo_ok:
    print("\n  [STOP] No se aplica nada porque hay avisos.")
    sys.exit(1)

print()
print("=" * 78)
print("  APLICAR")
print("=" * 78)

with transaction.atomic():
    for tx, cuerpo_new, cambios, w_old, w_new, ok, _ in plan:
        if cuerpo_new != tx.cuerpo:
            tx.cuerpo = cuerpo_new
            tx.save(update_fields=["cuerpo"])
            print(f"  [OK] id={tx.id:>3}  {w_old}w -> {w_new}w")

print()
print("=" * 78)
print("  VERIFICACION FINAL C1")
print("=" * 78)

textos = list(TX.objects.filter(nivel_mcer="C1").order_by("id"))
en_rango = 0
for t in textos:
    w = wc(t.cuerpo)
    ok = MIN_W <= w <= MAX_W
    en_rango += int(ok)
    print(f"  [{'OK ' if ok else 'FUERA'}] id={t.id:>3}  {w:>4}w  {t.titulo[:55]}")

print(f"\n  En rango {MIN_W}-{MAX_W}: {en_rango}/{len(textos)}")
if en_rango == len(textos):
    print(f"\n  [OK] FASE 1 C1 COMPLETA")
else:
    print(f"\n  [WARN] {len(textos) - en_rango} textos aun fuera de rango.")