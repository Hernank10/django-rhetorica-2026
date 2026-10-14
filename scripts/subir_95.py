"""A5: subir cobertura minima del CI de 90 a 95."""
from pathlib import Path

BASE = Path(r"E:\02_proyectos\django-rhetorica")
wf = BASE / ".github" / "workflows" / "tests.yml"
c = wf.read_text(encoding="utf-8")

if "--cov-fail-under=95" in c:
    print("[SKIP] ya estaba en 95")
elif "--cov-fail-under=90" in c:
    c = c.replace("--cov-fail-under=90", "--cov-fail-under=95")
    wf.write_text(c, encoding="utf-8")
    print("[OK] subido de 90 a 95 en CI")
else:
    print("[!] No se encontro --cov-fail-under")