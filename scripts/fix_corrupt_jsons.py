"""Fix quirurgico: psicolinguistica.json + semiotica.json."""
import json
import os
import re
from pathlib import Path

APPLY = os.environ.get("POPULATE_APPLY", "0") == "1"
DATA = Path(r"E:\02_proyectos\django-rhetorica\data")

FIXES = {
    "psicolinguistica.json": [
        # Cierre de objeto duplicado: "}, \n }, \n {" -> "}, \n {"
        (r"(\},\s*)\},\s*(\{)", r"\1\2", 1),
    ],
    "semiotica.json": [
        # String de ejemplo roto: "texto" (aclaracion). -> "texto (aclaracion).",
        (
            r'("ejemplo"\s*:\s*")([^"]*?)("\s*)\(([^)]*)\)\.(\s*)',
            r'\1\2 (\4).",\5',
            1,
        ),
    ],
}

for fname, fixes in FIXES.items():
    path = DATA / fname
    print("=" * 72)
    print(fname)
    print("=" * 72)

    original = path.read_text(encoding="utf-8", errors="replace")
    try:
        json.loads(original)
        print("[OK] ya carga: %d items" % len(json.loads(original)))
        continue
    except json.JSONDecodeError as e:
        print("[BROKEN] %s @line %d char %d" % (e.msg, e.lineno, e.pos))

    fixed = original
    for i, (pat, rep, count) in enumerate(fixes, 1):
        nuevo = re.sub(pat, rep, fixed, count=count)
        if nuevo != fixed:
            print("[FIX %d] aplicado (delta %d bytes)" % (i, len(fixed) - len(nuevo)))
            fixed = nuevo
        else:
            print("[FIX %d] no matcheo" % i)

    try:
        data = json.loads(fixed)
        n = len(data)
        status = "[OK]" if n == 100 else "[WARN] %d items" % n
        print("  %s tras fix: %d items" % (status, n))
    except json.JSONDecodeError as e:
        print("  [FAIL] aun roto: %s @line %d" % (e.msg, e.lineno))
        ctx = fixed[max(0, e.pos-80):e.pos+80]
        pos_rel = e.pos - max(0, e.pos-80)
        print("  Contexto: ...%s<ERR>%s..." % (ctx[:pos_rel], ctx[pos_rel:]))
        continue

    # Diff minimo
    for j in range(min(len(original), len(fixed))):
        if original[j] != fixed[j]:
            print("  Diff @char %d:" % j)
            print("    antes: %r" % original[max(0,j-60):j+60])
            print("    ahora: %r" % fixed[max(0,j-60):j+60])
            break

    if APPLY:
        bak = path.with_suffix(path.suffix + ".bak")
        if not bak.exists():
            bak.write_text(original, encoding="utf-8")
            print("  [BACKUP] %s" % bak.name)
        path.write_text(fixed, encoding="utf-8")
        print("  [APPLIED] %s" % fname)
    else:
        print("  [DRY_RUN] sin cambios")

print()
if APPLY:
    print("[OK] Fase APPLY completada")
else:
    print("[DRY_RUN] aplicar: $env:POPULATE_APPLY='1'; rerun")