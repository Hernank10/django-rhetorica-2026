from pathlib import Path
import re
root = Path(r"E:\02_proyectos\django-rhetorica\core\templates")
fixed = []
for p in root.rglob("*.html"):
    c = p.read_text(encoding="utf-8")
    if "{% extends" not in c:
        continue
    orig = c
    # separar lineas
    lines = c.splitlines(keepends=True)
    load_i18n = None
    extends_idx = None
    for i, line in enumerate(lines[:5]):
        s = line.strip()
        if s.startswith("{% extends"):
            extends_idx = i
        if s == "{% load i18n %}":
            load_i18n = i
    # si load esta antes de extends -> mover
    if load_i18n is not None and extends_idx is not None and load_i18n < extends_idx:
        lines.pop(load_i18n)
        # recolocar extends_idx si se movio
        new_ext = None
        for i, line in enumerate(lines[:5]):
            if line.strip().startswith("{% extends"):
                new_ext = i
                break
        lines.insert(new_ext + 1, "{% load i18n %}\n")
        c = "".join(lines)
    if c != orig:
        p.write_text(c, encoding="utf-8")
        fixed.append(str(p.relative_to(root)))
print(f"[OK] Templates arreglados: {len(fixed)}")
for f in fixed:
    print(f"  - {f}")