"""_map_tecnicas_textos_a1.py - Fase 2: redistribuir 100 técnicas entre 10 textos.

Objetivo: 10 técnicas por texto, sin sobrecarga.

Estrategia:
  - P1 (Localizar): funciona con cualquier texto → round-robin
  - P2 (Inferir): requiere texto con emociones → prioriza narrativos
  - P3 (Reconocer): requiere estructura clara → prioriza descriptivos
  - P4 (Distinguir): requiere pares opuestos → prioriza los que tienen contrastes

Modo: DRY-RUN por defecto. --apply para escribir.
"""
import os, sys, argparse
from pathlib import Path
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--apply", action="store_true")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_retorica.settings.dev"
import django; django.setup()
from django.apps import apps
from django.db import transaction

TL = apps.get_model("core", "TecnicaLectura")
EJ = apps.get_model("core", "EjercicioLectura")
TX = apps.get_model("core", "Texto")

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

# ═══════════════════════════════════════════════════════════════
header("A", "ESTADO ACTUAL")
# ═══════════════════════════════════════════════════════════════

textos = list(TX.objects.filter(nivel_mcer="A1").order_by("orden", "id"))
print(f"  Textos A1: {len(textos)}")
for t in textos:
    print(f"  id={t.id:>3}  {t.titulo[:40]:<40}")

tecnicas = list(TL.objects.filter(nivel_mcer="A1").order_by("numero"))
print(f"\n  Técnicas A1: {len(tecnicas)}")

# Mapeo actual: técnica → texto
actual = {}
for ej in EJ.objects.filter(tecnica__nivel_mcer="A1").values("tecnica_id", "texto_id"):
    if ej["tecnica_id"] and ej["texto_id"]:
        actual[ej["tecnica_id"]] = ej["texto_id"]

por_texto = defaultdict(list)
for tid, txid in actual.items():
    por_texto[txid].append(tid)

print(f"\n  Distribución actual:")
for t in textos:
    n = len(por_texto.get(t.id, []))
    print(f"    id={t.id:>3}  {t.titulo[:35]:<35}  {n:>3} técnicas")

# ═══════════════════════════════════════════════════════════════
header("B", "PLAN DE REDISTRIBUCIÓN")
# ═══════════════════════════════════════════════════════════════

# Clasificar textos por tipo para asignación semántica
textos_por_tipo = defaultdict(list)
for t in textos:
    textos_por_tipo[t.tipo or "otro"].append(t)

print(f"  Textos por tipo:")
for tipo, lista in textos_por_tipo.items():
    print(f"    {tipo:<12} {len(lista)}  {[t.id for t in lista]}")

# Clasificar técnicas por proceso
tecnicas_por_proceso = defaultdict(list)
for t in tecnicas:
    tecnicas_por_proceso[t.proceso].append(t)

print(f"\n  Técnicas por proceso:")
for proc in ("P1", "P2", "P3", "P4"):
    print(f"    {proc}: {len(tecnicas_por_proceso[proc])}")

# Asignación: distribución round-robin equilibrada
# P1: cualquier texto (round-robin simple)
# P2: narrativos primero (emociones), luego resto
# P3: descriptivos primero (estructura), luego resto
# P4: narrativos + opinion (contrastes), luego resto

def prioridad_textos(proceso):
    """Devuelve el orden de textos a preferir para un proceso."""
    if proceso == "P2":
        orden = ["narrativo", "dialogo", "descriptivo", "opinion", "instructivo", "otro"]
    elif proceso == "P3":
        orden = ["descriptivo", "instructivo", "narrativo", "dialogo", "opinion", "otro"]
    elif proceso == "P4":
        orden = ["narrativo", "opinion", "dialogo", "descriptivo", "instructivo", "otro"]
    else:  # P1
        orden = ["descriptivo", "narrativo", "dialogo", "instructivo", "opinion", "otro"]
    result = []
    for tipo in orden:
        result.extend(textos_por_tipo.get(tipo, []))
    return result

# Contador de técnicas por texto (para equilibrado)
contador = defaultdict(int)
plan = []  # (tecnica, texto_nuevo)

for proc in ("P1", "P2", "P3", "P4"):
    orden_textos = prioridad_textos(proc)
    for i, tec in enumerate(tecnicas_por_proceso[proc]):
        # elegir el texto con menos carga, respetando prioridad
        # entre los primeros 3 en prioridad
        candidatos = orden_textos[:max(3, len(orden_textos) // 2)]
        texto_elegido = min(candidatos, key=lambda t: (contador[t.id], orden_textos.index(t)))
        plan.append((tec, texto_elegido))
        contador[texto_elegido.id] += 1

# Mostrar plan
print(f"\n  Distribución propuesta:")
for t in textos:
    n = contador[t.id]
    status = "OK" if n <= 15 else f"SOBRECARGA ({n})"
    print(f"    id={t.id:>3}  {t.titulo[:35]:<35}  {n:>3} técnicas  [{status}]")

# ═══════════════════════════════════════════════════════════════
header("C", "DETALLE (primeras 20 asignaciones)")
# ═══════════════════════════════════════════════════════════════
for tec, tx in plan[:20]:
    print(f"  técnica #{tec.numero:>3} [{tec.proceso}] → texto {tx.id} '{tx.titulo[:30]}'")

# ═══════════════════════════════════════════════════════════════
header("D", "APLICAR" if args.apply else "DRY-RUN")
# ═══════════════════════════════════════════════════════════════

if not args.apply:
    print("  DRY-RUN. Nada modificado.")
    print("  Ejecuta con --apply para reasignar técnicas a textos.")
    print(f"\n  Cambios a aplicar: {len(plan)} asignaciones")
    print(f"  Textos afectados: {len([t for t in textos if contador[t.id] > 0])}")
    sys.exit(0)

# Aplicar: actualizar texto_id de cada ejercicio de la técnica
with transaction.atomic():
    actualizados = 0
    for tec, tx in plan:
        n = EJ.objects.filter(tecnica=tec, texto__isnull=False).update(texto=tx)
        actualizados += n
    print(f"\n  [OK] {actualizados} ejercicios reasignados")

# Verificar
header("E", "VERIFICAR")
por_texto_final = defaultdict(int)
for ej in EJ.objects.filter(tecnica__nivel_mcer="A1").values("tecnica_id", "texto_id"):
    if ej["tecnica_id"] and ej["texto_id"]:
        por_texto_final[ej["texto_id"]] += 1

print(f"  Distribución final:")
sobrecargados = 0
for t in textos:
    n = por_texto_final.get(t.id, 0)
    status = "OK" if n <= 15 else f"SOBRECARGA ({n})"
    if n > 15: sobrecargados += 1
    print(f"    id={t.id:>3}  {t.titulo[:35]:<35}  {n:>3} técnicas  [{status}]")

if sobrecargados == 0:
    print(f"\n  [OK] FASE 2 COMPLETA — sin sobrecarga")
else:
    print(f"\n  [WARN] {sobrecargados} textos aún sobrecargados")