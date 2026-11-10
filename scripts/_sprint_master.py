"""_sprint_master.py - Orquestador del sprint de contenido por nivel.

Lee docs/plan_<nivel>.json (generado por _diag_b1_plan.py) y ejecuta
las fases necesarias en orden, llamando a los sub-scripts parametrizados
por --nivel.

Fases (en orden):
  F1  -> _seed_textos_<nivel>.py      (solo si plan.f1_textos.necesario)
  F2  -> _map_tecnicas_textos_a2.py   (si plan.f2_mapeo.necesario)
  F3a -> _migrar_explicacion_a2.py    (si plan.f3a_explicacion.necesario)
  F3b -> _densificar_<nivel>.py       (si plan.f3b_densificar.necesario)
  F3c -> _fix_tildes_a2.py + extra + p3 (si plan.f3c_tildes.necesario)
  F4  -> _diag_<nivel>_plan.py        (verificacion final, read-only)

Uso:
    python scripts/_sprint_master.py --nivel B1                    # DRY-RUN
    python scripts/_sprint_master.py --nivel B1 --apply            # ejecuta todo
    python scripts/_sprint_master.py --nivel B1 --phase f1         # solo una fase
    python scripts/_sprint_master.py --nivel B1 --skip-f3b --apply # saltar densificar
"""
import os, sys, json, subprocess, argparse, time
from pathlib import Path
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--nivel", default="B1")
parser.add_argument("--apply", action="store_true", help="Aplica los cambios (sin esto, DRY-RUN)")
parser.add_argument("--phase", default=None, choices=["f1","f2","f3a","f3b","f3c","f4"],
                    help="Ejecutar solo esta fase")
parser.add_argument("--skip-f1", action="store_true")
parser.add_argument("--skip-f2", action="store_true")
parser.add_argument("--skip-f3a", action="store_true")
parser.add_argument("--skip-f3b", action="store_true")
parser.add_argument("--skip-f3c", action="store_true")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
sys.path.insert(0, str(ROOT))

PYTHON = sys.executable
NIVEL = args.nivel.upper()
JSON_PATH = ROOT / "docs" / f"plan_{NIVEL.lower()}.json"

def header(n, t):
    print(); print("=" * 78); print(f"[{n}] {t}"); print("=" * 78)

def run(cmd, dry_run=False):
    """Ejecuta un comando y devuelve (ok, output)."""
    if dry_run:
        print(f"  [DRY-RUN] {' '.join(str(c) for c in cmd)}")
        return True, ""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        out = result.stdout + result.stderr
        # Mostrar solo las ultimas lineas importantes
        lines = out.strip().split("\n")
        for line in lines[-15:]:
            print(f"  {line}")
        return result.returncode == 0, out
    except subprocess.TimeoutExpired:
        print("  [TIMEOUT] comando excedio 10 min")
        return False, ""
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False, ""

# ─── Cargar plan ──────────────────────────────────────────
header("A", f"SPRINT MAESTRO - NIVEL {NIVEL}")

if not JSON_PATH.exists():
    print(f"  [ERROR] No existe {JSON_PATH}")
    print(f"  Ejecuta primero: python scripts/_diag_b1_plan.py --nivel {NIVEL} --json")
    sys.exit(1)

with JSON_PATH.open("r", encoding="utf-8") as f:
    plan_json = json.load(f)

print(f"  Plan cargado: {JSON_PATH}")
print(f"  Veredicto:    {plan_json['veredicto']['tipo_sprint']} - {plan_json['veredicto']['razon']}")
print(f"  Modo:         {'APLICAR' if args.apply else 'DRY-RUN'}")

plan = plan_json["plan"]

# ─── Definir fases ────────────────────────────────────────
FASES = []

# F1
if plan["f1_textos"]["necesario"] and not args.skip_f1:
    FASES.append({
        "id": "f1", "nombre": "F1 - Textos (reescribir fuera rango + crear nuevos)",
        "script": f"_seed_textos_{NIVEL.lower()}.py",
        "extra": ["--apply"] if args.apply else [],
        "dryrun_ok": True,
    })

