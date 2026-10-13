from pathlib import Path
p = Path(r"E:\02_proyectos\django-rhetorica\.pre-commit-config.yaml")
c = p.read_text(encoding="utf-8")

if "_deprecated" not in c:
    c = c.replace(
        "    ejercicios_completos-lengua-castellana/|",
        "    ejercicios_completos-lengua-castellana/|\n    scripts/_deprecated/|",
        1,
    )
    p.write_text(c, encoding="utf-8")
    print("[OK] agregada exclusion scripts/_deprecated/")
else:
    print("[SKIP] ya estaba")