# F2
if plan["f2_mapeo"]["necesario"] and not args.skip_f2:
    FASES.append({
        "id": "f2", "nombre": "F2 - Mapeo técnicas a textos",
        "script": "_map_tecnicas_textos_a2.py",
        "extra": ["--nivel", NIVEL] + (["--apply"] if args.apply else []),
    })

# F3a
if plan["f3a_explicacion"]["necesario"] and not args.skip_f3a:
    FASES.append({
        "id": "f3a", "nombre": "F3a - Añadir explicación a los ejercicios",
        "script": "_migrar_explicacion_a2.py",
        "extra": ["--nivel", NIVEL] + (["--apply"] if args.apply else []),
    })

# F3b
if plan["f3b_densificar"]["necesario"] and not args.skip_f3b:
    FASES.append({
        "id": "f3b", "nombre": "F3b - Densificar (ratio 1.00 -> 2.00)",
        "script": f"_densificar_{NIVEL.lower()}.py",
        "extra": ["--nivel", NIVEL] + (["--apply"] if args.apply else []),
    })

# F3c (3 scripts de tildes)
if plan["f3c_tildes"]["necesario"] and not args.skip_f3c:
    FASES.append({
        "id": "f3c", "nombre": "F3c - Tildes (3 pasadas)",
        "scripts": [
            "_fix_tildes_a2.py",
            "_fix_tildes_a2_extra.py",
            "_fix_tildes_a2_p3.py",
        ],
        "extra": ["--nivel", NIVEL] + (["--apply"] if args.apply else []),
    })

# F4 (siempre al final)
FASES.append({
    "id": "f4", "nombre": "F4 - Verificación final",
    "script": "_diag_b1_plan.py",
    "extra": ["--nivel", NIVEL],
    "readonly": True,
})

# ─── Filtrar por --phase ──────────────────────────────────
if args.phase:
    FASES = [f for f in FASES if f["id"] == args.phase]
    if not FASES:
        print(f"\n  [WARN] Fase {args.phase} no necesaria o ya saltada")
        sys.exit(0)

# ─── Ejecutar ─────────────────────────────────────────────
header("B", f"EJECUTANDO {len(FASES)} FASE(S)")

inicio = time.time()
resultados = []

for i, fase in enumerate(FASES, 1):
    print(f"\n[{i}/{len(FASES)}] {fase['nombre']}")
    print("-" * 78)

    scripts = fase.get("scripts") or [fase["script"]]
    fase_ok = True

    for script_name in scripts:
        script_path = ROOT / "scripts" / script_name
        if not script_path.exists():
            print(f"  [ERROR] No existe {script_path}")
            fase_ok = False
            break
        cmd = [PYTHON, str(script_path)] + fase["extra"]
        ok, _ = run(cmd, dry_run=not args.apply)
        if not ok:
            fase_ok = False
            break

    resultados.append({"fase": fase["id"], "ok": fase_ok})
    print(f"  -> {fase['id'].upper()}: {'OK' if fase_ok else 'FALLO'}")

    if not fase_ok and not fase.get("readonly"):
        print(f"\n  [STOP] Fase {fase['id']} fallo. Deteniendo sprint.")
        break

# ─── Resumen ──────────────────────────────────────────────
duracion = time.time() - inicio

header("C", "RESUMEN DEL SPRINT")

print(f"  Duracion: {duracion:.1f}s")
print(f"  Modo:     {'APLICAR' if args.apply else 'DRY-RUN'}")
print(f"\n  Fases ejecutadas:")
for r in resultados:
    print(f"    [{r['fase']:>3}] {'OK' if r['ok'] else 'FALLO'}")

ok_total = all(r["ok"] for r in resultados)

if args.apply:
    if ok_total:
        print(f"\n  [OK] SPRINT {NIVEL} COMPLETO")
        print(f"\n  Proximo paso: verificar con _diag_b1_plan.py --nivel {NIVEL}")
        print(f"  Si sale COMPLETO, hacer commit + tag")
    else:
        print(f"\n  [WARN] Sprint con fallos. Revisar output arriba.")
else:
    print(f"\n  DRY-RUN. Para aplicar: python scripts/_sprint_master.py --nivel {NIVEL} --apply")

print()